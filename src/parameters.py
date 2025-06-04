"""Parameter configuration for the Keynesian model."""
from dataclasses import dataclass

@dataclass
class Parameters:
    """Holds all exogenous parameters for the model."""

    alpha: float
    beta: float
    investment_intercept: float
    investment_slope: float
    government: float
    tax: float
