import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar datos
bloques = pd.read_csv("Datasource/bloques_estandarizados.csv")

# Configurar estilo
plt.style.use('seaborn-v0_8-whitegrid')
fig = plt.figure(figsize=(18, 12))

# 1. Comparación de volúmenes
ax1 = plt.subplot(2, 3, 1)
x_pos = np.arange(len(bloques.head(20)))
width = 0.35
ax1.bar(x_pos - width/2, bloques['volumen_m3'].head(20), width, label='Volumen Original', color='steelblue', alpha=0.8)
ax1.bar(x_pos + width/2, bloques['volumen_estandar_m3'].head(20), width, label='Volumen Estandarizado', color='orange', alpha=0.8)
ax1.axhline(y=1000, color='red', linestyle='--', linewidth=2, alpha=0.5)
ax1.set_xlabel('ID Bloque', fontsize=10)
ax1.set_ylabel('Volumen (m³)', fontsize=10)
ax1.set_title('Comparación: Primeros 20 Bloques', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. Distribución de dilución planificada
ax2 = plt.subplot(2, 3, 2)
bins = np.linspace(bloques['dilucion_planificada_%'].min(), bloques['dilucion_planificada_%'].max(), 30)
colors = ['red' if x < 0 else 'green' for x in bloques['dilucion_planificada_%']]
ax2.hist(bloques['dilucion_planificada_%'], bins=bins, color='steelblue', edgecolor='black', alpha=0.7)
ax2.axvline(0, color='black', linestyle='-', linewidth=2, label='Sin cambio')
ax2.axvline(bloques['dilucion_planificada_%'].mean(), color='red', linestyle='--', linewidth=2, label=f'Media: {bloques["dilucion_planificada_%"].mean():.2f}%')
ax2.set_xlabel('Dilución Planificada (%)', fontsize=10)
ax2.set_ylabel('Cantidad de Bloques', fontsize=10)
ax2.set_title('Distribución de Dilución Planificada', fontsize=12, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 3. Volumen de estéril agregado vs mineral perdido
ax3 = plt.subplot(2, 3, 3)
dilucion = bloques[bloques['volumen_m3'] < 1000]
selectividad = bloques[bloques['volumen_m3'] > 1000]

categorias = ['Estéril a Agregar', 'Mineral a Dejar']
valores = [dilucion['volumen_esteril_agregado'].sum(), abs(selectividad['volumen_esteril_agregado'].sum())]
colores = ['#ff9999', '#66b3ff']
explode = (0.05, 0.05)

ax3.pie(valores, labels=categorias, autopct='%1.1f%%', colors=colores, explode=explode, startangle=90)
ax3.set_title('Distribución: Estéril vs Mineral', fontsize=12, fontweight='bold')

# 4. Clasificación de bloques
ax4 = plt.subplot(2, 3, 4)
clasificaciones = bloques['clasificacion'].value_counts()
colores_clasi = ['#ff6b6b', '#4ecdc4']
bars = ax4.bar(clasificaciones.index, clasificaciones.values, color=colores_clasi, edgecolor='black', linewidth=1.5)
ax4.set_ylabel('Cantidad de Bloques', fontsize=10)
ax4.set_title('Clasificación de Bloques', fontsize=12, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')

# Agregar valores en las barras
for bar in bars:
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}\n({height/len(bloques)*100:.1f}%)',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# 5. Dilución vs Nivel minero
ax5 = plt.subplot(2, 3, 5)
nivel_dilucion = bloques.groupby('nivel')['dilucion_planificada_%'].mean().sort_index()
colores_nivel = ['red' if x < 0 else 'green' for x in nivel_dilucion]
ax5.bar(nivel_dilucion.index, nivel_dilucion.values, color=colores_nivel, edgecolor='black', alpha=0.7)
ax5.axhline(0, color='black', linestyle='-', linewidth=1)
ax5.set_xlabel('Nivel Minero', fontsize=10)
ax5.set_ylabel('Dilución Promedio (%)', fontsize=10)
ax5.set_title('Dilución Planificada por Nivel', fontsize=12, fontweight='bold')
ax5.grid(True, alpha=0.3, axis='y')

# 6. Resumen estadístico
ax6 = plt.subplot(2, 3, 6)
ax6.axis('off')

stats_text = f"""
ESTANDARIZACIÓN A BLOQUES 10×10×10 m

Volumen por Bloque: 1,000 m³

CLASIFICACIÓN:
  • Requiere Dilución: {len(bloques[bloques['volumen_m3'] < 1000])} bloques ({len(bloques[bloques['volumen_m3'] < 1000])/len(bloques)*100:.1f}%)
  • Requiere Selectividad: {len(bloques[bloques['volumen_m3'] > 1000])} bloques ({len(bloques[bloques['volumen_m3'] > 1000])/len(bloques)*100:.1f}%)

VOLÚMENES:
  • Original Total: {bloques['volumen_m3'].sum():,.0f} m³
  • Estandarizado: {bloques['volumen_estandar_m3'].sum():,.0f} m³
  • Diferencia: {(bloques['volumen_estandar_m3'].sum() - bloques['volumen_m3'].sum()):+,.0f} m³

DILUCIÓN PLANIFICADA:
  • Estéril a Agregar: {bloques[bloques['volumen_m3'] < 1000]['volumen_esteril_agregado'].sum():,.0f} m³
  • Mineral a Dejar: {abs(bloques[bloques['volumen_m3'] > 1000]['volumen_esteril_agregado'].sum()):,.0f} m³
  • Dilución Neta: {bloques['dilucion_planificada_%'].mean():.2f}% (promedio)

RANGO DE DILUCIÓN:
  • Mínima: {bloques[bloques['volumen_m3'] < 1000]['dilucion_planificada_%'].min():.2f}%
  • Máxima: {bloques[bloques['volumen_m3'] < 1000]['dilucion_planificada_%'].max():.2f}%

RANGO DE SELECTIVIDAD:
  • Mínima: {bloques[bloques['volumen_m3'] > 1000]['dilucion_planificada_%'].min():.2f}%
  • Máxima: {bloques[bloques['volumen_m3'] > 1000]['dilucion_planificada_%'].max():.2f}%
"""

ax6.text(0.05, 0.95, stats_text, transform=ax6.transAxes, fontsize=9,
        verticalalignment='top', fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.suptitle('ANÁLISIS DE ESTANDARIZACIÓN DE BLOQUES A 10×10×10 METROS', 
             fontsize=14, fontweight='bold', y=0.995)
plt.tight_layout(rect=[0, 0.03, 1, 0.99])
plt.savefig('Datasource/analisis_estandarizacion.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico de estandarización guardado: Datasource/analisis_estandarizacion.png")
plt.show()

print("\n" + "="*100)
print("GENERACIÓN DE GRÁFICOS COMPLETADA")
print("="*100)
