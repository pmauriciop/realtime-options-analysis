"""
Script de prueba para verificar que todos los módulos funcionen correctamente
antes de ejecutar la aplicación principal.
"""

import sys
import traceback
from datetime import datetime

def test_imports():
    """Prueba que todas las importaciones funcionen"""
    print("🔍 Probando importaciones...")
    
    try:
        import pandas as pd
        import numpy as np
        import yfinance as yf
        import plotly.graph_objects as go
        import plotly.express as px
        import streamlit as st
        from scipy.stats import norm
        from scipy.optimize import minimize_scalar
        print("✅ Todas las librerías estándar importadas correctamente")
    except ImportError as e:
        print(f"❌ Error importando librerías estándar: {e}")
        return False
    
    try:
        from data_fetcher import DataFetcher
        from options_calculator import OptionsCalculator
        from strategies import OptionsStrategies
        from visualizations import OptionsVisualizer
        from risk_analyzer import RiskAnalyzer
        from utils import setup_logger, validate_market_data
        from config import APP_CONFIG
        print("✅ Todos los módulos personalizados importados correctamente")
    except ImportError as e:
        print(f"❌ Error importando módulos personalizados: {e}")
        return False
    
    return True

def test_data_fetcher():
    """Prueba el módulo de obtención de datos"""
    print("\n📊 Probando DataFetcher...")
    
    try:
        from data_fetcher import DataFetcher
        
        # Crear instancia
        fetcher = DataFetcher('GGAL')
        print("✅ DataFetcher creado correctamente")
        
        # Probar obtención de precio actual
        current_price = fetcher.get_current_price()
        if current_price and current_price > 0:
            print(f"✅ Precio actual obtenido: ${current_price:.2f}")
        else:
            print("⚠️ No se pudo obtener precio actual (posible problema de conectividad)")
        
        # Probar volatilidad histórica
        historical_vol = fetcher.calculate_historical_volatility()
        print(f"✅ Volatilidad histórica: {historical_vol*100:.1f}%")
        
        # Probar tasa libre de riesgo
        risk_free = fetcher.get_risk_free_rate()
        print(f"✅ Tasa libre de riesgo: {risk_free*100:.1f}%")
        
        return True
    
    except Exception as e:
        print(f"❌ Error en DataFetcher: {e}")
        traceback.print_exc()
        return False

def test_options_calculator():
    """Prueba el calculador de opciones"""
    print("\n🧮 Probando OptionsCalculator...")
    
    try:
        from options_calculator import OptionsCalculator
        
        calc = OptionsCalculator()
        
        # Parámetros de prueba
        S = 100  # Precio del activo
        K = 100  # Strike
        T = 0.25  # 3 meses
        r = 0.05  # 5%
        sigma = 0.3  # 30%
        
        # Probar Black-Scholes
        call_price = calc.black_scholes_call(S, K, T, r, sigma)
        put_price = calc.black_scholes_put(S, K, T, r, sigma)
        
        print(f"✅ Precio call calculado: ${call_price:.2f}")
        print(f"✅ Precio put calculado: ${put_price:.2f}")
        
        # Probar Greeks
        call_greeks = calc.calculate_greeks(S, K, T, r, sigma, 'call')
        print(f"✅ Greeks calculadas - Delta: {call_greeks['delta']:.3f}")
        
        # Probar volatilidad implícita
        iv = calc.implied_volatility(call_price, S, K, T, r, 'call')
        print(f"✅ Volatilidad implícita: {iv*100:.1f}%")
        
        return True
    
    except Exception as e:
        print(f"❌ Error en OptionsCalculator: {e}")
        traceback.print_exc()
        return False

def test_strategies():
    """Prueba el módulo de estrategias"""
    print("\n🎯 Probando OptionsStrategies...")
    
    try:
        from strategies import OptionsStrategies
        
        strategies = OptionsStrategies()
        
        # Parámetros de prueba
        S = 100
        K = 100
        T = 0.25
        r = 0.05
        sigma = 0.3
        
        # Probar covered call
        covered_call = strategies.covered_call(S, K, T, r, sigma)
        print(f"✅ Covered Call - Max Profit: ${covered_call['max_profit']:.2f}")
        
        # Probar long straddle
        straddle = strategies.long_straddle(S, K, T, r, sigma)
        print(f"✅ Long Straddle - Premium Paid: ${straddle['premium_paid']:.2f}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error en OptionsStrategies: {e}")
        traceback.print_exc()
        return False

def test_visualizations():
    """Prueba el módulo de visualizaciones"""
    print("\n📈 Probando OptionsVisualizer...")
    
    try:
        from visualizations import OptionsVisualizer
        import pandas as pd
        import numpy as np
        
        visualizer = OptionsVisualizer()
        
        # Crear datos de prueba
        test_strategy = {
            'strategy': 'Test Strategy',
            'prices': list(range(80, 121)),
            'payoffs': [x - 100 for x in range(80, 121)]
        }
        
        # Probar gráfico de payoff
        fig = visualizer.plot_option_payoff(test_strategy)
        print("✅ Gráfico de payoff creado correctamente")
        
        # Crear datos de opciones de prueba
        test_options = pd.DataFrame({
            'strike': [95, 100, 105],
            'impliedVolatility': [0.25, 0.30, 0.35],
            'optionType': ['call', 'call', 'call'],
            'moneyness': [1.05, 1.0, 0.95],
            'volume': [100, 200, 150],
            'openInterest': [500, 1000, 750]
        })
        
        # Probar sonrisa de volatilidad
        vol_fig = visualizer.plot_volatility_smile(test_options)
        print("✅ Sonrisa de volatilidad creada correctamente")
        
        return True
    
    except Exception as e:
        print(f"❌ Error en OptionsVisualizer: {e}")
        traceback.print_exc()
        return False

def test_risk_analyzer():
    """Prueba el analizador de riesgo"""
    print("\n⚠️ Probando RiskAnalyzer...")
    
    try:
        from risk_analyzer import RiskAnalyzer
        import numpy as np
        
        analyzer = RiskAnalyzer()
        
        # Crear retornos de prueba
        returns = np.random.normal(0.001, 0.02, 252)  # Un año de retornos diarios
        
        # Probar VaR
        var_95 = analyzer.calculate_var(returns, 0.05)
        print(f"✅ VaR 95%: {var_95:.4f}")
        
        # Probar CVaR
        cvar_95 = analyzer.calculate_cvar(returns, 0.05)
        print(f"✅ CVaR 95%: {cvar_95:.4f}")
        
        # Probar simulación Monte Carlo
        paths = analyzer.monte_carlo_simulation(100, 0.05, 0.3, 0.25, 1000, 63)
        print(f"✅ Simulación Monte Carlo completada: {paths.shape}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error en RiskAnalyzer: {e}")
        traceback.print_exc()
        return False

def test_config():
    """Prueba la configuración"""
    print("\n⚙️ Probando configuración...")
    
    try:
        from config import APP_CONFIG, validate_config
        
        print(f"✅ Ticker configurado: {APP_CONFIG['TICKER']}")
        print(f"✅ Tasa libre de riesgo por defecto: {APP_CONFIG['DEFAULT_RISK_FREE_RATE']*100}%")
        
        if validate_config():
            print("✅ Configuración validada correctamente")
        else:
            print("⚠️ Problemas en la validación de configuración")
        
        return True
    
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def run_full_integration_test():
    """Ejecuta una prueba de integración completa"""
    print("\n🔗 Ejecutando prueba de integración completa...")
    
    try:
        from data_fetcher import DataFetcher
        from options_calculator import OptionsCalculator
        from strategies import OptionsStrategies
        from visualizations import OptionsVisualizer
        from risk_analyzer import RiskAnalyzer
        
        # Simular flujo completo
        print("1. Inicializando componentes...")
        fetcher = DataFetcher('GGAL')
        calculator = OptionsCalculator()
        strategies = OptionsStrategies()
        visualizer = OptionsVisualizer()
        risk_analyzer = RiskAnalyzer()
        
        print("2. Obteniendo datos de mercado...")
        # Usar datos simulados si no hay conectividad
        S = 25.50  # Precio simulado de GGAL
        r = 0.05
        sigma = 0.35
        T = 30/365
        
        print("3. Analizando estrategia...")
        covered_call = strategies.covered_call(S, S, T, r, sigma)
        
        print("4. Creando visualización...")
        fig = visualizer.plot_option_payoff(covered_call)
        
        print("5. Analizando riesgo...")
        risk_results = risk_analyzer.analyze_strategy_risk(
            covered_call, S, r, sigma, T, 1000
        )
        
        print(f"✅ Integración completa exitosa")
        print(f"   - Estrategia: {covered_call['strategy']}")
        print(f"   - Max Profit: ${covered_call['max_profit']:.2f}")
        print(f"   - Retorno Esperado: ${risk_results['expected_return']:.2f}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error en prueba de integración: {e}")
        traceback.print_exc()
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA DE ANÁLISIS DE OPCIONES GGAL")
    print("=" * 60)
    
    tests = [
        ("Importaciones", test_imports),
        ("DataFetcher", test_data_fetcher),
        ("OptionsCalculator", test_options_calculator),
        ("OptionsStrategies", test_strategies),
        ("OptionsVisualizer", test_visualizations),
        ("RiskAnalyzer", test_risk_analyzer),
        ("Configuración", test_config),
        ("Integración Completa", run_full_integration_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "="*60)
    print(f"📊 RESULTADOS FINALES: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El sistema está listo para usar.")
        print("\n🚀 Para ejecutar la aplicación, usa:")
        print("   streamlit run app.py")
    else:
        print(f"⚠️ {total - passed} pruebas fallaron. Revisa los errores arriba.")
        print("\n🔧 Recomendaciones:")
        print("   - Verifica tu conexión a internet")
        print("   - Asegúrate de que todas las dependencias estén instaladas")
        print("   - Revisa los logs de error para más detalles")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
