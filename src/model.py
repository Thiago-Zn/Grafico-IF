"""DD-AA Economic Model Implementation."""
import numpy as np
from dataclasses import dataclass
from typing import Dict, Tuple, List


@dataclass
class DDAAParameters:
    """Parameters for DD-AA model."""
    # Goods market parameters
    consumption_sensitivity: float = 0.7  # MPC
    investment_sensitivity: float = 15.0  # Interest rate sensitivity
    export_sensitivity: float = 0.5       # Exchange rate sensitivity
    
    # Money market parameters
    money_demand_income: float = 0.02     # Income sensitivity of money demand
    money_demand_interest: float = 30.0   # Interest sensitivity
    
    # Asset market parameters
    uip_sensitivity: float = 0.08         # UIP condition sensitivity
    expected_depreciation: float = 0.0    # Expected exchange rate change
    
    # Policy parameters
    money_supply: float = 100.0           # Base money supply
    government_spending: float = 20.0     # Government expenditure
    
    # Initial equilibrium
    initial_output: float = 100.0
    initial_interest: float = 2.0
    initial_exchange: float = 1.5


class DDAAModel:
    """DD-AA model for open economy analysis."""
    
    def __init__(self, params: DDAAParameters):
        self.params = params
        self.history = []
    
    def dd_curve(self, Y_range: np.ndarray, shift: float = 0.0) -> np.ndarray:
        """
        Calculate DD curve (goods market equilibrium).
        E = f(Y) where goods market clears
        """
        # Base DD relationship: higher Y requires lower E for equilibrium
        # (due to import leakage)
        E = 2.0 - 0.005 * Y_range + shift
        return E
    
    def aa_curve(self, Y_range: np.ndarray, shift: float = 0.0) -> np.ndarray:
        """
        Calculate AA curve (asset market equilibrium).
        E = g(Y) where money and forex markets clear
        """
        # Base AA relationship: higher Y → higher money demand → higher i → lower E
        # But also: higher Y → higher imports → depreciation pressure
        # Net effect depends on parameters
        E = 0.8 + 0.008 * Y_range + shift
        return E
    
    def find_equilibrium(self, dd_shift: float = 0.0, aa_shift: float = 0.0) -> Tuple[float, float]:
        """
        Find intersection of DD and AA curves.
        Returns: (Y_equilibrium, E_equilibrium)
        """
        # Solve DD = AA
        # 2.0 - 0.005*Y + dd_shift = 0.8 + 0.008*Y + aa_shift
        # 1.2 + dd_shift - aa_shift = 0.013*Y
        Y_eq = (1.2 + dd_shift - aa_shift) / 0.013
        E_eq = self.dd_curve(np.array([Y_eq]), dd_shift)[0]
        
        return Y_eq, E_eq
    
    def money_market_equilibrium(self, Y: float, M_supply: float) -> float:
        """
        Calculate equilibrium interest rate in money market.
        L(i, Y) = M^S/P
        """
        # Money demand: L = kY - hi
        # Solving for i: i = (kY - M^S/P) / h
        k = self.params.money_demand_income
        h = self.params.money_demand_interest
        
        i_eq = max(0.1, (k * Y - M_supply / 100) / h + 1.2)  # Add base rate
        return i_eq
    
    def simulate_shock(self, shock_type: str, magnitude: float, 
                      periods: int = 6) -> Dict[str, List[float]]:
        """
        Simulate economic shock and adjustment path.
        
        shock_type: 'monetary', 'fiscal', 'real'
        magnitude: size of shock (positive = expansionary)
        periods: number of time periods to simulate
        """
        results = {
            'Y': [self.params.initial_output],
            'E': [self.params.initial_exchange],
            'i': [self.params.initial_interest],
            'dd_shift': [0.0],
            'aa_shift': [0.0]
        }
        
        for t in range(1, periods):
            if shock_type == 'monetary':
                if t == 1:
                    # Money supply increase
                    results['i'].append(results['i'][-1] - magnitude)
                    results['aa_shift'].append(magnitude * 0.1)  # AA shifts right
                    results['dd_shift'].append(0)
                elif t == 2:
                    # Exchange rate adjustment
                    results['i'].append(results['i'][-1])
                    results['aa_shift'].append(results['aa_shift'][-1])
                    results['dd_shift'].append(magnitude * 0.05)  # DD shifts right
                elif t >= 3:
                    # Long-run price adjustment
                    results['i'].append(self.params.initial_interest)
                    results['aa_shift'].append(results['aa_shift'][-1] * 0.8)
                    results['dd_shift'].append(results['dd_shift'][-1])
                    
            elif shock_type == 'fiscal':
                if t == 1:
                    # Government spending increase
                    results['dd_shift'].append(magnitude * 0.1)  # DD shifts right
                    results['aa_shift'].append(0)
                    results['i'].append(results['i'][-1] + magnitude * 0.5)
                elif t >= 2:
                    # Crowding out effects
                    results['dd_shift'].append(results['dd_shift'][-1])
                    results['aa_shift'].append(-magnitude * 0.05 * t)  # AA shifts left
                    results['i'].append(results['i'][-1])
                    
            elif shock_type == 'real':
                if t == 1:
                    # Productivity shock
                    results['i'].append(results['i'][-1] - magnitude * 0.3)
                    results['dd_shift'].append(magnitude * 0.1)
                    results['aa_shift'].append(magnitude * 0.05)
                else:
                    # Sustained at new level
                    results['i'].append(results['i'][-1])
                    results['dd_shift'].append(results['dd_shift'][-1])
                    results['aa_shift'].append(results['aa_shift'][-1])
            
            # Calculate new equilibrium
            Y_eq, E_eq = self.find_equilibrium(
                results['dd_shift'][-1], 
                results['aa_shift'][-1]
            )
            results['Y'].append(Y_eq)
            results['E'].append(E_eq)
        
        return results
    
    def get_curve_data(self, dd_shift: float = 0.0, aa_shift: float = 0.0) -> Dict:
        """Get data for plotting DD and AA curves."""
        Y_range = np.linspace(50, 150, 100)
        
        return {
            'Y_range': Y_range,
            'DD_curve': self.dd_curve(Y_range, dd_shift),
            'AA_curve': self.aa_curve(Y_range, aa_shift),
            'DD_base': self.dd_curve(Y_range, 0),
            'AA_base': self.aa_curve(Y_range, 0)
        }