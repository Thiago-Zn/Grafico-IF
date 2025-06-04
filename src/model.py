"""Core economic relations for the Keynesian cross."""
from .parameters import Parameters


def consumption(params: Parameters, income: float) -> float:
    """Compute consumption given income."""
    return params.alpha + params.beta * (income - params.tax)


def investment(params: Parameters, interest_rate: float) -> float:
    """Investment as decreasing function of the interest rate."""
    return params.investment_intercept - params.investment_slope * interest_rate


def aggregate_demand(params: Parameters, interest_rate: float, income: float) -> float:
    """Return aggregate demand at given income and interest rate."""
    return consumption(params, income) + investment(params, interest_rate) + params.government
