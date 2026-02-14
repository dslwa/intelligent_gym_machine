from typing import Optional, Tuple

import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.services.fis_service import FISResult, FISService, MembershipPlotData


# Color palette for dark mode visualizations
DARK_BG = '#111111'
DARK_FACE = '#0d0d0d'
DARK_TEXT = '#ffffff'
DARK_GRID = '#333333'
DARK_TICK = '#cccccc'
ACCENT_COLORS = ['#00e5ff', '#FF9800', '#4CAF50', '#BB86FC', '#FF5252',
                 '#FFD600', '#00E676', '#E040FB']


def apply_dark_style(ax):
    ax.set_facecolor(DARK_BG)
    ax.tick_params(colors=DARK_TICK, labelsize=8)
    ax.xaxis.label.set_color(DARK_TEXT)
    ax.yaxis.label.set_color(DARK_TEXT)
    ax.title.set_color(DARK_TEXT)
    for spine in ax.spines.values():
        spine.set_color(DARK_GRID)
    ax.grid(True, alpha=0.25, color=DARK_GRID, linewidth=0.5)


class MembershipFunctionsTab(QWidget):

    def __init__(self, membership_data: Tuple[MembershipPlotData, ...], rule_count: int):
        super().__init__()
        self.membership_data = membership_data
        self.rule_count = rule_count

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        self.figure = Figure(figsize=(12, 10), dpi=100, facecolor=DARK_FACE)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self._draw()

    def update_membership_data(self, membership_data: Tuple[MembershipPlotData, ...], rule_count: int):
        self.membership_data = membership_data
        self.rule_count = rule_count
        self._draw()

    def _draw(self):
        self.figure.clear()

        for idx, variable in enumerate(self.membership_data):
            ax = self.figure.add_subplot(4, 2, idx + 1)
            apply_dark_style(ax)

            for term_idx, term in enumerate(variable.terms):
                color = ACCENT_COLORS[term_idx % len(ACCENT_COLORS)]
                ax.plot(variable.universe, term.membership, linewidth=2.0,
                        label=term.name, color=color)
                ax.fill_between(variable.universe, term.membership, alpha=0.1, color=color)

            ax.set_title(variable.label, fontsize=10, fontweight='bold', color=DARK_TEXT)
            ax.set_ylabel('\u03bc', fontsize=10, color='#cccccc')
            ax.legend(fontsize=7, loc='upper right', facecolor='#1a1a1a',
                      edgecolor='#333333', labelcolor='#ffffff')
            ax.set_ylim(-0.05, 1.1)

        ax_info = self.figure.add_subplot(4, 2, 8)
        ax_info.set_facecolor(DARK_BG)
        ax_info.axis('off')
        info_text = (
            "FIS CONFIGURATION\n"
            "──────────────────────\n"
            "Type:       Mamdani\n"
            "Defuzz:     Centroid\n"
            "T-norm:     min\n"
            "S-norm:     max\n"
            "Implication: min\n"
            "Aggregation: max\n"
            f"Rules:      {self.rule_count}"
        )
        ax_info.text(0.5, 0.5, info_text, transform=ax_info.transAxes, fontsize=10,
                     verticalalignment='center', horizontalalignment='center',
                     fontfamily='monospace', color='#00e5ff',
                     bbox=dict(boxstyle='round,pad=0.8', facecolor='#1a1a1a',
                               edgecolor='#333333', linewidth=1))

        self.figure.tight_layout()
        self.canvas.draw()


class DefuzzificationTab(QWidget):

    def __init__(self, membership_data: Tuple[MembershipPlotData, ...]):
        super().__init__()
        self.membership_data = membership_data

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        self.figure = Figure(figsize=(10, 5), dpi=100, facecolor=DARK_FACE)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self._draw_empty()

    def update_membership_data(self, membership_data: Tuple[MembershipPlotData, ...]):
        self.membership_data = membership_data
        self._draw_empty()

    def _find_variable(self, identifier: str) -> Optional[MembershipPlotData]:
        return next((item for item in self.membership_data if item.identifier == identifier), None)

    def _draw_empty(self):
        self.figure.clear()

        for idx, (identifier, title) in enumerate([
            ('opor', 'Machine Resistance [%]'),
            ('feedback', 'Feedback Signal')
        ]):
            ax = self.figure.add_subplot(1, 2, idx + 1)
            var_data = self._find_variable(identifier)
            apply_dark_style(ax)

            if var_data is not None:
                for term_idx, term in enumerate(var_data.terms):
                    color = ACCENT_COLORS[term_idx % len(ACCENT_COLORS)]
                    ax.plot(var_data.universe, term.membership, linewidth=1.8,
                            label=term.name, alpha=0.4, color=color)

            ax.set_title(title, fontweight='bold', fontsize=12, color=DARK_TEXT)
            ax.set_ylabel('\u03bc', fontsize=10)
            ax.legend(fontsize=9, facecolor='#1a1a1a', edgecolor='#333333',
                      labelcolor='#ffffff')
            ax.set_ylim(-0.05, 1.1)

        self.figure.suptitle('Click EVALUATE to see defuzzification results',
                             color='#666666', fontsize=12, fontweight='bold')
        self.figure.tight_layout()
        self.canvas.draw()

    def update_results(self, result: FISResult):
        self.figure.clear()

        for idx, (identifier, value, title, fmt) in enumerate([
            ('opor', result.resistance, 'Machine Resistance [%]', '.1f'),
            ('feedback', result.feedback, 'Feedback Signal', '.2f'),
        ]):
            var_data = self._find_variable(identifier)
            ax = self.figure.add_subplot(1, 2, idx + 1)
            apply_dark_style(ax)

            if var_data is not None:
                for term_idx, term in enumerate(var_data.terms):
                    color = ACCENT_COLORS[term_idx % len(ACCENT_COLORS)]
                    ax.plot(var_data.universe, term.membership, linewidth=1.8,
                            label=term.name, alpha=0.35, color=color)
                    ax.fill_between(var_data.universe, term.membership, alpha=0.05, color=color)

                ax.axvline(x=value, color='#FF5252', linewidth=3, linestyle='--',
                           label=f'Result: {value:{fmt}}', zorder=10)
                ax.fill_betweenx([0, 1.1], value - 1.5, value + 1.5,
                                 alpha=0.2, color='#FF5252', zorder=5)

            ax.set_title(title, fontweight='bold', fontsize=12, color=DARK_TEXT)
            ax.set_ylabel('\u03bc', fontsize=10)
            ax.legend(fontsize=9, facecolor='#1a1a1a', edgecolor='#333333',
                      labelcolor='#ffffff')
            ax.set_ylim(-0.05, 1.1)

        self.figure.tight_layout()
        self.canvas.draw()


class VisualizationPanel(QWidget):

    def __init__(self, service: FISService):
        super().__init__()
        self.service = service
        self.membership_data = service.get_membership_plot_data()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()

        self.mf_tab = MembershipFunctionsTab(self.membership_data, service.rule_count)
        self.defuzz_tab = DefuzzificationTab(self.membership_data)

        self.tabs.addTab(self.mf_tab, "Membership Functions")
        self.tabs.addTab(self.defuzz_tab, "Defuzzification")

        layout.addWidget(self.tabs)

    def refresh_membership_data(self):
        self.membership_data = self.service.get_membership_plot_data()
        self.mf_tab.update_membership_data(self.membership_data, self.service.rule_count)
        self.defuzz_tab.update_membership_data(self.membership_data)

    def update_results(self, result: FISResult):
        self.defuzz_tab.update_results(result)
