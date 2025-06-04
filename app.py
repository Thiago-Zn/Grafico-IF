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

# Define all Chapter 17 scenarios
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
    ],
    "Temporary Monetary Expansion": [
        {
            "title": "Initial Equilibrium",
            "description": "Economy at full employment Y₁",
            "changes": {}
        },
        {
            "title": "Money Supply Increase",
            "description": "Central bank temporarily increases M^S → LM shifts right → i falls",
            "changes": {"lm_shift": True, "i_level": "i2"}
        },
        {
            "title": "Limited UIP Response",
            "description": "Lower i → Limited depreciation (agents expect reversal) → Small AA shift",
            "changes": {"lm_shift": True, "i_level": "i2", "aa_shift": 0.5}
        },
        {
            "title": "Short-Run Equilibrium",
            "description": "Small increase in Y and E due to expectations",
            "changes": {"lm_shift": True, "i_level": "i2", "aa_shift": 0.5, "equilibrium": "Y1.5"}
        },
        {
            "title": "Policy Reversal",
            "description": "Money supply returns to original level → Back to Y₁",
            "changes": {}
        }
    ],
    "Permanent Fiscal Expansion": [
        {
            "title": "Initial Equilibrium",
            "description": "Economy at full employment Y₁",
            "changes": {}
        },
        {
            "title": "Government Spending Increase",
            "description": "G increases → DD shifts right immediately",
            "changes": {"dd_shift": True}
        },
        {
            "title": "Short-Run Effects",
            "description": "Higher Y → Higher money demand → i rises → Currency appreciates",
            "changes": {"dd_shift": True, "i_level": "i2.5", "s_level": "s0.5"}
        },
        {
            "title": "AA Response",
            "description": "Higher i → AA shifts left → Partial crowding out",
            "changes": {"dd_shift": True, "aa_shift": -1, "equilibrium": "Y1.3"}
        },
        {
            "title": "Long-Run Adjustment",
            "description": "Prices rise → Real money supply falls → Further crowding out",
            "changes": {"dd_shift": True, "aa_shift": -1.5, "equilibrium": "Y1", "s_level": "s0.3"}
        }
    ],
    "Temporary Fiscal Expansion": [
        {
            "title": "Initial Equilibrium",
            "description": "Economy at full employment Y₁",
            "changes": {}
        },
        {
            "title": "Government Spending Increase",
            "description": "Temporary G increase → DD shifts right",
            "changes": {"dd_shift": True}
        },
        {
            "title": "Short-Run Response",
            "description": "Y rises → i rises → Limited currency appreciation",
            "changes": {"dd_shift": True, "i_level": "i2", "equilibrium": "Y1.2"}
        },
        {
            "title": "Policy Reversal",
            "description": "G returns to original level → DD shifts back",
            "changes": {}
        }
    ],
    "Permanent Real Sector Shock": [
        {
            "title": "Initial Equilibrium",
            "description": "Economy at full employment Y₁",
            "changes": {}
        },
        {
            "title": "Productivity Improvement",
            "description": "Technology advance → Potential output increases → Y* rises",
            "changes": {"y_potential": "Y2"}
        },
        {
            "title": "Investment Response",
            "description": "Higher productivity → Investment increases → i falls",
            "changes": {"y_potential": "Y2", "i_level": "i2", "investment_shift": True}
        },
        {
            "title": "DD and AA Adjustments",
            "description": "Higher I → DD shifts right; Lower i → AA shifts right",
            "changes": {"dd_shift": True, "aa_shift": 1, "equilibrium": "Y2"}
        },
        {
            "title": "New Long-Run Equilibrium",
            "description": "Economy at new full employment Y₂ > Y₁",
            "changes": {"dd_shift": True, "aa_shift": 1, "equilibrium": "Y2", "y_potential": "Y2"}
        }
    ],
    "Monetary Contraction": [
        {
            "title": "Initial Equilibrium",
            "description": "Economy at full employment Y₁",
            "changes": {}
        },
        {
            "title": "Money Supply Decrease",
            "description": "Central bank reduces M^S → LM shifts left → i rises",
            "changes": {"lm_shift": -1, "i_level": "i3"}
        },
        {
            "title": "UIP Response",
            "description": "Higher interest rate → Currency appreciates → AA shifts left",
            "changes": {"lm_shift": -1, "i_level": "i3", "aa_shift": -1}
        },
        {
            "title": "DD Adjustment",
            "description": "Appreciation hurts exports → DD shifts left",
            "changes": {"lm_shift": -1, "i_level": "i3", "aa_shift": -1, "dd_shift": -1}
        },
        {
            "title": "Short-Run Recession",
            "description": "Economy at Y₀ < Y₁ with lower exchange rate",
            "changes": {"lm_shift": -1, "i_level": "i3", "aa_shift": -1, "dd_shift": -1, "equilibrium": "Y0"}
        },
        {
            "title": "Long-Run Adjustment",
            "description": "Prices fall → AA shifts back → Return to Y₁ with lower E",
            "changes": {"lm_shift": -1, "i_level": "i1", "aa_shift": -0.5, "dd_shift": -1, "equilibrium": "Y1"}
        }
    ]
}

# Header with improved styling
st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 1rem 0;
    border-bottom: 3px solid #003366;
    margin-bottom: 2rem;
}
.scenario-title {
    color: #003366;
    font-size: 2.5rem;
    font-weight: bold;
    margin: 0;
}
.step-description {
    color: #666;
    font-size: 1.5rem;
    margin: 0.5rem 0 0 0;
}
</style>
""", unsafe_allow_html=True)

# Display header
current_scenario = st.session_state.scenario
current_step = st.session_state.current_step
steps = SCENARIOS[current_scenario]
current_data = steps[current_step]

st.markdown(f"""
<div class="main-header">
    <h1 class="scenario-title">{current_scenario}</h1>
    <p class="step-description">Step {current_step + 1} of {len(steps)}: {current_data['description']}</p>
</div>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([4.5, 1.5])

with col1:
    # Build and display the figure
    fig = charts.build_complete_diagram(current_data, current_step)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Scenario selector with all Chapter 17 options
    st.markdown("### Select Economic Scenario")
    new_scenario = st.selectbox(
        "Select scenario",
        options=list(SCENARIOS.keys()),
        index=list(SCENARIOS.keys()).index(st.session_state.scenario),
        key="scenario_selector",
        label_visibility="hidden"
    )
    
    if new_scenario != st.session_state.scenario:
        st.session_state.scenario = new_scenario
        st.session_state.current_step = 0
        st.rerun()
    
    st.markdown("---")
    
    # Navigation section
    st.markdown("### Navigation")
    
    col_back, col_forward = st.columns(2)
    
    with col_back:
        if st.button("⬅️ Previous", 
                    disabled=(current_step == 0),
                    use_container_width=True,
                    help="Go to previous step"):
            st.session_state.current_step = max(0, current_step - 1)
            st.rerun()
    
    with col_forward:
        max_steps = len(steps) - 1
        if st.button("Next ➡️",
                    disabled=(current_step >= max_steps),
                    use_container_width=True,
                    help="Go to next step"):
            st.session_state.current_step = min(max_steps, current_step + 1)
            st.rerun()
    
    # Progress indicator
    progress = (current_step + 1) / len(steps)
    st.progress(progress)
    st.markdown(f"**Step {current_step + 1} of {len(steps)}**")
    
    # Step details
    st.markdown("---")
    st.markdown("### Current Step")
    st.info(f"**{current_data['title']}**\n\n{current_data['description']}")
    
    # Economic indicators (optional)
    if current_data.get('changes'):
        st.markdown("### Key Changes")
        changes = current_data['changes']
        
        indicators = []
        if changes.get('i_level'):
            indicators.append(f"Interest rate: {changes['i_level']}")
        if changes.get('equilibrium'):
            indicators.append(f"Output: {changes['equilibrium']}")
        if changes.get('s_level'):
            indicators.append(f"Exchange rate: {changes['s_level']}")
        
        for indicator in indicators:
            st.markdown(f"- {indicator}")

# Add explanatory text at bottom
with st.expander("📚 About the DD-AA Model"):
    st.markdown("""
    The **DD-AA model** is a framework for analyzing the short-run behavior of an open economy under flexible exchange rates.
    
    - **DD curve**: Shows combinations of output (Y) and exchange rate (E) where the goods market is in equilibrium
    - **AA curve**: Shows combinations where the asset markets (money and foreign exchange) are in equilibrium
    
    This interactive tool demonstrates how various economic shocks affect the equilibrium through step-by-step animations.
    
    **Key mechanisms:**
    - Monetary policy affects interest rates → exchange rates → output
    - Fiscal policy affects demand → output → interest rates → exchange rates
    - Real shocks affect productivity → investment → both curves
    
    Each scenario shows the complete adjustment path from initial shock to new equilibrium.
    """)

# Hide Streamlit elements
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)