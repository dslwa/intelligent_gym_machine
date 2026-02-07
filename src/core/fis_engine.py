import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class IntelligentGymMachine:
    def __init__(self):
        self.setup_variables()
        self.setup_membership_functions()
        self.setup_rules()
        self.build_system()

    def setup_variables(self):
        self.sila = ctrl.Antecedent(np.arange(0, 501, 1), 'sila_generowana')
        self.predkosc = ctrl.Antecedent(np.arange(0, 1.51, 0.01), 'predkosc_ruchu')
        self.faza = ctrl.Antecedent(np.arange(0, 101, 1), 'faza_ruchu')
        self.zmeczenie = ctrl.Antecedent(np.arange(0, 101, 1), 'wskaznik_zmeczenia')
        self.tryb = ctrl.Antecedent(np.arange(1, 3.01, 0.01), 'tryb_treningu')

        self.opor = ctrl.Consequent(np.arange(0, 101, 1), 'opor_maszyny')
        self.feedback = ctrl.Consequent(np.arange(1, 5.01, 0.01), 'sygnal_feedback')

    def setup_membership_functions(self):
        self.sila['bardzo_niska'] = fuzz.trapmf(self.sila.universe, [0, 0, 50, 100])
        self.sila['niska'] = fuzz.trimf(self.sila.universe, [50, 125, 200])
        self.sila['srednia'] = fuzz.trimf(self.sila.universe, [150, 250, 350])
        self.sila['wysoka'] = fuzz.trimf(self.sila.universe, [300, 375, 450])
        self.sila['bardzo_wysoka'] = fuzz.trapmf(self.sila.universe, [400, 450, 500, 500])

        self.predkosc['bardzo_wolna'] = fuzz.trapmf(self.predkosc.universe, [0, 0, 0.1, 0.25])
        self.predkosc['wolna'] = fuzz.trimf(self.predkosc.universe, [0.15, 0.35, 0.55])
        self.predkosc['umiarkowana'] = fuzz.trimf(self.predkosc.universe, [0.45, 0.7, 0.95])
        self.predkosc['szybka'] = fuzz.trimf(self.predkosc.universe, [0.85, 1.1, 1.35])
        self.predkosc['bardzo_szybka'] = fuzz.trapmf(self.predkosc.universe, [1.2, 1.35, 1.5, 1.5])

        self.faza['poczatkowa'] = fuzz.trapmf(self.faza.universe, [0, 0, 10, 25])
        self.faza['dolna'] = fuzz.trimf(self.faza.universe, [15, 30, 45])
        self.faza['srodkowa'] = fuzz.trimf(self.faza.universe, [35, 50, 65])
        self.faza['gorna'] = fuzz.trimf(self.faza.universe, [55, 70, 85])
        self.faza['koncowa'] = fuzz.trapmf(self.faza.universe, [75, 90, 100, 100])

        self.zmeczenie['swiezy'] = fuzz.trapmf(self.zmeczenie.universe, [0, 0, 5, 15])
        self.zmeczenie['lekkie'] = fuzz.trimf(self.zmeczenie.universe, [10, 25, 40])
        self.zmeczenie['umiarkowane'] = fuzz.trimf(self.zmeczenie.universe, [30, 50, 70])
        self.zmeczenie['wysokie'] = fuzz.trimf(self.zmeczenie.universe, [60, 75, 90])
        self.zmeczenie['wyczerpanie'] = fuzz.trapmf(self.zmeczenie.universe, [80, 90, 100, 100])

        self.tryb['silowy'] = fuzz.trimf(self.tryb.universe, [1, 1, 1.8])
        self.tryb['hipertrofia'] = fuzz.trimf(self.tryb.universe, [1.5, 2, 2.5])
        self.tryb['wytrzymalosc'] = fuzz.trimf(self.tryb.universe, [2.2, 3, 3])

        self.opor['minimalny'] = fuzz.trapmf(self.opor.universe, [0, 0, 10, 20])
        self.opor['niski'] = fuzz.trimf(self.opor.universe, [15, 30, 45])
        self.opor['sredni'] = fuzz.trimf(self.opor.universe, [35, 50, 65])
        self.opor['wysoki'] = fuzz.trimf(self.opor.universe, [55, 70, 85])
        self.opor['maksymalny'] = fuzz.trapmf(self.opor.universe, [75, 90, 100, 100])

        self.feedback['zwolnij'] = fuzz.trimf(self.feedback.universe, [1, 1, 2])
        self.feedback['dobrze'] = fuzz.trimf(self.feedback.universe, [1.5, 2.5, 3.5])
        self.feedback['idealnie'] = fuzz.trimf(self.feedback.universe, [2.5, 3, 3.5])
        self.feedback['mocniej'] = fuzz.trimf(self.feedback.universe, [3, 3.5, 4.5])
        self.feedback['stop'] = fuzz.trimf(self.feedback.universe, [4, 5, 5])

    def setup_rules(self):
        self.rules = []

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

        self.rules.append(ctrl.Rule(
            self.predkosc['bardzo_szybka'] & self.zmeczenie['swiezy'],
            (self.opor['wysoki'], self.feedback['zwolnij'])
        ))
        self.rules.append(ctrl.Rule(
            self.predkosc['szybka'] & self.tryb['silowy'],
            (self.opor['wysoki'], self.feedback['dobrze'])
        ))
        self.rules.append(ctrl.Rule(
            self.predkosc['umiarkowana'] & self.tryb['hipertrofia'],
            (self.opor['sredni'], self.feedback['idealnie'])
        ))
        self.rules.append(ctrl.Rule(
            self.predkosc['wolna'] & self.zmeczenie['lekkie'],
            (self.opor['sredni'], self.feedback['dobrze'])
        ))
        self.rules.append(ctrl.Rule(
            self.predkosc['bardzo_wolna'] & self.zmeczenie['wysokie'],
            (self.opor['niski'], self.feedback['stop'])
        ))

        self.rules.append(ctrl.Rule(
            self.zmeczenie['swiezy'] & self.sila['bardzo_wysoka'],
            (self.opor['maksymalny'], self.feedback['idealnie'])
        ))
        self.rules.append(ctrl.Rule(
            self.zmeczenie['lekkie'] & self.sila['srednia'],
            (self.opor['sredni'], self.feedback['dobrze'])
        ))
        self.rules.append(ctrl.Rule(
            self.zmeczenie['umiarkowane'] & self.sila['srednia'],
            (self.opor['niski'], self.feedback['dobrze'])
        ))
        self.rules.append(ctrl.Rule(
            self.zmeczenie['wysokie'] & self.sila['niska'],
            (self.opor['minimalny'], self.feedback['stop'])
        ))
        self.rules.append(ctrl.Rule(
            self.zmeczenie['wyczerpanie'],
            (self.opor['minimalny'], self.feedback['stop'])
        ))

        self.rules.append(ctrl.Rule(
            self.tryb['silowy'] & self.sila['bardzo_wysoka'] & self.zmeczenie['swiezy'],
            (self.opor['maksymalny'], self.feedback['idealnie'])
        ))
        self.rules.append(ctrl.Rule(
            self.tryb['silowy'] & self.sila['srednia'] & self.faza['gorna'],
            (self.opor['wysoki'], self.feedback['mocniej'])
        ))
        self.rules.append(ctrl.Rule(
            self.tryb['hipertrofia'] & self.predkosc['umiarkowana'] & self.zmeczenie['lekkie'],
            (self.opor['sredni'], self.feedback['idealnie'])
        ))
        self.rules.append(ctrl.Rule(
            self.tryb['hipertrofia'] & self.zmeczenie['umiarkowane'],
            (self.opor['niski'], self.feedback['mocniej'])
        ))
        self.rules.append(ctrl.Rule(
            self.tryb['wytrzymalosc'] & self.predkosc['szybka'],
            (self.opor['niski'], self.feedback['idealnie'])
        ))
        self.rules.append(ctrl.Rule(
            self.tryb['wytrzymalosc'] & self.zmeczenie['umiarkowane'],
            (self.opor['niski'], self.feedback['dobrze'])
        ))

        self.rules.append(ctrl.Rule(
            self.sila['bardzo_niska'] & self.faza['poczatkowa'],
            (self.opor['minimalny'], self.feedback['mocniej'])
        ))
        self.rules.append(ctrl.Rule(
            self.sila['bardzo_niska'] & self.zmeczenie['wysokie'],
            (self.opor['minimalny'], self.feedback['stop'])
        ))
        self.rules.append(ctrl.Rule(
            self.sila['bardzo_wysoka'] & self.zmeczenie['wyczerpanie'],
            (self.opor['niski'], self.feedback['stop'])
        ))

        self.rules.append(ctrl.Rule(
            self.faza['poczatkowa'] & self.predkosc['bardzo_wolna'] & self.sila['niska'],
            (self.opor['minimalny'], self.feedback['mocniej'])
        ))
        self.rules.append(ctrl.Rule(
            self.faza['srodkowa'] & self.predkosc['umiarkowana'] & self.sila['srednia'],
            (self.opor['sredni'], self.feedback['idealnie'])
        ))
        self.rules.append(ctrl.Rule(
            self.faza['koncowa'] & self.predkosc['szybka'] & self.sila['wysoka'],
            (self.opor['maksymalny'], self.feedback['idealnie'])
        ))
        self.rules.append(ctrl.Rule(
            self.faza['gorna'] & self.tryb['silowy'] & self.sila['wysoka'],
            (self.opor['wysoki'], self.feedback['idealnie'])
        ))
        self.rules.append(ctrl.Rule(
            self.faza['dolna'] & self.predkosc['wolna'] & self.tryb['hipertrofia'],
            (self.opor['sredni'], self.feedback['idealnie'])
        ))

    def build_system(self):
        """Budowa systemu sterowania rozmytego."""
        self.system = ctrl.ControlSystem(self.rules)
        self.simulator = ctrl.ControlSystemSimulation(self.system)

    def compute(self, sila_val, predkosc_val, faza_val, zmeczenie_val, tryb_val):

        self.simulator.reset()

        self.simulator.input['sila_generowana'] = sila_val
        self.simulator.input['predkosc_ruchu'] = predkosc_val
        self.simulator.input['faza_ruchu'] = faza_val
        self.simulator.input['wskaznik_zmeczenia'] = zmeczenie_val
        self.simulator.input['tryb_treningu'] = tryb_val

        try:
            self.simulator.compute()
            return {
                'opor': self.simulator.output['opor_maszyny'],
                'feedback': self.simulator.output['sygnal_feedback'],
                'feedback_text': self._get_feedback_text(self.simulator.output['sygnal_feedback'])
            }
        except Exception as e:
            return {
                'opor': 50.0,
                'feedback': 3.0,
                'feedback_text': 'DOBRZE',
                'error': str(e)
            }

    def _get_feedback_text(self, feedback_val):
        if feedback_val < 1.5:
            return "ZWOLNIJ"
        elif feedback_val < 2.5:
            return "DOBRZE"
        elif feedback_val < 3.5:
            return "IDEALNIE"
        elif feedback_val < 4.5:
            return "MOCNIEJ"
        else:
            return "STOP"

    def get_membership_functions_table(self):
        tables = []

        variables = [
            ('Siła generowana', 'N', '0-500', self.sila),
            ('Prędkość ruchu', 'm/s', '0-1.5', self.predkosc),
            ('Faza ruchu', '% ROM', '0-100', self.faza),
            ('Wskaźnik zmęczenia', '%', '0-100', self.zmeczenie),
            ('Tryb treningu', '-', '1-3', self.tryb),
            ('Opór maszyny (WYJŚCIE)', '%', '0-100', self.opor),
            ('Sygnał feedbacku (WYJŚCIE)', '-', '1-5', self.feedback),
        ]

        for var_name, unit, range_str, var_obj in variables:
            table = f"\n{'='*80}\n"
            table += f"Zmienna: {var_name}\n"
            table += f"Jednostka: {unit} | Zakres: {range_str}\n"
            table += f"{'='*80}\n"
            table += f"{'Nazwa zbioru':<20} {'Typ funkcji':<12} {'Parametry (a, b, c, d)':<30}\n"
            table += f"{'-'*80}\n"

            for term_name in var_obj.terms:
                mf = var_obj[term_name].mf
                universe = var_obj.universe

                non_zero_indices = np.where(mf > 0)[0]
                if len(non_zero_indices) > 0:
                    start_idx = non_zero_indices[0]
                    end_idx = non_zero_indices[-1]
                    max_indices = np.where(mf == 1.0)[0]

                    if len(max_indices) > 1:
                        func_type = "trapmf"
                        a = universe[start_idx]
                        b = universe[max_indices[0]]
                        c = universe[max_indices[-1]]
                        d = universe[end_idx]
                        params = f"({a:.2f}, {b:.2f}, {c:.2f}, {d:.2f})"
                    else:
                        func_type = "trimf"
                        a = universe[start_idx]
                        b = universe[max_indices[0]] if len(max_indices) > 0 else universe[(start_idx + end_idx) // 2]
                        c = universe[end_idx]
                        params = f"({a:.2f}, {b:.2f}, {c:.2f}, -)"
                else:
                    func_type = "unknown"
                    params = "-"

                table += f"{term_name:<20} {func_type:<12} {params:<30}\n"

            tables.append(table)

        return '\n'.join(tables)

