# Script de PowerShell para desplegar GGAL Options Analyzer

Write-Host "🚀 SCRIPT DE DESPLIEGUE - GGAL OPTIONS ANALYZER" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "app.py")) {
    Write-Host "❌ Error: No se encuentra app.py. Ejecuta este script desde el directorio del proyecto." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Verificando archivos del proyecto..." -ForegroundColor Green
Start-Sleep 1

# Verificar archivos importantes
$files = @("app.py", "requirements.txt", "Dockerfile", "Procfile", ".streamlit/config.toml")
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file (faltante)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🔧 Opciones de despliegue disponibles:" -ForegroundColor Cyan
Write-Host "1. Streamlit Cloud (Recomendado - Gratis)" -ForegroundColor Yellow
Write-Host "2. Railway (Fácil - Gratis)" -ForegroundColor Yellow  
Write-Host "3. Render (Gratis)" -ForegroundColor Yellow
Write-Host "4. Heroku (Gratis limitado)" -ForegroundColor Yellow
Write-Host "5. Solo preparar para GitHub" -ForegroundColor Yellow

$option = Read-Host "Selecciona una opción (1-5)"

switch ($option) {
    1 {
        Write-Host ""
        Write-Host "📊 STREAMLIT CLOUD SELECCIONADO" -ForegroundColor Magenta
        Write-Host "================================" -ForegroundColor Magenta
        Write-Host "Pasos a seguir:"
        Write-Host "1. Ve a https://github.com y crea un nuevo repositorio 'ggal-options-analyzer'"
        Write-Host "2. Ejecuta estos comandos:"
        Write-Host "   git remote add origin https://github.com/TU_USUARIO/ggal-options-analyzer.git"
        Write-Host "   git branch -M main"
        Write-Host "   git push -u origin main"
        Write-Host "3. Ve a https://share.streamlit.io"
        Write-Host "4. Conecta con GitHub y despliega desde tu repositorio"
        Write-Host "5. Archivo principal: app.py"
    }
    2 {
        Write-Host ""
        Write-Host "🚂 RAILWAY SELECCIONADO" -ForegroundColor Blue
        Write-Host "======================" -ForegroundColor Blue
        Write-Host "Pasos a seguir:"
        Write-Host "1. Sube tu código a GitHub (mismo proceso que opción 1)"
        Write-Host "2. Ve a https://railway.app"
        Write-Host "3. Conecta con GitHub"
        Write-Host "4. Selecciona 'Deploy from GitHub repo'"
        Write-Host "5. ¡Railway detectará automáticamente tu app Python!"
    }
    3 {
        Write-Host ""
        Write-Host "🎨 RENDER SELECCIONADO" -ForegroundColor DarkGreen
        Write-Host "=====================" -ForegroundColor DarkGreen
        Write-Host "Pasos a seguir:"
        Write-Host "1. Sube tu código a GitHub"
        Write-Host "2. Ve a https://render.com"
        Write-Host "3. Crea 'Web Service' desde GitHub"
        Write-Host "4. Build Command: pip install -r requirements.txt"
        Write-Host "5. Start Command: streamlit run app.py --server.port=`$PORT --server.address=0.0.0.0"
    }
    4 {
        Write-Host ""
        Write-Host "🟣 HEROKU SELECCIONADO" -ForegroundColor DarkMagenta
        Write-Host "=====================" -ForegroundColor DarkMagenta
        Write-Host "Pasos a seguir:"
        Write-Host "1. Instala Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli"
        Write-Host "2. Ejecuta: heroku login"
        Write-Host "3. Ejecuta: heroku create ggal-options-analyzer"
        Write-Host "4. Ejecuta: git push heroku main"
    }
    5 {
        Write-Host ""
        Write-Host "📁 PREPARANDO PARA GITHUB" -ForegroundColor Gray
        Write-Host "=========================" -ForegroundColor Gray
    }
    default {
        Write-Host "❌ Opción no válida" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "📦 Verificando repositorio Git..." -ForegroundColor Cyan

# Verificar si ya hay commits
try {
    $gitLog = git log --oneline -1 2>$null
    if ($gitLog) {
        Write-Host "✅ Repositorio Git ya inicializado con commits" -ForegroundColor Green
    }
} catch {
    Write-Host "🔧 El repositorio necesita commits..." -ForegroundColor Yellow
    Write-Host "Ejecuta: git add . && git commit -m 'Initial commit'"
}

Write-Host ""
Write-Host "📋 RESUMEN DE TU APLICACIÓN:" -ForegroundColor Yellow
Write-Host "============================" -ForegroundColor Yellow
Write-Host "📊 Nombre: GGAL Options Analyzer"
Write-Host "🎯 Funcionalidad: Análisis de opciones financieras en tiempo real"
Write-Host "📈 Características:"
Write-Host "   • Dashboard en tiempo real"
Write-Host "   • Estrategias de opciones (Covered Call, Straddle, etc.)"
Write-Host "   • Análisis de riesgo con Monte Carlo"
Write-Host "   • Visualizaciones interactivas"
Write-Host "   • Análisis técnico avanzado"

Write-Host ""
Write-Host "🌐 SIGUIENTES PASOS:" -ForegroundColor Green
Write-Host "===================" -ForegroundColor Green
Write-Host "1. Crea una cuenta en GitHub si no tienes"
Write-Host "2. Crea un repositorio 'ggal-options-analyzer'"
Write-Host "3. Sube tu código:"
Write-Host "   git remote add origin https://github.com/TU_USUARIO/ggal-options-analyzer.git" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host "4. Despliega en la plataforma elegida"

Write-Host ""
Write-Host "🎉 ¡Tu aplicación estará disponible 24/7 en internet!" -ForegroundColor Green
Write-Host "📞 Si tienes problemas, revisa el archivo DESPLIEGUE_COMPLETO.md" -ForegroundColor Blue

Write-Host ""
Write-Host "Presiona cualquier tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
