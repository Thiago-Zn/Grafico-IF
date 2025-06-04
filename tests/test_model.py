import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
from src.parameters import Parameters
from src.model import aggregate_demand


def test_aggregate_demand():
    params = Parameters(alpha=50, beta=0.6, investment_intercept=40,
                        investment_slope=5, government=20, tax=10)
    y = 100
    r = 2
    ad = aggregate_demand(params, r, y)
    expected = 50 + 0.6 * (100 - 10) + 40 - 5 * 2 + 20
    assert np.isclose(ad, expected)
