# Keynesian Cross Interactive Model

This project provides a small economic simulator written in Python. It focuses on the basic Keynesian cross model widely used in introductory macroeconomics. The model illustrates how aggregate demand (AD) depends on income and how equilibrium output is determined when planned expenditure equals actual production. The repository includes a Streamlit application to explore the model interactively, a set of reusable Python modules, and unit tests that validate the economic relationships. A GitHub Actions workflow ensures that changes continue to pass the test suite.

## Economic background

The Keynesian cross is a simple framework capturing the short‑run relationship between output and planned spending. Households decide how much to consume based on disposable income, while firms plan investment according to the interest rate. Government spending and taxation are treated as policy variables. Formally, consumption is

```
C = α + β(Y − T)
```

where `α` is autonomous consumption, `β` is the marginal propensity to consume (MPC), `Y` is income, and `T` represents taxes. Investment decreases with the interest rate `r` according to

```
I = I0 − I1 r
```

Government spending `G` is assumed exogenous. Planned expenditure is then

```
AD = C + I + G
```

Equilibrium occurs when planned expenditure equals output (`Y = AD`). Solving this equation yields the level of income that clears the goods market. The solution is

```
Y = [α + I0 − I1 r + G − β T] / (1 − β)
```

The repository implements these formulas in straightforward Python functions. Although highly stylized, the model conveys the intuition of how fiscal policy and interest‑rate movements shift aggregate demand and, in turn, output.

## Repository structure

```
app.py                  – Streamlit user interface
requirements.txt        – Python dependencies
src/
    parameters.py       – Data classes for model parameters
    model.py            – Consumption, investment and AD functions
    solver.py           – Closed form solution for equilibrium
    charts.py           – Plotly chart helpers
tests/
    test_model.py       – Unit test for aggregate demand
    test_solver.py      – Unit test for the solver
.streamlit/config.toml  – Streamlit configuration
.github/workflows/      – Continuous integration via GitHub Actions
```

All economic logic resides within the `src` package, making it easy to import the functions into other projects or extend the model. The Streamlit application in `app.py` acts as a thin layer on top of these modules. Users can tweak parameters with sliders and immediately see how equilibrium output changes. A Plotly chart displays the aggregate demand curve together with the 45‑degree line commonly used in textbook diagrams. A dashed vertical marker highlights the equilibrium level of output.

## Usage

1. **Install dependencies.** Create a Python 3.11 virtual environment and install the packages:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run the app.** Launch Streamlit from the command line:
   ```bash
   streamlit run app.py
   ```
   A browser window will open showing sliders for the parameters. Adjusting these sliders updates the graph and equilibrium calculation in real time.

3. **Execute tests.** To make sure all functions behave as expected, run:
   ```bash
   pytest -q
   ```
   The included tests verify that aggregate demand is calculated correctly and that the closed form solver matches the economic formula derived above. Continuous integration on GitHub also runs these tests automatically for each push and pull request.

The project purposely avoids external data sources or advanced numerical solvers in order to remain lightweight. Nonetheless, it provides a foundation for exploring economic dynamics, experimenting with fiscal policy, or teaching the mechanics of the Keynesian cross. Because the model is coded in simple Python modules, you can easily modify or extend it—perhaps by adding an external sector, introducing expectations, or connecting it with econometric data.

## Contributing

Contributions are welcome. Please open an issue or pull request if you spot a bug or would like to discuss an enhancement. All changes should include appropriate tests so that the continuous integration workflow remains green.

## License

This project is released under the MIT License, allowing broad reuse as long as the license terms are preserved.
