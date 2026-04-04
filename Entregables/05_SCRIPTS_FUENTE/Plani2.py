from Bloque1 import * 
import numpy as np

periodos = 10

# Ordenar bloques por Z ascendente (más profundo primero = Z menor)
# Y distribuir en períodos para una extracción ascendente tipo cut & fill
bloques_ordenados = bloques.sort_values('z').reset_index(drop=True)

# Distribuir los bloques en períodos de forma ascendente
bloques_por_periodo = len(bloques_ordenados) // periodos  # 200 / 10 = 20 bloques por periodo

planificacion = []

for i, (idx, row) in enumerate(bloques_ordenados.iterrows()):
    # Cada bloque se asigna a un período basado en su posición en el orden Z
    periodo_asignado = i // bloques_por_periodo
    if periodo_asignado >= periodos:
        periodo_asignado = periodos - 1
    
    ley = row["ley_au_estimado"]
    ton = row["toneladas"]
    rec = row["recuperacion_esperada"]
    costo = row["costo_extraccion"]
    original_id = row["id_bloque"]
    z_coord = row["z"]
    
    # regla simple tipo cut-off
    destino = "planta" if ley > 2.5 else "stock"
    
    precio_oro = 60  # USD/g (simplificado)
    
    valor = ton * ley * rec * precio_oro
    costo_total = ton * costo
    margen = valor - costo_total
    
    planificacion.append([
        original_id, periodo_asignado, destino, ton, valor, costo_total, margen
    ])

planificacion = pd.DataFrame(planificacion, columns=[
    "id_bloque", "periodo", "destino",
    "toneladas_enviadas", "valor_bloque",
    "costo_total", "margen"
])

# Ordenar por periodo y luego por id_bloque
planificacion = planificacion.sort_values(["periodo", "id_bloque"]).reset_index(drop=True)

planificacion.to_csv("Datasource/planificacion.csv", index=False)
print("Planificación generada por PROFUNDIDAD (ascendente cut & fill)\n")
print(f"Distribución por período (de más profundo a menos profundo):")
print(planificacion.groupby('periodo').agg({
    'id_bloque': 'count',
    'toneladas_enviadas': 'sum',
    'margen': 'sum'
}).rename(columns={'id_bloque': 'bloques', 'toneladas_enviadas': 'toneladas', 'margen': 'margen_total'}))
