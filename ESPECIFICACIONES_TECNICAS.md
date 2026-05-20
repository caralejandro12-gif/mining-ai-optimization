# 🔧 ESPECIFICACIONES TÉCNICAS - ENTREGA FINAL ML

## Documento de Referencia Técnica

Fecha: Mayo 2026  
Proyecto: Optimización de Rentabilidad en Operaciones Mineras  
Estado: Entrega Final Completa

---

## 1. ARQUITECTURA DE SOLUCIÓN

### 1.1 Problemas Modelados

#### Problema 1: REGRESIÓN
```
Entrada: Características del bloque minero (29+ variables)
         - Geológicas (ley Au, ley Ag, dureza)
         - Logísticas (distancias, destino)
         - Geometría (coordenadas 3D)
         - Variables derivadas (valor mineral, ROI, etc.)

Salida:  Margen rentable predicho (valor continuo en $)

Métrica Principal: R² Score (coeficiente de determinación)
Métricas Secundarias: RMSE, MAE
```

#### Problema 2: CLASIFICACIÓN
```
Entrada: Características del bloque minero (29+ variables)

Salida:  Rentabilidad binaria (0 = No Rentable, 1 = Rentable)

Métrica Principal: ROC-AUC
Métricas Secundarias: Accuracy, F1-Score, Precision, Recall
```

---

## 2. INGENIERÍA DE ATRIBUTOS

### Variables Creadas (14 totales)

| Categoría | Variable | Fórmula | Propósito |
|-----------|----------|---------|----------|
| **Metalúrgico** | ley_total | au + ag | Ley combinada |
| | ratio_au_ag | au / ag | Proporción de metales |
| | valor_mineral | ley_total × recuperación | Potencial metalúrgico |
| **Costo** | costo_por_tonelada | extracción / toneladas | Eficiencia de costos |
| | costo_total_per_ton | costo_total / toneladas_enviadas | Costo logístico |
| | roi | (valor - costo) / costo | Retorno de inversión |
| **Logístico** | distancia_total | planta + stock | Distancia combinada |
| | diferencia_distancias | \|planta - stock\| | Preferencia de destino |
| | proximidad_planta | 1 / (planta + 1) | Inverso de distancia |
| **Geométrico** | distancia_3d | √(x² + y² + z²) | Posición en mina |
| | profundidad | \|z\| | Nivel de excavación |
| **Rentabilidad** | margen_por_tonelada | margen / toneladas | Margen unitario |
| **Binaria** | es_rentable | margen > 0 | Target clasificación |
| | destino_binary | destino == 'planta' | Codificación destino |

### Normalización
```
StandardScaler aplicado a todas las variables numéricas
- Media: 0
- Desviación estándar: 1
```

---

## 3. MODELOS IMPLEMENTADOS

### 3.1 Regresión

#### Modelo 1: Random Forest Regressor
```python
RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

Parámetros por defecto
```

**Validación Cruzada**: 5-fold
**Esperado R²**: 0.75-0.82

#### Modelo 2: XGBoost Regressor (Base)
```python
xgb.XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42,
    verbosity=0
)
```

**Validación Cruzada**: 5-fold  
**Esperado R²**: 0.80-0.85

#### Modelo 3: XGBoost Optimizado
```python
# GridSearchCV con parámetros optimizados
Espacio de búsqueda:
- max_depth: [3, 5, 7]
- learning_rate: [0.05, 0.1, 0.15]
- n_estimators: [50, 100, 150]
- subsample: [0.8, 0.9]
- colsample_bytree: [0.8, 0.9]

Total combinaciones: 108
```

**Esperado R²**: 0.82-0.88 (mejora ~5-10%)

### 3.2 Clasificación

#### Modelo 1: Random Forest Classifier
```python
RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)
```

**Validación Cruzada**: 5-fold (stratificada)  
**Esperado ROC-AUC**: 0.85-0.90

#### Modelo 2: XGBoost Classifier (Base)
```python
xgb.XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42,
    verbosity=0
)
```

**Validación Cruzada**: 5-fold (stratificada)  
**Esperado ROC-AUC**: 0.88-0.93

#### Modelo 3: XGBoost Optimizado
```python
# RandomizedSearchCV con 20 iteraciones
Espacio de búsqueda:
- max_depth: [3, 5, 7, 9]
- learning_rate: [0.01, 0.05, 0.1, 0.15, 0.2]
- n_estimators: [50, 100, 150, 200]
- subsample: [0.6, 0.8, 0.9, 1.0]
- colsample_bytree: [0.6, 0.8, 0.9, 1.0]
- min_child_weight: [1, 3, 5]

Total iteraciones: 20
```

**Esperado ROC-AUC**: 0.90-0.95 (mejora ~2-5%)

---

## 4. MÉTRICA DE VALIDACIÓN

### Train/Test Split
```
Proporción: 80% Training, 20% Testing
Método: random_state=42 para reproducibilidad
Estratificación: Usada en clasificación para mantener 
                 proporciones de clases
```

### Cross-Validation
```
Regresión:
  - Método: 5-Fold Cross-Validation
  - Scoring: 'r2'
  
Clasificación:
  - Método: 5-Fold Stratified Cross-Validation
  - Scoring: 'roc_auc'
```

---

## 5. INTERPRETABILIDAD SHAP

### Explicador SHAP
```python
from shap import TreeExplainer

explainer = TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
```

### Visualizaciones Generadas

1. **Summary Plot (Bar)**: Importancia promedio de features
2. **Dependence Plots**: Relación entre feature y SHAP value
3. **Waterfall Plots**: Explicación de predicción individual
4. **Force Plots**: Visualización de contribuciones

---

## 6. CALIDAD DE DATOS

### Dataset Original
```
Bloques de Mina:
- Registros: ~200
- Columnas originales: 15
- Valores faltantes: 0

Planificación:
- Registros: ~145
- Columnas: 7
- Valores faltantes: 0
```

### Dataset Procesado
```
After Merge (Inner Join):
- Registros: 120+
- Columnas: 29 (15 originales + 14 derivadas)
- Valores faltantes: 0
- Proporción Rentables: ~60-65%
- Proporción No Rentables: ~35-40%
```

---

## 7. RENDIMIENTO ESPERADO

### Regresión
| Métrica | Base | Optimizado | Mejora |
|---------|------|-----------|--------|
| R² | 0.80-0.85 | 0.82-0.88 | +2-5% |
| RMSE | $80K-100K | $50K-80K | -30% |
| MAE | $60K-80K | $35K-60K | -25% |

### Clasificación
| Métrica | Base | Optimizado | Mejora |
|---------|------|-----------|--------|
| ROC-AUC | 0.88-0.93 | 0.90-0.95 | +2-4% |
| Accuracy | 0.85-0.90 | 0.87-0.92 | +1-3% |
| F1-Score | 0.85-0.90 | 0.87-0.92 | +1-3% |

---

## 8. DURACIÓN DE EJECUCIÓN

| Etapa | Tiempo Estimado |
|-------|-----------------|
| Carga de datos | ~1 seg |
| EDA | ~10 seg |
| Ingeniería de atributos | ~5 seg |
| Entrenamiento RF Regresión | ~3 seg |
| Entrenamiento XGB Regresión | ~2 seg |
| Entrenamiento RF Clasificación | ~2 seg |
| Entrenamiento XGB Clasificación | ~2 seg |
| GridSearchCV Regresión | ~5-10 min |
| RandomizedSearchCV Clasificación | ~3-5 min |
| SHAP Regresión | ~30 seg |
| SHAP Clasificación | ~30 seg |
| **TOTAL** | **~20-30 min** |

---

## 9. REQUISITOS DEL SISTEMA

### Hardware Mínimo
```
CPU: 4+ cores (8+ recomendado)
RAM: 8 GB (16 GB recomendado)
Almacenamiento: 2 GB libre
```

### Software
```
Python: 3.9 o superior
OS: Windows, Linux, macOS
```

### Dependencias Principales
```
numpy>=1.21
pandas>=1.3
scikit-learn>=1.0
xgboost>=1.5
shap>=0.40
matplotlib>=3.4
seaborn>=0.11
```

---

## 10. REPRODUCIBILIDAD

### Random Seeds
```python
random_state=42  # Utilizado en todos los modelos
                 # y splits para reproducibilidad
```

### Parámetros Fijos
```
Train/Test Split: 0.2 (80/20)
Cross-Validation: 5 folds
Validación Cruzada Random State: 42
```

### Cómo Reproducir
1. Usar mismo dataset
2. Mantener `random_state=42` en todos los modelos
3. Usar mismas versiones de librerías
4. Ejecutar celdas secuencialmente

---

## 11. NOTAS IMPORTANTES

- ⚠️ GridSearchCV puede tomar 5-10 minutos  
- ⚠️ SHAP analysis requiere cálculos intensivos
- ✓ Código es modular y puede adaptarse fácilmente
- ✓ Modelos guardan parámetros optimizados automáticamente

---

**Documento Técnico - Entrega Final ML**  
**Versión**: 1.0  
**Última actualización**: Mayo 2026
