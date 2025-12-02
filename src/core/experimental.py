"""
Eksperymentalna wersja systemu FIS z różnymi typami funkcji przynależności.
Pozwala na porównanie: trójkątnych, Gaussowskich, Generalized Bell i sigmoidalnych.
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class IntelligentGymMachineExperimental:
    """
    Eksperymentalna wersja systemu FIS z różnymi typami funkcji przynależności.
    """

    FUNCTION_TYPES = ['triangular', 'gaussian', 'gbell', 'sigmoid']

    def __init__(self, mf_type='triangular'):
        """
        Inicjalizacja systemu FIS z wybranym typem funkcji przynależności.

        Args:
            mf_type: 'triangular' (domyślny), 'gaussian', 'gbell', 'sigmoid'
        """
        self.mf_type = mf_type
        self.setup_variables()
        self.setup_membership_functions()
        self.setup_rules()
        self.build_system()

    def setup_variables(self):
        """Definicja zmiennych lingwistycznych."""
        self.sila = ctrl.Antecedent(np.arange(0, 501, 1), 'sila_generowana')
        self.predkosc = ctrl.Antecedent(np.arange(0, 1.51, 0.01), 'predkosc_ruchu')
        self.faza = ctrl.Antecedent(np.arange(0, 101, 1), 'faza_ruchu')
        self.zmeczenie = ctrl.Antecedent(np.arange(0, 101, 1), 'wskaznik_zmeczenia')
        self.tryb = ctrl.Antecedent(np.arange(1, 3.01, 0.01), 'tryb_treningu')
        self.opor = ctrl.Consequent(np.arange(0, 101, 1), 'opor_maszyny')
        self.feedback = ctrl.Consequent(np.arange(1, 5.01, 0.01), 'sygnal_feedback')

    def _create_mf(self, universe, centers, names, is_boundary=None):
        """
        Tworzy funkcje przynależności według wybranego typu.
        """
        result = {}
        n = len(centers)
        if is_boundary is None:
            is_boundary = [False] * n
            is_boundary[0] = 'left'
            is_boundary[-1] = 'right'

        for i, (center, name) in enumerate(zip(centers, names)):
            if i == 0:
                width = (centers[1] - centers[0]) * 0.6
            elif i == n - 1:
                width = (centers[-1] - centers[-2]) * 0.6
            else:
                width = min(centers[i] - centers[i-1], centers[i+1] - centers[i]) * 0.6

            if self.mf_type == 'triangular':
                if is_boundary[i] == 'left':
                    left = universe.min()
                    result[name] = fuzz.trapmf(universe, [left, left, center, center + width * 1.5])
                elif is_boundary[i] == 'right':
                    right = universe.max()
                    result[name] = fuzz.trapmf(universe, [center - width * 1.5, center, right, right])
                else:
                    result[name] = fuzz.trimf(universe, [center - width * 1.5, center, center + width * 1.5])

            elif self.mf_type == 'gaussian':
                sigma = width * 0.8
                result[name] = fuzz.gaussmf(universe, center, sigma)

            elif self.mf_type == 'gbell':
                a = width * 1.2
                b = 2.5
                result[name] = fuzz.gbellmf(universe, a, b, center)

            elif self.mf_type == 'sigmoid':
                steepness = 0.1 / width if width > 0 else 0.1
                if is_boundary[i] == 'left':
                    result[name] = fuzz.sigmf(universe, center + width, -steepness * 5)
                elif is_boundary[i] == 'right':
                    result[name] = fuzz.sigmf(universe, center - width, steepness * 5)
                else:
                    sig1 = fuzz.sigmf(universe, center - width, steepness * 5)
                    sig2 = fuzz.sigmf(universe, center + width, -steepness * 5)
                    result[name] = sig1 * sig2

        return result

    def setup_membership_functions(self):
        """Definicja funkcji przynależności według wybranego typu."""

        # 1. SIŁA GENEROWANA
        sila_mf = self._create_mf(
            self.sila.universe,
            [50, 125, 250, 375, 450],
            ['bardzo_niska', 'niska', 'srednia', 'wysoka', 'bardzo_wysoka']
        )
        for name, mf in sila_mf.items():
            self.sila[name] = mf

        # 2. PRĘDKOŚĆ RUCHU
        predkosc_mf = self._create_mf(
            self.predkosc.universe,
            [0.1, 0.35, 0.7, 1.1, 1.4],
            ['bardzo_wolna', 'wolna', 'umiarkowana', 'szybka', 'bardzo_szybka']
        )
        for name, mf in predkosc_mf.items():
            self.predkosc[name] = mf

        # 3. FAZA RUCHU
        faza_mf = self._create_mf(
            self.faza.universe,
            [10, 30, 50, 70, 90],
            ['poczatkowa', 'dolna', 'srodkowa', 'gorna', 'koncowa']
        )
        for name, mf in faza_mf.items():
            self.faza[name] = mf

        # 4. WSKAŹNIK ZMĘCZENIA
        zmeczenie_mf = self._create_mf(
            self.zmeczenie.universe,
            [5, 25, 50, 75, 90],
            ['swiezy', 'lekkie', 'umiarkowane', 'wysokie', 'wyczerpanie']
        )
        for name, mf in zmeczenie_mf.items():
            self.zmeczenie[name] = mf

        # 5. TRYB TRENINGU (zawsze trójkątne)
        self.tryb['silowy'] = fuzz.trimf(self.tryb.universe, [1, 1, 1.8])
        self.tryb['hipertrofia'] = fuzz.trimf(self.tryb.universe, [1.5, 2, 2.5])
        self.tryb['wytrzymalosc'] = fuzz.trimf(self.tryb.universe, [2.2, 3, 3])

        # 6. OPÓR MASZYNY
        opor_mf = self._create_mf(
            self.opor.universe,
            [10, 30, 50, 70, 90],
            ['minimalny', 'niski', 'sredni', 'wysoki', 'maksymalny']
        )
        for name, mf in opor_mf.items():
            self.opor[name] = mf

        # 7. SYGNAŁ FEEDBACKU (zawsze trójkątne)
        self.feedback['zwolnij'] = fuzz.trimf(self.feedback.universe, [1, 1, 2])
        self.feedback['dobrze'] = fuzz.trimf(self.feedback.universe, [1.5, 2.5, 3.5])
        self.feedback['idealnie'] = fuzz.trimf(self.feedback.universe, [2.5, 3, 3.5])
        self.feedback['mocniej'] = fuzz.trimf(self.feedback.universe, [3, 3.5, 4.5])
        self.feedback['stop'] = fuzz.trimf(self.feedback.universe, [4, 5, 5])

    def setup_rules(self):
        """Definicja bazy reguł (uproszczona wersja)."""
        self.rules = []

        # Reguły dla accommodating resistance
        self.rules.append(ctrl.Rule(
            self.faza['poczatkowa'] & self.sila['srednia'],
            (self.opor['niski'], self.feedback['dobrze'])
        ))
        self.rules.append(ctrl.Rule(
            self.faza['dolna'] & self.sila['srednia'],
            (self.opor['sredni'], self.feedback['dobrze'])
        ))
        self.rules.append(ctrl.Rule(
            self.faza['srodkowa'] & self.sila['niska'],
            (self.opor['niski'], self.feedback['mocniej'])
        ))
        self.rules.append(ctrl.Rule(
            self.faza['srodkowa'] & self.sila['srednia'],
            (self.opor['sredni'], self.feedback['idealnie'])
        ))
        self.rules.append(ctrl.Rule(
            self.faza['gorna'] & self.sila['wysoka'],
            (self.opor['wysoki'], self.feedback['idealnie'])
        ))
        self.rules.append(ctrl.Rule(
            self.faza['koncowa'] & self.sila['bardzo_wysoka'],
            (self.opor['maksymalny'], self.feedback['idealnie'])
        ))

        # Reguły dla prędkości
        self.rules.append(ctrl.Rule(
            self.predkosc['bardzo_szybka'] & self.zmeczenie['swiezy'],
            (self.opor['wysoki'], self.feedback['zwolnij'])
        ))
        self.rules.append(ctrl.Rule(
            self.predkosc['bardzo_wolna'] & self.zmeczenie['swiezy'],
            (self.opor['niski'], self.feedback['mocniej'])
        ))

        # Reguły dla zmęczenia
        self.rules.append(ctrl.Rule(
            self.zmeczenie['wyczerpanie'],
            (self.opor['minimalny'], self.feedback['stop'])
        ))
        self.rules.append(ctrl.Rule(
            self.zmeczenie['wysokie'] & self.sila['niska'],
            (self.opor['niski'], self.feedback['mocniej'])
        ))
        self.rules.append(ctrl.Rule(
            self.zmeczenie['umiarkowane'] & self.tryb['hipertrofia'],
            (self.opor['sredni'], self.feedback['idealnie'])
        ))

        # Reguły dla trybów
        self.rules.append(ctrl.Rule(
            self.tryb['silowy'] & self.sila['bardzo_wysoka'],
            (self.opor['maksymalny'], self.feedback['idealnie'])
        ))
        self.rules.append(ctrl.Rule(
            self.tryb['wytrzymalosc'],
            (self.opor['niski'], self.feedback['dobrze'])
        ))

        # Reguły domyślne
        self.rules.append(ctrl.Rule(
            self.sila['srednia'] & self.predkosc['umiarkowana'] & self.zmeczenie['lekkie'],
            (self.opor['sredni'], self.feedback['idealnie'])
        ))

    def build_system(self):
        """Budowa systemu sterowania."""
        self.control_system = ctrl.ControlSystem(self.rules)
        self.simulator = ctrl.ControlSystemSimulation(self.control_system)

    def compute(self, sila, predkosc, faza, zmeczenie, tryb):
        """Wnioskowanie rozmyte."""
        try:
            self.simulator.input['sila_generowana'] = sila
            self.simulator.input['predkosc_ruchu'] = predkosc
            self.simulator.input['faza_ruchu'] = faza
            self.simulator.input['wskaznik_zmeczenia'] = zmeczenie
            self.simulator.input['tryb_treningu'] = tryb
            self.simulator.compute()
            return {
                'opor': self.simulator.output['opor_maszyny'],
                'feedback': self.simulator.output['sygnal_feedback']
            }
        except Exception as e:
            return {'opor': 50.0, 'feedback': 3.0, 'error': str(e)}
