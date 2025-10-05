# 📊 DataVision - Analizador de Datos Interactivo

Una herramienta completa y fácil de usar para análisis exploratorio de datos, desarrollada con Python y Streamlit.

## ✨ Características Principales

- **🔄 Carga Flexible de Datos**: Compatible con CSV y Excel, con auto-detección de encoding
- **📈 Análisis Estadístico Completo**: Estadísticas descriptivas, distribuciones y detección de outliers
- **🔗 Análisis de Correlaciones**: Matrices de correlación interactivas con mapas de calor
- **🧹 Limpieza Automática**: Detección y corrección de problemas de calidad de datos
- **📊 Visualizaciones Interactivas**: Gráficos dinámicos con matplotlib y seaborn
- **🎯 Interfaz Intuitiva**: Diseño simple y funcional basado en Streamlit
- **⚡ Procesamiento Rápido**: Optimizado para datasets de tamaño medio

## 🚀 Instalación Rápida

### 1. Clonar o descargar el proyecto
```bash
# Si tienes git instalado
git clone https://github.com/tu-usuario/DataVision.git
cd DataVision

# O simplemente descarga y descomprime el ZIP
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación
```bash
python main.py
```

¡Eso es todo! La aplicación se abrirá automáticamente en tu navegador.

## 📁 Estructura del Proyecto

```
DataVision/
├── 📄 main.py                    # Punto de entrada principal
├── 📄 requirements.txt           # Dependencias del proyecto
├── 📂 src/                       # Módulos de análisis de datos
│   ├── 📂 analisis/              # Funciones de análisis estadístico
│   ├── 📂 visualizacion/         # Generación de gráficos
│   ├── 📂 exportacion/           # Exportación de reportes
│   └── 📂 utilidades/            # Utilidades y validaciones
├── 📂 interfaz/                  # Interfaces de usuario
│   └── 📄 interfaz_streamlit.py  # Interfaz web principal
├── 📂 static/                    # Archivos estáticos
│   ├── 📂 css/                   # Estilos personalizados
│   └── 📂 js/                    # Scripts de JavaScript
├── 📂 datos/                     # Datasets
│   └── 📂 ejemplos/              # Datos de ejemplo incluidos
├── 📂 reportes/                  # Reportes generados
│   ├── 📂 pdf/                   # Reportes en PDF
│   └── 📂 excel/                 # Reportes en Excel
└── 📂 documentacion/             # Documentación adicional
```

## 🎯 Guía de Uso

### 1. Cargar Datos

**Opción A: Datos de Ejemplo**
- Haz clic en "📊 Usar datos de ejemplo" en la barra lateral
- Se cargarán automáticamente datos simulados para probar todas las funciones

**Opción B: Subir tu Archivo**
- Usa el selector "Cargar archivo CSV/Excel"
- Formatos soportados: `.csv`, `.xlsx`, `.xls`
- La aplicación detecta automáticamente el encoding y separadores

### 2. Explorar los Análisis

#### 📊 Vista General
- **Métricas del Dataset**: Filas, columnas, memoria utilizada
- **Vista Previa**: Primeras filas de tus datos
- **Información de Columnas**: Tipos de datos, valores únicos, nulos

#### 📈 Estadísticas
- **Estadísticas Descriptivas**: Media, mediana, desviación estándar, cuartiles
- **Análisis por Columna**: Estadísticas detalladas y gráficos de distribución
- **Detección de Outliers**: Identificación automática usando método IQR

#### 🔗 Correlaciones
- **Matriz de Correlación**: Mapa de calor interactivo
- **Correlaciones Significativas**: Lista filtrable por umbral
- **Interpretación**: Clasificación automática (fuerte, moderada, débil)

#### 🧹 Limpieza de Datos
- **Diagnóstico de Calidad**: Detección de valores nulos y duplicados
- **Limpieza Automática**: Eliminación de duplicados y tratamiento de nulos
- **Tratamiento Personalizado**: Opciones específicas por columna

### 3. Datos de Ejemplo Incluidos

El proyecto incluye datasets de ejemplo listos para usar:

#### 👥 Empleados (empleados.csv)
- 30 registros de empleados ficticios
- Variables: nombre, edad, salario, experiencia, departamento, ciudad, género, educación, puntuación
- Perfecto para análisis de recursos humanos

#### 🛍️ Ventas (ventas.csv)
- 30 transacciones de ventas
- Variables: fecha, producto, categoría, precio, cantidad, ingresos, región, vendedor
- Ideal para análisis de rendimiento comercial

## 🔧 Comandos Disponibles

```bash
# Ejecutar la aplicación (modo por defecto)
python main.py

# Mostrar información del proyecto
python main.py --info

# Verificar dependencias instaladas
python main.py --check

# Mostrar ayuda
python main.py --help

# Mostrar versión
python main.py --version
```

## 📋 Dependencias

- **streamlit** >= 1.28.0 - Framework web para la interfaz
- **pandas** >= 2.1.0 - Manipulación y análisis de datos
- **numpy** >= 1.24.0 - Computación numérica
- **matplotlib** >= 3.7.0 - Visualizaciones básicas
- **seaborn** >= 0.12.0 - Visualizaciones estadísticas avanzadas

## 🛠️ Funcionalidades Técnicas

### Carga de Datos Robusta
- Auto-detección de encoding (UTF-8, Latin-1, ISO-8859-1, CP1252)
- Manejo de errores de codificación
- Soporte para diferentes separadores CSV
- Validación automática de archivos

### Análisis Estadístico
- Estadísticas descriptivas completas
- Detección de outliers usando método IQR
- Análisis de distribución por tipo de variable
- Correlaciones con múltiples métodos (Pearson, Spearman, Kendall)

### Visualizaciones
- Histogramas automáticos para variables numéricas
- Gráficos de barras para variables categóricas
- Mapas de calor para matrices de correlación
- Personalización automática según tipo de datos

### Limpieza de Datos
- Detección automática de problemas de calidad
- Eliminación inteligente de duplicados
- Múltiples estrategias para valores nulos (media, mediana, moda)
- Preservación de datos originales

## 🚨 Solución de Problemas

### Error: "Streamlit no está instalado"
```bash
pip install streamlit>=1.28.0
```

### Error: "No se puede cargar el archivo"
- Verifica que el archivo sea CSV o Excel válido
- Revisa la codificación del archivo (se recomienda UTF-8)
- Asegúrate de que el archivo no esté corrupto

### Error: "No hay columnas numéricas"
- El análisis de correlaciones requiere al menos 2 columnas numéricas
- Verifica que tus datos tengan el formato correcto
- Revisa los tipos de datos en la pestaña "Vista General"

### Rendimiento lento
- Para archivos muy grandes (>100MB), considera usar una muestra
- Cierra otras aplicaciones que consuman memoria
- Actualiza a la última versión de pandas y numpy

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar DataVision:

1. 🍴 Haz fork del proyecto
2. 🌿 Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. 📝 Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. 📤 Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. 🎯 Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 📞 Soporte

Si necesitas ayuda o encuentras algún problema:

1. 📚 Consulta esta documentación
2. 🔍 Revisa la sección de solución de problemas
3. 🐛 Reporta bugs en el sistema de issues
4. 💡 Sugiere mejoras en las discusiones del proyecto

---

**Desarrollado con ❤️ usando Python y Streamlit**

¡Disfruta analizando tus datos con DataVision! 🚀📊