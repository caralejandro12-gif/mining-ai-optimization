import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import plotly.graph_objects as go

def cargar_datos():
    """Carga los datos de bloques estandarizados y mina"""
    bloques_est = pd.read_csv("Datasource/bloques_estandarizados.csv")
    bloques_mina = pd.read_csv("Datasource/bloques_mina.csv")
    
    # Combinar datos
    bloques = bloques_est.copy()
    bloques['ley_au'] = bloques_mina['ley_au_estimado']
    bloques['ley_ag'] = bloques_mina['ley_ag_estimado']
    
    return bloques

def crear_cubo_vertices(x, y, z, lado_x, lado_y, lado_z):
    """Crea los vértices de un cubo centrado en (x, y, z)"""
    # Desplazamientos desde el centro
    dx, dy, dz = lado_x/2, lado_y/2, lado_z/2
    
    # 8 vértices del cubo
    vertices = np.array([
        [x - dx, y - dy, z - dz],
        [x + dx, y - dy, z - dz],
        [x + dx, y + dy, z - dz],
        [x - dx, y + dy, z - dz],
        [x - dx, y - dy, z + dz],
        [x + dx, y - dy, z + dz],
        [x + dx, y + dy, z + dz],
        [x - dx, y + dy, z + dz],
    ])
    
    # 6 caras del cubo (cada cara es un cuadrilátero)
    caras = [
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # Frente
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # Atrás
        [vertices[0], vertices[3], vertices[7], vertices[4]],  # Izquierda
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # Derecha
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # Abajo
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # Arriba
    ]
    
    return caras

def graficar_3d_matplotlib(bloques, variable='ley_au', muestra=None):
    """Crea visualización 3D con matplotlib"""
    
    if muestra:
        bloques = bloques.head(muestra)
    
    print(f"Graficando {len(bloques)} bloques...")
    
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # Normalizar la variable para los colores
    norm = Normalize(vmin=bloques[variable].min(), vmax=bloques[variable].max())
    cmap = cm.viridis  # Espectro de colores del infrarrojo al ultravioleta
    
    # Dibujar cada bloque
    for idx, row in bloques.iterrows():
        x, y, z = row['x'], row['y'], row['z']
        lado_x, lado_y, lado_z = row['lado_x'], row['lado_y'], row['lado_z']
        
        # Crear caras del cubo
        caras = crear_cubo_vertices(x, y, z, lado_x, lado_y, lado_z)
        
        # Color basado en la ley
        color_valor = norm(row[variable])
        color = cmap(color_valor)
        
        # Agregar el cubo
        poly = Poly3DCollection(caras, alpha=0.7, edgecolor='black', linewidth=0.5)
        poly.set_facecolor(color)
        ax.add_collection3d(poly)
    
    # Configurar etiquetas y límites
    ax.set_xlabel('X (m)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Y (m)', fontsize=12, fontweight='bold')
    ax.set_zlabel('Z (m, profundidad)', fontsize=12, fontweight='bold')
    ax.set_title(f'Modelo 3D de Bloques - Codificados por {variable.replace("_", " ").title()}',
                 fontsize=14, fontweight='bold')
    
    # Establecer límites
    ax.set_xlim(bloques['x'].min() - 50, bloques['x'].max() + 50)
    ax.set_ylim(bloques['y'].min() - 50, bloques['y'].max() + 50)
    ax.set_zlim(bloques['z'].min() - 50, bloques['z'].max() + 50)
    
    # Barra de colores
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, pad=0.1, shrink=0.8)
    cbar.set_label(f'{variable.replace("_", " ").title()} (g/ton)', fontsize=11)
    
    # Ajustar vista
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.savefig('Datasource/modelo_bloques_3d.png', dpi=300, bbox_inches='tight')
    print("Gráfico guardado en: Datasource/modelo_bloques_3d.png")
    plt.show()

def graficar_3d_plotly(bloques, variable='ley_au', muestra=None):
    """Crea visualización 3D interactiva con plotly"""
    
    if muestra:
        bloques = bloques.head(muestra)
    
    print(f"Graficando {len(bloques)} bloques con Plotly...")
    
    # Crear figura
    fig = go.Figure()
    
    # Normalizar la variable para los colores
    ley_min = bloques[variable].min()
    ley_max = bloques[variable].max()
    
    # Agregar cada bloque como un scatter point con información
    fig.add_trace(go.Scatter3d(
        x=bloques['x'],
        y=bloques['y'],
        z=bloques['z'],
        mode='markers',
        marker=dict(
            size=6,
            color=bloques[variable],
            colorscale='Viridis',
            colorbar=dict(
                title=f"{variable.replace('_', ' ').title()}<br>(g/ton)",
                thickness=20,
                len=0.7
            ),
            line=dict(width=0),
            opacity=0.8,
            cmin=ley_min,
            cmax=ley_max
        ),
        text=[f"Bloque: {row['id_bloque']}<br>" +
              f"{variable.replace('_', ' ').title()}: {row[variable]:.3f}<br>" +
              f"X: {row['x']:.2f}<br>" +
              f"Y: {row['y']:.2f}<br>" +
              f"Z: {row['z']:.2f}<br>" +
              f"Volumen: {row['volumen_m3']:.2f} m³"
              for _, row in bloques.iterrows()],
        hovertemplate='%{text}<extra></extra>',
        name='Bloques'
    ))
    
    # Configurar layout
    fig.update_layout(
        title=f'Modelo 3D Interactivo de Bloques - Codificados por {variable.replace("_", " ").title()}',
        scene=dict(
            xaxis=dict(title='X (m)', gridwidth=2),
            yaxis=dict(title='Y (m)', gridwidth=2),
            zaxis=dict(title='Z (m, profundidad)', gridwidth=2),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.3)
            )
        ),
        width=1200,
        height=800,
        font=dict(size=12),
        showlegend=False,
        hovermode='closest'
    )
    
    # Guardar como HTML interactivo
    fig.write_html('Datasource/modelo_bloques_3d_interactivo.html')
    print("Gráfico interactivo guardado en: Datasource/modelo_bloques_3d_interactivo.html")
    fig.show()

def graficar_comparativo(bloques):
    """Crea gráficos comparativos de las leyes"""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Distribución de ley de oro
    axes[0, 0].hist(bloques['ley_au'], bins=30, color='gold', edgecolor='black', alpha=0.7)
    axes[0, 0].set_title('Distribución de Ley de Oro', fontweight='bold')
    axes[0, 0].set_xlabel('Ley Au (g/ton)')
    axes[0, 0].set_ylabel('Cantidad de Bloques')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Distribución de ley de plata
    axes[0, 1].hist(bloques['ley_ag'], bins=30, color='silver', edgecolor='black', alpha=0.7)
    axes[0, 1].set_title('Distribución de Ley de Plata', fontweight='bold')
    axes[0, 1].set_xlabel('Ley Ag (g/ton)')
    axes[0, 1].set_ylabel('Cantidad de Bloques')
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Scatter Au vs Ag
    scatter = axes[1, 0].scatter(bloques['ley_au'], bloques['ley_ag'], 
                                  c=bloques['ley_au'], cmap='viridis', 
                                  s=50, alpha=0.6, edgecolor='black', linewidth=0.5)
    axes[1, 0].set_title('Correlación: Ley de Oro vs Plata', fontweight='bold')
    axes[1, 0].set_xlabel('Ley Au (g/ton)')
    axes[1, 0].set_ylabel('Ley Ag (g/ton)')
    axes[1, 0].grid(True, alpha=0.3)
    plt.colorbar(scatter, ax=axes[1, 0], label='Ley Au')
    
    # 4. Estadísticas por nivel
    stats_por_nivel = bloques.groupby('nivel').agg({
        'ley_au': ['mean', 'min', 'max'],
        'ley_ag': 'mean'
    }).round(3)
    
    axes[1, 1].axis('off')
    tabla_text = stats_por_nivel.to_string()
    axes[1, 1].text(0.1, 0.5, tabla_text, fontfamily='monospace', fontsize=9)
    axes[1, 1].set_title('Estadísticas por Nivel', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('Datasource/comparativo_leyes.png', dpi=300, bbox_inches='tight')
    print("Gráfico comparativo guardado en: Datasource/comparativo_leyes.png")
    plt.show()

if __name__ == "__main__":
    # Cargar datos
    bloques = cargar_datos()
    
    print(f"Total de bloques cargados: {len(bloques)}")
    print(f"Rango de ley Au: {bloques['ley_au'].min():.3f} - {bloques['ley_au'].max():.3f} g/ton")
    print(f"Rango de ley Ag: {bloques['ley_ag'].min():.3f} - {bloques['ley_ag'].max():.3f} g/ton")
    print()
    
    # Opciones de visualización
    print("=== OPCIONES DE VISUALIZACIÓN ===")
    print("1. Gráfico 3D completo (matplotlib) - Ley de Oro")
    print("2. Gráfico 3D interactivo (Plotly) - Ley de Oro")
    print("3. Gráfico 3D interactivo (Plotly) - Ley de Plata")
    print("4. Gráfico 3D muestra (100 bloques)")
    print("5. Gráficos comparativos de leyes")
    print("6. Todos los gráficos")
    print()
    
    opcion = input("Selecciona una opción (1-6): ").strip()
    
    if opcion == '1':
        graficar_3d_matplotlib(bloques, variable='ley_au')
    elif opcion == '2':
        graficar_3d_plotly(bloques, variable='ley_au')
    elif opcion == '3':
        graficar_3d_plotly(bloques, variable='ley_ag')
    elif opcion == '4':
        graficar_3d_matplotlib(bloques, variable='ley_au', muestra=100)
    elif opcion == '5':
        graficar_comparativo(bloques)
    elif opcion == '6':
        graficar_3d_matplotlib(bloques, variable='ley_au', muestra=500)
        graficar_3d_plotly(bloques, variable='ley_au')
        graficar_comparativo(bloques)
    else:
        print("Opción no válida")
        # Por defecto, ejecutar la visualización interactiva
        graficar_3d_plotly(bloques, variable='ley_au')
