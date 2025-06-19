import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.optimize import minimize_scalar
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

class OptionsCalculator:
    """Calculadora de opciones usando el modelo Black-Scholes"""
    
    @staticmethod
    def black_scholes_call(S: float, K: float, T: float, r: float, sigma: float) -> float:
        """
        Calcula el precio de una opción call usando Black-Scholes
        
        Args:
            S: Precio actual del activo subyacente
            K: Precio de ejercicio
            T: Tiempo hasta expiración (en años)
            r: Tasa libre de riesgo
            sigma: Volatilidad implícita
        """
        if T <= 0:
            return max(S - K, 0)
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        return max(call_price, 0)
    
    @staticmethod
    def black_scholes_put(S: float, K: float, T: float, r: float, sigma: float) -> float:
        """
        Calcula el precio de una opción put usando Black-Scholes
        """
        if T <= 0:
            return max(K - S, 0)
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return max(put_price, 0)
    
    @staticmethod
    def calculate_greeks(S: float, K: float, T: float, r: float, sigma: float, option_type: str = 'call') -> Dict[str, float]:
        """
        Calcula todas las Greeks para una opción
        """
        if T <= 0:
            return {'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0, 'rho': 0}
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if option_type.lower() == 'call':
            # Greeks para Call
            delta = norm.cdf(d1)
            rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
            theta = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - 
                    r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
        else:
            # Greeks para Put
            delta = norm.cdf(d1) - 1
            rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100
            theta = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) + 
                    r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
        
        # Gamma y Vega son iguales para calls y puts
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * norm.pdf(d1) * np.sqrt(T) / 100
        
        return {
            'delta': delta,
            'gamma': gamma,
            'theta': theta,
            'vega': vega,
            'rho': rho
        }
    
    @staticmethod
    def implied_volatility(market_price: float, S: float, K: float, T: float, r: float, option_type: str = 'call') -> float:
        """
        Calcula la volatilidad implícita usando método de bisección
        """
        if T <= 0:
            return 0
        
        def objective(sigma):
            if option_type.lower() == 'call':
                theoretical_price = OptionsCalculator.black_scholes_call(S, K, T, r, sigma)
            else:
                theoretical_price = OptionsCalculator.black_scholes_put(S, K, T, r, sigma)
            return abs(theoretical_price - market_price)
        
        try:
            result = minimize_scalar(objective, bounds=(0.001, 5.0), method='bounded')
            return result.x if result.success else 0.3
        except:
            return 0.3
    
    @staticmethod
    def time_to_expiration(expiration_date: str) -> float:
        """
        Calcula el tiempo hasta expiración en años
        """
        try:
            exp_date = datetime.strptime(expiration_date, '%Y-%m-%d')
            today = datetime.now()
            days_to_exp = (exp_date - today).days
            return max(days_to_exp / 365.25, 0)
        except:
            return 0
    
    @staticmethod
    def probability_analysis(S: float, K: float, T: float, r: float, sigma: float) -> Dict[str, float]:
        """
        Calcula probabilidades relacionadas con las opciones
        """
        if T <= 0:
            return {'prob_itm_call': 1 if S > K else 0, 'prob_itm_put': 1 if S < K else 0, 'prob_touch': 0}
        
        d2 = (np.log(S / K) + (r - 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        
        # Probabilidad de que una call termine ITM
        prob_itm_call = norm.cdf(d2)
        
        # Probabilidad de que una put termine ITM  
        prob_itm_put = norm.cdf(-d2)
          # Probabilidad de tocar el strike (aproximación)
        prob_touch = 2 * norm.cdf(-abs(np.log(S/K))/(sigma * np.sqrt(T)))
        
        return {
            'prob_itm_call': prob_itm_call,
            'prob_itm_put': prob_itm_put,
            'prob_touch': min(prob_touch, 1.0)
        }
    
    @staticmethod
    def analyze_option_chain(options_data: pd.DataFrame, S: float, r: float, expiration_date: str) -> pd.DataFrame:
        """
        Analiza una cadena de opciones completa
        """
        if options_data.empty:
            return pd.DataFrame()
        
        T = OptionsCalculator.time_to_expiration(expiration_date)
        if T <= 0:
            return options_data
        
        results = []
        
        for _, option in options_data.iterrows():
            try:
                K = option.get('strike', 0)
                if K <= 0:
                    continue
                    
                market_price = option.get('lastPrice', option.get('bid', 0))
                bid = option.get('bid', 0)
                ask = option.get('ask', 0)
                volume = option.get('volume', 0)
                open_interest = option.get('openInterest', 0)
                  # Determinar tipo de opción desde contractSymbol o inferir
                contract_symbol = option.get('contractSymbol', '')
                if contract_symbol:
                    # Buscar indicadores de tipo en el símbolo
                    symbol_upper = contract_symbol.upper()
                    if 'C' in symbol_upper[-2:] or 'CALL' in symbol_upper:
                        option_type = 'call'
                    elif 'P' in symbol_upper[-2:] or 'PUT' in symbol_upper:
                        option_type = 'put'
                    else:
                        # Si no se puede determinar, usar call por defecto
                        option_type = 'call'
                else:
                    # Si no hay símbolo, usar call por defecto
                    option_type = 'call'
                
                if market_price > 0:
                    # Calcular volatilidad implícita
                    iv = OptionsCalculator.implied_volatility(market_price, S, K, T, r, option_type)
                    
                    # Calcular precio teórico
                    if option_type == 'call':
                        theoretical_price = OptionsCalculator.black_scholes_call(S, K, T, r, iv)
                    else:
                        theoretical_price = OptionsCalculator.black_scholes_put(S, K, T, r, iv)
                    
                    # Calcular Greeks
                    greeks = OptionsCalculator.calculate_greeks(S, K, T, r, iv, option_type)
                    
                    # Calcular probabilidades
                    probs = OptionsCalculator.probability_analysis(S, K, T, r, iv)
                    
                    # Análisis de valor
                    spread = ask - bid if ask > bid else 0
                    midpoint = (bid + ask) / 2 if ask > bid else market_price
                    
                    results.append({
                        'contractSymbol': contract_symbol,
                        'strike': K,
                        'lastPrice': market_price,
                        'bid': bid,
                        'ask': ask,
                        'spread': spread,
                        'midpoint': midpoint,
                        'volume': volume,
                        'openInterest': open_interest,
                        'impliedVolatility': iv,
                        'theoreticalPrice': theoretical_price,
                        'intrinsicValue': max(S - K, 0) if option_type == 'call' else max(K - S, 0),
                        'timeValue': market_price - max(0, (S - K) if option_type == 'call' else (K - S)),
                        'delta': greeks['delta'],
                        'gamma': greeks['gamma'],
                        'theta': greeks['theta'],
                        'vega': greeks['vega'],
                        'rho': greeks['rho'],
                        'probITM': probs['prob_itm_call'] if option_type == 'call' else probs['prob_itm_put'],
                        'moneyness': S / K,
                        'optionType': option_type
                    })
            
            except Exception as e:
                # Log del error pero continuar con las otras opciones
                print(f"Error analizando opción {option.get('contractSymbol', 'Unknown')}: {e}")
                continue
        
        return pd.DataFrame(results)
    
    @staticmethod
    def calculate_portfolio_greeks(positions: List[Dict]) -> Dict[str, float]:
        """
        Calcula las Greeks de un portafolio de opciones
        """
        total_greeks = {'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0, 'rho': 0}
        
        for position in positions:
            quantity = position.get('quantity', 0)
            greeks = position.get('greeks', {})
            
            for greek in total_greeks:
                total_greeks[greek] += quantity * greeks.get(greek, 0)
        
        return total_greeks
