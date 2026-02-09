import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import requests
import json
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
# loading the data from the api
api_response = requests.get("https://548eb008-db08-4d38-a570-a2583a5fa791.mock.pstmn.io/api/radar")
data = api_response.json()

# here we will extract the distance for all the targets then generate a signal of all there additions 
# Initialize a silent Rx signal (all zeros)
rx_signal = np.zeros(len(t))

# looping thro all the targets
for target in data['targets']:
    dist_m = target['distance_km'] * 1000
    td = 2 * dist_m / config.C
    
    # Calculate reflection for THIS specific target
    amplitude = 1 / (dist_m**2) # Basic path loss simulation
    
    reflection = amplitude * np.where(t >= td,
        np.cos(2 * np.pi * (config.FC * (t-td) + (0.5 * config.SLOPE * (t-td)**2))),
        0)
    
    # Add this target's echo to the total signal
    rx_signal += reflection



# ============= mixing the 2 signals =============
# mixing the 2 signals is as simple as multiplying them
beat_signal = rx_signal * tx_signal





# ============= transmitted signal plotting =============
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# 1. Time Domain (The Waveform)
ax1.set_title("tx signal (Time Domain)")
ax1.plot(t[:500], tx_signal[:500], color='firebrick') # Zoom in on first 500 samples
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




# ============= received signal plotting =============
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# 1. Time Domain (The Waveform)
ax1.set_title("rx signal (Time Domain)")
ax1.plot(t[:500], rx_signal[:500], color='blue') # Zoom in on first 500 samples
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Amplitude")
ax1.grid(True)

# 2. Frequency Domain (Spectrogram)
# This proves the frequency is actually climbing over time
ax2.set_title("Spectrogram (Frequency vs. Time)")
ax2.specgram(rx_signal, Fs=FS, cmap='inferno')
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Frequency (Hz)")
plt.tight_layout()





# ============= 2 signal comparison plotting =============
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# 1. Time Domain (The Waveform)
ax1.set_title("signal comparison (Time Domain)")
ax1.plot(t[:500], rx_signal[:500], color='blue') # Zoom in on first 500 samples
ax1.plot(t[:500], tx_signal[:500], color='firebrick') # Zoom in on first 500 samples
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





# ============= beat signal plotting =============
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# 1. Time Domain (The Waveform)
ax1.set_title("beat signal (Time Domain)")
ax1.plot(t[:500], beat_signal[:500], color='firebrick') # Zoom in on first 500 samples
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Amplitude")
ax1.grid(True)

# 2. Frequency Domain (Spectrogram)
# This proves the frequency is actually climbing over time
ax2.set_title("Spectrogram (Frequency vs. Time)")
ax2.specgram(beat_signal, Fs=FS, cmap='inferno')
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Frequency (Hz)")
plt.tight_layout()
plt.show()