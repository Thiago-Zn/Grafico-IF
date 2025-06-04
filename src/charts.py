"""Charts module for DD-AA economic model visualization."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def build_canvas(data: dict) -> go.Figure:
    """Build the complete DD-AA model visualization with all subplots."""
    
    # Create subplots layout
    fig = make_subplots(
        rows=3, cols=2,
        specs=[[{}, {}],
               [{}, {}],
               [{"colspan": 2}, None]],
        vertical_spacing=0.08,
        horizontal_spacing=0.05,
        subplot_titles=("Investment, i", "Aggregate demand", "S<sub>ERL/USD</sub>", 
                        "Real money balance M<sup>D</sup>/P and M/P", "")
    )
    
    # 1. Investment-i subplot (top-left)
    invest_x, invest_y = data["invest_curve"]
    fig.add_trace(
        go.Scatter(x=invest_x, y=invest_y, mode="lines", 
                   line=dict(color="#1f77b4", width=3),
                   showlegend=False),
        row=1, col=1
    )
    
    # Add horizontal dashed lines and labels for i0, i1, i2
    i_levels = [invest_y[0], invest_y[len(invest_y)//2], invest_y[-1]]
    i_labels = ["i<sub>0</sub>", "i<sub>1</sub>", "i<sub>2</sub>"]
    for i, (level, label) in enumerate(zip(i_levels, i_labels)):
        fig.add_hline(y=level, line=dict(color="gray", dash="dash", width=1),
                      row=1, col=1)
        fig.add_annotation(x=invest_x[0]-0.05*np.ptp(invest_x), y=level, 
                          text=label, showarrow=False, xanchor="right",
                          row=1, col=1)
    
    # Add vertical dashed lines
    for x_val in [invest_x[0], invest_x[len(invest_x)//2], invest_x[-1]]:
        fig.add_vline(x=x_val, line=dict(color="purple", dash="dash", width=1),
                      row=1, col=1)
    
    # 2. Demand D=Y subplot (top-right)
    demand_data = data["demand_line"]
    
    # 45-degree line (D = Y)
    fig.add_trace(
        go.Scatter(x=demand_data["line45_x"], y=demand_data["line45_y"],
                   mode="lines", line=dict(color="rgba(200,150,200,0.8)", width=2),
                   name="D = Y", showlegend=False),
        row=1, col=2
    )
    
    # Multiple demand lines D1, D2, D3
    colors = ["green", "green", "purple"]
    for i, color in enumerate(colors):
        y_shift = i * 0.1 * np.max(demand_data["ad_y"])
        fig.add_trace(
            go.Scatter(x=demand_data["ad_x"], 
                      y=demand_data["ad_y"] + y_shift,
                      mode="lines", line=dict(color=color, width=2),
                      name=f"D<sub>{i+1}</sub>", showlegend=False),
            row=1, col=2
        )
    
    # Add D3 = D1 annotation
    fig.add_annotation(
        text="D<sub>3</sub> = D<sub>1</sub>",
        xref="x2", yref="y2",
        x=demand_data["ad_x"][len(demand_data["ad_x"])//2],
        y=demand_data["ad_y"][len(demand_data["ad_y"])//2] + 0.2*np.max(demand_data["ad_y"]),
        showarrow=False,
        bgcolor="lavender",
        bordercolor="purple",
        borderwidth=1,
        row=1, col=2
    )
    
    # Add vertical dashed lines Y2, Y3, Y1
    y_positions = [0.3, 0.5, 0.7]
    y_labels = ["Y<sub>2</sub>", "Y<sub>3</sub>", "Y<sub>1</sub>"]
    for pos, label in zip(y_positions, y_labels):
        x_val = np.max(demand_data["ad_x"]) * pos
        fig.add_vline(x=x_val, line=dict(color="purple", dash="dash", width=1),
                      row=1, col=2)
        fig.add_annotation(x=x_val, y=0, text=label, showarrow=False,
                          yanchor="top", row=1, col=2)
    
    # 3. UIP subplot (middle-left)
    uip_x, uip_y = data["uip_curve"]
    fig.add_trace(
        go.Scatter(x=uip_x, y=uip_y, mode="lines",
                   line=dict(color="#1f77b4", width=3),
                   showlegend=False),
        row=2, col=1
    )
    
    # Add horizontal dashed lines for s1, s2, s3
    s_levels = [uip_y[-1], uip_y[len(uip_y)//2], uip_y[0]]
    s_labels = ["s<sub>1</sub>", "s<sub>2</sub>", "s<sub>3</sub>"]
    for level, label in zip(s_levels, s_labels):
        fig.add_hline(y=level, line=dict(color="gray", dash="dash", width=1),
                      row=2, col=1)
        fig.add_annotation(x=uip_x[0]-0.05*np.ptp(uip_x), y=level, 
                          text=label, showarrow=False, xanchor="right",
                          row=2, col=1)
    
    # Add vertical dashed lines from UIP points
    for i in [0, len(uip_x)//2, -1]:
        fig.add_vline(x=uip_x[i], line=dict(color="purple", dash="dash", width=1),
                      row=2, col=1)
    
    # Add UIP formula annotation
    fig.add_annotation(
        text="i<sub>USA</sub> + (s̄<sup>e</sup> - s)/s",
        xref="x3", yref="y3",
        x=np.mean(uip_x), y=np.min(uip_y) - 0.1*np.ptp(uip_y),
        showarrow=False, row=2, col=1
    )
    
    # 4. LM subplot (middle-right)
    lm_x, lm_y = data["lm_curve"]
    
    # Multiple LM curves
    colors = ["#1f77b4", "green", "#d62728"]
    labels = ["L<sub>1</sub>(i, Y<sub>1</sub>)", 
              "L<sub>2</sub>(i, Y<sub>2</sub>)", 
              "L<sub>3</sub>(i, Y<sub>3</sub>)"]
    
    for i, (color, label) in enumerate(zip(colors, labels)):
        x_shift = i * 0.2 * np.max(lm_x)
        fig.add_trace(
            go.Scatter(x=lm_x + x_shift, y=lm_y,
                      mode="lines", line=dict(color=color, width=2),
                      name=label, showlegend=False),
            row=2, col=2
        )
        # Add label
        fig.add_annotation(
            text=label, xref="x4", yref="y4",
            x=lm_x[-1] + x_shift, y=lm_y[-1],
            showarrow=False, xanchor="left",
            row=2, col=2
        )
    
    # Add M^S/P lines
    fig.add_annotation(
        text="M<sup>S</sup>/P<sub>1</sub>",
        xref="x4", yref="y4",
        x=np.max(lm_x)*0.8, y=np.mean(lm_y),
        showarrow=False, row=2, col=2
    )
    
    # 5. DD-AA Panel (bottom) - Add title
    fig.add_annotation(
        text="Rates of return<br>in terms of ERL",
        xref="x5", yref="y5",
        x=np.mean(data["points_DD_pre"][0])*0.5,
        y=np.max(data["points_AA_pre"][1])*1.1,
        showarrow=False,
        font=dict(size=10),
        row=3, col=1
    )
    
    # Pre-shock curves (gray)
    dd_pre_x, dd_pre_y = data["points_DD_pre"]
    aa_pre_x, aa_pre_y = data["points_AA_pre"]
    fig.add_trace(
        go.Scatter(x=dd_pre_x, y=dd_pre_y, mode="lines",
                   line=dict(color="rgba(0,0,0,0.25)", width=2),
                   name="DD<sub>1</sub>", showlegend=False),
        row=3, col=1
    )
    fig.add_annotation(
        text="DD<sub>1</sub>", x=dd_pre_x[-1], y=dd_pre_y[-1],
        showarrow=False, xanchor="left", row=3, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=aa_pre_x, y=aa_pre_y, mode="lines",
                   line=dict(color="rgba(0,0,0,0.25)", width=2),
                   name="AA<sub>1=3</sub>", showlegend=False),
        row=3, col=1
    )
    fig.add_annotation(
        text="AA<sub>1=3</sub>", x=aa_pre_x[0], y=aa_pre_y[0],
        showarrow=False, xanchor="right", row=3, col=1
    )
    
    # Post-shock curves
    dd_post_x, dd_post_y = data["points_DD_post"]
    aa_post_x, aa_post_y = data["points_AA_post"]
    fig.add_trace(
        go.Scatter(x=dd_post_x, y=dd_post_y, mode="lines",
                   line=dict(color="#1f77b4", width=3),
                   name="DD<sub>2</sub>", showlegend=False),
        row=3, col=1
    )
    fig.add_annotation(
        text="DD<sub>2</sub>", x=dd_post_x[-1], y=dd_post_y[-1],
        showarrow=False, xanchor="left", row=3, col=1
    )
    
    # AA2 curve (shifted right)
    aa2_x = aa_post_x
    aa2_y = aa_post_y
    fig.add_trace(
        go.Scatter(x=aa2_x, y=aa2_y, mode="lines",
                   line=dict(color="#d62728", width=3),
                   name="AA<sub>2</sub>", showlegend=False),
        row=3, col=1
    )
    fig.add_annotation(
        text="AA<sub>2</sub>", x=aa2_x[0], y=aa2_y[0],
        showarrow=False, xanchor="right", row=3, col=1
    )
    
    # Equilibrium points
    eq_pre = data["equilibrium_pre"]
    eq_post = data["equilibrium_post"]
    fig.add_trace(
        go.Scatter(x=[eq_pre[0]], y=[eq_pre[1]], mode="markers",
                   marker=dict(color="black", size=10),
                   showlegend=False),
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(x=[eq_post[0]], y=[eq_post[1]], mode="markers",
                   marker=dict(color="black", size=10),
                   showlegend=False),
        row=3, col=1
    )
    
    # Red arrows showing AA shifts
    arrow_y = np.mean(aa_pre_y)
    fig.add_annotation(
        x=aa2_x[len(aa2_x)//2], y=arrow_y,
        ax=aa_pre_x[len(aa_pre_x)//2], ay=arrow_y,
        xref="x5", yref="y5", axref="x5", ayref="y5",
        showarrow=True, arrowhead=3, arrowsize=1.5,
        arrowcolor="red", arrowwidth=3,
        row=3, col=1
    )
    
    # Add vertical lines for Y positions
    fig.add_vline(x=eq_pre[0], line=dict(color="purple", dash="dash", width=1),
                  row=3, col=1)
    fig.add_annotation(x=eq_pre[0], y=0, text="Y<sub>3</sub>→Y<sub>1</sub>",
                      showarrow=False, yanchor="top", row=3, col=1)
    
    # Add policy explanation box
    fig.add_annotation(
        text="The EXPANSIONARY MONETARY policy<br>compensates the change in money demand<br>and the interest rate remains at its level i<sub>1</sub>.<br>The AA shifts back to its original level The<br>output remains at it full-employment level:<br>Y<sub>1</sub> = Y<sub>3</sub>   i<sub>1</sub> = i<sub>3</sub>   s<sub>1</sub> = s<sub>3</sub>",
        xref="x5", yref="y5",
        x=np.max(dd_post_x)*0.95, y=np.min(aa_pre_y)*1.2,
        showarrow=False,
        bgcolor="lavender",
        bordercolor="purple",
        borderwidth=2,
        font=dict(size=11),
        align="left",
        row=3, col=1
    )
    
    # Red trajectory line
    fig.add_trace(
        go.Scatter(
            x=[0.22, 0.22, 0.45, 0.45, 0.55, 0.55, 0.78, 0.78, 0.50],
            y=[0.83, 0.78, 0.78, 0.55, 0.55, 0.50, 0.50, 0.35, 0.26],
            mode="lines",
            line=dict(color="red", width=4),
            xref="paper", yref="paper",
            showlegend=False
        )
    )
    
    # Top formula box
    fig.add_annotation(
        text="D<sub>3</sub> = D<sub>1</sub> = C<sub>1</sub>(Y<sub>1</sub> - T) + I(i<sub>1=4</sub>) + G<sub>1</sub> + CA<sub>1</sub>[(Y<sub>1</sub> - T), s<sub>1=4</sub>P*/P]",
        xref="paper", yref="paper",
        x=0.5, y=0.98,
        showarrow=False,
        bgcolor="lavender",
        bordercolor="purple",
        borderwidth=1,
        font=dict(size=12)
    )
    
    # D2 formula box
    fig.add_annotation(
        text="D<sub>2</sub> = C<sub>2</sub>(Y<sub>2</sub> - T) + I(i<sub>1</sub>)<br>+G<sub>1</sub> + CA<sub>2</sub>[(Y<sub>2</sub> - T), s<sub>3</sub>P*/P]",
        xref="x2", yref="y2",
        x=np.max(demand_data["ad_x"])*0.7,
        y=np.max(demand_data["ad_y"])*0.5,
        showarrow=False,
        bgcolor="lightgreen",
        bordercolor="green",
        borderwidth=1,
        font=dict(size=10),
        row=1, col=2
    )
    
    # Update axes
    fig.update_xaxes(showgrid=False, zeroline=False, showline=True, linecolor="black",
                     mirror=True, ticks="outside", tickcolor="black")
    fig.update_yaxes(showgrid=False, zeroline=False, showline=True, linecolor="black",
                     mirror=True, ticks="outside", tickcolor="black")
    
    # Add axis arrows
    for row in range(1, 4):
        for col in range(1, 3):
            if not (row == 3 and col == 2):  # Skip empty subplot
                # Add arrow to x-axis
                fig.add_annotation(
                    x=1, y=0, xref=f"x{(row-1)*2+col} domain", yref=f"y{(row-1)*2+col} domain",
                    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
                    arrowcolor="black", ax=-0.02, ay=0, axref=f"x{(row-1)*2+col} domain",
                    ayref=f"y{(row-1)*2+col} domain"
                )
                # Add arrow to y-axis
                fig.add_annotation(
                    x=0, y=1, xref=f"x{(row-1)*2+col} domain", yref=f"y{(row-1)*2+col} domain",
                    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
                    arrowcolor="black", ax=0, ay=-0.02, axref=f"x{(row-1)*2+col} domain",
                    ayref=f"y{(row-1)*2+col} domain"
                )
    
    # Set axis labels
    fig.update_xaxes(title_text="i", row=1, col=1)
    fig.update_xaxes(title_text="Output Y", row=1, col=2)
    fig.update_xaxes(title_text="i<sub>ERL</sub>", row=2, col=1)
    fig.update_xaxes(title_text="i", row=2, col=2)
    fig.update_xaxes(title_text="Output Y", row=3, col=1)
    
    fig.update_yaxes(title_text="I", row=1, col=1)
    fig.update_yaxes(title_text="", row=1, col=2)
    fig.update_yaxes(title_text="S<sub>ERL/USD</sub>", row=2, col=1)
    fig.update_yaxes(title_text="", row=2, col=2)
    fig.update_yaxes(title_text="S<sub>ERL/USD</sub>", row=3, col=1)
    
    # Update layout
    fig.update_layout(
        title={
            'text': "Maintaining the GPP at its Full Employment Level | Monetary Sector Shock<br>EXPANSIONARY MONETARY POLICY",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'darkblue'}
        },
        width=900,
        height=750,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=12, color="black"),
        margin=dict(t=100, l=50, r=50, b=50)
    )
    
    return fig