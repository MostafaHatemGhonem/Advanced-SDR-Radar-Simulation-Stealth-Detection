import numpy as np
from scipy.signal import windows


def apply_hamming(signal):
    
    window = windows.hamming(len(signal))
    return signal * window
