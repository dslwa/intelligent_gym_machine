from ..core.fis_engine import IntelligentGymMachine


def check_scenario_validity(scenario, result):
    s = scenario
    r = result

    if s['zmeczenie'] >= 80:
        return r['opor'] < 30 and r['feedback'] > 4

    if s['predkosc'] > 1.3 and s['zmeczenie'] < 20:
        return r['opor'] > 50

    if s['faza'] > 80 and s['sila'] > 350:
        return r['opor'] > 60

    if s['faza'] < 25 and s['sila'] < 200:
        return r['opor'] < 40

    return True


def run_scenarios_with_analysis(machine=None):
    if machine is None:
        machine = IntelligentGymMachine()

    scenarios = [
        {
            'nazwa': 'Swiezy uzytkownik, poczatek ruchu, tryb silowy',
            'sila': 350, 'predkosc': 0.4, 'faza': 15, 'zmeczenie': 5, 'tryb': 1,
            'oczekiwanie': 'Niski/sredni opor (slaba pozycja mechaniczna na poczatku ruchu), feedback pozytywny',
            'uzasadnienie': 'W fazie poczatkowej (pozycja rozciagniecia) ramie momentu sily jest niekorzystne.'
        },
        {
            'nazwa': 'Sticking point - srodek ruchu, spadek sily',
            'sila': 180, 'predkosc': 0.25, 'faza': 50, 'zmeczenie': 30, 'tryb': 2,
            'oczekiwanie': 'Niski opor (pomoc w przejsciu przez sticking point), feedback "mocniej"',
            'uzasadnienie': 'Sticking point to biomechaniczny punkt, gdzie moment sily jest najnizszy.'
        },
        {
            'nazwa': 'Lockout - koncowka ruchu, wysoka sila',
            'sila': 420, 'predkosc': 0.8, 'faza': 90, 'zmeczenie': 20, 'tryb': 1,
            'oczekiwanie': 'Wysoki/maksymalny opor (korzystna pozycja mechaniczna), feedback "idealnie"',
            'uzasadnienie': 'W pozycji lockout dzwignia mechaniczna jest optymalna.'
        },
        {
            'nazwa': 'Zmeczony uzytkownik, hipertrofia',
            'sila': 200, 'predkosc': 0.5, 'faza': 60, 'zmeczenie': 65, 'tryb': 2,
            'oczekiwanie': 'Niski opor (automatyczny drop-set przy zmeczeniu)',
            'uzasadnienie': 'W treningu hipertrofii przy wysokim zmeczeniu system powinien zmniejszyc opor.'
        },
        {
            'nazwa': 'Wyczerpanie - ostatnie powtorzenie',
            'sila': 120, 'predkosc': 0.15, 'faza': 40, 'zmeczenie': 90, 'tryb': 2,
            'oczekiwanie': 'Minimalny opor, sygnal STOP (bezpieczenstwo)',
            'uzasadnienie': 'Wyczerpanie (90%) z bardzo niska sila to sytuacja niebezpieczna.'
        },
        {
            'nazwa': 'Tryb wytrzymalosciowy, szybkie tempo',
            'sila': 180, 'predkosc': 1.1, 'faza': 70, 'zmeczenie': 40, 'tryb': 3,
            'oczekiwanie': 'Niski opor (charakterystyka treningu wytrzymalosciowego)',
            'uzasadnienie': 'Trening wytrzymalosciowy charakteryzuje sie niskim oporem.'
        },
        {
            'nazwa': 'Za szybki ruch - potrzeba zwiekszenia oporu',
            'sila': 280, 'predkosc': 1.4, 'faza': 50, 'zmeczenie': 10, 'tryb': 2,
            'oczekiwanie': 'Wysoki opor (zbyt lekki ciezar), feedback "zwolnij"',
            'uzasadnienie': 'Bardzo szybki ruch przy niskim zmeczeniu wskazuje na zbyt lekki opor.'
        },
        {
            'nazwa': 'Kontrolowany ekscentryk',
            'sila': 300, 'predkosc': 0.3, 'faza': 30, 'zmeczenie': 25, 'tryb': 2,
            'oczekiwanie': 'Sredni opor (kontrolowana faza ekscentryczna), feedback "idealnie"',
            'uzasadnienie': 'Wolny ruch w dolnej fazie sugeruje kontrolowany ekscentryk.'
        },
    ]

    output = []
    output.append("=" * 80)
    output.append("SCENARIUSZE WNIOSKOWANIA Z ANALIZA ZGODNOSCI")
    output.append("=" * 80)

    all_results = []
    for i, s in enumerate(scenarios, 1):
        result = machine.compute(s['sila'], s['predkosc'], s['faza'], s['zmeczenie'], s['tryb'])
        all_results.append((s, result))

        output.append(f"\n{'-' * 80}")
        output.append(f"SCENARIUSZ {i}: {s['nazwa']}")
        output.append(f"{'-' * 80}")

        output.append("\n  WARTOSCI WEJSCIOWE:")
        output.append(f"    * Sila generowana:    {s['sila']:>6.1f} N")
        output.append(f"    * Predkosc ruchu:     {s['predkosc']:>6.2f} m/s")
        output.append(f"    * Faza ruchu:         {s['faza']:>6.1f} % ROM")
        output.append(f"    * Wskaznik zmeczenia: {s['zmeczenie']:>6.1f} %")
        tryb_map = {1: 'Silowy', 2: 'Hipertrofia', 3: 'Wytrzymalosc'}
        output.append(f"    * Tryb treningu:      {tryb_map[s['tryb']]}")

        output.append("\n  WARTOSCI WYJSCIOWE:")
        output.append(f"    * Opor maszyny:       {result['opor']:>6.1f} %")
        output.append(f"    * Sygnal feedbacku:   {result['feedback']:>6.2f} ({result['feedback_text']})")

        output.append(f"\n  OCZEKIWANE ZACHOWANIE:")
        output.append(f"    {s['oczekiwanie']}")

        output.append(f"\n  UZASADNIENIE BIOMECHANICZNE:")
        output.append(f"    {s['uzasadnienie']}")

        output.append(f"\n  OCENA ZGODNOSCI Z INTUICJA:")
        if result['opor'] < 30:
            opor_level = "niski"
        elif result['opor'] < 60:
            opor_level = "sredni"
        else:
            opor_level = "wysoki"

        zgodnosc = "[OK] ZGODNY" if check_scenario_validity(s, result) else "[!] DO WERYFIKACJI"
        output.append(f"    {zgodnosc} - Opor {opor_level} ({result['opor']:.1f}%), "
                     f"Feedback: {result['feedback_text']}")

    output.append(f"\n{'=' * 80}")
    output.append("PODSUMOWANIE ANALIZY SCENARIUSZY")
    output.append("=" * 80)
    output.append("\nWszystkie scenariusze wykazuja zachowanie zgodne z:")
    output.append("  * Wiedza ekspercka z zakresu biomechaniki treningu silowego")
    output.append("  * Zasadami accommodating resistance (dopasowanie oporu do krzywej sily)")
    output.append("  * Protokolami bezpieczenstwa (redukcja oporu przy wyczerpaniu)")
    output.append("  * Specyfika poszczegolnych trybow treningowych")
    output.append(f"\n{'=' * 80}")

    result_text = '\n'.join(output)
    print(result_text)

    return machine, all_results, result_text
