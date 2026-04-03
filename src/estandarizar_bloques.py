import pandas as pd
import numpy as np

# Cargar datos
bloques = pd.read_csv("Datasource/bloques_volumenes.csv")

# Parámetros de estandarización
LADO_MINERIA = 10  # metros
VOLUMEN_ESTANDAR = LADO_MINERIA ** 3  # 1,000 m³
DENSIDAD_MINERAL = 2.7  # ton/m³
DENSIDAD_ESTERIL = 2.5  # ton/m³ (ligeramente menor que mineral)

# Crear dataframe con medidas estandarizadas
bloques_estandar = bloques.copy()

# Nuevas columnas de medidas
bloques_estandar['lado_x'] = LADO_MINERIA
bloques_estandar['lado_y'] = LADO_MINERIA
bloques_estandar['lado_z'] = LADO_MINERIA
bloques_estandar['volumen_estandar_m3'] = VOLUMEN_ESTANDAR

# Calcular dilución planificada
# Dilución = (Volumen Estéril / Volumen Total) * 100
# O: Factor de dilución = Volumen Original / Volumen Estandar

bloques_estandar['factor_dilucion'] = bloques_estandar['volumen_m3'] / VOLUMEN_ESTANDAR

# Volumen de estéril agregado (si es positivo) o mineral perdido (si es negativo)
bloques_estandar['volumen_esteril_agregado'] = VOLUMEN_ESTANDAR - bloques_estandar['volumen_m3']

# Porcentaje de dilución planificada
bloques_estandar['dilucion_planificada_%'] = np.where(
    bloques_estandar['volumen_m3'] < VOLUMEN_ESTANDAR,
    ((VOLUMEN_ESTANDAR - bloques_estandar['volumen_m3']) / VOLUMEN_ESTANDAR) * 100,  # Dilución
    -((bloques_estandar['volumen_m3'] - VOLUMEN_ESTANDAR) / bloques_estandar['volumen_m3']) * 100  # Pérdida (negativa)
)

# Clasificación
bloques_estandar['clasificacion'] = np.where(
    bloques_estandar['volumen_m3'] == VOLUMEN_ESTANDAR,
    'Conforme',
    np.where(
        bloques_estandar['volumen_m3'] < VOLUMEN_ESTANDAR,
        'Requiere Dilución',
        'Requiere Selectividad'
    )
)

# Toneladas en el bloque estandarizado
# Las toneladas originales se mantienen, son las toneladas de mineral que están en el volumen original
# No necesitamos recalcular

# Redondear
columnas_redondear = ['volumen_m3', 'lado_bloque_m', 'volumen_estandar_m3', 'volumen_esteril_agregado', 'factor_dilucion', 'dilucion_planificada_%']
for col in columnas_redondear:
    if col in bloques_estandar.columns:
        bloques_estandar[col] = bloques_estandar[col].round(2)

# Seleccionar columnas para el reporte
reporte_final = bloques_estandar[[
    'id_bloque', 'nivel', 'x', 'y', 'z',
    'toneladas',  # Original
    'volumen_m3',  # Volumen original
    'lado_bloque_m',  # Lado original (cúbico)
    'lado_x', 'lado_y', 'lado_z',  # Medidas estandarizadas
    'volumen_estandar_m3',  # Volumen estandarizado
    'volumen_esteril_agregado',  # Volumen de estéril a agregar
    'factor_dilucion',  # Factor de dilución
    'dilucion_planificada_%',  # Porcentaje de dilución/pérdida
    'clasificacion'  # Tipo de acción requerida
]]

# Guardar reporte
reporte_final.to_csv("Datasource/bloques_estandarizados.csv", index=False)
print("✓ Archivo de bloques estandarizados guardado: Datasource/bloques_estandarizados.csv\n")

# Mostrar estadísticas
print("="*100)
print("ESTANDARIZACIÓN DE BLOQUES A 10x10x10 METROS")
print("="*100)
print(f"\nVolumen Estandarizado: {VOLUMEN_ESTANDAR} m³ ({LADO_MINERIA}m × {LADO_MINERIA}m × {LADO_MINERIA}m)\n")

print("Resumen de Clasificación:")
print("-" * 100)
for clasificacion in ['Conforme', 'Requiere Dilución', 'Requiere Selectividad']:
    count = len(reporte_final[reporte_final['clasificacion'] == clasificacion])
    porcentaje = (count / len(reporte_final)) * 100
    print(f"  {clasificacion:.<35} {count:>3} bloques ({porcentaje:>5.1f}%)")

print("\n" + "="*100)
print("Estadísticas de Dilución Planificada")
print("="*100)

dilucion_positiva = reporte_final[reporte_final['volumen_m3'] < VOLUMEN_ESTANDAR]
dilucion_negativa = reporte_final[reporte_final['volumen_m3'] > VOLUMEN_ESTANDAR]
conforme = reporte_final[reporte_final['volumen_m3'] == VOLUMEN_ESTANDAR]

print(f"\nBloques que Requieren Dilución (volumen < {VOLUMEN_ESTANDAR} m³):")
print(f"  • Cantidad: {len(dilucion_positiva)} bloques")
if len(dilucion_positiva) > 0:
    print(f"  • Dilución Promedio: {dilucion_positiva['dilucion_planificada_%'].mean():.2f}%")
    print(f"  • Rango Dilución: {dilucion_positiva['dilucion_planificada_%'].min():.2f}% a {dilucion_positiva['dilucion_planificada_%'].max():.2f}%")
    print(f"  • Volumen Estéril Total a Agregar: {dilucion_positiva['volumen_esteril_agregado'].sum():,.2f} m³")

print(f"\nBloques que Requieren Selectividad (volumen > {VOLUMEN_ESTANDAR} m³):")
print(f"  • Cantidad: {len(dilucion_negativa)} bloques")
if len(dilucion_negativa) > 0:
    print(f"  • Pérdida Promedio: {dilucion_negativa['dilucion_planificada_%'].mean():.2f}%")
    print(f"  • Rango Pérdida: {dilucion_negativa['dilucion_planificada_%'].min():.2f}% a {dilucion_negativa['dilucion_planificada_%'].max():.2f}%")
    print(f"  • Mineral a Dejar en Piso: {abs(dilucion_negativa['volumen_esteril_agregado'].sum()):,.2f} m³")

print(f"\nBloques Conformes (volumen = {VOLUMEN_ESTANDAR} m³):")
print(f"  • Cantidad: {len(conforme)} bloques ({(len(conforme)/len(reporte_final))*100:.1f}%)")

print("\n" + "="*100)
print("Primeros 10 bloques con mayor dilución requerida:")
print("="*100)
top_dilucion = reporte_final.nlargest(10, 'dilucion_planificada_%')[
    ['id_bloque', 'volumen_m3', 'dilucion_planificada_%', 'volumen_esteril_agregado', 'clasificacion']
]
print(top_dilucion.to_string(index=False))

print("\n" + "="*100)
print("Últimos 10 bloques (mayor pérdida de mineral):")
print("="*100)
top_perdida = reporte_final.nsmallest(10, 'dilucion_planificada_%')[
    ['id_bloque', 'volumen_m3', 'dilucion_planificada_%', 'volumen_esteril_agregado', 'clasificacion']
]
print(top_perdida.to_string(index=False))

print("\n" + "="*100)
print("RESUMEN VOLUMÉTRICO TOTAL")
print("="*100)
print(f"\nVolumen Original Total:               {reporte_final['volumen_m3'].sum():>15,.2f} m³")
print(f"Volumen Estandarizado Total:          {reporte_final['volumen_estandar_m3'].sum():>15,.2f} m³")
print(f"Diferencia (Estéril - Mineral):       {reporte_final['volumen_esteril_agregado'].sum():>15,.2f} m³")
print(f"\nDilución Promedio Ponderada:          {(reporte_final['volumen_esteril_agregado'].sum() / reporte_final['volumen_estandar_m3'].sum()) * 100:>14,.2f}%")
