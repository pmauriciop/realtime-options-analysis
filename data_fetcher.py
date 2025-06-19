import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
from typing import Dict, List, Optional, Tuple
import time

class DataFetcher:
    """Clase para obtener datos financieros en tiempo real"""
    
    def __init__(self, ticker: str = "GGAL"):
        self.ticker = ticker
        self.yf_ticker = yf.Ticker(ticker)
    
    def get_current_price(self) -> float:
        """Obtiene el precio actual del ticker"""
        try:
            data = self.yf_ticker.history(period="1d", interval="1m")
            if not data.empty:
                return data['Close'].iloc[-1]
            else:
                # Fallback a precio de cierre del día anterior
                data = self.yf_ticker.history(period="5d")
                return data['Close'].iloc[-1]
        except Exception as e:
            print(f"Error obteniendo precio actual: {e}")
            return None
    
    def get_historical_data(self, period: str = "1y") -> pd.DataFrame:
        """Obtiene datos históricos del ticker"""
        try:
            data = self.yf_ticker.history(period=period)
            return data
        except Exception as e:
            print(f"Error obteniendo datos históricos: {e}")
            return pd.DataFrame()
    
    def get_options_chain(self) -> Dict:
        """Obtiene la cadena de opciones actual"""
        try:
            # Obtener fechas de expiración disponibles
            expirations = self.yf_ticker.options
            if not expirations:
                return {}
            
            options_data = {}
            for exp_date in expirations[:6]:  # Primeras 6 fechas
                try:
                    opt_chain = self.yf_ticker.option_chain(exp_date)
                    options_data[exp_date] = {
                        'calls': opt_chain.calls,
                        'puts': opt_chain.puts
                    }
                except:
                    continue
            
            return options_data
        except Exception as e:
            print(f"Error obteniendo cadena de opciones: {e}")
            return {}
    
    def calculate_historical_volatility(self, window: int = 252) -> float:
        """Calcula la volatilidad histórica anualizada"""
        try:
            data = self.get_historical_data(period="2y")
            if data.empty:
                return 0.2  # Valor por defecto
            
            returns = np.log(data['Close'] / data['Close'].shift(1)).dropna()
            if len(returns) < window:
                window = len(returns)
            
            volatility = returns.rolling(window=window).std().iloc[-1] * np.sqrt(252)
            return volatility if not np.isnan(volatility) else 0.2
        except Exception as e:
            print(f"Error calculando volatilidad histórica: {e}")
            return 0.2
    
    def get_risk_free_rate(self) -> float:
        """Obtiene la tasa libre de riesgo (aproximación con bonos del tesoro de EE.UU.)"""
        try:
            # Usar yield del Treasury a 10 años como proxy
            treasury = yf.Ticker("^TNX")
            data = treasury.history(period="5d")
            if not data.empty:
                return data['Close'].iloc[-1] / 100  # Convertir porcentaje a decimal
            else:
                return 0.05  # Valor por defecto 5%
        except Exception as e:
            print(f"Error obteniendo tasa libre de riesgo: {e}")
            return 0.05
    
    def get_market_data(self) -> Dict:
        """Obtiene un conjunto completo de datos de mercado"""
        current_price = self.get_current_price()
        historical_data = self.get_historical_data()
        options_chain = self.get_options_chain()
        historical_vol = self.calculate_historical_volatility()
        risk_free_rate = self.get_risk_free_rate()
        
        # Calcular algunos indicadores técnicos básicos
        technical_indicators = {}
        if not historical_data.empty:
            # RSI simple
            delta = historical_data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            technical_indicators['rsi'] = rsi.iloc[-1] if not rsi.empty else 50
            
            # Medias móviles
            technical_indicators['sma_20'] = historical_data['Close'].rolling(20).mean().iloc[-1]
            technical_indicators['sma_50'] = historical_data['Close'].rolling(50).mean().iloc[-1]
            
            # Bollinger Bands
            sma_20 = historical_data['Close'].rolling(20).mean()
            std_20 = historical_data['Close'].rolling(20).std()
            technical_indicators['bb_upper'] = (sma_20 + 2 * std_20).iloc[-1]
            technical_indicators['bb_lower'] = (sma_20 - 2 * std_20).iloc[-1]
        
        return {
            'current_price': current_price,
            'historical_data': historical_data,
            'options_chain': options_chain,
            'historical_volatility': historical_vol,
            'risk_free_rate': risk_free_rate,
            'technical_indicators': technical_indicators,
            'last_update': datetime.now()
        }
    
    def get_company_info(self) -> Dict:
        """Obtiene información básica de la empresa"""
        try:
            info = self.yf_ticker.info
            return {
                'name': info.get('longName', 'GGAL'),
                'sector': info.get('sector', 'Financial Services'),
                'market_cap': info.get('marketCap', 0),
                'beta': info.get('beta', 1.0),
                'pe_ratio': info.get('trailingPE', 0),
                'dividend_yield': info.get('dividendYield', 0)
            }
        except Exception as e:
            print(f"Error obteniendo información de la empresa: {e}")
            return {
                'name': 'GGAL',
                'sector': 'Financial Services',
                'market_cap': 0,
                'beta': 1.0,
                'pe_ratio': 0,
                'dividend_yield': 0
            }
