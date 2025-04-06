import tensorflow as tf
import numpy as np
import unittest
from nexri.dense import QPDense

class TestQPDense(unittest.TestCase):
    """Test cases for the QPDense layer."""

    def setUp(self):
        """Set up common test resources."""
        tf.random.set_seed(42)  # For reproducibility
        self.input_dim = 10
        self.output_dim = 5
        self.batch_size = 8
        self.inputs = tf.random.normal((self.batch_size, self.input_dim))

    def test_initialization(self):
        """Test that the layer can be initialized properly."""
        layer = QPDense(units=self.output_dim)
        self.assertEqual(layer.units, self.output_dim)
        self.assertEqual(layer.alfa_initial, 1.0)
        self.assertFalse(layer.alfa_trainable)
        self.assertTrue(layer.use_batch_norm)

    def test_build_and_call(self):
        """Test that the layer builds and can be called."""
        layer = QPDense(units=self.output_dim)
        outputs = layer(self.inputs)

        # Check output shape
        self.assertEqual(outputs.shape, (self.batch_size, self.output_dim))

        # Check that weights were created
        self.assertTrue(hasattr(layer, 'kernel'))
        self.assertTrue(hasattr(layer, 'bias'))
        self.assertTrue(hasattr(layer, 'alfa'))

        # Check batch norm was created
        self.assertTrue(hasattr(layer, 'batch_norm'))

    def test_without_batch_norm(self):
        """Test that the layer works without batch normalization."""
        layer = QPDense(units=self.output_dim, use_batch_norm=False)
        outputs = layer(self.inputs)

        # Check output shape
        self.assertEqual(outputs.shape, (self.batch_size, self.output_dim))

        # Ensure batch_norm wasn't created
        self.assertFalse(hasattr(layer, 'batch_norm'))

    def test_trainable_alfa(self):
        """Test that alfa is trainable when specified."""
        layer = QPDense(units=self.output_dim, alfa_trainable=True)

        # Call the layer to build it
        _ = layer(self.inputs)

        # Check if alfa is in trainable_weights
        trainable_weight_names = [w.name for w in layer.trainable_weights]
        self.assertIn('alfa', trainable_weight_names)

        # Alternatively, verify alfa.trainable is True
        self.assertTrue(layer.alfa.trainable)

    def test_serialization(self):
        """Test that the layer can be serialized and deserialized."""
        layer = QPDense(
            units=self.output_dim,
            alfa_initial=0.1,
            alfa_trainable=True,
            use_batch_norm=True,
            batch_norm_momentum=0.95
        )

        # Get config
        config = layer.get_config()

        # Check that our custom params are in the config
        self.assertEqual(config['units'], self.output_dim)
        self.assertEqual(config['alfa_initial'], 0.1)
        self.assertTrue(config['alfa_trainable'])
        self.assertEqual(config['batch_norm_momentum'], 0.95)

        # Create a new layer from config
        new_layer = QPDense.from_config(config)

        # Check the new layer has the same parameters
        self.assertEqual(new_layer.units, self.output_dim)
        self.assertEqual(new_layer.alfa_initial, 0.1)
        self.assertTrue(new_layer.alfa_trainable)
        self.assertEqual(new_layer.batch_norm_momentum, 0.95)

    def test_in_model(self):
        """Test that the layer works in a model."""
        # Create a simple model
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(self.input_dim,)),
            QPDense(self.output_dim, activation='relu'),
            QPDense(1, activation='sigmoid')
        ])

        # Compile the model
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

        # Create dummy data
        x = np.random.random((100, self.input_dim))
        y = np.random.randint(0, 2, (100, 1))

        # Fit for one epoch to test training
        history = model.fit(x, y, epochs=1, verbose=0)

        # Check that training happened (loss changed)
        self.assertTrue('loss' in history.history)

if __name__ == '__main__':
    unittest.main()
