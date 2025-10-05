"""
Módulo de limpieza y preprocesamiento de datos
Funciones para limpiar, transformar y preparar los datos para análisis.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any


def detectar_problemas_datos(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Detecta problemas comunes en el dataset.
    
    Args:
        df: DataFrame de pandas
    
    Returns:
        Diccionario con problemas detectados
    """
    problemas = {
        'valores_nulos': {},
        'duplicados': 0,
        'tipos_inconsistentes': {},
        'valores_extremos': {},
        'columnas_vacias': []
    }
    
    # Valores nulos
    nulos_por_columna = df.isnull().sum()
    problemas['valores_nulos'] = {
        col: {'cantidad': int(nulos), 'porcentaje': round((nulos/len(df))*100, 2)}
        for col, nulos in nulos_por_columna.items() if nulos > 0
    }
    
    # Duplicados
    problemas['duplicados'] = int(df.duplicated().sum())
    
    # Columnas completamente vacías
    problemas['columnas_vacias'] = [col for col in df.columns if df[col].isnull().all()]
    
    # Detectar problemas en columnas numéricas
    for col in df.select_dtypes(include=[np.number]).columns:
        serie = df[col].dropna()
        if not serie.empty:
            Q1 = serie.quantile(0.25)
            Q3 = serie.quantile(0.75)
            IQR = Q3 - Q1
            outliers_inf = (serie < (Q1 - 1.5 * IQR)).sum()
            outliers_sup = (serie > (Q3 + 1.5 * IQR)).sum()
            
            if outliers_inf > 0 or outliers_sup > 0:
                problemas['valores_extremos'][col] = {
                    'outliers_inferiores': int(outliers_inf),
                    'outliers_superiores': int(outliers_sup),
                    'total_outliers': int(outliers_inf + outliers_sup)
                }
    
    return problemas


def limpiar_valores_nulos(df: pd.DataFrame, estrategia: str = 'eliminar', 
                         columnas: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Limpia valores nulos según la estrategia especificada.
    
    Args:
        df: DataFrame de pandas
        estrategia: 'eliminar', 'media', 'mediana', 'moda', 'forward_fill', 'backward_fill'
        columnas: Lista de columnas a procesar (None para todas)
    
    Returns:
        DataFrame limpio
    """
    df_limpio = df.copy()
    
    if columnas is None:
        columnas = df.columns.tolist()
    
    for col in columnas:
        if col not in df.columns:
            continue
            
        if estrategia == 'eliminar':
            df_limpio = df_limpio.dropna(subset=[col])
        
        elif estrategia == 'media' and pd.api.types.is_numeric_dtype(df[col]):
            df_limpio[col].fillna(df[col].mean(), inplace=True)
        
        elif estrategia == 'mediana' and pd.api.types.is_numeric_dtype(df[col]):
            df_limpio[col].fillna(df[col].median(), inplace=True)
        
        elif estrategia == 'moda':
            moda = df[col].mode()
            if not moda.empty:
                df_limpio[col].fillna(moda.iloc[0], inplace=True)
        
        elif estrategia == 'forward_fill':
            df_limpio[col].fillna(method='ffill', inplace=True)
        
        elif estrategia == 'backward_fill':
            df_limpio[col].fillna(method='bfill', inplace=True)
    
    return df_limpio


def eliminar_duplicados(df: pd.DataFrame, columnas: Optional[List[str]] = None, 
                       mantener: str = 'first') -> pd.DataFrame:
    """
    Elimina filas duplicadas.
    
    Args:
        df: DataFrame de pandas
        columnas: Lista de columnas para considerar duplicados (None para todas)
        mantener: 'first', 'last', False (elimina todos los duplicados)
    
    Returns:
        DataFrame sin duplicados
    """
    if mantener == False:
        # Eliminar todos los duplicados
        return df[~df.duplicated(subset=columnas, keep=False)]
    else:
        return df.drop_duplicates(subset=columnas, keep=mantener)


def tratar_outliers(df: pd.DataFrame, columna: str, metodo: str = 'iqr_cap') -> pd.DataFrame:
    """
    Trata valores atípicos en una columna numérica.
    
    Args:
        df: DataFrame de pandas
        columna: Nombre de la columna
        metodo: 'iqr_cap' (limitación), 'iqr_remove' (eliminación), 'zscore_remove'
    
    Returns:
        DataFrame con outliers tratados
    """
    df_tratado = df.copy()
    serie = df[columna].dropna()
    
    if not pd.api.types.is_numeric_dtype(serie):
        raise ValueError(f"La columna '{columna}' debe ser numérica")
    
    if metodo == 'iqr_cap':
        Q1 = serie.quantile(0.25)
        Q3 = serie.quantile(0.75)
        IQR = Q3 - Q1
        limite_inf = Q1 - 1.5 * IQR
        limite_sup = Q3 + 1.5 * IQR
        
        df_tratado[columna] = df_tratado[columna].clip(lower=limite_inf, upper=limite_sup)
    
    elif metodo == 'iqr_remove':
        Q1 = serie.quantile(0.25)
        Q3 = serie.quantile(0.75)
        IQR = Q3 - Q1
        limite_inf = Q1 - 1.5 * IQR
        limite_sup = Q3 + 1.5 * IQR
        
        df_tratado = df_tratado[
            (df_tratado[columna] >= limite_inf) & (df_tratado[columna] <= limite_sup)
        ]
    
    elif metodo == 'zscore_remove':
        from scipy import stats
        z_scores = np.abs(stats.zscore(serie))
        df_tratado = df_tratado[z_scores <= 3]
    
    return df_tratado


def normalizar_datos(df: pd.DataFrame, columnas: Optional[List[str]] = None, 
                    metodo: str = 'minmax') -> pd.DataFrame:
    """
    Normaliza columnas numéricas.
    
    Args:
        df: DataFrame de pandas
        columnas: Lista de columnas a normalizar (None para todas las numéricas)
        metodo: 'minmax' (0-1), 'zscore' (estandarización), 'robust'
    
    Returns:
        DataFrame con datos normalizados
    """
    df_normalizado = df.copy()
    
    if columnas is None:
        columnas = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if metodo == 'minmax':
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        df_normalizado[columnas] = scaler.fit_transform(df[columnas])
    
    elif metodo == 'zscore':
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        df_normalizado[columnas] = scaler.fit_transform(df[columnas])
    
    elif metodo == 'robust':
        from sklearn.preprocessing import RobustScaler
        scaler = RobustScaler()
        df_normalizado[columnas] = scaler.fit_transform(df[columnas])
    
    return df_normalizado


def pipeline_limpieza_completa(df: pd.DataFrame, configuracion: Optional[Dict] = None) -> Dict:
    """
    Ejecuta un pipeline completo de limpieza de datos.
    
    Args:
        df: DataFrame de pandas
        configuracion: Diccionario con configuración personalizada
    
    Returns:
        Diccionario con DataFrame limpio y reporte de limpieza
    """
    config_default = {
        'eliminar_duplicados': True,
        'tratar_nulos': 'media',  # 'eliminar', 'media', 'mediana', 'moda'
        'tratar_outliers': False,
        'normalizar': False,
        'eliminar_columnas_vacias': True
    }
    
    if configuracion:
        config_default.update(configuracion)
    
    df_limpio = df.copy()
    reporte = {
        'filas_originales': len(df),
        'columnas_originales': len(df.columns),
        'acciones_realizadas': []
    }
    
    # Detectar problemas iniciales
    problemas_iniciales = detectar_problemas_datos(df)
    
    # Eliminar columnas completamente vacías
    if config_default['eliminar_columnas_vacias'] and problemas_iniciales['columnas_vacias']:
        df_limpio = df_limpio.drop(columns=problemas_iniciales['columnas_vacias'])
        reporte['acciones_realizadas'].append(
            f"Eliminadas {len(problemas_iniciales['columnas_vacias'])} columnas vacías"
        )
    
    # Eliminar duplicados
    if config_default['eliminar_duplicados'] and problemas_iniciales['duplicados'] > 0:
        df_limpio = eliminar_duplicados(df_limpio)
        reporte['acciones_realizadas'].append(
            f"Eliminadas {problemas_iniciales['duplicados']} filas duplicadas"
        )
    
    # Tratar valores nulos
    if config_default['tratar_nulos'] != 'ignorar':
        df_limpio = limpiar_valores_nulos(df_limpio, config_default['tratar_nulos'])
        reporte['acciones_realizadas'].append(
            f"Valores nulos tratados con estrategia: {config_default['tratar_nulos']}"
        )
    
    # Normalizar datos
    if config_default['normalizar']:
        df_limpio = normalizar_datos(df_limpio)
        reporte['acciones_realizadas'].append("Datos normalizados")
    
    # Estadísticas finales
    reporte.update({
        'filas_finales': len(df_limpio),
        'columnas_finales': len(df_limpio.columns),
        'filas_eliminadas': len(df) - len(df_limpio),
        'columnas_eliminadas': len(df.columns) - len(df_limpio.columns)
    })
    
    return {
        'datos_limpios': df_limpio,
        'reporte_limpieza': reporte,
        'problemas_detectados': problemas_iniciales
    }