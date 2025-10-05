"""
Módulo de estadísticas descriptivas
Funciones para calcular estadísticas básicas y avanzadas de los datos.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional


def estadisticas_basicas(df: pd.DataFrame, columna: Optional[str] = None) -> Dict[str, Any]:
    """
    Calcula estadísticas básicas para una columna específica o todo el DataFrame.
    
    Args:
        df: DataFrame de pandas
        columna: Nombre de la columna (opcional, si no se especifica se analizan todas)
    
    Returns:
        Diccionario con las estadísticas calculadas
    """
    if columna:
        if columna not in df.columns:
            raise ValueError(f"La columna '{columna}' no existe en el DataFrame")
        serie = df[columna]
        if pd.api.types.is_numeric_dtype(serie):
            return {
                'media': serie.mean(),
                'mediana': serie.median(),
                'moda': serie.mode().iloc[0] if not serie.mode().empty else None,
                'desviacion_estandar': serie.std(),
                'varianza': serie.var(),
                'minimo': serie.min(),
                'maximo': serie.max(),
                'rango': serie.max() - serie.min(),
                'cuartil_1': serie.quantile(0.25),
                'cuartil_3': serie.quantile(0.75),
                'valores_nulos': serie.isnull().sum(),
                'valores_unicos': serie.nunique()
            }
        else:
            return {
                'valores_unicos': serie.nunique(),
                'moda': serie.mode().iloc[0] if not serie.mode().empty else None,
                'valores_nulos': serie.isnull().sum(),
                'tipo_dato': str(serie.dtype)
            }
    else:
        return df.describe(include='all').to_dict()


def detectar_outliers(df: pd.DataFrame, columna: str, metodo: str = 'iqr') -> Dict[str, Any]:
    """
    Detecta valores atípicos en una columna numérica.
    
    Args:
        df: DataFrame de pandas
        columna: Nombre de la columna a analizar
        metodo: Método para detectar outliers ('iqr' o 'zscore')
    
    Returns:
        Diccionario con información sobre los outliers
    """
    if columna not in df.columns:
        raise ValueError(f"La columna '{columna}' no existe en el DataFrame")
    
    serie = df[columna].dropna()
    
    if not pd.api.types.is_numeric_dtype(serie):
        raise ValueError(f"La columna '{columna}' debe ser numérica")
    
    if metodo == 'iqr':
        Q1 = serie.quantile(0.25)
        Q3 = serie.quantile(0.75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR
        outliers = serie[(serie < limite_inferior) | (serie > limite_superior)]
        
        return {
            'metodo': 'IQR',
            'limite_inferior': limite_inferior,
            'limite_superior': limite_superior,
            'outliers': outliers.tolist(),
            'cantidad_outliers': len(outliers),
            'porcentaje_outliers': (len(outliers) / len(serie)) * 100
        }
    
    elif metodo == 'zscore':
        from scipy import stats
        z_scores = np.abs(stats.zscore(serie))
        outliers = serie[z_scores > 3]
        
        return {
            'metodo': 'Z-Score',
            'umbral': 3,
            'outliers': outliers.tolist(),
            'cantidad_outliers': len(outliers),
            'porcentaje_outliers': (len(outliers) / len(serie)) * 100
        }
    
    else:
        raise ValueError("El método debe ser 'iqr' o 'zscore'")


def resumen_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Genera un resumen completo del dataset.
    
    Args:
        df: DataFrame de pandas
    
    Returns:
        Diccionario con el resumen del dataset
    """
    return {
        'forma': df.shape,
        'columnas': df.columns.tolist(),
        'tipos_datos': df.dtypes.to_dict(),
        'valores_nulos_por_columna': df.isnull().sum().to_dict(),
        'valores_nulos_total': df.isnull().sum().sum(),
        'porcentaje_nulos': (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100,
        'memoria_uso': df.memory_usage(deep=True).sum(),
        'columnas_numericas': df.select_dtypes(include=[np.number]).columns.tolist(),
        'columnas_categoricas': df.select_dtypes(include=['object', 'category']).columns.tolist()
    }