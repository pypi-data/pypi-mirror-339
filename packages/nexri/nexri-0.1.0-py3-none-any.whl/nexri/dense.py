import tensorflow as tf

class QPDense(tf.keras.layers.Dense):
    """
    Quadratic Penalty Dense Layer (QPDense) with Batch Normalization

    This layer extends the standard Dense layer with quadratic penalty terms
    and integrated batch normalization, minimizing the amount of custom code needed.

    The layer computes:
    # Forward pass:

    output = BatchNorm(2 * (inputs · kernel) - α * (sum(inputs²)) - α * (sum(kernel²)) + bias)

    - where α (alpha) is a trainable or fixed parameter that controls the strength of the
      quadratic penalty terms.
    - BatchNorm applies normalization to stabilize and accelerate training (optional)

    # Backpropagation:

    - gradient of output with respect to input:           ∂y/∂x = 2W - 2αx
    - gradient of output with respect to kernel weights:  ∂y/∂W = 2x - 2αW
    - gradient of output with respect to alpha:           ∂y/∂α = -sum(x²) - sum(W²)
    - gradient of output with respect to bias:            ∂y/∂b = 1

    Args:
        units (int): Positive integer, dimensionality of the output space.
        alfa_initial (float): Initial value for the alfa parameter. Default is 1.0.
        alfa_trainable (bool): Whether alfa should be trainable. Default is False.
        weight_mean (float): Mean value for the kernel initializer. Default is 0.0.
        use_batch_norm (bool): Whether to apply batch normalization. Default is True.
        batch_norm_momentum (float): Momentum for the batch normalization layer. Default is 0.99.
        batch_norm_epsilon (float): Small float added to variance to avoid division by zero. Default is 1e-3.
        **kwargs: Additional keyword arguments passed to the Dense superclass.
    """

    def __init__(self, units=32,
                 alfa_initial=1.0,
                 alfa_trainable=False,
                 weight_mean=0.0,
                 use_batch_norm=True,
                 batch_norm_momentum=0.99,
                 batch_norm_epsilon=1e-3,
                 **kwargs):
        # Initialize the Dense layer with custom kernel initializer
        if 'kernel_initializer' not in kwargs:
            kwargs['kernel_initializer'] = tf.keras.initializers.RandomNormal(
                mean=weight_mean,
                stddev=0.05
            )

        # Pass units and kwargs to Dense class
        super(QPDense, self).__init__(
            units=units,
            **kwargs
        )

        # Store QPDense specific parameters
        self.alfa_initial = alfa_initial
        self.alfa_trainable = alfa_trainable
        self.weight_mean = weight_mean
        self.use_batch_norm = use_batch_norm
        self.batch_norm_momentum = batch_norm_momentum
        self.batch_norm_epsilon = batch_norm_epsilon

    def build(self, input_shape):
        # Call Dense's build method to create kernel and bias
        super(QPDense, self).build(input_shape)

        # Add alfa parameter (not in Dense by default)
        self.alfa = self.add_weight(
            name='alfa',
            shape=(self.units,),
            initializer=tf.keras.initializers.Constant(value=self.alfa_initial),
            trainable=self.alfa_trainable,
        )

        # Create batch normalization layer if enabled
        if self.use_batch_norm:
            self.batch_norm = tf.keras.layers.BatchNormalization(
                momentum=self.batch_norm_momentum,
                epsilon=self.batch_norm_epsilon,
                name='batch_norm'
            )
            # Build the batch norm layer with the correct output shape
            self.batch_norm.build((None, self.units))

    def call(self, inputs, training=None):
        """Forward pass with quadratic penalty logic and batch normalization."""
        # Variables that will be used in the custom gradient function
        kernel = self.kernel
        bias = self.bias
        alfa = self.alfa
        units = self.units

        @tf.custom_gradient
        def custom_op(x, w_arg, b_arg, alfa_arg, variables=None):
            # Pre-compute squared terms
            x_squared = tf.square(x)
            w_squared = tf.square(w_arg)

            # Calculate summations efficiently
            input_sq = tf.reduce_sum(x_squared, axis=1, keepdims=True)  # [batch_size, 1]
            kernel_sq = tf.reduce_sum(w_squared, axis=0)  # [units]

            # Matrix multiplication (main operation from Dense)
            xw = tf.matmul(x, w_arg)

            # Prepare for broadcasting
            alfa_expanded = tf.expand_dims(alfa_arg, 0)  # [1, units]
            kernel_sq_expanded = tf.expand_dims(kernel_sq, 0)  # [1, units]

            # Compute output with quadratic penalties
            out = 2 * xw - (input_sq * alfa_expanded + kernel_sq_expanded * alfa_expanded) + b_arg

            def grad(dy, variables=None):
                # Gradient calculations
                w_transposed = tf.transpose(w_arg)

                # Gradient for input x
                grad_x = 2 * tf.matmul(dy, w_transposed)
                alfa_for_x = tf.reshape(alfa_arg, [1, -1])
                penalty_sum = tf.reduce_sum(dy * alfa_for_x, axis=1, keepdims=True)
                grad_x -= 2 * x * penalty_sum

                # Gradient for weights w
                grad_w = 2 * tf.matmul(tf.transpose(x), dy)
                dy_sum = tf.reduce_sum(dy, axis=0)
                grad_w -= 2 * w_arg * tf.reshape(dy_sum * alfa_arg, [1, units])

                # Gradient for bias b
                grad_b = tf.reduce_sum(dy, axis=0)

                # Gradient for alfa
                grad_alfa = -tf.reduce_sum(dy * (input_sq + kernel_sq_expanded), axis=0)

                return grad_x, grad_w, grad_b, grad_alfa

            return out, grad

        # Use the custom operation with our weights
        output = custom_op(inputs, kernel, bias, alfa)

        # Apply batch normalization if enabled
        if self.use_batch_norm:
            output = self.batch_norm(output, training=training)

        return output

    def get_config(self):
        """Returns the configuration of the layer."""
        # Get base config from Dense
        base_config = super(QPDense, self).get_config()

        # Add QPDense specific config
        qp_config = {
            'alfa_initial': self.alfa_initial,
            'alfa_trainable': self.alfa_trainable,
            'weight_mean': self.weight_mean,
            'use_batch_norm': self.use_batch_norm,
            'batch_norm_momentum': self.batch_norm_momentum,
            'batch_norm_epsilon': self.batch_norm_epsilon,
        }

        # If kernel_initializer was set based on weight_mean, remove it to avoid duplication
        if isinstance(base_config.get('kernel_initializer'), dict):
            kernel_init = base_config['kernel_initializer']
            if kernel_init.get('class_name') == 'RandomNormal' and \
               kernel_init.get('config', {}).get('mean') == self.weight_mean and \
               kernel_init.get('config', {}).get('stddev') == 0.05:
                base_config.pop('kernel_initializer', None)

        # Combine configs
        return {**base_config, **qp_config}

    @classmethod
    def from_config(cls, config):
        """Creates a layer from its config."""
        return cls(**config)

# Register the custom layer for serialization
tf.keras.utils.get_custom_objects()['QPDense'] = QPDense
