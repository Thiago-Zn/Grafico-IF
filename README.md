# DD–AA Simulator

The **DD–AA simulator** is an interactive tool built with [Streamlit](https://streamlit.io/) that demonstrates a simple dynamic model. Adjust the parameters in the sidebar to explore how the Demand (DD) and Autonomous Adjustment (AA) components interact over time.

## Setup

1. Install the required Python packages:

```bash
pip install -r requirements.txt
```

2. Launch the application:

```bash
streamlit run app.py
```

The simulator opens in your browser and updates automatically as you change the parameters.

## Interface

The main page shows a chart of the model’s behavior. The sidebar contains several controls:

- **Demand rate** – growth factor for DD.
- **Adjustment rate** – system response coefficient (AA).
- **Initial values** – starting DD and AA levels.
- **Simulation steps** – number of iterations to compute.

Changing these fields immediately refreshes the visualizations so you can see how the model evolves.

## Example Scenarios

- **Stable market**: Choose a small demand rate with a moderate adjustment rate. The system quickly converges to equilibrium.
- **Volatile behavior**: Increase demand while lowering adjustment to observe oscillations around the target.
- **Rapid stabilization**: Set a large adjustment rate with minor initial imbalances to reach equilibrium in only a few steps.

Experiment with different combinations to understand the system’s dynamics.

## License

This project is available under the [MIT License](LICENSE).
