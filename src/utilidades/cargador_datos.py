"""
Módulo de carga de datos
Funciones para cargar y leer diferentes formatos de archivos de datos.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union, Tuple
import os
import chardet
import json
from pathlib import Path


class CargadorDatos:
    """Clase principal para cargar datos desde diferentes fuentes."""
    
    def __init__(self):
        """Inicializa el cargador de datos."""
        self.formatos_soportados = {
            '.csv': self._cargar_csv,
            '.xlsx': self._cargar_excel,
            '.xls': self._cargar_excel,
            '.json': self._cargar_json,
            '.parquet': self._cargar_parquet,
            '.txt': self._cargar_texto,
            '.tsv': self._cargar_tsv
        }
        
        self.ultimo_archivo = None
        self.ultimo_dataframe = None
        self.metadatos = {}
    
    def detectar_encoding(self, ruta_archivo: str) -> str:
        """
        Detecta automáticamente la codificación de un archivo de texto.
        
        Args:
            ruta_archivo: Ruta del archivo
        
        Returns:
            Codificación detectada
        """
        try:
            with open(ruta_archivo, 'rb') as archivo:
                raw_data = archivo.read(10000)  # Leer primeros 10KB
                resultado = chardet.detect(raw_data)
                encoding = resultado['encoding']
                
                # Mapear algunas codificaciones comunes
                if encoding and encoding.lower() in ['ascii']:
                    encoding = 'utf-8'
                elif encoding and 'iso' in encoding.lower():
                    encoding = 'latin-1'
                
                return encoding or 'utf-8'
        except Exception:
            return 'utf-8'  # Fallback por defecto
    
    def detectar_separador_csv(self, ruta_archivo: str, encoding: str = 'utf-8') -> str:
        """
        Detecta automáticamente el separador de un archivo CSV.
        
        Args:
            ruta_archivo: Ruta del archivo CSV
            encoding: Codificación del archivo
        
        Returns:
            Separador detectado
        """
        separadores_comunes = [',', ';', '\t', '|']
        
        try:
            with open(ruta_archivo, 'r', encoding=encoding) as archivo:
                primera_linea = archivo.readline()
                
                # Contar ocurrencias de cada separador
                conteos = {}
                for sep in separadores_comunes:
                    conteos[sep] = primera_linea.count(sep)
                
                # Devolver el separador más común
                separador_detectado = max(conteos, key=conteos.get)
                
                # Validar que el separador tenga sentido
                if conteos[separador_detectado] == 0:
                    return ','  # Default a coma
                
                return separador_detectado
        except Exception:
            return ','  # Fallback por defecto
    
    def _cargar_csv(self, ruta_archivo: str, **kwargs) -> pd.DataFrame:
        """Carga un archivo CSV con detección automática de parámetros."""
        # Detectar encoding si no se proporciona
        encoding = kwargs.get('encoding', self.detectar_encoding(ruta_archivo))
        
        # Detectar separador si no se proporciona
        separador = kwargs.get('sep', self.detectar_separador_csv(ruta_archivo, encoding))
        
        # Parámetros por defecto
        parametros_default = {
            'encoding': encoding,
            'sep': separador,
            'low_memory': False,
            'na_values': ['', 'NA', 'N/A', 'null', 'NULL', 'None', '#N/A', '#DIV/0!'],
        }
        
        # Combinar con parámetros proporcionados
        parametros_final = {**parametros_default, **kwargs}
        
        try:
            df = pd.read_csv(ruta_archivo, **parametros_final)
            
            # Guardar metadatos
            self.metadatos.update({
                'formato': 'CSV',
                'encoding_detectado': encoding,
                'separador_detectado': separador,
                'filas': len(df),
                'columnas': len(df.columns)
            })
            
            return df
            
        except UnicodeDecodeError:
            # Intentar con diferentes encodings
            encodings_alternativos = ['latin-1', 'cp1252', 'iso-8859-1']
            
            for enc in encodings_alternativos:
                try:
                    parametros_final['encoding'] = enc
                    df = pd.read_csv(ruta_archivo, **parametros_final)
                    self.metadatos['encoding_detectado'] = enc
                    return df
                except:
                    continue
            
            raise ValueError(f"No se pudo leer el archivo con ninguna codificación probada")
    
    def _cargar_excel(self, ruta_archivo: str, **kwargs) -> pd.DataFrame:
        """Carga un archivo Excel (.xlsx o .xls)."""
        parametros_default = {
            'na_values': ['', 'NA', 'N/A', 'null', 'NULL', 'None', '#N/A', '#DIV/0!'],
        }
        
        parametros_final = {**parametros_default, **kwargs}
        
        try:
            # Detectar hojas disponibles
            hojas_excel = pd.ExcelFile(ruta_archivo)
            nombres_hojas = hojas_excel.sheet_names
            
            # Si no se especifica hoja, usar la primera
            if 'sheet_name' not in parametros_final:
                parametros_final['sheet_name'] = nombres_hojas[0]
            
            df = pd.read_excel(ruta_archivo, **parametros_final)
            
            # Guardar metadatos
            self.metadatos.update({
                'formato': 'Excel',
                'hojas_disponibles': nombres_hojas,
                'hoja_cargada': parametros_final['sheet_name'],
                'filas': len(df),
                'columnas': len(df.columns)
            })
            
            return df
            
        except Exception as e:
            raise ValueError(f"Error al leer archivo Excel: {str(e)}")
    
    def _cargar_json(self, ruta_archivo: str, **kwargs) -> pd.DataFrame:
        """Carga un archivo JSON."""
        encoding = kwargs.get('encoding', 'utf-8')
        
        try:
            with open(ruta_archivo, 'r', encoding=encoding) as archivo:
                datos_json = json.load(archivo)
            
            # Intentar diferentes estructuras de JSON
            if isinstance(datos_json, list):
                df = pd.DataFrame(datos_json)
            elif isinstance(datos_json, dict):
                # Si es un dict, intentar diferentes interpretaciones
                if 'data' in datos_json:
                    df = pd.DataFrame(datos_json['data'])
                elif all(isinstance(v, list) for v in datos_json.values()):
                    df = pd.DataFrame(datos_json)
                else:
                    # Convertir dict a DataFrame con una sola fila
                    df = pd.DataFrame([datos_json])
            else:
                raise ValueError("Estructura JSON no soportada")
            
            # Guardar metadatos
            self.metadatos.update({
                'formato': 'JSON',
                'encoding': encoding,
                'filas': len(df),
                'columnas': len(df.columns)
            })
            
            return df
            
        except Exception as e:
            raise ValueError(f"Error al leer archivo JSON: {str(e)}")
    
    def _cargar_parquet(self, ruta_archivo: str, **kwargs) -> pd.DataFrame:
        """Carga un archivo Parquet."""
        try:
            df = pd.read_parquet(ruta_archivo, **kwargs)
            
            # Guardar metadatos
            self.metadatos.update({
                'formato': 'Parquet',
                'filas': len(df),
                'columnas': len(df.columns)
            })
            
            return df
            
        except Exception as e:
            raise ValueError(f"Error al leer archivo Parquet: {str(e)}")
    
    def _cargar_texto(self, ruta_archivo: str, **kwargs) -> pd.DataFrame:
        """Carga un archivo de texto plano."""
        # Intentar detectar si es un archivo delimitado
        encoding = kwargs.get('encoding', self.detectar_encoding(ruta_archivo))
        separador = kwargs.get('sep', self.detectar_separador_csv(ruta_archivo, encoding))
        
        # Si no hay separador claro, cargar como texto plano
        if separador == ',' and ruta_archivo.endswith('.txt'):
            separador = kwargs.get('sep', '\t')  # Asumir tab para .txt
        
        parametros = {
            'encoding': encoding,
            'sep': separador,
            'header': kwargs.get('header', 0)
        }
        
        return self._cargar_csv(ruta_archivo, **parametros)
    
    def _cargar_tsv(self, ruta_archivo: str, **kwargs) -> pd.DataFrame:
        """Carga un archivo TSV (Tab Separated Values)."""
        kwargs['sep'] = '\t'
        return self._cargar_csv(ruta_archivo, **kwargs)
    
    def cargar_archivo(self, ruta_archivo: str, **kwargs) -> pd.DataFrame:
        """
        Carga un archivo automáticamente según su extensión.
        
        Args:
            ruta_archivo: Ruta del archivo a cargar
            **kwargs: Parámetros adicionales específicos del formato
        
        Returns:
            DataFrame con los datos cargados
        """
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"El archivo '{ruta_archivo}' no existe")
        
        # Obtener extensión del archivo
        extension = Path(ruta_archivo).suffix.lower()
        
        if extension not in self.formatos_soportados:
            raise ValueError(f"Formato de archivo '{extension}' no soportado. "
                           f"Formatos soportados: {list(self.formatos_soportados.keys())}")
        
        # Cargar archivo usando el método apropiado
        cargador = self.formatos_soportados[extension]
        
        try:
            df = cargador(ruta_archivo, **kwargs)
            
            # Guardar información del último archivo cargado
            self.ultimo_archivo = ruta_archivo
            self.ultimo_dataframe = df
            
            # Agregar metadatos adicionales
            self.metadatos.update({
                'ruta_archivo': ruta_archivo,
                'tamano_archivo_mb': os.path.getsize(ruta_archivo) / 1024 / 1024,
                'fecha_modificacion': pd.Timestamp.fromtimestamp(os.path.getmtime(ruta_archivo))
            })
            
            print(f"✓ Archivo cargado exitosamente: {Path(ruta_archivo).name}")
            print(f"  Formato: {self.metadatos.get('formato', 'Desconocido')}")
            print(f"  Dimensiones: {len(df)} filas × {len(df.columns)} columnas")
            
            return df
            
        except Exception as e:
            raise ValueError(f"Error al cargar el archivo '{ruta_archivo}': {str(e)}")
    
    def obtener_metadatos(self) -> Dict[str, Any]:
        """
        Obtiene los metadatos del último archivo cargado.
        
        Returns:
            Diccionario con metadatos
        """
        return self.metadatos.copy()
    
    def listar_hojas_excel(self, ruta_archivo: str) -> List[str]:
        """
        Lista las hojas disponibles en un archivo Excel.
        
        Args:
            ruta_archivo: Ruta del archivo Excel
        
        Returns:
            Lista de nombres de hojas
        """
        if not ruta_archivo.lower().endswith(('.xlsx', '.xls')):
            raise ValueError("El archivo debe ser de formato Excel")
        
        try:
            hojas_excel = pd.ExcelFile(ruta_archivo)
            return hojas_excel.sheet_names
        except Exception as e:
            raise ValueError(f"Error al leer archivo Excel: {str(e)}")
    
    def preview_archivo(self, ruta_archivo: str, num_filas: int = 5) -> Dict[str, Any]:
        """
        Obtiene una vista previa del archivo sin cargarlo completamente.
        
        Args:
            ruta_archivo: Ruta del archivo
            num_filas: Número de filas para la vista previa
        
        Returns:
            Diccionario con vista previa e información básica
        """
        extension = Path(ruta_archivo).suffix.lower()
        
        try:
            if extension == '.csv':
                encoding = self.detectar_encoding(ruta_archivo)
                separador = self.detectar_separador_csv(ruta_archivo, encoding)
                df_preview = pd.read_csv(ruta_archivo, nrows=num_filas, 
                                       encoding=encoding, sep=separador)
            
            elif extension in ['.xlsx', '.xls']:
                df_preview = pd.read_excel(ruta_archivo, nrows=num_filas)
            
            else:
                # Para otros formatos, intentar carga limitada
                df_preview = self.cargar_archivo(ruta_archivo).head(num_filas)
            
            return {
                'preview': df_preview,
                'columnas': df_preview.columns.tolist(),
                'tipos_datos': df_preview.dtypes.to_dict(),
                'forma_preview': df_preview.shape,
                'archivo_info': {
                    'nombre': Path(ruta_archivo).name,
                    'extension': extension,
                    'tamano_mb': os.path.getsize(ruta_archivo) / 1024 / 1024
                }
            }
            
        except Exception as e:
            return {
                'error': f"No se pudo generar vista previa: {str(e)}",
                'archivo_info': {
                    'nombre': Path(ruta_archivo).name,
                    'extension': extension,
                    'tamano_mb': os.path.getsize(ruta_archivo) / 1024 / 1024
                }
            }


# Función de conveniencia para uso directo
def cargar_datos(ruta_archivo: str, **kwargs) -> pd.DataFrame:
    """
    Función de conveniencia para cargar datos rápidamente.
    
    Args:
        ruta_archivo: Ruta del archivo a cargar
        **kwargs: Parámetros adicionales
    
    Returns:
        DataFrame con los datos cargados
    """
    cargador = CargadorDatos()
    return cargador.cargar_archivo(ruta_archivo, **kwargs)


def detectar_tipos_columnas(df: pd.DataFrame) -> Dict[str, str]:
    """
    Detecta y sugiere tipos de datos óptimos para las columnas.
    
    Args:
        df: DataFrame a analizar
    
    Returns:
        Diccionario con sugerencias de tipos
    """
    sugerencias = {}
    
    for columna in df.columns:
        serie = df[columna].dropna()
        
        if len(serie) == 0:
            sugerencias[columna] = 'object'
            continue
        
        # Intentar conversiones
        try:
            # Probar entero
            pd.to_numeric(serie, downcast='integer')
            sugerencias[columna] = 'int64'
            continue
        except:
            pass
        
        try:
            # Probar float
            pd.to_numeric(serie)
            sugerencias[columna] = 'float64'
            continue
        except:
            pass
        
        try:
            # Probar fecha
            pd.to_datetime(serie)
            sugerencias[columna] = 'datetime64[ns]'
            continue
        except:
            pass
        
        # Verificar si es categórica
        if serie.nunique() / len(serie) < 0.5 and serie.nunique() < 50:
            sugerencias[columna] = 'category'
        else:
            sugerencias[columna] = 'object'
    
    return sugerencias


def optimizar_tipos_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimiza automáticamente los tipos de datos de un DataFrame.
    
    Args:
        df: DataFrame a optimizar
    
    Returns:
        DataFrame con tipos optimizados
    """
    df_optimizado = df.copy()
    
    for columna in df_optimizado.columns:
        serie_original = df_optimizado[columna]
        
        # Saltar columnas completamente nulas
        if serie_original.isnull().all():
            continue
        
        try:
            # Intentar conversión numérica
            if serie_original.dtype == 'object':
                # Limpiar datos antes de conversión
                serie_limpia = serie_original.astype(str).str.strip()
                
                # Probar conversión a numérico
                serie_numerica = pd.to_numeric(serie_limpia, errors='coerce')
                
                # Si la conversión es exitosa para la mayoría de valores
                if serie_numerica.notna().sum() / len(serie_original) > 0.8:
                    df_optimizado[columna] = serie_numerica
                    continue
            
            # Optimizar columnas numéricas existentes
            elif pd.api.types.is_numeric_dtype(serie_original):
                if pd.api.types.is_integer_dtype(serie_original):
                    df_optimizado[columna] = pd.to_numeric(serie_original, downcast='integer')
                elif pd.api.types.is_float_dtype(serie_original):
                    df_optimizado[columna] = pd.to_numeric(serie_original, downcast='float')
        
        except Exception:
            # Mantener tipo original si hay error
            continue
    
    return df_optimizado