# Inventario de Datos — Proyecto Domo San Pedro

Estado de cada capa requerida para el modelo Index Overlay.
Última actualización: Agosto 2026

## Capas Requeridas (Modelo Index Overlay)

| # | Capa | Peso | Estado | Fuente | Formato actual | Procesado |
|---|------|------|--------|--------|----------------|-----------|
| 01 | Fallas principales | 7 | ✅ Disponible | Ferrari 2003 + Corbo 2026 | Shapefile | Pendiente: distancia euclidiana |
| 02 | Manifestaciones termales | 5 | ⬜ Pendiente | Por digitalizar de publicaciones | — | — |
| 03 | Geología (fuente calor) | 5 | ✅ Disponible | SGM (Litología F13-8) + Ferrari 2003 | Shapefile | Recortada a área de estudio |
| 04 | Fracturamiento superficial | 5 | ⬜ Pendiente | Por interpretar de imágenes satelitales | — | — |
| 05 | Resistividad eléctrica | 9 | ✅ Extraída | Corbo 2026 (modelo MT 3D, 350 mbsl) | GeoTIFF (extraído de mapa) | `resistividad_350mbsl_UTM13N.tif` |

## Capas Complementarias (Opcionales)

| # | Capa | Estado | Fuente | Notas |
|---|------|--------|--------|-------|
| 06 | DEM / Topografía | ✅ Disponible | INEGI CEM 15m Nayarit | Reproyectado a 30m UTM13N |
| 07 | Anomalías térmicas satelitales | ⬜ Pendiente | ASTER TIR / Landsat Band 10 | Opcional |
| 08 | Geoquímica | 🔶 Parcial | SGM (shapefile en carpeta) | Revisar contenido |
| 09 | Gradiente geotérmico | ⬜ Pendiente | CFE / publicaciones | Opcional pero recomendado |
| 10 | Gravimetría / Magnetometría | ⬜ Pendiente | Publicaciones | Opcional (uso regional) |

## Datos Procesados Disponibles (`data/processed/`)

| Archivo | Descripción | CRS | Resolución |
|---------|-------------|-----|------------|
| `area_estudio_UTM13N.shp` | Polígono del área de estudio | EPSG:32613 | — |
| `DEM_Nayarit_UTM13N_30m.tif` | DEM Nayarit completo reproyectado | EPSG:32613 | 30 m |
| `DEM_area_estudio_UTM13N.tif` | DEM recortado al área de estudio | EPSG:32613 | 30 m |
| `geologia_area_estudio_UTM13N.shp` | Litología SGM recortada | EPSG:32613 | — |
| `resistividad_350mbsl_UTM13N.tif` | Resistividad (Corbo 2026, 38×52 celdas) | EPSG:32613 | 30 m |

## Datos por Generar (Pipeline pendiente)

| Archivo esperado | Script | Depende de |
|-----------------|--------|------------|
| `distancia_fallas.tif` | `02_calculo_distancias.py` | Capa 01 |
| `distancia_manifestaciones.tif` | `02_calculo_distancias.py` | Capa 02 |
| `distancia_domos.tif` | `02_calculo_distancias.py` | Capa 03 |
| `distancia_fracturamiento.tif` | `02_calculo_distancias.py` | Capa 04 |
| `score_fallas.tif` | `03_reclasificacion.py` | distancia_fallas |
| `score_manifestaciones.tif` | `03_reclasificacion.py` | distancia_manifestaciones |
| `score_domos.tif` | `03_reclasificacion.py` | distancia_domos |
| `score_fracturamiento.tif` | `03_reclasificacion.py` | distancia_fracturamiento |
| `score_resistividad.tif` | `03_reclasificacion.py` | resistividad_350mbsl |
| `mapa_favorabilidad.tif` | `04_index_overlay.py` | Todos los scores |

## Leyenda de Estado

- ✅ Disponible y listo para usar
- 🔶 Parcialmente disponible (necesita revisión o complemento)
- ⬜ Pendiente (no adquirido o no procesado)

## Notas sobre la Resistividad

La capa de resistividad (peso 9, la más importante) fue extraída del mapa
publicado por Corbo et al. (2026) usando el script `extraer_resistividad_de_mapa.py`.
El método (reverse color-mapping por celda) produce valores aproximados.
Cuando el Dr. Corbo proporcione el GeoTIFF original del modelo de inversión,
se reemplazará esta capa por la versión exacta.
