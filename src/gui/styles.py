"""Centralized style definitions for the GUI application."""

from PyQt5.QtGui import QPalette, QColor, QFont

# ── Color palette ──────────────────────────────────────────────────────────

BG_PRIMARY = '#0d0d0d'
BG_SECONDARY = '#111111'
BG_PANEL = '#141414'
BG_ELEMENT = '#1e1e1e'
BG_HOVER = '#262626'
BG_ACTIVE = '#333333'

TEXT_PRIMARY = '#f0f0f0'
TEXT_SECONDARY = '#cccccc'
TEXT_MUTED = '#aaaaaa'
TEXT_DISABLED = '#666666'
TEXT_RANGE = '#888888'

ACCENT = '#00e5ff'
ACCENT_DARK = '#0088cc'
ACCENT_HOVER = '#33eeff'
ACCENT_HOVER_DARK = '#00aadd'
ACCENT_PRESSED = '#0099cc'
ACCENT_PRESSED_DARK = '#006699'

BORDER = '#333333'
BORDER_HOVER = '#444444'
BORDER_ACTIVE = '#666666'

COLOR_SUCCESS = '#4CAF50'
COLOR_WARNING = '#FF9800'
COLOR_ERROR = '#FF5252'
COLOR_PURPLE = '#BB86FC'
COLOR_YELLOW = '#FFD600'
COLOR_GREEN_BRIGHT = '#00E676'
COLOR_PINK = '#E040FB'

# Ordered accent colors for charts
CHART_COLORS = [
    ACCENT, COLOR_WARNING, COLOR_SUCCESS, COLOR_PURPLE,
    COLOR_ERROR, COLOR_YELLOW, COLOR_GREEN_BRIGHT, COLOR_PINK,
]

# ── Matplotlib chart colors ───────────────────────────────────────────────

CHART_BG = BG_SECONDARY
CHART_FACE = BG_PRIMARY
CHART_TEXT = '#ffffff'
CHART_GRID = BORDER
CHART_TICK = TEXT_SECONDARY
CHART_LEGEND_BG = '#1a1a1a'
CHART_INFO_BG = '#1a1a1a'

# ── Feedback signal styles ────────────────────────────────────────────────

FEEDBACK_STYLES = {
    'ZWOLNIJ':  (COLOR_WARNING, '#1a1000', 'SLOW DOWN'),
    'DOBRZE':   (COLOR_SUCCESS, '#0a1a0b', 'GOOD'),
    'IDEALNIE': (ACCENT,        '#001a20', 'PERFECT'),
    'MOCNIEJ':  (COLOR_PURPLE,  '#0f001a', 'PUSH HARDER'),
    'STOP':     (COLOR_ERROR,   '#1a0000', 'STOP'),
}

FEEDBACK_DEFAULT = (TEXT_DISABLED, BG_ELEMENT)

# ── Resistance level thresholds ───────────────────────────────────────────

RESISTANCE_LEVELS = [
    (25,  COLOR_SUCCESS, 'Minimal / Low'),
    (50,  ACCENT,        'Low / Medium'),
    (75,  COLOR_WARNING, 'Medium / High'),
    (100, COLOR_ERROR,   'High / Maximal'),
]

# ── Font ──────────────────────────────────────────────────────────────────

FONT_FAMILY = 'Segoe UI'
FONT_SIZE = 11


def create_app_font():
    return QFont(FONT_FAMILY, FONT_SIZE)


# ── QPalette ──────────────────────────────────────────────────────────────

def create_dark_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(BG_PRIMARY))
    palette.setColor(QPalette.WindowText, QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.Base, QColor(BG_PANEL))
    palette.setColor(QPalette.AlternateBase, QColor(BG_ELEMENT))
    palette.setColor(QPalette.ToolTipBase, QColor(BG_ELEMENT))
    palette.setColor(QPalette.ToolTipText, QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.Text, QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.Button, QColor(BG_ELEMENT))
    palette.setColor(QPalette.ButtonText, QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.Highlight, QColor(ACCENT))
    palette.setColor(QPalette.HighlightedText, QColor('#000000'))
    return palette


# ── Global stylesheet ────────────────────────────────────────────────────

APP_STYLESHEET = f"""
    QMainWindow, QWidget {{
        background-color: {BG_PRIMARY};
        color: {TEXT_PRIMARY};
    }}

    QGroupBox {{
        font-size: 14px;
        font-weight: bold;
        color: {ACCENT};
        border: 1px solid {BORDER};
        border-radius: 10px;
        margin-top: 14px;
        padding: 20px 12px 12px 12px;
        background-color: {BG_PANEL};
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 14px;
        padding: 0 8px;
        color: {ACCENT};
    }}

    QLabel {{
        color: {TEXT_PRIMARY};
        font-size: 12px;
    }}

    QComboBox {{
        background-color: {BG_ELEMENT};
        color: #ffffff;
        border: 1px solid {BORDER_HOVER};
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 13px;
        font-weight: bold;
    }}
    QComboBox:hover {{
        border: 1px solid {ACCENT};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {BG_ELEMENT};
        color: #ffffff;
        selection-background-color: {BG_ACTIVE};
        border: 1px solid {BORDER_HOVER};
        font-size: 13px;
    }}

    QDoubleSpinBox {{
        background-color: {BG_ELEMENT};
        color: #ffffff;
        border: 1px solid {BORDER_HOVER};
        border-radius: 4px;
        padding: 4px;
        font-size: 13px;
        font-weight: bold;
    }}
    QDoubleSpinBox:hover {{
        border: 1px solid {ACCENT};
    }}

    QTabWidget::pane {{
        border: 1px solid {BORDER};
        border-radius: 6px;
        background-color: {BG_PRIMARY};
    }}
    QTabBar::tab {{
        background-color: {BG_PANEL};
        color: {TEXT_MUTED};
        padding: 12px 24px;
        border: 1px solid {BORDER};
        border-bottom: none;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        margin-right: 2px;
        font-size: 13px;
        font-weight: bold;
    }}
    QTabBar::tab:selected {{
        background-color: {BG_ELEMENT};
        color: {ACCENT};
        border-bottom: 3px solid {ACCENT};
    }}
    QTabBar::tab:hover:!selected {{
        background-color: {BG_HOVER};
        color: {TEXT_PRIMARY};
    }}

    QSplitter::handle {{
        background-color: {BORDER};
        width: 2px;
    }}

    QStatusBar {{
        background-color: {BG_PANEL};
        color: {ACCENT};
        font-size: 12px;
        font-weight: bold;
        padding: 6px;
        border-top: 1px solid {BORDER};
    }}

    QScrollBar:vertical {{
        background-color: {BG_PRIMARY};
        width: 10px;
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical {{
        background-color: {BG_ACTIVE};
        border-radius: 5px;
        min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: #555555;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
"""

# ── Component stylesheets ────────────────────────────────────────────────

SLIDER_STYLE = f"""
    QSlider::groove:horizontal {{
        height: 8px;
        background: {BG_HOVER};
        border-radius: 4px;
        border: 1px solid {BORDER};
    }}
    QSlider::handle:horizontal {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {ACCENT}, stop:1 {ACCENT_DARK});
        width: 20px;
        height: 20px;
        margin: -7px 0;
        border-radius: 10px;
        border: 2px solid {BG_PRIMARY};
    }}
    QSlider::handle:horizontal:hover {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {ACCENT_HOVER}, stop:1 {ACCENT_HOVER_DARK});
        border: 2px solid {ACCENT};
    }}
    QSlider::sub-page:horizontal {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {ACCENT_DARK}, stop:1 {ACCENT});
        border-radius: 4px;
    }}
"""

EVAL_BUTTON_STYLE = f"""
    QPushButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {ACCENT_DARK}, stop:1 {ACCENT});
        color: #000000;
        font-size: 16px;
        font-weight: bold;
        padding: 14px 24px;
        border: none;
        border-radius: 8px;
    }}
    QPushButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {ACCENT_HOVER_DARK}, stop:1 {ACCENT_HOVER});
    }}
    QPushButton:pressed {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {ACCENT_PRESSED_DARK}, stop:1 {ACCENT_PRESSED});
    }}
"""

RESET_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {BG_HOVER};
        color: {TEXT_MUTED};
        font-size: 14px;
        font-weight: bold;
        padding: 14px 18px;
        border: 1px solid {BORDER_HOVER};
        border-radius: 8px;
    }}
    QPushButton:hover {{
        background-color: {BG_ACTIVE};
        color: #ffffff;
        border: 1px solid {BORDER_ACTIVE};
    }}
"""

PROGRESS_BAR_DEFAULT_STYLE = f"""
    QProgressBar {{
        border: none;
        border-radius: 8px;
        background-color: {BG_ELEMENT};
    }}
    QProgressBar::chunk {{
        border-radius: 8px;
        background-color: {BG_ACTIVE};
    }}
"""


def progress_bar_style(color):
    return f"""
        QProgressBar {{
            border: none;
            border-radius: 8px;
            background-color: {BG_ELEMENT};
        }}
        QProgressBar::chunk {{
            border-radius: 8px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {color}88, stop:1 {color});
        }}
    """


def resistance_value_style(color):
    return f"font-size: 44px; font-weight: bold; color: {color};"


def resistance_desc_style(color):
    return f"font-size: 12px; color: {color}; font-weight: bold;"


def feedback_label_style(color, bg):
    return (
        f"font-size: 32px; font-weight: bold; color: {color};"
        f"padding: 20px; border-radius: 10px; background-color: {bg};"
        f"border: 2px solid {color}66;"
    )


def feedback_value_style(color):
    return f"font-size: 12px; color: {color};"


# Static variants for idle/cleared state
RESISTANCE_VALUE_IDLE = resistance_value_style(TEXT_DISABLED)
FEEDBACK_LABEL_IDLE = (
    f"font-size: 32px; font-weight: bold; color: {TEXT_DISABLED};"
    f"padding: 20px; border-radius: 10px; background-color: {BG_ELEMENT};"
)


def slider_label_html(name, unit):
    return (
        f"<b style='color:#ffffff; font-size:13px;'>{name}</b>"
        f"  <span style='color:{ACCENT}; font-size:12px;'>[{unit}]</span>"
    )


VALUE_LABEL_STYLE = f"color: {ACCENT}; font-weight: bold; font-size: 16px;"
RANGE_LABEL_STYLE = f"color: {TEXT_RANGE}; font-size: 10px;"
MODE_LABEL_HTML = "<b style='color:#ffffff; font-size:13px;'>Training Mode</b>"
ERROR_LABEL_STYLE = f"color: {COLOR_ERROR}; font-size: 12px; font-weight: bold;"
FEEDBACK_VALUE_IDLE_STYLE = f"font-size: 12px; color: {TEXT_DISABLED};"


# ── Matplotlib helpers ────────────────────────────────────────────────────

def apply_chart_dark_style(ax):
    ax.set_facecolor(CHART_BG)
    ax.tick_params(colors=CHART_TICK, labelsize=8)
    ax.xaxis.label.set_color(CHART_TEXT)
    ax.yaxis.label.set_color(CHART_TEXT)
    ax.title.set_color(CHART_TEXT)
    for spine in ax.spines.values():
        spine.set_color(CHART_GRID)
    ax.grid(True, alpha=0.25, color=CHART_GRID, linewidth=0.5)


def get_resistance_style(opor):
    for threshold, color, desc in RESISTANCE_LEVELS:
        if opor < threshold:
            return color, desc
    return COLOR_ERROR, 'High / Maximal'
