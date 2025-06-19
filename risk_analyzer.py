import numpy as np
import pandas as pd
from scipy.stats import norm
from typing import Dict, List, Tuple, Optional
from options_calculator import OptionsCalculator

class RiskAnalyzer:
    """Analizador de riesgo para opciones y portafolios"""
    
    def __init__(self):
        self.calculator = OptionsCalculator()
    
    def calculate_var(self, returns: np.array, confidence_level: float = 0.05) -> float:
        """
        Calcula Value at Risk (VaR) histórico
        """
        if len(returns) == 0:
            return 0
        
        return np.percentile(returns, confidence_level * 100)
    
    def calculate_cvar(self, returns: np.array, confidence_level: float = 0.05) -> float:
        """
        Calcula Conditional Value at Risk (CVaR)
        """
        var = self.calculate_var(returns, confidence_level)
        return returns[returns <= var].mean()
    
    def monte_carlo_simulation(self, S0: float, r: float, sigma: float, T: float, 
                             num_simulations: int = 10000, num_steps: int = 252) -> np.array:
        """
        Simulación Monte Carlo para precios futuros
        """
        dt = T / num_steps
        paths = np.zeros((num_simulations, num_steps + 1))
        paths[:, 0] = S0
        
        for t in range(1, num_steps + 1):
            Z = np.random.standard_normal(num_simulations)
            paths[:, t] = paths[:, t-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
        
        return paths
    
    def analyze_strategy_risk(self, strategy_data: Dict, S0: float, r: float, sigma: float, T: float,
                            num_simulations: int = 1000) -> Dict:
        """
        Analiza el riesgo de una estrategia usando simulaciones Monte Carlo
        """
        # Generar simulaciones de precios
        price_paths = self.monte_carlo_simulation(S0, r, sigma, T, num_simulations)
        final_prices = price_paths[:, -1]
        
        # Calcular P&L para cada precio simulado
        payoffs = []
        components = strategy_data.get('components', [])
        
        for price in final_prices:
            total_pnl = 0
            
            for component in components:
                if component['type'] == 'stock':
                    pnl = component['quantity'] * (price - component['price'])
                elif component['type'] in ['call', 'put']:
                    strike = component['strike']
                    if component['type'] == 'call':
                        intrinsic = max(price - strike, 0)
                    else:
                        intrinsic = max(strike - price, 0)
                    
                    cost = component['price']
                    pnl = component['quantity'] * (intrinsic - cost)
                
                total_pnl += pnl
            
            payoffs.append(total_pnl)
        
        payoffs = np.array(payoffs)
        
        # Calcular métricas de riesgo
        var_95 = self.calculate_var(payoffs, 0.05)
        var_99 = self.calculate_var(payoffs, 0.01)
        cvar_95 = self.calculate_cvar(payoffs, 0.05)
        expected_return = np.mean(payoffs)
        volatility = np.std(payoffs)
        sharpe_ratio = expected_return / volatility if volatility > 0 else 0
        
        # Probabilidades
        prob_profit = np.sum(payoffs > 0) / len(payoffs)
        prob_loss = np.sum(payoffs < 0) / len(payoffs)
        prob_breakeven = np.sum(payoffs == 0) / len(payoffs)
        
        # Percentiles
        percentiles = {
            '5%': np.percentile(payoffs, 5),
            '25%': np.percentile(payoffs, 25),
            '50%': np.percentile(payoffs, 50),
            '75%': np.percentile(payoffs, 75),
            '95%': np.percentile(payoffs, 95)
        }
        
        return {
            'expected_return': expected_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'var_95': var_95,
            'var_99': var_99,
            'cvar_95': cvar_95,
            'prob_profit': prob_profit,
            'prob_loss': prob_loss,
            'prob_breakeven': prob_breakeven,
            'percentiles': percentiles,
            'simulated_payoffs': payoffs,
            'final_prices': final_prices
        }
    
    def portfolio_risk_metrics(self, positions: List[Dict], market_data: Dict) -> Dict:
        """
        Calcula métricas de riesgo para un portafolio de opciones
        """
        total_delta = 0
        total_gamma = 0
        total_theta = 0
        total_vega = 0
        total_rho = 0
        total_value = 0
        
        S = market_data['current_price']
        r = market_data['risk_free_rate']
        
        for position in positions:
            quantity = position.get('quantity', 0)
            
            if position.get('type') == 'stock':
                total_delta += quantity
                total_value += quantity * S
            
            elif position.get('type') in ['call', 'put']:
                strike = position['strike']
                expiration = position.get('expiration', '2024-12-31')
                sigma = position.get('implied_vol', market_data.get('historical_volatility', 0.3))
                
                T = self.calculator.time_to_expiration(expiration)
                
                if T > 0:
                    greeks = self.calculator.calculate_greeks(S, strike, T, r, sigma, position['type'])
                    
                    total_delta += quantity * greeks['delta']
                    total_gamma += quantity * greeks['gamma']
                    total_theta += quantity * greeks['theta']
                    total_vega += quantity * greeks['vega']
                    total_rho += quantity * greeks['rho']
                    
                    if position['type'] == 'call':
                        option_value = self.calculator.black_scholes_call(S, strike, T, r, sigma)
                    else:
                        option_value = self.calculator.black_scholes_put(S, strike, T, r, sigma)
                    
                    total_value += quantity * option_value
        
        # Delta hedging requirements
        delta_hedge_shares = -total_delta
        delta_hedge_cost = delta_hedge_shares * S
        
        # Gamma risk (curvature risk)
        gamma_risk = 0.5 * total_gamma * (0.01 * S)**2  # 1% move
        
        # Theta decay (daily)
        daily_theta = total_theta
        
        # Vega risk (1% vol change)
        vega_risk = total_vega * 0.01
        
        return {
            'portfolio_value': total_value,
            'net_delta': total_delta,
            'net_gamma': total_gamma,
            'net_theta': total_theta,
            'net_vega': total_vega,
            'net_rho': total_rho,
            'delta_hedge_shares': delta_hedge_shares,
            'delta_hedge_cost': delta_hedge_cost,
            'gamma_risk_1pct': gamma_risk,
            'daily_theta_decay': daily_theta,
            'vega_risk_1pct': vega_risk,
            'delta_neutral': abs(total_delta) < 0.1,
            'gamma_neutral': abs(total_gamma) < 0.01
        }
    
    def stress_test(self, strategy_data: Dict, S0: float, scenarios: List[Dict]) -> Dict:
        """
        Realiza pruebas de estrés en diferentes escenarios
        """
        results = {}
        
        for scenario in scenarios:
            name = scenario['name']
            price_change = scenario.get('price_change', 0)  # % change
            vol_change = scenario.get('vol_change', 0)      # % change
            time_decay = scenario.get('time_decay', 0)      # days
            
            # Calcular nuevo precio y parámetros
            new_price = S0 * (1 + price_change)
            
            # Simular P&L bajo este escenario
            total_pnl = 0
            components = strategy_data.get('components', [])
            
            for component in components:
                if component['type'] == 'stock':
                    pnl = component['quantity'] * (new_price - component['price'])
                
                elif component['type'] in ['call', 'put']:
                    # Simplificación: usar valor intrínseco
                    strike = component['strike']
                    if component['type'] == 'call':
                        intrinsic = max(new_price - strike, 0)
                    else:
                        intrinsic = max(strike - new_price, 0)
                    
                    cost = component['price']
                    pnl = component['quantity'] * (intrinsic - cost)
                
                total_pnl += pnl
            
            results[name] = {
                'scenario_price': new_price,
                'total_pnl': total_pnl,
                'return_pct': (total_pnl / abs(strategy_data.get('net_cost', 1))) * 100
            }
        
        return results
    
    def correlation_analysis(self, asset_returns: pd.DataFrame) -> Dict:
        """
        Analiza correlaciones entre activos
        """
        correlation_matrix = asset_returns.corr()
        
        # Eigenvalues para análisis de componentes principales
        eigenvalues, eigenvectors = np.linalg.eig(correlation_matrix)
        
        # Diversification ratio
        weights = np.ones(len(asset_returns.columns)) / len(asset_returns.columns)
        portfolio_vol = np.sqrt(weights.T @ correlation_matrix @ weights)
        avg_vol = np.mean([asset_returns[col].std() for col in asset_returns.columns])
        diversification_ratio = avg_vol / portfolio_vol
        
        return {
            'correlation_matrix': correlation_matrix,
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors,
            'diversification_ratio': diversification_ratio,
            'max_correlation': correlation_matrix.max().max(),
            'min_correlation': correlation_matrix.min().min()
        }
    
    def liquidity_risk_assessment(self, options_data: pd.DataFrame) -> Dict:
        """
        Evalúa el riesgo de liquidez de las opciones
        """
        if options_data.empty:
            return {}
        
        # Métricas de liquidez
        avg_volume = options_data['volume'].mean()
        avg_open_interest = options_data['openInterest'].mean()
        avg_spread = options_data['spread'].mean() if 'spread' in options_data.columns else 0
        
        # Ratio bid-ask como % del precio medio
        if 'midpoint' in options_data.columns and 'spread' in options_data.columns:
            spread_pct = (options_data['spread'] / options_data['midpoint'] * 100).mean()
        else:
            spread_pct = 0
        
        # Clasificación de liquidez
        def classify_liquidity(volume, open_interest, spread_pct):
            if volume > 100 and open_interest > 500 and spread_pct < 5:
                return 'Alta'
            elif volume > 10 and open_interest > 100 and spread_pct < 10:
                return 'Media'
            else:
                return 'Baja'
        
        options_data['liquidity_score'] = options_data.apply(
            lambda row: classify_liquidity(
                row.get('volume', 0), 
                row.get('openInterest', 0), 
                spread_pct
            ), axis=1
        )
        
        liquidity_distribution = options_data['liquidity_score'].value_counts()
        
        return {
            'avg_volume': avg_volume,
            'avg_open_interest': avg_open_interest,
            'avg_spread_pct': spread_pct,
            'liquidity_distribution': liquidity_distribution.to_dict(),
            'high_liquidity_pct': liquidity_distribution.get('Alta', 0) / len(options_data) * 100
        }
    
    def generate_risk_report(self, strategy_data: Dict, market_data: Dict, 
                           monte_carlo_results: Dict = None) -> Dict:
        """
        Genera un reporte completo de riesgo
        """
        report = {
            'strategy_name': strategy_data.get('strategy', 'Unknown'),
            'timestamp': pd.Timestamp.now(),
            'market_conditions': {
                'current_price': market_data.get('current_price'),
                'historical_vol': market_data.get('historical_volatility'),
                'risk_free_rate': market_data.get('risk_free_rate')
            }
        }
        
        # Métricas básicas de la estrategia
        report['basic_metrics'] = {
            'max_profit': strategy_data.get('max_profit'),
            'max_loss': strategy_data.get('max_loss'),
            'breakeven': strategy_data.get('breakeven'),
            'net_cost': strategy_data.get('net_cost', strategy_data.get('net_credit', 0))
        }
        
        # Resultados de Monte Carlo si están disponibles
        if monte_carlo_results:
            report['risk_metrics'] = {
                'expected_return': monte_carlo_results['expected_return'],
                'volatility': monte_carlo_results['volatility'],
                'var_95': monte_carlo_results['var_95'],
                'cvar_95': monte_carlo_results['cvar_95'],
                'prob_profit': monte_carlo_results['prob_profit']
            }
        
        # Escenarios de estrés predefinidos
        stress_scenarios = [
            {'name': 'Mercado Bajista', 'price_change': -0.2, 'vol_change': 0.5},
            {'name': 'Mercado Alcista', 'price_change': 0.2, 'vol_change': -0.2},
            {'name': 'Alta Volatilidad', 'price_change': 0, 'vol_change': 1.0},
            {'name': 'Crash', 'price_change': -0.4, 'vol_change': 2.0}
        ]
        
        report['stress_tests'] = self.stress_test(strategy_data, market_data['current_price'], stress_scenarios)
        
        return report
