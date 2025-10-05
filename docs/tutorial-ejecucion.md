# 🚀 Tutorial de Ejecución - DataVision

Guía completa para instalar y ejecutar el proyecto DataVision en Windows.

## 📋 Prerrequisitos

- **Python 3.7+** instalado en el sistema
- **pip** (gestor de paquetes de Python)
- **PowerShell** o **CMD** (terminal de Windows)

### Verificar instalación de Python
```powershell
python --version
pip --version
```

## 🏃‍♂️ Ejecución Rápida

### 1. **Navegar al directorio del proyecto**
```powershell
cd c:\xampp\htdocs\DataVision
```

### 2. **Instalar dependencias (solo primera vez)**
```powershell
pip install -r requirements.txt
```

### 3. **Ejecutar la aplicación**
```powershell
python main.py
```

¡Listo! La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📚 Guía Detallada

### Opciones de instalación de dependencias

#### Opción A: Instalación Completa
```powershell
pip install -r requirements.txt
```
**Incluye:** Todas las funcionalidades (exportación PDF, validaciones avanzadas, testing)

#### Opción B: Instalación Básica
```powershell
pip install -r requirements_simple.txt
```
**Incluye:** Solo las dependencias esenciales para análisis básico

### Métodos de ejecución

#### Método 1: Usando main.py (Recomendado)
```powershell
python main.py
```
**Ventajas:**
- Configuración automática
- Validaciones iniciales
- Mensajes informativos
- Puerto predeterminado (8501)

#### Método 2: Streamlit directo
```powershell
streamlit run interfaz\interfaz_streamlit.py
```
**Ventajas:**
- Ejecución directa
- Más opciones de configuración

#### Método 3: Con configuración personalizada
```powershell
streamlit run interfaz\interfaz_streamlit.py --server.port=8502 --server.address=0.0.0.0
```

### Comandos adicionales

#### Ver información del proyecto
```powershell
# Ver versión
python main.py --version

# Ver ayuda
python main.py --help
```

#### Gestión de la aplicación
```powershell
# Detener la aplicación
# Presionar Ctrl+C en la terminal

# Verificar que el puerto esté libre
netstat -an | findstr :8501
```

## 🔧 Solución de Problemas

### Error: "python no se reconoce como comando"
```powershell
# Verificar que Python esté en el PATH
where python

# Si no está instalado, descargar desde python.org
```

### Error: "No module named 'streamlit'"
```powershell
# Instalar dependencias
pip install -r requirements.txt

# O instalar Streamlit manualmente
pip install streamlit
```

### Error: "Puerto ya en uso"
```powershell
# Usar un puerto diferente
streamlit run interfaz\interfaz_streamlit.py --server.port=8502

# O cerrar aplicaciones que usen el puerto 8501
```

### Error: "Permission denied" o permisos
```powershell
# Ejecutar PowerShell como administrador
# O cambiar la política de ejecución
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problemas con encoding de archivos CSV
- El proyecto incluye auto-detección de encoding
- Archivos de ejemplo disponibles en `datos/ejemplos/`

## 📁 Estructura de Archivos

```
DataVision/
├── 📄 main.py                    # ← Archivo principal para ejecutar
├── 📄 requirements.txt           # ← Dependencias completas
├── 📄 requirements_simple.txt    # ← Dependencias básicas
├── 📂 interfaz/
│   └── 📄 interfaz_streamlit.py  # ← Interfaz web
├── 📂 datos/
│   └── 📂 ejemplos/              # ← Archivos CSV de prueba
├── 📂 src/                       # ← Módulos del proyecto
└── 📂 docs/                      # ← Documentación
```

## 🌐 Acceso a la Aplicación

### URL local
- **Dirección principal:** http://localhost:8501
- **Red local:** http://[tu-ip]:8501 (si configuras server.address=0.0.0.0)

### Funcionalidades disponibles
- ✅ Carga de archivos CSV y Excel
- ✅ Análisis estadístico descriptivo
- ✅ Visualizaciones interactivas
- ✅ Matrices de correlación
- ✅ Limpieza automática de datos
- ✅ Exportación de reportes (con instalación completa)

## 🎯 Datos de Prueba

El proyecto incluye archivos de ejemplo:
```
datos/ejemplos/
├── empleados.csv
└── ventas.csv
```

Úsalos para probar la funcionalidad sin necesidad de tus propios datos.

## 📞 Comandos de Mantenimiento

### Actualizar dependencias
```powershell
pip install --upgrade -r requirements.txt
```

### Verificar dependencias
```powershell
pip list
```

### Limpiar caché de Python
```powershell
# Eliminar archivos __pycache__
Get-ChildItem -Path . -Recurse -Name "__pycache__" | Remove-Item -Recurse -Force
```

## 💡 Tips y Recomendaciones

1. **Primera ejecución:** Usa `requirements_simple.txt` para una instalación más rápida
2. **Desarrollo:** Usa `requirements.txt` para todas las funcionalidades
3. **Rendimiento:** Cierra otras aplicaciones que consuman mucha memoria
4. **Archivos grandes:** El sistema está optimizado para datasets de tamaño medio
5. **Navegador:** Funciona mejor en Chrome, Firefox o Edge

## 🆘 Obtener Ayuda

Si tienes problemas:

1. **Revisa los mensajes de error** en la terminal
2. **Verifica las dependencias** con `pip list`
3. **Prueba con los datos de ejemplo** primero
4. **Reinicia la aplicación** con Ctrl+C y vuelve a ejecutar
5. **Consulta los logs** en la interfaz de Streamlit

---

**Fecha de creación:** 4 de octubre de 2025  
**Proyecto:** DataVision - Analizador de Datos Interactivo  
**Versión:** 1.0