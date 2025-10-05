"""
Módulo de exportación a PDF
Funciones para generar reportes en PDF con gráficos y tablas.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import plotly.graph_objects as go
import plotly.io as pio
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import os
import tempfile


class GeneradorReportePDF:
    """Clase para generar reportes PDF completos."""
    
    def __init__(self, nombre_archivo: str, titulo: str = "Reporte de Análisis de Datos"):
        """
        Inicializa el generador de reportes PDF.
        
        Args:
            nombre_archivo: Nombre del archivo PDF a generar
            titulo: Título del reporte
        """
        self.nombre_archivo = nombre_archivo
        self.titulo = titulo
        self.elementos = []
        self.estilos = getSampleStyleSheet()
        self._crear_estilos_personalizados()
    
    def _crear_estilos_personalizados(self):
        """Crea estilos personalizados para el documento."""
        # Estilo para el título principal
        self.estilos.add(ParagraphStyle(
            name='TituloPersonalizado',
            parent=self.estilos['Title'],
            fontSize=24,
            textColor=colors.darkblue,
            spaceAfter=30,
            alignment=1  # Centrado
        ))
        
        # Estilo para subtítulos
        self.estilos.add(ParagraphStyle(
            name='SubtituloPersonalizado',
            parent=self.estilos['Heading1'],
            fontSize=16,
            textColor=colors.darkblue,
            spaceBefore=20,
            spaceAfter=12
        ))
        
        # Estilo para texto normal
        self.estilos.add(ParagraphStyle(
            name='TextoPersonalizado',
            parent=self.estilos['Normal'],
            fontSize=10,
            spaceAfter=12,
            alignment=0  # Justificado
        ))
    
    def agregar_portada(self, autor: str = "DataVision", descripcion: str = ""):
        """Agrega una portada al reporte."""
        # Título principal
        self.elementos.append(Spacer(1, 2*inch))
        self.elementos.append(Paragraph(self.titulo, self.estilos['TituloPersonalizado']))
        self.elementos.append(Spacer(1, 0.5*inch))
        
        # Información adicional
        if descripcion:
            self.elementos.append(Paragraph(descripcion, self.estilos['TextoPersonalizado']))
            self.elementos.append(Spacer(1, 0.3*inch))
        
        # Información del documento
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        info_doc = f"""
        <b>Autor:</b> {autor}<br/>
        <b>Fecha de generación:</b> {fecha_actual}<br/>
        <b>Herramienta:</b> DataVision - Analizador de Datos Interactivo
        """
        self.elementos.append(Paragraph(info_doc, self.estilos['TextoPersonalizado']))
        self.elementos.append(PageBreak())
    
    def agregar_seccion(self, titulo: str, contenido: str = ""):
        """Agrega una nueva sección al reporte."""
        self.elementos.append(Paragraph(titulo, self.estilos['SubtituloPersonalizado']))
        if contenido:
            self.elementos.append(Paragraph(contenido, self.estilos['TextoPersonalizado']))
    
    def agregar_tabla_dataframe(self, df: pd.DataFrame, titulo: str = "", 
                               max_filas: int = 20, max_columnas: int = 8):
        """
        Agrega una tabla basada en un DataFrame.
        
        Args:
            df: DataFrame a incluir
            titulo: Título de la tabla
            max_filas: Máximo número de filas a mostrar
            max_columnas: Máximo número de columnas a mostrar
        """
        if titulo:
            self.elementos.append(Paragraph(titulo, self.estilos['SubtituloPersonalizado']))
        
        # Limitar tamaño del DataFrame
        df_mostrar = df.iloc[:max_filas, :max_columnas].copy()
        
        # Preparar datos para la tabla
        datos_tabla = [df_mostrar.columns.tolist()]
        for _, fila in df_mostrar.iterrows():
            fila_formateada = []
            for valor in fila:
                if pd.isna(valor):
                    fila_formateada.append("N/A")
                elif isinstance(valor, float):
                    fila_formateada.append(f"{valor:.2f}")
                else:
                    fila_formateada.append(str(valor))
            datos_tabla.append(fila_formateada)
        
        # Crear tabla
        tabla = Table(datos_tabla)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        self.elementos.append(tabla)
        
        # Agregar nota si se truncaron datos
        if len(df) > max_filas or len(df.columns) > max_columnas:
            nota = f"Nota: Se muestran las primeras {min(max_filas, len(df))} filas y {min(max_columnas, len(df.columns))} columnas del dataset completo."
            self.elementos.append(Spacer(1, 6))
            self.elementos.append(Paragraph(nota, self.estilos['TextoPersonalizado']))
        
        self.elementos.append(Spacer(1, 12))
    
    def agregar_grafico_plotly(self, fig: go.Figure, titulo: str = "", 
                              ancho: int = 6, alto: int = 4):
        """
        Agrega un gráfico de Plotly al PDF.
        
        Args:
            fig: Figura de Plotly
            titulo: Título del gráfico
            ancho: Ancho en pulgadas
            alto: Alto en pulgadas
        """
        if titulo:
            self.elementos.append(Paragraph(titulo, self.estilos['SubtituloPersonalizado']))
        
        # Crear archivo temporal para la imagen
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            # Exportar gráfico como imagen
            pio.write_image(fig, tmp_file.name, width=ancho*100, height=alto*100, scale=2)
            
            # Agregar imagen al PDF
            imagen = Image(tmp_file.name, width=ancho*inch, height=alto*inch)
            self.elementos.append(imagen)
            self.elementos.append(Spacer(1, 12))
            
            # Eliminar archivo temporal
            os.unlink(tmp_file.name)
    
    def agregar_grafico_matplotlib(self, fig: plt.Figure, titulo: str = ""):
        """
        Agrega un gráfico de Matplotlib al PDF.
        
        Args:
            fig: Figura de Matplotlib
            titulo: Título del gráfico
        """
        if titulo:
            self.elementos.append(Paragraph(titulo, self.estilos['SubtituloPersonalizado']))
        
        # Crear archivo temporal para la imagen
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            fig.savefig(tmp_file.name, dpi=300, bbox_inches='tight')
            
            # Agregar imagen al PDF
            imagen = Image(tmp_file.name, width=6*inch, height=4*inch)
            self.elementos.append(imagen)
            self.elementos.append(Spacer(1, 12))
            
            # Eliminar archivo temporal
            os.unlink(tmp_file.name)
    
    def agregar_texto(self, texto: str):
        """Agrega un párrafo de texto al reporte."""
        self.elementos.append(Paragraph(texto, self.estilos['TextoPersonalizado']))
        self.elementos.append(Spacer(1, 12))
    
    def agregar_lista(self, items: List[str], titulo: str = ""):
        """Agrega una lista con viñetas al reporte."""
        if titulo:
            self.elementos.append(Paragraph(titulo, self.estilos['SubtituloPersonalizado']))
        
        for item in items:
            texto_item = f"• {item}"
            self.elementos.append(Paragraph(texto_item, self.estilos['TextoPersonalizado']))
    
    def generar_pdf(self):
        """Genera el archivo PDF con todos los elementos agregados."""
        doc = SimpleDocTemplate(
            self.nombre_archivo,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        doc.build(self.elementos)
        print(f"Reporte PDF generado: {self.nombre_archivo}")


def generar_reporte_estadisticas(df: pd.DataFrame, nombre_archivo: str, 
                                incluir_graficos: bool = True) -> str:
    """
    Genera un reporte completo de estadísticas en PDF.
    
    Args:
        df: DataFrame a analizar
        nombre_archivo: Nombre del archivo PDF
        incluir_graficos: Si incluir gráficos en el reporte
    
    Returns:
        Ruta del archivo generado
    """
    from ..analisis.estadisticas import estadisticas_basicas, resumen_dataset
    from ..visualizacion.tablas import (tabla_estadisticas_descriptivas, 
                                       tabla_informacion_dataset, 
                                       tabla_valores_nulos)
    
    # Crear generador de reporte
    reporte = GeneradorReportePDF(nombre_archivo, "Reporte de Análisis Estadístico")
    
    # Portada
    reporte.agregar_portada(
        descripcion="Análisis estadístico completo del dataset proporcionado."
    )
    
    # 1. Información general del dataset
    reporte.agregar_seccion("1. Información General del Dataset")
    tabla_info = tabla_informacion_dataset(df)
    reporte.agregar_tabla_dataframe(tabla_info, "Características del Dataset")
    
    # 2. Estadísticas descriptivas
    reporte.agregar_seccion("2. Estadísticas Descriptivas")
    try:
        tabla_stats = tabla_estadisticas_descriptivas(df)
        reporte.agregar_tabla_dataframe(tabla_stats, "Estadísticas por Variable")
    except ValueError as e:
        reporte.agregar_texto(f"No se pudieron calcular estadísticas descriptivas: {str(e)}")
    
    # 3. Análisis de valores nulos
    reporte.agregar_seccion("3. Análisis de Valores Nulos")
    tabla_nulos = tabla_valores_nulos(df)
    reporte.agregar_tabla_dataframe(tabla_nulos, "Valores Nulos por Columna")
    
    # 4. Muestra de datos
    reporte.agregar_seccion("4. Muestra de Datos")
    reporte.agregar_tabla_dataframe(df.head(10), "Primeras 10 filas del dataset")
    
    # 5. Gráficos (si se solicitan)
    if incluir_graficos:
        reporte.agregar_seccion("5. Visualizaciones")
        
        try:
            from ..visualizacion.graficos import dashboard_exploratorio
            graficos = dashboard_exploratorio(df)
            
            for nombre_grafico, fig in graficos.items():
                titulo_grafico = nombre_grafico.replace('_', ' ').title()
                reporte.agregar_grafico_plotly(fig, f"Gráfico: {titulo_grafico}")
        except Exception as e:
            reporte.agregar_texto(f"No se pudieron generar gráficos: {str(e)}")
    
    # Generar PDF
    reporte.generar_pdf()
    return nombre_archivo


def generar_reporte_correlaciones(df: pd.DataFrame, nombre_archivo: str) -> str:
    """
    Genera un reporte específico de análisis de correlaciones.
    
    Args:
        df: DataFrame a analizar
        nombre_archivo: Nombre del archivo PDF
    
    Returns:
        Ruta del archivo generado
    """
    from ..analisis.correlaciones import analisis_correlacion_completo
    from ..visualizacion.tablas import tabla_correlaciones_significativas
    from ..visualizacion.graficos import grafico_correlacion
    
    # Crear generador de reporte
    reporte = GeneradorReportePDF(nombre_archivo, "Reporte de Análisis de Correlaciones")
    
    # Portada
    reporte.agregar_portada(
        descripcion="Análisis detallado de correlaciones entre variables numéricas."
    )
    
    try:
        # Análisis de correlaciones
        analisis = analisis_correlacion_completo(df)
        
        # 1. Resumen ejecutivo
        reporte.agregar_seccion("1. Resumen Ejecutivo")
        stats = analisis['estadisticas_generales']
        resumen_texto = f"""
        El análisis identificó {stats['total_pares_variables']} pares de variables, 
        de los cuales {stats['pares_significativos']} muestran correlaciones significativas.
        La correlación promedio entre variables es {stats['correlacion_promedio']:.3f}.
        """
        reporte.agregar_texto(resumen_texto)
        
        # 2. Correlaciones significativas
        reporte.agregar_seccion("2. Correlaciones Significativas")
        tabla_corr = tabla_correlaciones_significativas(df)
        if not tabla_corr.empty:
            reporte.agregar_tabla_dataframe(tabla_corr, "Correlaciones Encontradas")
        else:
            reporte.agregar_texto("No se encontraron correlaciones significativas en el dataset.")
        
        # 3. Matriz de correlación visual
        reporte.agregar_seccion("3. Matriz de Correlación")
        fig_corr = grafico_correlacion(df)
        reporte.agregar_grafico_plotly(fig_corr, "Mapa de Calor de Correlaciones")
        
        # 4. Recomendaciones
        reporte.agregar_seccion("4. Recomendaciones")
        if analisis['recomendaciones']:
            reporte.agregar_lista(analisis['recomendaciones'])
        else:
            reporte.agregar_texto("No hay recomendaciones específicas para este dataset.")
    
    except Exception as e:
        reporte.agregar_texto(f"Error en el análisis de correlaciones: {str(e)}")
    
    # Generar PDF
    reporte.generar_pdf()
    return nombre_archivo


def exportar_datos_con_graficos(df: pd.DataFrame, graficos: Dict[str, go.Figure], 
                               nombre_archivo: str, titulo: str = "Reporte de Datos") -> str:
    """
    Exporta datos y gráficos en un solo reporte PDF.
    
    Args:
        df: DataFrame con los datos
        graficos: Diccionario con gráficos de Plotly
        nombre_archivo: Nombre del archivo PDF
        titulo: Título del reporte
    
    Returns:
        Ruta del archivo generado
    """
    reporte = GeneradorReportePDF(nombre_archivo, titulo)
    
    # Portada
    reporte.agregar_portada()
    
    # Datos
    reporte.agregar_seccion("Datos Analizados")
    reporte.agregar_tabla_dataframe(df, "Dataset Completo", max_filas=50)
    
    # Gráficos
    if graficos:
        reporte.agregar_seccion("Visualizaciones")
        for nombre, fig in graficos.items():
            titulo_grafico = nombre.replace('_', ' ').title()
            reporte.agregar_grafico_plotly(fig, titulo_grafico)
    
    # Generar PDF
    reporte.generar_pdf()
    return nombre_archivo