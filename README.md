# SkyGuard: Advanced SDR Radar Simulation & Stealth Detection
### 📡 IEEE CASS Student Design Competition 2025

SkyGuard is a high-fidelity **Software-Defined Radar (SDR)** simulator designed to monitor a **150km range**. The system integrates real-time civil aviation data with advanced Digital Signal Processing (DSP) to detect, track, and identify targets, including low-observable (Stealth) aircraft using adaptive algorithms.

---

## 🚀 Key Features
* **Real-time Tracking:** Integrated with OpenSky Network API to fetch live flight data.
* **150KM Range Emulation:** Long-range FMCW waveform design with high-resolution range-doppler mapping.
* **Anti-Stealth Logic:** Specialized Signal-to-Noise Ratio (SNR) enhancement to detect low RCS (Radar Cross Section) targets.
* **Modern DSP Pipeline:** Implements 2D-FFT, Windowing, and OS-CFAR (Ordered Statistic Constant False Alarm Rate) detection.
* **Interactive Dashboard:** Military-grade UI built with React & WebSockets for real-time visualization.

---

## 🏗️ System Architecture
The project is divided into four main modular pipelines:

1. **Data Acquisition (Navigation Team):** Fetches GPS coordinates and converts them to polar coordinates (Range/Azimuth).
2. **Signal Physics (Physics Team):** Generates FMCW Chirp signals, adds atmospheric noise, and emulates target reflections.
3. **DSP Engine (Signal Processing Team):** Processes raw IQ data through FFT stages to extract target distance and velocity.
4. **HMI Dashboard (UI/UX Team):** Visualizes targets on a PPI (Plan Position Indicator) radar sweep.

---

## 📁 Repository Structure
```text
├── /backend            # FastAPI Server & WebSocket Logic
├── /navigation         # API Integration & Coordinate Mapping
├── /signal_physics     # Waveform Generation & Noise Modeling
├── /dsp_engine         # FFT & OS-CFAR Detection Algorithms
├── /frontend           # React.js Radar Interface
├── config.py           # Global Radar Constants (Range, Frequency, etc.)
└── requirements.txt    # Project Dependencies
```

---

## 🛠️ Installation & Setup

1️⃣ Clone the repository

```bash
git clone https://github.com/MostafaHatemGhonem/Advanced-SDR-Radar-Simulation-Stealth-Detection.git
cd Advanced-SDR-Radar-Simulation-Stealth-Detection
```

2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

3️⃣ Run the Backend

```bash
python backend/main.py
```

---

## 👥 The Team

* Team Leader: Mostafa Hatem
* Systems Architect: [Name]
* DSP Lead: [Name]
* Physics & Signal Lead: [Name]
* Frontend Lead: [Name]

<p align="center"><b>© 2025 SkyGuard Project | IEEE CASS Competition</b></p>