import pandas as pd
import numpy as np

np.random.seed(42)

n = 200

bloques = pd.DataFrame({
    "id_bloque": range(n),
    "nivel": np.random.randint(1, 10, n),
    "x": np.random.uniform(0, 1000, n),
    "y": np.random.uniform(0, 1000, n),
    "z": np.random.uniform(-500, 0, n),
    "toneladas": np.random.uniform(500, 5000, n),
    "ley_au_estimado": np.random.uniform(1, 5, n),
    "ley_ag_estimado": np.random.uniform(10, 100, n),
    "dureza": np.random.uniform(1, 10, n),
    "recuperacion_esperada": np.random.uniform(0.6, 0.9, n),
    "costo_extraccion": np.random.uniform(20, 80, n),
    "distancia_planta": np.random.uniform(100, 1000, n),
    "distancia_stock": np.random.uniform(50, 500, n),
    "penalidad_impurezas": np.random.uniform(0.8, 1.2, n),
    "estado": ["no_extraido"] * n
})

bloques.to_csv("bloques_mina.csv", index=False)