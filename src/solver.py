"""Simplified solver for DD-AA model."""
import numpy as np
from .parameters import Parameters


def solve(params: Parameters) -> dict:
    """
    Legacy solve function that returns basic curve data.
    Used for compatibility with existing code.
    """
    # Generate basic ranges
    i_range = np.linspace(0, 8, 100)
    y_range = np.linspace(50, 150, 100)
    
    # Investment curve
    invest_x = i_range
    invest_y = 30 + 15 * np.sqrt(i_range)
    
    # Demand lines
    demand_line = {
        'ad_x': y_range,
        'ad_y': 0.7 * y_range + 20,
        'line45_x': y_range,
        'line45_y': y_range
    }
    
    # UIP curve
    uip_x = i_range[:60]
    uip_y = 1.8 - 0.08 * uip_x
    
    # LM curve
    lm_x = y_range[:80]
    lm_y = 1.5 + 0.02 * (lm_x - 100)
    
    # DD and AA curves
    dd_y = y_range
    dd_e = 2.0 - 0.005 * dd_y
    aa_y = y_range
    aa_e = 0.8 + 0.008 * aa_y

    # Alternate DD for policy shock
    dd_post_e = 2.1 - 0.005 * dd_y

    # Equilibrium
    y_eq = 100.0
    e_eq = 1.4

    # Simple demonstration trajectory across panels
    trajectory_path = [
        (0.75, 0.63),  # LM panel
        (0.25, 0.63),  # UIP panel
        (0.25, 0.52),  # move down
        (0.50, 0.25)   # DD-AA panel
    ]
    
    return {
        "invest_curve": (invest_x, invest_y),
        "demand_line": demand_line,
        "uip_curve": (uip_x, uip_y),
        "lm_curve": (lm_x, lm_y),
        "points_DD_pre": (dd_y, dd_e),
        "points_DD_post": (dd_y, dd_post_e),
        "points_AA_pre": (aa_y, aa_e),
        "points_AA_post": (aa_y, aa_e),
        "equilibrium_pre": (y_eq, e_eq),
        "equilibrium_post": (y_eq, e_eq),
        "dd_post_x": dd_y,
        "dd_post_y": dd_post_e,
        "trajectory_path": trajectory_path,
        "eq_x": y_eq,
        "eq_y": e_eq
    }


def solve_equilibrium(params: Parameters, interest_rate: float) -> float:
    """
    Legacy equilibrium solver for compatibility.
    """
    numerator = (
        params.alpha
        + params.investment_intercept
        - params.investment_slope * interest_rate
        + params.government
        - params.beta * params.tax
    )
    denominator = 1 - params.beta
    return numerator / denominator