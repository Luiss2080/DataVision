"""
Módulo de generación de tablas
Funciones para crear y formatear tablas de datos y estadísticas.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def tabla_estadisticas_descriptivas(df: pd.DataFrame, columnas: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Genera una tabla con estadísticas descriptivas.
    
    Args:
        df: DataFrame de pandas
        columnas: Lista de columnas a incluir (None para todas las numéricas)
    
    Returns:
        DataFrame con estadísticas descriptivas
    """
    if columnas is None:
        df_analisis = df.select_dtypes(include=[np.number])
    else:
        df_analisis = df[columnas].select_dtypes(include=[np.number])
    
    if df_analisis.empty:
        raise ValueError("No hay columnas numéricas para analizar")
    
    estadisticas = pd.DataFrame({
        'Columna': df_analisis.columns,
        'Tipo': [str(df_analisis[col].dtype) for col in df_analisis.columns],
        'Count': [df_analisis[col].count() for col in df_analisis.columns],
        'Nulos': [df_analisis[col].isnull().sum() for col in df_analisis.columns],
        'Únicos': [df_analisis[col].nunique() for col in df_analisis.columns],
        'Media': [df_analisis[col].mean() for col in df_analisis.columns],
        'Mediana': [df_analisis[col].median() for col in df_analisis.columns],
        'Desv_Std': [df_analisis[col].std() for col in df_analisis.columns],
        'Mínimo': [df_analisis[col].min() for col in df_analisis.columns],
        'Máximo': [df_analisis[col].max() for col in df_analisis.columns],
        'Q25': [df_analisis[col].quantile(0.25) for col in df_analisis.columns],
        'Q75': [df_analisis[col].quantile(0.75) for col in df_analisis.columns]
    })
    
    # Redondear valores numéricos
    columnas_numericas = ['Media', 'Mediana', 'Desv_Std', 'Mínimo', 'Máximo', 'Q25', 'Q75']
    estadisticas[columnas_numericas] = estadisticas[columnas_numericas].round(2)
    
    return estadisticas


def tabla_informacion_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera una tabla con información general del dataset.
    
    Args:
        df: DataFrame de pandas
    
    Returns:
        DataFrame con información del dataset
    """
    info_general = []
    
    # Información básica
    info_general.append(['Número de filas', f"{len(df):,}"])
    info_general.append(['Número de columnas', len(df.columns)])
    info_general.append(['Memoria total (MB)', f"{df.memory_usage(deep=True).sum() / 1024**2:.2f}"])
    info_general.append(['Valores nulos totales', f"{df.isnull().sum().sum():,}"])
    info_general.append(['% de valores nulos', f"{(df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100:.2f}%"])
    info_general.append(['Filas duplicadas', f"{df.duplicated().sum():,}"])
    
    # Información por tipo de datos
    tipos_datos = df.dtypes.value_counts()
    for tipo, cantidad in tipos_datos.items():
        info_general.append([f'Columnas {tipo}', cantidad])
    
    # Crear DataFrame
    tabla_info = pd.DataFrame(info_general, columns=['Característica', 'Valor'])
    
    return tabla_info


def tabla_correlaciones_significativas(df: pd.DataFrame, umbral: float = 0.5) -> pd.DataFrame:
    """
    Genera una tabla con correlaciones significativas.
    
    Args:
        df: DataFrame de pandas
        umbral: Umbral mínimo de correlación (valor absoluto)
    
    Returns:
        DataFrame con correlaciones significativas
    """
    # Seleccionar columnas numéricas
    df_numerico = df.select_dtypes(include=[np.number])
    
    if len(df_numerico.columns) < 2:
        return pd.DataFrame(columns=['Variable 1', 'Variable 2', 'Correlación', 'Interpretación'])
    
    # Calcular matriz de correlación
    corr_matrix = df_numerico.corr()
    
    # Encontrar correlaciones significativas
    correlaciones = []
    
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            col1 = corr_matrix.columns[i]
            col2 = corr_matrix.columns[j]
            valor_corr = corr_matrix.iloc[i, j]
            
            if abs(valor_corr) >= umbral and not pd.isna(valor_corr):
                # Interpretación
                abs_valor = abs(valor_corr)
                if abs_valor >= 0.9:
                    interpretacion = "Muy fuerte"
                elif abs_valor >= 0.7:
                    interpretacion = "Fuerte"
                elif abs_valor >= 0.5:
                    interpretacion = "Moderada"
                else:
                    interpretacion = "Débil"
                
                direccion = "positiva" if valor_corr > 0 else "negativa"
                interpretacion_completa = f"{interpretacion} {direccion}"
                
                correlaciones.append([col1, col2, round(valor_corr, 3), interpretacion_completa])
    
    # Crear DataFrame y ordenar por valor absoluto
    if correlaciones:
        tabla_corr = pd.DataFrame(correlaciones, 
                                columns=['Variable 1', 'Variable 2', 'Correlación', 'Interpretación'])
        tabla_corr['Abs_Correlacion'] = abs(tabla_corr['Correlación'])
        tabla_corr = tabla_corr.sort_values('Abs_Correlacion', ascending=False)
        tabla_corr = tabla_corr.drop('Abs_Correlacion', axis=1)
        return tabla_corr
    else:
        return pd.DataFrame(columns=['Variable 1', 'Variable 2', 'Correlación', 'Interpretación'])


def tabla_valores_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera una tabla detallada de valores nulos por columna.
    
    Args:
        df: DataFrame de pandas
    
    Returns:
        DataFrame con información de valores nulos
    """
    nulos_info = []
    
    for col in df.columns:
        nulos_count = df[col].isnull().sum()
        nulos_pct = (nulos_count / len(df)) * 100
        tipo_dato = str(df[col].dtype)
        
        nulos_info.append([
            col,
            tipo_dato,
            f"{len(df):,}",
            f"{nulos_count:,}",
            f"{nulos_pct:.2f}%",
            "Sí" if nulos_count > 0 else "No"
        ])
    
    tabla_nulos = pd.DataFrame(nulos_info, columns=[
        'Columna', 'Tipo', 'Total Valores', 'Valores Nulos', '% Nulos', 'Requiere Limpieza'
    ])
    
    # Ordenar por porcentaje de nulos (descendente)
    tabla_nulos['_pct_sort'] = [float(x.replace('%', '')) for x in tabla_nulos['% Nulos']]
    tabla_nulos = tabla_nulos.sort_values('_pct_sort', ascending=False)
    tabla_nulos = tabla_nulos.drop('_pct_sort', axis=1)
    
    return tabla_nulos


def tabla_outliers_resumen(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera una tabla resumen de outliers para columnas numéricas.
    
    Args:
        df: DataFrame de pandas
    
    Returns:
        DataFrame con información de outliers
    """
    outliers_info = []
    
    for col in df.select_dtypes(include=[np.number]).columns:
        serie = df[col].dropna()
        
        if len(serie) == 0:
            continue
        
        # Método IQR
        Q1 = serie.quantile(0.25)
        Q3 = serie.quantile(0.75)
        IQR = Q3 - Q1
        limite_inf = Q1 - 1.5 * IQR
        limite_sup = Q3 + 1.5 * IQR
        
        outliers_inf = (serie < limite_inf).sum()
        outliers_sup = (serie > limite_sup).sum()
        total_outliers = outliers_inf + outliers_sup
        pct_outliers = (total_outliers / len(serie)) * 100
        
        outliers_info.append([
            col,
            f"{len(serie):,}",
            f"{total_outliers:,}",
            f"{pct_outliers:.2f}%",
            f"{outliers_inf:,}",
            f"{outliers_sup:,}",
            f"{limite_inf:.2f}",
            f"{limite_sup:.2f}"
        ])
    
    if outliers_info:
        tabla_outliers = pd.DataFrame(outliers_info, columns=[
            'Columna', 'Total Valores', 'Outliers', '% Outliers',
            'Outliers Inf.', 'Outliers Sup.', 'Límite Inf.', 'Límite Sup.'
        ])
        
        # Ordenar por porcentaje de outliers
        tabla_outliers['_pct_sort'] = [float(x.replace('%', '')) for x in tabla_outliers['% Outliers']]
        tabla_outliers = tabla_outliers.sort_values('_pct_sort', ascending=False)
        tabla_outliers = tabla_outliers.drop('_pct_sort', axis=1)
        
        return tabla_outliers
    else:
        return pd.DataFrame(columns=[
            'Columna', 'Total Valores', 'Outliers', '% Outliers',
            'Outliers Inf.', 'Outliers Sup.', 'Límite Inf.', 'Límite Sup.'
        ])


def crear_tabla_interactiva_plotly(df: pd.DataFrame, titulo: str = "Tabla de Datos") -> go.Figure:
    """
    Crea una tabla interactiva usando Plotly.
    
    Args:
        df: DataFrame a mostrar
        titulo: Título de la tabla
    
    Returns:
        Figura de Plotly con la tabla
    """
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(df.columns),
            fill_color='lightblue',
            align='center',
            font=dict(size=12, color='white')
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            fill_color='white',
            align='center',
            font=dict(size=10)
        )
    )])
    
    fig.update_layout(
        title=titulo,
        height=min(600, 50 + len(df) * 25)  # Altura adaptativa
    )
    
    return fig


def resumen_calidad_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera un resumen de la calidad de los datos.
    
    Args:
        df: DataFrame de pandas
    
    Returns:
        DataFrame con métricas de calidad
    """
    calidad_info = []
    
    for col in df.columns:
        serie = df[col]
        
        # Métricas básicas
        total_valores = len(serie)
        valores_nulos = serie.isnull().sum()
        pct_nulos = (valores_nulos / total_valores) * 100
        valores_unicos = serie.nunique()
        pct_unicos = (valores_unicos / total_valores) * 100
        
        # Clasificación de calidad
        if pct_nulos == 0:
            calidad_nulos = "Excelente"
        elif pct_nulos <= 5:
            calidad_nulos = "Buena"
        elif pct_nulos <= 15:
            calidad_nulos = "Regular"
        else:
            calidad_nulos = "Deficiente"
        
        # Para columnas numéricas, detectar outliers
        outliers_info = "N/A"
        if pd.api.types.is_numeric_dtype(serie):
            serie_limpia = serie.dropna()
            if len(serie_limpia) > 0:
                Q1 = serie_limpia.quantile(0.25)
                Q3 = serie_limpia.quantile(0.75)
                IQR = Q3 - Q1
                outliers = ((serie_limpia < (Q1 - 1.5 * IQR)) | 
                          (serie_limpia > (Q3 + 1.5 * IQR))).sum()
                pct_outliers = (outliers / len(serie_limpia)) * 100
                outliers_info = f"{pct_outliers:.1f}%"
        
        calidad_info.append([
            col,
            str(serie.dtype),
            f"{total_valores:,}",
            f"{valores_nulos:,}",
            f"{pct_nulos:.1f}%",
            calidad_nulos,
            f"{valores_unicos:,}",
            f"{pct_unicos:.1f}%",
            outliers_info
        ])
    
    tabla_calidad = pd.DataFrame(calidad_info, columns=[
        'Columna', 'Tipo', 'Total', 'Nulos', '% Nulos', 'Calidad',
        'Únicos', '% Únicos', '% Outliers'
    ])
    
    return tabla_calidad