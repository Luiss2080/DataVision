#!/usr/bin/env python3
"""
DataVision - Sistema de Verificación de Requisitos
Verifica que el sistema cumple con los requisitos mínimos para ejecutar DataVision.

Autor: Luis Alberto
Versión: 2.0.0
Fecha: Enero 2025
"""

import sys
import os
import subprocess
import platform
import importlib.util
from pathlib import Path

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_status(message, status="info"):
    """Imprime mensaje con color según el estado."""
    colors = {
        "success": Colors.GREEN + "✅ ",
        "error": Colors.RED + "❌ ",
        "warning": Colors.YELLOW + "⚠️ ",
        "info": Colors.BLUE + "ℹ️ "
    }
    print(f"{colors.get(status, '')}{message}{Colors.END}")

def print_header():
    """Imprime el encabezado del verificador."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print("🔍 DATAVISION 2025 - VERIFICADOR DE SISTEMA")
    print("   Comprobando requisitos del sistema...")
    print(f"{'='*60}{Colors.END}\n")

def check_python_version():
    """Verifica la versión de Python."""
    print_status("Verificando versión de Python...", "info")
    
    version = sys.version_info
    python_version = f"{version.major}.{version.minor}.{version.micro}"
    
    if version >= (3, 9):
        print_status(f"Python {python_version} - ✅ Compatible", "success")
        return True
    else:
        print_status(f"Python {python_version} - ❌ Requiere Python 3.9+", "error")
        print_status("Descargar Python desde: https://www.python.org/downloads/", "info")
        return False

def check_pip():
    """Verifica que pip esté disponible."""
    print_status("Verificando pip...", "info")
    
    try:
        import pip
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True, check=True)
        pip_version = result.stdout.strip()
        print_status(f"pip disponible - {pip_version}", "success")
        return True
    except (ImportError, subprocess.CalledProcessError):
        print_status("pip no encontrado", "error")
        print_status("Instalar pip: python -m ensurepip --upgrade", "info")
        return False

def check_disk_space():
    """Verifica el espacio en disco disponible."""
    print_status("Verificando espacio en disco...", "info")
    
    try:
        if platform.system() == "Windows":
            import shutil
            free_space = shutil.disk_usage('.').free
        else:
            statvfs = os.statvfs('.')
            free_space = statvfs.f_frsize * statvfs.f_bavail
        
        free_space_mb = free_space / (1024 * 1024)
        
        if free_space_mb >= 500:
            print_status(f"Espacio disponible: {free_space_mb:.0f}MB - ✅ Suficiente", "success")
            return True
        else:
            print_status(f"Espacio disponible: {free_space_mb:.0f}MB - ❌ Requiere 500MB+", "error")
            return False
    except Exception as e:
        print_status(f"Error verificando espacio: {e}", "warning")
        return False

def check_internet_connection():
    """Verifica la conexión a internet."""
    print_status("Verificando conexión a internet...", "info")
    
    try:
        import urllib.request
        urllib.request.urlopen('https://pypi.org', timeout=10)
        print_status("Conexión a internet - ✅ Disponible", "success")
        return True
    except Exception:
        print_status("Conexión a internet - ❌ No disponible", "error")
        print_status("Conexión requerida para instalar dependencias", "warning")
        return False

def check_virtual_env_support():
    """Verifica soporte para entornos virtuales."""
    print_status("Verificando soporte de entornos virtuales...", "info")
    
    try:
        import venv
        print_status("Módulo venv - ✅ Disponible", "success")
        return True
    except ImportError:
        print_status("Módulo venv - ❌ No disponible", "error")
        print_status("Instalar: sudo apt-get install python3-venv (Linux)", "info")
        return False

def check_git():
    """Verifica si Git está disponible."""
    print_status("Verificando Git (opcional)...", "info")
    
    try:
        result = subprocess.run(["git", "--version"], 
                              capture_output=True, text=True, check=True)
        git_version = result.stdout.strip()
        print_status(f"Git disponible - {git_version}", "success")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_status("Git no encontrado - ⚠️ Opcional para descargas", "warning")
        print_status("Descargar desde: https://git-scm.com/downloads", "info")
        return False

def check_required_modules():
    """Verifica módulos críticos de Python."""
    print_status("Verificando módulos críticos...", "info")
    
    critical_modules = ['json', 'csv', 'urllib', 'pathlib', 'subprocess']
    all_available = True
    
    for module in critical_modules:
        try:
            __import__(module)
            print_status(f"  {module} - ✅", "success")
        except ImportError:
            print_status(f"  {module} - ❌", "error")
            all_available = False
    
    if all_available:
        print_status("Todos los módulos críticos disponibles", "success")
    else:
        print_status("Algunos módulos críticos no están disponibles", "error")
    
    return all_available

def check_system_info():
    """Muestra información del sistema."""
    print_status("Información del sistema:", "info")
    
    system_info = {
        "Sistema Operativo": platform.system(),
        "Versión": platform.release(),
        "Arquitectura": platform.machine(),
        "Procesador": platform.processor() or "No disponible",
        "Python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "Directorio actual": os.getcwd()
    }
    
    for key, value in system_info.items():
        print(f"  {Colors.BLUE}{key}:{Colors.END} {value}")
    
    return True

def generate_report(results):
    """Genera un resumen de los resultados."""
    print(f"\n{Colors.BOLD}{'='*60}")
    print("📋 RESUMEN DE VERIFICACIÓN")
    print(f"{'='*60}{Colors.END}")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    print(f"\n{Colors.BOLD}Resultados: {passed}/{total} verificaciones pasadas{Colors.END}")
    
    for check, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        color = Colors.GREEN if result else Colors.RED
        print(f"  {color}{status}{Colors.END} - {check}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ¡Sistema listo para DataVision!{Colors.END}")
        print(f"{Colors.GREEN}Puedes proceder con la instalación.{Colors.END}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}⚠️ Resolver problemas antes de instalar{Colors.END}")
        print(f"{Colors.YELLOW}Consulta la documentación para soluciones.{Colors.END}")
    
    return passed == total

def main():
    """Función principal del verificador."""
    print_header()
    
    # Ejecutar todas las verificaciones
    checks = {
        "Versión de Python": check_python_version,
        "Pip disponible": check_pip,
        "Espacio en disco": check_disk_space,
        "Conexión a internet": check_internet_connection,
        "Soporte entornos virtuales": check_virtual_env_support,
        "Git (opcional)": check_git,
        "Módulos críticos": check_required_modules,
    }
    
    results = {}
    
    # Mostrar información del sistema
    check_system_info()
    print()
    
    # Ejecutar verificaciones
    for check_name, check_func in checks.items():
        try:
            results[check_name] = check_func()
        except Exception as e:
            print_status(f"Error en {check_name}: {e}", "error")
            results[check_name] = False
        print()
    
    # Generar reporte final
    success = generate_report(results)
    
    # Mostrar próximos pasos
    print(f"\n{Colors.BLUE}📖 Próximos pasos:{Colors.END}")
    if success:
        print("1. Ejecutar: install.bat (Windows) o ./install.sh (Linux/Mac)")
        print("2. Ejecutar: run.bat (Windows) o activar venv + streamlit run")
        print("3. Abrir: http://localhost:8501")
    else:
        print("1. Resolver los problemas marcados arriba")
        print("2. Ejecutar este verificador nuevamente")
        print("3. Consultar QUICKSTART.md para ayuda")
    
    print(f"\n{Colors.BLUE}📚 Documentación: README.md | QUICKSTART.md{Colors.END}")
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Verificación cancelada por el usuario.{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")
        sys.exit(1)