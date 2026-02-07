import os
import warnings
warnings.filterwarnings('ignore')

from src.core.fis_engine import IntelligentGymMachine
from src.visualization.plots import (
    plot_membership_functions,
    plot_surface_3d,
    simulate_exercise
)
from src.analysis.scenarios import run_scenarios_with_analysis
from src.analysis.experiments import run_experiments


def ensure_output_dir():
    """Upewnia się, że katalog output istnieje."""
    if not os.path.exists('output'):
        os.makedirs('output')


def main():
    """Główna funkcja programu."""

    print("\n" + "=" * 70)
    print("  INTELIGENTNY SYSTEM STEROWANIA MASZYNA TRENINGOWA")
    print("  System wnioskowania rozmytego (FIS) typu Mamdani")
    print("=" * 70 + "\n")

    ensure_output_dir()

    print("Inicjalizacja systemu FIS...")
    machine = IntelligentGymMachine()
    print(f"System zainicjalizowany pomyslnie!")
    print(f"  * Liczba zmiennych wejsciowych: 5")
    print(f"  * Liczba zmiennych wyjsciowych: 2")
    print(f"  * Liczba regul: {len(machine.rules)}")

    print("\n[1/5] Generowanie wykresow funkcji przynaleznosci...")
    plot_membership_functions(machine, save_path='membership_functions.png', output_dir='output')

    print("\n[2/5] Uruchamianie scenariuszy wnioskowania z analiza...")
    run_scenarios_with_analysis(machine)

    print("\n[3/5] Generowanie powierzchni wnioskowania 3D...")

    plot_surface_3d(
        machine,
        'sila', 'faza',
        (50, 450, 10), (0, 100, 2),
        {'predkosc': 0.6, 'zmeczenie': 30, 'tryb': 2},
        save_path='surface_sila_faza.png',
        output_dir='output'
    )

    plot_surface_3d(
        machine,
        'zmeczenie', 'predkosc',
        (0, 100, 2), (0.1, 1.4, 0.05),
        {'sila': 250, 'faza': 50, 'tryb': 2},
        save_path='surface_zmeczenie_predkosc.png',
        output_dir='output'
    )

    print("\n[4/5] Symulacja pelnego cwiczenia...")

    simulate_exercise(machine, tryb=2, serie=3, powtorzenia=10,
                     save_path='simulation_hipertrofia.png', output_dir='output')

    simulate_exercise(machine, tryb=1, serie=4, powtorzenia=5,
                     save_path='simulation_silowy.png', output_dir='output')

    print("\n[5/5] Eksperymenty z roznymi typami funkcji przynaleznosci...")
    run_experiments(output_dir='output')

    print("\n" + "=" * 70)
    print("TABELE FUNKCJI PRZYNALEZNOSCI:")
    print("=" * 70)
    print(machine.get_membership_functions_table())


if __name__ == "__main__":
    main()
