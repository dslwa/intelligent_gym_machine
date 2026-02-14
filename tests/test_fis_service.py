import pytest

from src.services.fis_service import FISService, FISInputs, ValidationError


def test_compute_returns_valid_ranges():
    service = FISService()
    inputs = FISInputs(sila=250, predkosc=0.7, faza=50, zmeczenie=20, tryb=2)
    result = service.compute(inputs)
    assert 0 <= result.resistance <= 100
    assert 1 <= result.feedback <= 5
    assert result.feedback_text in {'ZWOLNIJ', 'DOBRZE', 'IDEALNIE', 'MOCNIEJ', 'STOP'}


def test_validation_fails_for_out_of_range():
    service = FISService()
    inputs = FISInputs(sila=-1, predkosc=0.7, faza=50, zmeczenie=20, tryb=2)
    with pytest.raises(ValidationError):
        service.compute(inputs)


def test_membership_snapshot_updates_on_mf_change():
    service = FISService()
    before = service.get_membership_plot_data()
    service.change_mf_type('gaussian')
    after = service.get_membership_plot_data()
    assert before != after
