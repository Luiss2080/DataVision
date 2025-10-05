"""
Módulo de generación de gráficos
Funciones para crear diferentes tipos de visualizaciones de datos.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Tuple, Any
import warnings

# Configuración de estilo
plt.style.use('default')
sns.set_palette("husl")
warnings.filterwarnings('ignore')


def configurar_estilo_matplotlib():
    """Configura el estilo base para matplotlib."""
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3


def grafico_distribucion(df: pd.DataFrame, columna: str, tipo: str = 'histograma') -> go.Figure:
    """
    Crea gráficos de distribución para una columna.
    
    Args:
        df: DataFrame de pandas
        columna: Nombre de la columna
        tipo: 'histograma', 'boxplot', 'violinplot', 'kde'
    
    Returns:
        Figura de Plotly
    """
    if columna not in df.columns:
        raise ValueError(f"La columna '{columna}' no existe")
    
    serie = df[columna].dropna()
    
    if tipo == 'histograma':
        fig = px.histogram(
            df, x=columna,
            title=f'Distribución de {columna}',
            nbins=30,
            marginal="box"
        )
        fig.update_layout(
            xaxis_title=columna,
            yaxis_title='Frecuencia',
            showlegend=False
        )
    
    elif tipo == 'boxplot':
        fig = px.box(
            df, y=columna,
            title=f'Diagrama de Caja de {columna}'
        )
        fig.update_layout(
            yaxis_title=columna,
            showlegend=False
        )
    
    elif tipo == 'violinplot':
        fig = go.Figure(data=go.Violin(
            y=serie,
            name=columna,
            box_visible=True,
            meanline_visible=True
        ))
        fig.update_layout(
            title=f'Gráfico de Violín de {columna}',
            yaxis_title=columna
        )
    
    elif tipo == 'kde':
        # Usar seaborn para KDE y convertir a plotly
        fig = go.Figure()
        
        # Calcular KDE manualmente
        from scipy import stats
        density = stats.gaussian_kde(serie)
        xs = np.linspace(serie.min(), serie.max(), 200)
        ys = density(xs)
        
        fig.add_trace(go.Scatter(
            x=xs, y=ys,
            mode='lines',
            name='Densidad',
            fill='tozeroy'
        ))
        
        fig.update_layout(
            title=f'Densidad de Probabilidad de {columna}',
            xaxis_title=columna,
            yaxis_title='Densidad'
        )
    
    return fig


def grafico_correlacion(df: pd.DataFrame, metodo: str = 'pearson') -> go.Figure:
    """
    Crea un mapa de calor de correlaciones.
    
    Args:
        df: DataFrame de pandas
        metodo: Método de correlación
    
    Returns:
        Figura de Plotly con mapa de calor
    """
    # Seleccionar solo columnas numéricas
    df_numerico = df.select_dtypes(include=[np.number])
    
    if df_numerico.empty:
        raise ValueError("No hay columnas numéricas para calcular correlaciones")
    
    # Calcular matriz de correlación
    corr_matrix = df_numerico.corr(method=metodo)
    
    # Crear mapa de calor
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title=f'Matriz de Correlación ({metodo.capitalize()})'
    )
    
    fig.update_layout(
        xaxis_title='Variables',
        yaxis_title='Variables'
    )
    
    return fig


def grafico_dispersion(df: pd.DataFrame, x: str, y: str, 
                      color: Optional[str] = None, size: Optional[str] = None) -> go.Figure:
    """
    Crea un gráfico de dispersión.
    
    Args:
        df: DataFrame de pandas
        x: Variable para eje X
        y: Variable para eje Y
        color: Variable para colorear puntos (opcional)
        size: Variable para tamaño de puntos (opcional)
    
    Returns:
        Figura de Plotly
    """
    fig = px.scatter(
        df, x=x, y=y,
        color=color,
        size=size,
        title=f'Gráfico de Dispersión: {x} vs {y}',
        hover_data=df.columns
    )
    
    # Agregar línea de tendencia
    fig.add_scatter(
        x=df[x], y=np.poly1d(np.polyfit(df[x].dropna(), df[y].dropna(), 1))(df[x]),
        mode='lines',
        name='Tendencia',
        line=dict(dash='dash', color='red')
    )
    
    return fig


def grafico_barras(df: pd.DataFrame, x: str, y: Optional[str] = None, 
                  orientacion: str = 'vertical') -> go.Figure:
    """
    Crea un gráfico de barras.
    
    Args:
        df: DataFrame de pandas
        x: Variable categórica
        y: Variable numérica (opcional, se contará frecuencia si no se especifica)
        orientacion: 'vertical' u 'horizontal'
    
    Returns:
        Figura de Plotly
    """
    if y is None:
        # Contar frecuencias
        datos = df[x].value_counts().reset_index()
        datos.columns = [x, 'count']
        x_col, y_col = x, 'count'
        titulo = f'Frecuencia de {x}'
    else:
        datos = df
        x_col, y_col = x, y
        titulo = f'{y} por {x}'
    
    if orientacion == 'vertical':
        fig = px.bar(datos, x=x_col, y=y_col, title=titulo)
    else:
        fig = px.bar(datos, x=y_col, y=x_col, orientation='h', title=titulo)
    
    return fig


def grafico_lineas(df: pd.DataFrame, x: str, y: str, 
                  color: Optional[str] = None) -> go.Figure:
    """
    Crea un gráfico de líneas.
    
    Args:
        df: DataFrame de pandas
        x: Variable para eje X (típicamente tiempo)
        y: Variable para eje Y
        color: Variable para múltiples líneas (opcional)
    
    Returns:
        Figura de Plotly
    """
    fig = px.line(
        df, x=x, y=y, color=color,
        title=f'Evolución de {y} en función de {x}',
        markers=True
    )
    
    return fig


def dashboard_exploratorio(df: pd.DataFrame) -> Dict[str, go.Figure]:
    """
    Crea un conjunto de gráficos para análisis exploratorio.
    
    Args:
        df: DataFrame de pandas
    
    Returns:
        Diccionario con múltiples figuras
    """
    graficos = {}
    
    # Columnas numéricas y categóricas
    cols_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    cols_categoricas = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # 1. Distribuciones de variables numéricas
    if len(cols_numericas) > 0:
        for col in cols_numericas[:4]:  # Máximo 4 gráficos
            try:
                graficos[f'dist_{col}'] = grafico_distribucion(df, col, 'histograma')
            except:
                continue
    
    # 2. Matriz de correlación
    if len(cols_numericas) > 1:
        try:
            graficos['correlacion'] = grafico_correlacion(df)
        except:
            pass
    
    # 3. Gráficos de barras para variables categóricas
    if len(cols_categoricas) > 0:
        for col in cols_categoricas[:3]:  # Máximo 3 gráficos
            try:
                # Solo si no hay demasiadas categorías
                if df[col].nunique() <= 20:
                    graficos[f'barras_{col}'] = grafico_barras(df, col)
            except:
                continue
    
    # 4. Scatter plots entre variables numéricas
    if len(cols_numericas) >= 2:
        try:
            graficos['scatter_principales'] = grafico_dispersion(
                df, cols_numericas[0], cols_numericas[1]
            )
        except:
            pass
    
    return graficos


def personalizar_figura(fig: go.Figure, titulo: str = None, 
                       colores: List[str] = None, tema: str = 'plotly_white') -> go.Figure:
    """
    Personaliza una figura de Plotly con estilos consistentes.
    
    Args:
        fig: Figura de Plotly
        titulo: Título personalizado
        colores: Paleta de colores personalizada
        tema: Tema de Plotly
    
    Returns:
        Figura personalizada
    """
    # Aplicar tema
    fig.update_layout(template=tema)
    
    # Actualizar título
    if titulo:
        fig.update_layout(title=titulo)
    
    # Actualizar colores si se proporcionan
    if colores and len(fig.data) > 0:
        for i, trace in enumerate(fig.data):
            if i < len(colores):
                trace.update(marker_color=colores[i])
    
    # Configuración general
    fig.update_layout(
        font=dict(size=12),
        showlegend=True,
        hovermode='closest'
    )
    
    return fig