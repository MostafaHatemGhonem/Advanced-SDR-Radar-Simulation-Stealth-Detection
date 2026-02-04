import numpy as np
import matplotlib.pyplot as plt
import sys
import os
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

import config


# ============= transmitted signal =============
B = config.B
TC = config.TC
FC = config.FC
FS = config.FS
N_SAMPLES = config.N_SAMPLES

# define the t as an array
t = np.linspace(0,TC,N_SAMPLES)

tx_signal = np.cos(2 * np.pi * ((FC * t) + ((B * t**2) / (2 * TC))))




# ============= received signal =============
B = config.B
TC = config.TC
FC = config.FC
FS = config.FS
N_SAMPLES = config.N_SAMPLES
c = config.C

target_dist = 150     # Target is 30 meters away
td = 2 * target_dist / c  # Round trip delay

# define the t as an array
t = np.linspace(0,TC,N_SAMPLES)

t_delay = t - td

rx_signal = np.where(t >= td,
                    np.cos(2 * np.pi * ((FC * (t-td) + ((B * (t-td)**2) / (2 * TC))))),
                    0)




# ============= transmitted signal plotting =============
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# 1. Time Domain (The Waveform)
ax1.set_title("Chirp tx (Time Domain)")
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






# ============= received signal plotting =============
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# 1. Time Domain (The Waveform)
ax1.set_title("Chirp rx (Time Domain)")
ax1.plot(t[:200], rx_signal[:200], color='blue') # Zoom in on first 100 samples
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Amplitude")
ax1.grid(True)

# 2. Frequency Domain (Spectrogram)
# This proves the frequency is actually climbing over time
ax2.set_title("Spectrogram (Frequency vs. Time)")
ax2.specgram(rx_signal, Fs=FS, cmap='inferno')
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Frequency (Hz)")



# ============= 2 signal comparison plotting =============
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# 1. Time Domain (The Waveform)
ax1.set_title("Chirp comparison (Time Domain)")
ax1.plot(t[:200], rx_signal[:200], color='blue') # Zoom in on first 100 samples
ax1.plot(t[:200], tx_signal[:200], color='firebrick') # Zoom in on first 100 samples
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Amplitude")
ax1.grid(True)

# 2. Frequency Domain (Spectrogram)
# This proves the frequency is actually climbing over time
ax2.set_title("Spectrogram (Frequency vs. Time)")
ax2.specgram(rx_signal, Fs=FS, cmap='inferno')
ax2.specgram(tx_signal, Fs=FS, cmap='inferno')
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Frequency (Hz)")

plt.tight_layout()
plt.show()