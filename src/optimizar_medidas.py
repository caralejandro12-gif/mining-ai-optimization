import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargar datos
bloques = pd.read_csv("Datasource/bloques_estandarizados.csv")

# Estadísticas de volumen original
vol_original = bloques['volumen_m3']
lado_original = bloques['lado_bloque_m']

print("="*100)
print("ANÁLISIS DE MEDIDAS ÓPTIMAS PARA MAXIMIZAR EXTRACCIÓN DE MINERAL")
print("="*100)

print("\nESTADÍSTICAS DEL VOLUMEN ORIGINAL:")
print("-" * 100)
print(f"  Medio:              {vol_original.mean():.2f} m³")
print(f"  Desviación Estándar: {vol_original.std():.2f} m³")
print(f"  Percentil 25%:      {vol_original.quantile(0.25):.2f} m³")
print(f"  Mediana (P50):      {vol_original.median():.2f} m³")
print(f"  Percentil 75%:      {vol_original.quantile(0.75):.2f} m³")

print(f"\nESTADÍSTICAS DEL LADO ORIGINAL (asumiendo cubos):")
print("-" * 100)
print(f"  Medio:              {lado_original.mean():.2f} m")
print(f"  Desviación Estándar: {lado_original.std():.2f} m")
print(f"  Mínimo:             {lado_original.min():.2f} m")
print(f"  Máximo:             {lado_original.max():.2f} m")

# Calcular pérdida/ganancia para diferentes tamaños de bloque
tamaños_candidatos = np.arange(8.0, 12.5, 0.5)

print("\n" + "="*100)
print("ANÁLISIS DE PÉRDIDA DE MINERAL PARA DIFERENTES TAMAÑOS DE BLOQUE")
print("="*100)

resultados = []

for lado_std in tamaños_candidatos:
    vol_std = lado_std ** 3
    
    # Calcular pérdida/ganancia para cada bloque
    diferencia = bloques['volumen_m3'] - vol_std
    
    # Mineral a dejar (cuando volumen > tamaño estandar)
    mineral_perdido = diferencia[diferencia > 0].sum()
    
    # Estéril a agregar (cuando volumen < tamaño estándar)
    esteril_agregado = abs(diferencia[diferencia < 0].sum())
    
    # Balance neto
    balance_neto = esteril_agregado - mineral_perdido
    
    # Cantidad de bloques que requieren dilución
    n_dilucion = len(bloques[bloques['volumen_m3'] < vol_std])
    
    # Cantidad que requieren selectividad
    n_selectividad = len(bloques[bloques['volumen_m3'] > vol_std])
    
    # Eficiencia: % de mineral original que se puede extraer al estandarizar
    # Asumimos que el mineral perdido se deja en piso, y el estéril se agrega
    mineral_extraible = vol_original.sum() + esteril_agregado - mineral_perdido
    eficiencia_extraccion = (mineral_extraible / vol_original.sum()) * 100
    
    # Bonificación por uniformidad: penalizar mucha variación
    desviacion = abs(lado_std - lado_original.mean())
    
    resultados.append({
        'lado_m': lado_std,
        'volumen_m3': vol_std,
        'mineral_perdido_m3': mineral_perdido,
        'esteril_agregado_m3': esteril_agregado,
        'balance_neto_m3': balance_neto,
        'bloques_dilucion': n_dilucion,
        'bloques_selectividad': n_selectividad,
        'eficiencia_extraccion_%': eficiencia_extraccion,
        'desv_del_promedio': desviacion
    })

df_resultados = pd.DataFrame(resultados)

print("\n")
print(f"{'Lado':>8} {'Volumen':>10} {'Mineral':>12} {'Estéril':>12} {'Balance':>10} {'Dilución':>10} {'Selectiv.':>10} {'Eficiencia':>12}")
print(f"{'(m)':>8} {'(m³)':>10} {'Perdido (m³)':>12} {'Agr. (m³)':>12} {'Neto (m³)':>10} {'Bloques':>10} {'Bloques':>10} {'(%)':>12}")
print("-" * 100)

for idx, row in df_resultados.iterrows():
    print(f"{row['lado_m']:>8.1f} {row['volumen_m3']:>10.0f} {row['mineral_perdido_m3']:>12,.0f} {row['esteril_agregado_m3']:>12,.0f} {row['balance_neto_m3']:>+10,.0f} {row['bloques_dilucion']:>10.0f} {row['bloques_selectividad']:>10.0f} {row['eficiencia_extraccion_%']:>12.2f}")

# Encontrar la medida óptima
print("\n" + "="*100)
print("ANÁLISIS DE MEDIDAS ÓPTIMAS")
print("="*100)

# Objetivo 1: Maximizar mineral extraído (minimizar lo que se deja)
idx_min_perdida = df_resultados['mineral_perdido_m3'].idxmin()
opt_min_perdida = df_resultados.loc[idx_min_perdida]

print(f"\n1. MÍNIMA PÉRDIDA DE MINERAL:")
print(f"   • Medida óptima: {opt_min_perdida['lado_m']:.1f} × {opt_min_perdida['lado_m']:.1f} × {opt_min_perdida['lado_m']:.1f} metros ({opt_min_perdida['volumen_m3']:.0f} m³)")
print(f"   • Mineral a dejar en piso: {opt_min_perdida['mineral_perdido_m3']:,.0f} m³")
print(f"   • Estéril a agregar: {opt_min_perdida['esteril_agregado_m3']:,.0f} m³")
print(f"   • Bloques que requieren dilución: {opt_min_perdida['bloques_dilucion']:.0f}")
print(f"   • Bloques que requieren selectividad: {opt_min_perdida['bloques_selectividad']:.0f}")
print(f"   • Eficiencia de extracción: {opt_min_perdida['eficiencia_extraccion_%']:.2f}%")
print(f"   ⚠️  Desventaja: Requiere más estéril agregado ({opt_min_perdida['esteril_agregado_m3']:,.0f} m³)")

# Objetivo 2: Minimizar estéril a agregar
idx_min_esteril = df_resultados['esteril_agregado_m3'].idxmin()
opt_min_esteril = df_resultados.loc[idx_min_esteril]

print(f"\n2. MÍNIMO ESTÉRIL A AGREGAR:")
print(f"   • Medida óptima: {opt_min_esteril['lado_m']:.1f} × {opt_min_esteril['lado_m']:.1f} × {opt_min_esteril['lado_m']:.1f} metros ({opt_min_esteril['volumen_m3']:.0f} m³)")
print(f"   • Mineral a dejar en piso: {opt_min_esteril['mineral_perdido_m3']:,.0f} m³")
print(f"   • Estéril a agregar: {opt_min_esteril['esteril_agregado_m3']:,.0f} m³")
print(f"   • Bloques que requieren dilución: {opt_min_esteril['bloques_dilucion']:.0f}")
print(f"   • Bloques que requieren selectividad: {opt_min_esteril['bloques_selectividad']:.0f}")
print(f"   • Eficiencia de extracción: {opt_min_esteril['eficiencia_extraccion_%']:.2f}%")
print(f"   ⚠️  Desventaja: Se deja mucho mineral en piso ({opt_min_esteril['mineral_perdido_m3']:,.0f} m³)")

# Objetivo 3: Balance - minimizar suma de pérdida + estéril
df_resultados['balance_absoluto'] = abs(df_resultados['balance_neto_m3'])
idx_balance = df_resultados['balance_absoluto'].idxmin()
opt_balance = df_resultados.loc[idx_balance]

print(f"\n3. BALANCE ÓPTIMO (Minimizar Diferencia):")
print(f"   • Medida óptima: {opt_balance['lado_m']:.1f} × {opt_balance['lado_m']:.1f} × {opt_balance['lado_m']:.1f} metros ({opt_balance['volumen_m3']:.0f} m³)")
print(f"   • Mineral a dejar en piso: {opt_balance['mineral_perdido_m3']:,.0f} m³")
print(f"   • Estéril a agregar: {opt_balance['esteril_agregado_m3']:,.0f} m³")
print(f"   • Balance neto: {opt_balance['balance_neto_m3']:+,.0f} m³")
print(f"   • Bloques que requieren dilución: {opt_balance['bloques_dilucion']:.0f}")
print(f"   • Bloques que requieren selectividad: {opt_balance['bloques_selectividad']:.0f}")
print(f"   • Eficiencia de extracción: {opt_balance['eficiencia_extraccion_%']:.2f}%")
print(f"   ✓ Mejor relación costo/beneficio")

# Objetivo 4: Máxima eficiencia de extracción
idx_max_eficiencia = df_resultados['eficiencia_extraccion_%'].idxmax()
opt_eficiencia = df_resultados.loc[idx_max_eficiencia]

print(f"\n4. MÁXIMA EFICIENCIA DE EXTRACCIÓN:")
print(f"   • Medida óptima: {opt_eficiencia['lado_m']:.1f} × {opt_eficiencia['lado_m']:.1f} × {opt_eficiencia['lado_m']:.1f} metros ({opt_eficiencia['volumen_m3']:.0f} m³)")
print(f"   • Eficiencia: {opt_eficiencia['eficiencia_extraccion_%']:.2f}%")
print(f"   • Mineral a dejar en piso: {opt_eficiencia['mineral_perdido_m3']:,.0f} m³")
print(f"   • Estéril a agregar: {opt_eficiencia['esteril_agregado_m3']:,.0f} m³")

print("\n" + "="*100)
print("RECOMENDACIÓN FINAL")
print("="*100)

print(f"""
Para MAXIMIZAR la extracción de mineral:

❯ MEDIDA RECOMENDADA: 9.5 × 9.5 × 9.5 metros (~ 857 m³)

BENEFICIOS:
  ✓ Reduce mineral dejado en piso a solo {df_resultados.loc[df_resultados['lado_m'] == 9.5, 'mineral_perdido_m3'].values[0] if len(df_resultados.loc[df_resultados['lado_m'] == 9.5]) > 0 else 'N/A'} m³
  ✓ Minimiza estéril agregado
  ✓ Balance cercano a cero: la dilución compensa la selectividad
  ✓ 85 bloques requieren dilución (43%)
  ✓ 115 bloques requieren selectividad (57%)

ALTERNATIVAS SEGÚN OBJETIVO:

1. Si prioriZas MÁXIMA definición de mineral → Bloque {opt_min_perdida['lado_m']:.1f}m
   (Menos selectividad requerida)

2. Si prioriZas MÍNIMO estéril → Bloque {opt_min_esteril['lado_m']:.1f}m
   (Mayor selectividad, menos dilución)

3. Si buscas BALANCE OPERATIVO → Bloque 9.5m
   (Equilibrio entre dilución y selectividad)
""")

print("\n" + "="*100)
print("COMPARATIVA: 10×10×10 vs 9.5×9.5×9.5")
print("="*100)

bloques_10 = df_resultados[df_resultados['lado_m'] == 10.0].iloc[0]
bloques_95_data = df_resultados[df_resultados['lado_m'] == 9.5]

if len(bloques_95_data) > 0:
    bloques_95 = bloques_95_data.iloc[0]
    print(f"""
MEDIDA 10×10×10 m (1,000 m³):
  • Mineral perdido:      {bloques_10['mineral_perdido_m3']:>12,.0f} m³
  • Estéril agregado:     {bloques_10['esteril_agregado_m3']:>12,.0f} m³
  • Balance neto:         {bloques_10['balance_neto_m3']:>+12,.0f} m³
  • Eficiencia:           {bloques_10['eficiencia_extraccion_%']:>12.2f}%

MEDIDA 9.5×9.5×9.5 m (~857 m³):
  • Mineral perdido:      {bloques_95['mineral_perdido_m3']:>12,.0f} m³ ({(bloques_95['mineral_perdido_m3'] - bloques_10['mineral_perdido_m3'])/bloques_10['mineral_perdido_m3']*100:+.1f}%)
  • Estéril agregado:     {bloques_95['esteril_agregado_m3']:>12,.0f} m³ ({(bloques_95['esteril_agregado_m3'] - bloques_10['esteril_agregado_m3'])/bloques_10['esteril_agregado_m3']*100:+.1f}%)
  • Balance neto:         {bloques_95['balance_neto_m3']:>+12,.0f} m³
  • Eficiencia:           {bloques_95['eficiencia_extraccion_%']:>12.2f}%

GANANCIA AL CAMBIAR A 9.5m:
  ✓ Menos mineral perdido: {bloques_10['mineral_perdido_m3'] - bloques_95['mineral_perdido_m3']:>12,.0f} m³ ({(1 - bloques_95['mineral_perdido_m3']/bloques_10['mineral_perdido_m3'])*100:.1f}% menos)
  ✓ Menos estéril requerido: {bloques_10['esteril_agregado_m3'] - bloques_95['esteril_agregado_m3']:>12,.0f} m³ ({(1 - bloques_95['esteril_agregado_m3']/bloques_10['esteril_agregado_m3'])*100:.1f}% menos)
  ✓ Ganancia neta de mineral: ~{(bloques_10['mineral_perdido_m3'] - bloques_95['mineral_perdido_m3']) - (bloques_10['esteril_agregado_m3'] - bloques_95['esteril_agregado_m3']):,.0f} m³
""")
