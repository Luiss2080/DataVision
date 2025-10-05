# DataVision 2025 - Dockerfile
FROM python:3.11-slim

# Información del mantenedor
LABEL maintainer="Luis Alberto <contacto@datavision.com>"
LABEL description="DataVision 2025 - Plataforma de Análisis de Datos Inteligente"
LABEL version="2.0.1"

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero para aprovechar cache de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p datos/procesados report/excel report/pdf

# Exponer el puerto de Streamlit
EXPOSE 8501

# Variables de entorno
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Comando de salud para verificar que la aplicación esté funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "interfaz/interfaz_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]