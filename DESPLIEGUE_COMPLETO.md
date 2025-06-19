# 🚀 Guía Paso a Paso para Exponer tu App en Internet

## 📋 Preparación Completada ✅

Tu aplicación ya está lista para ser desplegada. Los archivos creados incluyen:

- ✅ `Dockerfile` - Para contenedores Docker
- ✅ `Procfile` - Para Heroku
- ✅ `.streamlit/config.toml` - Configuración de Streamlit
- ✅ `.gitignore` - Archivos a ignorar en Git
- ✅ Repositorio Git inicializado

## 🌐 Opción 1: Streamlit Cloud (RECOMENDADO - GRATIS)

### Paso 1: Subir a GitHub
1. Ve a [GitHub.com](https://github.com)
2. Crea una cuenta si no tienes
3. Crea un nuevo repositorio público llamado `ggal-options-analyzer`
4. Ejecuta estos comandos:

```bash
git remote add origin https://github.com/TU_USUARIO/ggal-options-analyzer.git
git branch -M main
git push -u origin main
```

### Paso 2: Desplegar en Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Haz clic en "Sign in with GitHub"
3. Autoriza Streamlit Cloud
4. Haz clic en "New app"
5. Selecciona tu repositorio `ggal-options-analyzer`
6. Main file path: `app.py`
7. Haz clic en "Deploy!"

**Tu app estará disponible en:** `https://TU_USUARIO-ggal-options-analyzer-app-xxxxx.streamlit.app`

---

## ☁️ Opción 2: Railway (FÁCIL)

1. Ve a [railway.app](https://railway.app)
2. Crea una cuenta con GitHub
3. Haz clic en "New Project"
4. Selecciona "Deploy from GitHub repo"
5. Selecciona tu repositorio
6. Railway detectará automáticamente que es una app Python
7. ¡Despliega automáticamente!

---

## 🐳 Opción 3: Render (GRATIS)

1. Ve a [render.com](https://render.com)
2. Crea una cuenta con GitHub
3. Haz clic en "New +"
4. Selecciona "Web Service"
5. Conecta tu repositorio
6. Configuración:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

---

## ⚡ Opción 4: Heroku

1. Instala [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Ejecuta:
```bash
heroku login
heroku create ggal-options-analyzer
git push heroku main
```

---

## 🔧 Configuraciones Adicionales

### Variables de Entorno (Opcional)
Si quieres configurar parámetros específicos:

```bash
# Para Railway/Heroku
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Dominio Personalizado (Opcional)
- **Streamlit Cloud**: Solo con plan premium
- **Railway**: Dominio personalizado gratis
- **Render**: Dominio personalizado disponible
- **Heroku**: Requiere verificación con tarjeta

---

## 🚀 ¡Listo para Desplegar!

Tu aplicación incluye:
- 📊 Dashboard en tiempo real
- 🎯 Análisis de estrategias de opciones
- ⚠️ Gestión de riesgo
- 📈 Análisis técnico
- 📋 Cadena de opciones

**Próximos pasos:**
1. Elige una plataforma (recomiendo Streamlit Cloud)
2. Sube tu código a GitHub
3. Despliega siguiendo los pasos
4. ¡Comparte tu URL con el mundo!

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs de despliegue
2. Verifica que todas las dependencias estén en `requirements.txt`
3. Asegúrate de que `app.py` sea el archivo principal

¡Tu aplicación de análisis de opciones GGAL estará disponible 24/7 en internet! 🌐
