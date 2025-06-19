# Instrucciones para Desplegar en Streamlit Cloud

## 🚀 Pasos para Streamlit Cloud (GRATIS)

### 1. Preparar el repositorio
```bash
# Inicializar Git en tu proyecto
git init
git add .
git commit -m "Initial commit - GGAL Options Analyzer"
```

### 2. Subir a GitHub
1. Ve a [GitHub.com](https://github.com) y crea una nueva cuenta si no tienes
2. Crea un nuevo repositorio llamado "ggal-options-analyzer"
3. Sube tu código:
```bash
git remote add origin https://github.com/TU_USUARIO/ggal-options-analyzer.git
git branch -M main
git push -u origin main
```

### 3. Desplegar en Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta con tu cuenta de GitHub
3. Selecciona tu repositorio "ggal-options-analyzer"
4. Archivo principal: `app.py`
5. ¡Despliega!

**URL resultante:** `https://TU_USUARIO-ggal-options-analyzer-app-xxxxx.streamlit.app`

---

## 🐳 Opción 2: Docker + Railway/Render

### Crear Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Desplegar en Railway
1. Ve a [railway.app](https://railway.app)
2. Conecta GitHub
3. Despliega desde repositorio
4. Variables de entorno automáticas

---

## ☁️ Opción 3: Heroku (Gratis limitado)

### Crear Procfile
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### Pasos
1. Instalar Heroku CLI
2. `heroku create ggal-options-analyzer`
3. `git push heroku main`

---

## 🌟 Recomendación

**Streamlit Cloud** es la mejor opción porque:
- ✅ Completamente gratis
- ✅ Integración directa con GitHub
- ✅ SSL automático
- ✅ Actualizaciones automáticas
- ✅ Optimizado para Streamlit
