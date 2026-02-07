import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from ..core.experimental import IntelligentGymMachineExperimental


def compare_membership_functions(output_dir='output'):
    print("\n" + "=" * 70)
    print("  EKSPERYMENT: POROWNANIE FUNKCJI PRZYNALEZNOSCI")
    print("=" * 70)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Porownanie typow funkcji przynaleznosci\n(na przykladzie zmiennej: Sila generowana [N])',
                 fontsize=14, fontweight='bold')

    mf_types = ['triangular', 'gaussian', 'gbell', 'sigmoid']
    mf_names_pl = {
        'triangular': 'Trojkatne/Trapezoidalne',
        'gaussian': 'Gaussowskie',
        'gbell': 'Generalized Bell',
        'sigmoid': 'Sigmoidalne'
    }
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    labels = ['bardzo_niska', 'niska', 'srednia', 'wysoka', 'bardzo_wysoka']

    for idx, mf_type in enumerate(mf_types):
        ax = axes[idx // 2, idx % 2]

        try:
            machine = IntelligentGymMachineExperimental(mf_type=mf_type)

            for i, label in enumerate(labels):
                ax.plot(machine.sila.universe, machine.sila[label].mf,
                       color=colors[i], linewidth=2, label=label.replace('_', ' '))

            ax.set_title(f'{mf_names_pl[mf_type]}', fontsize=12, fontweight='bold')
            ax.set_xlabel('Sila [N]')
            ax.set_ylabel('Stopien przynaleznosci')
            ax.set_ylim([0, 1.05])
            ax.grid(True, alpha=0.3)
            ax.legend(loc='upper right', fontsize=8)

            print(f"  [OK] {mf_names_pl[mf_type]}")

        except Exception as e:
            ax.text(0.5, 0.5, f'Blad: {str(e)[:50]}',
                   transform=ax.transAxes, ha='center', va='center')
            print(f"  [!] {mf_names_pl[mf_type]}: {e}")

    plt.tight_layout()
    save_path = f"{output_dir}/comparison_membership_functions.png"
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nZapisano: {save_path}")


def compare_inference_results(output_dir='output'):
    print("\n" + "=" * 70)
    print("  EKSPERYMENT: POROWNANIE WYNIKOW WNIOSKOWANIA")
    print("=" * 70)

    scenarios = [
        {'nazwa': 'Poczatek ruchu', 'sila': 350, 'predkosc': 0.4, 'faza': 15, 'zmeczenie': 5, 'tryb': 1},
        {'nazwa': 'Sticking point', 'sila': 180, 'predkosc': 0.25, 'faza': 50, 'zmeczenie': 30, 'tryb': 2},
        {'nazwa': 'Lockout', 'sila': 420, 'predkosc': 0.8, 'faza': 90, 'zmeczenie': 20, 'tryb': 1},
        {'nazwa': 'Zmeczenie', 'sila': 200, 'predkosc': 0.5, 'faza': 60, 'zmeczenie': 65, 'tryb': 2},
        {'nazwa': 'Wyczerpanie', 'sila': 120, 'predkosc': 0.15, 'faza': 40, 'zmeczenie': 90, 'tryb': 2},
    ]

    mf_types = ['triangular', 'gaussian', 'gbell', 'sigmoid']
    mf_names_pl = {
        'triangular': 'Trojkatne',
        'gaussian': 'Gaussowskie',
        'gbell': 'Gen. Bell',
        'sigmoid': 'Sigmoidalne'
    }

    systems = {}
    for mf_type in mf_types:
        try:
            systems[mf_type] = IntelligentGymMachineExperimental(mf_type=mf_type)
        except Exception as e:
            print(f"  [!] Blad tworzenia systemu {mf_type}: {e}")

    print("\n" + "-" * 100)
    header = f"{'Scenariusz':<20}"
    for mf_type in mf_types:
        header += f" | {mf_names_pl[mf_type]:^18}"
    print(header)
    print("-" * 100)

    results_data = {mf: [] for mf in mf_types}

    for scenario in scenarios:
        row = f"{scenario['nazwa']:<20}"

        for mf_type in mf_types:
            if mf_type in systems:
                try:
                    result = systems[mf_type].compute(
                        scenario['sila'], scenario['predkosc'],
                        scenario['faza'], scenario['zmeczenie'], scenario['tryb']
                    )
                    opor = result['opor']
                    results_data[mf_type].append(opor)
                    row += f" | Opor: {opor:5.1f}%     "
                except Exception:
                    row += f" | Blad            "
                    results_data[mf_type].append(None)
            else:
                row += f" | N/A              "
                results_data[mf_type].append(None)

        print(row)

    print("-" * 100)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax1 = axes[0]
    x = np.arange(len(scenarios))
    width = 0.2
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    for i, mf_type in enumerate(mf_types):
        values = [v if v is not None else 0 for v in results_data[mf_type]]
        ax1.bar(x + i * width, values, width, label=mf_names_pl[mf_type], color=colors[i])

    ax1.set_xlabel('Scenariusz')
    ax1.set_ylabel('Opor maszyny [%]')
    ax1.set_title('Porownanie wynikow wnioskowania\ndla roznych typow funkcji przynaleznosci')
    ax1.set_xticks(x + width * 1.5)
    ax1.set_xticklabels([s['nazwa'] for s in scenarios], rotation=15, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')

    ax2 = axes[1]
    std_results = []

    for i, scenario in enumerate(scenarios):
        vals = [results_data[mf][i] for mf in mf_types if results_data[mf][i] is not None]
        std_results.append(np.std(vals) if vals else 0)

    ax2.bar(x, std_results, color='#9467bd', alpha=0.7)
    ax2.set_xlabel('Scenariusz')
    ax2.set_ylabel('Odchylenie standardowe [%]')
    ax2.set_title('Rozrzut wynikow miedzy typami funkcji\n(miara wrazliwosci na wybor funkcji)')
    ax2.set_xticks(x)
    ax2.set_xticklabels([s['nazwa'] for s in scenarios], rotation=15, ha='right')
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    save_path = f"{output_dir}/comparison_inference_results.png"
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nZapisano: {save_path}")

    print("\n" + "=" * 70)
    print("  WNIOSKI Z EKSPERYMENTU")
    print("=" * 70)



def run_experiments(output_dir='output'):
    print("\n" + "=" * 70)
    print("  EKSPERYMENTY Z FUNKCJAMI PRZYNALEZNOSCI")
    print("  (trojkatne, gaussowskie, generalized bell, sigmoidalne)")
    print("=" * 70)

    compare_membership_functions(output_dir)
    compare_inference_results(output_dir)

    print("\n" + "=" * 70)
    print("  EKSPERYMENTY ZAKONCZONE")
    print("  Wygenerowane pliki:")
    print(f"    * {output_dir}/comparison_membership_functions.png")
    print(f"    * {output_dir}/comparison_inference_results.png")
    print("=" * 70 + "\n")
