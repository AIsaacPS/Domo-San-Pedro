# Determinación de Zonas Favorables de Perforación Geotérmica — Domo San Pedro

## 1. Objetivo del Proyecto

Identificar y delimitar las zonas con mayor favorabilidad para la perforación de pozos geotérmicos exploratorios en el área del **Domo San Pedro**, mediante la integración de datos geocientíficos en un Sistema de Información Geográfica (SIG) utilizando el método **Index Overlay con mapas multi-clase**.

El enfoque se basa en la metodología propuesta por Prol-Ledesma (2000), adaptada al contexto geológico y geotérmico del Domo San Pedro. Se busca generar un mapa de favorabilidad (escala 0–1) que permita tomar decisiones informadas sobre la ubicación óptima de pozos exploratorios, minimizando el riesgo de perforación fallida.

---

## 2. Método: Index Overlay Multi-Clase

### 2.1 Fundamento

El modelo Index Overlay es un método *knowledge-driven* (guiado por conocimiento experto) que integra múltiples capas de evidencia geocientífica. Cada capa temática recibe:

- Un **peso** (*weight*, $w_i$) que refleja su importancia relativa para identificar el reservorio geotérmico.
- Un **puntaje** (*score*, $S_{ij}$) asignado a cada clase dentro de la capa, según la proximidad o magnitud de la evidencia.

A diferencia del modelo Booleano (binario: favorable/no favorable), el Index Overlay permite **clases intermedias**, lo que reduce los errores de omisión y amplía la capacidad predictiva sin incluir falsos positivos.

### 2.2 Fórmula Principal

El puntaje ponderado para cada píxel del mapa se calcula como:

$$
S = \frac{\sum_{i=1}^{n} S_{ij} \cdot w_i}{\sum_{i=1}^{n} w_i}
$$

Donde:

| Símbolo | Descripción |
|---------|-------------|
| $S$ | Puntaje de favorabilidad del píxel (valor entre 0 y 1) |
| $n$ | Número total de capas temáticas |
| $S_{ij}$ | Puntaje de la clase $j$ en la capa temática $i$ (0, 8, o 10) |
| $w_i$ | Peso asignado a la capa temática $i$ |

### 2.3 Sistema de Clasificación (Tres Clases)

Cada capa temática se reclasifica en tres categorías:

| Clase | Condición (distancias) | Condición (resistividad) | Score |
|-------|------------------------|--------------------------|-------|
| Alta favorabilidad | Distancia ≤ 100 m al rasgo | ≤ 10 Ω·m | 10 |
| Favorabilidad moderada | 100 m < Distancia ≤ 200 m | 10–20 Ω·m | 8 |
| No favorable | Distancia > 200 m | > 20 Ω·m | 0 |

### 2.4 Red de Inferencia

La lógica conceptual del modelo sigue la siguiente estructura:

```
FAVORABILIDAD = Resistividad ∩ ((Fallas ∪ Fracturamiento) ∪ (Fuente_Calor ∪ Manifestaciones))
```

En el contexto del Index Overlay, esta red se traduce en la asignación diferencial de pesos:

- Las capas que representan **condiciones en profundidad** (resistividad, fallas principales) reciben pesos mayores.
- Las capas que representan **evidencia superficial** (manifestaciones, geología, fracturamiento) reciben pesos menores pero significativos.

### 2.5 Umbral de Decisión

- **Favorabilidad > 0.7**: Zonas de máxima prioridad para perforación exploratoria.
- **Favorabilidad 0.6–0.7**: Zonas moderadamente favorables; candidatas a exploración detallada adicional.
- **Favorabilidad < 0.6**: Zonas no prioritarias.

El umbral de **0.6** ha demostrado capturar la mayoría de los pozos productores en campos análogos sin incluir pozos fallidos (Prol-Ledesma, 2000).

---

## 3. Flujo de Trabajo (Pipeline)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PIPELINE DE TRABAJO                          │
└─────────────────────────────────────────────────────────────────────┘

  FASE 1: RECOPILACIÓN DE DATOS
  ├── Recopilar mapas geológicos, geofísicos y de manifestaciones
  ├── CRS del proyecto: EPSG:32613 (WGS 84 / UTM Zona 13N)
  └── Inventario de datos disponibles vs. datos faltantes

         │
         ▼

  FASE 2: PREPARACIÓN DE DATOS (PRE-PROCESAMIENTO)
  ├── Digitalización de rasgos lineales y poligonales (formato vectorial)
  ├── Reproyección de todos los datos a EPSG:32613 (UTM 13N)
  ├── Conversión vector → raster (resolución de celda: 30 m)
  ├── Cálculo de mapas de distancia euclidiana a cada rasgo
  ├── Interpolación del mapa de resistividad (si viene en contornos)
  └── Verificación de extensión espacial común (bounding box)

         │
         ▼

  FASE 3: RECLASIFICACIÓN
  ├── Asignar scores (0, 8, 10) a cada capa según umbrales de distancia
  ├── Reclasificar mapa de resistividad según umbrales (≤10, 10-20, >20 Ω·m)
  └── Verificar que todas las capas tengan la misma extensión y resolución

         │
         ▼

  FASE 4: ASIGNACIÓN DE PESOS
  ├── Definir pesos por criterio experto basado en modelo conceptual
  ├── Considerar la importancia relativa de cada evidencia
  └── Documentar justificación de cada peso asignado

         │
         ▼

  FASE 5: CÁLCULO DEL INDEX OVERLAY
  ├── Aplicar la fórmula: S = Σ(Sij × wi) / Σ(wi)
  ├── Generar mapa de favorabilidad continuo (0–1)
  └── Exportar raster de favorabilidad

         │
         ▼

  FASE 6: INTERPRETACIÓN Y VISUALIZACIÓN
  ├── Aplicar umbrales (>0.6, >0.7) para delimitar zonas favorables
  ├── Superponer pozos existentes, estructuras y manifestaciones
  ├── Análisis de sensibilidad (variación de pesos y umbrales)
  └── Generación de mapas finales de favorabilidad

         │
         ▼

  FASE 7: VALIDACIÓN Y REPORTE
  ├── Comparar con datos conocidos (pozos, gradientes, geoquímica)
  ├── Cuantificar errores de omisión y comisión (si hay datos)
  └── Documento final con recomendaciones de perforación
```

---

## 4. Datos de Entrada Requeridos (Input)

Para aplicar el modelo Index Overlay al Domo San Pedro se requieren las siguientes capas de información:

### 4.1 Geología Estructural (Fallas Principales)

| Aspecto | Descripción |
|---------|-------------|
| **Qué se necesita** | Mapa de fallas activas y/o recientes del área del Domo San Pedro |
| **Formato** | Líneas vectoriales (shapefile, GeoJSON, o similar) |
| **Detalle requerido** | Ubicación, orientación (rumbo/echado), longitud, y si es posible: edad relativa y evidencia de actividad reciente |
| **Fuentes posibles** | Cartografía geológica del SGM, estudios estructurales locales, interpretación de imágenes satelitales, publicaciones académicas |
| **Justificación** | En sistemas con permeabilidad secundaria, las fallas controlan el flujo de fluidos geotérmicos hacia la superficie |

### 4.2 Manifestaciones Termales Superficiales

| Aspecto | Descripción |
|---------|-------------|
| **Qué se necesita** | Inventario georreferenciado de todas las manifestaciones termales: manantiales calientes, fumarolas, suelo vaporante, zonas de alteración, pozas de lodo |
| **Formato** | Puntos o polígonos vectoriales con coordenadas GPS |
| **Detalle requerido** | Tipo de manifestación, temperatura (si disponible), pH, extensión aproximada |
| **Fuentes posibles** | Trabajo de campo, reportes del SGM o CFE, publicaciones, imágenes satelitales térmicas (ASTER/Landsat banda térmica) |
| **Justificación** | Las manifestaciones marcan los flujos ascendentes del sistema hidrotermal y son indicadores directos de actividad en profundidad |

### 4.3 Geología Superficial (Contactos con Domos/Intrusivos Recientes)

| Aspecto | Descripción |
|---------|-------------|
| **Qué se necesita** | Mapa geológico detallado del área, con énfasis en la identificación de cuerpos volcánicos recientes (domos, flujos, intrusivos someros) que puedan representar la fuente de calor |
| **Formato** | Polígonos vectoriales de unidades litológicas |
| **Detalle requerido** | Contactos litológicos, edad de las unidades, composición (riolita, dacita, andesita), relación con el domo principal |
| **Fuentes posibles** | Cartas geológicas del SGM (1:50,000), tesis universitarias, publicaciones sobre la geología del Domo San Pedro |
| **Justificación** | Los cuerpos intrusivos/volcánicos recientes son el motor térmico del sistema geotérmico; la proximidad al contacto indica mayor probabilidad de gradiente geotérmico elevado |

### 4.4 Densidad de Fracturamiento Superficial

| Aspecto | Descripción |
|---------|-------------|
| **Qué se necesita** | Mapa de densidad de fracturamiento o lineamientos estructurales del área |
| **Formato** | Polígonos de zonas de alta densidad de fracturamiento, o mapa raster de densidad de lineamientos |
| **Detalle requerido** | Densidad de fracturas (fracturas/km²), orientación preferencial, relación con sistemas de fallas principales |
| **Fuentes posibles** | Interpretación de fotografías aéreas, imágenes satelitales de alta resolución (Google Earth, Sentinel-2), estudios de campo, análisis de lineamientos con software (PCI Geomatica, ArcGIS) |
| **Justificación** | El fracturamiento superficial puede ser indicativo de esfuerzos activos en profundidad relacionados con actividad hidrotermal, incrementando la permeabilidad del reservorio |

### 4.5 Resistividad Eléctrica (Geofísica)

| Aspecto | Descripción |
|---------|-------------|
| **Qué se necesita** | Mapa de resistividad aparente del subsuelo, preferentemente a profundidades relevantes del reservorio (500–2000 m) |
| **Formato** | Contornos de isoresistividad o raster interpolado |
| **Método preferido** | Sondeos eléctricos verticales (SEV Schlumberger), Magnetotelúrica (MT), o Transitorio electromagnético (TEM/TDEM) |
| **Detalle requerido** | Resistividad aparente en Ω·m a la profundidad objetivo, cobertura espacial del área de estudio |
| **Fuentes posibles** | Campañas geofísicas propias, datos de CFE, universidades, reportes de consultoría |
| **Justificación** | La baja resistividad (< 10–20 Ω·m) indica presencia de fluidos salinos calientes y/o minerales de alteración (arcillas), siendo el mejor indicador geofísico de zonas productivas en campos geotérmicos |

### 4.6 Datos Complementarios (Opcionales pero Recomendados)

| Dato | Utilidad |
|------|----------|
| Modelo Digital de Elevación (DEM) | Contexto topográfico, análisis de pendientes, delimitación de cuencas |
| Imágenes satelitales (Landsat/ASTER) | Detección de anomalías térmicas, mapeo de alteración hidrotermal |
| Gradiente geotérmico (si existe) | Discriminar zonas de actividad actual vs. relicta |
| Geoquímica de manifestaciones | Geotermometría para estimar temperatura del reservorio |
| Gravimetría/Magnetometría | Identificación de intrusivos y estructuras profundas (uso regional) |

---

## 5. Sistema de Referencia Espacial

| Parámetro | Valor |
|-----------|-------|
| **CRS del proyecto** | **EPSG:32613 — WGS 84 / UTM Zona 13N** |
| Datum | WGS 84 |
| Proyección | Transversa de Mercator |
| Zona UTM | 13 Norte |
| Meridiano central | 105° W |
| Unidades | Metros |
| Resolución raster | 30 m × 30 m |

### 5.1 Justificación

- El Domo San Pedro se ubica a ≈21.19°N, 104.72°W (San Pedro Lagunillas, Nayarit), a solo ~0.28° del meridiano central de la Zona 13N. Esto garantiza distorsión mínima.
- El modelo Index Overlay requiere cálculos de **distancia euclidiana** (buffers de 100 m y 200 m). Un sistema proyectado en metros es indispensable para que estas operaciones sean correctas.
- En coordenadas geográficas (EPSG:4326), 1° de longitud ≠ 1° de latitud a esta latitud, lo que introduciría errores sistemáticos en la reclasificación por distancias.

### 5.2 Reglas de Aplicación

1. **Todos** los datos de entrada (vector y raster) deben estar en EPSG:32613 antes de ingresar al modelo.
2. Si un dato fuente viene en coordenadas geográficas (EPSG:4326), debe reproyectarse:
   - Vector: Exportar → Guardar como → CRS: EPSG:32613
   - Raster: Raster → Proyecciones → Combar (Reproyectar) → CRS destino: EPSG:32613
3. El proyecto de QGIS debe configurarse con CRS = EPSG:32613 (Proyecto → Propiedades → SRC).
4. No se aceptan capas en otro CRS para el análisis final; la reproyección al vuelo (*on-the-fly*) de QGIS es solo para visualización, no para geoprocesamiento.

---

## 6. Software y Herramientas

| Herramienta | Uso |
|-------------|-----|
| **QGIS** | Digitalización, análisis espacial, cálculo de distancias, overlay, visualización |
| Python (Rasterio, NumPy, GeoPandas) | Automatización del pipeline, cálculo del Index Overlay |
| Google Earth Engine | Obtención de imágenes satelitales y DEM |
| GMT / Surfer | Visualización de mapas de contorno (opcional) |

---

## 7. Estructura del Proyecto

```
DOMO SAN PEDRO/
├── README.md                          ← Este archivo
├── data/
│   ├── raw/                           ← Datos crudos (shapefiles, geotiff, CSV)
│   │   ├── geologia/
│   │   ├── fallas/
│   │   ├── manifestaciones/
│   │   ├── fracturamiento/
│   │   └── resistividad/
│   └── processed/                     ← Datos reclasificados y en formato raster
│       ├── distancia_fallas.tif
│       ├── distancia_manifestaciones.tif
│       ├── distancia_domos.tif
│       ├── distancia_fracturamiento.tif
│       └── resistividad_interpolada.tif
├── scripts/
│   ├── 01_preprocesamiento.py
│   ├── 02_calculo_distancias.py
│   ├── 03_reclasificacion.py
│   ├── 04_index_overlay.py
│   └── 05_visualizacion.py
├── outputs/
│   ├── mapa_favorabilidad.tif
│   ├── mapa_favorabilidad_umbrales.png
│   └── reporte_final.pdf
├── docs/
│   └── referencias/
└── pdf-forge-exports/                 ← Artículos de referencia (texto extraído)
```

---

## 8. Referencias Principales

- Prol-Ledesma, R.M. (2000). Evaluation of the reconnaissance results in geothermal exploration using GIS. *Geothermics*, 29, 83–103.
- Bonham-Carter, G.F. (1994). *Geographical Information Systems for Geoscientists: Modelling with GIS*. Pergamon, 398 pp.
- Saaty, T.L. (1977). A scaling method for priorities in hierarchical structures. *J. Math. Psychology*, 15, 234–281.

---

## 9. Autor / Contacto

Proyecto desarrollado para la evaluación del potencial geotérmico del Domo San Pedro.

---

*Última actualización: Julio 2026*
