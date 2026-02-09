# main.py
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

# Import your pipeline modules
import Generator
import proccessor
import config as cfg


# --- NEW: Class to store detection data ---
class RadarObject:
    def __init__(self, obj_id, range_m, velocity_m_s, strength_db):
        self.id = obj_id
        self.range = range_m
        self.velocity = velocity_m_s
        self.strength = strength_db
        self.frequency = (cfg.SLOPE * 2 * range_m) / cfg.C

    def __str__(self):
        return (f"Object {self.id}: Range={self.range:.1f}m, "
                f"Vel={self.velocity:.1f}m/s, "
                f"Freq={self.frequency / 1e6:.2f}MHz, "
                f"SNR={self.strength:.1f}dB")


def main():
    # 1. RUN PIPELINE
    source = Generator.stream_raw_chirps()
    rd_map = proccessor.build_range_doppler_map(source)
    range_axis, vel_axis = proccessor.get_axes()

    # 2. DETECT OBJECTS (Range & Velocity)
    detected_objects = []

    # Step A: Find Range Peaks first (Collapse Doppler)
    range_profile = np.max(rd_map, axis=0)
    range_peaks, _ = find_peaks(range_profile, height=40, distance=10)

    # Step B: For each Range Peak, find the Velocity Peak
    for i, r_idx in enumerate(range_peaks):
        # Slice the 2D map at this specific range index
        doppler_profile = rd_map[:, r_idx]

        # Find the max velocity at this range
        v_idx = np.argmax(doppler_profile)

        # Extract values
        r_val = range_axis[r_idx]
        v_val = vel_axis[v_idx]
        strength = rd_map[v_idx, r_idx]

        # Create Object and Store
        obj = RadarObject(i + 1, r_val, v_val, strength)
        detected_objects.append(obj)

    # 3. PRINT REPORT
    print("\n" + "=" * 60)
    print(f"RADAR DETECTION REPORT ({len(detected_objects)} Objects Found)")
    print("=" * 60)
    print(f"{'ID':<4} | {'Range (m)':<12} | {'Velocity (m/s)':<15} | {'Freq (MHz)':<12} | {'Strength'}")
    print("-" * 65)

    for obj in detected_objects:
        print(
            f"{obj.id:<4} | {obj.range:<12.2f} | {obj.velocity:<15.2f} | {obj.frequency / 1e6:<12.2f} | {obj.strength:.1f} dB")

    # 4. VISUALIZATION
    # plt.figure(figsize=(12, 8))
    # plt.imshow(rd_map.T, aspect='auto', origin='lower', cmap='jet',
    #            extent=[vel_axis[0], vel_axis[-1], range_axis[0], range_axis[-1]],
    #            vmin=20, vmax=100)  # Adjusted scale for path loss
    #
    # plt.title(f"Physics-Accurate Radar Map\n{len(detected_objects)} Targets Detected")
    # plt.xlabel("Velocity (m/s)")
    # plt.ylabel("Range (m)")
    # plt.colorbar(label="Power (dB)")
    # plt.show()


if __name__ == "__main__":
    main()