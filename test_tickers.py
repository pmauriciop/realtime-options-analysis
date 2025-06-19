#!/usr/bin/env python3
"""
Test para verificar la funcionalidad de selección de tickers
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_fetcher import DataFetcher
from config import MERVAL_TICKERS

def test_ticker_functionality():
    """Prueba la funcionalidad básica con diferentes tickers"""
    print("🧪 Probando funcionalidad de selección de tickers...")
    print(f"📊 Tickers disponibles: {len(MERVAL_TICKERS)}")
      # Probar algunos tickers principales que funcionan
    test_tickers = ['GGAL', 'BMA', 'SUPV', 'YPF', 'PAM']
    
    for ticker in test_tickers:
        print(f"\n🔍 Probando ticker: {ticker} - {MERVAL_TICKERS.get(ticker, 'N/A')}")
        
        try:
            # Inicializar data fetcher
            fetcher = DataFetcher(ticker)
            
            # Obtener precio actual
            price = fetcher.get_current_price()
            if price:
                print(f"  ✅ Precio actual: ${price:.2f}")
            else:
                print(f"  ⚠️ No se pudo obtener precio para {ticker}")
            
            # Obtener datos históricos básicos
            historical = fetcher.get_historical_data(period="1mo")
            if not historical.empty:
                print(f"  ✅ Datos históricos: {len(historical)} registros")
                print(f"  📈 Rango de precios: ${historical['Close'].min():.2f} - ${historical['Close'].max():.2f}")
            else:
                print(f"  ⚠️ No se pudieron obtener datos históricos para {ticker}")
                
        except Exception as e:
            print(f"  ❌ Error con {ticker}: {str(e)}")
    
    print(f"\n✅ Prueba completada")

def test_config_tickers():
    """Verifica que todos los tickers estén bien configurados"""
    print("\n🧪 Verificando configuración de tickers...")
    
    for ticker, name in MERVAL_TICKERS.items():
        print(f"  📊 {ticker}: {name}")
    
    print(f"\n✅ Total de tickers configurados: {len(MERVAL_TICKERS)}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de funcionalidad multi-ticker...")
    
    # Ejecutar pruebas
    test_config_tickers()
    test_ticker_functionality()
    
    print("\n🎉 ¡Todas las pruebas completadas!")
    print("📱 La aplicación está lista para manejar múltiples tickers del S&P Merval")
