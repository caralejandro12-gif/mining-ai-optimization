import pandas as pd

# Cargar datos
bloques = pd.read_csv("Datasource/bloques_volumenes.csv")

# Crear reporte HTML
html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Volúmenes - Bloques de Mina</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #1f4788;
            border-bottom: 3px solid #ff6b35;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #2c5aa0;
            margin-top: 30px;
            border-left: 5px solid #ff6b35;
            padding-left: 15px;
        }}
        .stats-box {{
            background-color: #f0f8ff;
            border-left: 4px solid #2c5aa0;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        .alert {{
            background-color: #fff3cd;
            border-left: 4px solid #ff6b35;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th {{
            background-color: #1f4788;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }}
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background-color: #f9f9f9;
        }}
        .highlight {{
            background-color: #fffacd;
            font-weight: bold;
        }}
        .metric {{
            display: inline-block;
            background-color: #e8f4f8;
            padding: 15px 20px;
            margin: 10px;
            border-radius: 4px;
            text-align: center;
            border-left: 4px solid #2c5aa0;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #1f4788;
        }}
        .metric-label {{
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #666;
        }}
        .notes {{
            background-color: #f0fff0;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 REPORTE DE VOLÚMENES Y MEDIDAS GEOMÉTRICAS</h1>
        <p><strong>Proyecto:</strong> Mining AI Optimization</p>
        <p><strong>Fecha:</strong> 2 de abril de 2026</p>
        <p><strong>Total de Bloques Analizados:</strong> {len(bloques)}</p>
        
        <h2>🎯 RESUMEN EJECUTIVO</h2>
        
        <div style="display: flex; flex-wrap: wrap;">
            <div class="metric">
                <div class="metric-value">{bloques['volumen_m3'].sum():,.0f}</div>
                <div class="metric-label">Volumen Total (m³)</div>
            </div>
            <div class="metric">
                <div class="metric-value">{bloques['volumen_m3'].mean():.2f}</div>
                <div class="metric-label">Volumen Promedio (m³)</div>
            </div>
            <div class="metric">
                <div class="metric-value">{bloques['lado_bloque_m'].mean():.2f}</div>
                <div class="metric-label">Lado Promedio (m)</div>
            </div>
            <div class="metric">
                <div class="metric-value">{bloques['toneladas'].sum():,.0f}</div>
                <div class="metric-label">Toneladas Totales</div>
            </div>
        </div>

        <div class="alert">
            <strong>ℹ️ Nota Importante:</strong> Los volúmenes fueron calculados utilizando una <strong>densidad estándar de 2.7 ton/m³</strong> 
            (típica para roca mineralizada con oro y plata). Los bloques se asumen como <strong>cubos</strong> para fines de cálculo de geometría.
        </div>

        <h2>📈 ESTADÍSTICAS DETALLADAS</h2>

        <h3>Volumen de Bloques (m³)</h3>
        <div class="stats-box">
            <p><strong>Volumen Total:</strong> {bloques['volumen_m3'].sum():,.2f} m³</p>
            <p><strong>Promedio:</strong> {bloques['volumen_m3'].mean():.2f} m³</p>
            <p><strong>Desviación Estándar:</strong> {bloques['volumen_m3'].std():.2f} m³</p>
            <p><strong>Mínimo:</strong> {bloques['volumen_m3'].min():.2f} m³ (Bloque #{bloques.loc[bloques['volumen_m3'].idxmin(), 'id_bloque']})</p>
            <p><strong>Máximo:</strong> {bloques['volumen_m3'].max():.2f} m³ (Bloque #{bloques.loc[bloques['volumen_m3'].idxmax(), 'id_bloque']})</p>
            <p><strong>Percentil 25:</strong> {bloques['volumen_m3'].quantile(0.25):.2f} m³</p>
            <p><strong>Mediana (Percentil 50):</strong> {bloques['volumen_m3'].median():.2f} m³</p>
            <p><strong>Percentil 75:</strong> {bloques['volumen_m3'].quantile(0.75):.2f} m³</p>
        </div>

        <h3>Lado del Bloque Equivalente (m) - Asumiendo Geometría Cúbica</h3>
        <div class="stats-box">
            <p><strong>Promedio:</strong> {bloques['lado_bloque_m'].mean():.2f} m</p>
            <p><strong>Desviación Estándar:</strong> {bloques['lado_bloque_m'].std():.2f} m</p>
            <p><strong>Mínimo:</strong> {bloques['lado_bloque_m'].min():.2f} m</p>
            <p><strong>Máximo:</strong> {bloques['lado_bloque_m'].max():.2f} m</p>
            <p><strong>Rango:</strong> {bloques['lado_bloque_m'].max() - bloques['lado_bloque_m'].min():.2f} m</p>
        </div>

        <h3>Toneladas de Mineral</h3>
        <div class="stats-box">
            <p><strong>Total:</strong> {bloques['toneladas'].sum():,.2f} toneladas</p>
            <p><strong>Promedio:</strong> {bloques['toneladas'].mean():.2f} toneladas por bloque</p>
            <p><strong>Desviación Estándar:</strong> {bloques['toneladas'].std():.2f} toneladas</p>
            <p><strong>Mínimo:</strong> {bloques['toneladas'].min():.2f} toneladas</p>
            <p><strong>Máximo:</strong> {bloques['toneladas'].max():.2f} toneladas</p>
        </div>

        <h2>📍 ESTADÍSTICAS POR NIVEL MINERO</h2>
"""

# Agregar tabla por nivel
nivel_stats = bloques.groupby('nivel').agg({
    'id_bloque': 'count',
    'volumen_m3': ['sum', 'mean', 'min', 'max'],
    'lado_bloque_m': ['mean', 'min', 'max'],
    'toneladas': ['sum', 'mean']
}).round(2)

html_content += """
        <table>
            <tr>
                <th>Nivel</th>
                <th>Bloques</th>
                <th>Vol. Total (m³)</th>
                <th>Vol. Promedio (m³)</th>
                <th>Vol. Mín-Máx (m³)</th>
                <th>Lado Promedio (m)</th>
                <th>Ton. Total</th>
                <th>Ton. Promedio</th>
            </tr>
"""

for nivel in range(1, 10):
    if nivel in bloques['nivel'].values:
        nivel_data = bloques[bloques['nivel'] == nivel]
        html_content += f"""
            <tr>
                <td class="highlight">{nivel}</td>
                <td>{len(nivel_data)}</td>
                <td>{nivel_data['volumen_m3'].sum():,.2f}</td>
                <td>{nivel_data['volumen_m3'].mean():.2f}</td>
                <td>{nivel_data['volumen_m3'].min():.2f} - {nivel_data['volumen_m3'].max():.2f}</td>
                <td>{nivel_data['lado_bloque_m'].mean():.2f}</td>
                <td>{nivel_data['toneladas'].sum():,.2f}</td>
                <td>{nivel_data['toneladas'].mean():.2f}</td>
            </tr>
"""

html_content += """
        </table>

        <h2>📋 TOP 10 BLOQUES POR VOLUMEN</h2>
"""

top_10 = bloques.nlargest(10, 'volumen_m3')[['id_bloque', 'nivel', 'volumen_m3', 'lado_bloque_m', 'toneladas', 'x', 'y', 'z']]

html_content += """
        <table>
            <tr>
                <th>ID Bloque</th>
                <th>Nivel</th>
                <th>Volumen (m³)</th>
                <th>Lado (m)</th>
                <th>Toneladas</th>
                <th>Coordenadas (x, y, z)</th>
            </tr>
"""

for idx, row in top_10.iterrows():
    html_content += f"""
            <tr>
                <td class="highlight">{int(row['id_bloque'])}</td>
                <td>{int(row['nivel'])}</td>
                <td>{row['volumen_m3']:.2f}</td>
                <td>{row['lado_bloque_m']:.2f}</td>
                <td>{row['toneladas']:.2f}</td>
                <td>({row['x']:.1f}, {row['y']:.1f}, {row['z']:.1f})</td>
            </tr>
"""

html_content += """
        </table>

        <h2>🔍 NOTAS TÉCNICAS</h2>
        <div class="notes">
            <h4>Metodología de Cálculo:</h4>
            <ul>
                <li><strong>Densidad utilizada:</strong> 2.7 ton/m³ (estándar para minerales de oro/plata en roca)</li>
                <li><strong>Volumen (m³) = Toneladas / Densidad</strong></li>
                <li><strong>Lado del bloque (m) = ∛(Volumen)</strong> (asumiendo geometría cúbica)</li>
            </ul>
            <h4>Fuente de Datos:</h4>
            <ul>
                <li>Archivo: Datasource/bloques_mina.csv</li>
                <li>Total de registros: {len(bloques)}</li>
                <li>Niveles mineros: {len(bloques['nivel'].unique())}</li>
            </ul>
        </div>

        <h2>📁 ARCHIVOS GENERADOS</h2>
        <div class="stats-box">
            <ul>
                <li><strong>bloques_volumenes.csv</strong> - Detalle de volumen para cada bloque</li>
                <li><strong>estadisticas_por_nivel.csv</strong> - Resumen estadístico por nivel</li>
                <li><strong>analisis_volumenes.png</strong> - Gráficos de análisis</li>
                <li><strong>reporte_volumenes.html</strong> - Este reporte</li>
            </ul>
        </div>

        <div class="footer">
            <p><strong>Reporte generado automáticamente</strong> - Proyecto Mining AI Optimization</p>
            <p>Para más información, consulte los archivos CSV y el análisis gráfico adjunto.</p>
        </div>
    </div>
</body>
</html>
"""

# Guardar HTML
with open("Datasource/reporte_volumenes.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✓ Reporte HTML generado: Datasource/reporte_volumenes.html")

# Crear también un resumen en texto
with open("Datasource/resumen_volumenes.txt", "w", encoding="utf-8") as f:
    f.write("""
╔════════════════════════════════════════════════════════════════════════════════╗
║          REPORTE DE VOLÚMENES Y MEDIDAS GEOMÉTRICAS - BLOQUES DE MINA         ║
║                                                                                ║
║                      Proyecto: Mining AI Optimization                          ║
║                         Fecha: 2 de abril de 2026                             ║
╚════════════════════════════════════════════════════════════════════════════════╝

═════════════════════════════════════════════════════════════════════════════════
RESUMEN EJECUTIVO
═════════════════════════════════════════════════════════════════════════════════

Total de Bloques Analizados:           {len(bloques)} unidades

Densidad del Mineral Utilizada:        2.7 ton/m³
(Estándar para minerales de oro/plata en roca)

═════════════════════════════════════════════════════════════════════════════════
VOLÚMENES (m³)
═════════════════════════════════════════════════════════════════════════════════

    Volumen Total              :  {bloques['volumen_m3'].sum():>15,.2f} m³
    Volumen Promedio           :  {bloques['volumen_m3'].mean():>15,.2f} m³
    Desviación Estándar        :  {bloques['volumen_m3'].std():>15,.2f} m³
    
    Mínimo                     :  {bloques['volumen_m3'].min():>15,.2f} m³  (Bloque #{int(bloques.loc[bloques['volumen_m3'].idxmin(), 'id_bloque'])})
    Máximo                     :  {bloques['volumen_m3'].max():>15,.2f} m³  (Bloque #{int(bloques.loc[bloques['volumen_m3'].idxmax(), 'id_bloque'])})
    
    Percentil 25%              :  {bloques['volumen_m3'].quantile(0.25):>15,.2f} m³
    Mediana                    :  {bloques['volumen_m3'].median():>15,.2f} m³
    Percentil 75%              :  {bloques['volumen_m3'].quantile(0.75):>15,.2f} m³

═════════════════════════════════════════════════════════════════════════════════
MEDIDAS GEOMÉTRICAS - LADO DEL BLOQUE (m)
═════════════════════════════════════════════════════════════════════════════════
(Asumiendo bloques de geometría cúbica: Lado = ∛Volumen)

    Lado Promedio              :  {bloques['lado_bloque_m'].mean():>15,.2f} m
    Desviación Estándar        :  {bloques['lado_bloque_m'].std():>15,.2f} m
    
    Mínimo                     :  {bloques['lado_bloque_m'].min():>15,.2f} m
    Máximo                     :  {bloques['lado_bloque_m'].max():>15,.2f} m
    Rango                      :  {bloques['lado_bloque_m'].max() - bloques['lado_bloque_m'].min():>15,.2f} m

═════════════════════════════════════════════════════════════════════════════════
TONELADAS DE MINERAL
═════════════════════════════════════════════════════════════════════════════════

    Total de Toneladas         :  {bloques['toneladas'].sum():>15,.2f} ton
    Promedio por Bloque        :  {bloques['toneladas'].mean():>15,.2f} ton
    Desviación Estándar        :  {bloques['toneladas'].std():>15,.2f} ton
    
    Mínimo                     :  {bloques['toneladas'].min():>15,.2f} ton
    Máximo                     :  {bloques['toneladas'].max():>15,.2f} ton

═════════════════════════════════════════════════════════════════════════════════
ESTADÍSTICAS POR NIVEL MINERO
═════════════════════════════════════════════════════════════════════════════════
""")
    
    for nivel in range(1, 10):
        if nivel in bloques['nivel'].values:
            nivel_data = bloques[bloques['nivel'] == nivel]
            f.write(f"""
Nivel {nivel}:
  • Cantidad de Bloques        :  {len(nivel_data):>3} bloques
  • Volumen Total             :  {nivel_data['volumen_m3'].sum():>12,.2f} m³
  • Volumen Promedio          :  {nivel_data['volumen_m3'].mean():>12,.2f} m³
  • Volumen Min-Max           :  {nivel_data['volumen_m3'].min():.2f} - {nivel_data['volumen_m3'].max():.2f} m³
  • Lado Promedio             :  {nivel_data['lado_bloque_m'].mean():>12,.2f} m
  • Toneladas Total           :  {nivel_data['toneladas'].sum():>12,.2f} ton
  • Toneladas Promedio        :  {nivel_data['toneladas'].mean():>12,.2f} ton
""")

    f.write(f"""
═════════════════════════════════════════════════════════════════════════════════
TOP 10 BLOQUES POR VOLUMEN
═════════════════════════════════════════════════════════════════════════════════

""")
    
    top_10 = bloques.nlargest(10, 'volumen_m3')
    f.write(f"{'ID':>4} {'Nivel':>5} {'Volumen (m³)':>15} {'Lado (m)':>12} {'Toneladas':>15}\n")
    f.write("-" * 55 + "\n")
    for idx, row in top_10.iterrows():
        f.write(f"{int(row['id_bloque']):>4} {int(row['nivel']):>5} {row['volumen_m3']:>15.2f} {row['lado_bloque_m']:>12.2f} {row['toneladas']:>15.2f}\n")

    f.write(f"""
═════════════════════════════════════════════════════════════════════════════════
ARCHIVOS GENERADOS
═════════════════════════════════════════════════════════════════════════════════

✓ bloques_volumenes.csv           - Detalle completo de cada bloque
✓ estadisticas_por_nivel.csv      - Resumen estadístico por nivel
✓ analisis_volumenes.png          - Gráficos de análisis visual
✓ reporte_volumenes.html          - Reporte interactivo en HTML
✓ resumen_volumenes.txt           - Este resumen en texto

═════════════════════════════════════════════════════════════════════════════════
NOTAS TÉCNICAS
═════════════════════════════════════════════════════════════════════════════════

Metodología de Cálculo:
  • Densidad utilizada : 2.7 ton/m³ (estándar para minerales de oro/plata)
  • Volumen (m³)      : Toneladas ÷ Densidad
  • Lado del bloque   : ∛(Volumen en m³) - asumiendo geometría cúbica

Supuestos:
  • Los bloques se asumen como cubos regulares
  • La densidad es constante para todos los bloques
  • Los datos provienen del archivo bloques_mina.csv

═════════════════════════════════════════════════════════════════════════════════
Generado automáticamente - Proyecto Mining AI Optimization
═════════════════════════════════════════════════════════════════════════════════
""")

print("✓ Resumen en texto generado: Datasource/resumen_volumenes.txt")
print("\n" + "="*80)
print("TODOS LOS REPORTES HAN SIDO GENERADOS EXITOSAMENTE")
print("="*80)
