import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import logging

def setup_logger(name: str) -> logging.Logger:
    """Configura un logger para el módulo"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

def validate_market_data(data: Dict) -> bool:
    """Valida que los datos de mercado sean correctos"""
    required_fields = ['current_price', 'historical_volatility', 'risk_free_rate']
    
    for field in required_fields:
        if field not in data or data[field] is None:
            return False
        
        if isinstance(data[field], (int, float)) and (np.isnan(data[field]) or np.isinf(data[field])):
            return False
    
    return True

def format_currency(amount: float, decimals: int = 2) -> str:
    """Formatea un número como moneda"""
    if amount == float('inf'):
        return "Ilimitado"
    elif amount == float('-inf'):
        return "-Ilimitado"
    else:
        return f"${amount:,.{decimals}f}"

def format_percentage(value: float, decimals: int = 1) -> str:
    """Formatea un número como porcentaje"""
    return f"{value * 100:.{decimals}f}%"

def calculate_returns(prices: pd.Series, method: str = 'simple') -> pd.Series:
    """Calcula retornos de una serie de precios"""
    if method == 'simple':
        return prices.pct_change().dropna()
    elif method == 'log':
        return np.log(prices / prices.shift(1)).dropna()
    else:
        raise ValueError("Method must be 'simple' or 'log'")

def generate_strike_ladder(current_price: float, num_strikes: int = 5, 
                          range_pct: float = 0.2) -> List[float]:
    """Genera una escalera de strikes alrededor del precio actual"""
    strikes = []
    step = (range_pct * 2) / (num_strikes - 1)
    
    for i in range(num_strikes):
        multiplier = 1 + (-range_pct + i * step)
        strike = current_price * multiplier
        strikes.append(round(strike, 2))
    
    return strikes

def calculate_moneyness(spot_price: float, strike_price: float) -> float:
    """Calcula el moneyness (S/K)"""
    return spot_price / strike_price

def classify_option_moneyness(spot_price: float, strike_price: float, 
                            option_type: str) -> str:
    """Clasifica una opción como ITM, ATM, o OTM"""
    if option_type.lower() == 'call':
        if spot_price > strike_price * 1.02:
            return "ITM"
        elif spot_price < strike_price * 0.98:
            return "OTM"
        else:
            return "ATM"
    else:  # put
        if spot_price < strike_price * 0.98:
            return "ITM"
        elif spot_price > strike_price * 1.02:
            return "OTM"
        else:
            return "ATM"

def calculate_days_to_expiration(expiration_date: str) -> int:
    """Calcula días hasta expiración"""
    try:
        exp_date = datetime.strptime(expiration_date, '%Y-%m-%d')
        today = datetime.now()
        return max((exp_date - today).days, 0)
    except:
        return 0

def interpolate_volatility(strikes: List[float], vols: List[float], 
                          target_strike: float) -> float:
    """Interpola volatilidad para un strike específico"""
    if len(strikes) != len(vols) or len(strikes) < 2:
        return np.mean(vols) if vols else 0.3
    
    # Interpolación linear simple
    return np.interp(target_strike, strikes, vols)

def create_payoff_data(strategy_components: List[Dict], price_range: Tuple[float, float], 
                      num_points: int = 100) -> Tuple[List[float], List[float]]:
    """Crea datos de payoff para una estrategia"""
    prices = np.linspace(price_range[0], price_range[1], num_points)
    payoffs = []
    
    for price in prices:
        total_payoff = 0
        
        for component in strategy_components:
            if component['type'] == 'stock':
                payoff = component['quantity'] * (price - component['entry_price'])
            
            elif component['type'] == 'call':
                intrinsic = max(price - component['strike'], 0)
                payoff = component['quantity'] * (intrinsic - component['premium'])
            
            elif component['type'] == 'put':
                intrinsic = max(component['strike'] - price, 0)
                payoff = component['quantity'] * (intrinsic - component['premium'])
            
            else:
                payoff = 0
            
            total_payoff += payoff
        
        payoffs.append(total_payoff)
    
    return prices.tolist(), payoffs

def calculate_portfolio_metrics(returns: pd.Series) -> Dict[str, float]:
    """Calcula métricas básicas de un portafolio"""
    if returns.empty:
        return {}
    
    annual_return = returns.mean() * 252
    annual_vol = returns.std() * np.sqrt(252)
    sharpe_ratio = annual_return / annual_vol if annual_vol > 0 else 0
    
    # Drawdown máximo
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    
    return {
        'annual_return': annual_return,
        'annual_volatility': annual_vol,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'total_return': cumulative.iloc[-1] - 1,
        'num_observations': len(returns)
    }

def validate_strategy_parameters(strategy_type: str, parameters: Dict) -> bool:
    """Valida parámetros de una estrategia"""
    required_params = {
        'covered_call': ['spot_price', 'strike', 'premium'],
        'protective_put': ['spot_price', 'strike', 'premium'],
        'straddle': ['spot_price', 'strike', 'call_premium', 'put_premium'],
        'strangle': ['spot_price', 'call_strike', 'put_strike', 'call_premium', 'put_premium'],
        'iron_condor': ['spot_price', 'strikes', 'premiums'],
        'butterfly': ['spot_price', 'strikes', 'premiums']
    }
    
    if strategy_type not in required_params:
        return False
    
    required = required_params[strategy_type]
    return all(param in parameters for param in required)

def sanitize_numeric_input(value, default: float = 0.0, min_val: float = None, 
                          max_val: float = None) -> float:
    """Sanitiza entrada numérica"""
    try:
        num_val = float(value)
        
        if np.isnan(num_val) or np.isinf(num_val):
            return default
        
        if min_val is not None and num_val < min_val:
            return min_val
        
        if max_val is not None and num_val > max_val:
            return max_val
        
        return num_val
    
    except (ValueError, TypeError):
        return default

def create_summary_statistics(data: pd.DataFrame, columns: List[str] = None) -> Dict:
    """Crea estadísticas descriptivas de un DataFrame"""
    if data.empty:
        return {}
    
    if columns:
        data = data[columns]
    
    numeric_data = data.select_dtypes(include=[np.number])
    
    if numeric_data.empty:
        return {}
    
    stats = {
        'count': numeric_data.count().to_dict(),
        'mean': numeric_data.mean().to_dict(),
        'std': numeric_data.std().to_dict(),
        'min': numeric_data.min().to_dict(),
        'max': numeric_data.max().to_dict(),
        'median': numeric_data.median().to_dict(),
        'q25': numeric_data.quantile(0.25).to_dict(),
        'q75': numeric_data.quantile(0.75).to_dict()
    }
    
    return stats

def export_strategy_report(strategy_data: Dict, filename: str = None) -> str:
    """Exporta un reporte de estrategia a CSV o texto"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"strategy_report_{timestamp}.txt"
    
    report_lines = [
        f"REPORTE DE ESTRATEGIA DE OPCIONES",
        f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 50,
        f"Estrategia: {strategy_data.get('strategy', 'N/A')}",
        f"Descripción: {strategy_data.get('description', 'N/A')}",
        "",
        "MÉTRICAS FINANCIERAS:",
        f"- Ganancia Máxima: {format_currency(strategy_data.get('max_profit', 0))}",
        f"- Pérdida Máxima: {format_currency(strategy_data.get('max_loss', 0))}",
        f"- Punto de Equilibrio: {format_currency(strategy_data.get('breakeven', 0))}",
        f"- Costo/Crédito Neto: {format_currency(strategy_data.get('net_cost', 0))}",
        "",
        "COMPONENTES:",
    ]
    
    components = strategy_data.get('components', [])
    for i, comp in enumerate(components, 1):
        report_lines.append(f"{i}. {comp.get('type', 'N/A').title()}: "
                           f"Cantidad {comp.get('quantity', 0)}, "
                           f"Strike ${comp.get('strike', 0):.2f}, "
                           f"Premio ${comp.get('price', 0):.2f}")
    
    report_content = "\n".join(report_lines)
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        return filename
    except Exception as e:
        print(f"Error exportando reporte: {e}")
        return ""

class DataCache:
    """Cache simple para datos de mercado"""
    
    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}
        self.ttl = ttl_seconds
    
    def get(self, key: str):
        """Obtiene un valor del cache"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if (datetime.now() - timestamp).seconds < self.ttl:
                return data
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value):
        """Almacena un valor en el cache"""
        self.cache[key] = (value, datetime.now())
    
    def clear(self):
        """Limpia el cache"""
        self.cache.clear()
    
    def size(self):
        """Retorna el tamaño del cache"""
        return len(self.cache)
