# Configuración de la aplicación
import os

# Configuraciones de la aplicación
APP_CONFIG = {
    'TICKER': 'GGAL',
    'DEFAULT_RISK_FREE_RATE': 0.05,  # 5%
    'DEFAULT_VOLATILITY': 0.30,      # 30%
    'UPDATE_INTERVAL': 30,            # segundos
    'CACHE_TTL': 60,                  # segundos
    'MAX_SIMULATIONS': 10000,
    'DEFAULT_SIMULATIONS': 5000
}

# Configuraciones de visualización
PLOT_CONFIG = {
    'COLORS': {
        'primary': '#1f77b4',
        'secondary': '#ff7f0e', 
        'success': '#2ca02c',
        'danger': '#d62728',
        'warning': '#ff9800',
        'info': '#17a2b8',
        'dark': '#343a40'
    },
    'TEMPLATE': 'plotly_white',
    'HEIGHT': 400,
    'WIDTH': 800
}

# Configuraciones de opciones
OPTIONS_CONFIG = {
    'MIN_DAYS_TO_EXPIRATION': 1,
    'MAX_DAYS_TO_EXPIRATION': 365,
    'DEFAULT_DAYS_TO_EXPIRATION': 30,
    'STRIKE_RANGE': [-0.2, 0.2],  # ±20% del precio actual
    'NUM_STRIKES': 5
}

# Configuraciones de riesgo
RISK_CONFIG = {
    'VAR_CONFIDENCE_LEVELS': [0.01, 0.05, 0.10],
    'STRESS_SCENARIOS': [
        {'name': 'Mercado Bajista', 'price_change': -0.2, 'vol_change': 0.5},
        {'name': 'Mercado Alcista', 'price_change': 0.2, 'vol_change': -0.2},
        {'name': 'Alta Volatilidad', 'price_change': 0, 'vol_change': 1.0},
        {'name': 'Crash', 'price_change': -0.4, 'vol_change': 2.0},
        {'name': 'Rally', 'price_change': 0.3, 'vol_change': -0.1}
    ]
}

# URLs y endpoints
API_CONFIG = {
    'YAHOO_FINANCE_URL': 'https://finance.yahoo.com',
    'BACKUP_DATA_SOURCE': None,
    'TIMEOUT': 30  # segundos
}

# Configuraciones de logging
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('options_analyzer.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# Validación de configuración
def validate_config():
    """Valida que las configuraciones sean correctas"""
    try:
        assert 0 <= APP_CONFIG['DEFAULT_RISK_FREE_RATE'] <= 1
        assert 0 <= APP_CONFIG['DEFAULT_VOLATILITY'] <= 5
        assert APP_CONFIG['UPDATE_INTERVAL'] > 0
        assert APP_CONFIG['MAX_SIMULATIONS'] >= 1000
        return True
    except AssertionError:
        return False
