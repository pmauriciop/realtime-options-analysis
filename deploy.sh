#!/bin/bash

# Script para automatizar el despliegue de GGAL Options Analyzer

echo "🚀 SCRIPT DE DESPLIEGUE - GGAL OPTIONS ANALYZER"
echo "================================================="

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: No se encuentra app.py. Ejecuta este script desde el directorio del proyecto."
    exit 1
fi

echo "✅ Verificando archivos del proyecto..."
sleep 1

# Verificar archivos importantes
files=("app.py" "requirements.txt" "Dockerfile" "Procfile" ".streamlit/config.toml")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ❌ $file (faltante)"
    fi
done

echo ""
echo "🔧 Opciones de despliegue disponibles:"
echo "1. Streamlit Cloud (Recomendado - Gratis)"
echo "2. Railway (Fácil - Gratis)"
echo "3. Render (Gratis)"
echo "4. Heroku (Gratis limitado)"
echo "5. Solo preparar para GitHub"

read -p "Selecciona una opción (1-5): " option

case $option in
    1)
        echo ""
        echo "📊 STREAMLIT CLOUD SELECCIONADO"
        echo "================================"
        echo "Pasos a seguir:"
        echo "1. Ve a https://github.com y crea un nuevo repositorio 'ggal-options-analyzer'"
        echo "2. Ejecuta estos comandos:"
        echo "   git remote add origin https://github.com/TU_USUARIO/ggal-options-analyzer.git"
        echo "   git branch -M main"
        echo "   git push -u origin main"
        echo "3. Ve a https://share.streamlit.io"
        echo "4. Conecta con GitHub y despliega desde tu repositorio"
        echo "5. Archivo principal: app.py"
        ;;
    2)
        echo ""
        echo "🚂 RAILWAY SELECCIONADO"
        echo "======================"
        echo "Pasos a seguir:"
        echo "1. Sube tu código a GitHub (mismo proceso que opción 1)"
        echo "2. Ve a https://railway.app"
        echo "3. Conecta con GitHub"
        echo "4. Selecciona 'Deploy from GitHub repo'"
        echo "5. ¡Railway detectará automáticamente tu app Python!"
        ;;
    3)
        echo ""
        echo "🎨 RENDER SELECCIONADO"
        echo "====================="
        echo "Pasos a seguir:"
        echo "1. Sube tu código a GitHub"
        echo "2. Ve a https://render.com"
        echo "3. Crea 'Web Service' desde GitHub"
        echo "4. Build Command: pip install -r requirements.txt"
        echo "5. Start Command: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0"
        ;;
    4)
        echo ""
        echo "🟣 HEROKU SELECCIONADO"
        echo "====================="
        echo "Pasos a seguir:"
        echo "1. Instala Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli"
        echo "2. Ejecuta: heroku login"
        echo "3. Ejecuta: heroku create ggal-options-analyzer"
        echo "4. Ejecuta: git push heroku main"
        ;;
    5)
        echo ""
        echo "📁 PREPARANDO PARA GITHUB"
        echo "========================="
        ;;
    *)
        echo "❌ Opción no válida"
        exit 1
        ;;
esac

echo ""
echo "📦 Preparando repositorio Git..."

# Verificar si ya hay un commit
if git log --oneline -1 2>/dev/null; then
    echo "✅ Repositorio Git ya inicializado con commits"
else
    echo "🔧 Inicializando repositorio Git..."
    git init
    git add .
    git commit -m "Initial commit: GGAL Options Analyzer - Real-time options evaluation app"
fi

echo ""
echo "📋 RESUMEN DE TU APLICACIÓN:"
echo "============================"
echo "📊 Nombre: GGAL Options Analyzer"
echo "🎯 Funcionalidad: Análisis de opciones financieras en tiempo real"
echo "📈 Características:"
echo "   • Dashboard en tiempo real"
echo "   • Estrategias de opciones (Covered Call, Straddle, etc.)"
echo "   • Análisis de riesgo con Monte Carlo"
echo "   • Visualizaciones interactivas"
echo "   • Análisis técnico avanzado"

echo ""
echo "🌐 SIGUIENTES PASOS:"
echo "==================="
echo "1. Crea una cuenta en GitHub si no tienes"
echo "2. Crea un repositorio 'ggal-options-analyzer'"
echo "3. Sube tu código:"
echo "   git remote add origin https://github.com/TU_USUARIO/ggal-options-analyzer.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo "4. Despliega en la plataforma elegida"

echo ""
echo "🎉 ¡Tu aplicación estará disponible 24/7 en internet!"
echo "📞 Si tienes problemas, revisa el archivo DESPLIEGUE_COMPLETO.md"
