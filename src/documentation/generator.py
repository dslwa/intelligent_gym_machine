"""
Moduł generowania dokumentacji projektu.
"""

from ..core.fis_engine import IntelligentGymMachine
from ..analysis.scenarios import run_scenarios_with_analysis


def generate_full_documentation():
    """
    Generuje pełną dokumentację projektu zgodną z wymaganiami instrukcji.
    """
    machine = IntelligentGymMachine()
    doc = []

    # SEKCJA 1
    doc.append("""
================================================================================
1. WYBOR TEMATU I OPIS PROBLEMU
================================================================================

1.1 PROBLEM I ZASTOSOWANIE
--------------------------

a) Opis problemu:
   Projekt dotyczy inteligentnego sterowania maszyna treningowa do wyciskania
   (chest press) z silnikiem elektromagnetycznym. Problem polega na dynamicznym
   dostosowaniu oporu maszyny w czasie rzeczywistym.

b) Uzasadnienie wyboru logiki rozmytej:
   * Zmienne wejsciowe maja charakter ciagly i nieprecyzyjny
   * Decyzje sterujace wymagaja "miekkiego" przejscia miedzy stanami
   * Wiedza ekspercka jest wyrazana lingwistycznie
   * Brak precyzyjnego modelu matematycznego

c) Uzytkownik systemu:
   * Bezposredni: Maszyna treningowa (sterownik silnika)
   * Posredni: Osoba cwiczaca - otrzymuje feedback w czasie rzeczywistym

1.2 ZMIENNE WEJSCIOWE I WYJSCIOWE
---------------------------------

ZMIENNE WEJSCIOWE:
+---------------------+---------+-------------+--------------------------------+
| Zmienna             | Zakres  | Jednostka   | Sposob pozyskania              |
+---------------------+---------+-------------+--------------------------------+
| Sila generowana     | 0-500   | N           | Czujnik tensometryczny         |
| Predkosc ruchu      | 0-1.5   | m/s         | Enkoder liniowy                |
| Faza ruchu          | 0-100   | % ROM       | Enkoder katowy                 |
| Wskaznik zmeczenia  | 0-100   | %           | Obliczany ze spadku peak force |
| Tryb treningu       | 1-3     | -           | Wybor uzytkownika              |
+---------------------+---------+-------------+--------------------------------+

ZMIENNE WYJSCIOWE:
+---------------------+---------+-------------+--------------------------------+
| Zmienna             | Zakres  | Jednostka   | Sposob wykorzystania           |
+---------------------+---------+-------------+--------------------------------+
| Opor maszyny        | 0-100   | %           | Sygnal PWM do sterownika       |
| Sygnal feedbacku    | 1-5     | -           | Wyswietlacz LED dla uzytkownika|
+---------------------+---------+-------------+--------------------------------+
""")

    # SEKCJA 2
    doc.append("""
================================================================================
2. MODEL FIS
================================================================================

2.1 WYBOR TYPU SYSTEMU
----------------------

Typ modelu: MAMDANI

Uzasadnienie wyboru:
* Interpretowalnosc: Reguly Mamdaniego sa czytelne dla ekspertow
* Charakter wyjscia: Lepiej wyrazone przez zbiory rozmyte
* Zrodlo wiedzy: Wiedza pochodzi od ekspertow, nie od danych uczacych
* Brak danych uczacych: Nie dysponujemy danymi do treningu ANFIS

2.2 REPREZENTACJA ZMIENNYCH
---------------------------
""")

    doc.append(machine.get_membership_functions_table())

    doc.append("""
UZASADNIENIE WYBORU FUNKCJI PRZYNALEZNOSCI:

* Funkcje trapezoidalne (trapmf): Dla wartosci skrajnych
* Funkcje trojkatne (trimf): Dla wartosci posrednich
* Zachodzenie na siebie zbiorow: Zapewnia ciaglosc wnioskowania
""")

    # SEKCJA 2.3
    doc.append(machine.get_rules_documentation())

    # SEKCJA 3
    doc.append("""
================================================================================
3. WNIOSKOWANIE ROZMYTE - ANALIZA
================================================================================

3.1 SCENARIUSZE WNIOSKOWANIA
----------------------------
""")

    _, results, scenarios_text = run_scenarios_with_analysis(machine)
    doc.append(scenarios_text)

    doc.append("""
3.2 ANALIZA TRENDOW
-------------------

Na podstawie wygenerowanych powierzchni 3D mozna zaobserwowac:

a) Sila vs Faza ruchu:
   * Opor rosnie wraz z faza ruchu
   * Przy wyzszej sile system pozwala na wyzszy opor
   * Widoczna "dolina" w srodku zakresu fazy - sticking point

b) Zmeczenie vs Predkosc:
   * Opor maleje wraz ze wzrostem zmeczenia
   * Przy bardzo niskiej predkosci i wysokim zmeczeniu - minimalny opor

3.3 OCENA POPRAWNOSCI DZIALANIA
-------------------------------

Wyniki systemu sa zgodne z:
* Intuicja ekspercka
* Wiedza z literatury (Zatsiorsky, Schoenfeld, Kompf)
* Obserwacjami procesow treningowych
""")

    # SEKCJA 4
    doc.append("""
================================================================================
4. PODSUMOWANIE I WNIOSKI
================================================================================

4.1 DZIALANIE SYSTEMU
---------------------

Opracowany system FIS typu Mamdani realizuje inteligentne sterowanie maszyna
treningowa poprzez:
* Dynamiczna adaptacje oporu do aktualnej pozycji i sily uzytkownika
* Automatyczna kompensacje zmeczenia (drop-set)
* Dostosowanie do trzech trybow treningowych
* Generowanie feedbacku w czasie rzeczywistym

4.2 REALIZACJA CELOW
--------------------

[OK] Cel glowny: Zaprojektowano dzialajacy system FIS rozwiazujacy rzeczywisty
     problem sterowania maszyna treningowa.

[OK] Cele szczegolowe:
  - Zdefiniowano 5 zmiennych wejsciowych i 2 wyjsciowe
  - Opracowano 30 regul opartych na wiedzy eksperckiej
  - Zaimplementowano i przetestowano system w Pythonie
  - Wygenerowano wizualizacje i analizy dzialania

4.3 PRAKTYCZNE ZASTOSOWANIA
---------------------------

* Silownie komercyjne: Automatyzacja personalizacji treningu
* Rehabilitacja: Precyzyjna kontrola obciazenia
* Sport wyczynowy: Optymalizacja bodzca treningowego
* Trening domowy: Inteligentne maszyny bez potrzeby trenera

================================================================================
5. IMPLEMENTACJA
================================================================================

Forma implementacji: Python 3

Uzyte biblioteki:
* numpy - obliczenia numeryczne
* scikit-fuzzy - implementacja logiki rozmytej
* matplotlib - wizualizacje

Struktura projektu:
intelligent_gym_machine/
  src/
    core/         - glowne klasy FIS
    visualization/ - wykresy i wizualizacje
    analysis/      - scenariusze i eksperymenty
    documentation/ - generowanie dokumentacji
  output/          - wygenerowane pliki
  main.py          - punkt wejscia

Uruchomienie:
  pip install -r requirements.txt
  python main.py

================================================================================
""")

    return '\n'.join(doc)


def save_documentation(filepath='output/dokumentacja_fis.txt'):
    """Zapisuje pełną dokumentację do pliku."""
    doc = generate_full_documentation()
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(doc)
    print(f"Dokumentacja zapisana do: {filepath}")
    return filepath
