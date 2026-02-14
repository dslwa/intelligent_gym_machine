from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QSplitter, QApplication
)
from PyQt5.QtCore import Qt

from config import fis_config
from src.gui.input_panel import InputPanel
from src.gui.output_panel import OutputPanel
from src.gui.visualization_panel import VisualizationPanel
from src.services.fis_service import FISService


class MainWindow(QMainWindow):

    def __init__(self, service: FISService):
        super().__init__()
        self.service = service

        self.setWindowTitle("Intelligent Gym Machine — FIS Controller")
        self.setMinimumSize(1200, 700)
        self.resize(1400, 800)

        self._setup_ui()
        self._setup_statusbar()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        self.main_layout = QHBoxLayout(central)
        self.main_layout.setContentsMargins(8, 8, 8, 8)

        self.splitter = QSplitter(Qt.Horizontal)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.input_panel = InputPanel()
        self.output_panel = OutputPanel()

        left_layout.addWidget(self.input_panel)
        left_layout.addWidget(self.output_panel)

        self.viz_panel = VisualizationPanel(self.service)

        self.splitter.addWidget(left)
        self.splitter.addWidget(self.viz_panel)
        self.splitter.setSizes([400, 800])
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)

        self.main_layout.addWidget(self.splitter)

        self.input_panel.evaluateClicked.connect(self._evaluate)
        self.input_panel.mfTypeChanged.connect(self._change_mf_type)

    def _setup_statusbar(self):
        self._update_status_idle()

    def _update_status_idle(self):
        self.statusBar().showMessage(
            f"FIS ready — {self.service.rule_count} rules  |  "
            f"MF type: {self.service.current_mf_label}  |  "
            "Set inputs and click Evaluate"
        )

    def _change_mf_type(self, mf_type: str):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.service.change_mf_type(mf_type)
            self.viz_panel.refresh_membership_data()
            self.output_panel.clear()
            self._update_status_idle()
        finally:
            QApplication.restoreOverrideCursor()

    def _evaluate(self):
        inputs = self.input_panel.get_values()
        result = self.service.compute(inputs)

        self.output_panel.update_results(result)
        self.viz_panel.update_results(result)

        mode_label = fis_config.TRAINING_MODE_STATUS_NAMES.get(inputs.tryb, str(inputs.tryb))
        self.statusBar().showMessage(
            f"[{self.service.current_mf_label}]  "
            f"Force={inputs.sila:.0f}N, "
            f"Speed={inputs.predkosc:.2f}m/s, "
            f"Phase={inputs.faza:.0f}%, "
            f"Fatigue={inputs.zmeczenie:.0f}%, "
            f"Mode={mode_label} → "
            f"Resistance={result.resistance:.1f}%, "
            f"Feedback={result.feedback_text}"
        )
