# Intelligent Gym Machine - Fuzzy Inference System

An intelligent training machine control system based on fuzzy logic (Mamdani FIS). Dynamically adjusts machine resistance and generates real-time feedback based on the user's biomechanical parameters during exercise.

## Table of Contents

- [System Overview](#system-overview)
- [Architecture](#architecture)
- [Linguistic Variables](#linguistic-variables)
- [Rule Base](#rule-base)
- [Installation](#installation)
- [Usage](#usage)
- [Output](#output)
- [Technologies](#technologies)

## System Overview

The system implements a Mamdani-type fuzzy controller with the following configuration:

| Parameter | Value |
|---|---|
| FIS Type | Mamdani |
| T-norm (AND) | Minimum |
| S-norm (OR) | Maximum |
| Implication | Minimum |
| Aggregation | Maximum |
| Defuzzification | Centroid |
| Number of Rules | 30+ |

The system incorporates sports biomechanics principles:
- **Accommodating resistance** — adjusts load based on mechanical leverage across movement phases
- **Drop-set protocol** — reduces resistance as fatigue increases
- **Safety constraints** — prevents overloading under high fatigue conditions
- **Movement phase optimization** — varies system response depending on range of motion (ROM)

## Architecture

```
src/
├── core/
│   ├── fis_engine.py          # Main FIS engine (IntelligentGymMachine class)
│   └── experimental.py        # Experimental version with multiple MF types
├── analysis/
│   ├── scenarios.py           # 8 biomechanical test scenarios
│   └── experiments.py         # Comparative experiments across MF types
└── visualization/
    └── plots.py               # Visualizations: MFs, 3D surfaces, workout simulations
```

## Linguistic Variables

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

## Rule Base

The system contains over 30 fuzzy rules grounded in sports biomechanics. Examples:

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

## Installation

```bash
git clone https://github.com/dslwa/intelligent_gym_machine.git
cd intelligent_gym_machine
pip install -r requirements.txt
```

**Requirements:** Python 3.8+

## Usage

### Full Demo

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

## Output

The system generates the following visualizations in the `output/` directory:

| File | Description |
|---|---|
| `membership_functions.png` | Membership functions for all input and output variables |
| `surface_sila_faza.png` | 3D surface: force × movement phase |
| `surface_zmeczenie_predkosc.png` | 3D surface: fatigue × speed |
| `simulation_hipertrofia.png` | Hypertrophy workout simulation (force, speed, fatigue, feedback) |
| `simulation_silowy.png` | Strength workout simulation |
| `comparison_membership_functions.png` | Membership function type comparison |
| `comparison_inference_results.png` | Inference output comparison across MF types |

### Experimental Version

The `IntelligentGymMachineExperimental` class allows testing with four membership function types:

- **triangular** — triangle/trapezoid functions (default)
- **gaussian** — Gaussian bell curves (smooth transitions)
- **gbell** — generalized bell curves
- **sigmoid** — sigmoid functions

## Technologies

- **Python 3** — implementation language
- **NumPy** — numerical computation
- **scikit-fuzzy** — fuzzy logic engine
- **Matplotlib** — data visualization
