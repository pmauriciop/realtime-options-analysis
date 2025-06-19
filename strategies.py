import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from options_calculator import OptionsCalculator
from datetime import datetime, timedelta

class OptionsStrategies:
    """Implementación de estrategias de opciones financieras"""
    
    def __init__(self):
        self.calculator = OptionsCalculator()
    
    def covered_call(self, S: float, K: float, T: float, r: float, sigma: float, 
                    shares_owned: int = 100) -> Dict:
        """
        Estrategia Covered Call: Poseer acciones + vender call
        """
        call_price = self.calculator.black_scholes_call(S, K, T, r, sigma)
        
        # Posición larga en acciones + posición corta en call
        stock_value = shares_owned * S
        call_premium = shares_owned * call_price
        
        # Cálculo de P&L en diferentes precios
        prices = np.linspace(S * 0.7, S * 1.3, 50)
        payoffs = []
        
        for price in prices:
            stock_pnl = shares_owned * (price - S)
            call_pnl = call_premium - shares_owned * max(price - K, 0)
            total_pnl = stock_pnl + call_pnl
            payoffs.append(total_pnl)
        
        max_profit = call_premium + shares_owned * max(K - S, 0)
        max_loss = -stock_value + call_premium  # Pérdida teórica ilimitada
        breakeven = S - call_price
        
        return {
            'strategy': 'Covered Call',
            'description': f'Poseer {shares_owned} acciones y vender {shares_owned//100} calls',
            'premium_received': call_premium,
            'max_profit': max_profit,
            'max_loss': max_loss,
            'breakeven': breakeven,
            'prices': prices.tolist(),
            'payoffs': payoffs,
            'probability_profit': self.calculator.probability_analysis(S, breakeven, T, r, sigma)['prob_itm_put'],
            'components': [
                {'type': 'stock', 'quantity': shares_owned, 'price': S},
                {'type': 'call', 'quantity': -shares_owned//100, 'strike': K, 'price': call_price}
            ]
        }
    
    def protective_put(self, S: float, K: float, T: float, r: float, sigma: float,
                      shares_owned: int = 100) -> Dict:
        """
        Estrategia Protective Put: Poseer acciones + comprar put
        """
        put_price = self.calculator.black_scholes_put(S, K, T, r, sigma)
        
        stock_value = shares_owned * S
        put_cost = shares_owned * put_price
        
        # Cálculo de P&L
        prices = np.linspace(S * 0.5, S * 1.5, 50)
        payoffs = []
        
        for price in prices:
            stock_pnl = shares_owned * (price - S)
            put_pnl = shares_owned * max(K - price, 0) - put_cost
            total_pnl = stock_pnl + put_pnl
            payoffs.append(total_pnl)
        
        max_profit = float('inf')  # Ilimitado
        max_loss = put_cost + shares_owned * (S - K) if S > K else put_cost
        breakeven = S + put_price
        
        return {
            'strategy': 'Protective Put',
            'description': f'Poseer {shares_owned} acciones y comprar {shares_owned//100} puts',
            'premium_paid': put_cost,
            'max_profit': max_profit,
            'max_loss': max_loss,
            'breakeven': breakeven,
            'prices': prices.tolist(),
            'payoffs': payoffs,
            'probability_profit': self.calculator.probability_analysis(S, breakeven, T, r, sigma)['prob_itm_call'],
            'components': [
                {'type': 'stock', 'quantity': shares_owned, 'price': S},
                {'type': 'put', 'quantity': shares_owned//100, 'strike': K, 'price': put_price}
            ]
        }
    
    def long_straddle(self, S: float, K: float, T: float, r: float, sigma: float) -> Dict:
        """
        Estrategia Long Straddle: Comprar call y put con mismo strike
        """
        call_price = self.calculator.black_scholes_call(S, K, T, r, sigma)
        put_price = self.calculator.black_scholes_put(S, K, T, r, sigma)
        
        total_premium = call_price + put_price
        
        # Cálculo de P&L
        prices = np.linspace(S * 0.6, S * 1.4, 50)
        payoffs = []
        
        for price in prices:
            call_pnl = max(price - K, 0) - call_price
            put_pnl = max(K - price, 0) - put_price
            total_pnl = call_pnl + put_pnl
            payoffs.append(total_pnl)
        
        max_profit = float('inf')  # Teóricamente ilimitado
        max_loss = -total_premium
        breakeven_up = K + total_premium
        breakeven_down = K - total_premium
        
        return {
            'strategy': 'Long Straddle',
            'description': f'Comprar call y put strike {K}',
            'premium_paid': total_premium,
            'max_profit': max_profit,
            'max_loss': max_loss,
            'breakeven_up': breakeven_up,
            'breakeven_down': breakeven_down,
            'prices': prices.tolist(),
            'payoffs': payoffs,
            'probability_profit': 1 - self.calculator.probability_analysis(S, K, T, r, sigma)['prob_touch'],
            'components': [
                {'type': 'call', 'quantity': 1, 'strike': K, 'price': call_price},
                {'type': 'put', 'quantity': 1, 'strike': K, 'price': put_price}
            ]
        }
    
    def iron_condor(self, S: float, K1: float, K2: float, K3: float, K4: float, 
                   T: float, r: float, sigma: float) -> Dict:
        """
        Estrategia Iron Condor: K1 < K2 < K3 < K4
        Vender call spread (K3-K4) + vender put spread (K1-K2)
        """
        # Calcular precios de las opciones
        put_K1 = self.calculator.black_scholes_put(S, K1, T, r, sigma)
        put_K2 = self.calculator.black_scholes_put(S, K2, T, r, sigma)
        call_K3 = self.calculator.black_scholes_call(S, K3, T, r, sigma)
        call_K4 = self.calculator.black_scholes_call(S, K4, T, r, sigma)
        
        # Crédito neto recibido
        net_credit = (put_K2 - put_K1) + (call_K3 - call_K4)
        
        # Cálculo de P&L
        prices = np.linspace(K1 * 0.9, K4 * 1.1, 100)
        payoffs = []
        
        for price in prices:
            # Put spread: Largo K1, Corto K2
            put_spread_pnl = max(K1 - price, 0) - max(K2 - price, 0)
            # Call spread: Corto K3, Largo K4  
            call_spread_pnl = max(price - K3, 0) - max(price - K4, 0)
            
            total_pnl = put_spread_pnl - call_spread_pnl + net_credit
            payoffs.append(total_pnl)
        
        max_profit = net_credit
        max_loss = min(K2 - K1, K4 - K3) - net_credit
        breakeven_down = K2 - net_credit
        breakeven_up = K3 + net_credit
        
        return {
            'strategy': 'Iron Condor',
            'description': f'Vender put spread {K1}-{K2} y call spread {K3}-{K4}',
            'net_credit': net_credit,
            'max_profit': max_profit,
            'max_loss': max_loss,
            'breakeven_down': breakeven_down,
            'breakeven_up': breakeven_up,
            'prices': prices.tolist(),
            'payoffs': payoffs,
            'probability_profit': (norm.cdf((np.log(breakeven_up/S))/(sigma*np.sqrt(T))) - 
                                 norm.cdf((np.log(breakeven_down/S))/(sigma*np.sqrt(T)))),
            'components': [
                {'type': 'put', 'quantity': 1, 'strike': K1, 'price': put_K1},
                {'type': 'put', 'quantity': -1, 'strike': K2, 'price': put_K2},
                {'type': 'call', 'quantity': -1, 'strike': K3, 'price': call_K3},
                {'type': 'call', 'quantity': 1, 'strike': K4, 'price': call_K4}
            ]
        }
    
    def butterfly_spread(self, S: float, K1: float, K2: float, K3: float, 
                        T: float, r: float, sigma: float, option_type: str = 'call') -> Dict:
        """
        Estrategia Butterfly Spread: K1 < K2 < K3, donde K2 = (K1 + K3) / 2
        """
        if option_type.lower() == 'call':
            price_K1 = self.calculator.black_scholes_call(S, K1, T, r, sigma)
            price_K2 = self.calculator.black_scholes_call(S, K2, T, r, sigma)
            price_K3 = self.calculator.black_scholes_call(S, K3, T, r, sigma)
        else:
            price_K1 = self.calculator.black_scholes_put(S, K1, T, r, sigma)
            price_K2 = self.calculator.black_scholes_put(S, K2, T, r, sigma)
            price_K3 = self.calculator.black_scholes_put(S, K3, T, r, sigma)
        
        # Costo neto (comprar 1 K1, vender 2 K2, comprar 1 K3)
        net_cost = price_K1 - 2 * price_K2 + price_K3
        
        # Cálculo de P&L
        prices = np.linspace(K1 * 0.9, K3 * 1.1, 100)
        payoffs = []
        
        for price in prices:
            if option_type.lower() == 'call':
                pnl = (max(price - K1, 0) - 2 * max(price - K2, 0) + 
                      max(price - K3, 0) - net_cost)
            else:
                pnl = (max(K1 - price, 0) - 2 * max(K2 - price, 0) + 
                      max(K3 - price, 0) - net_cost)
            payoffs.append(pnl)
        
        max_profit = (K2 - K1) - net_cost
        max_loss = -net_cost
        breakeven_down = K1 + net_cost
        breakeven_up = K3 - net_cost
        
        return {
            'strategy': f'{option_type.title()} Butterfly Spread',
            'description': f'Comprar {option_type} {K1}, vender 2 {option_type}s {K2}, comprar {option_type} {K3}',
            'net_cost': net_cost,
            'max_profit': max_profit,
            'max_loss': max_loss,
            'breakeven_down': breakeven_down,
            'breakeven_up': breakeven_up,
            'prices': prices.tolist(),
            'payoffs': payoffs,
            'probability_profit': 0.5,  # Simplificación
            'components': [
                {'type': option_type, 'quantity': 1, 'strike': K1, 'price': price_K1},
                {'type': option_type, 'quantity': -2, 'strike': K2, 'price': price_K2},
                {'type': option_type, 'quantity': 1, 'strike': K3, 'price': price_K3}
            ]
        }
    
    def collar(self, S: float, put_strike: float, call_strike: float, T: float, r: float, sigma: float,
              shares_owned: int = 100) -> Dict:
        """
        Estrategia Collar: Poseer acciones + comprar put + vender call
        """
        put_price = self.calculator.black_scholes_put(S, put_strike, T, r, sigma)
        call_price = self.calculator.black_scholes_call(S, call_strike, T, r, sigma)
        
        net_cost = put_price - call_price
        
        # Cálculo de P&L
        prices = np.linspace(S * 0.6, S * 1.4, 50)
        payoffs = []
        
        for price in prices:
            stock_pnl = shares_owned * (price - S)
            put_pnl = shares_owned * max(put_strike - price, 0) - shares_owned * put_price
            call_pnl = shares_owned * call_price - shares_owned * max(price - call_strike, 0)
            total_pnl = stock_pnl + put_pnl + call_pnl
            payoffs.append(total_pnl)
        
        max_profit = shares_owned * (call_strike - S) + shares_owned * (call_price - put_price)
        max_loss = shares_owned * (put_strike - S) + shares_owned * (call_price - put_price)
        
        return {
            'strategy': 'Collar',
            'description': f'Poseer {shares_owned} acciones, comprar put {put_strike}, vender call {call_strike}',
            'net_cost': net_cost * shares_owned,
            'max_profit': max_profit,
            'max_loss': max_loss,
            'prices': prices.tolist(),
            'payoffs': payoffs,
            'probability_profit': 0.5,  # Simplificación
            'components': [
                {'type': 'stock', 'quantity': shares_owned, 'price': S},
                {'type': 'put', 'quantity': shares_owned//100, 'strike': put_strike, 'price': put_price},
                {'type': 'call', 'quantity': -shares_owned//100, 'strike': call_strike, 'price': call_price}
            ]
        }
    
    def analyze_all_strategies(self, S: float, T: float, r: float, sigma: float, 
                             strikes: List[float] = None) -> Dict:
        """
        Analiza múltiples estrategias y devuelve un resumen
        """
        if strikes is None:
            strikes = [S * 0.95, S, S * 1.05]
        
        strategies = {}
        
        # Single leg strategies
        for strike in strikes:
            strategies[f'covered_call_{strike}'] = self.covered_call(S, strike, T, r, sigma)
            strategies[f'protective_put_{strike}'] = self.protective_put(S, strike, T, r, sigma)
        
        # Multi-leg strategies
        if len(strikes) >= 3:
            strategies['long_straddle'] = self.long_straddle(S, strikes[1], T, r, sigma)
            strategies['butterfly_call'] = self.butterfly_spread(S, strikes[0], strikes[1], strikes[2], T, r, sigma, 'call')
            strategies['collar'] = self.collar(S, strikes[0], strikes[2], T, r, sigma)
        
        if len(strikes) >= 4:
            strategies['iron_condor'] = self.iron_condor(S, strikes[0], strikes[1], strikes[2], strikes[3], T, r, sigma)
        
        return strategies
    
    def rank_strategies(self, strategies: Dict, ranking_criteria: str = 'risk_reward') -> List[Tuple[str, Dict, float]]:
        """
        Rankea estrategias basado en diferentes criterios
        """
        ranked = []
        
        for name, strategy in strategies.items():
            if ranking_criteria == 'risk_reward':
                max_profit = strategy.get('max_profit', 0)
                max_loss = abs(strategy.get('max_loss', 1))
                score = max_profit / max_loss if max_loss > 0 else 0
            elif ranking_criteria == 'probability':
                score = strategy.get('probability_profit', 0)
            elif ranking_criteria == 'max_profit':
                score = strategy.get('max_profit', 0)
            else:
                score = 0
            
            ranked.append((name, strategy, score))
        
        return sorted(ranked, key=lambda x: x[2], reverse=True)

# Importar norm para iron_condor
from scipy.stats import norm
