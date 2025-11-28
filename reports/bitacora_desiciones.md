# Bitácora de Decisiones - Análisis de Patrones de Ventas

## 1. Limpieza de Datos

### 1.1 Eliminación de Duplicados
- Identificamos 29 registros duplicados en `ID_Venta` (de 3029 a 3000 registros únicos)
- **Decisión:** Eliminamos duplicados usando `drop_duplicates(subset='ID_Venta')`
- **Justificación:** Los duplicados representan errores de registro, no transacciones válidas

### 1.2 Integración de Tablas
- Agregamos al dataset ventas las regiones de acuerdo al ID de cliente
- Agregamos las categorías de acuerdo al ID de producto
- Agregamos precio unitario desde la tabla de productos
- Agregamos método de pago desde la tabla de métodos de pago
- **Justificación:** Consolidar toda la información relevante en un solo DataFrame para facilitar el análisis

### 1.3 Estandarización de Formatos
- Renombramos columnas para eliminar acentos (`Categoría` → `Categoria`, `Región` → `Region`, `Método` → `Metodo_Pago`)
- Convertimos `Precio_Unitario` de formato europeo (coma decimal) a formato estándar (punto decimal)
- Convertimos columna `Fecha` a formato datetime con `dayfirst=True`
- **Justificación:** Evitar problemas de encoding y facilitar manipulación programática

### 1.4 Tratamiento de Período Temporal
- Eliminamos enero por empezar en el día 31 (no representativo del mes)
- **Decisión:** `df = df[df['Fecha'].dt.month != 1]`
- **Justificación:** Un solo día de enero sesgaría cualquier análisis mensual

### 1.5 Tratamiento de Outliers
- Identificamos outliers en `Monto_Venta` usando el método IQR (Rango Intercuartílico)
- Fórmula: Outlier si `x < Q1 - 1.5*IQR` o `x > Q3 + 1.5*IQR`
- Los outliers detectados tenían montos idénticos y no correspondían a fechas especiales
- **Decisión:** Eliminamos los outliers por categoría
- **Justificación:** En retail es importante predecir los outliers para prepararse en cuanto a fuerza de ventas e inventarios. Sin embargo, un análisis de ls outliers reveló que parecen ser aleatorios (no tienen una periodicidad clara ni corresponden a fechas importantes de Argentina o globales). Por esto, se decidió descartarlos.

### 1.6 Creación de Tickets
- Creamos `ID_Ticket` agrupando por `ID_Cliente` y `Fecha`
- Identificamos solo 44 de 3000 tickets con múltiples productos
- **Nota:** Esta baja proporción de tickets multi-producto debe validarse con el equipo de datos

---

## 2. Feature Engineering

### 2.1 Columna de Monto de Venta
- Agregamos columna `Monto_Venta = Cantidad * Precio_Unitario`
- **Justificación:** Variable clave para análisis financiero

### 2.2 Variables Temporales
- `semana`: Semana del año (ISO calendar)
- `mes`: Mes del año
- `dia_semana`: Día de la semana (0=Lunes, 6=Domingo)
- **Justificación:** Capturar patrones estacionales y cíclicos

### 2.3 Variables de Lag
- `ventas_categoria_lag_1`: Ventas de la categoría en el período anterior
- `ventas_region_lag_1`: Ventas de la región en el período anterior
- `cantidad_lag_1`: Cantidad vendida (categoría × región) en período anterior
- **Justificación:** Capturar autocorrelación temporal para modelos predictivos

### 2.4 Medias Móviles (Rolling Features)
- Ventanas de 3, 7, 14 y 30 días para categoría y región
- Ventanas semanales de 2, 3, 4, 5 y 6 semanas
- Incluye medias móviles (`rolling_mean`) y volatilidad (`rolling_std`)
- **Decisión:** Usamos `shift(1)` antes del rolling para evitar data leakage
- **Justificación:** Suavizar ruido y capturar tendencias de diferentes horizontes

### 2.5 Variables de Interacción
- Ratios cantidad/media móvil (normalización relativa)
- Ratios entre diferentes ventanas (ej: MA7/MA14 para detectar cambios de tendencia)
- Combinaciones media + volatilidad y media × volatilidad
- **Justificación:** Capturar relaciones no lineales entre variables

### 2.6 Codificación Categórica
- `ID_Region`: Codificación numérica de regiones (category codes)
- **Justificación:** LightGBM requiere variables numéricas

### 2.7 Tratamiento de NaNs en Features
- **Decisión:** No rellenamos los NaNs generados por medias móviles y lags
- **Justificación:** LightGBM maneja valores faltantes nativamente; rellenar podría introducir sesgo

---

## 3. Análisis Exploratorio (EDA)

### 3.1 Granularidad Temporal
- **Decisión:** Realizar análisis a nivel semanal en lugar de diario
- **Justificación:** 
  - Es impráctico optimizar inventarios y fuerza de ventas a nivel diario
  - Reduce ruido en los datos
  - Fácil de ajustar a n semanas o meses si el negocio lo requiere


---

## 4. Clustering

### 4.1 Preparación de Datos
- Estandarización con `StandardScaler`
- Forward/backward fill para NaNs antes de clustering
- **Justificación:** K-Means requiere datos completos y escalados

### 4.2 Variables para Clustering
- Cantidad, medias móviles (3 y 7 días), volatilidad (3 y 7 días)
- ID_Region, ID_Categoria
- **Justificación:** Capturar tanto nivel como comportamiento temporal

### 4.3 Selección de Número de Clusters
- Método del codo (inercia) + Silhouette Score
- **Decisión:** 6 clusters
- **Justificación:** Silhouette Score óptimo y punto de inflexión claro en gráfico de codo

### 4.4 Visualización
- PCA con 4 componentes para reducción de dimensionalidad
- Visualización 2D y 3D
- **Justificación:** Validar separación visual de clusters

---

## 5. Modelado Predictivo

### 5.1 Estrategia Híbrida
- **LightGBM:** Para regiones con suficiente volumen (Buenos Aires, Centro, Cuyo, Patagonia)
- **Media Móvil:** Para regiones con menor volumen (NEA, NOA)
- **Justificación:** 
Basado en pruebas empíricas. Probablemente esto es debido a que LightGBM requiere suficientes datos para generalizar; MA es más robusto con pocos datos.

### 5.2 Variable Objetivo
- `Cantidad_Semanal`: Cantidad vendida agregada por semana, región y categoría
- **Justificación:** Granularidad práctica para planificación de inventarios

### 5.3 Validación Temporal
- TimeSeriesSplit con 5 folds
- **Decisión:** No usar validación cruzada estándar
- **Justificación:** Respetar orden temporal y evitar fuga de información del futuro

### 5.4 Optimización de Hiperparámetros (LightGBM)
- Framework: Optuna con 50 trials
- Sampler: TPE (Tree-structured Parzen Estimator)
- Pruner: MedianPruner (elimina trials poco prometedores)
- Early stopping: 50 rounds sin mejora
- **Decisión:** Guardar mejores parámetros en JSON para reproducibilidad
- **Justificación:** Optimización eficiente sin búsqueda exhaustiva

### 5.5 Optimización de Media Móvil
- Evaluamos ventanas de 1 a 16 semanas
- Seleccionamos n que minimiza RMSE en validación temporal
- **Justificación:** Encontrar balance entre suavizado y reactividad

### 5.6 Semillas Aleatorias
- `seed=42` en todos los componentes (Optuna, LightGBM, KMeans)
- **Justificación:** Reproducibilidad de resultados

---

## 6. Decisiones de Alcance

### 6.1 Limitaciones Aceptadas
- No realizamos optimización de fuerza de ventas ni inventarios
- **Justificación:** Faltan datos necesarios (volumen de productos, costos de almacenamiento, costos de transporte, capacidad logística)

### 6.2 Análisis No Realizados
- Elasticidad de precios (precios fijos en el dataset)
- Estacionalidad interanual (solo un año de datos)
- Correlación con eventos externos

### 6.3 Trabajo Futuro Identificado
- Obtener datos de costos para optimización de inventarios
- Recolectar datos de múltiples años para validar estacionalidad
- Integrar datos externos (clima, eventos, competencia)