"""Utilities for plotting using Plotly."""
import numpy as np
import plotly.graph_objects as go

from .parameters import Parameters
from .model import aggregate_demand
from .solver import solve_equilibrium


def default_range(equilibrium: float, span: float = 100) -> np.ndarray:
    """Return a symmetric range around equilibrium for plotting."""
    lower = max(0, equilibrium - span)
    upper = equilibrium + span
    return np.linspace(lower, upper, 100)


def ad_curve(params: Parameters, interest_rate: float, y_values: np.ndarray) -> np.ndarray:
    """Compute aggregate demand curve for many income levels."""
    return np.array([aggregate_demand(params, interest_rate, y) for y in y_values])


def ad_chart(params: Parameters, interest_rate: float, y_values: np.ndarray) -> go.Figure:
    """Build a Plotly figure showing AD and the 45-degree line."""
    ad = ad_curve(params, interest_rate, y_values)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y_values, y=ad, name="AD"))
    fig.add_trace(go.Scatter(x=y_values, y=y_values, name="45-degree"))
    eq_y = solve_equilibrium(params, interest_rate)
    fig.add_vline(eq_y, line_dash="dash", line_color="green")
    fig.update_layout(xaxis_title="Income (Y)", yaxis_title="Planned Expenditure")
    return fig
