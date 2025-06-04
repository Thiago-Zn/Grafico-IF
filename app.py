import streamlit as st
from src.parameters import Parameters
from src import solver, charts

st.set_page_config(page_title="DD-AA Model Simulator", layout="centered")

st.title("DD-AA Model: Monetary Policy Analysis")
st.markdown("**Maintaining the GDP at its Full Employment Level | Monetary Sector Shock**")

with st.sidebar:
    st.header("Model Parameters")
    
    st.subheader("Fiscal Policy")
    government = st.number_input("Government Spending (G)", min_value=0.0, max_value=100.0, value=50.0, step=5.0)
    tax = st.number_input("Taxes (T)", min_value=0.0, max_value=100.0, value=40.0, step=5.0)
    
    st.subheader("Monetary Policy")
    money_supply = st.slider("Money Supply (M)", min_value=50.0, max_value=200.0, value=100.0, step=10.0)
    interest = st.slider("Interest Rate (i)", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
    
    st.subheader("Consumption Parameters")
    alpha = st.number_input("Autonomous Consumption (α)", min_value=10.0, max_value=100.0, value=50.0, step=5.0)
    beta = st.slider("MPC (β)", min_value=0.0, max_value=0.95, value=0.6, step=0.05)
    
    st.subheader("Investment Parameters")
    invest_intercept = st.number_input("Investment Intercept (I₀)", min_value=10.0, max_value=100.0, value=40.0, step=5.0)
    invest_slope = st.number_input("Investment Slope (I₁)", min_value=1.0, max_value=20.0, value=5.0, step=1.0)
    
    st.subheader("Exchange Rate")
    exchange_rate = st.slider("Exchange Rate (E)", min_value=0.5, max_value=3.0, value=1.5, step=0.1)

# Create parameters object
params = Parameters(
    alpha=alpha,
    beta=beta,
    investment_intercept=invest_intercept,
    investment_slope=invest_slope,
    government=government,
    tax=tax
)

# Solve the model
data = solver.solve(params)

# Build and display the visualization
fig = charts.build_canvas(data)
st.plotly_chart(fig, use_container_width=True)

# Display key results
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Pre-shock Output (Y₁)", f"{data['equilibrium_pre'][0]:.1f}")
with col2:
    st.metric("Post-shock Output (Y₃)", f"{data['equilibrium_post'][0]:.1f}")
with col3:
    st.metric("Policy Result", "Y₁ = Y₃" if abs(data['equilibrium_pre'][0] - data['equilibrium_post'][0]) < 0.1 else "Adjustment needed")

# Add explanation
with st.expander("📖 Model Explanation", expanded=False):
    st.markdown("""
    ### The DD-AA Model Framework
    
    This interactive model demonstrates how **expansionary monetary policy** can maintain output at its full-employment level 
    following a monetary sector shock.
    
    #### Key Components:
    
    1. **Investment-i Panel**: Shows how investment responds to interest rate changes
    2. **Aggregate Demand Panel**: Displays the relationship between output (Y) and demand (D)
    3. **UIP Panel**: Uncovered Interest Parity condition linking domestic and foreign interest rates
    4. **LM Panel**: Money market equilibrium showing real money balance demand
    5. **DD-AA Panel**: The main equilibrium framework showing:
       - **DD Curve**: Goods market equilibrium
       - **AA Curve**: Asset market equilibrium
    
    #### Policy Mechanism:
    
    The **red trajectory** shows how the economy moves through the adjustment process:
    - Starting from initial equilibrium
    - Following the monetary expansion
    - Returning to full-employment output
    
    The expansionary monetary policy compensates for the change in money demand, keeping the interest rate 
    stable and maintaining output at its full-employment level: **Y₁ = Y₃**
    """)

with st.expander("🔧 Technical Details", expanded=False):
    st.markdown("""
    ### Model Equations
    
    **Consumption Function:**
    ```
    C = α + β(Y - T)
    ```
    
    **Investment Function:**
    ```
    I = I₀ - I₁ × i
    ```
    
    **Aggregate Demand:**
    ```
    D = C + I + G + CA(Y-T, E×P*/P)
    ```
    
    **Equilibrium Conditions:**
    - Goods Market: Y = D
    - Money Market: M/P = L(i, Y)
    - Foreign Exchange: i = i* + (Eᵉ - E)/E
    """)

# Footer
st.markdown("---")
st.caption("DD-AA Model Simulator | Based on Krugman-Obstfeld-Melitz International Economics framework")