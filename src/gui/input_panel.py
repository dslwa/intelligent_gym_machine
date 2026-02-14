from typing import Dict

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider,
    QDoubleSpinBox, QComboBox, QPushButton, QGroupBox
)
from PyQt5.QtCore import Qt, pyqtSignal

from config import fis_config
from src.gui.styles import (
    EVAL_BUTTON_STYLE,
    MODE_LABEL_HTML,
    RESET_BUTTON_STYLE,
    RANGE_LABEL_STYLE,
    SLIDER_STYLE,
    VALUE_LABEL_STYLE,
    slider_label_html,
)
from src.services.fis_service import FISInputs


class InputSlider(QWidget):

    valueChanged = pyqtSignal(float)

    def __init__(self, name, unit, min_val, max_val, default, step=1.0, decimals=0):
        super().__init__()
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.decimals = decimals
        self.default = default

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 8)
        layout.setSpacing(3)

        header = QHBoxLayout()
        self.label = QLabel(slider_label_html(name, unit))
        self.value_label = QLabel(f"{default:.{decimals}f}")
        self.value_label.setStyleSheet(VALUE_LABEL_STYLE)
        header.addWidget(self.label)
        header.addStretch()
        header.addWidget(self.value_label)
        layout.addLayout(header)

        slider_row = QHBoxLayout()
        slider_row.setSpacing(10)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(int((max_val - min_val) / step))
        self.slider.setValue(int((default - min_val) / step))
        self.slider.setFixedHeight(24)
        self.slider.setStyleSheet(SLIDER_STYLE)

        self.spinbox = QDoubleSpinBox()
        self.spinbox.setRange(min_val, max_val)
        self.spinbox.setSingleStep(step)
        self.spinbox.setDecimals(decimals)
        self.spinbox.setValue(default)
        self.spinbox.setFixedWidth(85)

        slider_row.addWidget(self.slider)
        slider_row.addWidget(self.spinbox)
        layout.addLayout(slider_row)

        range_row = QHBoxLayout()
        min_label = QLabel(f"{min_val:.{decimals}f}")
        min_label.setStyleSheet(RANGE_LABEL_STYLE)
        max_label = QLabel(f"{max_val:.{decimals}f}")
        max_label.setStyleSheet(RANGE_LABEL_STYLE)
        range_row.addWidget(min_label)
        range_row.addStretch()
        range_row.addWidget(max_label)
        layout.addLayout(range_row)

        self.slider.valueChanged.connect(self._slider_changed)
        self.spinbox.valueChanged.connect(self._spinbox_changed)

    def _slider_changed(self, pos):
        val = self.min_val + pos * self.step
        self.spinbox.blockSignals(True)
        self.spinbox.setValue(val)
        self.spinbox.blockSignals(False)
        self.value_label.setText(f"{val:.{self.decimals}f}")
        self.valueChanged.emit(val)

    def _spinbox_changed(self, val):
        self.slider.blockSignals(True)
        self.slider.setValue(int((val - self.min_val) / self.step))
        self.slider.blockSignals(False)
        self.value_label.setText(f"{val:.{self.decimals}f}")
        self.valueChanged.emit(val)

    def value(self):
        return self.spinbox.value()

    def reset(self):
        self.spinbox.setValue(self.default)


class InputPanel(QWidget):

    evaluateClicked = pyqtSignal()
    mfTypeChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        group = QGroupBox("Input Variables")
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(4)

        self.sliders: Dict[str, InputSlider] = {}
        for identifier, config in fis_config.INPUT_VARIABLES.items():
            slider = InputSlider(
                config.label,
                config.unit,
                config.range_min,
                config.range_max,
                config.default,
                step=config.step,
                decimals=config.decimals,
            )
            self.sliders[identifier] = slider
            group_layout.addWidget(slider)

        mode_row = QHBoxLayout()
        mode_label = QLabel(MODE_LABEL_HTML)
        self.tryb_combo = QComboBox()
        self.training_mode_values = []
        for label, value in fis_config.TRAINING_MODE_OPTIONS:
            self.tryb_combo.addItem(label)
            self.training_mode_values.append(value)
        default_training_index = next(
            (idx for idx, value in enumerate(self.training_mode_values) if value == 2),
            0
        )
        self.tryb_combo.setCurrentIndex(default_training_index)
        self.default_training_index = default_training_index
        mode_row.addWidget(mode_label)
        mode_row.addWidget(self.tryb_combo, 1)
        group_layout.addLayout(mode_row)

        layout.addWidget(group)

        # MF type selector
        mf_group = QGroupBox("Membership Function Type")
        mf_layout = QHBoxLayout(mf_group)
        self.mf_combo = QComboBox()
        self.mf_combo.addItems([label for label, _ in fis_config.MF_TYPE_OPTIONS])
        default_mf_index = next(
            idx for idx, (_, mf_type) in enumerate(fis_config.MF_TYPE_OPTIONS)
            if mf_type == fis_config.DEFAULT_MF_TYPE
        )
        self.mf_combo.setCurrentIndex(default_mf_index)
        self.mf_combo.currentIndexChanged.connect(self._mf_type_changed)
        mf_layout.addWidget(self.mf_combo)
        layout.addWidget(mf_group)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.eval_btn = QPushButton("EVALUATE")
        self.eval_btn.setStyleSheet(EVAL_BUTTON_STYLE)
        self.eval_btn.clicked.connect(self.evaluateClicked.emit)

        self.reset_btn = QPushButton("RESET")
        self.reset_btn.setStyleSheet(RESET_BUTTON_STYLE)
        self.reset_btn.clicked.connect(self._reset_all)

        btn_layout.addWidget(self.eval_btn, 2)
        btn_layout.addWidget(self.reset_btn, 1)
        layout.addLayout(btn_layout)

        layout.addStretch()

    def _mf_type_changed(self, index):
        _, mf_type = fis_config.MF_TYPE_OPTIONS[index]
        self.mfTypeChanged.emit(mf_type)

    def _reset_all(self):
        for slider in self.sliders.values():
            slider.reset()
        self.tryb_combo.setCurrentIndex(self.default_training_index)

    def get_values(self):
        return FISInputs(
            sila=self.sliders['sila'].value(),
            predkosc=self.sliders['predkosc'].value(),
            faza=self.sliders['faza'].value(),
            zmeczenie=self.sliders['zmeczenie'].value(),
            tryb=self.training_mode_values[self.tryb_combo.currentIndex()]
        )
