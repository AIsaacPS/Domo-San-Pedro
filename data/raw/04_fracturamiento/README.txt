================================================================================
  CAPA 04: DENSIDAD DE FRACTURAMIENTO SUPERFICIAL
  Dominio de profundidad: SUPERFICIAL (0–100 m)
                          Indicador indirecto de esfuerzos activos que pueden
                          extenderse a profundidad del reservorio
  Peso en el modelo: 5/10 (importancia media)
================================================================================

DESCRIPCIÓN
===========
Mapa de densidad de fracturamiento superficial en el área del Domo San Pedro.
El fracturamiento intenso en superficie puede ser indicativo de:
- Fracturamiento hidráulico por presión de fluidos en profundidad
- Esfuerzos tectónicos activos que generan permeabilidad secundaria
- Actividad hidrotermal vigorosa que fractura las rocas suprayacentes

QUÉ DATOS COLOCAR AQUÍ
========================
Opción A (preferida): Polígonos delimitando zonas de ALTA densidad de
fracturamiento, derivados de estudios de campo o fotointerpretación.

Opción B: Mapa raster de densidad de lineamientos (lineamientos/km²)
derivado de análisis automatizado de imágenes satelitales.

Opción C: Archivo vectorial de lineamientos individuales (líneas) a partir
del cual se calculará la densidad.

MÉTODOS DE OBTENCIÓN
=====================
1. FOTOINTERPRETACIÓN MANUAL:
   - Imágenes satelitales de alta resolución (Google Earth, Sentinel-2)
   - Identificación visual de lineamientos y fracturas
   - Delimitación de zonas con alta concentración

2. ANÁLISIS AUTOMATIZADO DE LINEAMIENTOS:
   - Filtros direccionales sobre DEM (hillshade multiángulo)
   - Detección de bordes en imágenes satelitales
   - Software: PCI LINE module, ArcGIS Spatial Analyst
   - Cálculo de densidad con kernel density o line density

3. LEVANTAMIENTO DE CAMPO:
   - Estaciones de medición de fracturas (scanlines)
   - Mapeo directo de zonas intensamente fracturadas
   - Medición de orientación y espaciamiento

ATRIBUTOS DESEABLES
====================
- Densidad (fracturas/km² o lineamientos/km)
- Orientación predominante
- Relación con sistemas de fallas conocidos
- Método de obtención
- Escala de la fuente original

CONSIDERACIONES PARA QUE EL DATO SEA VÁLIDO
============================================
1. Distinguir entre fracturamiento TECTÓNICO (relevante) y fracturamiento
   por enfriamiento de lavas (columnar jointing, menos relevante para
   permeabilidad profunda).

2. CUIDADO con el auto-sellado: zonas con alta densidad de fracturamiento
   PERO también abundante mineralización hidrotermal (sílice, calcita,
   arcillas) pueden tener permeabilidad REDUCIDA. Si se identifican estas
   zonas, marcarlas como "selladas" en los atributos.

3. La densidad de fracturamiento puede variar con la litología. Rocas
   frágiles (riolitas, ignimbritas) se fracturan más fácilmente que rocas
   dúctiles. Normalizar si es posible.

4. El análisis de lineamientos desde satélite tiene sesgo direccional
   (detecta mejor lineamientos perpendiculares a la iluminación). Usar
   hillshade con múltiples ángulos de iluminación para minimizar este sesgo.

5. IMPORTANTE: En el modelo, se calculará la DISTANCIA EUCLIDIANA desde cada
   píxel hasta la zona de alto fracturamiento más cercana:
   - ≤ 100 m → Score 10
   - 100–200 m → Score 8
   - > 200 m → Score 0

6. Si se usa densidad de lineamientos (Opción B), primero se debe definir
   un umbral de densidad que delimite las "zonas de alta densidad" y
   convertirlas a polígonos para calcular distancias.

FUENTES SUGERIDAS
=================
- Análisis propio de imágenes Sentinel-2 o SPOT
- Google Earth Pro (fotointerpretación manual)
- DEM ALOS PALSAR (12.5 m) o SRTM (30 m) para hillshade
- Estudios estructurales publicados del área
- Tesis universitarias con levantamiento de fracturas en campo

================================================================================
