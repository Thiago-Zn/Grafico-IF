"""Charts module for DD-AA economic model visualization with animation support."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def build_canvas(data: dict) -> go.Figure:
    """Build the complete DD-AA model visualization with all subplots."""
    
    # Create subplots layout with better spacing
    fig = make_subplots(
        rows=3, cols=2,
        row_heights=[0.3, 0.3, 0.4],
        column_widths=[0.5, 0.5],
        specs=[[{"type": "xy"}, {"type": "xy"}],
               [{"type": "xy"}, {"type": "xy"}],
               [{"colspan": 2, "type": "xy"}, None]],
        vertical_spacing=0.10,
        horizontal_spacing=0.08,
        subplot_titles=None  # We'll add custom titles
    )
    
    # Add custom subplot titles with proper styling
    _add_subplot_titles(fig)
    
    # 1. Investment-i subplot (top-left)
    _add_investment_panel(fig, data, row=1, col=1)
    
    # 2. Aggregate Demand subplot (top-right)
    _add_demand_panel(fig, data, row=1, col=2)
    
    # 3. UIP subplot (middle-left)
    _add_uip_panel(fig, data, row=2, col=1)
    
    # 4. LM subplot (middle-right)
    _add_lm_panel(fig, data, row=2, col=2)
    
    # 5. DD-AA Panel (bottom)
    _add_ddaa_panel(fig, data, row=3, col=1)
    
    # Add trajectory line if needed
    if data.get("trajectory_progress", 0) > 0:
        _add_trajectory_line(fig, data["trajectory_progress"])
    
    # Add formula boxes
    _add_formula_boxes(fig, data)
    
    # Style the figure
    _style_figure(fig, data)
    
    return fig


def _add_subplot_titles(fig):
    """Add custom styled subplot titles."""
    titles = [
        ("Investment, i", 0.22, 0.95),
        ("Aggregate demand", 0.72, 0.95),
        ("S<sub>ERL/USD</sub>", 0.22, 0.62),
        ("Real money balance M<sup>D</sup>/P and M/P", 0.72, 0.62),
        ("Rates of return<br>in terms of ERL", 0.15, 0.28)
    ]
    
    for title, x, y in titles:
        fig.add_annotation(
            text=title,
            xref="paper", yref="paper",
            x=x, y=y,
            showarrow=False,
            font=dict(size=12, color="black"),
            xanchor="center"
        )


def _add_investment_panel(fig, data, row, col):
    """Add investment curve panel."""
    invest_x, invest_y = data["invest_curve"]
    
    # Main investment curve
    fig.add_trace(
        go.Scatter(
            x=invest_x, y=invest_y,
            mode="lines",
            line=dict(color="#1f77b4", width=3),
            showlegend=False,
            hovertemplate="i: %{x:.1f}<br>I: %{y:.1f}"
        ),
        row=row, col=col
    )
    
    # Add interest rate levels
    i_levels = data.get("interest_levels", {})
    for key in ["i1", "i2", "i3"]:
        if key in i_levels:
            i_val = i_levels[key]
            # Find corresponding y value
            idx = np.argmin(np.abs(invest_x - i_val))
            y_val = invest_y[idx]
            
            # Horizontal dashed line
            fig.add_hline(
                y=y_val,
                line=dict(color="gray", dash="dash", width=1),
                row=row, col=col
            )
            
            # Vertical dashed line
            fig.add_vline(
                x=i_val,
                line=dict(color="purple", dash="dash", width=1),
                row=row, col=col
            )
            
            # Label
            fig.add_annotation(
                text=f"i<sub>{key[-1]}</sub>",
                x=-0.5, y=y_val,
                xref=f"x{(row-1)*2+col}", yref=f"y{(row-1)*2+col}",
                showarrow=False,
                font=dict(size=10)
            )


def _add_demand_panel(fig, data, row, col):
    """Add aggregate demand panel."""
    demand_data = data["demand_line"]
    
    # 45-degree line
    fig.add_trace(
        go.Scatter(
            x=demand_data["line45_x"], y=demand_data["line45_y"],
            mode="lines",
            line=dict(color="gray", width=2),
            name="D = Y",
            showlegend=False
        ),
        row=row, col=col
    )
    
    # Multiple demand curves or single curve
    if data.get("demand_curves_multi", False):
        # D1, D2, D3 curves
        colors = ["#1f77b4", "green", "purple"]
        labels = ["D<sub>1</sub>", "D<sub>2</sub>", "D<sub>3</sub>"]
        shifts = [0, 10, 0]  # D3 = D1
        
        for i, (color, label, shift) in enumerate(zip(colors, labels, shifts)):
            fig.add_trace(
                go.Scatter(
                    x=demand_data["ad_x"],
                    y=demand_data["ad_y"] + shift,
                    mode="lines",
                    line=dict(color=color, width=2),
                    showlegend=False
                ),
                row=row, col=col
            )
            
            # Add label at end of curve
            fig.add_annotation(
                text=label,
                x=demand_data["ad_x"][-1] * 0.9,
                y=(demand_data["ad_y"][-1] + shift) * 0.9,
                xref=f"x{(row-1)*2+col}", yref=f"y{(row-1)*2+col}",
                showarrow=False,
                font=dict(size=10, color=color)
            )
    else:
        # Single demand curve
        fig.add_trace(
            go.Scatter(
                x=demand_data["ad_x"], y=demand_data["ad_y"],
                mode="lines",
                line=dict(color="#1f77b4", width=2),
                showlegend=False
            ),
            row=row, col=col
        )
    
    # Output level markers
    output_levels = data.get("output_levels", {})
    for key in ["Y1", "Y2", "Y3"]:
        if key in output_levels:
            y_val = output_levels[key]
            fig.add_vline(
                x=y_val,
                line=dict(color="purple", dash="dash", width=1),
                row=row, col=col
            )
            fig.add_annotation(
                text=f"Y<sub>{key[-1]}</sub>",
                x=y_val, y=50,
                xref=f"x{(row-1)*2+col}", yref=f"y{(row-1)*2+col}",
                showarrow=False,
                yanchor="top",
                font=dict(size=10)
            )


def _add_uip_panel(fig, data, row, col):
    """Add UIP curve panel."""
    uip_x, uip_y = data["uip_curve"]
    
    # UIP curve
    fig.add_trace(
        go.Scatter(
            x=uip_x, y=uip_y,
            mode="lines",
            line=dict(color="#1f77b4", width=3),
            showlegend=False
        ),
        row=row, col=col
    )
    
    # Exchange rate levels
    s_levels = data.get("exchange_levels", {})
    for i, key in enumerate(["s1", "s2", "s3"]):
        if key in s_levels:
            s_val = s_levels[key]
            
            # Horizontal line
            fig.add_hline(
                y=s_val,
                line=dict(color="gray", dash="dash", width=1),
                row=row, col=col
            )
            
            # Label
            fig.add_annotation(
                text=f"s<sub>{key[-1]}</sub>",
                x=uip_x[0] - 0.5,
                y=s_val,
                xref=f"x{(row-1)*2+col}", yref=f"y{(row-1)*2+col}",
                showarrow=False,
                xanchor="right",
                font=dict(size=10)
            )
    
    # Add UIP formula
    fig.add_annotation(
        text="i<sub>USA</sub> + (s̄<sup>e</sup> - s)/s",
        x=np.mean(uip_x),
        y=np.min(uip_y) - 0.1,
        xref=f"x{(row-1)*2+col}", yref=f"y{(row-1)*2+col}",
        showarrow=False,
        font=dict(size=10)
    )


def _add_lm_panel(fig, data, row, col):
    """Add LM curves panel."""
    lm_x, lm_y = data["lm_curve"]
    
    # Check if we need to show original curve
    if "lm_curve_original" in data:
        orig_x, orig_y = data["lm_curve_original"]
        fig.add_trace(
            go.Scatter(
                x=orig_x, y=orig_y,
                mode="lines",
                line=dict(color="rgba(0,0,0,0.25)", width=2),
                showlegend=False
            ),
            row=row, col=col
        )
    
    # Current LM curve(s)
    if data.get("demand_curves_multi", False):
        # Multiple LM curves
        colors = ["#1f77b4", "green", "#d62728"]
        labels = ["L(i, Y<sub>1</sub>)", "L(i, Y<sub>2</sub>)", "L(i, Y<sub>3</sub>)"]
        
        for i, (color, label) in enumerate(zip(colors, labels)):
            x_shift = i * 15
            fig.add_trace(
                go.Scatter(
                    x=lm_x + x_shift, y=lm_y,
                    mode="lines",
                    line=dict(color=color, width=2),
                    showlegend=False
                ),
                row=row, col=col
            )
            
            # Add label
            fig.add_annotation(
                text=label,
                x=(lm_x[-1] + x_shift),
                y=lm_y[-1],
                xref=f"x{(row-1)*2+col}", yref=f"y{(row-1)*2+col}",
                showarrow=False,
                xanchor="left",
                font=dict(size=9, color=color)
            )
    else:
        # Single LM curve
        fig.add_trace(
            go.Scatter(
                x=lm_x, y=lm_y,
                mode="lines",
                line=dict(color="#1f77b4", width=3),
                showlegend=False
            ),
            row=row, col=col
        )
    
    # Money supply lines
    fig.add_vline(
        x=np.max(lm_x) * 0.9,
        line=dict(color="black", width=1),
        row=row, col=col
    )
    fig.add_annotation(
        text="M<sup>S</sup>/P<sub>1</sub>",
        x=np.max(lm_x) * 0.9,
        y=np.mean(lm_y),
        xref=f"x{(row-1)*2+col}", yref=f"y{(row-1)*2+col}",
        showarrow=False,
        xanchor="right",
        font=dict(size=10)
    )


def _add_ddaa_panel(fig, data, row, col):
    """Add DD-AA panel."""
    # Pre-shock curves (gray)
    dd_pre_x, dd_pre_y = data["points_DD_pre"]
    aa_pre_x, aa_pre_y = data["points_AA_pre"]
    
    # DD pre-shock
    fig.add_trace(
        go.Scatter(
            x=dd_pre_x, y=dd_pre_y,
            mode="lines",
            line=dict(color="rgba(0,0,0,0.25)", width=2),
            showlegend=False
        ),
        row=row, col=col
    )
    
    # AA pre-shock
    fig.add_trace(
        go.Scatter(
            x=aa_pre_x, y=aa_pre_y,
            mode="lines",
            line=dict(color="rgba(0,0,0,0.25)", width=2),
            showlegend=False
        ),
        row=row, col=col
    )
    
    # Post-shock curves (if different)
    dd_post_x, dd_post_y = data["points_DD_post"]
    aa_post_x, aa_post_y = data["points_AA_post"]
    
    if not np.array_equal(dd_pre_y, dd_post_y):
        fig.add_trace(
            go.Scatter(
                x=dd_post_x, y=dd_post_y,
                mode="lines",
                line=dict(color="#1f77b4", width=3),
                showlegend=False
            ),
            row=row, col=col
        )
        fig.add_annotation(
            text="DD<sub>2</sub>",
            x=dd_post_x[-1], y=dd_post_y[-1],
            xref=f"x5", yref=f"y5",
            showarrow=False,
            xanchor="left",
            font=dict(size=10, color="#1f77b4")
        )
    
    if not np.array_equal(aa_pre_y, aa_post_y):
        fig.add_trace(
            go.Scatter(
                x=aa_post_x, y=aa_post_y,
                mode="lines",
                line=dict(color="#d62728", width=3),
                showlegend=False
            ),
            row=row, col=col
        )
        fig.add_annotation(
            text="AA<sub>2</sub>",
            x=aa_post_x[0], y=aa_post_y[0],
            xref=f"x5", yref=f"y5",
            showarrow=False,
            xanchor="right",
            font=dict(size=10, color="#d62728")
        )
    
    # Curve labels
    fig.add_annotation(
        text="DD<sub>1</sub>",
        x=dd_pre_x[-1], y=dd_pre_y[-1],
        xref=f"x5", yref=f"y5",
        showarrow=False,
        xanchor="left",
        font=dict(size=10, color="gray")
    )
    
    fig.add_annotation(
        text="AA<sub>1=3</sub>",
        x=aa_pre_x[0], y=aa_pre_y[0],
        xref=f"x5", yref=f"y5",
        showarrow=False,
        xanchor="right",
        font=dict(size=10, color="gray")
    )
    
    # Equilibrium points
    eq_pre = data["equilibrium_pre"]
    eq_post = data["equilibrium_post"]
    
    fig.add_trace(
        go.Scatter(
            x=[eq_pre[0]], y=[eq_pre[1]],
            mode="markers",
            marker=dict(color="black", size=10),
            showlegend=False
        ),
        row=row, col=col
    )
    
    if eq_pre != eq_post:
        fig.add_trace(
            go.Scatter(
                x=[eq_post[0]], y=[eq_post[1]],
                mode="markers",
                marker=dict(color="black", size=10),
                showlegend=False
            ),
            row=row, col=col
        )
    
    # AA shift arrows
    if data.get("show_aa_arrows", False) and not np.array_equal(aa_pre_y, aa_post_y):
        mid_idx = len(aa_pre_x) // 2
        fig.add_annotation(
            x=aa_post_x[mid_idx], y=aa_post_y[mid_idx],
            ax=aa_pre_x[mid_idx], ay=aa_pre_y[mid_idx],
            xref="x5", yref="y5",
            axref="x5", ayref="y5",
            showarrow=True,
            arrowhead=3,
            arrowsize=1.5,
            arrowcolor="red",
            arrowwidth=3
        )
    
    # Policy explanation box
    if data.get("show_policy_box", False):
        fig.add_annotation(
            text=data.get("policy_text", "Policy adjustment"),
            x=0.95, y=0.05,
            xref="paper", yref="paper",
            showarrow=False,
            bgcolor="lavender",
            bordercolor="purple",
            borderwidth=2,
            font=dict(size=11, family="monospace"),
            align="left",
            xanchor="right",
            yanchor="bottom"
        )


def _add_trajectory_line(fig, progress):
    """Add the red trajectory line that connects panels."""
    # Define waypoints for the trajectory
    waypoints = [
        (0.22, 0.83),  # Start at investment panel
        (0.22, 0.78),  # Move down
        (0.45, 0.78),  # Move right to demand panel
        (0.45, 0.55),  # Move down
        (0.22, 0.55),  # Move left to UIP
        (0.22, 0.50),  # Move down
        (0.55, 0.50),  # Move right to LM
        (0.55, 0.35),  # Move down
        (0.50, 0.26)   # End at DD-AA equilibrium
    ]
    
    # Skip drawing if no progress
    if progress <= 0:
        return

    # Draw trajectory using shapes in paper coordinates
    total_segments = len(waypoints) - 1
    segments_to_draw = int(total_segments * progress)

    # Add full segments
    for i in range(segments_to_draw):
        x0, y0 = waypoints[i]
        x1, y1 = waypoints[i + 1]
        fig.add_shape(
            type="line",
            x0=x0, y0=y0,
            x1=x1, y1=y1,
            xref="paper", yref="paper",
            line=dict(color="red", width=4),
            layer="above"
        )

    # Add partial segment if progress is between two waypoints
    remaining = total_segments * progress - segments_to_draw
    if remaining > 0 and segments_to_draw < total_segments:
        x0, y0 = waypoints[segments_to_draw]
        x1, y1 = waypoints[segments_to_draw + 1]
        x_end = x0 + (x1 - x0) * remaining
        y_end = y0 + (y1 - y0) * remaining
        fig.add_shape(
            type="line",
            x0=x0, y0=y0,
            x1=x_end, y1=y_end,
            xref="paper", yref="paper",
            line=dict(color="red", width=4),
            layer="above"
        )


def _add_formula_boxes(fig, data):
    """Add formula annotation boxes."""
    formulas = data.get("formulas", {})
    
    # Top formula box
    if "top" in formulas:
        fig.add_annotation(
            text=formulas["top"],
            x=0.5, y=0.98,
            xref="paper", yref="paper",
            showarrow=False,
            bgcolor="lavender",
            bordercolor="purple",
            borderwidth=1,
            font=dict(size=11),
            xanchor="center",
            yanchor="top"
        )
    
    # Green box for D2 formula
    if "green_box" in formulas:
        fig.add_annotation(
            text=formulas["green_box"],
            x=0.85, y=0.85,
            xref="paper", yref="paper",
            showarrow=False,
            bgcolor="lightgreen",
            bordercolor="green",
            borderwidth=1,
            font=dict(size=10),
            align="left"
        )
    
    # D3 = D1 annotation
    if data.get("demand_curves_multi", False):
        fig.add_annotation(
            text="D<sub>3</sub> = D<sub>1</sub>",
            x=0.80, y=0.88,
            xref="paper", yref="paper",
            showarrow=False,
            bgcolor="lavender",
            bordercolor="purple",
            borderwidth=1,
            font=dict(size=10)
        )


def _style_figure(fig, data):
    """Apply consistent styling to the figure."""
    # Update all axes
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor="black",
        linewidth=1,
        mirror=True,
        ticks="outside",
        tickcolor="black",
        ticklen=5
    )
    
    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor="black",
        linewidth=1,
        mirror=True,
        ticks="outside",
        tickcolor="black",
        ticklen=5
    )
    
    # Add axis arrows
    for i in range(1, 6):
        # Plotly uses "x" for the first subplot rather than "x1"
        axis_suffix = "" if i == 1 else str(i)

        fig.add_annotation(
            x=1.02, y=0,
            xref=f"x{axis_suffix} domain", yref=f"y{axis_suffix} domain",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.2,
            arrowwidth=2,
            arrowcolor="black",
            ax=-0.02, ay=0
        )

        fig.add_annotation(
            x=0, y=1.02,
            xref=f"x{axis_suffix} domain", yref=f"y{axis_suffix} domain",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.2,
            arrowwidth=2,
            arrowcolor="black",
            ax=0, ay=-0.02
        )
    
    # Set axis labels
    fig.update_xaxes(title_text="i", row=1, col=1)
    fig.update_xaxes(title_text="Output Y", row=1, col=2)
    fig.update_xaxes(title_text="i<sub>ERL</sub>", row=2, col=1)
    fig.update_xaxes(title_text="", row=2, col=2)
    fig.update_xaxes(title_text="Output Y", row=3, col=1)
    
    fig.update_yaxes(title_text="I", row=1, col=1)
    fig.update_yaxes(title_text="", row=1, col=2)
    fig.update_yaxes(title_text="", row=2, col=1)
    fig.update_yaxes(title_text="", row=2, col=2)
    fig.update_yaxes(title_text="S<sub>ERL/USD</sub>", row=3, col=1)
    
    # Update layout
    title = data.get("title", "DD-AA Model Analysis")
    
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': '#003366'}
        },
        width=900,
        height=750,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=11, color="black"),
        margin=dict(t=100, l=60, r=60, b=60)
    )


def create_transition(from_frame: dict, to_frame: dict, steps: int = 10) -> list:
    """Create transition frames for smooth animation between two states."""
    frames = []
    
    for i in range(steps):
        t = i / (steps - 1)  # Interpolation parameter 0 to 1
        
        # Create interpolated frame
        frame = {}
        
        # Interpolate numeric values
        for key in from_frame:
            if key in to_frame:
                if isinstance(from_frame[key], tuple) and len(from_frame[key]) == 2:
                    # Interpolate curve data
                    x1, y1 = from_frame[key]
                    x2, y2 = to_frame[key]
                    
                    if isinstance(x1, np.ndarray) and isinstance(x2, np.ndarray):
                        # Interpolate arrays
                        x_interp = x1 * (1 - t) + x2 * t
                        y_interp = y1 * (1 - t) + y2 * t
                        frame[key] = (x_interp, y_interp)
                    else:
                        # Interpolate single points
                        x_interp = x1 * (1 - t) + x2 * t
                        y_interp = y1 * (1 - t) + y2 * t
                        frame[key] = (x_interp, y_interp)
                elif isinstance(from_frame[key], dict):
                    # Copy dictionaries (like demand_line)
                    frame[key] = from_frame[key].copy()
                elif isinstance(from_frame[key], (int, float)):
                    # Interpolate numeric values
                    if key in to_frame and isinstance(to_frame[key], (int, float)):
                        frame[key] = from_frame[key] * (1 - t) + to_frame[key] * t
                    else:
                        frame[key] = from_frame[key]
                else:
                    # Copy other values
                    frame[key] = from_frame[key]
        
        # Handle trajectory progress
        if "trajectory_progress" in from_frame and "trajectory_progress" in to_frame:
            frame["trajectory_progress"] = (
                from_frame["trajectory_progress"] * (1 - t) + 
                to_frame["trajectory_progress"] * t
            )
        
        # Copy non-numeric values from target frame
        for key in ["title", "description", "formulas", "show_shifts", 
                    "show_aa_arrows", "show_policy_box", "policy_text"]:
            if key in to_frame:
                frame[key] = to_frame[key]
        
        frames.append(frame)
    
    return frames


# Legacy functions for compatibility
def default_range(equilibrium: float, span: float = 100) -> np.ndarray:
    """Return a symmetric range around equilibrium for plotting."""
    lower = max(0, equilibrium - span)
    upper = equilibrium + span
    return np.linspace(lower, upper, 100)


def ad_curve(params, interest_rate: float, y_values: np.ndarray) -> np.ndarray:
    """Compute aggregate demand curve for many income levels."""
    from .model import aggregate_demand
    return np.array([aggregate_demand(params, interest_rate, y) for y in y_values])


def ad_chart(params, interest_rate: float, y_values: np.ndarray) -> go.Figure:
    """Legacy chart function."""
    from .solver import solve
    data = solve(params)
    return build_canvas(data)