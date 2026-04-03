import pandas as pd
import numpy as np

# Cargar datos de bloques
bloques = pd.read_csv("Datasource/bloques_mina.csv")

# Densidad estándar para minerales de oro/plata (ton/m³)
# Oro: 19.3 ton/m³, Plata: 10.5 ton/m³, Roca mineralizada: 2.6-2.8 ton/m³
# Usamos 2.7 ton/m³ como promedio de la roca mineralizada
DENSIDAD_MINERAL = 2.7  # ton/m³

# Calcular volumen de cada bloque
bloques['volumen_m3'] = bloques['toneladas'] / DENSIDAD_MINERAL

# Asumir bloques cúbicos (lado = raíz cúbica del volumen)
bloques['lado_bloque_m'] = np.cbrt(bloques['volumen_m3'])

# Crear un reporte con medidas geométricas
reporte = bloques[['id_bloque', 'nivel', 'x', 'y', 'z', 'toneladas', 
                    'volumen_m3', 'lado_bloque_m']].copy()

# Redondear a 2 decimales
reporte['volumen_m3'] = reporte['volumen_m3'].round(2)
reporte['lado_bloque_m'] = reporte['lado_bloque_m'].round(2)

# Mostrar resumen estadístico
print("="*80)
print("RESUMEN DE VOLÚMENES Y MEDIDAS GEOMÉTRICAS DE BLOQUES")
print("="*80)
print(f"\nDensidad del mineral utilizada: {DENSIDAD_MINERAL} ton/m³\n")

print("Estadísticas generales:")
print(f"  Total de bloques: {len(reporte)}")
print(f"  Volumen total: {reporte['volumen_m3'].sum():.2f} m³")
print(f"  Volumen promedio: {reporte['volumen_m3'].mean():.2f} m³")
print(f"  Volumen mínimo: {reporte['volumen_m3'].min():.2f} m³")
print(f"  Volumen máximo: {reporte['volumen_m3'].max():.2f} m³")

print(f"\n  Lado de bloque promedio: {reporte['lado_bloque_m'].mean():.2f} m")
print(f"  Lado de bloque mínimo: {reporte['lado_bloque_m'].min():.2f} m")
print(f"  Lado de bloque máximo: {reporte['lado_bloque_m'].max():.2f} m")

print("\n" + "="*80)
print("DETALLE POR BLOQUE")
print("="*80)
print(reporte.to_string(index=False))

# Guardar reporte en CSV y en Excel
reporte.to_csv("Datasource/bloques_volumenes.csv", index=False)
print("\n\n✓ Reporte guardado en: Datasource/bloques_volumenes.csv")

# Estadísticas por nivel
print("\n" + "="*80)
print("ESTADÍSTICAS POR NIVEL")
print("="*80 + "\n")

estadisticas_nivel = reporte.groupby('nivel').agg({
    'volumen_m3': ['count', 'sum', 'mean'],
    'lado_bloque_m': ['mean', 'min', 'max'],
    'toneladas': ['sum', 'mean']
}).round(2)

print(estadisticas_nivel)

# Guardar estadísticas por nivel
estadisticas_nivel.to_csv("Datasource/estadisticas_por_nivel.csv")
print("\n✓ Estadísticas por nivel guardadas en: Datasource/estadisticas_por_nivel.csv")
