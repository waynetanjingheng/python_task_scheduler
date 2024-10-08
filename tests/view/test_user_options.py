import pytest
from src.view import UserOptions


@pytest.fixture(autouse=True)
def after_each():
    yield
    UserOptions.type = None
    UserOptions.num_workers = None
    UserOptions.num_tasks = None


def test_display_options_and_accept_input(monkeypatch):
    # Mock the input to simulate user interaction
    inputs = [2, 5, 10]
    inputs_iter = iter(
        inputs
    )  # Simulate inputs: scheduling type, num_workers, num_tasks
    monkeypatch.setattr("builtins.input", lambda: next(inputs_iter))

    UserOptions.display_options_and_accept_input()

    assert UserOptions.type == inputs[0]
    assert UserOptions.num_workers == inputs[1]
    assert UserOptions.num_tasks == inputs[2]
