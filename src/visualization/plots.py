"""
Moduł wizualizacji - funkcje do generowania wykresów.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.ndimage import gaussian_filter

plt.rcParams['font.family'] = 'DejaVu Sans'


def plot_membership_functions(machine, save_path=None, output_dir='output'):
    fig = plt.figure(figsize=(16, 14))
    gs = GridSpec(4, 2, figure=fig, hspace=0.35, wspace=0.25)

    ax1 = fig.add_subplot(gs[0, 0])
    for label in machine.sila.terms:
        ax1.plot(machine.sila.universe, machine.sila[label].mf, linewidth=2, label=label)
    ax1.set_title('1. Sila generowana [N]', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Sila [N]')
    ax1.set_ylabel('Stopien przynaleznosci')
    ax1.legend(loc='upper right', fontsize=8)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-0.05, 1.1)

    ax2 = fig.add_subplot(gs[0, 1])
    for label in machine.predkosc.terms:
        ax2.plot(machine.predkosc.universe, machine.predkosc[label].mf, linewidth=2, label=label)
    ax2.set_title('2. Predkosc ruchu [m/s]', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Predkosc [m/s]')
    ax2.set_ylabel('Stopien przynaleznosci')
    ax2.legend(loc='upper right', fontsize=8)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-0.05, 1.1)

    ax3 = fig.add_subplot(gs[1, 0])
    for label in machine.faza.terms:
        ax3.plot(machine.faza.universe, machine.faza[label].mf, linewidth=2, label=label)
    ax3.set_title('3. Faza ruchu [% ROM]', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Faza ruchu [%]')
    ax3.set_ylabel('Stopien przynaleznosci')
    ax3.legend(loc='upper right', fontsize=8)
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(-0.05, 1.1)

    ax4 = fig.add_subplot(gs[1, 1])
    for label in machine.zmeczenie.terms:
        ax4.plot(machine.zmeczenie.universe, machine.zmeczenie[label].mf, linewidth=2, label=label)
    ax4.set_title('4. Wskaznik zmeczenia [%]', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Zmeczenie [%]')
    ax4.set_ylabel('Stopien przynaleznosci')
    ax4.legend(loc='upper right', fontsize=8)
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(-0.05, 1.1)

    ax5 = fig.add_subplot(gs[2, 0])
    for label in machine.tryb.terms:
        ax5.plot(machine.tryb.universe, machine.tryb[label].mf, linewidth=2, label=label)
    ax5.set_title('5. Tryb treningu', fontsize=12, fontweight='bold')
    ax5.set_xlabel('Tryb (1=silowy, 2=hipertrofia, 3=wytrzymalosc)')
    ax5.set_ylabel('Stopien przynaleznosci')
    ax5.legend(loc='upper right', fontsize=8)
    ax5.grid(True, alpha=0.3)
    ax5.set_ylim(-0.05, 1.1)

    ax6 = fig.add_subplot(gs[2, 1])
    for label in machine.opor.terms:
        ax6.plot(machine.opor.universe, machine.opor[label].mf, linewidth=2, label=label)
    ax6.set_title('6. Opor maszyny [%] - WYJSCIE', fontsize=12, fontweight='bold')
    ax6.set_xlabel('Opor [%]')
    ax6.set_ylabel('Stopien przynaleznosci')
    ax6.legend(loc='upper right', fontsize=8)
    ax6.grid(True, alpha=0.3)
    ax6.set_ylim(-0.05, 1.1)

    ax7 = fig.add_subplot(gs[3, 0])
    for label in machine.feedback.terms:
        ax7.plot(machine.feedback.universe, machine.feedback[label].mf, linewidth=2, label=label)
    ax7.set_title('7. Sygnal feedbacku - WYJSCIE', fontsize=12, fontweight='bold')
    ax7.set_xlabel('Feedback (1=zwolnij, 3=idealnie, 5=stop)')
    ax7.set_ylabel('Stopien przynaleznosci')
    ax7.legend(loc='upper right', fontsize=8)
    ax7.grid(True, alpha=0.3)
    ax7.set_ylim(-0.05, 1.1)

    ax8 = fig.add_subplot(gs[3, 1])
    ax8.axis('off')
    info_text = """
    SYSTEM FIS - INTELIGENTNA MASZYNA TRENINGOWA
    ============================================

    Typ systemu: Mamdani
    Metoda defuzyfikacji: Centroid
    Operatory:
      * AND (T-norma): minimum
      * OR (S-norma): maximum
      * Implikacja: minimum
      * Agregacja: maximum

    Zmienne wejsciowe: 5
    Zmienne wyjsciowe: 2
    Liczba regul: 30
    """
    ax8.text(0.1, 0.5, info_text, transform=ax8.transAxes, fontsize=10,
            verticalalignment='center', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))

    plt.suptitle('Funkcje przynaleznosci zmiennych lingwistycznych',
                fontsize=14, fontweight='bold', y=0.98)

    if save_path:
        full_path = f"{output_dir}/{save_path}" if output_dir else save_path
        plt.savefig(full_path, dpi=150, bbox_inches='tight')
        print(f"Zapisano wykres: {full_path}")

    plt.close()


def plot_surface_3d(machine, var1_name, var2_name, var1_range, var2_range,
                    fixed_values, save_path=None, output_dir='output', smooth=True):

    var1_start, var1_end, var1_step = var1_range
    var2_start, var2_end, var2_step = var2_range

    var1_step_fine = var1_step / 2
    var2_step_fine = var2_step / 2

    var1_vals = np.arange(var1_start, var1_end, var1_step_fine)
    var2_vals = np.arange(var2_start, var2_end, var2_step_fine)

    X, Y = np.meshgrid(var1_vals, var2_vals)
    Z_opor = np.zeros_like(X, dtype=float)
    Z_feedback = np.zeros_like(X, dtype=float)

    var_mapping = {
        'sila': 'sila_generowana',
        'predkosc': 'predkosc_ruchu',
        'faza': 'faza_ruchu',
        'zmeczenie': 'wskaznik_zmeczenia',
        'tryb': 'tryb_treningu'
    }

    for i in range(len(var2_vals)):
        for j in range(len(var1_vals)):
            machine.simulator.reset()

            for var, val in fixed_values.items():
                machine.simulator.input[var_mapping[var]] = val

            machine.simulator.input[var_mapping[var1_name]] = var1_vals[j]
            machine.simulator.input[var_mapping[var2_name]] = var2_vals[i]

            try:
                machine.simulator.compute()
                Z_opor[i, j] = machine.simulator.output['opor_maszyny']
                Z_feedback[i, j] = machine.simulator.output['sygnal_feedback']
            except Exception:
                Z_opor[i, j] = np.nan
                Z_feedback[i, j] = np.nan

    if smooth:
        Z_opor = np.nan_to_num(Z_opor, nan=np.nanmean(Z_opor))
        Z_feedback = np.nan_to_num(Z_feedback, nan=np.nanmean(Z_feedback))

        Z_opor = gaussian_filter(Z_opor, sigma=1.5)
        Z_feedback = gaussian_filter(Z_feedback, sigma=1.5)

    fig = plt.figure(figsize=(14, 6))

    ax1 = fig.add_subplot(121, projection='3d')
    surf1 = ax1.plot_surface(X, Y, Z_opor, cmap='viridis', edgecolor='none',
                              alpha=0.9, antialiased=True, rstride=1, cstride=1)
    ax1.set_xlabel(f'{var1_name}')
    ax1.set_ylabel(f'{var2_name}')
    ax1.set_zlabel('Opor [%]')
    ax1.set_title(f'Powierzchnia wnioskowania: Opor maszyny\n({var1_name} vs {var2_name})')
    fig.colorbar(surf1, ax=ax1, shrink=0.5, label='Opor [%]')

    ax2 = fig.add_subplot(122, projection='3d')
    surf2 = ax2.plot_surface(X, Y, Z_feedback, cmap='plasma', edgecolor='none',
                              alpha=0.9, antialiased=True, rstride=1, cstride=1)
    ax2.set_xlabel(f'{var1_name}')
    ax2.set_ylabel(f'{var2_name}')
    ax2.set_zlabel('Feedback')
    ax2.set_title(f'Powierzchnia wnioskowania: Feedback\n({var1_name} vs {var2_name})')
    fig.colorbar(surf2, ax=ax2, shrink=0.5, label='Feedback')

    fixed_str = ', '.join([f'{k}={v}' for k, v in fixed_values.items()])
    plt.suptitle(f'Ustalone wartosci: {fixed_str}', fontsize=10, y=0.02)

    plt.tight_layout()

    if save_path:
        full_path = f"{output_dir}/{save_path}" if output_dir else save_path
        plt.savefig(full_path, dpi=150, bbox_inches='tight')
        print(f"Zapisano wykres: {full_path}")

    plt.close()


def simulate_exercise(machine, tryb=2, serie=3, powtorzenia=10, save_path=None, output_dir='output'):

    tryb_nazwa = {1: 'Silowy', 2: 'Hipertrofia', 3: 'Wytrzymalosc'}

    results = {
        'time': [], 'seria': [], 'powtorzenie': [], 'faza': [],
        'sila': [], 'predkosc': [], 'zmeczenie': [], 'opor': [], 'feedback': []
    }

    t = 0
    base_sila = 300 if tryb == 1 else (250 if tryb == 2 else 200)
    base_predkosc = 0.5 if tryb == 1 else (0.7 if tryb == 2 else 1.0)

    for s in range(1, serie + 1):
        zmeczenie_base = (s - 1) * 25

        for p in range(1, powtorzenia + 1):
            zmeczenie = min(100, zmeczenie_base + (p - 1) * 3)

            for faza in np.linspace(0, 100, 20):
                sila_mod = np.sin(np.pi * faza / 100) * 0.5 + 0.5
                sila = base_sila * sila_mod * (1 - zmeczenie/200)

                predkosc = base_predkosc * (1 - zmeczenie/300) * (1 - abs(faza - 50)/150)
                predkosc = max(0.05, min(1.45, predkosc))

                result = machine.compute(sila, predkosc, faza, zmeczenie, tryb)

                results['time'].append(t)
                results['seria'].append(s)
                results['powtorzenie'].append(p)
                results['faza'].append(faza)
                results['sila'].append(sila)
                results['predkosc'].append(predkosc)
                results['zmeczenie'].append(zmeczenie)
                results['opor'].append(result['opor'])
                results['feedback'].append(result['feedback'])

                t += 0.05

    fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)
    time = np.array(results['time'])

    ax1 = axes[0]
    ax1.plot(time, results['sila'], 'b-', label='Sila generowana [N]', linewidth=1)
    ax1_twin = ax1.twinx()
    ax1_twin.plot(time, results['opor'], 'r-', label='Opor maszyny [%]', linewidth=1)
    ax1.set_ylabel('Sila [N]', color='blue')
    ax1_twin.set_ylabel('Opor [%]', color='red')
    ax1.legend(loc='upper left')
    ax1_twin.legend(loc='upper right')
    ax1.set_title(f'Symulacja cwiczenia: Chest Press | Tryb: {tryb_nazwa[tryb]} | {serie} serie x {powtorzenia} powtorzen')
    ax1.grid(True, alpha=0.3)

    ax2 = axes[1]
    ax2.plot(time, results['predkosc'], 'g-', label='Predkosc [m/s]', linewidth=1)
    ax2_twin = ax2.twinx()
    ax2_twin.plot(time, results['faza'], 'm-', label='Faza ruchu [%]', linewidth=1, alpha=0.5)
    ax2.set_ylabel('Predkosc [m/s]', color='green')
    ax2_twin.set_ylabel('Faza [%]', color='purple')
    ax2.legend(loc='upper left')
    ax2_twin.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)

    ax3 = axes[2]
    ax3.fill_between(time, results['zmeczenie'], alpha=0.3, color='orange')
    ax3.plot(time, results['zmeczenie'], 'orange', label='Wskaznik zmeczenia [%]', linewidth=1)
    ax3.set_ylabel('Zmeczenie [%]')
    ax3.legend(loc='upper left')
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 105)

    ax4 = axes[3]
    feedback_colors = ['red' if f < 1.5 else 'green' if f < 2.5 else 'blue' if f < 3.5 else 'yellow' if f < 4.5 else 'red'
                      for f in results['feedback']]
    ax4.scatter(time, results['feedback'], c=feedback_colors, s=2, alpha=0.5)
    ax4.axhline(y=1, color='red', linestyle='--', alpha=0.3, label='Zwolnij')
    ax4.axhline(y=3, color='blue', linestyle='--', alpha=0.3, label='Idealnie')
    ax4.axhline(y=5, color='red', linestyle='--', alpha=0.3, label='Stop')
    ax4.set_ylabel('Feedback')
    ax4.set_xlabel('Czas [s]')
    ax4.legend(loc='upper right')
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(0.5, 5.5)

    serie_changes = [0]
    for i in range(1, len(results['seria'])):
        if results['seria'][i] != results['seria'][i-1]:
            serie_changes.append(i)

    for ax in axes:
        for idx in serie_changes[1:]:
            ax.axvline(x=time[idx], color='gray', linestyle=':', alpha=0.5)

    plt.tight_layout()

    if save_path:
        full_path = f"{output_dir}/{save_path}" if output_dir else save_path
        plt.savefig(full_path, dpi=150, bbox_inches='tight')
        print(f"Zapisano wykres: {full_path}")

    plt.close()

    return results
