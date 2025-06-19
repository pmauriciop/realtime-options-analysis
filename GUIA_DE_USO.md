# 🚀 Guía de Uso - Evaluador de Opciones GGAL en Tiempo Real

## 🎯 ¿Qué hace esta aplicación?

Esta aplicación te permite evaluar oportunidades de inversión en opciones del ticker GGAL (Grupo Financiero Galicia) aplicando estrategias de opciones financieras en tiempo real. Es una herramienta completa para:

- **Análisis en tiempo real** de datos de GGAL
- **Evaluación de estrategias** de opciones (Covered Call, Protective Put, Straddle, etc.)
- **Gestión de riesgo** con simulaciones Monte Carlo
- **Visualizaciones interactivas** de payoffs y Greeks
- **Análisis técnico** avanzado

## 🏃‍♂️ Inicio Rápido

### 1. Ejecutar la aplicación
```bash
cd c:\Proyectos\RealTime
streamlit run app.py
```

### 2. Acceder a la aplicación
Abre tu navegador en: `http://localhost:8501`

## 📊 Funcionalidades Principales

### Dashboard Principal
- **Precio en tiempo real** de GGAL
- **Indicadores técnicos** (RSI, Medias móviles, Bollinger Bands)
- **Gráfico de precios** históricos con indicadores
- **Información corporativa** de GGAL

### Análisis de Estrategias
#### Estrategias Disponibles:
1. **Covered Call** - Poseer acciones + vender call
2. **Protective Put** - Poseer acciones + comprar put
3. **Long Straddle** - Comprar call y put mismo strike
4. **Iron Condor** - Vender spreads de calls y puts
5. **Butterfly Spread** - Estrategia neutral de volatilidad
6. **Collar** - Combinar put protector con call cubierto

#### Para cada estrategia verás:
- **Gráfico de Payoff** interactivo
- **Máxima ganancia/pérdida**
- **Puntos de equilibrio**
- **Probabilidad de ganancia**
- **Costo/crédito neto**

### Análisis Técnico
- **Volatilidad histórica** vs implícita
- **Distribución de retornos**
- **Análisis de tendencias**
- **Estadísticas descriptivas**

### Gestión de Riesgo
- **Simulaciones Monte Carlo** (hasta 10,000 simulaciones)
- **Value at Risk (VaR)** al 95% y 99%
- **Conditional VaR (CVaR)**
- **Pruebas de estrés** en diferentes escenarios
- **Distribución de P&L**

### Cadena de Opciones
- **Análisis completo** de calls y puts
- **Greeks calculadas** (Delta, Gamma, Theta, Vega, Rho)
- **Volatilidad implícita** por strike
- **Sonrisa de volatilidad**
- **Perfil de volumen** e interés abierto

## ⚙️ Configuración

### Parámetros Personalizables:
- **Tasa libre de riesgo** (0-10%)
- **Volatilidad implícita** (10-100%)
- **Días hasta expiración** (7-365)
- **Número de simulaciones** Monte Carlo (1,000-10,000)
- **Auto-actualización** cada 30 segundos

### Opciones de Volatilidad:
- ✅ **Usar volatilidad histórica** (recomendado)
- 📊 **Volatilidad manual** para análisis de escenarios

## 🎯 Casos de Uso Principales

### 1. Evaluación de Covered Call
**Objetivo:** Generar ingresos adicionales con acciones que ya posees

**Cómo usar:**
1. Ve a la pestaña "Estrategias"
2. Selecciona "Covered Call"
3. Ajusta días hasta expiración
4. Revisa el gráfico de payoff
5. Analiza máxima ganancia vs riesgo

### 2. Protección con Protective Put
**Objetivo:** Proteger una posición larga en acciones

**Cómo usar:**
1. Selecciona "Protective Put"
2. Compara diferentes strikes
3. Evalúa costo de protección vs beneficio
4. Revisa probabilidad de activación

### 3. Estrategia de Volatilidad con Straddle
**Objetivo:** Beneficiarse de movimientos fuertes en cualquier dirección

**Cómo usar:**
1. Selecciona "Long Straddle"
2. Analiza volatilidad implícita vs histórica
3. Evalúa puntos de equilibrio
4. Considera el decay temporal (Theta)

### 4. Análisis de Riesgo
**Objetivo:** Cuantificar riesgo antes de implementar estrategia

**Cómo usar:**
1. Ve a "Gestión de Riesgo"
2. Selecciona estrategia a analizar
3. Ejecuta simulación Monte Carlo
4. Revisa VaR y pruebas de estrés
5. Evalúa distribución de resultados

## 📈 Interpretación de Resultados

### Métricas Clave:
- **Max Profit:** Ganancia máxima teórica
- **Max Loss:** Pérdida máxima posible
- **Breakeven:** Precio donde P&L = 0
- **Prob. Ganancia:** Probabilidad de obtener ganancia
- **VaR 95%:** Pérdida máxima esperada 95% del tiempo

### Greeks Importantes:
- **Delta:** Sensibilidad al precio del activo
- **Gamma:** Curvatura (cambio en Delta)
- **Theta:** Decay temporal diario
- **Vega:** Sensibilidad a volatilidad

### Indicadores de Calidad:
- **Volumen:** Liquidez de la opción
- **Spread Bid-Ask:** Costo de transacción
- **Interés Abierto:** Actividad en el mercado

## ⚠️ Consideraciones Importantes

### Riesgos:
- **Mercado:** Precios pueden moverse adversamente
- **Liquidez:** Algunas opciones pueden tener baja liquidez
- **Temporal:** El tiempo siempre trabaja contra comprador de opciones
- **Volatilidad:** Cambios inesperados en volatilidad implícita

### Limitaciones:
- **Modelo Black-Scholes:** Asume volatilidad constante
- **Comisiones:** No incluidas en cálculos
- **Dividendos:** No considerados automáticamente
- **Datos en tiempo real:** Dependiente de conectividad

## 🔧 Solución de Problemas

### Problemas Comunes:

**Error: "No se pudieron obtener datos de GGAL"**
- ✅ Verifica conexión a internet
- ✅ El ticker GGAL puede estar fuera de horario de mercado
- ✅ Usa datos simulados para pruebas

**Error: "No hay opciones disponibles"**
- ✅ GGAL puede no tener opciones listadas
- ✅ Verifica que esté en horario de mercado
- ✅ Algunos valores no tienen mercado de opciones activo

**Aplicación lenta:**
- ✅ Reduce número de simulaciones Monte Carlo
- ✅ Desactiva auto-actualización
- ✅ Cierra otras pestañas del navegador

### Comandos Útiles:

**Reiniciar aplicación:**
```bash
Ctrl + C  # En terminal
streamlit run app.py  # Ejecutar nuevamente
```

**Limpiar cache:**
```bash
streamlit cache clear
```

**Ver logs:**
```bash
python test_system.py  # Ejecutar pruebas de diagnóstico
```

## 📚 Recursos Adicionales

### Educación en Opciones:
- [Conceptos básicos de opciones](https://www.investopedia.com/options-basics-tutorial-4583012)
- [Estrategias de opciones](https://www.optionsplaybook.com/)
- [Greeks explicadas](https://www.investopedia.com/trading/using-the-greeks-to-understand-options/)

### Análisis Técnico:
- [Indicadores técnicos](https://www.investopedia.com/technical-analysis-4689633)
- [Análisis de volatilidad](https://www.investopedia.com/articles/optioninvestor/08/implied-volatility.asp)

## 📞 Soporte

Para problemas técnicos:
1. Ejecuta `python test_system.py` para diagnóstico
2. Revisa los logs de error en la consola
3. Verifica que todas las dependencias estén instaladas

## ⚖️ Disclaimer Legal

**⚠️ IMPORTANTE:**
- Esta aplicación es solo para fines educativos y de análisis
- No constituye asesoramiento financiero profesional
- Los resultados pasados no garantizan resultados futuros
- Siempre consulta con un asesor financiero calificado
- Opera solo con capital que puedas permitirte perder

---

🎯 **¡Éxito en tus análisis de opciones con GGAL!**
