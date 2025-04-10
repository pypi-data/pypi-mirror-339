from .pnne_estimate import *
import os
import numpy as np

def load_example_data():
    base_dir = os.path.dirname(__file__)
    return np.load(os.path.join(base_dir, 'data.npz'))

__version__ = "0.1.0"