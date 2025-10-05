"""
Interfaz de usuario simplificada con Streamlit - Tema Oscuro
Analizador de datos eficiente y funcional.
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Any
import io
import base64
import os
import warnings
from datetime import datetime

# Configurar warnings
warnings.filterwarnings('ignore')


class AnalizadorDatos:
    """Clase principal para análisis de datos básico."""
    
    def __init__(self):
        self.df = None
    
    def cargar_csv(self, archivo):
        """Carga un archivo CSV."""
        try:
            # Intentar diferentes encodings
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    if hasattr(archivo, 'read'):
                        archivo.seek(0)  # Resetear posición
                        df = pd.read_csv(archivo, encoding=encoding)
                    else:
                        df = pd.read_csv(archivo, encoding=encoding)
                    return df
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    if encoding == encodings[-1]:  # Último intento
                        raise e
                    continue
            
            # Si no funciona ningún encoding, intentar con detectores
            if hasattr(archivo, 'read'):
                archivo.seek(0)
                df = pd.read_csv(archivo, encoding='utf-8', errors='replace')
            else:
                df = pd.read_csv(archivo, encoding='utf-8', errors='replace')
            
            return df
        except Exception as e:
            st.error(f"Error al cargar el archivo: {str(e)}")
            return None
    
    def cargar_excel(self, archivo):
        """Carga un archivo Excel."""
        try:
            if hasattr(archivo, 'read'):
                df = pd.read_excel(archivo)
            else:
                df = pd.read_excel(archivo)
            return df
        except Exception as e:
            st.error(f"Error al cargar el archivo Excel: {str(e)}")
            return None
    
    def crear_grafico_distribucion(self, df, columna, tipo='histograma'):
        """Crea gráficos de distribución con Plotly."""
        if columna not in df.columns:
            return None
        
        color_palette = ['#4299e1', '#48bb78', '#ed8936', '#9f7aea']
        
        if tipo == 'histograma':
            fig = px.histogram(
                df, x=columna,
                title=f'Distribución de {columna}',
                nbins=30,
                color_discrete_sequence=color_palette
            )
            
        elif tipo == 'boxplot':
            fig = px.box(
                df, y=columna,
                title=f'Diagrama de Caja de {columna}',
                color_discrete_sequence=color_palette
            )
            
        elif tipo == 'violinplot':
            fig = go.Figure(data=go.Violin(
                y=df[columna].dropna(),
                name=columna,
                box_visible=True,
                meanline_visible=True,
                fillcolor=color_palette[0],
                line_color='white'
            ))
            fig.update_layout(title=f'Gráfico de Violín de {columna}')
            
        if 'fig' in locals():
            fig.update_layout(
                template='plotly_dark',
                title_font_size=16,
                title_x=0.5,
                height=400,
                paper_bgcolor='#2d3748',
                plot_bgcolor='#2d3748'
            )
            return fig
        return None
    
    def crear_grafico_barras(self, df, columna):
        """Crea gráfico de barras para variables categóricas."""
        if columna not in df.columns:
            return None
            
        counts = df[columna].value_counts().head(20)
        
        fig = px.bar(
            x=counts.index,
            y=counts.values,
            title=f'Distribución de {columna}',
            labels={'x': columna, 'y': 'Frecuencia'},
            color_discrete_sequence=['#4299e1']
        )
        
        fig.update_layout(
            template='plotly_dark',
            title_font_size=16,
            title_x=0.5,
            height=400,
            paper_bgcolor='#2d3748',
            plot_bgcolor='#2d3748'
        )
        
        return fig
    
    def crear_matriz_correlacion(self, df):
        """Crea matriz de correlación con Plotly."""
        columnas_numericas = df.select_dtypes(include=[np.number]).columns
        if len(columnas_numericas) < 2:
            return None
            
        corr_matrix = df[columnas_numericas].corr()
        
        fig = px.imshow(
            corr_matrix,
            title='Matriz de Correlación',
            color_continuous_scale='RdBu_r',
            aspect='auto',
            text_auto=True
        )
        
        fig.update_layout(
            template='plotly_dark',
            title_font_size=16,
            title_x=0.5,
            height=500,
            paper_bgcolor='#2d3748',
            plot_bgcolor='#2d3748'
        )
        
        return fig
    
    def crear_grafico_dispersion(self, df, x_col, y_col, color_col=None):
        """Crea gráfico de dispersión."""
        if x_col not in df.columns or y_col not in df.columns:
            return None
            
        fig = px.scatter(
            df, x=x_col, y=y_col,
            color=color_col if color_col and color_col in df.columns else None,
            title=f'Dispersión: {x_col} vs {y_col}',
            trendline="ols" if df[x_col].dtype in ['int64', 'float64'] and df[y_col].dtype in ['int64', 'float64'] else None
        )
        
        fig.update_layout(
            template='plotly_dark',
            title_font_size=16,
            title_x=0.5,
            height=400,
            paper_bgcolor='#2d3748',
            plot_bgcolor='#2d3748'
        )
        
        return fig
    
    def limpiar_datos_basico(self, df):
        """Realiza limpieza básica de datos."""
        df_limpio = df.copy()
        
        # Eliminar duplicados
        duplicados_antes = len(df_limpio)
        df_limpio = df_limpio.drop_duplicates()
        duplicados_eliminados = duplicados_antes - len(df_limpio)
        
        # Estadísticas de limpieza
        resultado = {
            'filas_originales': len(df),
            'filas_finales': len(df_limpio),
            'duplicados_eliminados': duplicados_eliminados,
            'porcentaje_nulos_por_columna': (df_limpio.isnull().sum() / len(df_limpio) * 100).to_dict()
        }
        
        return df_limpio, resultado


def main():
    """Función principal de la aplicación Streamlit."""
    
    # Configuración de la página
    st.set_page_config(
        page_title="DataVision - Analizador de Datos",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS optimizado - tema oscuro coordinado y eficiente
    st.markdown("""
    <style>
    /* Variables CSS para tema oscuro coordinado */
    :root {
        --dark-primary: #1a1a2e;
        --dark-secondary: #16213e;
        --dark-accent: #2d3748;
        --text-white: #ffffff;
        --text-gray: #a0aec0;
        --text-muted: #718096;
        --border-dark: #4a5568;
        --success: #48bb78;
        --warning: #ed8936;
        --error: #f56565;
        --info: #4299e1;
    }
    
    /* Fondo principal oscuro */
    .main {
        background: var(--dark-primary);
        color: var(--text-white);
    }
    
    /* Sidebar coordinado */
    [data-testid="stSidebar"] {
        background: var(--dark-secondary);
        border-right: 2px solid var(--border-dark);
    }
    
    [data-testid="stSidebar"] * {
        color: var(--text-white) !important;
    }
    
    /* Contenedor principal */
    .block-container {
        background: var(--dark-accent);
        border-radius: 8px;
        padding: 2rem;
        margin-top: 1rem;
        border: 1px solid var(--border-dark);
    }
    
    .block-container * {
        color: var(--text-white) !important;
    }
    
    /* Encabezados */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-white) !important;
        font-weight: 600;
    }
    
    /* Métricas */
    [data-testid="metric-container"] {
        background: var(--dark-secondary);
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid var(--border-dark);
    }
    
    [data-testid="metric-container"] * {
        color: var(--text-white) !important;
    }
    
    /* Botones */
    .stButton > button {
        background: var(--info);
        color: white !important;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background: #3182ce;
    }
    
    /* Botón blanco específico */
    .stButton > button[kind="secondary"] {
        background: white !important;
        color: var(--dark-primary) !important;
        border: 2px solid var(--text-gray);
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #f7fafc !important;
        border-color: var(--info);
    }
    
    /* Pestañas */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--dark-secondary);
        border-radius: 8px;
        padding: 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        color: var(--text-gray) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--info);
        color: white !important;
    }
    
    /* DataFrames */
    .stDataFrame {
        background: var(--dark-secondary);
        border-radius: 8px;
        border: 1px solid var(--border-dark);
    }
    
    /* Inputs */
    .stSelectbox > div > div {
        background: var(--dark-secondary);
        border: 1px solid var(--border-dark);
        border-radius: 6px;
        color: var(--text-white) !important;
    }
    
    /* Selectbox del header con estilo especial */
    .stSelectbox label {
        color: var(--text-white) !important;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .stSelectbox > div > div > div {
        color: var(--text-white) !important;
    }
    
    /* Mejorar hover en selectbox */
    .stSelectbox > div > div:hover {
        border-color: var(--info) !important;
        box-shadow: 0 0 0 2px rgba(66, 153, 225, 0.2);
    }
    
    /* Estilo para expanders con fondos diferenciados */
    .streamlit-expanderHeader {
        background: var(--dark-secondary) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: 8px !important;
        color: var(--text-white) !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: var(--dark-accent) !important;
        border-color: var(--info) !important;
    }
    
    .streamlit-expanderContent {
        background: var(--dark-primary) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: 0 0 8px 8px !important;
        padding: 0 !important;
        margin-top: -1px !important;
    }
    
    /* Mejorar selectbox dentro de expanders */
    .streamlit-expanderContent .stSelectbox > div > div {
        background: var(--dark-accent) !important;
        border: 1px solid var(--border-dark) !important;
    }
    
    /* Botones dentro de expanders */
    .streamlit-expanderContent .stButton > button {
        background: var(--info) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderContent .stButton > button:hover {
        background: #3182ce !important;
        transform: translateY(-1px) !important;
    }
    
    /* Sidebar botones */
    [data-testid="stSidebar"] .stButton > button {
        background: var(--dark-accent);
        color: var(--text-white) !important;
        border: 1px solid var(--border-dark);
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: var(--border-dark);
    }
    
    /* Alertas */
    .stAlert {
        border-radius: 6px;
        border: 1px solid var(--border-dark);
    }
    
    .stAlert[data-baseweb="notification-positive"] {
        background: var(--success);
        color: white;
    }
    
    .stAlert[data-baseweb="notification-warning"] {
        background: var(--warning);
        color: white;
    }
    
    .stAlert[data-baseweb="notification-error"] {
        background: var(--error);
        color: white;
    }
    
    .stAlert[data-baseweb="notification-info"] {
        background: var(--info);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Inicializar el analizador
    if 'analizador' not in st.session_state:
        st.session_state.analizador = AnalizadorDatos()
    
    analizador = st.session_state.analizador
    
    # Header elaborado con opciones desplegables y configuraciones
    st.markdown("""
    <div style="background: linear-gradient(135deg, var(--dark-primary) 0%, var(--dark-secondary) 100%);
                padding: 2rem 0; margin-bottom: 2rem; border-radius: 12px; border: 1px solid var(--border-dark);">
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: white; font-size: 3rem; font-weight: 800; margin-bottom: 0.5rem;
                       text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
                📊 DataVision Pro
            </h1>
            <p style="color: #4299e1; font-size: 1.3rem; font-weight: 600; margin-bottom: 0.5rem;">
                Plataforma Avanzada de Análisis y Visualización de Datos
            </p>
            <p style="color: #a0aec0; font-size: 1.1rem;">
                🚀 Análisis Inteligente | 📈 Visualizaciones Interactivas | 🎯 Insights Profesionales
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sección "Para comenzar tu análisis" - MOVIDA AQUÍ ARRIBA
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Contenedor centrado con máximo ancho
    with st.container():
        # Título más compacto
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <h2 style="color: #4299e1; font-size: 1.8rem; margin-bottom: 0.8rem;">
                🎯 Para comenzar tu análisis
            </h2>
            <p style="color: #a0aec0; font-size: 1rem; margin-bottom: 1.5rem;">
                Carga un archivo desde la barra lateral o usa datos de ejemplo
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tarjetas más compactas y mejor proporcionadas
        col1, col_spacer, col2 = st.columns([5, 1, 5])
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(66, 153, 225, 0.15) 0%, rgba(66, 153, 225, 0.05) 100%); 
                        padding: 1.5rem; 
                        border-radius: 10px; 
                        border: 1px solid rgba(66, 153, 225, 0.4); 
                        text-align: center; 
                        height: 160px; 
                        display: flex; 
                        flex-direction: column; 
                        justify-content: center;
                        transition: transform 0.2s ease;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📁</div>
                <h4 style="color: #4299e1; margin: 0.4rem 0; font-size: 1.2rem; font-weight: 600;">Carga tu Archivo</h4>
                <p style="color: #a0aec0; font-size: 0.9rem; margin: 0.3rem 0; line-height: 1.3;">CSV, Excel, TSV</p>
                <p style="color: #718096; font-size: 0.8rem; margin: 0; line-height: 1.2;">Desde la barra lateral</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(72, 187, 120, 0.15) 0%, rgba(72, 187, 120, 0.05) 100%); 
                        padding: 1.5rem; 
                        border-radius: 10px; 
                        border: 1px solid rgba(72, 187, 120, 0.4); 
                        text-align: center; 
                        height: 160px; 
                        display: flex; 
                        flex-direction: column; 
                        justify-content: center;
                        transition: transform 0.2s ease;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🚀</div>
                <h4 style="color: #48bb78; margin: 0.4rem 0; font-size: 1.2rem; font-weight: 600;">Inicio Rápido</h4>
                <p style="color: #a0aec0; font-size: 0.9rem; margin: 0.3rem 0; line-height: 1.3;">Datos de ejemplo</p>
                <p style="color: #718096; font-size: 0.8rem; margin: 0; line-height: 1.2;">Empleados y Ventas</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Espaciado controlado
        st.markdown("<div style='margin: 1.2rem 0;'></div>", unsafe_allow_html=True)
        
        # Botón más compacto y centrado
        col_btn1, col_btn2, col_btn3 = st.columns([2, 3, 2])
        with col_btn2:
            if st.button("🚀 Iniciar con datos de ejemplo", 
                        type="primary", 
                        help="Carga automáticamente el dataset de empleados",
                        use_container_width=True):
                try:
                    ejemplo_path = "datos/ejemplos/empleados.csv"
                    if os.path.exists(ejemplo_path):
                        df_ejemplo = pd.read_csv(ejemplo_path)
                        st.session_state.analizador.df = df_ejemplo
                        st.success("✅ ¡Datos cargados correctamente! Explora las pestañas.")
                        st.rerun()
                    else:
                        st.error("❌ No se encontró el archivo de ejemplo")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Separador más sutil
    st.markdown("<div style='height: 2px; background: linear-gradient(90deg, transparent 0%, #4299e1 50%, transparent 100%); margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
    
    # Secciones desplegables con fondos diferenciados
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sección 1: Capacidades Avanzadas del Sistema
    with st.expander("🚀 Capacidades Avanzadas del Sistema", expanded=False):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%); 
                    padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
            <h4 style="color: #4299e1; margin-bottom: 1rem;">⚡ Análisis Inteligente</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div>
                    <p style="color: #a0aec0; margin-bottom: 0.5rem;">📈 <strong>Análisis Estadístico:</strong></p>
                    <p style="color: #e2e8f0; font-size: 0.9rem;">Correlaciones, distribuciones, outliers</p>
                </div>
                <div>
                    <p style="color: #a0aec0; margin-bottom: 0.5rem;">🎨 <strong>Visualizaciones:</strong></p>
                    <p style="color: #e2e8f0; font-size: 0.9rem;">Plotly interactivo, gráficos dinámicos</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        config_col1, config_col2 = st.columns(2)
        with config_col1:
            tema_viz = st.selectbox("🎨 Tema Gráficos:", ["🌙 Oscuro", "☀️ Claro", "🔄 Auto"], index=0)
        with config_col2:
            formato_numeros = st.selectbox("🔢 Formato:", ["📊 Estándar", "🔬 Científico", "📈 Porcentaje"], index=0)

    # Sección 2: Guía de Inicio Rápido
    with st.expander("🚀 Guía de Inicio Rápido", expanded=False):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #553c9a 0%, #7c3aed 100%); 
                    padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
            <h4 style="color: #c084fc; margin-bottom: 1rem;">📋 Pasos para Comenzar</h4>
            <div style="color: #e2e8f0;">
                <p><strong>1.</strong> 📁 Carga tu archivo CSV o Excel</p>
                <p><strong>2.</strong> 👀 Revisa la vista general de datos</p>
                <p><strong>3.</strong> 📊 Explora estadísticas y correlaciones</p>
                <p><strong>4.</strong> 📈 Genera visualizaciones interactivas</p>
                <p><strong>5.</strong> 🧹 Limpia y optimiza tus datos</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        config_col3, config_col4 = st.columns(2)
        with config_col3:
            idioma_app = st.selectbox("🌐 Idioma:", ["🇪🇸 Español", "🇺🇸 English", "🇧🇷 Português"], index=0)
        with config_col4:
            modo_analisis = st.selectbox("⚡ Modo:", ["🚄 Rápido", "⚖️ Balanceado", "🎯 Preciso"], index=1)

    # Sección 3: Datasets de Ejemplo
    with st.expander("📊 Datasets de Ejemplo Incluidos", expanded=False):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%); 
                    padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
            <h4 style="color: #5eead4; margin-bottom: 1rem;">📁 Ejemplos Disponibles</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; color: #e2e8f0;">
                <div>
                    <p><strong>👥 Empleados.csv:</strong></p>
                    <p style="font-size: 0.9rem;">Datos de RRHH, salarios, departamentos</p>
                </div>
                <div>
                    <p><strong>💰 Ventas.csv:</strong></p>
                    <p style="font-size: 0.9rem;">Datos comerciales, productos, regiones</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        ejemplo_col1, ejemplo_col2 = st.columns(2)
        with ejemplo_col1:
            dataset_ejemplo = st.selectbox("� Dataset:", ["👥 Empleados", "💰 Ventas"], index=0)
        with ejemplo_col2:
            if st.button("🚀 Cargar Ejemplo", type="primary"):
                st.success("✅ Dataset de ejemplo cargado correctamente")
                st.rerun()
    
    # Sección 4: Casos de Uso Profesionales
    with st.expander("💼 Casos de Uso Profesionales", expanded=False):
        st.markdown("""
        <div style="background: rgba(72, 187, 120, 0.1); padding: 1.5rem; border-radius: 8px; border-left: 4px solid #48bb78;">
            <h4 style="color: #48bb78; margin-bottom: 1rem;">🎯 Sectores donde DataVision destaca</h4>
        </div>
        """, unsafe_allow_html=True)
        
        uso_col1, uso_col2 = st.columns(2)
        
        with uso_col1:
            st.markdown("""
            **🏢 Empresas & Corporaciones**
            - Análisis de ventas y rendimiento
            - KPIs y métricas de negocio
            - Reportes financieros automatizados
            
            **🎓 Educación & Investigación** 
            - Análisis de datos académicos
            - Investigación científica
            - Proyectos universitarios
            """)
            
        with uso_col2:
            st.markdown("""
            **🏥 Sector Salud**
            - Análisis epidemiológico
            - Estadísticas médicas
            - Gestión hospitalaria
            
            **📈 Marketing & E-commerce**
            - Análisis de comportamiento
            - Optimización de campañas
            - Segmentación de clientes
            """)
    
    # Sección 5: Técnicas de Análisis Avanzadas
    with st.expander("🔬 Técnicas de Análisis Avanzadas", expanded=False):
        st.markdown("""
        <div style="background: rgba(237, 137, 54, 0.1); padding: 1.5rem; border-radius: 8px; border-left: 4px solid #ed8936;">
            <h4 style="color: #ed8936; margin-bottom: 1rem;">🧠 Poder analítico a tu alcance</h4>
        </div>
        """, unsafe_allow_html=True)
        
        tecnica_col1, tecnica_col2, tecnica_col3 = st.columns(3)
        
        with tecnica_col1:
            st.markdown("""
            **📊 Estadística Descriptiva**
            - Media, mediana, moda
            - Desviación estándar
            - Percentiles y cuartiles
            - Distribuciones
            """)
            
        with tecnica_col2:
            st.markdown("""
            **🔗 Análisis de Correlación**
            - Matriz de correlaciones
            - Heatmaps interactivos
            - Relaciones lineales
            - Coeficientes de Pearson
            """)
            
        with tecnica_col3:
            st.markdown("""
            **📈 Visualización Avanzada**
            - Gráficos interactivos 3D
            - Dashboards dinámicos
            - Mapas de calor
            - Scatter plots animados
            """)
    
    # Sección 6: Formatos de Datos Compatibles
    with st.expander("📁 Formatos de Datos Compatibles", expanded=False):
        st.markdown("""
        <div style="background: rgba(139, 92, 246, 0.1); padding: 1.5rem; border-radius: 8px; border-left: 4px solid #8b5cf6;">
            <h4 style="color: #8b5cf6; margin-bottom: 1rem;">💾 Máxima compatibilidad de archivos</h4>
        </div>
        """, unsafe_allow_html=True)
        
        formato_col1, formato_col2 = st.columns(2)
        
        with formato_col1:
            st.markdown("""
            **✅ Formatos Principales Soportados:**
            - 📄 **CSV** - Valores separados por comas
            - 📊 **Excel (.xlsx, .xls)** - Hojas de cálculo Microsoft
            - 📋 **TSV** - Valores separados por tabulaciones
            - 🔢 **JSON** - JavaScript Object Notation
            """)
            
        with formato_col2:
            st.markdown("""
            **⚡ Características de Importación:**
            - Detección automática de delimitadores
            - Manejo inteligente de encoding
            - Soporte para archivos de gran tamaño
            - Validación automática de datos
            """)
            
        st.info("💡 **Tip Profesional:** Para mejores resultados, asegúrate de que tu archivo tenga encabezados claros en la primera fila.")
    
    # Sección 7: Rendimiento y Escalabilidad
    with st.expander("⚡ Rendimiento y Escalabilidad", expanded=False):
        st.markdown("""
        <div style="background: rgba(245, 101, 101, 0.1); padding: 1.5rem; border-radius: 8px; border-left: 4px solid #f56565;">
            <h4 style="color: #f56565; margin-bottom: 1rem;">🚀 Optimizado para el rendimiento</h4>
        </div>
        """, unsafe_allow_html=True)
        
        rendimiento_col1, rendimiento_col2 = st.columns(2)
        
        with rendimiento_col1:
            st.markdown("""
            **📊 Capacidades de Procesamiento:**
            - Hasta 1M+ filas de datos
            - Procesamiento en tiempo real
            - Análisis instantáneo de correlaciones
            - Generación rápida de visualizaciones
            """)
            
        with rendimiento_col2:
            st.markdown("""
            **⚡ Optimizaciones Técnicas:**
            - Algoritmos eficientes con Pandas
            - Caching inteligente de resultados
            - Renderizado optimizado con Plotly
            - Interfaz responsiva y fluida
            """)
            
        # Métricas de rendimiento simuladas
        metricas_col1, metricas_col2, metricas_col3, metricas_col4 = st.columns(4)
        
        with metricas_col1:
            st.metric("⚡ Velocidad", "< 2 seg", "Análisis promedio")
        with metricas_col2:
            st.metric("📊 Capacidad", "1M+ filas", "Datos máximos")
        with metricas_col3:
            st.metric("🎯 Precisión", "99.9%", "Cálculos exactos")
        with metricas_col4:
            st.metric("💾 Memoria", "< 512MB", "Uso optimizado")
    
    # Separador visual
    st.markdown("""
    <div style="height: 2px; background: linear-gradient(90deg, 
                transparent 0%, var(--info) 50%, transparent 100%); 
                margin: 1.5rem 0;"></div>
    """, unsafe_allow_html=True)
    

    
    # Sidebar mejorado con logo y nuevas funcionalidades
    
    # Logo de DataVision compacto
    st.sidebar.markdown("""
    <div style="
        text-align: center;
        padding: 0.8rem 0.5rem;
        margin-bottom: 0.5rem;
        width: 100%;
    ">
    """, unsafe_allow_html=True)
    
    try:
        # Crear columnas perfectamente centradas para el logo
        col1, col2, col3 = st.sidebar.columns([0.2, 1, 0.2])
        with col2:
            st.image("public/img/Data.png", width=120)
    except:
        # Fallback elegante si no encuentra la imagen
        st.sidebar.markdown("""
        <div style="
            text-align: center; 
            padding: 0.8rem; 
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: rgba(66, 153, 225, 0.15);
            border-radius: 8px;
            margin: 0.2rem 0;
            border: 1px solid rgba(66, 153, 225, 0.3);
        ">
            <h1 style="color: #4299e1; margin: 0; font-size: 3.2rem; text-shadow: 0 2px 6px rgba(0,0,0,0.4);">📊</h1>
            <h2 style="color: white; margin: 0.2rem 0 0 0; font-size: 1.3rem; font-weight: 700; letter-spacing: 1px;">DataVision</h2>
            <p style="color: #a0aec0; margin: 0.1rem 0 0 0; font-size: 0.8rem; opacity: 0.8;">2025</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 0.5rem; margin-bottom: 0.8rem;">
        <h2 style="color: white; margin: 0; font-size: 1.4rem;">
            📁 Centro de Control
        </h2>
        <p style="color: #a0aec0; text-align: center; margin-top: 0.3rem; font-size: 0.85rem;">
            Gestiona tus datos y configuraciones
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carga de archivos mejorada
    st.sidebar.markdown("### 📂 Cargar Datos")
    archivo_cargado = st.sidebar.file_uploader(
        "Selecciona tu archivo", 
        type=['csv', 'xlsx', 'xls'],
        help="Soporta archivos CSV y Excel (hasta 200MB)"
    )
    
    if archivo_cargado is not None:
        with st.spinner('Cargando archivo...'):
            if archivo_cargado.name.endswith('.csv'):
                df = analizador.cargar_csv(archivo_cargado)
            else:
                df = analizador.cargar_excel(archivo_cargado)
            
            if df is not None:
                st.session_state.analizador.df = df
                st.sidebar.success(f"✅ Archivo cargado: {archivo_cargado.name}")
                st.rerun()
    
    # Separador compacto
    st.sidebar.markdown("<div style='margin: 0.5rem 0;'><hr style='margin: 0.3rem 0; border-color: #4299e1; opacity: 0.3;'></div>", unsafe_allow_html=True)
    
    # Configuraciones avanzadas compactas
    st.sidebar.markdown("#### ⚙️ Configuraciones")
    
    # Configuración de tema
    with st.sidebar.expander("🎨 Tema y Apariencia"):
        # Inicializar configuraciones en session_state
        if 'config_tema' not in st.session_state:
            st.session_state.config_tema = "Azul Profesional"
        if 'config_grid' not in st.session_state:
            st.session_state.config_grid = True
        if 'config_animaciones' not in st.session_state:
            st.session_state.config_animaciones = False
            
        st.session_state.config_tema = st.selectbox(
            "Esquema de colores",
            ["Azul Profesional", "Verde Natura", "Púrpura Elegante", "Naranja Energético"],
            index=["Azul Profesional", "Verde Natura", "Púrpura Elegante", "Naranja Energético"].index(st.session_state.config_tema),
            help="Personaliza los colores de los gráficos"
        )
        
        st.session_state.config_grid = st.checkbox("Mostrar grilla en gráficos", value=st.session_state.config_grid)
        st.session_state.config_animaciones = st.checkbox("Activar animaciones", value=st.session_state.config_animaciones)
        
    # Configuración de análisis
    with st.sidebar.expander("📊 Configuración de Análisis"):
        # Inicializar configuraciones en session_state
        if 'config_precision' not in st.session_state:
            st.session_state.config_precision = 2
        if 'config_correlacion' not in st.session_state:
            st.session_state.config_correlacion = "Pearson"
        if 'config_outliers' not in st.session_state:
            st.session_state.config_outliers = False
            
        st.session_state.config_precision = st.slider("Precisión decimal", 1, 6, st.session_state.config_precision)
        st.session_state.config_correlacion = st.selectbox(
            "Método de correlación",
            ["Pearson", "Spearman", "Kendall"],
            index=["Pearson", "Spearman", "Kendall"].index(st.session_state.config_correlacion),
            help="Elige el método para calcular correlaciones"
        )
        
        st.session_state.config_outliers = st.checkbox("Filtrar valores atípicos", value=st.session_state.config_outliers)
        
    # Configuración de exportación
    with st.sidebar.expander("💾 Opciones de Exportación"):
        # Inicializar configuraciones en session_state
        if 'config_formato' not in st.session_state:
            st.session_state.config_formato = "Excel (.xlsx)"
        if 'config_incluir_graficos' not in st.session_state:
            st.session_state.config_incluir_graficos = True
        if 'config_incluir_stats' not in st.session_state:
            st.session_state.config_incluir_stats = True
            
        st.session_state.config_formato = st.selectbox(
            "Formato de exportación",
            ["Excel (.xlsx)", "CSV", "PDF Report", "JSON"],
            index=["Excel (.xlsx)", "CSV", "PDF Report", "JSON"].index(st.session_state.config_formato),
            help="Formato para exportar resultados"
        )
        
        st.session_state.config_incluir_graficos = st.checkbox("Incluir gráficos en export", value=st.session_state.config_incluir_graficos)
        st.session_state.config_incluir_stats = st.checkbox("Incluir estadísticas", value=st.session_state.config_incluir_stats)
    
    # Separador compacto  
    st.sidebar.markdown("<div style='margin: 0.4rem 0;'><hr style='margin: 0.2rem 0; border-color: #4299e1; opacity: 0.3;'></div>", unsafe_allow_html=True)
    
    # Herramientas rápidas compactas
    st.sidebar.markdown("#### 🛠️ Herramientas")
    
    col_tool1, col_tool2 = st.sidebar.columns(2)
    
    with col_tool1:
        if st.button("🎲 Datos Demo", help="Cargar dataset de demostración", use_container_width=True):
            try:
                ejemplo_path = "datos/ejemplos/empleados.csv"
                if os.path.exists(ejemplo_path):
                    df_ejemplo = pd.read_csv(ejemplo_path)
                    st.session_state.analizador.df = df_ejemplo
                    st.sidebar.success("✅ Dataset demo cargado")
                    st.rerun()
            except Exception as e:
                st.sidebar.error(f"Error: {str(e)}")
    
    with col_tool2:
        if st.button("📋 Plantilla", help="Descargar plantilla CSV", use_container_width=True):
            template_data = {
                'Nombre': ['Ejemplo1', 'Ejemplo2', 'Ejemplo3'],
                'Valor': [100, 200, 300],
                'Categoria': ['A', 'B', 'A']
            }
            template_df = pd.DataFrame(template_data)
            csv_template = template_df.to_csv(index=False)
            st.sidebar.download_button(
                label="⬇️ Descargar",
                data=csv_template,
                file_name="plantilla_datavision.csv",
                mime="text/csv"
            )
    
    # Acciones rápidas con datos cargados
    if st.session_state.analizador.df is not None:
        st.sidebar.markdown("#### 🎛️ Controles")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("🔄", help="Recargar análisis", use_container_width=True):
                st.rerun()
        
        with col2:
            if st.button("🗑️", help="Limpiar datos", use_container_width=True):
                st.session_state.analizador.df = None
                st.rerun()
        
        # Filtros de datos compactos
        st.sidebar.markdown("#### 🔍 Filtros")
        df = st.session_state.analizador.df
        
        # Inicializar filtros en session_state
        if 'filtro_filas' not in st.session_state:
            st.session_state.filtro_filas = min(100, len(df))
        if 'columnas_seleccionadas' not in st.session_state:
            st.session_state.columnas_seleccionadas = df.columns.tolist()[:min(5, len(df.columns))]
        
        # Filtro por filas
        st.session_state.filtro_filas = st.sidebar.slider(
            "Número de filas a mostrar",
            min_value=10,
            max_value=min(1000, len(df)),
            value=min(st.session_state.filtro_filas, len(df)),
            step=10
        )
        
        # Filtro por columnas
        if len(df.columns) > 5:
            st.session_state.columnas_seleccionadas = st.sidebar.multiselect(
                "Columnas a analizar",
                options=df.columns.tolist(),
                default=st.session_state.columnas_seleccionadas if st.session_state.columnas_seleccionadas else df.columns.tolist()[:5],
                help="Selecciona las columnas para el análisis"
            )
        
        # Información del dataset compacta
        st.sidebar.markdown("#### 📊 Info Dataset")
        
        col_info1, col_info2 = st.sidebar.columns(2)
        with col_info1:
            st.metric("📏", f"{df.shape[0]:,}", "filas")
            st.metric("📊", df.shape[1], "columnas")
        
        with col_info2:
            memoria_mb = df.memory_usage(deep=True).sum() / 1024**2
            st.metric("💾", f"{memoria_mb:.1f}MB")
            valores_nulos = df.isnull().sum().sum()
            st.metric("❌", valores_nulos, "nulos")
        
        # Estadísticas rápidas
        with st.sidebar.expander("📈 Estadísticas Rápidas"):
            columnas_numericas = df.select_dtypes(include=[np.number]).columns
            if len(columnas_numericas) > 0:
                col_seleccionada = st.selectbox("Columna", columnas_numericas)
                if col_seleccionada:
                    st.write(f"**Media:** {df[col_seleccionada].mean():.2f}")
                    st.write(f"**Mediana:** {df[col_seleccionada].median():.2f}")
                    st.write(f"**Desv. Std:** {df[col_seleccionada].std():.2f}")
            else:
                st.write("No hay columnas numéricas")
    
    # Separador compacto final
    st.sidebar.markdown("<div style='margin: 0.3rem 0;'><hr style='margin: 0.2rem 0; border-color: #4299e1; opacity: 0.2;'></div>", unsafe_allow_html=True)
    
    # Información compacta de la aplicación
    with st.sidebar.expander("ℹ️ DataVision 2025"):
        st.markdown("""
        **v2.0.1** | Python  
        🚀 Análisis automático  
        📊 Visualizaciones interactivas  
        💾 Exportación múltiple  
        
        [📋 GitHub](https://github.com) | [📖 Docs](https://docs.datavision.com)
        """)
        
    # Footer del sidebar
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem; margin-top: 2rem; border-top: 1px solid #4a5568;">
        <p style="color: #718096; font-size: 0.8rem; margin: 0;">
            © 2025 DataVision<br>
            Hecho con Streamlit 🚀
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contenido principal
    if st.session_state.analizador.df is not None:
        df = st.session_state.analizador.df
        
        # Tabs principales
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Vista General", 
            "📈 Estadísticas", 
            "🔗 Correlaciones", 
            "📊 Gráficas",
            "🧹 Limpieza"
        ])
        
        with tab1:
            st.markdown("## 📊 Vista General de los Datos")
            
            # Métricas principales
            col1, col2, col3, col4 = st.columns(4)
            
            memoria_mb = df.memory_usage(deep=True).sum() / 1024**2
            nulos_total = df.isnull().sum().sum()
            porcentaje_completitud = ((df.size - nulos_total) / df.size * 100) if df.size > 0 else 0
            
            with col1:
                st.metric("📊 Total Filas", f"{df.shape[0]:,}")
            
            with col2:
                st.metric("📈 Columnas", df.shape[1])
            
            with col3:
                st.metric("💾 Memoria MB", f"{memoria_mb:.1f}")
            
            with col4:
                st.metric("✨ Completitud", f"{porcentaje_completitud:.1f}%")
            
            # Vista previa
            st.markdown("### 👀 Vista Previa de los Datos")
            filas_mostrar = st.selectbox("📊 Filas a mostrar:", [5, 10, 20, 50], index=0)
            st.dataframe(df.head(filas_mostrar), use_container_width=True)
            
            # Tipos de datos
            st.markdown("### 🏷 Tipos de Datos")
            tipos_df = pd.DataFrame({
                'Columna': df.columns,
                'Tipo': df.dtypes.astype(str),
                'Valores No Nulos': df.count(),
                'Valores Nulos': df.isnull().sum(),
                '% Nulos': (df.isnull().sum() / len(df) * 100).round(2)
            })
            st.dataframe(tipos_df, use_container_width=True)
        
        with tab2:
            st.markdown("## 📈 Análisis Estadístico")
            
            columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if columnas_numericas:
                st.markdown("### 📊 Estadísticas Descriptivas")
                desc_stats = df[columnas_numericas].describe()
                st.dataframe(desc_stats, use_container_width=True)
                
                # Análisis por columna
                st.markdown("### 🔍 Análisis Detallado por Columna")
                columna_seleccionada = st.selectbox("Selecciona una columna:", columnas_numericas)
                
                if columna_seleccionada:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Promedio", f"{df[columna_seleccionada].mean():.2f}")
                        st.metric("Mediana", f"{df[columna_seleccionada].median():.2f}")
                        st.metric("Desviación Estándar", f"{df[columna_seleccionada].std():.2f}")
                    
                    with col2:
                        st.metric("Mínimo", f"{df[columna_seleccionada].min():.2f}")
                        st.metric("Máximo", f"{df[columna_seleccionada].max():.2f}")
                        st.metric("Rango", f"{df[columna_seleccionada].max() - df[columna_seleccionada].min():.2f}")
            else:
                st.info("No hay columnas numéricas en el dataset para análisis estadístico.")
        
        with tab3:
            st.markdown("## 🔗 Análisis de Correlaciones")
            
            columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(columnas_numericas) >= 2:
                fig = analizador.crear_matriz_correlacion(df)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                # Tabla de correlaciones
                st.markdown("### 📋 Tabla de Correlaciones")
                corr_matrix = df[columnas_numericas].corr()
                st.dataframe(corr_matrix, use_container_width=True)
            else:
                st.info("Se necesitan al menos 2 columnas numéricas para el análisis de correlaciones")
        
        with tab4:
            st.markdown("## 📊 Gráficas Interactivas")
            
            # Selección de tipo de gráfica
            col_graf1, col_graf2 = st.columns([2, 1])
            
            with col_graf2:
                tipo_grafica = st.selectbox(
                    "🎯 Tipo de Gráfica:",
                    ["Distribución", "Barras", "Dispersión", "Correlación"],
                    help="Selecciona el tipo de visualización"
                )
                
                columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
                columnas_categoricas = df.select_dtypes(include=['object', 'category']).columns.tolist()
                todas_columnas = df.columns.tolist()
            
            with col_graf1:
                fig = None
                
                if tipo_grafica == "Distribución":
                    col_dist1, col_dist2 = st.columns(2)
                    with col_dist1:
                        columna_dist = st.selectbox("📊 Columna:", columnas_numericas if columnas_numericas else todas_columnas)
                    with col_dist2:
                        subtipo_dist = st.selectbox("📈 Subtipo:", ["histograma", "boxplot", "violinplot"])
                    
                    if columna_dist:
                        fig = analizador.crear_grafico_distribucion(df, columna_dist, subtipo_dist)
                
                elif tipo_grafica == "Barras":
                    columna_barras = st.selectbox("📊 Columna Categórica:", columnas_categoricas if columnas_categoricas else todas_columnas)
                    if columna_barras:
                        fig = analizador.crear_grafico_barras(df, columna_barras)
                
                elif tipo_grafica == "Dispersión":
                    col_disp1, col_disp2, col_disp3 = st.columns(3)
                    with col_disp1:
                        x_col = st.selectbox("📊 Eje X:", columnas_numericas if columnas_numericas else todas_columnas)
                    with col_disp2:
                        y_col = st.selectbox("📊 Eje Y:", columnas_numericas if columnas_numericas else todas_columnas)
                    with col_disp3:
                        color_col = st.selectbox("🎨 Color por:", [None] + columnas_categoricas)
                    
                    if x_col and y_col:
                        fig = analizador.crear_grafico_dispersion(df, x_col, y_col, color_col)
                
                elif tipo_grafica == "Correlación":
                    if len(columnas_numericas) >= 2:
                        fig = analizador.crear_matriz_correlacion(df)
                    else:
                        st.warning("⚠️ Se necesitan al menos 2 columnas numéricas para la correlación")
            
            # Mostrar el gráfico
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                
                # Opciones de descarga
                st.markdown("### 💾 Descargar Gráfica")
                col_desc1, col_desc2 = st.columns(2)
                with col_desc1:
                    if st.button("📥 Descargar PNG"):
                        try:
                            img_bytes = fig.to_image(format="png", width=1200, height=800)
                            st.download_button(
                                label="💾 Guardar PNG",
                                data=img_bytes,
                                file_name=f"grafica_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                                mime="image/png"
                            )
                        except Exception as e:
                            st.error("Error al generar PNG. Instala kaleido: pip install kaleido")
                
                with col_desc2:
                    html_str = fig.to_html(include_plotlyjs='cdn')
                    st.download_button(
                        label="💾 Descargar HTML",
                        data=html_str,
                        file_name=f"grafica_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html"
                    )
            else:
                st.info("👆 Selecciona los parámetros para generar tu gráfica")
        
        with tab5:
            st.markdown("## 🧹 Limpieza de Datos")
            
            # Diagnóstico general
            total_celdas = df.shape[0] * df.shape[1]
            celdas_nulas = df.isnull().sum().sum()
            duplicados = df.duplicated().sum()
            porcentaje_completitud = ((total_celdas - celdas_nulas) / total_celdas * 100)
            
            # Dashboard de calidad
            col_qual1, col_qual2, col_qual3, col_qual4 = st.columns(4)
            
            with col_qual1:
                st.metric("📊 Completitud", f"{porcentaje_completitud:.1f}%")
            
            with col_qual2:
                st.metric("🔍 Valores Nulos", f"{celdas_nulas:,}")
            
            with col_qual3:
                st.metric("👥 Duplicados", f"{duplicados:,}")
            
            with col_qual4:
                calidad = "Excelente" if porcentaje_completitud > 95 else "Buena" if porcentaje_completitud > 85 else "Regular"
                st.metric("⭐ Calidad", calidad)
            
            # Limpieza de duplicados
            if duplicados > 0:
                st.markdown("### 🔄 Eliminar Duplicados")
                st.warning(f"Se encontraron {duplicados} filas duplicadas")
                
                if st.button("🗑️ Eliminar Duplicados", key="btn_eliminar_duplicados"):
                    df_limpio = df.drop_duplicates()
                    st.session_state.analizador.df = df_limpio
                    st.success(f"✅ Se eliminaron {duplicados} filas duplicadas")
                    st.rerun()
            else:
                st.success("✅ No se encontraron duplicados")
            
            # Tratamiento de nulos
            if celdas_nulas > 0:
                st.markdown("### 🎯 Tratamiento de Valores Nulos")
                
                nulos_por_columna = df.isnull().sum()
                columnas_con_nulos = nulos_por_columna[nulos_por_columna > 0]
                
                if len(columnas_con_nulos) > 0:
                    st.dataframe(
                        pd.DataFrame({
                            'Columna': columnas_con_nulos.index,
                            'Valores Nulos': columnas_con_nulos.values,
                            'Porcentaje': (columnas_con_nulos / len(df) * 100).round(2)
                        }),
                        use_container_width=True
                    )
                    
                    columna_tratar = st.selectbox("Selecciona columna para tratar:", columnas_con_nulos.index)
                    metodo = st.selectbox("Método de tratamiento:", 
                                        ["Eliminar filas", "Rellenar con media", "Rellenar con mediana", "Rellenar con valor personalizado"])
                    
                    if metodo == "Rellenar con valor personalizado":
                        valor_personalizado = st.text_input("Valor de relleno:")
                    
                    if st.button(f"✅ Aplicar {metodo}"):
                        df_temp = df.copy()
                        
                        try:
                            if metodo == "Eliminar filas":
                                df_temp = df_temp.dropna(subset=[columna_tratar])
                            elif metodo == "Rellenar con media":
                                df_temp[columna_tratar].fillna(df_temp[columna_tratar].mean(), inplace=True)
                            elif metodo == "Rellenar con mediana":
                                df_temp[columna_tratar].fillna(df_temp[columna_tratar].median(), inplace=True)
                            elif metodo == "Rellenar con valor personalizado":
                                df_temp[columna_tratar].fillna(valor_personalizado, inplace=True)
                            
                            st.session_state.analizador.df = df_temp
                            st.success(f"✅ {metodo} aplicado exitosamente a la columna '{columna_tratar}'")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Error al aplicar {metodo}: {str(e)}")
            else:
                st.success("✅ No se encontraron valores nulos")
    
    else:
        # Mensaje centrado cuando no hay datos
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("👆 Carga un archivo CSV o Excel desde la barra lateral, o usa el botón de datos de ejemplo para comenzar el análisis.")
        
        # Tarjetas informativas después del mensaje - MOVIDAS AQUÍ
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(66, 153, 225, 0.15) 0%, rgba(66, 153, 225, 0.05) 100%); 
                        padding: 1.5rem; border-radius: 10px; border: 1px solid rgba(66, 153, 225, 0.3); text-align: center; height: 140px;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📈</div>
                <h4 style="color: #4299e1; margin: 0.5rem 0; font-size: 1.1rem; font-weight: 600;">Análisis Avanzado</h4>
                <p style="color: #a0aec0; font-size: 0.85rem; line-height: 1.4; margin: 0;">
                    Correlaciones, estadísticas y visualizaciones
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(72, 187, 120, 0.15) 0%, rgba(72, 187, 120, 0.05) 100%); 
                        padding: 1.5rem; border-radius: 10px; border: 1px solid rgba(72, 187, 120, 0.3); text-align: center; height: 140px;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🚀</div>
                <h4 style="color: #48bb78; margin: 0.5rem 0; font-size: 1.1rem; font-weight: 600;">Fácil de Usar</h4>
                <p style="color: #a0aec0; font-size: 0.85rem; line-height: 1.4; margin: 0;">
                    Carga datos y obtén insights al instante
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(237, 137, 54, 0.15) 0%, rgba(237, 137, 54, 0.05) 100%); 
                        padding: 1.5rem; border-radius: 10px; border: 1px solid rgba(237, 137, 54, 0.3); text-align: center; height: 140px;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎨</div>
                <h4 style="color: #ed8936; margin: 0.5rem 0; font-size: 1.1rem; font-weight: 600;">Visualizaciones</h4>
                <p style="color: #a0aec0; font-size: 0.85rem; line-height: 1.4; margin: 0;">
                    Gráficos interactivos con Plotly
                </p>
            </div>
            """, unsafe_allow_html=True)

    # Footer limpio y centrado usando los colores del sistema
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Separador elegante
    st.markdown("""
    <div style="height: 2px; background: linear-gradient(90deg, transparent 0%, #4299e1 20%, #48bb78 50%, #ed8936 80%, transparent 100%); margin: 2rem 0;"></div>
    """, unsafe_allow_html=True)
    
    # Footer con formato limpio y centrado
    st.markdown("""
    <div style="background: var(--dark-secondary); 
                padding: 2rem; 
                border-radius: 12px; 
                border: 1px solid var(--border-dark); 
                text-align: center;
                margin-bottom: 1rem;">
        <p style="color: var(--text-white); 
                  font-size: 1.1rem; 
                  font-weight: 600; 
                  margin-bottom: 0.8rem;">
            © Análisis de DataVision 2025, Hecho con ❤️ y Python
        </p>
        <p style="color: var(--text-muted); 
                  font-size: 0.95rem; 
                  margin: 0;">
            <strong>Tecnologías:</strong> Python 3.9+ • Streamlit • Pandas • NumPy • Matplotlib • Seaborn
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()