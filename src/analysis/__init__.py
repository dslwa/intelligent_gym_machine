"""
Analysis module - analiza scenariuszy i eksperymenty.
"""

from .scenarios import run_scenarios_with_analysis, check_scenario_validity
from .experiments import compare_membership_functions, compare_inference_results, run_experiments

__all__ = [
    'run_scenarios_with_analysis',
    'check_scenario_validity',
    'compare_membership_functions',
    'compare_inference_results',
    'run_experiments'
]
