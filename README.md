<h1 align="center">Intelligent Gym Machine</h1>
<h3 align="center">Fuzzy Inference System for Adaptive Resistance Training</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy">
  <img src="https://img.shields.io/badge/scikit--fuzzy-0.4.2-F7931E?style=for-the-badge" alt="scikit-fuzzy">
  <img src="https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=plotly&logoColor=white" alt="Matplotlib">
  <img src="https://img.shields.io/badge/PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt5">
</p>

<p align="center">
  An intelligent training machine control system based on <strong>Mamdani-type fuzzy logic</strong>.<br>
  Dynamically adjusts machine resistance and generates real-time feedback<br>
  based on the user's biomechanical parameters during exercise.
</p>

---

## System Overview

The system implements a **Mamdani-type fuzzy controller** with the following configuration:

| Parameter | Value |
|---|---|
| FIS Type | Mamdani |
| T-norm (AND) | Minimum |
| S-norm (OR) | Maximum |
| Implication | Minimum |
| Aggregation | Maximum |
| Defuzzification | Centroid |
| Number of Rules | 30+ |

The system incorporates **sports biomechanics** principles:
- **Accommodating resistance** — adjusts load based on mechanical leverage across movement phases
- **Drop-set protocol** — reduces resistance as fatigue increases
- **Safety constraints** — prevents overloading under high fatigue conditions
- **Movement phase optimization** — varies system response depending on range of motion (ROM)

## Membership Functions

<p align="center">
  <img src="output/membership_functions.png" alt="Membership Functions" width="90%">
</p>

### Inputs

| Variable | Range | Linguistic Terms |
|---|---|---|
| Generated Force | 0–500 N | bardzo_niska, niska, srednia, wysoka, bardzo_wysoka |
| Movement Speed | 0–1.5 m/s | bardzo_wolna, wolna, umiarkowana, szybka, bardzo_szybka |
| Movement Phase | 0–100 % ROM | poczatkowa, dolna, srodkowa, gorna, koncowa |
| Fatigue Index | 0–100 % | swiezy, lekkie, umiarkowane, wysokie, wyczerpanie |
| Training Mode | 1–3 | silowy, hipertrofia, wytrzymalosc |

### Outputs

| Variable | Range | Linguistic Terms |
|---|---|---|
| Machine Resistance | 0–100 % | minimalny, niski, sredni, wysoki, maksymalny |
| Feedback Signal | 1–5 | zwolnij, dobrze, idealnie, mocniej, stop |

## 3D Inference Surfaces

<p align="center">
  <img src="output/surface_sila_faza.png" alt="Surface: Force x Phase" width="90%">
</p>
<p align="center">
  <img src="output/surface_zmeczenie_predkosc.png" alt="Surface: Fatigue x Speed" width="90%">
</p>

## Workout Simulation

<p align="center">
  <img src="output/simulation_hipertrofia.png" alt="Hypertrophy Simulation" width="90%">
</p>
<p align="center">
  <img src="output/simulation_silowy.png" alt="Strength Simulation" width="90%">
</p>

## Rule Base

The system contains over **30 fuzzy rules** grounded in sports biomechanics. Examples:

```
IF (phase = initial AND force = medium)
    THEN (resistance = low, feedback = good)

IF (fatigue = exhausted)
    THEN (resistance = minimal, feedback = stop)

IF (speed = very_fast AND fatigue = fresh)
    THEN (resistance = high, feedback = slow_down)

IF (mode = strength AND force = very_high AND fatigue = fresh)
    THEN (resistance = maximal, feedback = perfect)
```

## Architecture

```
intelligent_gym_machine/
├── main.py                     # Full demo runner
├── gui_app.py                  # GUI application entry point
├── generate_comparison.py      # MF type comparison tool
├── requirements.txt
│
├── src/
│   ├── core/
│   │   ├── fis_engine.py       # Main FIS engine (IntelligentGymMachine)
│   │   └── experimental.py     # Experimental version with multiple MF types
│   ├── analysis/
│   │   ├── scenarios.py        # 8 biomechanical test scenarios
│   │   └── experiments.py      # Comparative experiments across MF types
│   ├── visualization/
│   │   └── plots.py            # Matplotlib plotting functions
│   └── gui/
│       ├── main_window.py      # PyQt5 main window
│       ├── input_panel.py      # Input sliders and controls
│       ├── output_panel.py     # Output results display
│       └── visualization_panel.py  # Embedded matplotlib charts
│
└── output/                     # Generated visualizations
```

## Installation

```bash
git clone https://github.com/dslwa/intelligent_gym_machine.git
cd intelligent_gym_machine
pip install -r requirements.txt
```

## Usage

### GUI Application

```bash
python gui_app.py
```

Interactive graphical interface with:
- Input sliders for all 5 FIS variables
- Real-time inference results
- Embedded membership function visualizations

### Full Demo (CLI)

```bash
python main.py
```

Runs a complete system demonstration:
1. FIS engine initialization
2. Membership function visualization
3. 8 biomechanical scenario evaluation
4. 3D surface plot generation
5. Full workout simulations (hypertrophy and strength modes)
6. Comparative experiments across membership function types

### Membership Function Comparison

```bash
python generate_comparison.py
```

Generates results for two MF types (triangular vs. Gaussian) in separate output folders.

## MF Type Comparison

<p align="center">
  <img src="output/comparison_membership_functions.png" alt="MF Comparison" width="90%">
</p>

The `IntelligentGymMachineExperimental` class supports four membership function types:

- **triangular** — triangle/trapezoid functions (default)
- **gaussian** — Gaussian bell curves (smooth transitions)
- **gbell** — generalized bell curves
- **sigmoid** — sigmoid functions

## Technologies

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy">
  <img src="https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge" alt="Matplotlib">
  <img src="https://img.shields.io/badge/PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt5">
</p>
