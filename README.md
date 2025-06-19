# Evaluador de Opciones GGAL en Tiempo Real

Una aplicación completa para evaluar oportunidades de inversión en opciones del ticker GGAL (Grupo Financiero Galicia) en tiempo real.

## Características

- **Análisis en Tiempo Real**: Datos actualizados del mercado para GGAL
- **Estrategias de Opciones**: Implementación de múltiples estrategias como:
  - Covered Call
  - Protective Put
  - Iron Condor
  - Butterfly Spread
  - Straddle/Strangle
- **Cálculo de Greeks**: Delta, Gamma, Theta, Vega, Rho
- **Análisis de Volatilidad**: Volatilidad implícita vs histórica
- **Dashboard Interactivo**: Visualización en tiempo real con Streamlit

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
streamlit run app.py
```

## Estructura del Proyecto

- `app.py`: Aplicación principal de Streamlit
- `data_fetcher.py`: Módulo para obtener datos en tiempo real
- `options_calculator.py`: Cálculos de opciones y Greeks
- `strategies.py`: Implementación de estrategias de opciones
- `visualizations.py`: Gráficos y visualizaciones
- `risk_analyzer.py`: Análisis de riesgo y probabilidades

## Disclaimer

Esta aplicación es solo para fines educativos y de análisis. No constituye asesoramiento financiero.
