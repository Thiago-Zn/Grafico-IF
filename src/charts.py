"""Charts module for DD-AA economic model visualization."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
        subplot_titles=("Invest-i", "Demanda D=Y", "UIP", "LM", "Painel DD-AA")
    )
    
    # 1. Investment-i subplot (top-left)
    invest_x, invest_y = data["invest_curve"]
    fig.add_trace(
        go.Scatter(x=invest_x, y=invest_y, mode="lines", 
                   line=dict(color="#1f77b4", width=3),
                   showlegend=False),
        row=1, col=1
    )
    
    # 2. Demand D=Y subplot (top-right)
    demand_data = data["demand_line"]
    # 45-degree line
    fig.add_trace(
        go.Scatter(x=demand_data["line45_x"], y=demand_data["line45_y"],
                   mode="lines", line=dict(color="rgba(200,150,200,0.8)", width=2),
                   showlegend=False),
        row=1, col=2
    )
    # AD line
    fig.add_trace(
        go.Scatter(x=demand_data["ad_x"], y=demand_data["ad_y"],
                   mode="lines", line=dict(color="green", width=2),
                   showlegend=False),
        row=1, col=2
    )
    
    # 3. UIP subplot (middle-left)
    uip_x, uip_y = data["uip_curve"]
    fig.add_trace(
        go.Scatter(x=uip_x, y=uip_y, mode="lines",
                   line=dict(color="#1f77b4", width=3),
                   showlegend=False),
        row=2, col=1
    )
    
    # 4. LM subplot (middle-right)
    lm_x, lm_y = data["lm_curve"]
    fig.add_trace(
        go.Scatter(x=lm_x, y=lm_y, mode="lines",
                   line=dict(color="#1f77b4", width=3),
                   showlegend=False),
        row=2, col=2
    )
    
    # 5. DD-AA Panel (bottom)
    # Pre-shock curves (gray)
    dd_pre_x, dd_pre_y = data["points_DD_pre"]
    aa_pre_x, aa_pre_y = data["points_AA_pre"]
    fig.add_trace(
        go.Scatter(x=dd_pre_x, y=dd_pre_y, mode="lines",
                   line=dict(color="rgba(0,0,0,0.25)", width=2),
                   name="DD (pré)", showlegend=False),
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(x=aa_pre_x, y=aa_pre_y, mode="lines",
                   line=dict(color="rgba(0,0,0,0.25)", width=2),
                   name="AA (pré)", showlegend=False),
        row=3, col=1
    )
    
    # Post-shock curves
    dd_post_x, dd_post_y = data["points_DD_post"]
    aa_post_x, aa_post_y = data["points_AA_post"]
    fig.add_trace(
        go.Scatter(x=dd_post_x, y=dd_post_y, mode="lines",
                   line=dict(color="#1f77b4", width=3),
                   name="DD", showlegend=False),
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(x=aa_post_x, y=aa_post_y, mode="lines",
                   line=dict(color="#d62728", width=3),
                   name="AA", showlegend=False),
        row=3, col=1
    )
    
    # Equilibrium points
    eq_pre = data["equilibrium_pre"]
    eq_post = data["equilibrium_post"]
    fig.add_trace(
        go.Scatter(x=[eq_pre[0]], y=[eq_pre[1]], mode="markers",
                   marker=dict(color="black", size=8),
                   showlegend=False),
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(x=[eq_post[0]], y=[eq_post[1]], mode="markers",
                   marker=dict(color="black", size=8),
                   showlegend=False),
        row=3, col=1
    )
    
    # Red trajectory line (using paper coordinates)
    fig.add_trace(
        go.Scatter(
            x=[0.05, 0.45, 0.45, 0.70, 0.70, 0.50],
            y=[0.88, 0.88, 0.66, 0.66, 0.44, 0.26],
            mode="lines",
            line=dict(color="red", width=4),
            xref="paper", yref="paper",
            showlegend=False
        )
    )
    
    # Add arrows showing AA displacement
    fig.add_shape(
        type="line",
        x0=aa_pre_x[len(aa_pre_x)//2], y0=aa_pre_y[len(aa_pre_y)//2],
        x1=aa_post_x[len(aa_post_x)//2], y1=aa_post_y[len(aa_post_y)//2],
        line=dict(color="red", width=2),
        xref="x5", yref="y5",
        row=3, col=1
    )
    fig.add_annotation(
        x=aa_post_x[len(aa_post_x)//2], y=aa_post_y[len(aa_post_y)//2],
        ax=aa_pre_x[len(aa_pre_x)//2], ay=aa_pre_y[len(aa_pre_y)//2],
        xref="x5", yref="y5",
        axref="x5", ayref="y5",
        showarrow=True,
        arrowhead=3,
        arrowcolor="red",
        arrowwidth=2,
        row=3, col=1
    )
    
    # Add text box in DD-AA panel
    fig.add_annotation(
        text="The expansionary monetary policy<br>compensates for the initial<br>contractionary fiscal shock",
        xref="paper", yref="paper",
        x=0.95, y=0.05,
        showarrow=False,
        bgcolor="lavender",
        bordercolor="purple",
        borderwidth=1,
        font=dict(size=10)
    )
    
    # Update axes
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    
    # Set minimal ticks for mini panels
    for row in range(1, 3):
        for col in range(1, 3):
            fig.update_xaxes(showticklabels=True, tickmode="linear", 
                            nticks=4, row=row, col=col)
            fig.update_yaxes(showticklabels=True, tickmode="linear", 
                            nticks=4, row=row, col=col)
    
    # DD-AA panel axes labels
    fig.update_xaxes(title_text="Y", row=3, col=1)
    fig.update_yaxes(title_text="E", row=3, col=1)
    
    # Update layout
    fig.update_layout(
        width=900,
        height=750,
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=12, color="black")
    )
    
    return fig