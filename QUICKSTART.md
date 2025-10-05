# 🚀 Guía de Inicio Rápido - DataVision 2025

Esta guía te ayudará a ejecutar DataVision en cualquier computadora en menos de 5 minutos.

## 📋 Requisitos Mínimos

- 🐍 **Python 3.9+** (recomendado: Python 3.11)
- 💾 **4GB RAM** (recomendado: 8GB)
- 💽 **500MB** espacio libre
- 🌐 **Navegador web** moderno

## ⚡ Instalación Rápida

### Windows (Automática)
```batch
# 1. Descargar/clonar el proyecto
git clone https://github.com/Luiss2080/DataVision.git
cd DataVision

# 2. Ejecutar instalación automática
install.bat

# 3. Ejecutar la aplicación
run.bat
```

### Linux/Mac (Automática)
```bash
# 1. Descargar/clonar el proyecto
git clone https://github.com/Luiss2080/DataVision.git
cd DataVision

# 2. Dar permisos y ejecutar instalación
chmod +x install.sh
./install.sh

# 3. Ejecutar la aplicación
source venv/bin/activate
streamlit run interfaz/interfaz_streamlit.py
```

### Instalación Manual (Universal)
```bash
# 1. Clonar repositorio
git clone https://github.com/Luiss2080/DataVision.git
cd DataVision

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar aplicación
streamlit run interfaz/interfaz_streamlit.py
```

## 🐳 Con Docker (Recomendado para Producción)

```bash
# Opción 1: Docker Compose (Más fácil)
git clone https://github.com/Luiss2080/DataVision.git
cd DataVision
docker-compose up -d

# Opción 2: Docker manual
docker build -t datavision .
docker run -p 8501:8501 datavision
```

## 🎯 Uso Básico

### 1. **Cargar Datos**
- 📁 Arrastra tu archivo CSV/Excel al área de carga
- 🎲 O usa "Datos Demo" para probar con ejemplos
- ✅ Formatos soportados: `.csv`, `.xlsx`, `.xls`

### 2. **Explorar Análisis**
- 📊 **Vista General**: Estadísticas automáticas
- 🔗 **Correlaciones**: Matrices interactivas
- 📈 **Gráficas**: Visualizaciones personalizables
- 📋 **Exportar**: Reportes en múltiples formatos

### 3. **Personalizar**
- ⚙️ Configurar tema de colores
- 🎯 Ajustar precisión de cálculos
- 🔍 Filtrar datos por filas/columnas

## 🛠️ Solución de Problemas

### Error: "Python no encontrado"
```bash
# Verificar instalación de Python
python --version
# O en algunos sistemas:
python3 --version
```

### Error: "pip no encontrado"
```bash
# Instalar pip (Ubuntu/Debian)
sudo apt install python3-pip

# Instalar pip (CentOS/RHEL)
sudo yum install python3-pip
```

### Error: "Dependencias faltantes"
```bash
# Actualizar pip
pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt
```

### Puerto 8501 ocupado
```bash
# Usar puerto diferente
streamlit run interfaz/interfaz_streamlit.py --server.port=8502
```

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# Configurar puerto personalizado
export STREAMLIT_SERVER_PORT=8502

# Desactivar telemetría
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### Configuración Personalizada
Edita `.streamlit/config.toml` para:
- 🎨 Cambiar colores del tema
- 📊 Ajustar límites de carga
- 🔒 Configurar opciones de seguridad

## 📞 Soporte

### 🐛 Reportar Problemas
- [GitHub Issues](https://github.com/Luiss2080/DataVision/issues)
- Incluye: SO, versión Python, mensaje de error

### 📚 Documentación Completa
- [README principal](README.md)
- [Changelog](CHANGELOG.md)
- [Arquitectura del proyecto](docs/arquitectura.md)

### 💬 Comunidad
- 🐦 Twitter: [@DataVision2025](https://twitter.com/DataVision2025)
- 💼 LinkedIn: [Luis Alberto](https://linkedin.com/in/luis-alberto)

---

## ✅ Lista de Verificación

Antes de reportar problemas, verifica:

- [ ] Python 3.9+ instalado
- [ ] pip funcionando correctamente
- [ ] Entorno virtual activado
- [ ] Todas las dependencias instaladas
- [ ] Puerto 8501 libre
- [ ] Permisos de escritura en directorio

---

**🎉 ¡Listo! DataVision debería estar ejecutándose en http://localhost:8501**

*¿Problemas? Revisa la sección de solución de problemas o abre un issue en GitHub.*