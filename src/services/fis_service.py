import logging
from dataclasses import dataclass
from typing import Tuple, Optional

import numpy as np

from config import fis_config
from config.logging_config import configure_logging, LOGGER_NAME
from src.core.experimental import IntelligentGymMachineExperimental
from src.core.fis_engine import IntelligentGymMachine

configure_logging()
LOGGER = logging.getLogger(LOGGER_NAME)


@dataclass(frozen=True)
class FISInputs:
    sila: float
    predkosc: float
    faza: float
    zmeczenie: float
    tryb: float


@dataclass(frozen=True)
class FISResult:
    resistance: float
    feedback: float
    feedback_text: str
    error: Optional[str] = None


@dataclass(frozen=True)
class TermPlotData:
    name: str
    membership: np.ndarray


@dataclass(frozen=True)
class MembershipPlotData:
    identifier: str
    label: str
    unit: str
    universe: np.ndarray
    terms: Tuple[TermPlotData, ...]


class ValidationError(ValueError):
    pass


class FISService:
    def __init__(self, mf_type: str = fis_config.DEFAULT_MF_TYPE):
        self.logger = LOGGER
        self._machine = None
        self._membership_snapshot: Tuple[MembershipPlotData, ...] = ()
        self.current_mf_type = ''
        self.change_mf_type(mf_type)

    def change_mf_type(self, mf_type: str):
        if mf_type not in fis_config.MF_TYPE_LABELS:
            raise ValidationError(f"Unknown MF type: {mf_type}")
        self.logger.info("Switching machine to %s MFs", fis_config.MF_TYPE_LABELS[mf_type])
        self.current_mf_type = mf_type
        if mf_type == fis_config.DEFAULT_MF_TYPE:
            self._machine = IntelligentGymMachine()
        else:
            self._machine = IntelligentGymMachineExperimental(mf_type=mf_type)
        self._membership_snapshot = self._snapshot_membership()

    def get_membership_plot_data(self) -> Tuple[MembershipPlotData, ...]:
        return self._membership_snapshot

    def compute(self, inputs: FISInputs) -> FISResult:
        self._validate_inputs(inputs)
        self.logger.debug("Computing FIS for inputs %s", inputs)
        raw = self._machine.compute(
            inputs.sila,
            inputs.predkosc,
            inputs.faza,
            inputs.zmeczenie,
            inputs.tryb
        )
        return FISResult(
            resistance=raw['opor'],
            feedback=raw['feedback'],
            feedback_text=raw['feedback_text'],
            error=raw.get('error')
        )

    def _snapshot_membership(self) -> Tuple[MembershipPlotData, ...]:
        snapshots = []
        for identifier in fis_config.VISUALIZATION_ORDER:
            variable = getattr(self._machine, identifier)
            metadata = fis_config.VARIABLE_METADATA[identifier]
            universe = np.array(variable.universe, copy=True)
            terms = tuple(
                TermPlotData(name, np.array(variable[name].mf, copy=True))
                for name in variable.terms
            )
            snapshots.append(MembershipPlotData(identifier, metadata.label, metadata.unit, universe, terms))
        return tuple(snapshots)

    def _validate_inputs(self, inputs: FISInputs):
        for field_name, value in inputs.__dict__.items():
            if field_name not in fis_config.INPUT_VALIDATION_BOUNDS:
                continue
            min_val, max_val = fis_config.INPUT_VALIDATION_BOUNDS[field_name]
            if not (min_val <= value <= max_val):
                raise ValidationError(f"{field_name}={value} outside [{min_val}, {max_val}]")

    @property
    def rule_count(self) -> int:
        return len(self._machine.rules)

    @property
    def machine(self):
        return self._machine

    @property
    def current_mf_label(self):
        return fis_config.MF_TYPE_LABELS.get(self.current_mf_type, self.current_mf_type)
