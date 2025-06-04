"""Charts module for DD-AA model - simplified and accurate."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def build_complete_diagram(step_data, step_index):
    """Build the complete DD-AA diagram for a given step."""
    
    # Create the correct subplot layout
    fig = make_subplots(
        rows=3,
        cols=3,
        row_heights=[0.25, 0.25, 0.5],
        column_widths=[0.3, 0.3, 0.4],
        specs=[
            [{"type": "xy"}, {"type": "xy"}, None],
            [{"type": "xy"}, {"type": "xy"}, None],
            [{"type": "xy"}, {"colspan": 2, "type": "xy"}, None],
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.10,
    )
    
    # Get data for current step
    changes = step_data.get("changes", {})

    # Domain mapping for trajectory normalisation
    layout_json = fig.to_dict()["layout"]
    x_domains = {k: layout_json[k]["domain"] for k in layout_json if k.startswith("xaxis")}
    y_domains = {k.replace("xaxis", "yaxis"): layout_json[k.replace("xaxis", "yaxis")]["domain"] for k in x_domains}
    
    # Add all panels
    _add_investment_panel(fig, changes, row=1, col=1)
    _add_demand_panel(fig, changes, row=1, col=2)
    _add_serl_panel(fig, changes, row=2, col=1)
    _add_money_balance_panel(fig, changes, row=3, col=1)
    _add_ddaa_panel(fig, changes, row=3, col=2)
    
    # Add trajectory line based on step
    if step_index > 0:
        _add_trajectory(fig, step_index, x_domains, y_domains)
    
    # Add title and annotations
    _add_annotations(fig, step_data, changes)
    
    # Style the figure
    _style_figure(fig)
    
    return fig


def _add_investment_panel(fig, changes, row, col):
    """Investment-i panel (top-left)."""
    # Investment curve
    i = np.linspace(0, 8, 100)
    I = 30 + 15 * np.sqrt(i)
    
    trace = go.Scatter(x=i, y=I, mode='lines',
                       line=dict(color='#1f77b4', width=3),
                       showlegend=False)
    fig.add_trace(trace, row=row, col=col)

    xaxis_id = fig.data[-1].xaxis
    yaxis_id = fig.data[-1].yaxis
    
    # Interest rate levels
    i_levels = {"i1": 2, "i2": 1, "i3": 2}
    current_i = changes.get("i_level", "i1")
    
    for level_name, i_val in i_levels.items():
        if level_name == "i1" or level_name == current_i:
            I_val = 30 + 15 * np.sqrt(i_val)
            # Horizontal line
            fig.add_hline(y=I_val, line=dict(color='gray', dash='dash', width=1),
                         row=row, col=col)
            # Vertical line
            fig.add_vline(x=i_val, line=dict(color='purple', dash='dash', width=1),
                         row=row, col=col)
            # Label
            fig.add_annotation(
                text=f"{level_name}", x=-0.5, y=I_val,
                xref=xaxis_id, yref=yaxis_id,
                showarrow=False, font=dict(size=10)
            )
    
    # Title
    fig.add_annotation(
        text="Investment, i", x=4, y=52,
        xref=xaxis_id, yref=yaxis_id,
        showarrow=False, font=dict(size=12)
    )


def _add_demand_panel(fig, changes, row, col):
    """Aggregate demand panel (top-right)."""
    Y = np.linspace(60, 150, 100)
    
    # 45-degree line
    trace = go.Scatter(x=Y, y=Y, mode='lines',
                       line=dict(color='gray', width=2),
                       showlegend=False)
    fig.add_trace(trace, row=row, col=col)

    xaxis_id = fig.data[-1].xaxis
    yaxis_id = fig.data[-1].yaxis
    
    # Demand curves based on step
    if changes.get("dd_shift"):
        # Show D1, D2, D3
        D1 = 0.7 * Y + 20
        D2 = 0.7 * Y + 25  # Shifted up
        D3 = 0.7 * Y + 20  # Same as D1
        
        fig.add_trace(
            go.Scatter(x=Y, y=D1, mode='lines',
                       line=dict(color='purple', width=2),
                       showlegend=False),
            row=row, col=col
        )
        fig.add_trace(
            go.Scatter(x=Y, y=D2, mode='lines',
                       line=dict(color='green', width=2),
                       showlegend=False),
            row=row, col=col
        )
        
        # Labels
        fig.add_annotation(
            text="D₁ = D₃", x=130, y=111,
            xref=xaxis_id, yref=yaxis_id,
            showarrow=False, bgcolor='lavender', bordercolor='purple',
            borderwidth=1, font=dict(size=10)
        )
    else:
        # Just D1
        D1 = 0.7 * Y + 20
        fig.add_trace(
            go.Scatter(x=Y, y=D1, mode='lines',
                       line=dict(color='#1f77b4', width=2),
                       showlegend=False),
            row=row, col=col
        )
    
    # Y markers
    Y_levels = {"Y1": 100, "Y2": 110, "Y3": 100}
    for name, val in Y_levels.items():
        if name == "Y1" or (name == "Y2" and changes.get("equilibrium") == "Y2"):
            fig.add_vline(x=val, line=dict(color='purple', dash='dash', width=1),
                         row=row, col=col)
            fig.add_annotation(
                text=f"{name}", x=val, y=65,
                xref=xaxis_id, yref=yaxis_id,
                showarrow=False, yanchor='top', font=dict(size=10)
            )
    
    # Title
    fig.add_annotation(
        text="Aggregate demand", x=105, y=148,
        xref=xaxis_id, yref=yaxis_id,
        showarrow=False, font=dict(size=12)
    )


def _add_serl_panel(fig, changes, row, col):
    """S_ERL/USD panel (middle-left)."""
    i = np.linspace(0, 6, 100)
    s = 1.8 - 0.08 * i
    
    trace = go.Scatter(x=i, y=s, mode='lines',
                       line=dict(color='#1f77b4', width=3),
                       showlegend=False)
    fig.add_trace(trace, row=row, col=col)

    xaxis_id = fig.data[-1].xaxis
    yaxis_id = fig.data[-1].yaxis
    
    # Exchange rate levels
    s_levels = {"s1": 1.4, "s2": 1.6, "s3": 1.4}
    for name, val in s_levels.items():
        if name == "s1" or (name == "s2" and changes.get("aa_shift")):
            fig.add_hline(y=val, line=dict(color='gray', dash='dash', width=1),
                         row=row, col=col)
            fig.add_annotation(
                text=f"{name}", x=-0.3, y=val,
                xref=xaxis_id, yref=yaxis_id,
                showarrow=False, xanchor='right', font=dict(size=10)
            )
    
    # Formula
    fig.add_annotation(
        text="i<sub>USA</sub> + (s̄<sup>e</sup> - s)/s", x=3, y=1.3,
        xref=xaxis_id, yref=yaxis_id,
        showarrow=False, font=dict(size=10)
    )
    
    # Title
    fig.add_annotation(
        text="S<sub>ERL/USD</sub>", x=3, y=1.85,
        xref=xaxis_id, yref=yaxis_id,
        showarrow=False, font=dict(size=12)
    )


def _add_money_balance_panel(fig, changes, row, col):
    """Real money balance panel."""
    L = np.linspace(60, 140, 100)
    i_eq = 1.2

    # Money supply (horizontal)
    fig.add_hline(y=i_eq, line=dict(color="black", width=2), row=row, col=col)

    xaxis_id = fig.data[-1].xaxis
    yaxis_id = fig.data[-1].yaxis

    def lm_curve(shift):
        return i_eq + 0.02 * (L - (100 + shift))


    curves = [(lm_curve(0), "#1f77b4", "L(i, Y₁)")]
    if changes.get("lm_shift"):
        curves.append((lm_curve(10), "green", "L(i, Y₂)"))
        if changes.get("equilibrium") == "Y3":
            curves.append((lm_curve(0), "red", "L(i, Y₃)"))

    for curve, color, label in curves:
        fig.add_trace(
            go.Scatter(x=L, y=curve, mode='lines',
                       line=dict(color=color, width=3),
                       showlegend=False),
            row=row, col=col
        )
        fig.add_annotation(
            text=label, x=L[-1], y=curve[-1],
            xref=xaxis_id, yref=yaxis_id,
            showarrow=False, xanchor='left',
            font=dict(size=10, color=color)
        )

    # Axis arrows
    fig.add_annotation(
        x=L[-1], y=0, ax=L[-1] + 5, ay=0,
        xref=xaxis_id, yref=yaxis_id,
        axref=xaxis_id, ayref=yaxis_id,
        showarrow=True, arrowhead=2,
    )
    fig.add_annotation(
        x=0, y=i_eq + 1.5, ax=0, ay=i_eq + 2.0,
        xref=xaxis_id, yref=yaxis_id,
        axref=xaxis_id, ayref=yaxis_id,
        showarrow=True, arrowhead=2,
    )

    # Title
    fig.add_annotation(
        text="Money market", x=110, y=i_eq + 2.1,
        xref=xaxis_id, yref=yaxis_id,
        showarrow=False, font=dict(size=12)
    )

   


def _add_ddaa_panel(fig, changes, row, col):
    """DD-AA panel (bottom)."""
    Y = np.linspace(50, 150, 100)
    
    # Base curves
    DD1 = 2.0 - 0.005 * Y
    AA1 = 0.8 + 0.008 * Y
    
    # Pre-shock curves (gray)
    trace = go.Scatter(x=Y, y=DD1, mode='lines',
                       line=dict(color='rgba(0,0,0,0.3)', width=2),
                       showlegend=False)
    fig.add_trace(trace, row=row, col=col)
    xaxis_id = fig.data[-1].xaxis
    yaxis_id = fig.data[-1].yaxis
    fig.add_trace(
        go.Scatter(x=Y, y=AA1, mode='lines',
                   line=dict(color='rgba(0,0,0,0.3)', width=2),
                   showlegend=False),
        row=row, col=col
    )
    
    # Labels for base curves
    fig.add_annotation(
        text="DD₁", x=Y[-1], y=DD1[-1],
        xref=xaxis_id, yref=yaxis_id,
        showarrow=False, xanchor='left', font=dict(size=10)
    )
    fig.add_annotation(
        text="AA₁=₃", x=Y[0], y=AA1[0],
        xref=xaxis_id, yref=yaxis_id,
        showarrow=False, xanchor='right', font=dict(size=10)
    )
    
    # Shifted curves based on changes
    if changes.get("dd_shift"):
        DD2 = 2.1 - 0.005 * Y  # Shifted right
        fig.add_trace(
            go.Scatter(x=Y, y=DD2, mode='lines',
                       line=dict(color='#1f77b4', width=3),
                       showlegend=False),
            row=row, col=col
        )
        fig.add_annotation(
            text="DD₂", x=Y[-1], y=DD2[-1],
            xref=xaxis_id, yref=yaxis_id,
            showarrow=False, xanchor='left', font=dict(size=10, color='#1f77b4')
        )
    
    if changes.get("aa_shift") == 1:
        AA2 = 0.9 + 0.008 * Y  # Shifted right
        fig.add_trace(
            go.Scatter(x=Y, y=AA2, mode='lines',
                       line=dict(color='red', width=3),
                       showlegend=False),
            row=row, col=col
        )
        fig.add_annotation(
            text="AA₂", x=Y[0], y=AA2[0],
            xref=xaxis_id, yref=yaxis_id,
            showarrow=False, xanchor='right', font=dict(size=10, color='red')
        )
        # Arrow
        fig.add_annotation(
            x=110, y=1.68, ax=100, ay=1.6,
            xref=xaxis_id, yref=yaxis_id, axref=xaxis_id, ayref=yaxis_id,
            showarrow=True, arrowhead=3, arrowcolor='red',
            arrowwidth=3, arrowsize=1.5
        )
    elif changes.get("aa_shift") == 2:
        # AA partially returns
        AA3 = 0.82 + 0.008 * Y
        fig.add_trace(
            go.Scatter(x=Y, y=AA3, mode='lines',
                       line=dict(color='red', width=3),
                       showlegend=False),
            row=row, col=col
        )
    
    # Equilibrium points
    eq_points = {
        "default": (100, 1.4),
        "Y2": (110, 1.5),
        "Y3": (100, 1.42)
    }
    eq = eq_points.get(changes.get("equilibrium", "default"), eq_points["default"])
    
    fig.add_trace(
        go.Scatter(x=[eq[0]], y=[eq[1]], mode='markers',
                   marker=dict(color='black', size=12),
                   showlegend=False),
        row=row, col=col
    )
    
    # Title
    fig.add_annotation(
        text="Rates of return<br>in terms of ERL", x=70, y=1.9,
        xref=xaxis_id, yref=yaxis_id,
        showarrow=False, font=dict(size=12)
    )
    
    # Policy text box (for final step)
    if changes.get("equilibrium") == "Y3":
        fig.add_annotation(
            text="and the interest rate remains at its level i₁. The AA shifts back to its original level The output remains at it full-employment level: Y₁ = Y₃    i₁ = i₃    s₁ = s₃",
            x=0.98, y=0.02,
            xref="paper", yref="paper",
            showarrow=False, xanchor='right', yanchor='bottom',
            bgcolor='rgba(255,255,255,0.8)', bordercolor='red',
            borderwidth=1, font=dict(size=11, color='red')
        )


def _add_trajectory(fig, step_index, x_domains, y_domains):
    """Add red trajectory line based on step."""

    def center(dom):
        return dom[0] + (dom[1] - dom[0]) / 2

    centers = {
        'investment': (center(x_domains['xaxis']), center(y_domains['yaxis'])),
        'demand': (center(x_domains['xaxis2']), center(y_domains['yaxis2'])),
        'uip': (center(x_domains['xaxis3']), center(y_domains['yaxis3'])),
        'lm': (center(x_domains['xaxis4']), center(y_domains['yaxis4'])),
        'ddaa': (center(x_domains['xaxis5']), center(y_domains['yaxis5'])),
    }

    trajectories = {
        1: [(centers['investment'][0], y_domains['yaxis'][1]),
            (centers['investment'][0], centers['investment'][1])],
        2: [(centers['investment'][0], y_domains['yaxis'][1]),
            (centers['investment'][0], centers['uip'][1]),
            centers['uip']],
        3: [
            centers['lm'],
            centers['uip'],
            (centers['uip'][0], y_domains['yaxis3'][0]),
            (centers['lm'][0], y_domains['yaxis4'][0]),
            centers['ddaa'],
        ],
        4: [(centers['investment'][0], y_domains['yaxis'][1]),
            centers['uip'],
            (centers['uip'][0], y_domains['yaxis3'][0]),
            (centers['lm'][0], y_domains['yaxis4'][0]),
            (centers['lm'][0], centers['lm'][1])],
        5: [(centers['investment'][0], y_domains['yaxis'][1]),
            centers['uip'],
            (centers['uip'][0], y_domains['yaxis3'][0]),
            (centers['lm'][0], y_domains['yaxis4'][0]),
            (centers['lm'][0], centers['lm'][1]),
            centers['ddaa']],
        6: [(centers['investment'][0], y_domains['yaxis'][1]),
            centers['uip'],
            (centers['uip'][0], y_domains['yaxis3'][0]),
            (centers['lm'][0], y_domains['yaxis4'][0]),
            (centers['lm'][0], centers['lm'][1]),
            centers['ddaa']]
    }
    
    if step_index in trajectories:
        points = trajectories[step_index]
        x_vals = [p[0] for p in points]
        y_vals = [p[1] for p in points]

        for start, end in zip(points[:-1], points[1:]):
            fig.add_shape(
                type="line",
                x0=start[0], y0=start[1],
                x1=end[0], y1=end[1],
                xref="paper", yref="paper",
                line=dict(color="red", width=4)
            )


def _add_annotations(fig, step_data, changes):
    """Add title and formula annotations."""
    # Top formula (for later steps)
    if changes.get("dd_shift"):
        fig.add_annotation(
            text="D₃ = C₁(Y₃ - T) + I(i₃) + G₁ + CA₃[(Y₃ - T), s₃P*/P]",
            x=0.5, y=0.98,
            xref="paper", yref="paper",
            showarrow=False, xanchor='center',
            bgcolor='lavender', bordercolor='purple',
            borderwidth=1, font=dict(size=11)
        )
    elif step_data.get("title") == "Initial Equilibrium":
        fig.add_annotation(
            text="D₁ = C₁(Y₁ - T) + I(i₁) + G₁ + CA₁[(Y₁ - T), s₁P*/P]",
            x=0.5, y=0.98,
            xref="paper", yref="paper",
            showarrow=False, xanchor='center',
            bgcolor='lavender', bordercolor='purple',
            borderwidth=1, font=dict(size=11)
        )
    
    # Green D2 box (for middle steps)
    if changes.get("equilibrium") == "Y2":
        fig.add_annotation(
            text="D₂ = C₁(Y₁ - T) + I(i₁)\n+G₁ + CA₂[(Y₂ - T), s₃P*/P]",
            x=0.85, y=0.85,
            xref="paper", yref="paper",
            showarrow=False,
            bgcolor='lightgreen', bordercolor='green',
            borderwidth=1, font=dict(size=10)
        )


def _style_figure(fig):
    """Apply consistent styling."""
    # Update all axes
    fig.update_xaxes(
        showgrid=False, zeroline=False,
        showline=True, linecolor='black',
        mirror=True, ticks='outside'
    )
    fig.update_yaxes(
        showgrid=False, zeroline=False,
        showline=True, linecolor='black',
        mirror=True, ticks='outside'
    )
    
    # Specific axis labels
    fig.update_xaxes(title_text="i", row=1, col=1)
    fig.update_yaxes(title_text="I", row=1, col=1)
    fig.update_xaxes(title_text="Output Y", row=1, col=2)
    fig.update_xaxes(title_text="i<sub>ERL</sub>", row=2, col=1)
    fig.update_yaxes(title_text="S<sub>ERL/USD</sub>", row=2, col=1)
    fig.update_xaxes(title_text="L", row=3, col=1)
    fig.update_yaxes(title_text="i", row=3, col=1)
    fig.update_xaxes(title_text="Output Y", row=3, col=2)
    fig.update_yaxes(title_text="S<sub>ERL/USD</sub>", row=3, col=2)
    
    # Layout
    fig.update_layout(
        width=900,
        height=700,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=30, l=50, r=50, b=50)
    )


# Compatibility function
def build_canvas(data, frame=0):
    """Build diagram using solver output."""
    fig = build_complete_diagram({"changes": {}}, frame)

    # Optional post-shift DD curve
    if "dd_post_x" in data and "dd_post_y" in data:
        fig.add_trace(
            go.Scatter(
                x=data["dd_post_x"],
                y=data["dd_post_y"],
                mode="lines",
                line=dict(color="#1f77b4", width=3),
                showlegend=False,
            ),
            row=3,
            col=1,
        )

    # Updated equilibrium marker
    if "eq_x" in data and "eq_y" in data:
        fig.add_trace(
            go.Scatter(
                x=[data["eq_x"]],
                y=[data["eq_y"]],
                mode="markers",
                marker=dict(color="black", size=12),
                showlegend=False,
            ),
            row=3,
            col=1,
        )

    # Frame caption
    captions = data.get("captions", [])
    if frame < len(captions):
        fig.add_annotation(
            text=captions[frame],
            x=0.5,
            y=1.05,
            xref="paper",
            yref="paper",
            showarrow=False,
            xanchor="center",
            font=dict(size=12),
        )

    return fig
