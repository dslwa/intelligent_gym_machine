from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QProgressBar, QGroupBox
)
from PyQt5.QtCore import Qt

from src.services.fis_service import FISResult


FEEDBACK_STYLES = {
    'ZWOLNIJ':  ('#FF9800', '#1a1000', 'SLOW DOWN'),
    'DOBRZE':   ('#4CAF50', '#0a1a0b', 'GOOD'),
    'IDEALNIE': ('#00e5ff', '#001a20', 'PERFECT'),
    'MOCNIEJ':  ('#BB86FC', '#0f001a', 'PUSH HARDER'),
    'STOP':     ('#FF5252', '#1a0000', 'STOP'),
}


class OutputPanel(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # --- Resistance ---
        res_group = QGroupBox("Machine Resistance")
        res_layout = QVBoxLayout(res_group)

        self.resistance_value = QLabel("—")
        self.resistance_value.setAlignment(Qt.AlignCenter)
        self.resistance_value.setStyleSheet(
            "font-size: 44px; font-weight: bold; color: #666666;"
        )
        res_layout.addWidget(self.resistance_value)

        self.resistance_bar = QProgressBar()
        self.resistance_bar.setRange(0, 100)
        self.resistance_bar.setValue(0)
        self.resistance_bar.setTextVisible(False)
        self.resistance_bar.setFixedHeight(16)
        self.resistance_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 8px;
                background-color: #1e1e1e;
            }
            QProgressBar::chunk {
                border-radius: 8px;
                background-color: #333333;
            }
        """)
        res_layout.addWidget(self.resistance_bar)

        self.resistance_desc = QLabel("No evaluation yet")
        self.resistance_desc.setAlignment(Qt.AlignCenter)
        self.resistance_desc.setStyleSheet("font-size: 12px; color: #666666; font-weight: bold;")
        res_layout.addWidget(self.resistance_desc)

        layout.addWidget(res_group)

        # --- Feedback ---
        fb_group = QGroupBox("Feedback Signal")
        fb_layout = QVBoxLayout(fb_group)

        self.feedback_label = QLabel("—")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet(
            "font-size: 32px; font-weight: bold; color: #666666;"
            "padding: 20px; border-radius: 10px; background-color: #1e1e1e;"
        )
        fb_layout.addWidget(self.feedback_label)

        self.feedback_value = QLabel("")
        self.feedback_value.setAlignment(Qt.AlignCenter)
        self.feedback_value.setStyleSheet("font-size: 12px; color: #666666;")
        fb_layout.addWidget(self.feedback_value)

        layout.addWidget(fb_group)

        # --- Error ---
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("color: #FF5252; font-size: 12px; font-weight: bold;")
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        layout.addWidget(self.error_label)

        layout.addStretch()

    def update_results(self, result: FISResult):
        opor = result.resistance
        feedback = result.feedback
        feedback_text = result.feedback_text

        # Resistance
        self.resistance_value.setText(f"{opor:.1f} %")
        self.resistance_bar.setValue(int(opor))

        if opor < 25:
            color = '#4CAF50'
            desc = 'Minimal / Low'
        elif opor < 50:
            color = '#00e5ff'
            desc = 'Low / Medium'
        elif opor < 75:
            color = '#FF9800'
            desc = 'Medium / High'
        else:
            color = '#FF5252'
            desc = 'High / Maximal'

        self.resistance_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 8px;
                background-color: #1e1e1e;
            }}
            QProgressBar::chunk {{
                border-radius: 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color}88, stop:1 {color});
            }}
        """)
        self.resistance_value.setStyleSheet(
            f"font-size: 44px; font-weight: bold; color: {color};"
        )
        self.resistance_desc.setText(desc)
        self.resistance_desc.setStyleSheet(f"font-size: 12px; color: {color}; font-weight: bold;")

        # Feedback
        fb_color, fb_bg, fb_en = FEEDBACK_STYLES.get(
            feedback_text, ('#666666', '#1e1e1e', feedback_text)
        )
        self.feedback_label.setText(fb_en)
        self.feedback_label.setStyleSheet(
            f"font-size: 32px; font-weight: bold; color: {fb_color};"
            f"padding: 20px; border-radius: 10px; background-color: {fb_bg};"
            f"border: 2px solid {fb_color}66;"
        )
        self.feedback_value.setText(f"Signal value: {feedback:.2f} / 5.00")
        self.feedback_value.setStyleSheet(f"font-size: 12px; color: {fb_color};")

        # Error
        if result.error:
            self.error_label.setText(f"Warning: {result.error}")
            self.error_label.show()
        else:
            self.error_label.hide()

    def clear(self):
        self.resistance_value.setText("—")
        self.resistance_value.setStyleSheet(
            "font-size: 44px; font-weight: bold; color: #666666;"
        )
        self.resistance_bar.setValue(0)
        self.resistance_desc.setText("No evaluation yet")
        self.feedback_label.setText("—")
        self.feedback_label.setStyleSheet(
            "font-size: 32px; font-weight: bold; color: #666666;"
            "padding: 20px; border-radius: 10px; background-color: #1e1e1e;"
        )
        self.feedback_value.setText("")
        self.error_label.hide()
