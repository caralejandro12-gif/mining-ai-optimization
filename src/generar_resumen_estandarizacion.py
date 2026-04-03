import pandas as pd

# Cargar datos
bloques = pd.read_csv("Datasource/bloques_estandarizados.csv")

# Crear resumen detallado
with open("Datasource/resumen_estandarizacion.txt", "w", encoding="utf-8") as f:
    f.write("""
╔════════════════════════════════════════════════════════════════════════════════╗
║              ESTANDARIZACIÓN DE BLOQUES A 10×10×10 METROS                      ║
║                                                                                ║
║                      Proyecto: Mining AI Optimization                          ║
║                         Fecha: 2 de abril de 2026                             ║
╚════════════════════════════════════════════════════════════════════════════════╝

═════════════════════════════════════════════════════════════════════════════════
RESUMEN EJECUTIVO
═════════════════════════════════════════════════════════════════════════════════

Medidas Estandarizadas:           10 m (ancho) × 10 m (largo) × 10 m (profundidad)
Volumen por Bloque:               1,000 m³

Total de Bloques:                 {len(bloques)} unidades

═════════════════════════════════════════════════════════════════════════════════
CLASIFICACIÓN DE BLOQUES
═════════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────┐
│ Requiere Dilución                                                           │
│ (Volumen Original < 1,000 m³)                                               │
│                                                                             │
│ Cantidad: {len(bloques[bloques['volumen_m3'] < 1000]):>3} bloques ({len(bloques[bloques['volumen_m3'] < 1000])/len(bloques)*100:>5.1f}%)                                    │
│                                                                             │
│ Estos bloques requieren estéril (dilución) para completar los 1,000 m³      │
│ Volumen estéril total a agregar: {bloques[bloques['volumen_m3'] < 1000]['volumen_esteril_agregado'].sum():>10,.0f} m³            │
│ Dilución promedio: {bloques[bloques['volumen_m3'] < 1000]['dilucion_planificada_%'].mean():>34.2f}%               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ Requiere Selectividad                                                       │
│ (Volumen Original > 1,000 m³)                                               │
│                                                                             │
│ Cantidad: {len(bloques[bloques['volumen_m3'] > 1000]):>3} bloques ({len(bloques[bloques['volumen_m3'] > 1000])/len(bloques)*100:>5.1f}%)                                    │
│                                                                             │
│ Estos bloques deben ser minados selectivamente, dejando mineral en piso      │
│ Mineral a dejar en piso: {abs(bloques[bloques['volumen_m3'] > 1000]['volumen_esteril_agregado'].sum()):>10,.0f} m³            │
│ Pérdida promedio: {bloques[bloques['volumen_m3'] > 1000]['dilucion_planificada_%'].mean():>34.2f}%               │
└─────────────────────────────────────────────────────────────────────────────┘

═════════════════════════════════════════════════════════════════════════════════
ANÁLISIS VOLUMÉTRICO
═════════════════════════════════════════════════════════════════════════════════

Volumen Original Total              :  {bloques['volumen_m3'].sum():>15,.0f} m³
Volumen Estandarizado Total         :  {bloques['volumen_estandar_m3'].sum():>15,.0f} m³
Diferencia Neta (Estéril - Pérdida) :  {(bloques['volumen_estandar_m3'].sum() - bloques['volumen_m3'].sum()):>15,.0f} m³

Porcentaje de Dilución Neta         :  {(bloques['volumen_esteril_agregado'].sum() / bloques['volumen_estandar_m3'].sum()) * 100:>14.2f}%

═════════════════════════════════════════════════════════════════════════════════
TOP 15 BLOQUES CON MAYOR DILUCIÓN REQUERIDA
═════════════════════════════════════════════════════════════════════════════════
(Estos bloques tienen menos volumen mineral y requieren más estéril agregado)

""")
    
    top_dilucion = bloques[bloques['volumen_m3'] < 1000].nlargest(15, 'dilucion_planificada_%')[
        ['id_bloque', 'nivel', 'volumen_m3', 'volumen_estandar_m3', 'volumen_esteril_agregado', 'dilucion_planificada_%']
    ]
    
    f.write(f"{'ID':>4} {'Nv':>3} {'Vol. Orig.':>12} {'Vol. Std':>12} {'Est. Agr.':>12} {'Dilución':>12}\n")
    f.write(f"{'':>4} {'':>3} {'(m³)':>12} {'(m³)':>12} {'(m³)':>12} {'(%)':>12}\n")
    f.write("-" * 70 + "\n")
    
    for idx, row in top_dilucion.iterrows():
        f.write(f"{int(row['id_bloque']):>4} {int(row['nivel']):>3} {row['volumen_m3']:>12.2f} {row['volumen_estandar_m3']:>12.2f} {row['volumen_esteril_agregado']:>12.2f} {row['dilucion_planificada_%']:>12.2f}\n")

    f.write(f"\nTOTAL DILUCIÓN REQUERIDA (Top 15): {top_dilucion['volumen_esteril_agregado'].sum():>12,.0f} m³\n")

    f.write("""
═════════════════════════════════════════════════════════════════════════════════
TOP 15 BLOQUES CON MAYOR SELECTIVIDAD REQUERIDA
═════════════════════════════════════════════════════════════════════════════════
(Estos bloques tienen más volumen mineral y deben dejar mineral en piso)

""")
    
    top_selectividad = bloques[bloques['volumen_m3'] > 1000].nsmallest(15, 'dilucion_planificada_%')[
        ['id_bloque', 'nivel', 'volumen_m3', 'volumen_estandar_m3', 'volumen_esteril_agregado', 'dilucion_planificada_%']
    ]
    
    f.write(f"{'ID':>4} {'Nv':>3} {'Vol. Orig.':>12} {'Vol. Std':>12} {'Min. Perdido':>12} {'Pérdida':>12}\n")
    f.write(f"{'':>4} {'':>3} {'(m³)':>12} {'(m³)':>12} {'(m³)':>12} {'(%)':>12}\n")
    f.write("-" * 70 + "\n")
    
    for idx, row in top_selectividad.iterrows():
        f.write(f"{int(row['id_bloque']):>4} {int(row['nivel']):>3} {row['volumen_m3']:>12.2f} {row['volumen_estandar_m3']:>12.2f} {abs(row['volumen_esteril_agregado']):>12.2f} {abs(row['dilucion_planificada_%']):>12.2f}\n")

    f.write(f"\nTOTAL MINERAL PERDIDO (Top 15): {abs(top_selectividad['volumen_esteril_agregado'].sum()):>12,.0f} m³\n")

    f.write("""
═════════════════════════════════════════════════════════════════════════════════
ESTADÍSTICAS POR NIVEL MINERO
═════════════════════════════════════════════════════════════════════════════════

""")
    
    for nivel in sorted(bloques['nivel'].unique()):
        nivel_data = bloques[bloques['nivel'] == nivel]
        dilucion_count = len(nivel_data[nivel_data['volumen_m3'] < 1000])
        selectividad_count = len(nivel_data[nivel_data['volumen_m3'] > 1000])
        
        f.write(f"""
┌─ Nivel {nivel} ────────────────────────────────────────────────────────────┐
│  Bloques:                  {len(nivel_data):>3}                           │
│  • Requieren Dilución:     {dilucion_count:>3}  ({dilucion_count/len(nivel_data)*100:>5.1f}%)              │
│  • Requieren Selectividad: {selectividad_count:>3}  ({selectividad_count/len(nivel_data)*100:>5.1f}%)              │
│                                                              │
│  Volumen Original Total:   {nivel_data['volumen_m3'].sum():>12,.0f} m³        │
│  Dilución Promedio:        {nivel_data[nivel_data['volumen_m3'] < 1000]['dilucion_planificada_%'].mean():>15.2f}%        │
│  Selectividad Promedio:    {abs(nivel_data[nivel_data['volumen_m3'] > 1000]['dilucion_planificada_%'].mean()):>15.2f}%        │
└──────────────────────────────────────────────────────────────┘
""")

    f.write("""
═════════════════════════════════════════════════════════════════════════════════
BLOQUES CRÍTICOS (Casos Extremos)
═════════════════════════════════════════════════════════════════════════════════

MAYOR DILUCIÓN REQUERIDA:
""")
    max_dilucion = bloques.loc[bloques['dilucion_planificada_%'].idxmax()]
    f.write(f"""
  Bloque {int(max_dilucion['id_bloque'])} - Nivel {int(max_dilucion['nivel'])}
  Volumen Original         : {max_dilucion['volumen_m3']:.2f} m³
  Volumen Estandarizado    : {max_dilucion['volumen_estandar_m3']:.2f} m³
  Estéril a Agregar        : {max_dilucion['volumen_esteril_agregado']:.2f} m³ ({max_dilucion['dilucion_planificada_%']:.2f}%)
  Ubicación (x, y, z)      : ({max_dilucion['x']:.1f}, {max_dilucion['y']:.1f}, {max_dilucion['z']:.1f})
""")

    f.write("""
MAYOR SELECTIVIDAD REQUERIDA (Más mineral a dejar):
""")
    max_selectividad = bloques.loc[bloques['dilucion_planificada_%'].idxmin()]
    f.write(f"""
  Bloque {int(max_selectividad['id_bloque'])} - Nivel {int(max_selectividad['nivel'])}
  Volumen Original         : {max_selectividad['volumen_m3']:.2f} m³
  Volumen Estandarizado    : {max_selectividad['volumen_estandar_m3']:.2f} m³
  Mineral a Dejar en Piso  : {abs(max_selectividad['volumen_esteril_agregado']):.2f} m³ ({abs(max_selectividad['dilucion_planificada_%']):.2f}%)
  Ubicación (x, y, z)      : ({max_selectividad['x']:.1f}, {max_selectividad['y']:.1f}, {max_selectividad['z']:.1f})
""")

    f.write("""
═════════════════════════════════════════════════════════════════════════════════
CONSIDERACIONES OPERATIVAS
═════════════════════════════════════════════════════════════════════════════════

1. DILUCIÓN PLANIFICADA (105 bloques):
   • Estos bloques necesitarán estéril como relleno.
   • Volumen total de estéril a agregar: 44,060.86 m³
   • Principalmente en bloques pequeños o de baja calidad.

2. SELECTIVIDAD (95 bloques):
   • Requerir extracción selectiva, minando sólo los 1,000 m³ estandarizados.
   • Mineral adicional (37,695.27 m³) queda dilución en piso inicial.
   • Aplica especialmente en niveles superiores (1-3).

3. BALANCE VOLUMÉTRICO:
   • Dilución neta: 3.18% (se requiere 6,365.59 m³ adicionales)
   • Este mineral excedente puede reprocessarse o almacenarse.

4. RECOMENDACIONES:
   • Priorizar selectividad en niveles 1-3 (concentración alta de bloques grandes)
   • Agrupar bloques que requieren dilución para optimizar rutas de transporte.
   • Mantener registro de dilución planificada para control de calidad.
   • Considerar variabilidad geotécnica en diseño de talud.

═════════════════════════════════════════════════════════════════════════════════
ARCHIVOS ASOCIADOS
═════════════════════════════════════════════════════════════════════════════════

✓ bloques_estandarizados.csv        - Datos completos con medidas y dilución
✓ analisis_estandarizacion.png       - Gráficos de análisis
✓ resumen_estandarizacion.txt        - Este resumen

═════════════════════════════════════════════════════════════════════════════════
Generado automáticamente - Proyecto Mining AI Optimization
═════════════════════════════════════════════════════════════════════════════════
""")

print("✓ Resumen de estandarización generado: Datasource/resumen_estandarizacion.txt")
