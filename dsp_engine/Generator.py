# generator.py
import numpy as np
import config_Kamal as cfg  # Imports constants from file 1


def stream_raw_chirps():
    """
    Yields ONE raw chirp (Time Domain) at a time.
    Simulates Path Loss (1/R^4) for realistic signal strength.
    """
    t = np.linspace(0, cfg.TC, cfg.N_SAMPLES, endpoint=False)

    # Define Targets [Range(m), Velocity(m/s), RCS(m^2)]
    # RCS = Radar Cross Section (Size of target). Car ~ 10, Person ~ 1.
    targets = [
        (100, 0, 10.0),  # Wall (Close, Big)
        (2000, 30, 5.0),  # Car (Mid range, medium size)
        (4500, -60, 20.0),  # Truck (Far, Huge size)
        (6000,60,30.0)
    ]

    print(f"[Generator] Simulating {len(targets)} targets with Path Loss...")

    for m in range(cfg.N_CHIRPS):
        chirp_signal = np.zeros(cfg.N_SAMPLES, dtype=np.complex128)
        slow_time = m * cfg.TC

        for r, v, rcs in targets:
            if r > cfg.MAX_RANGE_WANTED: continue

            # --- PHYSICS UPDATE: RADAR EQUATION ---
            # Power received is proportional to RCS / R^4
            # We use a simplified multiplier to keep amplitudes visible
            path_loss = np.sqrt(rcs) / (r ** 2)
            # Scale it up so it's not tiny in the simulation (Arbitrary Gain)
            amplitude = path_loss * 1e5

            fb = (cfg.SLOPE * 2 * r) / cfg.C
            fd = (2 * v) / cfg.LAMBDA

            phase = np.exp(1j * 2 * np.pi * fd * slow_time)
            chirp_signal += amplitude * np.exp(1j * 2 * np.pi * fb * t) * phase

        # Add Noise (Thermal Floor)
        chirp_signal += 0.01 * (np.random.randn(cfg.N_SAMPLES) + 1j * np.random.randn(cfg.N_SAMPLES))

        yield chirp_signal