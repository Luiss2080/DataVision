@echo off
title DataVision 2025 - Ejecutar Aplicacion

echo 🚀 DataVision 2025 - Iniciando aplicacion...
echo =============================================
echo.

REM Verificar si el entorno virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo ❌ ERROR: Entorno virtual no encontrado
    echo Por favor ejecuta install.bat primero
    pause
    exit /b 1
)

REM Activar entorno virtual
echo 🔄 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar si streamlit esta instalado
streamlit --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Streamlit no esta instalado
    echo Por favor ejecuta install.bat primero
    pause
    exit /b 1
)

REM Verificar si el archivo principal existe
if not exist "interfaz\interfaz_streamlit.py" (
    echo ❌ ERROR: interfaz\interfaz_streamlit.py no encontrado
    pause
    exit /b 1
)

echo ✅ Iniciando DataVision 2025...
echo.
echo 💡 TIP: La aplicacion se abrira automaticamente en tu navegador
echo 📍 URL: http://localhost:8501
echo.
echo 🛑 Para detener la aplicacion, presiona Ctrl+C
echo.

REM Ejecutar la aplicacion
streamlit run interfaz\interfaz_streamlit.py

echo.
echo 👋 DataVision cerrado. ¡Gracias por usar nuestra aplicacion!
pause