import numpy as np
import matplotlib.pyplot as plt
import sys
import os
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

import config




# ============= mathematical implementation =============
B = config.B
TC = config.TC
FC = config.FC
FS = config.FS
N_SAMPLES = config.N_SAMPLES

# define the t as an array
t = np.linspace(0,TC,N_SAMPLES)

tx_signal = np.cos(2 * np.pi * ((FC * t) + ((B * t**2) / (2 * TC))))








# ============= plotting =============
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# 1. Time Domain (The Waveform)
ax1.set_title("Chirp (Time Domain)")
ax1.plot(t[:100], tx_signal[:100], color='firebrick') # Zoom in on first 100 samples
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Amplitude")
ax1.grid(True)

# 2. Frequency Domain (Spectrogram)
# This proves the frequency is actually climbing over time
ax2.set_title("Spectrogram (Frequency vs. Time)")
ax2.specgram(tx_signal, Fs=FS, cmap='inferno')
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Frequency (Hz)")

plt.tight_layout()
plt.show()