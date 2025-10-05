"""
Módulo de análisis de correlaciones
Funciones para calcular y analizar correlaciones entre variables.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import warnings


def matriz_correlacion(df: pd.DataFrame, metodo: str = 'pearson') -> pd.DataFrame:
    """
    Calcula la matriz de correlación para variables numéricas.
    
    Args:
        df: DataFrame de pandas
        metodo: Método de correlación ('pearson', 'spearman', 'kendall')
    
    Returns:
        Matriz de correlación como DataFrame
    """
    df_numerico = df.select_dtypes(include=[np.number])
    
    if df_numerico.empty:
        raise ValueError("No se encontraron columnas numéricas para calcular correlaciones")
    
    return df_numerico.corr(method=metodo)


def correlaciones_significativas(df: pd.DataFrame, umbral: float = 0.5, 
                               metodo: str = 'pearson') -> List[Tuple[str, str, float]]:
    """
    Encuentra correlaciones significativas basadas en un umbral.
    
    Args:
        df: DataFrame de pandas
        umbral: Umbral mínimo de correlación (valor absoluto)
        metodo: Método de correlación
    
    Returns:
        Lista de tuplas con (variable1, variable2, correlacion)
    """
    corr_matrix = matriz_correlacion(df, metodo)
    correlaciones = []
    
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            col1 = corr_matrix.columns[i]
            col2 = corr_matrix.columns[j]
            valor_corr = corr_matrix.iloc[i, j]
            
            if abs(valor_corr) >= umbral and not pd.isna(valor_corr):
                correlaciones.append((col1, col2, valor_corr))
    
    # Ordenar por valor absoluto de correlación (descendente)
    correlaciones.sort(key=lambda x: abs(x[2]), reverse=True)
    
    return correlaciones


def interpretar_correlacion(valor: float) -> str:
    """
    Interpreta el valor de correlación en términos descriptivos.
    
    Args:
        valor: Valor de correlación (-1 a 1)
    
    Returns:
        Interpretación textual de la correlación
    """
    abs_valor = abs(valor)
    
    if abs_valor >= 0.9:
        intensidad = "muy fuerte"
    elif abs_valor >= 0.7:
        intensidad = "fuerte"
    elif abs_valor >= 0.5:
        intensidad = "moderada"
    elif abs_valor >= 0.3:
        intensidad = "débil"
    else:
        intensidad = "muy débil"
    
    direccion = "positiva" if valor > 0 else "negativa"
    
    return f"Correlación {direccion} {intensidad}"


def analisis_correlacion_completo(df: pd.DataFrame, umbral: float = 0.3) -> Dict:
    """
    Realiza un análisis completo de correlaciones.
    
    Args:
        df: DataFrame de pandas
        umbral: Umbral mínimo para considerar correlaciones significativas
    
    Returns:
        Diccionario con análisis completo de correlaciones
    """
    try:
        # Calcular matriz de correlación
        corr_matrix = matriz_correlacion(df)
        
        # Encontrar correlaciones significativas
        correlaciones_sig = correlaciones_significativas(df, umbral)
        
        # Interpretar correlaciones
        interpretaciones = []
        for col1, col2, valor in correlaciones_sig:
            interpretaciones.append({
                'variables': f"{col1} - {col2}",
                'correlacion': valor,
                'interpretacion': interpretar_correlacion(valor)
            })
        
        # Estadísticas generales
        valores_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                valor = corr_matrix.iloc[i, j]
                if not pd.isna(valor):
                    valores_corr.append(valor)
        
        return {
            'matriz_correlacion': corr_matrix,
            'correlaciones_significativas': interpretaciones,
            'estadisticas_generales': {
                'correlacion_promedio': np.mean(valores_corr),
                'correlacion_maxima': max(valores_corr) if valores_corr else 0,
                'correlacion_minima': min(valores_corr) if valores_corr else 0,
                'total_pares_variables': len(valores_corr),
                'pares_significativos': len(correlaciones_sig)
            },
            'recomendaciones': generar_recomendaciones_correlacion(interpretaciones)
        }
    
    except Exception as e:
        return {
            'error': f"Error en el análisis de correlaciones: {str(e)}",
            'matriz_correlacion': None,
            'correlaciones_significativas': [],
            'estadisticas_generales': {},
            'recomendaciones': []
        }


def generar_recomendaciones_correlacion(interpretaciones: List[Dict]) -> List[str]:
    """
    Genera recomendaciones basadas en el análisis de correlaciones.
    
    Args:
        interpretaciones: Lista de interpretaciones de correlaciones
    
    Returns:
        Lista de recomendaciones
    """
    recomendaciones = []
    
    if not interpretaciones:
        recomendaciones.append("No se encontraron correlaciones significativas en los datos.")
        return recomendaciones
    
    # Correlaciones muy fuertes
    muy_fuertes = [i for i in interpretaciones if abs(i['correlacion']) >= 0.9]
    if muy_fuertes:
        recomendaciones.append(
            f"Se detectaron {len(muy_fuertes)} correlaciones muy fuertes. "
            "Considere si hay multicolinealidad en sus datos."
        )
    
    # Correlaciones negativas fuertes
    negativas_fuertes = [i for i in interpretaciones if i['correlacion'] <= -0.7]
    if negativas_fuertes:
        recomendaciones.append(
            f"Hay {len(negativas_fuertes)} correlaciones negativas fuertes. "
            "Estas variables tienen una relación inversa importante."
        )
    
    # Correlaciones positivas fuertes
    positivas_fuertes = [i for i in interpretaciones if i['correlacion'] >= 0.7]
    if positivas_fuertes:
        recomendaciones.append(
            f"Se encontraron {len(positivas_fuertes)} correlaciones positivas fuertes. "
            "Estas variables tienden a aumentar juntas."
        )
    
    return recomendaciones