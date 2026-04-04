import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def cargar_datos():
    """Carga y prepara los datos de planificación y bloques"""
    # Cargar datos
    planificacion = pd.read_csv("Datasource/planificacion.csv")
    bloques_vol = pd.read_csv("Datasource/bloques_volumenes.csv")
    bloques_est = pd.read_csv("Datasource/bloques_estandarizados.csv")
    bloques_mina = pd.read_csv("Datasource/bloques_mina.csv")
    
    # Combinar datos
    bloques = bloques_vol.copy()
    bloques['ley_au'] = bloques_mina['ley_au_estimado']
    bloques['ley_ag'] = bloques_mina['ley_ag_estimado']
    bloques['clasificacion'] = bloques_est['clasificacion']
    
    # Combinar planificación con datos de bloques
    datos = planificacion.merge(bloques, left_on='id_bloque', right_on='id_bloque')
    
    return datos, bloques, bloques_vol, bloques_mina, bloques_est

def calcular_consumo_por_periodo(datos):
    """Calcula el consumo de reservas por periodo y nivel"""
    # Agrupar por periodo y nivel
    consumo = datos.groupby(['periodo', 'nivel']).agg({
        'toneladas_enviadas': 'sum',
        'margen': 'sum',
        'valor_bloque': 'sum',
        'costo_total': 'sum',
        'ley_au': 'mean',
        'ley_ag': 'mean',
        'id_bloque': 'count'  # Cantidad de bloques
    }).reset_index()
    
    consumo.rename(columns={'id_bloque': 'cantidad_bloques'}, inplace=True)
    
    # Calcular acumuladas
    consumo['toneladas_acumuladas'] = consumo.groupby('nivel')['toneladas_enviadas'].cumsum()
    consumo['margen_acumulado'] = consumo.groupby('nivel')['margen'].cumsum()
    
    return consumo

def crear_fecha_periodo(periodo):
    """Convierte número de periodo a fecha (0 = enero 2024, etc.)"""
    inicio = datetime(2024, 1, 1)
    fecha = inicio + timedelta(days=30 * periodo)
    return fecha.strftime('%Y-%m')

def graficar_consumo_acumulado(datos):
    """Gráfico de consumo acumulado por nivel en el tiempo"""
    consumo = calcular_consumo_por_periodo(datos)
    
    # Crear figura con Plotly
    fig = go.Figure()
    
    # Para cada nivel, agregar una línea de consumo acumulado
    niveles = sorted(consumo['nivel'].unique())
    
    for nivel in niveles:
        nivel_data = consumo[consumo['nivel'] == nivel].sort_values('periodo')
        fechas = [crear_fecha_periodo(p) for p in nivel_data['periodo']]
        
        fig.add_trace(go.Scatter(
            x=fechas,
            y=nivel_data['toneladas_acumuladas'],
            mode='lines+markers',
            name=f'Nivel {int(nivel)}',
            line=dict(width=3),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title='Consumo Acumulado de Reservas por Nivel',
        xaxis_title='Periodo (Mes)',
        yaxis_title='Toneladas Acumuladas',
        hovermode='x unified',
        template='plotly_white',
        height=500,
        width=1000
    )
    
    fig.write_html('Datasource/consumo_acumulado.html')
    print("✓ Gráfico de consumo acumulado guardado")
    
    return fig

def graficar_consumo_mensal_apilado(datos):
    """Gráfico de barras apiladas del consumo mensual por nivel"""
    consumo = calcular_consumo_por_periodo(datos)
    
    # Crear pivot table para barras apiladas
    pivot_consumo = consumo.pivot_table(
        values='toneladas_enviadas',
        index='periodo',
        columns='nivel',
        aggfunc='sum',
        fill_value=0
    )
    
    fechas = [crear_fecha_periodo(p) for p in pivot_consumo.index]
    
    fig = go.Figure()
    
    for nivel in sorted(pivot_consumo.columns):
        fig.add_trace(go.Bar(
            x=fechas,
            y=pivot_consumo[nivel],
            name=f'Nivel {int(nivel)}',
            hovertemplate='<b>Nivel %{fullData.name}</b><br>Toneladas: %{y:,.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        barmode='stack',
        title='Toneladas Extraídas por Nivel (Mensual)',
        xaxis_title='Periodo (Mes)',
        yaxis_title='Toneladas Extraídas',
        template='plotly_white',
        height=500,
        width=1000,
        hovermode='x unified'
    )
    
    fig.write_html('Datasource/consumo_mensual_apilado.html')
    print("✓ Gráfico de consumo mensual apilado guardado")
    
    return fig

def graficar_beneficio_economico(datos):
    """Gráfico de beneficio económico acumulado"""
    consumo = calcular_consumo_por_periodo(datos)
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Beneficio Acumulado por Nivel', 'Beneficio Mensual por Nivel')
    )
    
    niveles = sorted(consumo['nivel'].unique())
    
    # Subplot 1: Beneficio acumulado
    for nivel in niveles:
        nivel_data = consumo[consumo['nivel'] == nivel].sort_values('periodo')
        fechas = [crear_fecha_periodo(p) for p in nivel_data['periodo']]
        
        fig.add_trace(go.Scatter(
            x=fechas,
            y=nivel_data['margen_acumulado'],
            mode='lines+markers',
            name=f'Nivel {int(nivel)}',
            line=dict(width=2),
            marker=dict(size=6),
            showlegend=True
        ), row=1, col=1)
    
    # Subplot 2: Beneficio mensual
    pivot_margen = consumo.pivot_table(
        values='margen',
        index='periodo',
        columns='nivel',
        aggfunc='sum',
        fill_value=0
    )
    
    fechas = [crear_fecha_periodo(p) for p in pivot_margen.index]
    
    for nivel in sorted(pivot_margen.columns):
        fig.add_trace(go.Bar(
            x=fechas,
            y=pivot_margen[nivel],
            name=f'Nivel {int(nivel)}',
            showlegend=False
        ), row=1, col=2)
    
    fig.update_xaxes(title_text='Periodo', row=1, col=1)
    fig.update_xaxes(title_text='Periodo', row=1, col=2)
    fig.update_yaxes(title_text='Margen Acumulado ($)', row=1, col=1)
    fig.update_yaxes(title_text='Margen Mensual ($)', row=1, col=2)
    
    fig.update_layout(
        title_text='Beneficio Económico por Nivel',
        height=500,
        width=1400,
        hovermode='x unified',
        template='plotly_white'
    )
    
    fig.write_html('Datasource/beneficio_economico.html')
    print("✓ Gráfico de beneficio económico guardado")
    
    return fig

def crear_tabla_resumen(datos):
    """Crea tabla de resumen por periodo"""
    consumo = calcular_consumo_por_periodo(datos)
    
    # Resumen por periodo (todos los niveles)
    resumen = consumo.groupby('periodo').agg({
        'toneladas_enviadas': 'sum',
        'margen': 'sum',
        'margen_acumulado': 'first',  # No es correcto, recalcular
        'cantidad_bloques': 'sum',
        'ley_au': 'mean',
        'ley_ag': 'mean'
    }).reset_index()
    
    # Calcular margen acumulado total
    resumen['margen_acumulado'] = resumen['margen'].cumsum()
    resumen['toneladas_acumuladas'] = resumen['toneladas_enviadas'].cumsum()
    
    # Formatear fechas
    resumen['Periodo'] = resumen['periodo'].apply(crear_fecha_periodo)
    
    # Seleccionar columnas para mostrar
    resumen_display = resumen[[
        'Periodo',
        'toneladas_enviadas',
        'toneladas_acumuladas',
        'margen',
        'margen_acumulado',
        'cantidad_bloques',
        'ley_au',
        'ley_ag'
    ]].copy()
    
    resumen_display.columns = [
        'Periodo',
        'Ton. Mensuales',
        'Ton. Acumuladas',
        'Margen Mensual ($)',
        'Margen Acumulado ($)',
        'Bloques Extraídos',
        'Ley Au Promedio',
        'Ley Ag Promedio'
    ]
    
    # Formatear números
    for col in ['Ton. Mensuales', 'Ton. Acumuladas', 'Margen Mensual ($)', 'Margen Acumulado ($)']:
        resumen_display[col] = resumen_display[col].apply(lambda x: f'{x:,.0f}')
    
    resumen_display['Bloques Extraídos'] = resumen_display['Bloques Extraídos'].astype(int)
    resumen_display['Ley Au Promedio'] = resumen_display['Ley Au Promedio'].apply(lambda x: f'{x:.3f}')
    resumen_display['Ley Ag Promedio'] = resumen_display['Ley Ag Promedio'].apply(lambda x: f'{x:.2f}')
    
    print("\n" + "="*150)
    print("RESUMEN DE PLAN DE MINADO POR PERÍODO")
    print("="*150)
    print(resumen_display.to_string(index=False))
    print("="*150 + "\n")
    
    # Guardar como CSV
    resumen_display.to_csv('Datasource/resumen_plan_minado.csv', index=False)
    print("✓ Tabla de resumen guardada en: Datasource/resumen_plan_minado.csv\n")
    
    return resumen_display

def graficar_analisis_por_nivel(datos):
    """Análisis detallado por nivel"""
    consumo = calcular_consumo_por_periodo(datos)
    
    # Total por nivel
    total_por_nivel = datos.groupby('nivel').agg({
        'toneladas_enviadas': 'sum',
        'margen': 'sum',
        'ley_au': 'mean',
        'ley_ag': 'mean',
        'id_bloque': 'count'
    }).reset_index()
    
    total_por_nivel.columns = ['nivel', 'toneladas_totales', 'margen_total', 'ley_au_promedio', 'ley_ag_promedio', 'cantidad_bloques']
    total_por_nivel = total_por_nivel.sort_values('nivel')
    
    # Crear subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Toneladas Totales por Nivel',
            'Beneficio Total por Nivel',
            'Ley de Oro Promedio por Nivel',
            'Cantidad de Bloques por Nivel'
        ),
        specs=[
            [{'type': 'bar'}, {'type': 'bar'}],
            [{'type': 'bar'}, {'type': 'bar'}]
        ]
    )
    
    # Plot 1: Toneladas
    fig.add_trace(
        go.Bar(x=total_por_nivel['nivel'], y=total_por_nivel['toneladas_totales'],
               name='Toneladas', marker_color='lightblue', showlegend=False),
        row=1, col=1
    )
    
    # Plot 2: Beneficio
    fig.add_trace(
        go.Bar(x=total_por_nivel['nivel'], y=total_por_nivel['margen_total'],
               name='Margen', marker_color='lightgreen', showlegend=False),
        row=1, col=2
    )
    
    # Plot 3: Ley Au
    fig.add_trace(
        go.Bar(x=total_por_nivel['nivel'], y=total_por_nivel['ley_au_promedio'],
               name='Ley Au', marker_color='gold', showlegend=False),
        row=2, col=1
    )
    
    # Plot 4: Cantidad de bloques
    fig.add_trace(
        go.Bar(x=total_por_nivel['nivel'], y=total_por_nivel['cantidad_bloques'],
               name='Bloques', marker_color='orange', showlegend=False),
        row=2, col=2
    )
    
    fig.update_yaxes(title_text='Toneladas', row=1, col=1)
    fig.update_yaxes(title_text='Margen ($)', row=1, col=2)
    fig.update_yaxes(title_text='Ley Au (g/ton)', row=2, col=1)
    fig.update_yaxes(title_text='Cantidad', row=2, col=2)
    
    fig.update_layout(
        title_text='Análisis de Reservas por Nivel',
        height=800,
        width=1200,
        showlegend=False,
        template='plotly_white'
    )
    
    fig.write_html('Datasource/analisis_por_nivel.html')
    print("✓ Análisis por nivel guardado")
    
    return fig

def crear_dashboard_interactivo(datos):
    """Crea un dashboard completo e interactivo"""
    consumo = calcular_consumo_por_periodo(datos)
    
    # Preparar datos
    resumen_periodo = consumo.groupby('periodo').agg({
        'toneladas_enviadas': 'sum',
        'margen': 'sum',
        'cantidad_bloques': 'sum',
        'ley_au': 'mean'
    }).reset_index()
    
    resumen_periodo['margen_acumulado'] = resumen_periodo['margen'].cumsum()
    resumen_periodo['toneladas_acumuladas'] = resumen_periodo['toneladas_enviadas'].cumsum()
    resumen_periodo['fecha'] = resumen_periodo['periodo'].apply(crear_fecha_periodo)
    
    # Dashboard con subplots
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            'Toneladas Extraídas Mensualmente',
            'Toneladas Acumuladas',
            'Margen Económico Mensual',
            'Margen Económico Acumulado',
            'Ley de Oro Promedio',
            'Bloques Extraídos'
        ),
        specs=[
            [{'type': 'bar'}, {'type': 'scatter'}],
            [{'type': 'bar'}, {'type': 'scatter'}],
            [{'type': 'bar'}, {'type': 'bar'}]
        ]
    )
    
    # Row 1: Toneladas
    fig.add_trace(
        go.Bar(x=resumen_periodo['fecha'], y=resumen_periodo['toneladas_enviadas'],
               name='Toneladas Mensuales', marker_color='steelblue', showlegend=True),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=resumen_periodo['fecha'], y=resumen_periodo['toneladas_acumuladas'],
                   mode='lines+markers', name='Toneladas Acumuladas',
                   line=dict(color='darkblue', width=3), showlegend=True),
        row=1, col=2
    )
    
    # Row 2: Margen
    fig.add_trace(
        go.Bar(x=resumen_periodo['fecha'], y=resumen_periodo['margen'],
               name='Margen Mensual', marker_color='lightgreen', showlegend=False),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=resumen_periodo['fecha'], y=resumen_periodo['margen_acumulado'],
                   mode='lines+markers', name='Margen Acumulado',
                   line=dict(color='darkgreen', width=3), showlegend=False),
        row=2, col=2
    )
    
    # Row 3: Ley y Bloques
    fig.add_trace(
        go.Bar(x=resumen_periodo['fecha'], y=resumen_periodo['ley_au'],
               name='Ley Au Promedio', marker_color='gold', showlegend=False),
        row=3, col=1
    )
    
    fig.add_trace(
        go.Bar(x=resumen_periodo['fecha'], y=resumen_periodo['cantidad_bloques'],
               name='Bloques Extraídos', marker_color='orange', showlegend=False),
        row=3, col=2
    )
    
    # Actualizar ejes
    fig.update_xaxes(title_text='Periodo', row=1, col=1)
    fig.update_xaxes(title_text='Periodo', row=1, col=2)
    fig.update_xaxes(title_text='Periodo', row=2, col=1)
    fig.update_xaxes(title_text='Periodo', row=2, col=2)
    fig.update_xaxes(title_text='Periodo', row=3, col=1)
    fig.update_xaxes(title_text='Periodo', row=3, col=2)
    
    fig.update_yaxes(title_text='Toneladas', row=1, col=1)
    fig.update_yaxes(title_text='Acumuladas', row=1, col=2)
    fig.update_yaxes(title_text='Margen ($)', row=2, col=1)
    fig.update_yaxes(title_text='Acumulado ($)', row=2, col=2)
    fig.update_yaxes(title_text='Ley (g/ton)', row=3, col=1)
    fig.update_yaxes(title_text='Cantidad', row=3, col=2)
    
    fig.update_layout(
        title_text='Dashboard: Plan de Minado y Evolución de Reservas',
        height=1200,
        width=1400,
        showlegend=True,
        hovermode='x unified',
        template='plotly_white'
    )
    
    fig.write_html('Datasource/dashboard_plan_minado.html')
    print("✓ Dashboard interactivo guardado")
    
    return fig

if __name__ == "__main__":
    print("\n" + "="*80)
    print("ANÁLISIS DE PLAN DE MINADO Y CONSUMO DE RESERVAS")
    print("="*80 + "\n")
    
    # Cargar datos
    datos, bloques, bloques_vol, bloques_mina, bloques_est = cargar_datos()
    
    print(f"Total de bloques: {len(bloques)}")
    print(f"Periodos planificados: {datos['periodo'].max() + 1}")
    print(f"Toneladas totales a extraer: {datos['toneladas_enviadas'].sum():,.0f}")
    print(f"Beneficio total esperado: ${datos['margen'].sum():,.0f}")
    print(f"Niveles disponibles: {sorted(datos['nivel'].unique())}\n")
    
    # Generar visualizaciones
    print("Generando visualizaciones...\n")
    
    crear_tabla_resumen(datos)
    graficar_consumo_acumulado(datos)
    graficar_consumo_mensal_apilado(datos)
    graficar_beneficio_economico(datos)
    graficar_analisis_por_nivel(datos)
    crear_dashboard_interactivo(datos)
    
    print("\n" + "="*80)
    print("✓ Análisis completado")
    print("="*80)
    print("\nArchivos generados:")
    print("  • Datasource/resumen_plan_minado.csv - Tabla de resumen")
    print("  • Datasource/consumo_acumulado.html - Consumo acumulado por nivel")
    print("  • Datasource/consumo_mensual_apilado.html - Extracción mensual por nivel")
    print("  • Datasource/beneficio_economico.html - Beneficio económico")
    print("  • Datasource/analisis_por_nivel.html - Análisis detallado por nivel")
    print("  • Datasource/dashboard_plan_minado.html - Dashboard completo ⭐")
    print("="*80 + "\n")
