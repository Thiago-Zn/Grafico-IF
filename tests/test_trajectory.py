import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.parameters import Parameters
from src.solver import solve


def test_trajectory_length():
    params = Parameters(alpha=50, beta=0.6, investment_intercept=40,
                        investment_slope=5, government=20, tax=10)
    data = solve(params)
    assert isinstance(data["trajectory_path"], list)
    assert len(data["trajectory_path"]) >= 4
