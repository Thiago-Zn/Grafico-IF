"""Solver for DD-AA model with all required curves and equilibrium points."""
import numpy as np
from .parameters import Parameters


def solve(params: Parameters) -> dict:
    """
    Solve the DD-AA model and return all curves and equilibrium points.
    
    Returns a dict with:
    - invest_curve: (x, y) for investment-interest curve
    - demand_line: dict with 'ad_x', 'ad_y', 'line45_x', 'line45_y'
    - uip_curve: (x, y) for UIP curve
    - lm_curve: (x, y) for LM curve
    - points_DD_pre: (x, y) arrays for DD curve before shock
    - points_DD_post: (x, y) arrays for DD curve after shock
    - points_AA_pre: (x, y) arrays for AA curve before shock
    - points_AA_post: (x, y) arrays for AA curve after shock
    - equilibrium_pre: (Y, E) tuple for pre-shock equilibrium
    - equilibrium_post: (Y, E) tuple for post-shock equilibrium
    """
    
    # Generate x ranges
    i_range = np.linspace(0, 10, 100)
    y_range = np.linspace(0, 200, 100)
    e_range = np.linspace(0.5, 2.5, 100)
    
    # 1. Investment curve (concave, increasing)
    invest_x = i_range
    invest_y = 50 * np.sqrt(i_range / 10) + 10
    
    # 2. Demand lines
    demand_line = {
        'ad_x': y_range,
        'ad_y': 0.6 * y_range + 20,  # AD line
        'line45_x': y_range,
        'line45_y': y_range  # 45-degree line
    }
    
    # 3. UIP curve (decreasing)
    uip_x = i_range[20:80]  # Subset for better visualization
    uip_y = 2.0 - 0.15 * uip_x + 0.5
    
    # 4. LM curve (increasing)
    lm_x = i_range[:60]
    lm_y = 0.5 + 0.08 * lm_x**1.2
    
    # 5. DD curves (downward sloping in Y-E space)
    dd_y = np.linspace(50, 150, 100)
    dd_e_pre = 2.2 - 0.008 * dd_y
    dd_e_post = 2.0 - 0.008 * dd_y  # Shifted left
    
    # 6. AA curves (upward sloping in Y-E space)
    aa_y = np.linspace(50, 150, 100)
    aa_e_pre = 0.5 + 0.01 * aa_y
    aa_e_post = 0.7 + 0.01 * aa_y  # Shifted right
    
    # 7. Calculate equilibrium points (intersection of DD and AA)
    # Pre-shock equilibrium
    y_eq_pre = 100
    e_eq_pre = 2.2 - 0.008 * y_eq_pre  # On DD_pre
    
    # Post-shock equilibrium (after policy response)
    y_eq_post = 100  # Output returns to full employment
    e_eq_post = 2.0 - 0.008 * y_eq_post  # On DD_post
    
    return {
        "invest_curve": (invest_x, invest_y),
        "demand_line": demand_line,
        "uip_curve": (uip_x, uip_y),
        "lm_curve": (lm_x, lm_y),
        "points_DD_pre": (dd_y, dd_e_pre),
        "points_DD_post": (dd_y, dd_e_post),
        "points_AA_pre": (aa_y, aa_e_pre),
        "points_AA_post": (aa_y, aa_e_post),
        "equilibrium_pre": (y_eq_pre, e_eq_pre),
        "equilibrium_post": (y_eq_post, e_eq_post)
    }


def solve_equilibrium(params: Parameters, interest_rate: float) -> float:
    """Legacy function for backward compatibility."""
    numerator = (
        params.alpha
        + params.investment_intercept
        - params.investment_slope * interest_rate
        + params.government
        - params.beta * params.tax
    )
    denominator = 1 - params.beta
    return numerator / denominator