import streamlit as st
from src.parameters import Parameters
from src.model import aggregate_demand
from src.solver import solve_equilibrium
from src import charts

st.set_page_config(page_title="Keynesian Cross", layout="centered")

st.title("Keynesian Cross Model")

with st.sidebar:
    st.header("Parameters")
    alpha = st.number_input("Autonomous Consumption (alpha)", value=50.0)
    beta = st.slider("MPC (beta)", min_value=0.0, max_value=0.9, value=0.6)
    invest_intercept = st.number_input("Investment Intercept", value=40.0)
    invest_slope = st.number_input("Investment Slope", value=5.0)
    government = st.number_input("Government Spending", value=20.0)
    tax = st.number_input("Taxes", value=10.0)
    interest = st.number_input("Interest Rate", value=2.0)
    params = Parameters(alpha=alpha, beta=beta,
                        investment_intercept=invest_intercept,
                        investment_slope=invest_slope,
                        government=government,
                        tax=tax)

equilibrium = solve_equilibrium(params, interest)

st.write(f"### Equilibrium Output: {equilibrium:.2f}")

y_range = charts.default_range(equilibrium)
fig = charts.ad_chart(params, interest, y_range)

st.plotly_chart(fig, use_container_width=True)
