"""
Módulo de validaciones
Funciones para validar datos, parámetros y configuraciones.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union, Tuple, Callable
import os
import re
from pathlib import Path


class ValidadorDatos:
    """Clase para validar diferentes aspectos de los datos y configuraciones."""
    
    def __init__(self):
        """Inicializa el validador de datos."""
        self.reglas_validacion = {}
        self.errores_encontrados = []
        self.advertencias = []
    
    def validar_dataframe(self, df: pd.DataFrame, reglas: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Valida un DataFrame según reglas específicas.
        
        Args:
            df: DataFrame a validar
            reglas: Diccionario con reglas de validación personalizadas
        
        Returns:
            Diccionario con resultados de validación
        """
        self.errores_encontrados = []
        self.advertencias = []
        
        # Validaciones básicas
        resultado = {
            'valido': True,
            'errores': [],
            'advertencias': [],
            'metricas': {}
        }
        
        # 1. Verificar que no esté vacío
        if df.empty:
            self.errores_encontrados.append("El DataFrame está vacío")
            resultado['valido'] = False
        
        # 2. Verificar estructura básica
        if len(df.columns) == 0:
            self.errores_encontrados.append("El DataFrame no tiene columnas")
            resultado['valido'] = False
        
        # 3. Validar nombres de columnas
        problemas_columnas = self._validar_nombres_columnas(df)
        if problemas_columnas:
            self.advertencias.extend(problemas_columnas)
        
        # 4. Validar tipos de datos
        problemas_tipos = self._validar_tipos_datos(df)
        if problemas_tipos:
            self.advertencias.extend(problemas_tipos)
        
        # 5. Detectar problemas de calidad
        problemas_calidad = self._detectar_problemas_calidad(df)
        if problemas_calidad:
            self.advertencias.extend(problemas_calidad)
        
        # 6. Aplicar reglas personalizadas si se proporcionan
        if reglas:
            resultados_personalizados = self._aplicar_reglas_personalizadas(df, reglas)
            self.errores_encontrados.extend(resultados_personalizados.get('errores', []))
            self.advertencias.extend(resultados_personalizados.get('advertencias', []))
            if resultados_personalizados.get('errores'):
                resultado['valido'] = False
        
        # Compilar resultados
        resultado['errores'] = self.errores_encontrados
        resultado['advertencias'] = self.advertencias
        resultado['metricas'] = self._calcular_metricas_calidad(df)
        
        return resultado
    
    def _validar_nombres_columnas(self, df: pd.DataFrame) -> List[str]:
        """Valida los nombres de las columnas."""
        problemas = []
        
        # Verificar duplicados
        columnas_duplicadas = df.columns[df.columns.duplicated()].tolist()
        if columnas_duplicadas:
            problemas.append(f"Columnas duplicadas encontradas: {columnas_duplicadas}")
        
        # Verificar caracteres problemáticos
        caracteres_problematicos = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for col in df.columns:
            if any(char in str(col) for char in caracteres_problematicos):
                problemas.append(f"Columna '{col}' contiene caracteres problemáticos")
        
        # Verificar espacios al inicio/final
        for col in df.columns:
            if str(col) != str(col).strip():
                problemas.append(f"Columna '{col}' tiene espacios al inicio o final")
        
        # Verificar nombres muy largos
        for col in df.columns:
            if len(str(col)) > 100:
                problemas.append(f"Columna '{col}' tiene un nombre muy largo (>100 caracteres)")
        
        return problemas
    
    def _validar_tipos_datos(self, df: pd.DataFrame) -> List[str]:
        """Valida los tipos de datos de las columnas."""
        problemas = []
        
        for col in df.columns:
            serie = df[col]
            
            # Verificar mixed types (object que podría ser numérico)
            if serie.dtype == 'object' and not serie.empty:
                muestra = serie.dropna().head(100)
                
                # Contar cuántos valores parecen numéricos
                numericos = 0
                for valor in muestra:
                    try:
                        float(str(valor).replace(',', '.'))
                        numericos += 1
                    except:
                        pass
                
                if numericos / len(muestra) > 0.8:
                    problemas.append(f"Columna '{col}' parece numérica pero está como texto")
            
            # Verificar fechas mal formateadas
            if serie.dtype == 'object' and not serie.empty:
                muestra_str = serie.dropna().astype(str).head(50)
                posibles_fechas = 0
                
                patron_fecha = r'\d{1,4}[-/]\d{1,2}[-/]\d{1,4}'
                for valor in muestra_str:
                    if re.search(patron_fecha, valor):
                        posibles_fechas += 1
                
                if posibles_fechas / len(muestra_str) > 0.7:
                    problemas.append(f"Columna '{col}' parece contener fechas sin formato datetime")
        
        return problemas
    
    def _detectar_problemas_calidad(self, df: pd.DataFrame) -> List[str]:
        """Detecta problemas de calidad en los datos."""
        problemas = []
        
        # Verificar alta proporción de valores nulos
        for col in df.columns:
            pct_nulos = (df[col].isnull().sum() / len(df)) * 100
            if pct_nulos > 50:
                problemas.append(f"Columna '{col}' tiene {pct_nulos:.1f}% de valores nulos")
            elif pct_nulos > 80:
                problemas.append(f"Columna '{col}' está casi vacía ({pct_nulos:.1f}% nulos)")
        
        # Verificar columnas con un solo valor único
        for col in df.columns:
            valores_unicos = df[col].nunique(dropna=True)
            if valores_unicos == 1 and len(df) > 1:
                problemas.append(f"Columna '{col}' tiene un solo valor único")
        
        # Verificar alta cardinalidad en columnas categóricas
        for col in df.select_dtypes(include=['object', 'category']).columns:
            valores_unicos = df[col].nunique(dropna=True)
            if valores_unicos > len(df) * 0.8:
                problemas.append(f"Columna '{col}' tiene muy alta cardinalidad ({valores_unicos} valores únicos)")
        
        # Verificar filas completamente vacías
        filas_vacias = df.isnull().all(axis=1).sum()
        if filas_vacias > 0:
            problemas.append(f"Encontradas {filas_vacias} filas completamente vacías")
        
        return problemas
    
    def _aplicar_reglas_personalizadas(self, df: pd.DataFrame, reglas: Dict) -> Dict:
        """Aplica reglas de validación personalizadas."""
        resultados = {'errores': [], 'advertencias': []}
        
        for nombre_regla, configuracion in reglas.items():
            try:
                if configuracion['tipo'] == 'rango_numerico':
                    columna = configuracion['columna']
                    min_val = configuracion.get('min')
                    max_val = configuracion.get('max')
                    
                    if columna in df.columns:
                        serie = pd.to_numeric(df[columna], errors='coerce')
                        
                        if min_val is not None:
                            violaciones = (serie < min_val).sum()
                            if violaciones > 0:
                                resultados['errores'].append(
                                    f"Regla '{nombre_regla}': {violaciones} valores menores que {min_val}"
                                )
                        
                        if max_val is not None:
                            violaciones = (serie > max_val).sum()
                            if violaciones > 0:
                                resultados['errores'].append(
                                    f"Regla '{nombre_regla}': {violaciones} valores mayores que {max_val}"
                                )
                
                elif configuracion['tipo'] == 'valores_permitidos':
                    columna = configuracion['columna']
                    valores_permitidos = set(configuracion['valores'])
                    
                    if columna in df.columns:
                        valores_actuales = set(df[columna].dropna().unique())
                        valores_invalidos = valores_actuales - valores_permitidos
                        
                        if valores_invalidos:
                            resultados['errores'].append(
                                f"Regla '{nombre_regla}': Valores no permitidos encontrados: {valores_invalidos}"
                            )
                
                elif configuracion['tipo'] == 'patron_regex':
                    columna = configuracion['columna']
                    patron = configuracion['patron']
                    
                    if columna in df.columns:
                        serie_str = df[columna].astype(str)
                        coincidencias = serie_str.str.match(patron, na=False)
                        violaciones = (~coincidencias).sum()
                        
                        if violaciones > 0:
                            resultados['errores'].append(
                                f"Regla '{nombre_regla}': {violaciones} valores no coinciden con el patrón"
                            )
            
            except Exception as e:
                resultados['advertencias'].append(f"Error aplicando regla '{nombre_regla}': {str(e)}")
        
        return resultados
    
    def _calcular_metricas_calidad(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calcula métricas de calidad de los datos."""
        if df.empty:
            return {}
        
        total_celdas = len(df) * len(df.columns)
        celdas_no_nulas = df.count().sum()
        
        metricas = {
            'completitud_general': (celdas_no_nulas / total_celdas) * 100,
            'filas_completas_pct': (df.dropna().shape[0] / len(df)) * 100,
            'columnas_sin_nulos_pct': ((df.columns.size - df.isnull().any().sum()) / df.columns.size) * 100,
            'duplicados_pct': (df.duplicated().sum() / len(df)) * 100,
            'consistencia_tipos': self._calcular_consistencia_tipos(df)
        }
        
        return metricas
    
    def _calcular_consistencia_tipos(self, df: pd.DataFrame) -> float:
        """Calcula un score de consistencia de tipos de datos."""
        if df.empty:
            return 100.0
        
        score = 100.0
        
        for col in df.columns:
            serie = df[col].dropna()
            
            if serie.empty:
                continue
            
            # Penalizar columnas object que podrían ser numéricas
            if serie.dtype == 'object':
                numericos = 0
                total = min(len(serie), 100)
                
                for i, valor in enumerate(serie.head(100)):
                    try:
                        float(str(valor))
                        numericos += 1
                    except:
                        pass
                
                if numericos / total > 0.8:
                    score -= 10  # Penalización por tipo inconsistente
        
        return max(0, score)


def validar_archivo_entrada(ruta_archivo: str) -> Dict[str, Any]:
    """
    Valida que un archivo sea válido para carga.
    
    Args:
        ruta_archivo: Ruta del archivo a validar
    
    Returns:
        Diccionario con resultados de validación
    """
    resultado = {
        'valido': True,
        'errores': [],
        'advertencias': [],
        'info': {}
    }
    
    # Verificar existencia
    if not os.path.exists(ruta_archivo):
        resultado['errores'].append(f"El archivo '{ruta_archivo}' no existe")
        resultado['valido'] = False
        return resultado
    
    # Verificar permisos de lectura
    if not os.access(ruta_archivo, os.R_OK):
        resultado['errores'].append(f"No hay permisos de lectura para '{ruta_archivo}'")
        resultado['valido'] = False
    
    # Información del archivo
    try:
        stats = os.stat(ruta_archivo)
        resultado['info'] = {
            'tamano_bytes': stats.st_size,
            'tamano_mb': stats.st_size / 1024 / 1024,
            'extension': Path(ruta_archivo).suffix.lower(),
            'nombre': Path(ruta_archivo).name
        }
        
        # Advertencias sobre tamaño
        if resultado['info']['tamano_mb'] > 100:
            resultado['advertencias'].append(f"Archivo grande ({resultado['info']['tamano_mb']:.1f} MB)")
        elif resultado['info']['tamano_mb'] > 500:
            resultado['advertencias'].append(f"Archivo muy grande ({resultado['info']['tamano_mb']:.1f} MB) - puede ser lento")
        
        # Verificar extensión soportada
        extensiones_soportadas = ['.csv', '.xlsx', '.xls', '.json', '.parquet', '.txt', '.tsv']
        if resultado['info']['extension'] not in extensiones_soportadas:
            resultado['advertencias'].append(f"Extensión '{resultado['info']['extension']}' no típicamente soportada")
    
    except Exception as e:
        resultado['errores'].append(f"Error accediendo al archivo: {str(e)}")
        resultado['valido'] = False
    
    return resultado


def validar_configuracion_analisis(config: Dict) -> Dict[str, Any]:
    """
    Valida una configuración de análisis.
    
    Args:
        config: Diccionario con configuración
    
    Returns:
        Diccionario con resultados de validación
    """
    resultado = {
        'valido': True,
        'errores': [],
        'advertencias': []
    }
    
    # Validar claves requeridas
    claves_requeridas = ['tipo_analisis']
    for clave in claves_requeridas:
        if clave not in config:
            resultado['errores'].append(f"Clave requerida '{clave}' no encontrada")
    
    # Validar tipos de análisis
    tipos_validos = ['estadistico', 'correlacion', 'exploratorio', 'limpieza']
    if 'tipo_analisis' in config:
        if config['tipo_analisis'] not in tipos_validos:
            resultado['errores'].append(f"Tipo de análisis '{config['tipo_analisis']}' no válido")
    
    # Validar parámetros específicos
    if 'umbral_correlacion' in config:
        umbral = config['umbral_correlacion']
        if not isinstance(umbral, (int, float)) or not (0 <= umbral <= 1):
            resultado['errores'].append("umbral_correlacion debe ser un número entre 0 y 1")
    
    # Validar configuración de exportación
    if 'exportar' in config:
        export_config = config['exportar']
        if 'formato' in export_config:
            formatos_validos = ['pdf', 'excel', 'csv']
            if export_config['formato'] not in formatos_validos:
                resultado['errores'].append(f"Formato de exportación '{export_config['formato']}' no válido")
    
    if resultado['errores']:
        resultado['valido'] = False
    
    return resultado


def validar_parametros_grafico(tipo_grafico: str, parametros: Dict) -> Dict[str, Any]:
    """
    Valida parámetros para generación de gráficos.
    
    Args:
        tipo_grafico: Tipo de gráfico a validar
        parametros: Diccionarios con parámetros
    
    Returns:
        Diccionario con resultados de validación
    """
    resultado = {
        'valido': True,
        'errores': [],
        'advertencias': []
    }
    
    # Validar tipo de gráfico
    tipos_validos = ['histograma', 'boxplot', 'scatter', 'barras', 'lineas', 'correlacion']
    if tipo_grafico not in tipos_validos:
        resultado['errores'].append(f"Tipo de gráfico '{tipo_grafico}' no válido")
        resultado['valido'] = False
        return resultado
    
    # Validaciones específicas por tipo
    if tipo_grafico == 'scatter':
        if 'x' not in parametros or 'y' not in parametros:
            resultado['errores'].append("Gráfico scatter requiere parámetros 'x' y 'y'")
    
    elif tipo_grafico in ['histograma', 'boxplot']:
        if 'columna' not in parametros:
            resultado['errores'].append(f"Gráfico {tipo_grafico} requiere parámetro 'columna'")
    
    elif tipo_grafico == 'barras':
        if 'x' not in parametros:
            resultado['errores'].append("Gráfico de barras requiere parámetro 'x'")
    
    # Validar nombres de columnas si se proporcionan
    columnas_parametros = ['x', 'y', 'color', 'size', 'columna']
    for param in columnas_parametros:
        if param in parametros:
            valor = parametros[param]
            if not isinstance(valor, str) or len(valor.strip()) == 0:
                resultado['advertencias'].append(f"Parámetro '{param}' debe ser un nombre de columna válido")
    
    if resultado['errores']:
        resultado['valido'] = False
    
    return resultado


def sanitizar_nombre_archivo(nombre: str) -> str:
    """
    Sanitiza un nombre de archivo removiendo caracteres problemáticos.
    
    Args:
        nombre: Nombre original del archivo
    
    Returns:
        Nombre sanitizado
    """
    # Caracteres no permitidos en nombres de archivo
    caracteres_invalidos = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    
    nombre_limpio = nombre
    for char in caracteres_invalidos:
        nombre_limpio = nombre_limpio.replace(char, '_')
    
    # Remover espacios múltiples y al inicio/final
    nombre_limpio = re.sub(r'\s+', ' ', nombre_limpio.strip())
    
    # Limitar longitud
    if len(nombre_limpio) > 200:
        nombre_limpio = nombre_limpio[:200]
    
    return nombre_limpio


def validar_memoria_disponible(df: pd.DataFrame, operacion: str = 'general') -> Dict[str, Any]:
    """
    Valida si hay suficiente memoria para una operación.
    
    Args:
        df: DataFrame a procesar
        operacion: Tipo de operación a realizar
    
    Returns:
        Diccionario con información de memoria
    """
    import psutil
    
    # Memoria del DataFrame
    memoria_df = df.memory_usage(deep=True).sum() / 1024**2  # MB
    
    # Memoria disponible del sistema
    memoria_disponible = psutil.virtual_memory().available / 1024**2  # MB
    
    # Factores de multiplicación por tipo de operación
    factores_operacion = {
        'general': 2,
        'correlacion': 3,
        'limpieza': 2.5,
        'graficos': 1.5,
        'exportacion': 2
    }
    
    factor = factores_operacion.get(operacion, 2)
    memoria_requerida = memoria_df * factor
    
    resultado = {
        'memoria_df_mb': memoria_df,
        'memoria_disponible_mb': memoria_disponible,
        'memoria_requerida_mb': memoria_requerida,
        'suficiente': memoria_disponible > memoria_requerida,
        'porcentaje_uso': (memoria_requerida / memoria_disponible) * 100
    }
    
    return resultado