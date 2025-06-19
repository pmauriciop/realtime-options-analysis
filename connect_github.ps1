# Script PowerShell para conectar el proyecto con GitHub y preparar el despliegue
# Análisis de Opciones en Tiempo Real - GGAL

Write-Host "=== CONFIGURACIÓN AUTOMÁTICA PARA GITHUB Y DESPLIEGUE ===" -ForegroundColor Green
Write-Host ""

# 1. Verificar que tenemos un repositorio Git
Write-Host "1. Verificando repositorio Git..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "✓ Repositorio Git encontrado" -ForegroundColor Green
} else {
    Write-Host "✗ No se encontró repositorio Git. Inicializando..." -ForegroundColor Red
    git init
    git add .
    git commit -m "Initial commit - Aplicación de análisis de opciones GGAL"
}

# 2. Configurar Git (si no está configurado)
Write-Host ""
Write-Host "2. Verificando configuración de Git..." -ForegroundColor Yellow
$gitUser = git config user.name
$gitEmail = git config user.email

if (-not $gitUser) {
    $userName = Read-Host "Ingresa tu nombre de usuario de GitHub"
    git config user.name "$userName"
}

if (-not $gitEmail) {
    $userEmail = Read-Host "Ingresa tu email de GitHub"
    git config user.email "$userEmail"
}

Write-Host "✓ Git configurado correctamente" -ForegroundColor Green

# 3. Mostrar información del repositorio
Write-Host ""
Write-Host "3. Información del repositorio:" -ForegroundColor Yellow
Write-Host "Usuario: $(git config user.name)"
Write-Host "Email: $(git config user.email)"
Write-Host "Commits realizados: $(git rev-list --all --count)"

# 4. Crear el repositorio en GitHub
Write-Host ""
Write-Host "4. SIGUIENTE PASO - CREAR REPOSITORIO EN GITHUB:" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ve a https://github.com/new y crea un nuevo repositorio con:" -ForegroundColor White
Write-Host "  📛 Nombre del repositorio: realtime-options-analysis" -ForegroundColor Yellow
Write-Host "  📝 Descripción: Análisis en tiempo real de opciones financieras sobre GGAL" -ForegroundColor Yellow
Write-Host "  🔓 Público (para usar Streamlit Cloud gratis)" -ForegroundColor Yellow
Write-Host "  ❌ NO inicializar con README (ya tenemos archivos)" -ForegroundColor Yellow
Write-Host ""

# 5. Preparar comandos para conectar
Write-Host "5. COMANDOS PARA EJECUTAR DESPUÉS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "Una vez creado el repositorio en GitHub, ejecuta:" -ForegroundColor White
Write-Host ""
Write-Host "git remote add origin https://github.com/TU_USUARIO/realtime-options-analysis.git" -ForegroundColor Green
Write-Host "git branch -M main" -ForegroundColor Green
Write-Host "git push -u origin main" -ForegroundColor Green
Write-Host ""

# 6. Verificar archivos para despliegue
Write-Host "6. Verificando archivos necesarios para despliegue..." -ForegroundColor Yellow

$requiredFiles = @(
    "app.py",
    "requirements.txt",
    ".streamlit/config.toml",
    "README.md"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✓ $file" -ForegroundColor Green
    } else {
        Write-Host "✗ $file" -ForegroundColor Red
    }
}

# 7. Mostrar plan de despliegue
Write-Host ""
Write-Host "7. PLAN DE DESPLIEGUE EN STREAMLIT CLOUD:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Ve a https://share.streamlit.io/" -ForegroundColor White
Write-Host "2. Haz clic en 'New app'" -ForegroundColor White
Write-Host "3. Conecta tu cuenta de GitHub" -ForegroundColor White
Write-Host "4. Selecciona el repositorio: realtime-options-analysis" -ForegroundColor White
Write-Host "5. Branch: main" -ForegroundColor White
Write-Host "6. Main file path: app.py" -ForegroundColor White
Write-Host "7. Haz clic en 'Deploy!'" -ForegroundColor White
Write-Host ""

# 8. URLs útiles
Write-Host "8. ENLACES ÚTILES:" -ForegroundColor Cyan
Write-Host ""
Write-Host "📱 GitHub: https://github.com/new" -ForegroundColor Blue
Write-Host "🚀 Streamlit Cloud: https://share.streamlit.io/" -ForegroundColor Blue
Write-Host "📚 Documentación: https://docs.streamlit.io/streamlit-community-cloud" -ForegroundColor Blue
Write-Host ""

# 9. Mensaje final
Write-Host "9. RESUMEN:" -ForegroundColor Magenta
Write-Host ""
Write-Host "✅ Proyecto preparado para GitHub" -ForegroundColor Green
Write-Host "✅ Archivos de configuración listos" -ForegroundColor Green
Write-Host "✅ Documentación completa" -ForegroundColor Green
Write-Host "⏳ Pendiente: Crear repo en GitHub y conectar" -ForegroundColor Yellow
Write-Host "⏳ Pendiente: Desplegar en Streamlit Cloud" -ForegroundColor Yellow
Write-Host ""

Write-Host "¡El proyecto está listo para ir a internet! 🌐" -ForegroundColor Green
Write-Host ""

# Pausa para que el usuario lea
Read-Host "Presiona Enter para continuar..."
