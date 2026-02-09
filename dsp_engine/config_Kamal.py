# config.py
import numpy as np

# --- 1. HARDWARE SPECS (The Physics) ---
FS = 3.5e9                   # 3.5 GHz Sampling (High Fidelity)
TC = 50e-6                   # 50 us Chirp Time
B = 150e6                    # 150 MHz Bandwidth
C = 3e8                      # Speed of Light
FC = 10e9                    # 10 GHz Carrier
N_CHIRPS = 128               # Number of chirps

# --- 2. USER SETTINGS (The Constraints) ---
MAX_RANGE_WANTED = 5000      # 5 km (The "Crop" Limit)

# --- 3. DERIVED CONSTANTS (Auto-calculated) ---
LAMBDA = C / FC
SLOPE = B / TC
N_SAMPLES = int(FS * TC)     # 175,000 samples

# Calculate how many FFT bins we need to keep for 5km
# Formula: Index = (Freq * N) / FS
max_beat_freq = (SLOPE * 2 * MAX_RANGE_WANTED) / C
STOP_INDEX = int((max_beat_freq * N_SAMPLES) / FS) + 50