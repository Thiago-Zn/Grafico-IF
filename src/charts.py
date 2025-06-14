"""Charts module for DD-AA model - Enhanced with proper styling and animations."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def build_complete_diagram(step_data, step_index):
    """Build the complete DD-AA diagram for a given step."""
    
    # Create the correct subplot layout with increased spacing for trajectories
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
        vertical_spacing=0.15,  # Increased for trajectory corridors
        horizontal_spacing=0.12,
    )
    
    # Get data for current step
    changes = step_data.get("changes", {})

    # Domain mapping for trajectory normalisation
    layout_json = fig.to_dict()["layout"]
    x_domains = {k: layout_json[k]["domain"] for k in layout_json if k.startswith("xaxis")}
    y_domains = {k.replace("xaxis", "yaxis"): layout_json[k.replace("xaxis", "yaxis")]["domain"] for k in x_domains}
    
    # Add all panels with enhanced styling
    _add_investment_panel(fig, changes, row=1, col=1)
    _add_demand_panel(fig, changes, row=1, col=2)
    _add_serl_panel(fig, changes, row=2, col=1)
    _add_money_market_panel(fig, changes, row=3, col=1)
    _add_ddaa_panel(fig, changes, row=3, col=2)
    
    # Add trajectory line based on step
    if step_index > 0:
        _add_trajectory(fig, step_index, x_domains, y_domains)
    
    # Add shift arrows for economic transitions
    if changes:
        _add_shift_arrows(fig, changes, step_index)
    
    # Add title and annotations
    _add_annotations(fig, step_data, changes)
    
    # Style the figure with thick black axes
    _style_figure(fig)
    
    return fig


def _add_investment_panel(fig, changes, row, col):
    """Investment-i panel (top-left) with economic arrows."""
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
    
    # Add arrow showing interest rate fall
    if current_i == "i2" and changes.get("show_i_arrow"):
        fig.add_annotation(
            x=2, y=45, ax=1, ay=42,
            xref=xaxis_id, yref=yaxis_id,
            showarrow=True, arrowhead=3, arrowcolor='red',
            arrowwidth=3, arrowsize=1.5,
            text="i ↓", font=dict(size=12, color='red')
        )
    
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
        fig.add_annotation(
            text="D₂", x=140, y=118,
            xref=xaxis_id, yref=yaxis_id,
            showarrow=False, font=dict(size=10, color='green')
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
    
    # Y markers with proper equilibrium tracking
    Y_levels = {"Y1": 100, "Y2": 110, "Y3": 100}
    eq_state = changes.get("equilibrium", "Y1")
    
    for name, val in Y_levels.items():
        if name == "Y1" or name == eq_state:
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
    """S_ERL/USD panel (middle-left) with currency depreciation arrow."""
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
    current_s = changes.get("s_level", "s1")
    
    # Add arrow showing currency depreciation
    if changes.get("aa_shift") == 1 and changes.get("show_s_arrow"):
        fig.add_annotation(
            x=3, y=1.4, ax=3, ay=1.6,
            xref=xaxis_id, yref=yaxis_id,
            showarrow=True, arrowhead=3, arrowcolor='green',
            arrowwidth=3, arrowsize=1.5,
            text="S ↑", font=dict(size=12, color='green')
        )
    
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


def _add_money_market_panel(fig, changes, row, col):
    """Money Market panel with proper economic logic."""
    
    # Define the real money balance range
    M_range = np.linspace(60, 140, 100)
    
    # 1. FIXED MONEY SUPPLY LINE M^S₁/P₁ (horizontal)
    ms_level = 100  # Initial money supply level
    fig.add_trace(
        go.Scatter(x=[60, 140], y=[1.2, 1.2], mode='lines',
                   line=dict(color='red', width=3),
                   showlegend=False,
                   name="M^S₁/P₁"),
        row=row, col=col
    )
    
    # Get axis references after adding first trace
    xaxis_id = fig.data[-1].xaxis
    yaxis_id = fig.data[-1].yaxis
    
    # Add M^S₁/P₁ label with arrow pointing to the line
    fig.add_annotation(
        text="M<sup>S</sup>₁/P₁", x=65, y=1.15,
        xref=xaxis_id, yref=yaxis_id,
        showarrow=True, arrowhead=2,
        ax=65, ay=1.0,
        font=dict(size=12, color='red')
    )
    
    # 2. L CURVES - Show progressively based on step
    
    # L curve generation function
    def L_curve(Y_level, color, shift=0):
        """Generate L-shaped money demand curve"""
        # Vertical portion (liquidity trap at low i)
        vert_M = np.linspace(60, 75, 10)
        vert_i = np.full_like(vert_M, 0.4)
        
        # Curved transition
        trans_M = np.linspace(75, 90 + Y_level/10 + shift, 20)
        trans_i = 0.4 + (trans_M - 75)**1.5 / 500
        
        # Steep portion (normal money demand)
        steep_M = np.linspace(90 + Y_level/10 + shift, 140, 30)
        steep_i = trans_i[-1] + (steep_M - steep_M[0]) * 0.04
        
        M_full = np.concatenate([vert_M, trans_M, steep_M])
        i_full = np.concatenate([vert_i, trans_i, steep_i])
        
        return M_full, i_full
    
    # Define all three curves
    curves_data = [
        ("L₁(i, Y₁)", 100, "#1f77b4", 0),      # Blue - Initial
        ("L₂(i, Y₂)", 110, "green", 10),       # Green - Higher Y
        ("L₃(i, Y₁)", 100, "purple", -5)       # Purple - Back to Y₁
    ]
    
    # Determine which curves to show based on current state
    curves_to_show = []
    
    # For transition steps, show all three curves
    if changes.get("show_transition") or changes.get("equilibrium") == "Y3":
        curves_to_show = curves_data  # Show all three
    else:
        # Otherwise show progressively
        # Always show L₁
        curves_to_show.append(curves_data[0])
        
        # Show L₂ if there's a shift
        if changes.get("lm_shift"):
            curves_to_show.append(curves_data[1])
    
    # Draw selected curves
    for label, Y_level, color, shift in curves_to_show:
        M_vals, i_vals = L_curve(Y_level, color, shift)
        fig.add_trace(
            go.Scatter(x=M_vals, y=i_vals, mode='lines',
                       line=dict(color=color, width=2.5),
                       showlegend=False,
                       name=label),
            row=row, col=col
        )
        
        # Add curve label
        fig.add_annotation(
            text=label, x=M_vals[-1], y=i_vals[-1],
            xref=xaxis_id, yref=yaxis_id,
            showarrow=False, xanchor='left',
            font=dict(size=10, color=color)
        )
    
    # 3. EQUILIBRIUM POINTS (black dots)
    # Calculate intersection points with M^S₁/P₁ line
    eq_points = []
    
    # Always show initial equilibrium
    eq_points.append((100, 1.2, "Initial"))
    
    # Show subsequent equilibria based on step
    if changes.get("lm_shift"):
        eq_points.append((110, 1.2, "Short-run"))
        
    if changes.get("equilibrium") in ["Y3"]:
        eq_points.append((95, 1.2, "Transition"))
    
    for M_eq, i_eq, label in eq_points:
        fig.add_trace(
            go.Scatter(x=[M_eq], y=[i_eq], mode='markers',
                       marker=dict(color='black', size=10),
                       showlegend=False,
                       name=label),
            row=row, col=col
        )
    
    # 4. TRANSITION ARROWS between equilibrium points
    # Show arrows based on current step
    if changes.get("show_money_increase"):
        # Initial arrow showing money increase effect
        fig.add_annotation(
            text="", x=105, y=1.25, ax=100, ay=1.2,
            xref=xaxis_id, yref=yaxis_id,
            showarrow=True, arrowhead=2,
            arrowcolor='red', arrowwidth=3,
            arrowsize=1.5
        )
        
    if changes.get("show_transition"):
        # Arrow showing full transition sequence
        fig.add_annotation(
            text="①", x=100, y=1.15,
            xref=xaxis_id, yref=yaxis_id,
            showarrow=False,
            font=dict(size=12, color='black'),
            bgcolor='white', bordercolor='black', borderwidth=1
        )
        fig.add_annotation(
            text="②", x=110, y=1.15,
            xref=xaxis_id, yref=yaxis_id,
            showarrow=False,
            font=dict(size=12, color='black'),
            bgcolor='white', bordercolor='black', borderwidth=1
        )
        fig.add_annotation(
            text="③", x=95, y=1.15,
            xref=xaxis_id, yref=yaxis_id,
            showarrow=False,
            font=dict(size=12, color='black'),
            bgcolor='white', bordercolor='black', borderwidth=1
        )
        
        # Curved arrow showing sequence
        fig.add_annotation(
            x=110, y=1.25, ax=100, ay=1.25,
            xref=xaxis_id, yref=yaxis_id,
            showarrow=True, arrowhead=2,
            arrowcolor='darkgreen', arrowwidth=2,
            arrowsize=1.2
        )
        
    if changes.get("equilibrium") == "Y3":
        # Arrow to final equilibrium
        fig.add_annotation(
            x=95, y=1.25, ax=110, ay=1.25,
            xref=xaxis_id, yref=yaxis_id,
            showarrow=True, arrowhead=2,
            arrowcolor='orange', arrowwidth=2,
            arrowsize=1.2
        )
    
    # 5. LONG-RUN: New money supply line M^S₂/P₂
    if changes.get("equilibrium") == "Y3":
        # Add new money supply line (prices have adjusted)
        fig.add_trace(
            go.Scatter(x=[60, 140], y=[1.8, 1.8], mode='lines',
                       line=dict(color='darkred', width=3, dash='dash'),
                       showlegend=False,
                       name="M^S₂/P₂"),
            row=row, col=col
        )
        
        # Label for new money supply
        fig.add_annotation(
            text="M<sup>S</sup>₂/P₂", x=65, y=1.75,
            xref=xaxis_id, yref=yaxis_id,
            showarrow=True, arrowhead=2,
            ax=65, ay=1.6,
            font=dict(size=12, color='darkred')
        )
        
        # Long-run equilibrium point
        fig.add_trace(
            go.Scatter(x=[100], y=[1.8], mode='markers',
                       marker=dict(color='black', size=10, symbol='diamond'),
                       showlegend=False,
                       name="Long-run eq"),
            row=row, col=col
        )
    
    # Vertical arrows showing money supply changes
    if changes.get("show_money_increase"):
        # Add downward arrow showing M^S increase
        fig.add_annotation(
            text="M<sup>S</sup>↑", x=125, y=1.5,
            xref=xaxis_id, yref=yaxis_id,
            showarrow=True, arrowhead=2,
            ax=125, ay=1.0,
            font=dict(size=16, color='red', weight='bold'),
            arrowcolor='red', arrowwidth=4
        )
        
    if changes.get("show_long_run"):
        # Show price adjustment arrow
        fig.add_annotation(
            text="P↑", x=135, y=1.5,
            xref=xaxis_id, yref=yaxis_id,
            showarrow=True, arrowhead=2,
            ax=135, ay=1.9,
            font=dict(size=16, color='darkred', weight='bold'),
            arrowcolor='darkred', arrowwidth=4
        )
    
    # Green dashed guide lines connecting to other panels
    if changes.get("lm_shift") and not changes.get("equilibrium") == "Y3":
        # Horizontal guide line at new interest rate
        fig.add_hline(y=1.0, line=dict(color='green', dash='dash', width=2),
                     row=row, col=col)
        # Vertical guide line at new money balance
        fig.add_vline(x=110, line=dict(color='green', dash='dash', width=2),
                     row=row, col=col)
        
        # Labels for guide lines
        fig.add_annotation(
            text="i₂", x=57, y=1.0,
            xref=xaxis_id, yref=yaxis_id,
            showarrow=False, font=dict(size=10, color='green'),
            bgcolor='white'
        )
    
    # Title
    fig.add_annotation(
        text="Money market", 
        x=100, y=3.8,
        xref=xaxis_id, yref=yaxis_id,
        showarrow=False, font=dict(size=12, weight='bold')
    )


def _add_ddaa_panel(fig, changes, row, col):
    """DD-AA panel with shift arrows."""
    Y = np.linspace(50, 150, 100)
    
    xaxis_id = fig.data[-1].xaxis
    yaxis_id = fig.data[-1].yaxis
    
    # Base curves
    DD1 = 2.0 - 0.005 * Y
    AA1 = 0.8 + 0.008 * Y
    
    # Pre-shock curves (gray)
    fig.add_trace(
        go.Scatter(x=Y, y=DD1, mode='lines',
                   line=dict(color='rgba(0,0,0,0.3)', width=2),
                   showlegend=False),
        row=row, col=col
    )
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
        text="AA₁", x=Y[0], y=AA1[0],
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
        
        # DD shift arrow
        if changes.get("show_dd_arrow"):
            fig.add_annotation(
                x=90, y=1.55, ax=110, ay=1.55,
                xref=xaxis_id, yref=yaxis_id,
                showarrow=True, arrowhead=3, arrowcolor='blue',
                arrowwidth=3, arrowsize=1.5,
                text="DD →", font=dict(size=12, color='blue')
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
        
        # AA shift arrow
        if changes.get("show_aa_arrow"):
            fig.add_annotation(
                x=80, y=1.44, ax=80, ay=1.54,
                xref=xaxis_id, yref=yaxis_id,
                showarrow=True, arrowhead=3, arrowcolor='red',
                arrowwidth=3, arrowsize=1.5,
                text="AA →", font=dict(size=12, color='red')
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
        fig.add_annotation(
            text="AA₃", x=Y[0], y=AA3[0],
            xref=xaxis_id, yref=yaxis_id,
            showarrow=False, xanchor='right', font=dict(size=10, color='red')
        )
        
        # AA return arrow
        if changes.get("show_aa_return_arrow"):
            fig.add_annotation(
                x=80, y=1.54, ax=80, ay=1.46,
                xref=xaxis_id, yref=yaxis_id,
                showarrow=True, arrowhead=3, arrowcolor='orange',
                arrowwidth=3, arrowsize=1.5,
                text="AA ←", font=dict(size=12, color='orange')
            )
    
    # Equilibrium points - calculated from curve intersections
    def calculate_equilibrium(dd_shift=0, aa_shift=0):
        # Solve: 2.0 - 0.005*Y + dd_shift = 0.8 + 0.008*Y + aa_shift
        Y = (1.2 + dd_shift - aa_shift) / 0.013
        E = 2.0 - 0.005 * Y + dd_shift
        return Y, E
    
    # Get equilibrium based on current state
    eq_state = changes.get("equilibrium", "Y1")
    
    if eq_state == "Y1":
        eq = calculate_equilibrium(0, 0)
    elif eq_state == "Y2":
        dd_s = 0.1 if changes.get("dd_shift") else 0
        aa_s = 0.1 if changes.get("aa_shift") == 1 else 0
        eq = calculate_equilibrium(dd_s, aa_s)
    elif eq_state == "Y3":
        dd_s = 0.1 if changes.get("dd_shift") else 0
        aa_s = 0.02 if changes.get("aa_shift") == 2 else 0
        eq = calculate_equilibrium(dd_s, aa_s)
    else:
        eq = calculate_equilibrium(0, 0)
    
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
            text="The interest rate remains at its level i₁. The AA shifts back to its original level.<br>The output remains at full-employment level: Y₁ = Y₃, i₁ = i₃, s₁ = s₃",
            x=0.98, y=0.02,
            xref="paper", yref="paper",
            showarrow=False, xanchor='right', yanchor='bottom',
            bgcolor='rgba(255,255,255,0.9)', bordercolor='red',
            borderwidth=2, font=dict(size=11, color='red')
        )


def _add_trajectory(fig, step_index, x_domains, y_domains):
    """Add red trajectory line with proper boundary handling."""
    
    def center(dom):
        return dom[0] + (dom[1] - dom[0]) / 2
    
    def get_panel_coords(panel_name, x_frac=0.5, y_frac=0.5):
        """Get coordinates within a specific panel"""
        panel_map = {
            'investment': ('xaxis', 'yaxis'),
            'demand': ('xaxis2', 'yaxis2'),
            'uip': ('xaxis3', 'yaxis3'),
            'lm': ('xaxis4', 'yaxis4'),
            'ddaa': ('xaxis5', 'yaxis5'),
        }
        x_axis, y_axis = panel_map[panel_name]
        x_dom = x_domains[x_axis]
        y_dom = y_domains[y_axis]
        return (
            x_dom[0] + (x_dom[1] - x_dom[0]) * x_frac,
            y_dom[0] + (y_dom[1] - y_dom[0]) * y_frac
        )
    
    # Define trajectories for each step
    trajectories = {
        1: [
            get_panel_coords('investment', 0.5, 1.0),  # Top of investment panel
            get_panel_coords('investment', 0.5, 0.5),  # Center of investment panel
        ],
        2: [
            get_panel_coords('investment', 0.5, 1.0),
            get_panel_coords('investment', 0.5, 0.5),
            get_panel_coords('uip', 0.5, 0.5),  # Center of UIP panel
        ],
        3: [
            get_panel_coords('investment', 0.5, 0.5),
            get_panel_coords('uip', 0.5, 0.5),
            get_panel_coords('uip', 0.5, 0.0),  # Bottom of UIP
            get_panel_coords('lm', 0.5, 0.0),    # Top of LM
            get_panel_coords('lm', 0.5, 0.5),    # Center of LM
        ],
        4: [
            get_panel_coords('investment', 0.5, 0.5),
            get_panel_coords('uip', 0.5, 0.5),
            get_panel_coords('uip', 0.5, 0.0),
            get_panel_coords('lm', 0.5, 0.0),
            get_panel_coords('lm', 0.5, 0.5),
            get_panel_coords('ddaa', 0.5, 0.5),  # Center of DD-AA
        ],
        5: [
            get_panel_coords('investment', 0.5, 0.5),
            get_panel_coords('uip', 0.5, 0.5),
            get_panel_coords('ddaa', 0.5, 0.5),
        ],
        6: [
            get_panel_coords('investment', 0.5, 0.5),
            get_panel_coords('uip', 0.5, 0.5),
            get_panel_coords('lm', 0.5, 0.5),
            get_panel_coords('ddaa', 0.5, 0.5),
        ]
    }
    
    if step_index in trajectories:
        points = trajectories[step_index]
        
        # Draw trajectory segments
        for i in range(len(points) - 1):
            fig.add_shape(
                type="line",
                x0=points[i][0], y0=points[i][1],
                x1=points[i+1][0], y1=points[i+1][1],
                xref="paper", yref="paper",
                line=dict(color="red", width=4),
                layer="above"
            )
        
        # Add arrowhead at the end
        if len(points) > 1:
            fig.add_annotation(
                x=points[-1][0], y=points[-1][1],
                ax=points[-2][0], ay=points[-2][1],
                xref="paper", yref="paper",
                showarrow=True, arrowhead=3,
                arrowcolor="red", arrowwidth=4,
                arrowsize=1.5
            )


def _add_shift_arrows(fig, changes, step_index):
    """Add animated shift arrows based on current step."""
    # Map step index to which arrows should be shown
    arrow_schedule = {
        1: ["show_i_arrow"],
        2: ["show_s_arrow"],
        3: ["show_aa_arrow"],
        4: ["show_dd_arrow"],
        5: [],
        6: ["show_aa_return_arrow"]
    }
    
    # Enable appropriate arrows for current step
    if step_index in arrow_schedule:
        for arrow_flag in arrow_schedule[step_index]:
            changes[arrow_flag] = True


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
            text="D₂ = C₂(Y₂ - T) + I(i₂)\n+G₁ + CA₂[(Y₂ - T), s₂P*/P]",
            x=0.85, y=0.85,
            xref="paper", yref="paper",
            showarrow=False,
            bgcolor='lightgreen', bordercolor='green',
            borderwidth=1, font=dict(size=10)
        )


def _style_figure(fig):
    """Apply consistent styling with thick black axes."""
    # Update all axes with thick black lines
    fig.update_xaxes(
        showgrid=False, zeroline=False,
        showline=True, linecolor='black', linewidth=3,  # Thick black axes
        mirror=True, ticks='outside',
        tickwidth=2, tickcolor='black'
    )
    fig.update_yaxes(
        showgrid=False, zeroline=False,
        showline=True, linecolor='black', linewidth=3,  # Thick black axes
        mirror=True, ticks='outside',
        tickwidth=2, tickcolor='black'
    )
    
    # Specific axis labels
    fig.update_xaxes(title_text="i", row=1, col=1)
    fig.update_yaxes(title_text="I", row=1, col=1)
    fig.update_xaxes(title_text="Output Y", row=1, col=2)
    fig.update_xaxes(title_text="i<sub>ERL</sub>", row=2, col=1)
    fig.update_yaxes(title_text="S<sub>ERL/USD</sub>", row=2, col=1)
    fig.update_xaxes(title_text="Real money balance M<sup>D</sup>/P and M<sup>S</sup>/P", row=3, col=1)
    fig.update_yaxes(title_text="i", row=3, col=1)
    fig.update_xaxes(title_text="Output Y", row=3, col=2)
    fig.update_yaxes(title_text="S<sub>ERL/USD</sub>", row=3, col=2)
    
    # Enhanced axis ranges for better visibility
    fig.update_xaxes(range=[0, 8], row=1, col=1)
    fig.update_yaxes(range=[30, 55], row=1, col=1)
    fig.update_xaxes(range=[60, 150], row=1, col=2)
    fig.update_yaxes(range=[60, 150], row=1, col=2)
    fig.update_xaxes(range=[0, 6], row=2, col=1)
    fig.update_yaxes(range=[1.2, 1.9], row=2, col=1)
    fig.update_xaxes(range=[55, 145], row=3, col=1)
    fig.update_yaxes(range=[0.2, 4], row=3, col=1)
    fig.update_xaxes(range=[50, 150], row=3, col=2)
    fig.update_yaxes(range=[1.2, 2.0], row=3, col=2)
    
    # Layout
    fig.update_layout(
        width=1000,
        height=750,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=40, l=60, r=60, b=60),
        font=dict(family="Arial, sans-serif", size=12, color="black")
    )


# Compatibility function
def build_canvas(data, frame=0):
    """Build diagram using solver output."""
    step_data = {"changes": {}}
    fig = build_complete_diagram(step_data, frame)
    return fig