import os
import warnings

from config.logging_config import configure_logging
from src.core.fis_engine import IntelligentGymMachine
from src.visualization.plots import (
    plot_membership_functions,
    plot_surface_3d,
    simulate_exercise
)
from src.analysis.scenarios import run_scenarios_with_analysis
from src.analysis.experiments import run_experiments


warnings.filterwarnings('ignore')
logger = configure_logging()


def ensure_output_dir():
    """Upewnia sie, ze katalog output istnieje."""
    os.makedirs('output', exist_ok=True)


def main():
    """Glowna funkcja programu."""

    logger.info("%s", "=" * 70)
    logger.info("INTELIGENTNY SYSTEM STEROWANIA MASZYNA TRENINGOWA")
    logger.info("System wnioskowania rozmytego (FIS) typu Mamdani")
    logger.info("%s", "=" * 70)

    ensure_output_dir()

    logger.info("Inicjalizacja systemu FIS...")
    machine = IntelligentGymMachine()
    logger.info("System zainicjalizowany pomyslnie!")
    logger.info("  * Liczba zmiennych wejsciowych: %s", 5)
    logger.info("  * Liczba zmiennych wyjsciowych: %s", 2)
    logger.info("  * Liczba regul: %s", len(machine.rules))

    logger.info("[1/5] Generowanie wykresow funkcji przynaleznosci...")
    plot_membership_functions(machine, save_path='membership_functions.png', output_dir='output')

    logger.info("[2/5] Uruchamianie scenariuszy wnioskowania z analiza...")
    run_scenarios_with_analysis(machine)

    logger.info("[3/5] Generowanie powierzchni wnioskowania 3D...")
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

    logger.info("[4/5] Symulacja pelnego cwiczenia...")
    simulate_exercise(machine, tryb=2, serie=3, powtorzenia=10,
                     save_path='simulation_hipertrofia.png', output_dir='output')

    simulate_exercise(machine, tryb=1, serie=4, powtorzenia=5,
                     save_path='simulation_silowy.png', output_dir='output')

    logger.info("[5/5] Eksperymenty z roznymi typami funkcji przynaleznosci...")
    run_experiments(output_dir='output')

    logger.info("%s", "=" * 70)
    logger.info("TABELE FUNKCJI PRZYNALEZNOSCI:")
    logger.info("%s", "=" * 70)
    logger.info("\n%s", machine.get_membership_functions_table())


if __name__ == "__main__":
    main()
