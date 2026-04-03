import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Datos de análisis
tamaños = [8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0]
mineral_perdido = [98489, 83394, 68096, 52353, 37695, 24157, 13775, 5835, 526]
esteril_agregado = [7255, 12584, 20261, 30193, 44061, 62048, 86340, 116376, 152491]
eficiencia = [52.88, 63.43, 75.30, 88.56, 103.29, 119.57, 137.48, 157.09, 178.48]

# Crear figura
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Mineral perdido vs Tamaño
ax1 = axes[0, 0]
ax1.plot(tamaños, mineral_perdido, 'o-', color='#d62728', linewidth=2.5, markersize=8, label='Mineral Perdido')
ax1.axvline(x=9.5, color='green', linestyle='--', linewidth=2, alpha=0.7, label='Óptimo (9.5m)')
ax1.axvline(x=10.0, color='blue', linestyle='--', linewidth=2, alpha=0.7, label='Actual (10m)')
ax1.fill_between(tamaños, mineral_perdido, alpha=0.3, color='#d62728')
ax1.set_xlabel('Tamaño de Bloque (lado en m)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Mineral Perdido (m³)', fontsize=11, fontweight='bold')
ax1.set_title('Mineral Dejado en Piso vs Tamaño de Bloque', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10)
ax1.set_xticks(tamaños)

# 2. Estéril agregado vs Tamaño
ax2 = axes[0, 1]
ax2.plot(tamaños, esteril_agregado, 's-', color='#1f77b4', linewidth=2.5, markersize=8, label='Estéril Agregado')
ax2.axvline(x=9.5, color='green', linestyle='--', linewidth=2, alpha=0.7, label='Óptimo (9.5m)')
ax2.axvline(x=10.0, color='blue', linestyle='--', linewidth=2, alpha=0.7, label='Actual (10m)')
ax2.fill_between(tamaños, esteril_agregado, alpha=0.3, color='#1f77b4')
ax2.set_xlabel('Tamaño de Bloque (lado en m)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Estéril a Agregar (m³)', fontsize=11, fontweight='bold')
ax2.set_title('Estéril Requerido vs Tamaño de Bloque', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=10)
ax2.set_xticks(tamaños)

# 3. Eficiencia
ax3 = axes[1, 0]
colors = ['red' if x < 100 else 'green' for x in eficiencia]
bars = ax3.bar(tamaños, eficiencia, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5, width=0.3)
ax3.axhline(y=100, color='black', linestyle='-', linewidth=1, alpha=0.5)
ax3.axvline(x=9.5, color='darkgreen', linestyle='--', linewidth=2.5, alpha=0.8, label='Óptimo')
ax3.axvline(x=10.0, color='darkblue', linestyle='--', linewidth=2.5, alpha=0.8, label='Actual')
ax3.set_xlabel('Tamaño de Bloque (lado en m)', fontsize=11, fontweight='bold')
ax3.set_ylabel('Eficiencia de Extracción (%)', fontsize=11, fontweight='bold')
ax3.set_title('Eficiencia de Extracción vs Tamaño', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')
ax3.set_xticks(tamaños)
ax3.legend(fontsize=10)

# Agregar valores en las barras
for i, (t, e) in enumerate(zip(tamaños, eficiencia)):
    ax3.text(t, e + 3, f'{e:.1f}%', ha='center', fontsize=9, fontweight='bold')

# 4. Comparativa Mineral Perdido vs Estéril
ax4 = axes[1, 1]
x = np.arange(len(tamaños))
width = 0.35

bars1 = ax4.bar(x - width/2, mineral_perdido, width, label='Mineral Perdido', color='#d62728', alpha=0.8)
bars2 = ax4.bar(x + width/2, np.array(esteril_agregado)/10, width, label='Estéril Agreg. (÷10)', color='#1f77b4', alpha=0.8)

ax4.axvline(x=np.where(np.array(tamaños) == 9.5)[0][0] - 0.2, color='darkgreen', linestyle='--', linewidth=2.5, alpha=0.8)
ax4.axvline(x=np.where(np.array(tamaños) == 10.0)[0][0], color='darkblue', linestyle='--', linewidth=2.5, alpha=0.8)

ax4.set_xlabel('Tamaño de Bloque (lado en m)', fontsize=11, fontweight='bold')
ax4.set_ylabel('Volumen (m³)', fontsize=11, fontweight='bold')
ax4.set_title('Balance: Mineral Perdido vs Estéril Agregado', fontsize=12, fontweight='bold')
ax4.set_xticks(x)
ax4.set_xticklabels([f'{t:.1f}m' for t in tamaños])
ax4.legend(fontsize=10)
ax4.grid(True, alpha=0.3, axis='y')

plt.suptitle('ANÁLISIS COMPARATIVO: MEDIDAS ÓPTIMAS PARA MAXIMIZAR EXTRACCIÓN', 
             fontsize=14, fontweight='bold', y=0.995)
plt.tight_layout(rect=[0, 0.03, 1, 0.99])
plt.savefig('Datasource/analisis_medidas_optimas.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico de análisis de medidas óptimas guardado: Datasource/analisis_medidas_optimas.png")
plt.show()

print("\n" + "="*100)
print("GENERACIÓN DE GRÁFICOS COMPLETADA")
print("="*100)
