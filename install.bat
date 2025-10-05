@echo off
@echo off
cls
echo.
echo 📊 DataVision 2025 - Instalacion Automatica
echo ==========================================
echo.

REM Colores para Windows (limitados)
set "GREEN=[92m"
set "RED=[91m"  
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

REM 🔍 VERIFICACION PREVIA DEL SISTEMA
echo %BLUE%🔍 Verificando requisitos del sistema...%NC%
python check_system.py
if %ERRORLEVEL% neq 0 (
    echo %RED%❌ Verificacion fallo. Resolver problemas antes de continuar.%NC%
    echo %YELLOW%💡 Consulta QUICKSTART.md para ayuda%NC%
    pause
    exit /b 1
)

echo %GREEN%✅ Verificacion completada exitosamente%NC%
echo.
echo %BLUE%🔧 Procediendo con la instalacion...%NC%
echo ========================================================
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no esta instalado
    echo Por favor instala Python 3.9 o superior desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python detectado:
python --version

REM Verificar version de Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Version de Python: %PYTHON_VERSION%

REM Verificar si pip esta instalado
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: pip no esta instalado
    echo Por favor instala pip
    pause
    exit /b 1
)

echo ✅ pip detectado

REM Crear entorno virtual
echo.
echo 🔧 Creando entorno virtual...
if not exist "venv" (
    python -m venv venv
    echo ✅ Entorno virtual creado
) else (
    echo ⚠️  El entorno virtual ya existe
)

REM Activar entorno virtual
echo.
echo 🔄 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo.
echo 📦 Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo.
echo 📋 Instalando dependencias...
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo ✅ Dependencias instaladas correctamente
) else (
    echo ❌ ERROR: Archivo requirements.txt no encontrado
    pause
    exit /b 1
)

REM Crear directorios necesarios
echo.
echo 📁 Creando directorios necesarios...
if not exist "datos\procesados" mkdir datos\procesados
if not exist "report\excel" mkdir report\excel
if not exist "report\pdf" mkdir report\pdf
echo ✅ Directorios creados

REM Verificar instalacion
echo.
echo 🔍 Verificando instalacion...
python -c "import streamlit, pandas, plotly; print('✅ Dependencias principales verificadas')" 2>nul
if errorlevel 1 (
    echo ❌ ERROR: Error en la verificacion de dependencias
    pause
    exit /b 1
)

echo.
echo 🎉 ¡Instalacion completada exitosamente!
echo ========================================
echo.
echo 📋 Para ejecutar DataVision:
echo    1. Activa el entorno virtual: venv\Scripts\activate
echo    2. Ejecuta: streamlit run interfaz\interfaz_streamlit.py
echo    3. Abre tu navegador en: http://localhost:8501
echo.
echo 📚 Para mas informacion, consulta el README.md
echo.
echo ✅ ¡Disfruta usando DataVision 2025! 🚀
echo.
pause