import streamlit as st
from src import charts
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="DD-AA Model Simulator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'scenario' not in st.session_state:
    st.session_state.scenario = "Permanent Monetary Expansion"

# Define scenarios and their steps
SCENARIOS = {
    "Permanent Monetary Expansion": [
        {
            "title": "Initial Equilibrium",
            "description": "Economy at full employment Y₁",
            "changes": {}
        },
        {
            "title": "Money Supply Increase",
            "description": "Central bank increases M^S → LM shifts right → i falls",
            "changes": {"lm_shift": True, "i_level": "i2"}
        },
        {
            "title": "UIP Response",
            "description": "Lower interest rate → Currency depreciates → AA shifts right",
            "changes": {"lm_shift": True, "i_level": "i2", "aa_shift": 1}
        },
        {
            "title": "DD Adjustment",
            "description": "Depreciation boosts exports → DD shifts right",
            "changes": {"lm_shift": True, "i_level": "i2", "aa_shift": 1, "dd_shift": True}
        },
        {
            "title": "New Short-Run Equilibrium",
            "description": "Economy at Y₂ > Y₁ with higher exchange rate",
            "changes": {"lm_shift": True, "i_level": "i2", "aa_shift": 1, "dd_shift": True, "equilibrium": "Y2"}
        },
        {
            "title": "Long-Run Adjustment",
            "description": "Prices adjust → AA shifts back → Return to Y₁ with permanently higher E",
            "changes": {"lm_shift": True, "i_level": "i3", "aa_shift": 2, "dd_shift": True, "equilibrium": "Y3"}
        }
    ]
}

# Header
st.markdown("""
<h2 style='text-align: center; color: #003366;'>
Maintaining the GDP at its Full Employment Level
</h2>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([5, 1])

with col1:
    # Get current step data
    steps = SCENARIOS[st.session_state.scenario]
    current_data = steps[st.session_state.current_step]
    
    # Build the figure
    fig = charts.build_complete_diagram(current_data, st.session_state.current_step)
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Scenario selector
    st.selectbox(
        "Select Scenario",
        options=list(SCENARIOS.keys()),
        key="scenario",
        on_change=lambda: setattr(st.session_state, 'current_step', 0)
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation buttons
    col_back, col_forward = st.columns(2)
    
    with col_back:
        if st.button("⬅️ Back", 
                    disabled=(st.session_state.current_step == 0),
                    use_container_width=True):
            st.session_state.current_step = max(0, st.session_state.current_step - 1)
            st.rerun()
    
    with col_forward:
        max_steps = len(SCENARIOS[st.session_state.scenario]) - 1
        if st.button("Forward ➡️",
                    disabled=(st.session_state.current_step >= max_steps),
                    use_container_width=True):
            st.session_state.current_step = min(max_steps, st.session_state.current_step + 1)
            st.rerun()
    
    # Step indicator
    st.markdown(f"""
    <div style='text-align: center; padding: 20px 0;'>
    <b>Frame {st.session_state.current_step + 1} of {len(steps)}</b>
    </div>
    """, unsafe_allow_html=True)
    
    # Current step description
    st.info(current_data["description"])

# Hide Streamlit elements
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)