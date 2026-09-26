# Determinación de Nuevas Zonas Favorables para la Expansión del Campo Geotérmico Domo San Pedro, Nayarit

> Repositorio técnico de la tesina de posgrado (Especialidad en Exploración y Aprovechamiento de Recursos Geotérmicos, UNAM).

## 1. Objetivo del Proyecto

Identificar y delimitar **nuevas zonas favorables para la expansión** del Campo Geotérmico **Domo San Pedro** —actualmente en producción (35.5 MW instalados de un potencial estimado de hasta ~200 MW)— mediante la integración de evidencia geocientífica en un Sistema de Información Geográfica (SIG) con el método **Index Overlay multi-clase**.

El enfoque se basa en la metodología de Prol-Ledesma (2000), adaptada al contexto geológico y geotérmico del Domo San Pedro. Se busca generar un mapa de favorabilidad (escala 0–1) que permita priorizar la ubicación de nuevos pozos dentro o de forma contigua a la concesión, aprovechando la infraestructura existente y minimizando el riesgo de perforación fallida. Al tratarse de un campo activo (no un prospecto virgen), el análisis se enfoca en la **expansión** apoyada en el conocimiento de subsuelo ya disponible (pozos, MT 3D, geoquímica).

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


| Símbolo | Descripción                                                 |
| -------- | ------------------------------------------------------------ |
| $S$      | Puntaje de favorabilidad del píxel (valor entre 0 y 1)      |
| $n$      | Número total de capas temáticas                            |
| $S_{ij}$ | Puntaje de la clase$j$ en la capa temática $i$ (0, 8, o 10) |
| $w_i$    | Peso asignado a la capa temática$i$                         |

### 2.3 Sistema de Clasificación (Tres Clases)

Cada capa temática se reclasifica en tres categorías:


| Clase                  | Condición (distancias)     | Condición (resistividad) | Score |
| ---------------------- | --------------------------- | ------------------------- | ----- |
| Alta favorabilidad     | Distancia ≤ 100 m al rasgo | 20–50 Ω·m (yacimiento)  | 10    |
| Favorabilidad moderada | 100 m < Distancia ≤ 200 m  | 15–20 y 50–55 Ω·m (halo de transición) | 8     |
| No favorable           | Distancia > 200 m           | < 15 Ω·m (sello) o > 55 Ω·m (roca fría) | 0     |

> **Nota sobre la resistividad (aclaración Dra. Prol-Ledesma, reunión 2026-08-29):** a diferencia de las capas de distancia, la resistividad **no** es monótona ("más baja = mejor"). Los valores bajos (**capa sello de arcillas / *clay cap***) no corresponden al reservorio. El yacimiento geotérmico se caracteriza por una **ventana** de resistividad intermedia de **20–50 Ω·m**; valores altos indican roca resistiva fría o basamento. La clase moderada (Score 8) es un **halo de transición simétrico** alrededor de la ventana (**15–20 y 50–55 Ω·m**), no el rango bajo 10–20 Ω·m, que corresponde al techo del sello arcilloso. Por eso la alta favorabilidad es un rango cerrado, no un umbral inferior.

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
  ├── Reclasificar resistividad como VENTANA del reservorio (ver §2.3):
  │     20–50 Ω·m → 10 | 15–20 y 50–55 Ω·m → 8 | <15 o >55 Ω·m → 0
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

## 4. Control de Calidad: Georreferenciación de Imágenes

Cuando se georreferencian mapas escaneados o extraídos de artículos (PDF → PNG), es necesario evaluar la precisión del ajuste mediante los **residuales** reportados por el georreferenciador de QGIS.

### 4.1 Concepto de Residual

El residual de un punto de control (GCP) indica la distancia, en **píxeles**, entre la posición asignada por el usuario y la posición calculada por el modelo de transformación. Un residual alto indica que ese punto no es consistente con los demás.

### 4.2 Conversión de Píxeles a Metros

Para interpretar los residuales en unidades de terreno:

$$
\text{Error en terreno (m)} = \text{Residual (px)} \times \text{Tamaño de píxel (m/px)}
$$

El tamaño de píxel se calcula como:

$$
\text{Tamaño de píxel} = \frac{\text{Extensión del mapa en metros}}{\text{Ancho de la imagen en píxeles}}
$$

**Ejemplo para este proyecto** (mapa Ferrari, ~20 km de extensión, imagen de 6600 px):

- Tamaño de píxel ≈ 20,000 m / 6600 px ≈ **3 m/px**

### 4.3 Umbrales Aceptables para este Proyecto

El criterio se establece en función de:

- **Resolución del análisis**: 30 m (tamaño de celda del raster final)
- **Buffer mínimo de decisión**: 100 m (umbral de alta favorabilidad)


| Métrica                          | Umbral máximo | Justificación                                    |
| --------------------------------- | -------------- | ------------------------------------------------- |
| **RMS total (Mean Error)**        | ≤ 3 píxeles  | Error < 10 m, menor que 1/3 de la celda           |
| **Residual por punto individual** | ≤ 5 píxeles  | Error < 15 m, menor que 15% del buffer de 100 m   |
| **Punto inaceptable**             | > 10 píxeles  | Error > 30 m, supera la resolución del análisis |

### 4.4 Tabla de Evaluación (referencia rápida, a 3 m/px)


| Residual (px) | Error en terreno | Evaluación                       |
| ------------- | ---------------- | --------------------------------- |
| < 3           | < 9 m            | Excelente                         |
| 3–5          | 9–15 m          | Aceptable                         |
| 5–10         | 15–30 m         | Marginal (revisar punto)          |
| > 10          | > 30 m           | Inaceptable (eliminar o reubicar) |

### 4.5 Recomendaciones Prácticas

1. Usar al menos **6–8 puntos de control** bien distribuidos por toda la imagen.
2. Preferir intersecciones de coordenadas, vértices de cuerpos geológicos identificables, o esquinas de cuadrantes cartográficos como GCPs.
3. Si un punto tiene residual > 10 px, verificar que fue correctamente identificado antes de eliminarlo.
4. Si el mapa tiene distorsión por la proyección original del artículo, usar **transformación polinomial de 2° orden** o **Thin Plate Spline** en lugar de transformación lineal.
5. El error posicional inherente a mapas publicados a escala 1:100,000 es de ~50 m (0.5 mm a escala del mapa). No tiene sentido exigir precisión sub-pixel si la fuente original tiene esa incertidumbre.

### 4.6 Resultado Obtenido

- **Mapa geológico Ferrari (georreferenciado)**: RMS total = **38 píxeles** → Evaluado contra los criterios anteriores, a confirmar con el tamaño de píxel real de la imagen utilizada.

---

## 5. Datos de Entrada Requeridos (Input)

Para aplicar el modelo Index Overlay al Domo San Pedro se requieren las siguientes capas de información:

### 5.1 Geología Estructural (Fallas Principales)


| Aspecto               | Descripción                                                                                                                         |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Qué se necesita**  | Mapa de fallas activas y/o recientes del área del Domo San Pedro                                                                    |
| **Formato**           | Líneas vectoriales (shapefile, GeoJSON, o similar)                                                                                  |
| **Detalle requerido** | Ubicación, orientación (rumbo/echado), longitud, y si es posible: edad relativa y evidencia de actividad reciente                  |
| **Fuentes posibles**  | Cartografía geológica del SGM, estudios estructurales locales, interpretación de imágenes satelitales, publicaciones académicas (Ferrari 2003, Corbo 2026, Muñoz 2024) |
| **Justificación**    | En sistemas con permeabilidad secundaria, las fallas controlan el flujo de fluidos geotérmicos hacia la superficie                  |

> **Tratamiento aplicado:** las trazas provienen de tres fuentes (Ferrari 2003, Corbo 2026, Muñoz 2024). Se **excluye del análisis el borde de caldera inferido** (catalogado como tal en la tabla de atributos), por no constituir una falla con permeabilidad demostrada. La zona de daño se representa con un buffer de **alta favorabilidad ≤ 100 m** y transición **100–200 m** (ver `scripts/05_visualizacion.py`).

### 5.2 Manifestaciones Termales Superficiales


| Aspecto               | Descripción                                                                                                                                              |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Qué se necesita**  | Inventario georreferenciado de todas las manifestaciones termales: manantiales calientes, fumarolas, suelo vaporante, zonas de alteración, pozas de lodo |
| **Formato**           | Puntos o polígonos vectoriales con coordenadas GPS                                                                                                       |
| **Detalle requerido** | Tipo de manifestación, temperatura (si disponible), pH, extensión aproximada                                                                            |
| **Fuentes posibles**  | Trabajo de campo, reportes del SGM o CFE, publicaciones, imágenes satelitales térmicas (ASTER/Landsat banda térmica)                                   |
| **Justificación**    | Las manifestaciones marcan los flujos ascendentes del sistema hidrotermal y son indicadores directos de actividad en profundidad                          |

### 5.3 Geología Superficial (Contactos con Domos/Intrusivos Recientes)


| Aspecto               | Descripción                                                                                                                                                                           |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Qué se necesita**  | Mapa geológico detallado del área, con énfasis en la identificación de cuerpos volcánicos recientes (domos, flujos, intrusivos someros) que puedan representar la fuente de calor |
| **Formato**           | Polígonos vectoriales de unidades litológicas                                                                                                                                        |
| **Detalle requerido** | Contactos litológicos, edad de las unidades, composición (riolita, dacita, andesita), relación con el domo principal                                                                |
| **Fuentes posibles**  | Cartas geológicas del SGM (1:50,000), tesis universitarias, publicaciones sobre la geología del Domo San Pedro                                                                       |
| **Justificación**    | Los cuerpos intrusivos/volcánicos recientes son el motor térmico del sistema geotérmico; la proximidad al contacto indica mayor probabilidad de gradiente geotérmico elevado       |

### 5.4 Densidad de Fracturamiento Superficial


| Aspecto               | Descripción                                                                                                                                                                                     |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Qué se necesita**  | Mapa de densidad de fracturamiento o lineamientos estructurales del área                                                                                                                        |
| **Formato**           | Polígonos de zonas de alta densidad de fracturamiento, o mapa raster de densidad de lineamientos                                                                                                |
| **Detalle requerido** | Densidad de fracturas (fracturas/km²), orientación preferencial, relación con sistemas de fallas principales                                                                                  |
| **Fuentes posibles**  | Interpretación de fotografías aéreas, imágenes satelitales de alta resolución (Google Earth, Sentinel-2), estudios de campo, análisis de lineamientos con software (PCI Geomatica, ArcGIS) |
| **Justificación**    | El fracturamiento superficial puede ser indicativo de esfuerzos activos en profundidad relacionados con actividad hidrotermal, incrementando la permeabilidad del reservorio                     |

### 5.5 Resistividad Eléctrica (Geofísica)


| Aspecto               | Descripción                                                                                                                                                                                                  |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Qué se necesita**  | Mapa de resistividad del subsuelo al intervalo objetivo del reservorio (**1,000–2,000 m de profundidad**, según Prol-Ledesma 2026-08-29). El corte inicial a 350 mbsl se considera somero y debe re-extraerse a este intervalo.                                                                                           |
| **Formato**           | Contornos de isoresistividad o raster interpolado                                                                                                                                                             |
| **Método preferido** | Sondeos eléctricos verticales (SEV Schlumberger), Magnetotelúrica (MT), o Transitorio electromagnético (TEM/TDEM)                                                                                          |
| **Detalle requerido** | Resistividad aparente en Ω·m a la profundidad objetivo, cobertura espacial del área de estudio                                                                                                             |
| **Fuentes posibles**  | Campañas geofísicas propias, datos de CFE, universidades, reportes de consultoría                                                                                                                          |
| **Justificación**    | La respuesta de resistividad en un sistema geotérmico es zonada: la resistividad **muy baja (< 10 Ω·m)** corresponde a la **capa sello de arcillas** (esmectita) que cubre el reservorio, **no** al reservorio productivo. El **yacimiento** se asocia a una **ventana intermedia de 20–50 Ω·m** (transición esmectita→illita/clorita, fluidos calientes en roca fracturada), mientras que valores **> 50 Ω·m** indican roca fría o basamento resistivo. Por eso el mejor indicador no es "la resistividad más baja" sino el rango intermedio correcto (Prol-Ledesma, 2026-08-29). |

### 5.6 Datos Complementarios (Opcionales pero Recomendados)


| Dato                                  | Utilidad                                                                 |
| ------------------------------------- | ------------------------------------------------------------------------ |
| Modelo Digital de Elevación (DEM)    | Contexto topográfico, análisis de pendientes, delimitación de cuencas |
| Imágenes satelitales (Landsat/ASTER) | Detección de anomalías térmicas, mapeo de alteración hidrotermal     |
| Gradiente geotérmico (si existe)     | Discriminar zonas de actividad actual vs. relicta                        |
| Geoquímica de manifestaciones        | Geotermometría para estimar temperatura del reservorio                  |
| Gravimetría/Magnetometría           | Identificación de intrusivos y estructuras profundas (uso regional)     |

---

## 6. Sistema de Referencia Espacial


| Parámetro           | Valor                                   |
| -------------------- | --------------------------------------- |
| **CRS del proyecto** | **EPSG:32613 — WGS 84 / UTM Zona 13N** |
| Datum                | WGS 84                                  |
| Proyección          | Transversa de Mercator                  |
| Zona UTM             | 13 Norte                                |
| Meridiano central    | 105° W                                 |
| Unidades             | Metros                                  |
| Resolución raster   | 30 m × 30 m                            |

### 6.0 Área de Estudio y Área Concesionada

El proyecto maneja **dos dominios espaciales distintos** que no deben confundirse:

**Área de estudio** (rectángulo de análisis / marco de cómputo del SIG):

| Parámetro | Valor |
| ---------- | ----- |
| XMIN (Easting) | 520,000 m |
| XMAX (Easting) | 535,000 m |
| YMIN (Northing) | 2,328,000 m |
| YMAX (Northing) | 2,348,000 m |
| Ancho | 15 km |
| Alto | 20 km |
| Área | 300 km² |

**Área concesionada** (frontera legal y dominio prioritario / *clipping mask*):

| Parámetro | Valor |
| ---------- | ----- |
| Titular | Geotérmica para el Desarrollo, S.A.P.I. de C.V. (Grupo Dragón) |
| Otorgamiento | SENER, 30 de octubre de 2015 (vigencia 30 años) |
| Superficie | **129.18 km² (12,918 ha)** — polígono de 7 vértices UTM 13N |
| Rol en el SIG | Máscara de recorte; las nuevas zonas favorables deben caer dentro o ser contiguas |

> Las nuevas zonas favorables se evalúan **dentro o de forma contigua** a la concesión para aprovechar la infraestructura existente (caminos, subestación en Chapalilla a ~10 km, derechos de agua CONAGUA). Detalle de vértices en `BIBLIOGRAFIA/resumen_concesion_domo_san_pedro.txt`.

### 6.1 Justificación

- El Domo San Pedro se ubica a ≈21.19°N, 104.72°W (San Pedro Lagunillas, Nayarit), a solo ~0.28° del meridiano central de la Zona 13N. Esto garantiza distorsión mínima.
- El modelo Index Overlay requiere cálculos de **distancia euclidiana** (buffers de 100 m y 200 m). Un sistema proyectado en metros es indispensable para que estas operaciones sean correctas.
- En coordenadas geográficas (EPSG:4326), 1° de longitud ≠ 1° de latitud a esta latitud, lo que introduciría errores sistemáticos en la reclasificación por distancias.

### 6.2 Reglas de Aplicación

1. **Todos** los datos de entrada (vector y raster) deben estar en EPSG:32613 antes de ingresar al modelo.
2. Si un dato fuente viene en coordenadas geográficas (EPSG:4326), debe reproyectarse:
   - Vector: Exportar → Guardar como → CRS: EPSG:32613
   - Raster: Raster → Proyecciones → Combar (Reproyectar) → CRS destino: EPSG:32613
3. El proyecto de QGIS debe configurarse con CRS = EPSG:32613 (Proyecto → Propiedades → SRC).
4. No se aceptan capas en otro CRS para el análisis final; la reproyección al vuelo (*on-the-fly*) de QGIS es solo para visualización, no para geoprocesamiento.

---

## 7. Software y Herramientas


| Herramienta                         | Uso                                                                                  |
| ----------------------------------- | ------------------------------------------------------------------------------------ |
| **QGIS** (PyQGIS)                   | Digitalización, carga/recorte de capas, análisis espacial, visualización            |
| Python: NumPy, SciPy, Rasterio      | Pipeline fuera de QGIS, rasterización, distancia euclidiana, cálculo del Index Overlay |
| Python: pyshp (`shapefile`)         | Lectura de shapefiles de fallas sin dependencias binarias pesadas                    |
| Python: Matplotlib                  | Generación de los mapas (fallas, resistividad, favorabilidad, booleano)              |
| Python: PyMuPDF, python-docx        | Extracción de texto de bibliografía (PDF) y generación de documentos Word            |
| Google Earth Engine                 | Obtención de imágenes satelitales y DEM                                            |

---

## 8. Estructura del Proyecto

```
DOMO SAN PEDRO/
├── README.md                          ← Este archivo
├── CONTRIBUTING.md                    ← Guía de configuración y contribución
├── .gitignore                         ← Excluye binarios pesados de Git
├── requirements.txt                   ← Dependencias Python
├── PROYECTO - GIS.qgz                 ← Proyecto QGIS principal (NO en Git)
│
├── .kiro/
│   ├── steering/
│   │   └── contexto-tesina.md         ← Contexto común (título, zona, concesión, reglas)
│   └── agents/                        ← Panel de 7 auditores especializados (solo lectura + web)
│       ├── 01-geologia-mexico.json
│       ├── 02-geotermia-mexico.json
│       ├── 03-geoquimica-geotermia.json
│       ├── 04-geofisica-geotermia.json
│       ├── 05-sig-geotermia.json
│       ├── 06-vulcanologia-neotectonica.json
│       └── 07-estructural-jalisco-nayarit.json
│
├── DATA INPUT/                        ← Datos fuente para el modelo, organizados por tema
│   ├── 01_FALLAS_PRINCIPALES/         ← Fallas: Ferrari 2003, Corbo 2026, Muñoz 2024
│   ├── 02_MANIFESTACIONES_TERMALES/
│   ├── 03_GEOLOGIA_FUENTE_CALOR/      ← Litología SGM + Ferrari 2003
│   ├── 04_FRACTURAMIENTO/
│   ├── 05_RESISTIVIDAD/               ← Mapas MT de Corbo 2026
│   ├── 06_DEM_TOPOGRAFIA/            ← CEM INEGI
│   ├── 07_ANOMALIAS_TERMICAS/  08_GEOQUIMICA/
│   └── 09_GRADIENTE_GEOTERMICO/  10_GRAVIMETRIA_MAGNETOMETRIA/
│
├── data/
│   └── processed/                     ← Datos procesados listos para el modelo
│       ├── area_estudio_UTM13N.*      ← Polígono del área de estudio (300 km²)
│       ├── DEM_area_estudio_UTM13N.tif
│       ├── geologia_area_estudio_UTM13N.*
│       └── resistividad_350mbsl_UTM13N.tif  ← Extraída desde mapa MT (corte somero)
│
├── scripts/
│   ├── README.md
│   ├── config.py                          ← Configuración centralizada (rutas, CRS, pesos, umbrales)
│   ├── 01_cargar_datos_y_area_estudio.py  ← PyQGIS: carga y preprocesamiento
│   ├── extraer_resistividad_de_mapa.py    ← color→resistividad (Ω·m) desde mapa MT
│   ├── 05_visualizacion.py                ← Genera los 4 mapas (fallas, resistividad, index overlay, booleano)
│   ├── extraer_texto_bibliografia.py      ← PDF/DOCX → texto plano (auto-descubre BIBLIOGRAFIA/)
│   ├── generar_borrador_metodologia.py    ← Borrador de metodología (Word + Markdown)
│   ├── generar_capitulo2_corregido.py     ← Capítulo II con correcciones del panel (Word + Markdown)
│   ├── generar_bibliografia.py            ← .docx de bibliografía comentada
│   ├── generar_propuesta_sig.py           ← .docx de propuesta de proyecto
│   └── convertir_pdf_a_png.py             ← Utilidad: PDF → PNG para georreferenciar
│
├── outputs/                           ← Resultados generados (NO en Git)
│   ├── fallas_zona_dano_UTM13N.png
│   ├── resistividad_MT_350mbsl_UTM13N.png
│   ├── index_overlay_gradiente_UTM13N.png
│   ├── modelo_booleano_UTM13N.png
│   ├── Borrador_Metodologia_Domo_San_Pedro.docx / .md
│   └── Capitulo2_Descripcion_Zona_Estudio_CORREGIDO.docx / .md
│
├── BIBLIOGRAFIA/                      ← PDFs por tema + capítulos de tesina + resumen de concesión
│   ├── 01_GEOLOGIA_VULCANOLOGIA_TECTONICA/
│   ├── 02_GEOQUIMICA/
│   ├── 03_GEOFISICA/
│   ├── 04_HIDROGEOLOGIA/
│   ├── 05_SIG_GEOTERMIA/
│   ├── 06_GEOTERMIA/
│   ├── capitulo_2_descripcion_zona_estudio-v4.*
│   └── resumen_concesion_domo_san_pedro.txt
│
└── docs/
    ├── extracted-text/                ← Texto extraído de toda la bibliografía (en Git)
    └── revisiones/                    ← Informes del panel de auditores
```

> **Nota sobre Git**: Los archivos binarios (`.tif`, `.shp`, `.pdf`, `.png`) están excluidos
> por `.gitignore`. Solo se versiona el código, documentación y archivos de texto plano.

---

## 9. Estado Actual del Proyecto (Septiembre 2026)

### Completado ✓

| Fase | Tarea | Script/Archivo |
|------|-------|----------------|
| 1 | Área de estudio definida (15×20 km, 300 km², UTM 13N) | `01_cargar_datos_y_area_estudio.py` |
| 1 | DEM reproyectado y recortado (30 m) | `01_cargar_datos_y_area_estudio.py` |
| 1 | Geología (SGM) recortada | `01_cargar_datos_y_area_estudio.py` |
| 2 | Resistividad extraída de modelo MT (350 mbsl, corte somero) | `extraer_resistividad_de_mapa.py` |
| 2 | Criterio de resistividad corregido a ventana 20–50 Ω·m | `config.py` (reunión Prol-Ledesma) |
| 3 | Fallas rasterizadas + zona de daño (buffer 100 m); exclusión del borde de caldera | `05_visualizacion.py` |
| 5–6 | Index Overlay continuo (fuzzy) + 4 mapas (fallas, resistividad, gradiente, booleano) | `05_visualizacion.py` |
| — | Bibliografía extraída a texto (22 fuentes, 6 temas) | `extraer_texto_bibliografia.py` |
| — | Borrador de metodología (Word + Markdown) | `generar_borrador_metodologia.py` |
| — | Capítulo II corregido por panel de auditores (Word + Markdown) | `generar_capitulo2_corregido.py` |
| — | Panel de 7 auditores especializados (revisión + investigación web) | `.kiro/agents/` |

### Pendiente

| Fase | Tarea | Prioridad |
|------|-------|-----------|
| 2 | Re-extraer resistividad al corte del reservorio (1,000–2,000 m) | Alta |
| 1 | Digitalizar manifestaciones termales | Alta |
| 1 | Obtener/digitalizar fracturamiento | Media |
| 4 | Definir pesos finales (con Dra. Prol-Ledesma) | Alta |
| — | Aplicar puntos `[VERIFICAR]` del Capítulo II corregido | Alta |
| 5 | Integrar todas las capas al Index Overlay (hoy: fallas + resistividad) | Alta |
| 7 | Validar contra pozos existentes | Media |

---

## 9.1 Sistema de Revisión por Auditores (agentes de Kiro)

El proyecto incluye un **panel de 7 auditores especializados** (en `.kiro/agents/`) que revisan la redacción de la tesina contra la bibliografía real y pueden proponer referencias verificables mediante búsqueda web:

1. Geología de México · 2. Geotermia en México · 3. Geoquímica · 4. Geofísica · 5. SIG · 6. Vulcanología y neotectónica · 7. Geología estructural (Bloque de Jalisco / Nayarit).

Comparten el contexto en `.kiro/steering/contexto-tesina.md` (título, objetivo de expansión, zona de estudio vs. concesión, bibliografía y reglas). Son de **solo lectura** (no modifican archivos) y entregan hallazgos por severidad. Sus informes se guardan en `docs/revisiones/`.

---

## 10. Referencias Principales

- Prol-Ledesma, R.M. (2000). Evaluation of the reconnaissance results in geothermal exploration using GIS. *Geothermics*, 29, 83–103.
- Bonham-Carter, G.F. (1994). *Geographical Information Systems for Geoscientists: Modelling with GIS*. Pergamon, 398 pp.
- Moeck, I.S. (2014). Catalog of geothermal play types based on geologic controls. *Renewable and Sustainable Energy Reviews*, 37, 867–882.
- Corbo-Camargo, F. et al. (2026). The geothermal system of the San Pedro Dome constrained by magnetotelluric and lithological information. *GSA Special Paper* 566, 53–67. https://doi.org/10.1130/2026.2566(04)
- Ferrari, L. et al. (2003). Geology of the San Pedro–Ceboruco graben, western Trans-Mexican Volcanic Belt. *Rev. Mex. Cienc. Geol.*, 20(3), 165–181.
- Caine, J.S., Evans, J.P. & Forster, C.B. (1996). Fault zone architecture and permeability structure. *Geology*, 24(11), 1025–1028.
- Reyes-Orozco, A. et al. (2019). Preliminary Conceptual Model of the Domo San Pedro Geothermal Field. *44th Stanford Geothermal Workshop*.

> La bibliografía completa (22 fuentes) está en `BIBLIOGRAFIA/` y su texto extraído en `docs/extracted-text/`.

---

## 11. Autor / Contacto

Proyecto desarrollado por: A. Isaac P.S.

Tesina de posgrado para la Especialidad en Exploración y Aprovechamiento de Recursos Geotérmicos (UNAM), sobre la expansión del Campo Geotérmico Domo San Pedro, Nayarit.

---

*Última actualización: Septiembre 2026*
