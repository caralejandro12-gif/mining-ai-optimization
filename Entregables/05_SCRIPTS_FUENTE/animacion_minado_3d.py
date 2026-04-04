import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def cargar_datos():
    """Carga y prepara los datos"""
    planificacion = pd.read_csv("Datasource/planificacion.csv")
    bloques_vol = pd.read_csv("Datasource/bloques_volumenes.csv")
    bloques_mina = pd.read_csv("Datasource/bloques_mina.csv")
    bloques_est = pd.read_csv("Datasource/bloques_estandarizados.csv")
    
    # Combinar datos
    bloques = bloques_vol.copy()
    bloques['ley_au'] = bloques_mina['ley_au_estimado']
    bloques['ley_ag'] = bloques_mina['ley_ag_estimado']
    bloques['clasificacion'] = bloques_est['clasificacion']
    
    # Combinar con planificación
    datos = planificacion.merge(bloques, left_on='id_bloque', right_on='id_bloque')
    
    return datos, bloques

def crear_animacion_3d_minado(datos):
    """Crea animación 3D mostrando cómo se extraen los bloques con el tiempo"""
    
    # Preparar datos por periodo
    periodos_unicos = sorted(datos['periodo'].unique())
    max_periodo = periodos_unicos[-1]
    
    # Crear traces para cada frame (período)
    frames = []
    
    for periodo_actual in periodos_unicos:
        # Bloques que se extraen EXACTAMENTE EN ESTE período
        bloques_este_periodo = datos[datos['periodo'] == periodo_actual].drop_duplicates('id_bloque')
        
        # Bloques que se extraerán EN PERIODOS FUTUROS (no en este ni antes)
        bloques_futuros = datos[datos['periodo'] > periodo_actual].drop_duplicates('id_bloque')
        
        bloques_activos = []
        bloques_futuros_mostrar = []
        
        # Agregar bloques que se extraen AHORA (rojo)
        for idx, row in bloques_este_periodo.iterrows():
            bloques_activos.append(row)
        
        # Agregar bloques que se extraerán después (gris)
        for idx, row in bloques_futuros.iterrows():
            bloques_futuros_mostrar.append(row)
        
        # Crear tres traces separadas para mejor visualización
        traces_periodo = []
        
        # Trace 1: Bloques siendo extraídos (ROJO)
        if bloques_activos:
            datos_activos_df = pd.DataFrame(bloques_activos)
            traces_periodo.append(go.Scatter3d(
                x=datos_activos_df['x'],
                y=datos_activos_df['y'],
                z=datos_activos_df['z'],
                mode='markers',
                marker=dict(
                    size=6,
                    color='red',
                    line=dict(color='darkred', width=2),
                    opacity=1.0,
                    symbol='circle'
                ),
                text=[f"<b>EXTRAYENDO ESTE PERÍODO</b><br>" +
                      f"Bloque: {row['id_bloque']}<br>" +
                      f"Nivel: {row['nivel']}<br>" +
                      f"Toneladas: {row['toneladas']:,.0f}<br>" +
                      f"Ley Au: {row['ley_au']:.3f}"
                      for _, row in datos_activos_df.iterrows()],
                hovertemplate='%{text}<extra></extra>',
                name='Extrayendo Ahora',
                showlegend=True
            ))
        
        # Trace 2: Bloques futuros (GRIS)
        if bloques_futuros_mostrar:
            datos_futuros_df = pd.DataFrame(bloques_futuros_mostrar)
            traces_periodo.append(go.Scatter3d(
                x=datos_futuros_df['x'],
                y=datos_futuros_df['y'],
                z=datos_futuros_df['z'],
                mode='markers',
                marker=dict(
                    size=5,
                    color='lightgray',
                    line=dict(width=0),
                    opacity=0.3
                ),
                text=[f"A extraer en período {int(datos[datos['id_bloque'] == row['id_bloque']]['periodo'].min())}<br>" +
                      f"Bloque: {row['id_bloque']}<br>" +
                      f"Nivel: {row['nivel']}<br>" +
                      f"Toneladas: {row['toneladas']:,.0f}"
                      for _, row in datos_futuros_df.iterrows()],
                hovertemplate='%{text}<extra></extra>',
                name='Por Extraer',
                showlegend=True
            ))
        
        # Calcular estadísticas del período
        toneladas_este_periodo = bloques_este_periodo['toneladas_enviadas'].sum()
        margen_este_periodo = bloques_este_periodo['margen'].sum()
        bloques_count = len(bloques_activos)
        
        frames.append(go.Frame(data=traces_periodo, name=str(periodo_actual),
                              layout=dict(title_text=f'Período {periodo_actual} | Toneladas: {toneladas_este_periodo:,.0f} | Margen: ${margen_este_periodo:,.0f} | Bloques: {bloques_count}')))
    
    # Frame inicial - mostrar el primer período
    datos_inicial_rojo = datos[datos['periodo'] == periodos_unicos[0]].drop_duplicates('id_bloque')
    datos_inicial_gris = datos[datos['periodo'] > periodos_unicos[0]].drop_duplicates('id_bloque')
    
    trace_inicial_activos = go.Scatter3d(
        x=datos_inicial_rojo['x'],
        y=datos_inicial_rojo['y'],
        z=datos_inicial_rojo['z'],
        mode='markers',
        marker=dict(
            size=6,
            color='red',
            line=dict(color='darkred', width=2),
            opacity=1.0
        ),
        text=[f"<b>EXTRAYENDO ESTE PERÍODO</b><br>" +
              f"Bloque: {row['id_bloque']}<br>" +
              f"Nivel: {row['nivel']}<br>" +
              f"Toneladas: {row['toneladas']:,.0f}"
              for _, row in datos_inicial_rojo.iterrows()],
        hovertemplate='%{text}<extra></extra>',
        name='Extrayendo Ahora'
    )
    
    # Bloques futuros en el frame inicial
    trace_inicial_futuros = go.Scatter3d(
        x=datos_inicial_gris['x'],
        y=datos_inicial_gris['y'],
        z=datos_inicial_gris['z'],
        mode='markers',
        marker=dict(
            size=5,
            color='lightgray',
            line=dict(width=0),
            opacity=0.3
        ),
        text=[f"A extraer<br>" +
              f"Bloque: {row['id_bloque']}<br>" +
              f"Nivel: {row['nivel']}"
              for _, row in datos_inicial_gris.iterrows()],
        hovertemplate='%{text}<extra></extra>',
        name='Por Extraer'
    )
    
    toneladas_inicial = datos_inicial_rojo['toneladas_enviadas'].sum()
    margen_inicial = datos_inicial_rojo['margen'].sum()
    
    # Crear figura con animación
    fig = go.Figure(
        data=[trace_inicial_activos, trace_inicial_futuros],
        frames=frames,
        layout=dict(title_text=f'Período 0 | Toneladas: {toneladas_inicial:,.0f} | Margen: ${margen_inicial:,.0f}')
    )
    
    # Configurar layout
    fig.update_layout(
        title='Animación 3D: Consumo de Reservas por Período de Extracción',
        scene=dict(
            xaxis=dict(title='X (m)', gridcolor='lightgray'),
            yaxis=dict(title='Y (m)', gridcolor='lightgray'),
            zaxis=dict(title='Z (m, profundidad)', gridcolor='lightgray'),
            bgcolor='rgba(240,240,240,0.5)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.3)
            )
        ),
        width=1400,
        height=900,
        template='plotly_dark',
        hovermode='closest',
        font=dict(size=12),
        showlegend=True,
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor='white',
            borderwidth=1
        ),
        updatemenus=[
            dict(
                type='buttons',
                showactive=True,
                buttons=[
                    dict(label='▶ REPRODUCIR',
                         method='animate',
                         args=[None, {
                             'frame': {'duration': 1000, 'redraw': True},
                             'fromcurrent': True,
                             'mode': 'immediate',
                             'transition': {'duration': 500, 'easing': 'linear'}
                         }]),
                    dict(label='⏸ PAUSA',
                         method='animate',
                         args=[[None], {
                             'frame': {'duration': 0, 'redraw': False},
                             'mode': 'immediate',
                             'transition': {'duration': 0}
                         }])
                ],
                x=0.05,
                xanchor='left',
                y=1.12,
                yanchor='top'
            )
        ],
        sliders=[{
            'active': 0,
            'steps': [
                {
                    'args': [[f.name], {
                        'frame': {'duration': 500, 'redraw': True},
                        'mode': 'immediate',
                        'transition': {'duration': 300, 'easing': 'quad-in-out'}
                    }],
                    'label': f'Mes {i}',
                    'method': 'animate'
                }
                for i, f in enumerate(frames)
            ],
            'x': 0.05,
            'xanchor': 'left',
            'y': -0.08,
            'yanchor': 'top',
            'len': 0.9,
            'transition': {'duration': 300, 'easing': 'quad-in-out'},
            'currentvalue': {
                'prefix': '<b>PERÍODO: </b>',
                'visible': True,
                'xanchor': 'center',
                'font': {'size': 16, 'color': 'white'}
            },
            'pad': {'t': 80, 'b': 10}
        }]
    )
    
    # Agregar anotación informativa
    fig.add_annotation(
        text="ROJO = Bloques siendo extraídos | GRIS = Bloques futuros",
        xref="paper", yref="paper",
        x=0.5, y=-0.05,
        showarrow=False,
        font=dict(size=12, color='white')
    )
    
    fig.write_html('Datasource/animacion_3d_minado.html')
    print("✓ Animación 3D de minado guardada: Datasource/animacion_3d_minado.html")
    
    return fig

def crear_grafico_consumo_3d_por_periodo(datos):
    """Crea gráfico 3D comparativo del consumo por periodo"""
    
    # Resumen por periodo
    consumo_periodo = datos.groupby('periodo').agg({
        'toneladas_enviadas': 'sum',
        'margen': 'sum',
        'ley_au': 'mean',
        'id_bloque': 'count'
    }).reset_index()
    
    consumo_periodo['toneladas_acumuladas'] = consumo_periodo['toneladas_enviadas'].cumsum()
    consumo_periodo['margen_acumulado'] = consumo_periodo['margen'].cumsum()
    
    # Crear figura 3D con superficie
    fechas = [f'P{int(p)}' for p in consumo_periodo['periodo']]
    
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'bar'}, {'type': 'scatter'}]]
    )
    
    # Barras de consumo
    fig.add_trace(
        go.Bar(
            x=fechas,
            y=consumo_periodo['toneladas_enviadas'],
            name='Toneladas Mensuales',
            marker=dict(color='#1f77b4'),
            hovertemplate='<b>%{x}</b><br>Toneladas: %{y:,.0f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Línea de acumulado
    fig.add_trace(
        go.Scatter(
            x=fechas,
            y=consumo_periodo['toneladas_acumuladas'],
            mode='lines+markers',
            name='Acumulado',
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=8),
            yaxis='y2',
            hovertemplate='<b>%{x}</b><br>Total Acumulado: %{y:,.0f}<extra></extra>'
        ),
        row=1, col=2
    )
    
    fig.update_xaxes(title_text='Periodo', row=1, col=1)
    fig.update_yaxes(title_text='Toneladas/Mes', row=1, col=1)
    fig.update_yaxes(title_text='Toneladas Acumuladas', row=1, col=2)
    
    fig.update_layout(
        title='Consumo Mensual vs Acumulado de Reservas',
        height=500,
        width=1200,
        template='plotly_white',
        hovermode='x unified'
    )
    
    fig.write_html('Datasource/consumo_3d_periodos.html')
    print("✓ Gráfico de consumo por período guardado")
    
    return fig

def crear_mapa_calor_consumo_nivel_periodo(datos):
    """Crea un mapa de calor mostrando consumo por nivel y periodo"""
    
    # Crear matriz
    matriz = datos.pivot_table(
        values='toneladas_enviadas',
        index='nivel',
        columns='periodo',
        aggfunc='sum',
        fill_value=0
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=matriz.values,
        x=[f'P{int(p)}' for p in matriz.columns],
        y=matriz.index,
        colorscale='YlOrRd',
        colorbar=dict(title='Toneladas')
    ))
    
    fig.update_layout(
        title='Mapa de Calor: Toneladas Extraídas por Nivel y Período',
        xaxis_title='Período',
        yaxis_title='Nivel',
        height=500,
        width=1000,
        template='plotly_white'
    )
    
    fig.write_html('Datasource/mapa_calor_consumo.html')
    print("✓ Mapa de calor de consumo guardado")
    
    return fig

def crear_waterfall_beneficio(datos):
    """Crea gráfico Waterfall del beneficio acumulado"""
    
    beneficio_periodo = datos.groupby('periodo').agg({
        'margen': 'sum'
    }).reset_index()
    
    beneficio_periodo['margen_acumulado'] = beneficio_periodo['margen'].cumsum()
    
    # Para Waterfall necesitamos estructurar los datos
    valores = [0] + list(beneficio_periodo['margen'].values)
    periodos = ['Inicio'] + [f'P{int(p)}' for p in beneficio_periodo['periodo']]
    
    fig = go.Figure(go.Waterfall(
        name='Beneficio',
        orientation='v',
        x=periodos,
        textposition='outside',
        y=valores,
        connector={'line': {'color': 'rgba(63, 63, 63, 0.4)'}},
        decreasing={'marker': {'color': '#ef553b'}},
        increasing={'marker': {'color': '#636EFA'}},
        totals={'marker': {'color': '#AB63FA'}}
    ))
    
    fig.update_layout(
        title='Acumulación de Beneficio Económico por Período',
        xaxis_title='Período',
        yaxis_title='Margen ($)',
        height=600,
        width=1200,
        template='plotly_white',
        waterfallgap=0.3
    )
    
    fig.write_html('Datasource/waterfall_beneficio.html')
    print("✓ Gráfico Waterfall de beneficio guardado")
    
    return fig

if __name__ == "__main__":
    print("\n" + "="*80)
    print("VISUALIZACIONES AVANZADAS DEL PLAN DE MINADO")
    print("="*80 + "\n")
    
    # Cargar datos
    datos, bloques = cargar_datos()
    
    print("Generando visualizaciones avanzadas...\n")
    
    crear_animacion_3d_minado(datos)
    crear_grafico_consumo_3d_por_periodo(datos)
    crear_mapa_calor_consumo_nivel_periodo(datos)
    crear_waterfall_beneficio(datos)
    
    print("\n" + "="*80)
    print("✓ Nuevas visualizaciones completadas")
    print("="*80)
    print("\nArchivos generados:")
    print("  • Datasource/animacion_3d_minado.html - Animación 3D interactiva ⭐")
    print("  • Datasource/consumo_3d_periodos.html - Consumo por período")
    print("  • Datasource/mapa_calor_consumo.html - Mapa de calor por nivel y período")
    print("  • Datasource/waterfall_beneficio.html - Evolución del beneficio económico")
    print("="*80 + "\n")
