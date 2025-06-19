import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import seaborn as sns
import matplotlib.pyplot as plt

class OptionsVisualizer:
    """Clase para crear visualizaciones de opciones y estrategias"""
    
    def __init__(self):
        # Configurar estilo de Plotly
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e', 
            'success': '#2ca02c',
            'danger': '#d62728',
            'warning': '#ff9800',
            'info': '#17a2b8',
            'dark': '#343a40'
        }
    
    def plot_option_payoff(self, strategy_data: Dict, title: str = None) -> go.Figure:
        """
        Crea un gráfico de payoff para una estrategia de opciones
        """
        prices = strategy_data.get('prices', [])
        payoffs = strategy_data.get('payoffs', [])
        
        if not prices or not payoffs:
            return go.Figure()
        
        fig = go.Figure()
        
        # Línea de payoff
        fig.add_trace(go.Scatter(
            x=prices,
            y=payoffs,
            mode='lines',
            name='P&L',
            line=dict(color=self.colors['primary'], width=3),
            fill='tonexty',
            fillcolor='rgba(31, 119, 180, 0.1)'
        ))
        
        # Línea de breakeven
        fig.add_hline(y=0, line_dash="dash", line_color="gray", 
                     annotation_text="Breakeven")
        
        # Destacar zonas de ganancia y pérdida
        positive_payoffs = [max(0, p) for p in payoffs]
        negative_payoffs = [min(0, p) for p in payoffs]
        
        fig.add_trace(go.Scatter(
            x=prices,
            y=positive_payoffs,
            fill='tozeroy',
            fillcolor='rgba(40, 167, 69, 0.3)',
            line=dict(color='rgba(40, 167, 69, 0)'),
            name='Ganancia',
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=prices,
            y=negative_payoffs,
            fill='tozeroy',
            fillcolor='rgba(220, 53, 69, 0.3)',
            line=dict(color='rgba(220, 53, 69, 0)'),
            name='Pérdida',
            showlegend=False
        ))
        
        fig.update_layout(
            title=title or strategy_data.get('strategy', 'Estrategia de Opciones'),
            xaxis_title='Precio del Activo ($)',
            yaxis_title='P&L ($)',
            template='plotly_white',
            hovermode='x unified',
            showlegend=True
        )
        
        return fig
    
    def plot_volatility_smile(self, options_data: pd.DataFrame) -> go.Figure:
        """
        Crea un gráfico de sonrisa de volatilidad
        """
        if options_data.empty or 'impliedVolatility' not in options_data.columns:
            return go.Figure()
        
        fig = go.Figure()
        
        # Separar calls y puts - manejo defensivo
        if 'optionType' in options_data.columns:
            calls = options_data[options_data['optionType'] == 'call']
            puts = options_data[options_data['optionType'] == 'put']
        else:
            # Si no hay columna optionType, usar todos los datos como calls por defecto
            calls = options_data
            puts = pd.DataFrame()
        
        if not calls.empty and 'moneyness' in calls.columns:
            fig.add_trace(go.Scatter(
                x=calls['moneyness'],
                y=calls['impliedVolatility'] * 100,
                mode='markers+lines',
                name='Calls',
                marker=dict(color=self.colors['success'], size=8),
                line=dict(color=self.colors['success'])
            ))
        
        if not puts.empty and 'moneyness' in puts.columns:
            fig.add_trace(go.Scatter(
                x=puts['moneyness'],
                y=puts['impliedVolatility'] * 100,
                mode='markers+lines',
                name='Puts',
                marker=dict(color=self.colors['danger'], size=8),
                line=dict(color=self.colors['danger'])
            ))
        
        fig.update_layout(
            title='Sonrisa de Volatilidad Implícita',
            xaxis_title='Moneyness (S/K)',
            yaxis_title='Volatilidad Implícita (%)',
            template='plotly_white',
            hovermode='closest'
        )
        
        return fig
    
    def plot_greeks_heatmap(self, options_data: pd.DataFrame) -> go.Figure:
        """
        Crea un mapa de calor de las Greeks
        """
        if options_data.empty:
            return go.Figure()
        
        greeks = ['delta', 'gamma', 'theta', 'vega']
        available_greeks = [g for g in greeks if g in options_data.columns]
        
        if not available_greeks or 'strike' not in options_data.columns:
            return go.Figure()
        
        # Preparar datos para el heatmap
        heatmap_data = options_data[['strike'] + available_greeks].set_index('strike')
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values.T,
            x=heatmap_data.index,
            y=available_greeks,
            colorscale='RdYlBu',
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='Mapa de Calor de Greeks',
            xaxis_title='Strike Price',
            yaxis_title='Greeks',
            template='plotly_white'
        )
        
        return fig
    
    def plot_price_history(self, historical_data: pd.DataFrame, technical_indicators: Dict = None) -> go.Figure:
        """
        Crea un gráfico de precios históricos con indicadores técnicos
        """
        if historical_data.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        # Candlestick chart
        fig.add_trace(go.Candlestick(
            x=historical_data.index,
            open=historical_data['Open'],
            high=historical_data['High'],
            low=historical_data['Low'],
            close=historical_data['Close'],
            name='GGAL'
        ))
        
        # Añadir indicadores técnicos si están disponibles
        if technical_indicators:
            if 'sma_20' in technical_indicators and not pd.isna(technical_indicators['sma_20']):
                fig.add_trace(go.Scatter(
                    x=historical_data.index,
                    y=[technical_indicators['sma_20']] * len(historical_data),
                    mode='lines',
                    name='SMA 20',
                    line=dict(color=self.colors['warning'], dash='dash')
                ))
            
            if 'sma_50' in technical_indicators and not pd.isna(technical_indicators['sma_50']):
                fig.add_trace(go.Scatter(
                    x=historical_data.index,
                    y=[technical_indicators['sma_50']] * len(historical_data),
                    mode='lines',
                    name='SMA 50',
                    line=dict(color=self.colors['info'], dash='dash')
                ))
            
            # Bollinger Bands
            if ('bb_upper' in technical_indicators and 'bb_lower' in technical_indicators and 
                not pd.isna(technical_indicators['bb_upper']) and not pd.isna(technical_indicators['bb_lower'])):
                fig.add_trace(go.Scatter(
                    x=historical_data.index,
                    y=[technical_indicators['bb_upper']] * len(historical_data),
                    mode='lines',
                    name='BB Superior',
                    line=dict(color='rgba(128, 128, 128, 0.5)'),
                    showlegend=False
                ))
                
                fig.add_trace(go.Scatter(
                    x=historical_data.index,
                    y=[technical_indicators['bb_lower']] * len(historical_data),
                    mode='lines',
                    name='BB Inferior',
                    line=dict(color='rgba(128, 128, 128, 0.5)'),
                    fill='tonexty',
                    fillcolor='rgba(128, 128, 128, 0.1)',
                    showlegend=False
                ))
        
        fig.update_layout(
            title='Precio Histórico de GGAL',
            xaxis_title='Fecha',
            yaxis_title='Precio ($)',
            template='plotly_white',
            xaxis_rangeslider_visible=False
        )
        
        return fig
    
    def plot_volume_profile(self, options_data: pd.DataFrame) -> go.Figure:
        """
        Crea un perfil de volumen de opciones
        """
        if options_data.empty or 'volume' not in options_data.columns or 'strike' not in options_data.columns:
            return go.Figure()
        
        fig = go.Figure()
        
        # Agrupar por tipo de opción - manejo defensivo
        if 'optionType' in options_data.columns:
            calls = options_data[options_data['optionType'] == 'call']
            puts = options_data[options_data['optionType'] == 'put']
        else:
            # Si no hay columna optionType, usar todos los datos como calls
            calls = options_data
            puts = pd.DataFrame()
        
        if not calls.empty:
            fig.add_trace(go.Bar(
                x=calls['strike'],
                y=calls['volume'],
                name='Calls Volume',
                marker_color=self.colors['success'],
                opacity=0.7
            ))
        
        if not puts.empty:
            fig.add_trace(go.Bar(
                x=puts['strike'],
                y=-puts['volume'],  # Negativo para mostrar hacia abajo
                name='Puts Volume',
                marker_color=self.colors['danger'],
                opacity=0.7
            ))
        
        fig.update_layout(
            title='Perfil de Volumen de Opciones',
            xaxis_title='Strike Price',
            yaxis_title='Volumen',
            template='plotly_white',
            barmode='relative'
        )
        
        return fig
    
    def plot_open_interest(self, options_data: pd.DataFrame) -> go.Figure:
        """
        Crea un gráfico de interés abierto
        """
        if options_data.empty or 'openInterest' not in options_data.columns or 'strike' not in options_data.columns:
            return go.Figure()
        
        fig = go.Figure()
        
        # Separar calls y puts con manejo defensivo
        if 'optionType' in options_data.columns:
            calls = options_data[options_data['optionType'] == 'call']
            puts = options_data[options_data['optionType'] == 'put']
        else:
            # Si no hay columna optionType, usar todos los datos como calls
            calls = options_data
            puts = pd.DataFrame()
        
        if not calls.empty:
            fig.add_trace(go.Scatter(
                x=calls['strike'],
                y=calls['openInterest'],
                mode='markers+lines',
                name='Calls OI',
                marker=dict(color=self.colors['success'], size=10),
                line=dict(color=self.colors['success'])
            ))
        
        if not puts.empty:
            fig.add_trace(go.Scatter(
                x=puts['strike'],
                y=puts['openInterest'],
                mode='markers+lines',
                name='Puts OI',
                marker=dict(color=self.colors['danger'], size=10),
                line=dict(color=self.colors['danger'])
            ))
        
        fig.update_layout(
            title='Interés Abierto por Strike',
            xaxis_title='Strike Price',
            yaxis_title='Interés Abierto',
            template='plotly_white'
        )
        
        return fig
    
    def plot_strategy_comparison(self, strategies: Dict) -> go.Figure:
        """
        Compara múltiples estrategias en un solo gráfico
        """
        fig = go.Figure()
        
        colors = [self.colors['primary'], self.colors['secondary'], self.colors['success'], 
                 self.colors['danger'], self.colors['warning'], self.colors['info']]
        
        for i, (name, strategy) in enumerate(strategies.items()):
            if 'prices' in strategy and 'payoffs' in strategy:
                color = colors[i % len(colors)]
                fig.add_trace(go.Scatter(
                    x=strategy['prices'],
                    y=strategy['payoffs'],
                    mode='lines',
                    name=name.replace('_', ' ').title(),
                    line=dict(color=color, width=2)
                ))
        
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        
        fig.update_layout(
            title='Comparación de Estrategias',
            xaxis_title='Precio del Activo ($)',
            yaxis_title='P&L ($)',
            template='plotly_white',
            hovermode='x unified'
        )
        
        return fig
    
    def create_strategy_summary_table(self, strategies: Dict) -> pd.DataFrame:
        """
        Crea una tabla resumen de estrategias
        """
        summary_data = []
        
        for name, strategy in strategies.items():
            max_profit = strategy.get('max_profit', 0)
            max_loss = strategy.get('max_loss', 0)
            net_cost = strategy.get('net_cost', strategy.get('net_credit', strategy.get('premium_paid', 0)))
            prob_profit = strategy.get('probability_profit', 0)
            
            summary_data.append({
                'Estrategia': name.replace('_', ' ').title(),
                'Max Ganancia': f"${max_profit:,.2f}" if max_profit != float('inf') else "Ilimitado",
                'Max Pérdida': f"${max_loss:,.2f}" if max_loss != float('-inf') else "Ilimitado",
                'Costo/Crédito': f"${net_cost:,.2f}",
                'Prob. Ganancia': f"{prob_profit*100:.1f}%",
                'Descripción': strategy.get('description', '')
            })
        
        return pd.DataFrame(summary_data)
    
    def plot_risk_metrics_radar(self, strategy_data: Dict) -> go.Figure:
        """
        Crea un gráfico radar de métricas de riesgo
        """
        # Normalizar métricas (0-100 scale)
        max_profit = strategy_data.get('max_profit', 0)
        max_loss = abs(strategy_data.get('max_loss', 1))
        prob_profit = strategy_data.get('probability_profit', 0) * 100
        
        # Calcular métricas normalizadas
        metrics = {
            'Potencial de Ganancia': min(max_profit / 1000 * 100, 100) if max_profit != float('inf') else 100,
            'Control de Riesgo': max(0, 100 - (max_loss / 1000 * 100)),
            'Probabilidad de Éxito': prob_profit,
            'Simplicidad': 100 - len(strategy_data.get('components', [])) * 20,
            'Liquidez': 70  # Valor por defecto
        }
        
        categories = list(metrics.keys())
        values = list(metrics.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=strategy_data.get('strategy', 'Estrategia'),
            marker_color=self.colors['primary']
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title='Perfil de Riesgo de la Estrategia',
            template='plotly_white'
        )
        
        return fig
