# Script simple para conectar con GitHub
# Análisis de Opciones en Tiempo Real - GGAL

Write-Host "=== CONEXIÓN CON GITHUB ===" -ForegroundColor Green
Write-Host ""

# Verificar repositorio
Write-Host "1. Estado del repositorio:" -ForegroundColor Yellow
git status
Write-Host ""

# Mostrar configuración actual
Write-Host "2. Configuración actual de Git:" -ForegroundColor Yellow
Write-Host "Usuario: $(git config user.name)"
Write-Host "Email: $(git config user.email)"
Write-Host ""

# Archivos importantes
Write-Host "3. Archivos para despliegue:" -ForegroundColor Yellow
$files = @("app.py", "requirements.txt", ".streamlit/config.toml", "README.md")
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "✓ $file existe" -ForegroundColor Green
    } else {
        Write-Host "✗ $file falta" -ForegroundColor Red
    }
}
Write-Host ""

# Instrucciones para GitHub
Write-Host "4. CREAR REPOSITORIO EN GITHUB:" -ForegroundColor Cyan
Write-Host "   - Ve a: https://github.com/new"
Write-Host "   - Nombre: realtime-options-analysis"
Write-Host "   - Descripción: Análisis en tiempo real de opciones GGAL"
Write-Host "   - Público (para Streamlit Cloud gratis)"
Write-Host "   - NO inicializar con README"
Write-Host ""

Write-Host "5. COMANDOS A EJECUTAR DESPUÉS:" -ForegroundColor Cyan
Write-Host "   git remote add origin https://github.com/TU_USUARIO/realtime-options-analysis.git"
Write-Host "   git branch -M main"
Write-Host "   git push -u origin main"
Write-Host ""

Write-Host "6. DESPLEGAR EN STREAMLIT CLOUD:" -ForegroundColor Cyan
Write-Host "   - Ve a: https://share.streamlit.io/"
Write-Host "   - New app > GitHub > realtime-options-analysis"
Write-Host "   - Branch: main, File: app.py"
Write-Host ""

Write-Host "¡Proyecto listo para internet! 🚀" -ForegroundColor Green
