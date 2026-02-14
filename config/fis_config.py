from dataclasses import dataclass
from typing import Tuple, Dict


@dataclass(frozen=True)
class SliderConfig:
    label: str
    unit: str
    range_min: float
    range_max: float
    step: float
    decimals: int
    default: float


@dataclass(frozen=True)
class TermDefinition:
    name: str
    function: str
    params: Tuple[float, ...]


@dataclass(frozen=True)
class VariableMetadata:
    label: str
    unit: str


INPUT_VARIABLES = {
    'sila': SliderConfig('Generated Force', 'N', 0, 500, 1, 0, 250),
    'predkosc': SliderConfig('Movement Speed', 'm/s', 0.0, 1.5, 0.01, 2, 0.7),
    'faza': SliderConfig('Movement Phase', '% ROM', 0, 100, 1, 0, 50),
    'zmeczenie': SliderConfig('Fatigue Index', '%', 0, 100, 1, 0, 20),
}

TRAINING_MODE_OPTIONS = (
    ('Strength (Silowy)', 1),
    ('Hypertrophy (Hipertrofia)', 2),
    ('Endurance (Wytrzymalosc)', 3),
)

TRAINING_MODE_STATUS_NAMES = {
    1: 'Strength',
    2: 'Hypertrophy',
    3: 'Endurance',
}

MF_TYPE_OPTIONS = (
    ('Triangular (default)', 'triangular'),
    ('Gaussian', 'gaussian'),
    ('Generalized Bell', 'gbell'),
    ('Sigmoid', 'sigmoid'),
)

MF_TYPE_LABELS = {value: label for label, value in MF_TYPE_OPTIONS}
DEFAULT_MF_TYPE = 'triangular'

VARIABLE_UNIVERSES = {
    'sila': (0, 500, 1),
    'predkosc': (0.0, 1.5, 0.01),
    'faza': (0, 100, 1),
    'zmeczenie': (0, 100, 1),
    'tryb': (1, 3, 0.01),
    'opor': (0, 100, 1),
    'feedback': (1, 5, 0.01),
}

TERM_DEFINITIONS = {
    'sila': (
        TermDefinition('bardzo_niska', 'trapmf', (0, 0, 50, 100)),
        TermDefinition('niska', 'trimf', (50, 125, 200)),
        TermDefinition('srednia', 'trimf', (150, 250, 350)),
        TermDefinition('wysoka', 'trimf', (300, 375, 450)),
        TermDefinition('bardzo_wysoka', 'trapmf', (400, 450, 500, 500)),
    ),
    'predkosc': (
        TermDefinition('bardzo_wolna', 'trapmf', (0, 0, 0.1, 0.25)),
        TermDefinition('wolna', 'trimf', (0.15, 0.35, 0.55)),
        TermDefinition('umiarkowana', 'trimf', (0.45, 0.7, 0.95)),
        TermDefinition('szybka', 'trimf', (0.85, 1.1, 1.35)),
        TermDefinition('bardzo_szybka', 'trapmf', (1.2, 1.35, 1.5, 1.5)),
    ),
    'faza': (
        TermDefinition('poczatkowa', 'trapmf', (0, 0, 10, 25)),
        TermDefinition('dolna', 'trimf', (15, 30, 45)),
        TermDefinition('srodkowa', 'trimf', (35, 50, 65)),
        TermDefinition('gorna', 'trimf', (55, 70, 85)),
        TermDefinition('koncowa', 'trapmf', (75, 90, 100, 100)),
    ),
    'zmeczenie': (
        TermDefinition('swiezy', 'trapmf', (0, 0, 5, 15)),
        TermDefinition('lekkie', 'trimf', (10, 25, 40)),
        TermDefinition('umiarkowane', 'trimf', (30, 50, 70)),
        TermDefinition('wysokie', 'trimf', (60, 75, 90)),
        TermDefinition('wyczerpanie', 'trapmf', (80, 90, 100, 100)),
    ),
    'tryb': (
        TermDefinition('silowy', 'trimf', (1, 1, 1.8)),
        TermDefinition('hipertrofia', 'trimf', (1.5, 2, 2.5)),
        TermDefinition('wytrzymalosc', 'trimf', (2.2, 3, 3)),
    ),
    'opor': (
        TermDefinition('minimalny', 'trapmf', (0, 0, 10, 20)),
        TermDefinition('niski', 'trimf', (15, 30, 45)),
        TermDefinition('sredni', 'trimf', (35, 50, 65)),
        TermDefinition('wysoki', 'trimf', (55, 70, 85)),
        TermDefinition('maksymalny', 'trapmf', (75, 90, 100, 100)),
    ),
    'feedback': (
        TermDefinition('zwolnij', 'trimf', (1, 1, 2)),
        TermDefinition('dobrze', 'trimf', (1.5, 2.5, 3.5)),
        TermDefinition('idealnie', 'trimf', (2.5, 3, 3.5)),
        TermDefinition('mocniej', 'trimf', (3, 3.5, 4.5)),
        TermDefinition('stop', 'trimf', (4, 5, 5)),
    ),
}

MF_CENTER_POINTS = {
    'sila': (50, 125, 250, 375, 450),
    'predkosc': (0.1, 0.35, 0.7, 1.1, 1.4),
    'faza': (10, 30, 50, 70, 90),
    'zmeczenie': (5, 25, 50, 75, 90),
    'opor': (10, 30, 50, 70, 90),
}

VARIABLE_METADATA = {
    'sila': VariableMetadata('Generated Force', 'N'),
    'predkosc': VariableMetadata('Movement Speed', 'm/s'),
    'faza': VariableMetadata('Movement Phase', '% ROM'),
    'zmeczenie': VariableMetadata('Fatigue Index', '%'),
    'tryb': VariableMetadata('Training Mode', '-'),
    'opor': VariableMetadata('Machine Resistance', '%'),
    'feedback': VariableMetadata('Feedback Signal', '-'),
}

INPUT_VALIDATION_BOUNDS = {
    identifier: (config.range_min, config.range_max)
    for identifier, config in INPUT_VARIABLES.items()
}

VISUALIZATION_ORDER = (
    'sila',
    'predkosc',
    'faza',
    'zmeczenie',
    'tryb',
    'opor',
    'feedback',
)
