"""
DataVision - Analizador de Datos Interactivo
Archivo principal del proyecto

Uso:
    python main.py                  # Ejecutar interfaz Streamlit
    python main.py --help           # Mostrar ayuda
    python main.py --version        # Mostrar versión
"""

import sys
import os
import argparse
from pathlib import Path

# Agregar el directorio del proyecto al path de Python
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def ejecutar_streamlit():
    """Ejecuta la aplicación Streamlit."""
    try:
        import subprocess
        import streamlit.web.cli as stcli
        
        # Ruta al archivo de la interfaz
        interfaz_path = PROJECT_ROOT / "interfaz" / "interfaz_streamlit.py"
        
        if not interfaz_path.exists():
            print("❌ Error: No se encontró el archivo de la interfaz")
            print(f"Buscando en: {interfaz_path}")
            return False
        
        print("🚀 Iniciando DataVision...")
        print("📊 Abriendo navegador automáticamente...")
        print("💡 Presiona Ctrl+C para detener el servidor")
        print("-" * 50)
        
        # Ejecutar Streamlit
        sys.argv = [
            "streamlit", 
            "run", 
            str(interfaz_path),
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false"
        ]
        
        stcli.main()
        return True
        
    except ImportError:
        print("❌ Error: Streamlit no está instalado")
        print("💡 Instala las dependencias con: pip install -r requirements.txt")
        return False
    except KeyboardInterrupt:
        print("\n👋 Cerrando DataVision...")
        return True
    except Exception as e:
        print(f"❌ Error al ejecutar la aplicación: {str(e)}")
        return False


def mostrar_informacion_proyecto():
    """Muestra información del proyecto."""
    print("""
📊 DataVision - Analizador de Datos Interactivo
=============================================

Versión: 1.0.0
Autor: Proyecto DataVision
Descripción: Herramienta completa para análisis exploratorio de datos

Estructura del proyecto:
├── src/               # Módulos de análisis de datos
├── interfaz/          # Interfaces de usuario
├── static/           # Archivos CSS y JavaScript
├── datos/            # Datasets de ejemplo y cargados
├── reportes/         # Reportes generados
├── tests/            # Pruebas unitarias
└── documentacion/    # Documentación del proyecto

Características principales:
✅ Carga de archivos CSV y Excel
✅ Análisis estadístico completo
✅ Visualizaciones interactivas
✅ Detección de outliers
✅ Análisis de correlaciones
✅ Limpieza automática de datos
✅ Generación de reportes
✅ Interfaz web intuitiva

Para más información, consulta la documentación en /documentacion/
    """)


def mostrar_ayuda():
    """Muestra la ayuda del programa."""
    print("""
📊 DataVision - Analizador de Datos Interactivo

Uso:
    python main.py [opciones]

Opciones:
    (sin argumentos)    Ejecutar la interfaz web de Streamlit
    --help, -h         Mostrar esta ayuda
    --version, -v      Mostrar versión del proyecto
    --info, -i         Mostrar información del proyecto
    --check, -c        Verificar dependencias

Ejemplos:
    python main.py                 # Iniciar la aplicación web
    python main.py --info          # Ver información del proyecto
    python main.py --check         # Verificar si las dependencias están instaladas

Dependencias necesarias:
    - streamlit>=1.28.0
    - pandas>=2.1.0
    - numpy>=1.24.0
    - matplotlib>=3.7.0
    - seaborn>=0.12.0

Instalar dependencias:
    pip install -r requirements.txt
    """)


def verificar_dependencias():
    """Verifica si las dependencias están instaladas."""
    dependencias = {
        'streamlit': '1.28.0',
        'pandas': '2.1.0',
        'numpy': '1.24.0',
        'matplotlib': '3.7.0',
        'seaborn': '0.12.0'
    }
    
    print("🔍 Verificando dependencias...\n")
    
    todas_ok = True
    
    for paquete, version_min in dependencias.items():
        try:
            __import__(paquete)
            print(f"✅ {paquete} - Instalado")
        except ImportError:
            print(f"❌ {paquete} - NO instalado (requerido: >={version_min})")
            todas_ok = False
    
    print("\n" + "="*50)
    
    if todas_ok:
        print("🎉 Todas las dependencias están instaladas correctamente!")
        print("💡 Puedes ejecutar la aplicación con: python main.py")
    else:
        print("⚠️  Faltan algunas dependencias.")
        print("💡 Instálalas con: pip install -r requirements.txt")
    
    return todas_ok


def main():
    """Función principal del programa."""
    parser = argparse.ArgumentParser(
        description='DataVision - Analizador de Datos Interactivo',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='DataVision 1.0.0'
    )
    
    parser.add_argument(
        '--info', '-i',
        action='store_true',
        help='Mostrar información del proyecto'
    )
    
    parser.add_argument(
        '--check', '-c',
        action='store_true',
        help='Verificar dependencias'
    )
    
    # Si no hay argumentos, ejecutar la aplicación
    if len(sys.argv) == 1:
        ejecutar_streamlit()
        return
    
    args = parser.parse_args()
    
    if args.info:
        mostrar_informacion_proyecto()
    elif args.check:
        verificar_dependencias()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Programa interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        sys.exit(1)