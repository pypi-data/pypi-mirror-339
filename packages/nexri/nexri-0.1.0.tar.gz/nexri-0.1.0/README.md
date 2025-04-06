# Nexri

Nexri provides specialized neural network layers for TensorFlow that extend standard Keras layers with advanced features.

## Installation

```bash
pip install nexri
```

## Features

### QPDense Layer

A Quadratic Penalty Dense layer (QPDense) with integrated batch normalization that offers:

- Quadratic penalty terms that modify the optimization landscape
- Integrated batch normalization for faster convergence
- Built on top of Keras Dense layer for maximum compatibility

The layer computes:

```
output = BatchNorm(2 * (inputs · kernel) - α * (sum(inputs²)) - α * (sum(kernel²)) + bias)
```

Where:
- α (alpha) is a trainable or fixed parameter that controls the strength of the quadratic penalty terms
- BatchNorm applies normalization to stabilize and accelerate training (optional)

## Usage

```python
# Import nexRI advanced dense layer
from nexri import QPDense

# Import regular Tensorflow and Keras components
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Flatten, Activation
from tensorflow.keras.utils import to_categorical

# Load MNIST dataset
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Normalize and reshape
train_images = train_images.reshape((60000, 28, 28, 1)).astype('float32') / 255
test_images = test_images.reshape((10000, 28, 28, 1)).astype('float32') / 255

# Prepare outputs
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# Create a simple model with QPDense layers
model = Sequential([
    Input(shape=(28, 28, 1)),
    Flatten(),
    QPDense(units=128, weight_mean=0.5),
    Activation('relu'),
    QPDense(units=10),
    Activation('softmax'),
])

# Compile and train as usual
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train the model
history = model.fit(train_images,
                    train_labels,
                    epochs=5,
                    batch_size=64,
                    validation_data=(test_images, test_labels),
                    callbacks=[])
```

## Advanced Configuration

The QPDense layer accepts all parameters that a regular Dense layer accepts, plus these additional options:

- `alfa_initial`: Initial value for the alpha parameter (default: 1.0)
- `alfa_trainable`: Whether alpha should be trainable (default: False)
- `weight_mean`: Mean value for the kernel initializer (default: 0.0)
- `use_batch_norm`: Whether to apply batch normalization (default: True)
- `batch_norm_momentum`: Momentum for the batch normalization layer (default: 0.99)
- `batch_norm_epsilon`: Small float added to variance to avoid division by zero (default: 1e-3)

## License

MIT
