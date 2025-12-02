# Inteligentny System Sterowania Maszyną Treningową

System wnioskowania rozmytego (FIS) typu Mamdani do dynamicznego sterowania oporem maszyny treningowej.

## Opis projektu

Projekt realizowany w ramach przedmiotu **Inżynieria wiedzy i systemy ekspertowe** na AGH.

System steruje maszyną do wyciskania (chest press) z silnikiem elektromagnetycznym, dynamicznie dostosowując opór w zależności od:
- Aktualnej siły generowanej przez użytkownika
- Prędkości wykonywania ruchu
- Fazy ruchu (pozycji w zakresie ROM)
- Poziomu zmęczenia użytkownika
- Wybranego trybu treningowego

## Struktura projektu

```
intelligent_gym_machine/
├── src/
│   ├── core/
│   │   ├── fis_engine.py      # Główny silnik FIS (klasa IntelligentGymMachine)
│   │   └── experimental.py     # Wersja eksperymentalna z różnymi funkcjami MF
│   ├── visualization/
│   │   └── plots.py           # Wykresy i wizualizacje
│   ├── analysis/
│   │   ├── scenarios.py       # Scenariusze wnioskowania
│   │   └── experiments.py     # Eksperymenty porównawcze
│   └── documentation/
│       └── generator.py       # Generator dokumentacji
├── output/                    # Wygenerowane pliki
├── main.py                    # Punkt wejścia
└── requirements.txt
```

## Instalacja

```bash
pip install -r requirements.txt
```

## Uruchomienie

```bash
python main.py
```

## Zmienne lingwistyczne

### Wejściowe
| Zmienna | Zakres | Jednostka | Opis |
|---------|--------|-----------|------|
| Siła generowana | 0-500 | N | Z czujnika tensometrycznego |
| Prędkość ruchu | 0-1.5 | m/s | Z enkodera liniowego |
| Faza ruchu | 0-100 | % ROM | Pozycja w zakresie ruchu |
| Wskaźnik zmęczenia | 0-100 | % | Spadek peak force |
| Tryb treningu | 1-3 | - | 1=siłowy, 2=hipertrofia, 3=wytrzymałość |

### Wyjściowe
| Zmienna | Zakres | Jednostka | Opis |
|---------|--------|-----------|------|
| Opór maszyny | 0-100 | % | Sygnał PWM do silnika |
| Sygnał feedbacku | 1-5 | - | 1=zwolnij, 3=idealnie, 5=stop |

## Baza reguł

System zawiera 30 reguł rozmytych opartych na wiedzy eksperckiej z zakresu:
- Biomechaniki treningu siłowego
- Zasady accommodating resistance
- Protokołów bezpieczeństwa

## Wygenerowane pliki

Po uruchomieniu w katalogu `output/` znajdziesz:

| Plik | Opis |
|------|------|
| `membership_functions.png` | Funkcje przynależności wszystkich zmiennych |
| `surface_sila_faza.png` | Powierzchnia 3D: siła vs faza |
| `surface_zmeczenie_predkosc.png` | Powierzchnia 3D: zmęczenie vs prędkość |
| `simulation_hipertrofia.png` | Symulacja treningu hipertrofii |
| `simulation_silowy.png` | Symulacja treningu siłowego |
| `comparison_membership_functions.png` | Porównanie typów funkcji MF |
| `comparison_inference_results.png` | Porównanie wyników wnioskowania |
| `dokumentacja_fis.txt` | Pełna dokumentacja do sprawozdania |

## Technologie

- Python 3.8+
- NumPy
- scikit-fuzzy
- Matplotlib

## Autor

Projekt studencki AGH - Inżynieria wiedzy i systemy ekspertowe

## Licencja

MIT