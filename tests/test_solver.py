import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.parameters import Parameters
from src.solver import solve_equilibrium


def test_solve_equilibrium():
    params = Parameters(alpha=50, beta=0.6, investment_intercept=40,
                        investment_slope=5, government=20, tax=10)
    r = 2
    y = solve_equilibrium(params, r)
    # analytic solution
    expected = (50 + 40 - 5 * r + 20 - 0.6 * 10) / (1 - 0.6)
    assert abs(y - expected) < 1e-8
