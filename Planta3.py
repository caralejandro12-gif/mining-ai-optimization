from Plani2 import *

planta = []

for p in range(periodos):
    
    bloques_periodo = planificacion[
        (planificacion["periodo"] == p) &
        (planificacion["destino"] == "planta")
    ]
    
    if len(bloques_periodo) == 0:
        continue
    
    ids = bloques_periodo["id_bloque"]
    subset = bloques.loc[ids]
    
    ton_total = subset["toneladas"].sum()
    
    # ley real con ruido (diferencia vs estimado)
    ley_real = np.average(
        subset["ley_au_estimado"] * np.random.uniform(0.9, 1.1, len(subset)),
        weights=subset["toneladas"]
    )
    
    recuperacion_real = np.mean(subset["recuperacion_esperada"]) * np.random.uniform(0.95, 1.05)
    
    oro_recuperado = ton_total * ley_real * recuperacion_real
    
    planta.append([
        p, ton_total, ley_real, recuperacion_real, oro_recuperado
    ])

planta = pd.DataFrame(planta, columns=[
    "periodo", "toneladas_procesadas",
    "ley_cabeza_au", "recuperacion_real",
    "oro_recuperado"
])

planta.to_csv("planta_lixiviacion.csv", index=False)