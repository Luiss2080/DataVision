#!/bin/bash

# 🚀 DataVision 2025 - Script de Instalación Automática
# Este script instala y configura DataVision automáticamente

echo "📊 Iniciando instalación de DataVision 2025..."
echo "============================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con color
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# 🔍 VERIFICACIÓN PREVIA DEL SISTEMA
echo -e "${BLUE}🔍 Verificando requisitos del sistema...${NC}"
if python3 check_system.py; then
    echo -e "${GREEN}✅ Verificación completada exitosamente${NC}"
else
    echo -e "${RED}❌ Verificación falló. Resolver problemas antes de continuar.${NC}"
    echo -e "${YELLOW}💡 Consulta QUICKSTART.md para ayuda${NC}"
    exit 1
fi

echo -e "\n${BLUE}🔧 Procediendo con la instalación...${NC}"

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si Python está instalado
print_status "Verificando instalación de Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python $PYTHON_VERSION detectado"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    print_success "Python $PYTHON_VERSION detectado"
    PYTHON_CMD="python"
else
    print_error "Python no está instalado. Por favor instala Python 3.9 o superior."
    exit 1
fi

# Verificar versión de Python
PYTHON_VERSION_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_VERSION_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_VERSION_MAJOR" -lt 3 ] || ([ "$PYTHON_VERSION_MAJOR" -eq 3 ] && [ "$PYTHON_VERSION_MINOR" -lt 9 ]); then
    print_error "Se requiere Python 3.9 o superior. Versión actual: $PYTHON_VERSION"
    exit 1
fi

print_success "Versión de Python compatible: $PYTHON_VERSION"

# Verificar si pip está instalado
print_status "Verificando instalación de pip..."
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    print_error "pip no está instalado. Por favor instala pip."
    exit 1
fi

print_success "pip detectado"

# Crear entorno virtual
print_status "Creando entorno virtual..."
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    print_success "Entorno virtual creado"
else
    print_warning "El entorno virtual ya existe"
fi

# Activar entorno virtual
print_status "Activando entorno virtual..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    print_success "Entorno virtual activado (Linux/Mac)"
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
    print_success "Entorno virtual activado (Windows Git Bash)"
else
    print_warning "No se pudo activar el entorno virtual automáticamente"
    print_warning "Actívalo manualmente con: source venv/bin/activate (Linux/Mac) o venv\\Scripts\\activate (Windows)"
fi

# Actualizar pip
print_status "Actualizando pip..."
$PIP_CMD install --upgrade pip

# Instalar dependencias
print_status "Instalando dependencias..."
if [ -f "requirements.txt" ]; then
    $PIP_CMD install -r requirements.txt
    print_success "Dependencias instaladas correctamente"
else
    print_error "Archivo requirements.txt no encontrado"
    exit 1
fi

# Crear directorios necesarios
print_status "Creando directorios necesarios..."
mkdir -p datos/procesados
mkdir -p report/excel
mkdir -p report/pdf
print_success "Directorios creados"

# Verificar instalación
print_status "Verificando instalación..."
if $PYTHON_CMD -c "import streamlit, pandas, plotly; print('✅ Dependencias principales verificadas')" 2>/dev/null; then
    print_success "Instalación verificada correctamente"
else
    print_error "Error en la verificación de dependencias"
    exit 1
fi

echo ""
echo "🎉 ¡Instalación completada exitosamente!"
echo "============================================="
echo ""
echo "📋 Para ejecutar DataVision:"
echo "   1. Activa el entorno virtual:"
echo "      • Linux/Mac: source venv/bin/activate"
echo "      • Windows: venv\\Scripts\\activate"
echo ""
echo "   2. Ejecuta la aplicación:"
echo "      streamlit run interfaz/interfaz_streamlit.py"
echo ""
echo "   3. Abre tu navegador en: http://localhost:8501"
echo ""
echo "📚 Para más información, consulta el README.md"
echo ""
print_success "¡Disfruta usando DataVision 2025! 🚀"