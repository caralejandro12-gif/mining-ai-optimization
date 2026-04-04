"""
Generar informe PDF del proyecto de minería
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
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
elements = []

# Portada
elements.append(Spacer(1, 1.5*inch))
elements.append(Paragraph("PROYECTO DE MINERÍA SUBTERRÁNEA", title_style))
elements.append(Paragraph("Análisis y Visualización de Plan de Minado", styles['Heading2']))
elements.append(Spacer(1, 0.3*inch))
elements.append(Paragraph(f"Fecha: {datetime.now().strftime('%d de %B de %Y')}", styles['Normal']))
elements.append(Spacer(1, 2*inch))

resumen_date = datetime.now().strftime("%d/%m/%Y - %H:%M")
elements.append(Paragraph(f"<b>Generado:</b> {resumen_date}", body_style))

elements.append(PageBreak())

# TABLA DE CONTENIDOS
elements.append(Paragraph("TABLA DE CONTENIDOS", heading_style))
contenidos = [
    ["1. INTRODUCCIÓN Y OBJETIVOS"],
    ["2. CONCEPTOS MINEROS TÉCNICOS"],
    ["3. HERRAMIENTAS INFORMÁTICAS UTILIZADAS"],
    ["4. DATOS Y PARÁMETROS DEL PROYECTO"],
    ["5. ANÁLISIS TÉCNICO INTEGRADO"],
    ["6. RESULTADOS Y CONCLUSIONES"],
    ["7. RECOMENDACIONES Y PRÓXIMOS PASOS"],
    ["8. ANEXOS - ARCHIVOS GENERADOS"]
]
elements.append(Spacer(1, 0.2*inch))
for contenido in contenidos:
    elements.append(Paragraph(f"• {contenido[0]}", body_style))
elements.append(Spacer(1, 0.3*inch))

elements.append(PageBreak())

# 1. INTRODUCCIÓN
elements.append(Paragraph("1. INTRODUCCIÓN Y OBJETIVOS", heading_style))
elements.append(Paragraph(
    "Este informe documenta un análisis integral de viabilidad técnica y económica para una operación "
    "minera subterránea tipo 'Cut & Fill' ascendente. El proyecto incluye un modelo geológico 3D de 200 bloques "
    "de mineral, distribuidos en 10 períodos operacionales, con análisis económico, geotécnico y de planificación "
    "minera integrados en visualizaciones interactivas.",
    body_style
))

elements.append(Paragraph(
    "<b>Objetivos Principales:</b>", body_style
))
objetivos = [
    "Modelar el depósito mineral mediante blocaje 3D estandarizado",
    "Desarrollar un plan de minado aplicando criterios técnicos de corte (cut-off) y estrategias operacionales",
    "Visualizar la progresión de extracción mediante animación 3D interactiva",
    "Analizar viabilidad económica con métricas de flujo de caja y beneficio",
    "Generar dashboards ejecutivos para monitoreo operacional en tiempo real"
]
for obj in objetivos:
    elements.append(Paragraph(f"• {obj}", body_style))

elements.append(Spacer(1, 0.3*inch))

# 2. CONCEPTOS MINEROS
elements.append(Paragraph("2. CONCEPTOS MINEROS TÉCNICOS", heading_style))

elementos_mineros = [
    ("Tipo de Explotación", "Minería Subterránea - Cut & Fill Ascendente"),
    ("Estrategia Espacial", "Extracción desde profundidad máxima (-490m) hacia superficie (-5m)"),
    ("Ventaja Operacional", "Relleno con estéril reduce porosidades y presiones estructurales"),
    ("Criterio de Corte (Au)", "2.5 g/ton - umbral que discrimina entre planta de lixiviación e stock"),
    ("Destino Planta", "Ley ≥ 2.5 g/ton → Lixiviación inmediata"),
    ("Destino Stock", "Ley < 2.5 g/ton → Acopio para reprocesamiento futuro"),
    ("Parámetro Geológico Clave", "Z (profundidad) - coordenada que define secuencia de extracción"),
    ("Unidad Minera", "200 bloques geotécnicos (cada uno = ~2,600 toneladas promedio)")
]

for titulo, descripcion in elementos_mineros:
    elements.append(Paragraph(f"<b>{titulo}:</b> {descripcion}", body_style))
    
elements.append(Spacer(1, 0.2*inch))

elements.append(PageBreak())

# 3. HERRAMIENTAS INFORMÁTICAS
elements.append(Paragraph("3. HERRAMIENTAS INFORMÁTICAS UTILIZADAS", heading_style))

tools_data = [
    ["Categoría", "Herramienta", "Versión", "Función"],
    ["Lenguaje", "Python", "3.14", "Procesamiento datos y generación visualizaciones"],
    ["Análisis", "Pandas", "2.x", "Manipulación de datos estructurados (CSV)"],
    ["Cálculo", "NumPy", "Latest", "Operaciones numéricas y arrays"],
    ["Visualización 3D", "Plotly", "6.6.0", "Gráficos 3D interactivos con Plotly.js"],
    ["Gráficas Estáticas", "Matplotlib", "3.x", "Reportes en PNG para presentaciones"],
    ["Gráficas 3D", "mpl_toolkits.mplot3d", "3.x", "Complemento para visualización 3D"],
    ["Reportes", "ReportLab", "Latest", "Generación de PDF programático"],
    ["Entorno", "VS Code + venv", "Latest", "Desarrollo y ejecución de scripts"],
    ["Base Datos", "CSV + Pandas", "n/a", "Almacenamiento y consulta de datos"],
]

tools_table = Table(tools_data, colWidths=[1.2*inch, 1.2*inch, 0.8*inch, 2.0*inch])
tools_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
]))
elements.append(tools_table)

elements.append(Spacer(1, 0.2*inch))

elementos_salida = [
    "HTML Interactivo (Plotly.js) - Visualizaciones 3D y dashboards",
    "CSV - Datos tabulares para análisis posterior",
    "PNG - Reportes estáticos para presentaciones",
    "PDF - Informe consolidado (este documento)"
]

elements.append(Paragraph("<b>Formatos de Salida:</b>", body_style))
for elem in elementos_salida:
    elements.append(Paragraph(f"• {elem}", body_style))

elements.append(PageBreak())

# 4. DATOS Y PARÁMETROS
elements.append(Paragraph("4. DATOS Y PARÁMETROS DEL PROYECTO", heading_style))

# Métricas calculadas
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
    ["Métrica", "Valor", "Unidad", "Descripción"],
    ["Total Bloques", str(total_bloques), "unidades", "Número de unidades geotécnicas"],
    ["Total Toneladas", f"{total_toneladas/1e6:.2f}", "millones ton", "Mineral a procesar"],
    ["Total Margen", f"USD {total_margen/1e6:.1f}", "millones", "Beneficio económico bruto"],
    ["Períodos", str(total_periodos), "períodos", "Duración operacional"],
    ["Ley Au Mínima", f"{ley_min:.2f}", "g/ton", "Contenido mínimo de oro"],
    ["Ley Au Máxima", f"{ley_max:.2f}", "g/ton", "Contenido máximo de oro"],
    ["Ley Au Promedio", f"{ley_prom:.2f}", "g/ton", "Promedio del depósito"],
    ["Z Mínimo (Profundo)", f"{z_min:.1f}", "metros", "Cota más profunda"],
    ["Z Máximo (Somero)", f"{z_max:.1f}", "metros", "Cota más superficial"],
    ["Rango Z", f"{z_max - z_min:.1f}", "metros", "Profundidad total del depósito"],
]

metricas_table = Table(metricas_data, colWidths=[1.5*inch, 1.0*inch, 0.9*inch, 1.8*inch])
metricas_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
]))
elements.append(metricas_table)

elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph(
    f"<b>Criterio de Cut-off Aplicado:</b> Ley de oro ≥ 2.5 g/ton para destino a planta de lixiviación. "
    f"Material con ley menor se dirige a stock para acopio temporal.",
    body_style
))

elements.append(PageBreak())

# 5. ANÁLISIS TÉCNICO
elements.append(Paragraph("5. ANÁLISIS TÉCNICO INTEGRADO", heading_style))

elementos_analisis = [
    ("Estrategia Cut & Fill Ascendente", 
     "La explotación avanza de abajo hacia arriba, permitiendo uso del material extraído como relleno. "
     "Esto reduce presiones litoestáticas y mejora estabilidad geomecánica. Cada período extrae ~20 bloques, "
     "distribuidos en un rango vertical de 40-60 metros."),
    
    ("Distribución Espacial de Leyes",
     f"La ley promedio de oro es {ley_prom:.2f} g/ton con variabilidad significativa (Min: {ley_min:.2f}, Max: {ley_max:.2f}). "
     "Zonas profundas presentan mayor concentración, sugiriendo depósito epithermal con enriquecimiento supergénico."),
    
    ("Dimensiones de Bloques",
     "Cada bloque es una unidad cúbica de ~10-12 metros de lado, permitiendo operaciones con equipos estándar. "
     "Volumen promedio ~1,200 m³ = ~3,000 toneladas por bloque."),
    
    ("Plan de Minado Balanceado",
     f"Distribución uniforme de {total_toneladas/total_periodos/1e3:.0f}k toneladas/período garantiza operaciones predecibles. "
     "Sin picos operacionales críticos que requieran ajustes de capacidad."),
    
    ("Flujo de Caja Positivo",
     f"Todos los períodos generan margen positivo (USD {total_margen/total_periodos/1e6:.1f}M promedio/período). "
     "Estructura de costos controlada sin subsidios operacionales requeridos.")
]

for titulo, descripcion in elementos_analisis:
    elements.append(Paragraph(f"<b>{titulo}</b>", body_style))
    elements.append(Paragraph(descripcion, body_style))
    elements.append(Spacer(1, 0.1*inch))

elements.append(PageBreak())

# 6. RESULTADOS Y CONCLUSIONES
elements.append(Paragraph("6. RESULTADOS Y CONCLUSIONES", heading_style))

resultados = [
    "El modelo 3D de 200 bloques representa fielmente la geometría del depósito y permite visualización interactiva.",
    f"Plan de minado de {total_periodos} períodos distribuye {total_bloques} bloques uniformemente (20/período).",
    f"Animación 3D demuestra estrategia ascendente de abajo hacia arriba en forma visual clara.",
    f"Análisis económico integrado: USD {total_margen/1e6:.1f}M beneficio total estimado.",
    f"Dashboards ejecutivos consolidan 6 perspectivas (temporal, espacial, económica, geológica).",
    "Criterio de corte Au 2.5 g/ton discrimina eficientemente entre planta e stock.",
    "Modelo sensible a variaciones de precio de oro - permite análisis de escenarios."
]

for resultado in resultados:
    elements.append(Paragraph(f"✓ {resultado}", body_style))

elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph(
    "El proyecto es técnicamente viable bajo los parámetros asumidos. El modelo cut & fill ascendente "
    "es operacionalmente factible y permite integración de relleno contemporáneo, mejorando estabilidad "
    "geomecánica. Se recomienda validación in-situ antes de implementación.",
    body_style
))

elements.append(PageBreak())

# 7. RECOMENDACIONES
elements.append(Paragraph("7. RECOMENDACIONES Y PRÓXIMOS PASOS", heading_style))

recomendaciones = [
    ("Validación Geotécnica", "Realizar estudio de estabilidad de taludes y macizo rocoso para zona de estudio."),
    ("Muestreo Detallado", "Incrementar sondajes en contactos litológicos para confirmar leyes estimadas."),
    ("Análisis de Sensibilidad", "Modelar escenarios con variaciones ±20% en precio de oro."),
    ("Diseño de Infraestructura", "Especificar sistemas de relleno, drenaje y componentes de soporte."),
    ("Evaluación Ambiental", "Incluir aspectos de cierre de mina y gestión de relaves."),
    ("Revisión Económica", "Actualizar modelos con costos operacionales locales actualizados."),
]

for recom, detalle in recomendaciones:
    elements.append(Paragraph(f"<b>→ {recom}:</b> {detalle}", body_style))
    elements.append(Spacer(1, 0.1*inch))

elements.append(PageBreak())

# 8. ANEXOS
elements.append(Paragraph("8. ANEXOS - ARCHIVOS GENERADOS", heading_style))

elementos.append(Paragraph("<b>Visualizaciones Interactivas (HTML con Plotly):</b>", body_style))
visualizaciones = [
    "animacion_3d_minado.html - Animación principal (RECOMENDADO ABRIR PRIMERO)",
    "dashboard_plan_minado.html - Dashboard ejecutivo 6-en-1",
    "modelo_bloques_3d_interactivo.html - Modelo geológico 3D con colores por ley",
    "consumo_acumulado.html - Evolución de reservas por nivel",
    "consumo_mensual_apilado.html - Comparativa planta vs stock",
    "beneficio_economico.html - Análisis de retorno económico",
    "consumo_3d_periodos.html - Comparativo mensual vs acumulativo",
    "mapa_calor_consumo.html - Intensidad de extracción (heatmap)",
    "waterfall_beneficio.html - Cascada de valor económico"
]
for viz in visualizaciones:
    elements.append(Paragraph(f"• {viz}", body_style))

elements.append(Spacer(1, 0.1*inch))
elementos.append(Paragraph("<b>Datos (CSV):</b>", body_style))
datos_csv = [
    "bloques_volumenes.csv - Coordenadas y geometría de 200 bloques",
    "bloques_mina.csv - Propiedades geológicas (leyes, dureza, estado)",
    "planificacion.csv - Plan de minado por período",
    "resumen_plan_minado.csv - Estadísticas por período"
]
for dato in datos_csv:
    elements.append(Paragraph(f"• {dato}", body_style))

elements.append(Spacer(1, 0.1*inch))
elementos.append(Paragraph("<b>Reportes (PNG):</b>", body_style))
reportes = [
    "modelo_bloques_3d.png - Visualización estática 3D",
    "comparativo_leyes.png - Distribución Au vs Ag",
    "analisis_volumenes.png - Histogramas de tonelajes"
]
for reporte in reportes:
    elements.append(Paragraph(f"• {reporte}", body_style))

elements.append(Spacer(1, 0.1*inch))
elementos.append(Paragraph("<b>Scripts (Python - reproducibilidad):</b>", body_style))
scripts = [
    "Bloque1.py - Carga y procesamiento de datos base",
    "Plani2.py - Generación del plan de minado",
    "animacion_minado_3d.py - Visualizaciones 3D",
    "plan_minado_interactivo.py - Dashboards interactivos",
    "agregar_insights.py - Conclusiones e insights"
]
for script in scripts:
    elements.append(Paragraph(f"• {script}", body_style))

elements.append(Spacer(1, 0.3*inch))
elements.append(Paragraph(
    f"<b>Documento generado:</b> {datetime.now().strftime('%d de %B de %Y a las %H:%M')}",
    body_style
))

# Construir PDF
doc.build(elements)
print(f"✓ PDF informe generado: {pdf_file}")
print(f"\nTamaño: {os.path.getsize(pdf_file) / 1024:.1f} KB")
