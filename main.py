"""
============================================================================
INTELIGENTNY SYSTEM STEROWANIA MASZYNĄ TRENINGOWĄ Z DYNAMICZNYM OPOREM
System wnioskowania rozmytego (FIS) typu Mamdani
============================================================================
Przedmiot: Inżynieria wiedzy i systemy ekspertowe
Temat: Logika rozmyta jako forma reprezentacji wiedzy w systemach sterowania

Uruchomienie:
    python main.py
============================================================================
"""

import os
import warnings
warnings.filterwarnings('ignore')

# Importy z modułów projektu
from src.core.fis_engine import IntelligentGymMachine
from src.visualization.plots import (
    plot_membership_functions,
    plot_surface_3d,
    simulate_exercise
)
from src.analysis.scenarios import run_scenarios_with_analysis
from src.analysis.experiments import run_experiments
from src.documentation.generator import save_documentation


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

    # Przygotowanie katalogów
    ensure_output_dir()

    # Inicjalizacja systemu
    print("Inicjalizacja systemu FIS...")
    machine = IntelligentGymMachine()
    print(f"System zainicjalizowany pomyslnie!")
    print(f"  * Liczba zmiennych wejsciowych: 5")
    print(f"  * Liczba zmiennych wyjsciowych: 2")
    print(f"  * Liczba regul: {len(machine.rules)}")

    # 1. Wykresy funkcji przynależności
    print("\n[1/6] Generowanie wykresow funkcji przynaleznosci...")
    plot_membership_functions(machine, save_path='membership_functions.png', output_dir='output')

    # 2. Scenariusze wnioskowania z analizą
    print("\n[2/6] Uruchamianie scenariuszy wnioskowania z analiza...")
    run_scenarios_with_analysis(machine)

    # 3. Powierzchnie 3D
    print("\n[3/6] Generowanie powierzchni wnioskowania 3D...")

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

    # 4. Symulacja ćwiczenia
    print("\n[4/6] Symulacja pelnego cwiczenia...")

    simulate_exercise(machine, tryb=2, serie=3, powtorzenia=10,
                     save_path='simulation_hipertrofia.png', output_dir='output')

    simulate_exercise(machine, tryb=1, serie=4, powtorzenia=5,
                     save_path='simulation_silowy.png', output_dir='output')

    # 5. Generowanie dokumentacji
    print("\n[5/6] Generowanie pelnej dokumentacji projektu...")
    save_documentation('output/dokumentacja_fis.txt')

    # 6. Eksperymenty z funkcjami przynależności
    print("\n[6/6] Eksperymenty z roznymi typami funkcji przynaleznosci...")
    run_experiments(output_dir='output')

    # Wyświetl tabele funkcji przynależności
    print("\n" + "=" * 70)
    print("TABELE FUNKCJI PRZYNALEZNOSCI:")
    print("=" * 70)
    print(machine.get_membership_functions_table())

    print("\n" + "=" * 70)
    print("  ZAKONCZONO POMYSLNIE")
    print("  Wygenerowane pliki w katalogu 'output/':")
    print("    * membership_functions.png")
    print("    * surface_sila_faza.png")
    print("    * surface_zmeczenie_predkosc.png")
    print("    * simulation_hipertrofia.png")
    print("    * simulation_silowy.png")
    print("    * dokumentacja_fis.txt  <-- PELNA DOKUMENTACJA DO SPRAWOZDANIA")
    print("    * comparison_membership_functions.png  <-- POROWNANIE FUNKCJI")
    print("    * comparison_inference_results.png     <-- POROWNANIE WYNIKOW")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
