from Bloque1 import * 

periodos = 10

planificacion = []

for i in range(len(bloques)):
    for p in range(periodos):
        
        ley = bloques.loc[i, "ley_au_estimado"]
        ton = bloques.loc[i, "toneladas"]
        rec = bloques.loc[i, "recuperacion_esperada"]
        costo = bloques.loc[i, "costo_extraccion"]
        
        # regla simple tipo cut-off
        destino = "planta" if ley > 2.5 else "stock"
        
        precio_oro = 60  # USD/g (simplificado)
        
        valor = ton * ley * rec * precio_oro
        costo_total = ton * costo
        margen = valor - costo_total
        
        planificacion.append([
            i, p, destino, ton, valor, costo_total, margen
        ])

planificacion = pd.DataFrame(planificacion, columns=[
    "id_bloque", "periodo", "destino",
    "toneladas_enviadas", "valor_bloque",
    "costo_total", "margen"
])


planificacion.to_csv("planificacion.csv", index=False)
