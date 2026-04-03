import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar datos
bloques = pd.read_csv("Datasource/bloques_volumenes.csv")

# Configurar estilo
plt.style.use('seaborn-v0_8-darkgrid')
fig = plt.figure(figsize=(16, 12))

# 1. Distribución de volúmenes
ax1 = plt.subplot(2, 3, 1)
bins = np.linspace(bloques['volumen_m3'].min(), bloques['volumen_m3'].max(), 30)
ax1.hist(bloques['volumen_m3'], bins=bins, color='steelblue', edgecolor='black', alpha=0.7)
ax1.axvline(bloques['volumen_m3'].mean(), color='red', linestyle='--', linewidth=2, label=f'Media: {bloques["volumen_m3"].mean():.2f} m³')
ax1.set_xlabel('Volumen (m³)', fontsize=10)
ax1.set_ylabel('Frecuencia', fontsize=10)
ax1.set_title('Distribución de Volúmenes de Bloques', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. Volumen vs Toneladas
ax2 = plt.subplot(2, 3, 2)
scatter = ax2.scatter(bloques['toneladas'], bloques['volumen_m3'], c=bloques['nivel'], 
                     cmap='viridis', s=50, alpha=0.6, edgecolors='black', linewidth=0.5)
ax2.set_xlabel('Toneladas', fontsize=10)
ax2.set_ylabel('Volumen (m³)', fontsize=10)
ax2.set_title('Relación: Toneladas vs Volumen', fontsize=12, fontweight='bold')
cbar = plt.colorbar(scatter, ax=ax2)
cbar.set_label('Nivel', fontsize=9)
ax2.grid(True, alpha=0.3)

# 3. Volumen por Nivel - Box Plot
ax3 = plt.subplot(2, 3, 3)
bloques.boxplot(column='volumen_m3', by='nivel', ax=ax3)
ax3.set_xlabel('Nivel Minero', fontsize=10)
ax3.set_ylabel('Volumen (m³)', fontsize=10)
ax3.set_title('Distribución de Volúmenes por Nivel', fontsize=12, fontweight='bold')
plt.sca(ax3)
plt.xticks(rotation=0)

# 4. Lado de bloque vs Nivel
ax4 = plt.subplot(2, 3, 4)
volumen_por_nivel = bloques.groupby('nivel')['volumen_m3'].mean()
lado_por_nivel = bloques.groupby('nivel')['lado_bloque_m'].mean()
x = np.arange(len(volumen_por_nivel))
width = 0.35
bars1 = ax4.bar(x - width/2, volumen_por_nivel, width, label='Volumen promedio (m³)', color='skyblue', edgecolor='black')
ax4_2 = ax4.twinx()
bars2 = ax4_2.bar(x + width/2, lado_por_nivel, width, label='Lado promedio (m)', color='orange', edgecolor='black')
ax4.set_xlabel('Nivel Minero', fontsize=10)
ax4.set_ylabel('Volumen Promedio (m³)', color='skyblue', fontsize=10)
ax4_2.set_ylabel('Lado Promedio (m)', color='orange', fontsize=10)
ax4.set_title('Volumen y Lado Promedio por Nivel', fontsize=12, fontweight='bold')
ax4.set_xticks(x)
ax4.set_xticklabels(volumen_por_nivel.index)
ax4.tick_params(axis='y', labelcolor='skyblue')
ax4_2.tick_params(axis='y', labelcolor='orange')
ax4.grid(True, alpha=0.3, axis='y')

# 5. Distribución del lado del bloque
ax5 = plt.subplot(2, 3, 5)
bins_lado = np.linspace(bloques['lado_bloque_m'].min(), bloques['lado_bloque_m'].max(), 25)
ax5.hist(bloques['lado_bloque_m'], bins=bins_lado, color='lightgreen', edgecolor='darkgreen', alpha=0.7)
ax5.axvline(bloques['lado_bloque_m'].mean(), color='red', linestyle='--', linewidth=2, label=f'Media: {bloques["lado_bloque_m"].mean():.2f} m')
ax5.set_xlabel('Lado del Bloque (m)', fontsize=10)
ax5.set_ylabel('Frecuencia', fontsize=10)
ax5.set_title('Distribución de Lado de Bloque (Cúbico)', fontsize=12, fontweight='bold')
ax5.legend()
ax5.grid(True, alpha=0.3)

# 6. Estadísticas resumidas
ax6 = plt.subplot(2, 3, 6)
ax6.axis('off')

stats_text = f"""
RESUMEN ESTADÍSTICO - VOLÚMENES Y MEDIDAS GEOMÉTRICAS

Densidad del Mineral: 2.7 ton/m³

VOLUMEN (m³):
  • Total:       {bloques['volumen_m3'].sum():>12,.2f} m³
  • Promedio:    {bloques['volumen_m3'].mean():>12,.2f} m³
  • Mín:         {bloques['volumen_m3'].min():>12,.2f} m³
  • Máx:         {bloques['volumen_m3'].max():>12,.2f} m³
  • Desv. Est.:  {bloques['volumen_m3'].std():>12,.2f} m³

LADO DEL BLOQUE (m) - Asumiendo Cubos:
  • Promedio:    {bloques['lado_bloque_m'].mean():>12,.2f} m
  • Mín:         {bloques['lado_bloque_m'].min():>12,.2f} m
  • Máx:         {bloques['lado_bloque_m'].max():>12,.2f} m
  • Desv. Est.:  {bloques['lado_bloque_m'].std():>12,.2f} m

TONELADAS:
  • Total:       {bloques['toneladas'].sum():>12,.2f} ton
  • Promedio:    {bloques['toneladas'].mean():>12,.2f} ton
  • Mín:         {bloques['toneladas'].min():>12,.2f} ton
  • Máx:         {bloques['toneladas'].max():>12,.2f} ton

BLOQUES: {len(bloques)} unidades distribuidas en 9 niveles
"""

ax6.text(0.05, 0.95, stats_text, transform=ax6.transAxes, fontsize=9,
        verticalalignment='top', fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.suptitle('ANÁLISIS GEOMÉTRICO Y VOLUMÉTRICO - BLOQUES DE MINA', 
             fontsize=14, fontweight='bold', y=0.995)
plt.tight_layout(rect=[0, 0.03, 1, 0.99])
plt.savefig('Datasource/analisis_volumenes.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico guardado en: Datasource/analisis_volumenes.png")
plt.show()

print("\n" + "="*80)
print("GENERACIÓN DE GRÁFICOS COMPLETADA")
print("="*80)
