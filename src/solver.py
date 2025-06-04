"""Solver for DD-AA model with pre-calculated scenario frames."""
import numpy as np
from .parameters import Parameters


def get_scenario_frames(scenario_index: int) -> list:
    """
    Get pre-calculated frames for a given scenario.
    
    Each frame is a dict containing all curve data and metadata for that state.
    """
    if scenario_index == 0:  # Initial Equilibrium
        return _initial_equilibrium_frames()
    elif scenario_index == 1:  # Temporary Monetary Expansion
        return _temporary_monetary_expansion_frames()
    elif scenario_index == 2:  # Permanent Monetary Expansion
        return _permanent_monetary_expansion_frames()
    elif scenario_index == 3:  # Temporary Fiscal Expansion
        return _temporary_fiscal_expansion_frames()
    elif scenario_index == 4:  # Permanent Fiscal Expansion
        return _permanent_fiscal_expansion_frames()
    elif scenario_index == 5:  # Exchange Rate Crisis
        return _exchange_rate_crisis_frames()
    else:
        return _initial_equilibrium_frames()


def _initial_equilibrium_frames():
    """Initial equilibrium scenario - single frame."""
    base_data = _generate_base_curves()
    
    return [{
        **base_data,
        "title": "Initial Equilibrium | GDP at Full Employment Level",
        "description": "Economy at full employment with stable prices and exchange rate.",
        "trajectory_progress": 0.0,
        "show_shifts": False
    }]


def _temporary_monetary_expansion_frames():
    """Temporary monetary expansion scenario."""
    frames = []
    base = _generate_base_curves()
    
    # Frame 1: Initial state
    frames.append({
        **base,
        "title": "Initial Equilibrium | GDP at Full Employment Level",
        "description": "Starting point: Full employment equilibrium",
        "trajectory_progress": 0.0,
        "show_shifts": False
    })
    
    # Frame 2: Money supply increases
    frame2 = _shift_lm_curves(base, shift_right=True)
    frame2.update({
        "title": "Monetary Expansion | Step 1: Money Supply Increases",
        "description": "Central bank increases money supply, shifting LM curve right",
        "trajectory_progress": 0.2,
        "show_shifts": True,
        "highlight_curve": "lm"
    })
    frames.append(frame2)
    
    # Frame 3: Interest rate falls
    frame3 = _adjust_interest_rate(frame2, decrease=True)
    frame3.update({
        "title": "Monetary Expansion | Step 2: Interest Rate Falls",
        "description": "Lower money demand leads to lower interest rates",
        "trajectory_progress": 0.4,
        "show_shifts": True,
        "highlight_curve": "investment"
    })
    frames.append(frame3)
    
    # Frame 4: AA shifts right
    frame4 = _shift_aa_curve(frame3, shift_right=True)
    frame4.update({
        "title": "Monetary Expansion | Step 3: AA Curve Shifts",
        "description": "Lower interest rate causes currency depreciation, AA shifts right",
        "trajectory_progress": 0.7,
        "show_shifts": True,
        "highlight_curve": "aa"
    })
    frames.append(frame4)
    
    # Frame 5: New equilibrium
    frame5 = _calculate_new_equilibrium(frame4, output_increase=True)
    frame5.update({
        "title": "Monetary Expansion | New Equilibrium",
        "description": "Output increases temporarily above full employment",
        "trajectory_progress": 1.0,
        "show_shifts": True,
        "show_equilibrium_comparison": True
    })
    frames.append(frame5)
    
    return frames


def _permanent_monetary_expansion_frames():
    """Permanent monetary expansion scenario - as shown in reference images."""
    frames = []
    base = _generate_base_curves()
    
    # Frame 1: Initial state (Figure 1)
    frames.append({
        **base,
        "title": "INITIAL EQUILIBRIUM | GDP is at its Full Employment Level",
        "description": "Y₁ at full employment, stable interest rate i₁",
        "trajectory_progress": 0.0,
        "show_shifts": False,
        "formulas": {
            "top": "D₁ = C₁(Y₁ - T) + I(i₁) + G₁ + CA₁[(Y₁ - T), s₁P*/P]"
        }
    })
    
    # Frame 2: Permanent expansion announcement
    frame2 = {**base}
    frame2.update({
        "title": "PERMANENT Expansionary Monetary Policy - SHORT RUN",
        "description": "Central bank announces permanent money supply increase",
        "trajectory_progress": 0.15,
        "show_shifts": True,
        "highlight_announcement": True
    })
    frames.append(frame2)
    
    # Frame 3: Multiple shifts begin
    frame3 = _permanent_expansion_shifts(base, step=1)
    frame3.update({
        "title": "PERMANENT Expansionary Monetary Policy - Adjustments",
        "description": "LM shifts right, interest rates fall to i₂",
        "trajectory_progress": 0.4,
        "show_shifts": True,
        "show_multiple_curves": True,
        "formulas": {
            "top": "D₂ = C₂(Y₂ - T) + I(i₂) + G₁ + CA₂[(Y₂ - T), s₂P*/P]",
            "green_box": "D₂ = C₁(Y₁ - T) + I(i₁)\n+G₁ + CA₂[(Y₂ - T), s₃P*/P]"
        }
    })
    frames.append(frame3)
    
    # Frame 4: AA shifts and DD adjustment
    frame4 = _permanent_expansion_shifts(base, step=2)
    frame4.update({
        "title": "PERMANENT Expansionary Monetary Policy - AA Response",
        "description": "AA shifts right due to expected depreciation",
        "trajectory_progress": 0.7,
        "show_shifts": True,
        "show_aa_arrows": True
    })
    frames.append(frame4)
    
    # Frame 5: Final equilibrium
    frame5 = _permanent_expansion_shifts(base, step=3)
    frame5.update({
        "title": "Maintaining the GDP at its Full Employment Level",
        "description": "The EXPANSIONARY MONETARY policy compensates the change in money demand",
        "trajectory_progress": 1.0,
        "show_shifts": True,
        "show_policy_box": True,
        "policy_text": "The EXPANSIONARY MONETARY policy\ncompensates the change in money demand\nand the interest rate remains at its level i₁.\nThe AA shifts back to its original level The\noutput remains at it full-employment level:\nY₁ = Y₃   i₁ = i₃   s₁ = s₃"
    })
    frames.append(frame5)
    
    return frames


def _generate_base_curves():
    """Generate base curve data for all panels."""
    # Common x ranges
    i_range = np.linspace(0, 8, 100)
    y_range = np.linspace(50, 150, 100)
    e_range = np.linspace(0.8, 2.2, 100)
    
    # Investment curve (concave)
    invest_x = i_range
    invest_y = 30 + 20 * np.sqrt(i_range / 8)
    
    # Demand lines
    demand_line = {
        'ad_x': y_range,
        'ad_y': 0.7 * y_range + 15,
        'line45_x': y_range,
        'line45_y': y_range
    }
    
    # UIP curve (downward sloping)
    uip_x = i_range[10:70]
    uip_y = 1.8 - 0.012 * uip_x
    
    # LM curve (upward sloping)
    lm_x = y_range[:80]
    lm_y = 1.5 + 0.025 * (lm_x - 50)
    
    # DD curves (downward in Y-E space)
    dd_y = y_range
    dd_e_pre = 1.8 - 0.006 * (dd_y - 100)
    
    # AA curves (upward in Y-E space)
    aa_y = y_range
    aa_e_pre = 1.0 + 0.008 * (aa_y - 100)
    
    # Equilibrium
    y_eq = 100.0
    e_eq = 1.4
    i_eq = 3.0
    
    return {
        "invest_curve": (invest_x, invest_y),
        "demand_line": demand_line,
        "uip_curve": (uip_x, uip_y),
        "lm_curve": (lm_x, lm_y),
        "points_DD_pre": (dd_y, dd_e_pre),
        "points_DD_post": (dd_y, dd_e_pre),  # Initially same
        "points_AA_pre": (aa_y, aa_e_pre),
        "points_AA_post": (aa_y, aa_e_pre),  # Initially same
        "equilibrium_pre": (y_eq, e_eq),
        "equilibrium_post": (y_eq, e_eq),   # Initially same
        "interest_levels": {"i1": i_eq, "i2": i_eq - 1, "i3": i_eq},
        "exchange_levels": {"s1": 1.4, "s2": 1.5, "s3": 1.4},
        "output_levels": {"Y1": 100, "Y2": 110, "Y3": 100}
    }


def _shift_lm_curves(data, shift_right=True):
    """Shift LM curves for monetary policy."""
    new_data = data.copy()
    lm_x, lm_y = data["lm_curve"]
    
    shift = 15 if shift_right else -15
    new_lm_x = lm_x + shift
    
    new_data["lm_curve"] = (new_lm_x, lm_y)
    new_data["lm_curve_original"] = data["lm_curve"]
    
    return new_data


def _shift_aa_curve(data, shift_right=True):
    """Shift AA curve."""
    new_data = data.copy()
    aa_y, aa_e = data["points_AA_post"]
    
    shift = 0.2 if shift_right else -0.2
    new_aa_e = aa_e + shift
    
    new_data["points_AA_post"] = (aa_y, new_aa_e)
    
    return new_data


def _adjust_interest_rate(data, decrease=True):
    """Adjust interest rate levels."""
    new_data = data.copy()
    
    if decrease:
        new_data["interest_levels"]["i2"] = new_data["interest_levels"]["i1"] - 1
    else:
        new_data["interest_levels"]["i2"] = new_data["interest_levels"]["i1"] + 1
    
    return new_data


def _calculate_new_equilibrium(data, output_increase=True):
    """Calculate new equilibrium point."""
    new_data = data.copy()
    
    if output_increase:
        new_y = data["equilibrium_pre"][0] + 10
        new_e = data["equilibrium_pre"][1] + 0.1
    else:
        new_y = data["equilibrium_pre"][0] - 10
        new_e = data["equilibrium_pre"][1] - 0.1
    
    new_data["equilibrium_post"] = (new_y, new_e)
    new_data["output_levels"]["Y2"] = new_y
    
    return new_data


def _permanent_expansion_shifts(base_data, step):
    """Generate shifts for permanent expansion scenario."""
    data = base_data.copy()
    
    if step >= 1:
        # LM shifts right
        data = _shift_lm_curves(data, shift_right=True)
        data["interest_levels"]["i2"] = data["interest_levels"]["i1"] - 1
        
        # Add multiple demand curves
        data["demand_curves_multi"] = True
        
    if step >= 2:
        # AA shifts right significantly
        aa_y, aa_e = data["points_AA_pre"]
        data["points_AA_post"] = (aa_y, aa_e + 0.3)
        data["exchange_levels"]["s2"] = 1.6
        
        # DD also shifts
        dd_y, dd_e = data["points_DD_pre"]
        data["points_DD_post"] = (dd_y, dd_e - 0.1)
        
    if step >= 3:
        # Final adjustment - AA returns closer to original
        aa_y, aa_e = data["points_AA_pre"]
        data["points_AA_post"] = (aa_y, aa_e + 0.05)
        data["equilibrium_post"] = data["equilibrium_pre"]  # Returns to full employment
        data["interest_levels"]["i3"] = data["interest_levels"]["i1"]
        data["exchange_levels"]["s3"] = data["exchange_levels"]["s1"]
        
    return data


def _temporary_fiscal_expansion_frames():
    """Temporary fiscal expansion scenario."""
    # Similar structure to monetary expansion but with different shifts
    return _initial_equilibrium_frames()  # Placeholder


def _permanent_fiscal_expansion_frames():
    """Permanent fiscal expansion scenario."""
    return _initial_equilibrium_frames()  # Placeholder


def _exchange_rate_crisis_frames():
    """Exchange rate crisis scenario."""
    return _initial_equilibrium_frames()  # Placeholder


# Legacy functions for compatibility
def solve(params: Parameters) -> dict:
    """Legacy solve function."""
    return _generate_base_curves()


def solve_equilibrium(params: Parameters, interest_rate: float) -> float:
    """Legacy equilibrium solver."""
    numerator = (
        params.alpha
        + params.investment_intercept
        - params.investment_slope * interest_rate
        + params.government
        - params.beta * params.tax
    )
    denominator = 1 - params.beta
    return numerator / denominator