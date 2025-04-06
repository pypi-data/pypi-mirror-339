"""
Nexri - Advanced Layers for TensorFlow Keras
============================================

Nexri provides specialized neural network layers that extend TensorFlow's
capabilities with optimized implementations for advanced modeling techniques.

Main Components
--------------
* dense: Quadratic Penalty Dense layer with integrated batch normalization
"""

__version__ = "0.1.0"

# Import and expose the main components
from .dense import QPDense

# Make these classes available at the package level
__all__ = ['QPDense']
