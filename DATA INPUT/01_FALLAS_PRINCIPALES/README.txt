================================================================================
  CAPA 01: FALLAS PRINCIPALES
  Dominio de profundidad: SUBSUPERFICIAL (se observan en superficie pero
                          controlan la permeabilidad en profundidad, 0–3000 m)
  Peso en el modelo: 7/10 (alta importancia)
================================================================================

DESCRIPCIÓN
===========
Mapa de las fallas principales activas o recientes en el área del Domo San
Pedro. Las fallas son el control primario de permeabilidad secundaria en
sistemas geotérmicos volcánicos; determinan por dónde circulan los fluidos
del reservorio.

QUÉ DATOS COLOCAR AQUÍ
========================
- Archivos vectoriales (shapefile o similar) con las trazas de fallas.
- Cada falla debe ser una línea (polyline) georreferenciada.

ATRIBUTOS DESEABLES (tabla de atributos del shapefile)
======================================================
- Nombre o ID de la falla
- Sistema al que pertenece (orientación: E-W, NE-SW, N-S, NW-SE)
- Tipo de falla (normal, inversa, lateral, inferida)
- Longitud (km)
- Evidencia de actividad reciente (sí/no, edad estimada)
- Buzamiento (si se conoce)
- Fuente del dato

CONSIDERACIONES PARA QUE EL DATO SEA VÁLIDO
============================================
1. Incluir TODAS las fallas con evidencia de actividad cuaternaria o reciente.
   Las fallas antiguas selladas no aportan permeabilidad al reservorio actual.

2. No discriminar por orientación: en etapa de reconocimiento, se asume que
   todos los sistemas de fallas contribuyen igualmente a la permeabilidad
   hasta que se demuestre lo contrario.

3. Si solo se tienen fallas inferidas (de imágenes satelitales o fotointerpretación),
   indicarlo claramente en los atributos. Son válidas pero con mayor incertidumbre.

4. La escala mínima aceptable es 1:50,000. Mapas a escala 1:250,000 son
   demasiado generales para este análisis a nivel de campo geotérmico.

5. IMPORTANTE: En el modelo, se calculará la DISTANCIA EUCLIDIANA desde cada
   píxel hasta la falla más cercana. Los umbrales son:
   - ≤ 100 m → Score 10 (máxima favorabilidad)
   - 100–200 m → Score 8 (favorabilidad moderada)
   - > 200 m → Score 0 (no favorable)

FUENTES SUGERIDAS
=================
- Servicio Geológico Mexicano (SGM): Cartas geológico-mineras 1:50,000
- Publicaciones académicas sobre la geología del Domo San Pedro
- Interpretación propia de imágenes satelitales (Sentinel-2, Google Earth)
- Datos de campo (levantamiento estructural)
- Base de datos de fallas activas de México (CENAPRED/UNAM)

================================================================================
