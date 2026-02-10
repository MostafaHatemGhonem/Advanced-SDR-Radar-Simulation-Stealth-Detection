# processor.py
import numpy as np
from scipy.fft import fft, fftshift
from scipy.signal import butter, lfilter
import config_Kamal as cfg


def design_filter():
    """
    Creates a Low-Pass Butterworth filter.
    Cutoff: The frequency corresponding to MAX_RANGE_WANTED + buffer.
    """
    # 1. Calculate the Beat Frequency for the Max Range (e.g., 5km -> ~100 MHz)
    # We add a 20% buffer to avoid attenuating the target at the very edge.
    max_freq = (cfg.SLOPE * 2 * cfg.MAX_RANGE_WANTED) / cfg.C
    cutoff_freq = max_freq * 1.2

    # 2. Normalize frequency (Nyquist limit is FS / 2)
    nyquist = 0.5 * cfg.FS
    normal_cutoff = cutoff_freq / nyquist

    # 3. Design Filter coefficients (b, a)
    # Order=6 gives a sharp cutoff (steep slope)
    b, a = butter(N=6, Wn=normal_cutoff, btype='low', analog=False)
    return b, a


def build_range_doppler_map(chirp_stream):
    """
    Consumes stream, Filters (New!), Windows, and performs FFTs.
    """
    compressed_cube = np.zeros((cfg.N_CHIRPS, cfg.STOP_INDEX), dtype=np.complex128)

    # Design the filter once before the loop
    b, a = design_filter()

    # Create Window for FFT
    range_window = np.hanning(cfg.N_SAMPLES)

    print(
        f"[Processor] Filter Configured. Cutoff: {(cfg.SLOPE * 2 * cfg.MAX_RANGE_WANTED * 1.2 / cfg.C) / 1e6:.1f} MHz")

    for i, raw_chirp in enumerate(chirp_stream):
        # --- STEP 1: SCIPY FILTERING (New!) ---
        # Removes high-frequency noise > 120 MHz (for 5km)
        filtered_chirp = lfilter(b, a, raw_chirp)

        # --- STEP 2: WINDOWING ---
        # Tapers edges to reduce side-lobes
        windowed_chirp = filtered_chirp * range_window

        # --- STEP 3: FFT ---
        chirp_fft = fft(windowed_chirp)
        compressed_cube[i, :] = chirp_fft[:cfg.STOP_INDEX]

    # Doppler FFT (Slow Time)
    doppler_window = np.hanning(cfg.N_CHIRPS)[:, np.newaxis]
    doppler_input = compressed_cube * doppler_window

    doppler_fft = fftshift(fft(doppler_input, axis=0), axes=0)

    rd_map = 20 * np.log10(np.abs(doppler_fft) + 1e-9)
    return rd_map


def get_axes():
    # Range Axis
    max_freq_view = (cfg.STOP_INDEX / cfg.N_SAMPLES) * cfg.FS
    max_range_view = (max_freq_view * cfg.C) / (2 * cfg.SLOPE)
    range_axis = np.linspace(0, max_range_view, cfg.STOP_INDEX)

    # Velocity Axis
    max_vel = cfg.LAMBDA / (4 * cfg.TC)
    vel_axis = np.linspace(-max_vel, max_vel, cfg.N_CHIRPS)

    return range_axis, vel_axis