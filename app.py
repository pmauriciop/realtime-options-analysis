import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

# Importar módulos personalizados
from data_fetcher import DataFetcher
from options_calculator import OptionsCalculator
from strategies import OptionsStrategies
from visualizations import OptionsVisualizer
from risk_analyzer import RiskAnalyzer

# Configuración de la página
st.set_page_config(
    page_title="GGAL Options Analyzer - Tiempo Real",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .profit-positive {
        color: #28a745;
        font-weight: bold;
    }
    .loss-negative {
        color: #dc3545;
        font-weight: bold;
    }
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar objetos
@st.cache_resource
def initialize_analyzers():
    return {
        'data_fetcher': DataFetcher('GGAL'),
        'calculator': OptionsCalculator(),
        'strategies': OptionsStrategies(),
        'visualizer': OptionsVisualizer(),
        'risk_analyzer': RiskAnalyzer()
    }

# Función para cargar datos
@st.cache_data(ttl=60)  # Cache por 1 minuto
def load_market_data():
    analyzers = initialize_analyzers()
    return analyzers['data_fetcher'].get_market_data()

# Función principal
def main():
    # Header
    st.markdown('<h1 class="main-header">📈 Evaluador de Opciones GGAL - Tiempo Real</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.markdown('<div class="sidebar-header">⚙️ Configuración</div>', unsafe_allow_html=True)
    
    # Auto-refresh
    auto_refresh = st.sidebar.checkbox("Auto-actualizar (30s)", value=True)
    if auto_refresh:
        time.sleep(30)
        st.rerun()
    
    # Configuración manual
    st.sidebar.subheader("Parámetros de Análisis")
    
    # Parámetros del mercado
    risk_free_rate = st.sidebar.slider("Tasa Libre de Riesgo (%)", 0.0, 10.0, 5.0, 0.1) / 100
    volatility_override = st.sidebar.slider("Volatilidad Implícita (%)", 10.0, 100.0, 30.0, 1.0) / 100
    use_historical_vol = st.sidebar.checkbox("Usar Volatilidad Histórica", value=True)
    
    # Parámetros de simulación
    num_simulations = st.sidebar.slider("Simulaciones Monte Carlo", 1000, 10000, 5000, 1000)
    
    try:
        # Cargar datos del mercado
        with st.spinner("Cargando datos del mercado..."):
            market_data = load_market_data()
            analyzers = initialize_analyzers()
        
        if market_data['current_price'] is None:
            st.error("❌ No se pudieron obtener datos de GGAL. Verifica la conexión o el ticker.")
            return
        
        # Información básica
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Precio Actual GGAL",
                f"${market_data['current_price']:.2f}",
                f"{((market_data['current_price'] / market_data['historical_data']['Close'].iloc[-2] - 1) * 100):.2f}%" if len(market_data['historical_data']) > 1 else "N/A"
            )
        
        with col2:
            vol_to_use = market_data['historical_volatility'] if use_historical_vol else volatility_override
            st.metric(
                "Volatilidad",
                f"{vol_to_use * 100:.1f}%",
                "Histórica" if use_historical_vol else "Manual"
            )
        
        with col3:
            st.metric(
                "Tasa Libre Riesgo",
                f"{risk_free_rate * 100:.1f}%",
                "Treasury 10Y" if risk_free_rate == market_data['risk_free_rate'] else "Manual"
            )
        
        with col4:
            st.metric(
                "Última Actualización",
                market_data['last_update'].strftime("%H:%M:%S"),
                market_data['last_update'].strftime("%d/%m/%Y")
            )
        
        # Tabs principales
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Dashboard", "🎯 Estrategias", "📈 Análisis Técnico", 
            "⚠️ Gestión de Riesgo", "📋 Cadena de Opciones"
        ])
        
        with tab1:
            st.subheader("Dashboard Principal")
            
            # Información de la empresa
            company_info = analyzers['data_fetcher'].get_company_info()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Gráfico de precios históricos
                if not market_data['historical_data'].empty:
                    price_fig = analyzers['visualizer'].plot_price_history(
                        market_data['historical_data'], 
                        market_data['technical_indicators']
                    )
                    st.plotly_chart(price_fig, use_container_width=True)
            
            with col2:
                st.subheader("Información de GGAL")
                st.write(f"**Sector:** {company_info['sector']}")
                st.write(f"**Beta:** {company_info['beta']:.2f}")
                if company_info['pe_ratio']:
                    st.write(f"**P/E Ratio:** {company_info['pe_ratio']:.2f}")
                if company_info['dividend_yield']:
                    st.write(f"**Dividend Yield:** {company_info['dividend_yield']*100:.2f}%")
                
                # Indicadores técnicos
                st.subheader("Indicadores Técnicos")
                tech_ind = market_data['technical_indicators']
                if tech_ind:
                    st.write(f"**RSI:** {tech_ind.get('rsi', 0):.1f}")
                    st.write(f"**SMA 20:** ${tech_ind.get('sma_20', 0):.2f}")
                    st.write(f"**SMA 50:** ${tech_ind.get('sma_50', 0):.2f}")
        
        with tab2:
            st.subheader("🎯 Análisis de Estrategias de Opciones")
            
            # Configuración de estrategias
            col1, col2 = st.columns(2)
            
            with col1:
                expiration_days = st.slider("Días hasta Expiración", 7, 365, 30)
                T = expiration_days / 365.25
            
            with col2:
                strategy_type = st.selectbox(
                    "Tipo de Estrategia",
                    ["Todas", "Covered Call", "Protective Put", "Long Straddle", 
                     "Iron Condor", "Butterfly Spread", "Collar"]
                )
            
            # Generar strikes alrededor del precio actual
            current_price = market_data['current_price']
            strikes = [
                current_price * 0.90,
                current_price * 0.95,
                current_price,
                current_price * 1.05,
                current_price * 1.10
            ]
            
            vol_to_use = market_data['historical_volatility'] if use_historical_vol else volatility_override
            
            # Analizar estrategias
            with st.spinner("Analizando estrategias..."):
                if strategy_type == "Todas":
                    strategies = analyzers['strategies'].analyze_all_strategies(
                        current_price, T, risk_free_rate, vol_to_use, strikes
                    )
                else:
                    strategies = {}
                    if strategy_type == "Covered Call":
                        strategies['covered_call'] = analyzers['strategies'].covered_call(
                            current_price, strikes[2], T, risk_free_rate, vol_to_use
                        )
                    elif strategy_type == "Protective Put":
                        strategies['protective_put'] = analyzers['strategies'].protective_put(
                            current_price, strikes[1], T, risk_free_rate, vol_to_use
                        )
                    elif strategy_type == "Long Straddle":
                        strategies['long_straddle'] = analyzers['strategies'].long_straddle(
                            current_price, strikes[2], T, risk_free_rate, vol_to_use
                        )
                    elif strategy_type == "Iron Condor":
                        strategies['iron_condor'] = analyzers['strategies'].iron_condor(
                            current_price, strikes[0], strikes[1], strikes[3], strikes[4],
                            T, risk_free_rate, vol_to_use
                        )
                    elif strategy_type == "Butterfly Spread":
                        strategies['butterfly_call'] = analyzers['strategies'].butterfly_spread(
                            current_price, strikes[1], strikes[2], strikes[3],
                            T, risk_free_rate, vol_to_use, 'call'
                        )
                    elif strategy_type == "Collar":
                        strategies['collar'] = analyzers['strategies'].collar(
                            current_price, strikes[1], strikes[3], T, risk_free_rate, vol_to_use
                        )
            
            if strategies:
                # Ranking de estrategias
                ranked_strategies = analyzers['strategies'].rank_strategies(strategies, 'risk_reward')
                
                # Mostrar tabla resumen
                summary_df = analyzers['visualizer'].create_strategy_summary_table(strategies)
                st.subheader("📊 Resumen de Estrategias")
                st.dataframe(summary_df, use_container_width=True)
                
                # Gráficos de payoff
                st.subheader("📈 Gráficos de Payoff")
                
                if len(strategies) > 1:
                    # Comparación múltiple
                    comparison_fig = analyzers['visualizer'].plot_strategy_comparison(strategies)
                    st.plotly_chart(comparison_fig, use_container_width=True)
                
                # Gráficos individuales
                for name, strategy in strategies.items():
                    with st.expander(f"📊 {strategy.get('strategy', name)}"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            payoff_fig = analyzers['visualizer'].plot_option_payoff(strategy)
                            st.plotly_chart(payoff_fig, use_container_width=True)
                        
                        with col2:
                            # Análisis de riesgo para esta estrategia
                            risk_results = analyzers['risk_analyzer'].analyze_strategy_risk(
                                strategy, current_price, risk_free_rate, vol_to_use, T, 1000
                            )
                            
                            st.markdown("**Métricas de Riesgo:**")
                            st.write(f"Retorno Esperado: ${risk_results['expected_return']:.2f}")
                            st.write(f"Volatilidad: ${risk_results['volatility']:.2f}")
                            st.write(f"VaR 95%: ${risk_results['var_95']:.2f}")
                            st.write(f"Prob. Ganancia: {risk_results['prob_profit']*100:.1f}%")
                            
                            # Gráfico radar de riesgo
                            radar_fig = analyzers['visualizer'].plot_risk_metrics_radar(strategy)
                            st.plotly_chart(radar_fig, use_container_width=True)
        
        with tab3:
            st.subheader("📈 Análisis Técnico Avanzado")
            
            if not market_data['historical_data'].empty:
                col1, col2 = st.columns(2)
                
                # Análisis de volatilidad
                with col1:
                    st.subheader("Análisis de Volatilidad")
                    
                    # Calcular volatilidad rodante
                    returns = np.log(market_data['historical_data']['Close'] / 
                                   market_data['historical_data']['Close'].shift(1)).dropna()
                    
                    vol_windows = [20, 50, 100]
                    vol_data = {}
                    
                    for window in vol_windows:
                        vol_data[f'Vol_{window}d'] = returns.rolling(window).std() * np.sqrt(252) * 100
                    
                    vol_df = pd.DataFrame(vol_data, index=returns.index)
                    st.line_chart(vol_df)
                    
                    # Estadísticas de volatilidad
                    st.write(f"**Vol. Histórica (252d):** {market_data['historical_volatility']*100:.1f}%")
                    st.write(f"**Vol. Actual (20d):** {vol_df['Vol_20d'].iloc[-1]:.1f}%")
                    st.write(f"**Vol. Promedio (1y):** {vol_df['Vol_20d'].mean():.1f}%")
                
                with col2:
                    st.subheader("Distribución de Retornos")
                    
                    # Histograma de retornos
                    fig_hist = px.histogram(
                        returns * 100, 
                        nbins=50,
                        title="Distribución de Retornos Diarios (%)",
                        labels={'value': 'Retorno (%)', 'count': 'Frecuencia'}
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                    
                    # Estadísticas descriptivas
                    st.write(f"**Media:** {returns.mean()*252*100:.1f}% anual")
                    st.write(f"**Desv. Std:** {returns.std()*np.sqrt(252)*100:.1f}% anual")
                    st.write(f"**Skewness:** {returns.skew():.2f}")
                    st.write(f"**Kurtosis:** {returns.kurtosis():.2f}")
        
        with tab4:
            st.subheader("⚠️ Gestión de Riesgo")
            
            # Seleccionar estrategia para análisis de riesgo
            if 'strategies' in locals() and strategies:
                strategy_names = list(strategies.keys())
                selected_strategy = st.selectbox("Seleccionar Estrategia para Análisis", strategy_names)
                
                if selected_strategy:
                    strategy = strategies[selected_strategy]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Simulación Monte Carlo")
                        
                        # Análisis de riesgo completo
                        risk_results = analyzers['risk_analyzer'].analyze_strategy_risk(
                            strategy, current_price, risk_free_rate, vol_to_use, T, num_simulations
                        )
                        
                        # Métricas principales
                        st.metric("Retorno Esperado", f"${risk_results['expected_return']:.2f}")
                        st.metric("VaR 95%", f"${risk_results['var_95']:.2f}")
                        st.metric("CVaR 95%", f"${risk_results['cvar_95']:.2f}")
                        
                        # Distribución de P&L
                        fig_dist = px.histogram(
                            risk_results['simulated_payoffs'],
                            nbins=50,
                            title="Distribución de P&L (Monte Carlo)",
                            labels={'value': 'P&L ($)', 'count': 'Frecuencia'}
                        )
                        fig_dist.add_vline(x=0, line_dash="dash", line_color="red")
                        st.plotly_chart(fig_dist, use_container_width=True)
                    
                    with col2:
                        st.subheader("Pruebas de Estrés")
                        
                        # Generar reporte de riesgo
                        risk_report = analyzers['risk_analyzer'].generate_risk_report(
                            strategy, market_data, risk_results
                        )
                        
                        # Mostrar resultados de stress tests
                        stress_results = risk_report['stress_tests']
                        
                        for scenario, results in stress_results.items():
                            with st.expander(f"📊 {scenario}"):
                                st.write(f"**Precio Simulado:** ${results['scenario_price']:.2f}")
                                
                                pnl = results['total_pnl']
                                if pnl >= 0:
                                    st.markdown(f"**P&L:** <span class='profit-positive'>${pnl:.2f}</span>", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"**P&L:** <span class='loss-negative'>${pnl:.2f}</span>", unsafe_allow_html=True)
                                
                                st.write(f"**Retorno:** {results['return_pct']:.1f}%")
                          # Percentiles de P&L
                        st.subheader("Percentiles de P&L")
                        percentiles_df = pd.DataFrame([risk_results['percentiles']]).T
                        percentiles_df.columns = ['P&L ($)']
                        st.dataframe(percentiles_df)
        
        with tab5:
            st.subheader("📋 Cadena de Opciones")
            
            options_chain = market_data['options_chain']
            
            if options_chain:
                # Selector de fecha de expiración
                expiration_dates = list(options_chain.keys())
                selected_expiration = st.selectbox("Fecha de Expiración", expiration_dates)
                
                if selected_expiration:
                    chain_data = options_chain[selected_expiration]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📞 Calls")
                        if not chain_data['calls'].empty:
                            # Analizar cadena de calls
                            calls_analyzed = analyzers['calculator'].analyze_option_chain(
                                chain_data['calls'], current_price, risk_free_rate, selected_expiration
                            )
                            
                            if not calls_analyzed.empty:
                                # Seleccionar columnas disponibles
                                available_cols = ['strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest']
                                optional_cols = ['impliedVolatility', 'delta', 'probITM']
                                
                                display_cols = available_cols.copy()
                                for col in optional_cols:
                                    if col in calls_analyzed.columns:
                                        display_cols.append(col)
                                
                                # Mostrar tabla de calls
                                calls_display = calls_analyzed[display_cols].round(4)
                                st.dataframe(calls_display, use_container_width=True)
                            else:
                                st.info("No se pudieron analizar las opciones call")
                        else:
                            st.info("No hay datos de calls disponibles")
                    
                    with col2:
                        st.subheader("📉 Puts")
                        if not chain_data['puts'].empty:
                            # Analizar cadena de puts
                            puts_analyzed = analyzers['calculator'].analyze_option_chain(
                                chain_data['puts'], current_price, risk_free_rate, selected_expiration
                            )
                            
                            if not puts_analyzed.empty:
                                # Seleccionar columnas disponibles
                                available_cols = ['strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest']
                                optional_cols = ['impliedVolatility', 'delta', 'probITM']
                                
                                display_cols = available_cols.copy()
                                for col in optional_cols:
                                    if col in puts_analyzed.columns:
                                        display_cols.append(col)
                                
                                # Mostrar tabla de puts
                                puts_display = puts_analyzed[display_cols].round(4)
                                st.dataframe(puts_display, use_container_width=True)
                            else:
                                st.info("No se pudieron analizar las opciones put")
                        else:
                            st.info("No hay datos de puts disponibles")
                    
                    # Gráficos de la cadena de opciones
                    if 'calls_analyzed' in locals() or 'puts_analyzed' in locals():
                        st.subheader("📊 Visualizaciones de la Cadena")
                        
                        tab_vol, tab_volume, tab_oi = st.tabs(["Volatilidad", "Volumen", "Interés Abierto"])
                        
                        with tab_vol:
                            # Combinar datos para sonrisa de volatilidad
                            all_options = pd.DataFrame()
                            if 'calls_analyzed' in locals() and not calls_analyzed.empty:
                                all_options = pd.concat([all_options, calls_analyzed])
                            if 'puts_analyzed' in locals() and not puts_analyzed.empty:
                                all_options = pd.concat([all_options, puts_analyzed])
                            
                            if not all_options.empty:
                                vol_smile_fig = analyzers['visualizer'].plot_volatility_smile(all_options)
                                st.plotly_chart(vol_smile_fig, use_container_width=True)
                        
                        with tab_volume:
                            if not all_options.empty:
                                volume_fig = analyzers['visualizer'].plot_volume_profile(all_options)
                                st.plotly_chart(volume_fig, use_container_width=True)
                        
                        with tab_oi:
                            if not all_options.empty:
                                oi_fig = analyzers['visualizer'].plot_open_interest(all_options)
                                st.plotly_chart(oi_fig, use_container_width=True)
            else:
                st.warning("⚠️ No se encontraron datos de opciones para GGAL. Puede que no haya opciones disponibles o problemas de conectividad.")
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.8rem;'>
            📊 Evaluador de Opciones GGAL - Desarrollado para análisis educativo<br>
            ⚠️ Este análisis no constituye asesoramiento financiero
        </div>
        """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Error en la aplicación: {str(e)}")
        st.info("🔄 Intenta actualizar la página o verifica tu conexión a internet.")

# Imports adicionales necesarios
import plotly.express as px

if __name__ == "__main__":
    main()
