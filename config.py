from logging import Handler
from Json_Handler import save_to_json
import numpy as np
# --- Radar Hardware & Waveform ---
C = 3e8                      # Speed of light (m/s)
FC = 10e9                    # 10 GHz (X-band)
LAMBDA = C / FC              # Wavelength (0.03 meters)
B = 150e6                    # Bandwidth (150 MHz)
TC = 2e-3                    # Chirp time (2ms)
SLOPE = B / TC               # Chirp slope (Hz/s)

# --- Sampling & Resolution ---
FS = 2.5e6                   # Sampling rate (2.5 MHz)
N_SAMPLES = int(FS * TC)     # Number of samples per chirp (5000 samples)
R_MAX = 150000               # Max range (150 KM)
RANGE_RES = C / (2 * B)      # Range resolution (1.0 meter)

# --- Target Specs ---
MIN_RCS = 0.01               # Stealth target RCS (m^2)
BOLTZMANN = 1.38e-23         # Boltzmann constant
