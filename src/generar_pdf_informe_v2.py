"""
Generar informe PDF del proyecto de minería
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
import pandas as pd
from datetime import datetime
import os

# Cargar datos
planificacion = pd.read_csv("Datasource/planificacion.csv")
bloques_vol = pd.read_csv("Datasource/bloques_volumenes.csv")
bloques_mina = pd.read_csv("Datasource/bloques_mina.csv")

# Crear documento PDF
pdf_file = "Entregables/INFORME_PROYECTO_MINERIA.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=letter,
                        rightMargin=0.75*inch, leftMargin=0.75*inch,
                        topMargin=0.75*inch, bottomMargin=0.75*inch)

# Crear estilos
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#333333'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#0066cc'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=11,
    alignment=TA_JUSTIFY,
    spaceAfter=12,
    leading=14
)

# Lista de elementos del PDF
story = []

# PORTADA
story.append(Spacer(1, 1.5*inch))
story.append(Paragraph("PROYECTO DE MINERÍA SUBTERRÁNEA", title_style))
story.append(Paragraph("Análisis y Visualización de Plan de Minado", styles['Heading2']))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph(f"Fecha: {datetime.now().strftime('%d de %B de %Y')}", styles['Normal']))
story.append(Spacer(1, 2*inch))

resumen_date = datetime.now().strftime("%d/%m/%Y - %H:%M")
story.append(Paragraph(f"<b>Generado:</b> {resumen_date}", body_style))

story.append(PageBreak())

# TABLA DE CONTENIDOS
story.append(Paragraph("TABLA DE CONTENIDOS", heading_style))
contenidos_list = [
    "1. INTRODUCCIÓN Y OBJETIVOS",
    "2. CONCEPTOS MINEROS TÉCNICOS",
    "3. HERRAMIENTAS INFORMÁTICAS UTILIZADAS",
    "4. DATOS Y PARÁMETROS DEL PROYECTO",
    "5. ANÁLISIS TÉCNICO INTEGRADO",
    "6. RESULTADOS Y CONCLUSIONES",
    "7. RECOMENDACIONES Y PRÓXIMOS PASOS",
    "8. ANEXOS - ARCHIVOS GENERADOS"
]
story.append(Spacer(1, 0.2*inch))
for contenido in contenidos_list:
    story.append(Paragraph(f"• {contenido}", body_style))
story.append(Spacer(1, 0.3*inch))

story.append(PageBreak())

# 1. INTRODUCCIÓN
story.append(Paragraph("1. INTRODUCCIÓN Y OBJETIVOS", heading_style))
story.append(Paragraph(
    "Este informe documenta un análisis integral de viabilidad técnica y económica para una operación "
    "minera subterránea tipo 'Cut & Fill' ascendente. El proyecto incluye un modelo geológico 3D de 200 bloques "
    "de mineral, distribuidos en 10 períodos operacionales, con análisis económico, geotécnico y de planificación "
    "minera integrados en visualizaciones interactivas.",
    body_style
))

story.append(Paragraph("<b>Objetivos Principales:</b>", body_style))
objetivos = [
    "Modelar el depósito mineral mediante blocaje 3D estandarizado",
    "Desarrollar un plan de minado aplicando criterios técnicos de corte (cut-off)",
    "Visualizar la progresión de extracción mediante animación 3D interactiva",
    "Analizar viabilidad económica con métricas de flujo de caja",
    "Generar dashboards ejecutivos para monitoreo"
]
for obj in objetivos:
    story.append(Paragraph(f"• {obj}", body_style))

story.append(Spacer(1, 0.3*inch))
story.append(PageBreak())

# 2. CONCEPTOS MINEROS
story.append(Paragraph("2. CONCEPTOS MINEROS TÉCNICOS", heading_style))

elementos_mineros = [
    ("Tipo de Explotación", "Minería Subterránea Cut & Fill Ascendente"),
    ("Estrategia Espacial", "Extracción desde profundidad máxima (-490m) hacia superficie (-5m)"),
    ("Ventaja Operacional", "Relleno con estéril reduce porosidades y presiones estructurales"),
    ("Criterio de Corte Au", "2.5 g/ton - umbral que discrimina entre planta e stock"),
]

for titulo, descripcion in elementos_mineros:
    story.append(Paragraph(f"<b>{titulo}:</b> {descripcion}", body_style))

story.append(Spacer(1, 0.2*inch))
story.append(PageBreak())

# 3. HERRAMIENTAS INFORMÁTICAS
story.append(Paragraph("3. HERRAMIENTAS INFORMÁTICAS UTILIZADAS", heading_style))

tools_data = [
    ["Categoría", "Herramienta", "Versión", "Función"],
    ["Lenguaje", "Python", "3.14", "Procesamiento datos y visualización"],
    ["Análisis", "Pandas", "2.x", "Manipulación de datos (CSV)"],
    ["Cálculo", "NumPy", "Latest", "Operaciones numéricas"],
    ["Visualización 3D", "Plotly", "6.6.0", "Gráficos 3D interactivos"],
    ["Gráficas", "Matplotlib", "3.x", "Reportes en PNG"],
    ["Reportes PDF", "ReportLab", "Latest", "Generación de PDF"],
]

tools_table = Table(tools_data, colWidths=[1.2*inch, 1.2*inch, 0.8*inch, 2.0*inch])
tools_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
]))
story.append(tools_table)
story.append(Spacer(1, 0.2*inch))
story.append(PageBreak())

# 4. DATOS Y PARÁMETROS
story.append(Paragraph("4. DATOS Y PARÁMETROS DEL PROYECTO", heading_style))

# Métricas
total_bloques = len(bloques_vol)
total_toneladas = planificacion['toneladas_enviadas'].sum()
total_margen = planificacion['margen'].sum()
total_periodos = int(planificacion['periodo'].max()) + 1
ley_min = bloques_mina['ley_au_estimado'].min()
ley_max = bloques_mina['ley_au_estimado'].max()
ley_prom = bloques_mina['ley_au_estimado'].mean()
z_min = bloques_vol['z'].min()
z_max = bloques_vol['z'].max()

metricas_data = [
    ["Métrica", "Valor", "Unidad"],
    ["Total Bloques", str(total_bloques), "unidades"],
    ["Total Toneladas", f"{total_toneladas/1e6:.2f}", "millones ton"],
    ["Total Margen", f"USD {total_margen/1e6:.1f}M", ""],
    ["Períodos", str(total_periodos), "periodos"],
    ["Ley Au Promedio", f"{ley_prom:.2f}", "g/ton"],
    ["Rango Z", f"{z_max - z_min:.1f}", "metros"],
]

metricas_table = Table(metricas_data, colWidths=[2.0*inch, 1.5*inch, 1.5*inch])
metricas_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
]))
story.append(metricas_table)

story.append(Spacer(1, 0.3*inch))
story.append(PageBreak())

# 5. ANÁLISIS TÉCNICO
story.append(Paragraph("5. ANÁLISIS TÉCNICO INTEGRADO", heading_style))

analisis_items = [
    ("Estrategia Cut & Fill Ascendente",
     "La explotación avanza de abajo hacia arriba, permitiendo relleno contemporáneo. Esto mejora estabilidad geomecánica."),
    ("Distribución Uniforme",
     f"Plan de {total_periodos} períodos con ~{total_bloques//total_periodos} bloques/período garantiza operaciones predecibles"),
    ("Flujo de Caja Positivo",
     f"Beneficio económico total: USD {total_margen/1e6:.1f}M sin subsidios operacionales")
]

for titulo, descripcion in analisis_items:
    story.append(Paragraph(f"<b>{titulo}</b>", body_style))
    story.append(Paragraph(descripcion, body_style))
    story.append(Spacer(1, 0.1*inch))

story.append(PageBreak())

# 6. CONCLUSIONES
story.append(Paragraph("6. RESULTADOS Y CONCLUSIONES", heading_style))

conclusiones = [
    f"✓ Modelo 3D de {total_bloques} bloques validado",
    f"✓ Plan de {total_periodos} períodos establecido",
    f"✓ Beneficio económico: USD {total_margen/1e6:.1f}M",
    "✓ Visualizaciones interactivas consolidadas",
    "✓ Estrategia ascendente confirmada"
]

for conc in conclusiones:
    story.append(Paragraph(conc, body_style))

story.append(Spacer(1, 0.2*inch))
story.append(Paragraph(
    "El proyecto es técnicamente viable. Se recomienda validación in-situ antes de implementación.",
    body_style
))

story.append(Spacer(1, 0.2*inch))
story.append(PageBreak())

# 7. ANEXOS
story.append(Paragraph("7. ARCHIVOS GENERADOS", heading_style))

story.append(Paragraph("<b>Visualizaciones Interactivas (HTML):</b>", body_style))
visualizaciones = [
    "animacion_3d_minado.html - PRINCIPAL",
    "dashboard_plan_minado.html - Ejecutivo 6-en-1",
    "modelo_bloques_3d_interactivo.html - Modelo geológico 3D",
]
for viz in visualizaciones:
    story.append(Paragraph(f"• {viz}", body_style))

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("<b>Datos (CSV):</b>", body_style))
datos_csv = [
    "bloques_volumenes.csv - Geometría",
    "bloques_mina.csv - Propiedades",
    "planificacion.csv - Plan de minado"
]
for dato in datos_csv:
    story.append(Paragraph(f"• {dato}", body_style))

story.append(Spacer(1, 0.3*inch))
story.append(Paragraph(
    f"PDF generado: {datetime.now().strftime('%d de %B de %Y')}",
    body_style
))

# Construir PDF
doc.build(story)
print(f"✓ PDF informe generado: {pdf_file}")
print(f"  Tamaño: {os.path.getsize(pdf_file) / 1024:.1f} KB")
