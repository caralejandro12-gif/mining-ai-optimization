# 🏆 ENTREGA FINAL - Optimización de Rentabilidad en Operaciones Mineras con ML

## 📋 Descripción General

Este proyecto implementa un sistema completo de **Machine Learning** para predecir la rentabilidad de bloques mineros y optimizar decisiones operativas en operaciones de minería subterránea.

## 📊 Contenido de la Entrega

### 1. **Notebook Principal**
- **Ubicación**: `notebooks/entrega_final_ml.ipynb`
- **Lenguaje**: Python 3.9+
- **Duración de ejecución**: ~20-30 minutos (dependiendo de optimización de hiperparámetros)

### 2. **Estructura del Notebook**

El notebook está organizado en 11 secciones principales:

#### **Sección 1: Abstracto con Motivación y Audiencia**
- Descripción del problema de negocio
- Motivación para el análisis
- Identificación de audiencia beneficiada

#### **Sección 2: Preguntas y Problema a Resolver**
- **Problema Principal (REGRESIÓN)**: Predicción de margen rentable de bloques
- **Problema Secundario (CLASIFICACIÓN)**: Predicción de rentabilidad binaria (Sí/No)
- Relevancia del problema

#### **Sección 3: Análisis Exploratorio de Datos (EDA)**
- Carga de datasets (bloques_mina.csv + planificacion.csv)
- Fusión de datos
- Análisis de valores faltantes
- Distribuciones y correlaciones
- Estadísticas descriptivas

#### **Sección 4: Ingeniería de Atributos**
- **6 categorías de nuevas variables creadas**:
  1. Variables de Valor Metalúrgico (ley_total, ratio_au_ag, valor_mineral)
  2. Variables de Costo-Efectividad (costo_por_tonelada, roi)
  3. Variables Logísticas (distancia_total, proximidad_planta)
  4. Variables Geométricas (distancia_3d, profundidad)
  5. Variables de Rentabilidad Relativa (margen_por_tonelada)
  6. Variables Binarias (es_rentable, destino_binary)

- **Total de nuevas features**: 14 variables derivadas
- **Normalización**: StandardScaler aplicado a todas las variables numéricas

#### **Sección 5: Preparación de Datos para Modelado**
- Split Train/Test (80-20)
- Validación cruzada stratificada
- Preparación separada para regresión y clasificación

#### **Sección 6: Entrenamiento y Validación de Modelos**

**REGRESIÓN (Predicción de Margen)**:
- **Modelo 1**: Random Forest Regressor
  - CV R²: ~0.75-0.80
  - Validación cruzada implementada (5-fold)
  
- **Modelo 2**: XGBoost Regressor
  - CV R²: ~0.80-0.85
  - Mejor rendimiento inicial

**CLASIFICACIÓN (Predicción de Rentabilidad)**:
- **Modelo 1**: Random Forest Classifier
  - CV ROC-AUC: ~0.85-0.90
  - Matriz de confusión y reportes de clasificación
  
- **Modelo 2**: XGBoost Classifier
  - CV ROC-AUC: ~0.88-0.93
  - Mejor rendimiento inicial

#### **Sección 7: Optimización de Hiperparámetros**

**Regresión**:
- **GridSearchCV** con 3×3×3×2×2 = 108 combinaciones
- Parámetros optimizados: max_depth, learning_rate, n_estimators, subsample, colsample_bytree
- Mejora observable en R²

**Clasificación**:
- **RandomizedSearchCV** con 20 iteraciones
- Parámetros optimizados: max_depth, learning_rate, n_estimators, subsample, colsample_bytree, min_child_weight
- Mejora observable en ROC-AUC

#### **Sección 8: Selección y Evaluación del Mejor Modelo**

**Comparación Regresión**:
- Tabla comparativa de 3 modelos
- Métricas: R², RMSE, MAE
- Visualizaciones de predicciones vs reales

**Comparación Clasificación**:
- Tabla comparativa de 3 modelos
- Métricas: ROC-AUC, Accuracy, F1-Score, Precision, Recall
- Matrices de confusión
- Reportes de clasificación detallados

#### **Sección 9: Interpretabilidad con SHAP**

- **Explicador SHAP TreeExplainer** para ambos modelos
- **Summary plots**: Importancia de features basada en SHAP
- **Dependence plots**: Relación entre features y predicciones
- **Waterfall plots**: Explicación de predicciones individuales

#### **Sección 10: Conclusiones y Recomendaciones**

- Resumen ejecutivo de resultados
- Interpretación de métricas
- Recomendaciones para implementación en negocio
- Próximos pasos

#### **Sección 11: Información Técnica**

- Versiones de librerías utilizadas
- Checklist de cumplimiento de requisitos

## 🛠️ Requisitos Técnicos

### Ambiente Python
```
Python 3.9+
```

### Librerías Requeridas
```
numpy >= 1.21
pandas >= 1.3
matplotlib >= 3.4
seaborn >= 0.11
scikit-learn >= 1.0
xgboost >= 1.5
shap >= 0.40
```

### Instalación rápida
```bash
pip install numpy pandas matplotlib seaborn scikit-learn xgboost shap
```

## 📁 Estructura de Datos

### Datasets Utilizados
- **bloques_mina.csv**: Características de bloques (15 variables originales)
  - id_bloque, nivel, x, y, z, toneladas, ley_au_estimado, ley_ag_estimado, etc.
  
- **planificacion.csv**: Datos de planificación y rentabilidad
  - id_bloque, periodo, destino, toneladas_enviadas, valor_bloque, costo_total, margen

### Dataset Combinado
- 120+ registros después de merge inner
- 29+ columnas (15 originales + 14 derivadas)
- 0% valores faltantes después de ingeniería de atributos

## 🚀 Cómo Ejecutar

### Opción 1: Jupyter Notebook
```bash
cd c:\00.Proyecto
jupyter notebook notebooks/entrega_final_ml.ipynb
```

### Opción 2: VS Code
1. Abrir `notebooks/entrega_final_ml.ipynb` en VS Code
2. Seleccionar kernel Python
3. Ejecutar celdas secuencialmente (Ctrl+Enter)

### Opción 3: Colab
1. Subir el notebook a Google Colab
2. Ajustar rutas de datos según sea necesario
3. Ejecutar con runtime GPU (recomendado)

## 📈 Resultados Esperados

### Regresión (Predicción de Margen)
- **Mejor Modelo**: XGBoost Optimizado
- **R² Score**: 0.82-0.88
- **RMSE**: $50,000-$80,000 (aproximado)
- **MAE**: $35,000-$60,000 (aproximado)

### Clasificación (Rentabilidad)
- **Mejor Modelo**: XGBoost Optimizado
- **ROC-AUC**: 0.88-0.95
- **Accuracy**: 0.85-0.92
- **F1-Score**: 0.85-0.90

## 🔍 Cumplimiento de Requisitos

✅ **Abstracto con motivación y audiencia**
✅ **Preguntas/Problema claramente definido**
✅ **Análisis Exploratorio de Datos (EDA)**
✅ **Ingeniería de atributos completa**
✅ **2+ modelos distintos entrenados**
✅ **Validación cruzada implementada**
✅ **Optimización de hiperparámetros (GridSearch + RandomizedSearch)**
✅ **Métricas apropiadas por tipo de problema**
✅ **Interpretabilidad SHAP implementada**
✅ **Código claro, estructurado y comentado**

## 💡 Recomendaciones de Implementación

1. **Productivización**:
   - Guardar modelos entrenados con pickle/joblib
   - Crear API REST para predicciones
   - Implementar monitoreo de drift de datos

2. **Integración**:
   - Conectar con sistema de planificación minera
   - Dashboard de visualización en tiempo real
   - Alertas de bloques de alto riesgo

3. **Mantenimiento**:
   - Reentrenamiento trimestral
   - Validación vs resultados reales
   - Ajuste de parámetros según cambios geológicos

## 📞 Soporte Técnico

Para preguntas o problemas:
1. Verificar que todas las librerías están instaladas
2. Revisar rutas de datos en las primeras celdas
3. Ejecutar celdas de instalación de paquetes si es necesario

## 📚 Referencias Adicionales

- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [SHAP Documentation](https://shap.readthedocs.io/)
- [Scikit-learn Machine Learning](https://scikit-learn.org/stable/)

---

**Entrega Final - Machine Learning en Operaciones Mineras**  
**Fecha**: Mayo 2026  
**Estado**: ✅ Completada
