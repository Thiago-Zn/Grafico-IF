"""Closed form solver for the Keynesian cross."""
from .parameters import Parameters
from .model import aggregate_demand


def solve_equilibrium(params: Parameters, interest_rate: float) -> float:
    """Solve for income where planned expenditure equals output."""
    numerator = (
        params.alpha
        + params.investment_intercept
        - params.investment_slope * interest_rate
        + params.government
        - params.beta * params.tax
    )
    denominator = 1 - params.beta
    return numerator / denominator
