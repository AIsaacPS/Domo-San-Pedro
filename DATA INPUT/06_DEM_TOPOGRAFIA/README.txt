================================================================================
  CAPA 06 (COMPLEMENTARIA): MODELO DIGITAL DE ELEVACIÓN (DEM)
  Dominio de profundidad: SUPERFICIAL (topografía, 0 m)
  Peso en el modelo: No participa directamente en el Index Overlay
================================================================================

DESCRIPCIÓN
===========
Modelo Digital de Elevación del área del Domo San Pedro. Aunque no es una
capa directa del Index Overlay, es INDISPENSABLE como dato base para:
- Análisis de lineamientos (hillshade multiángulo)
- Contexto topográfico para la visualización de resultados
- Delimitación del área de estudio
- Análisis de cuencas y drenaje (control estructural)
- Cálculo de pendientes (accesibilidad para perforación)

QUÉ DATOS COLOCAR AQUÍ
========================
- DEM en formato raster (GeoTIFF)
- Resolución recomendada: 12.5–30 m

FUENTES GRATUITAS
=================
- ALOS PALSAR (12.5 m): https://search.asf.alaska.edu/
- SRTM (30 m): https://earthexplorer.usgs.gov/
- ASTER GDEM v3 (30 m): https://earthexplorer.usgs.gov/
- CEM 3.0 INEGI (15 m, México): https://www.inegi.org.mx/
- Copernicus DEM (30 m): https://spacedata.copernicus.eu/

CONSIDERACIONES
===============
1. Para análisis de lineamientos, preferir resolución ≤ 15 m.
2. Verificar que no haya artefactos (huecos, picos anómalos).
3. En zonas con vegetación densa, los DEM derivados de radar (SRTM)
   representan el dosel, no el terreno. Los DEM de INEGI (LiDAR donde
   disponible) son más precisos.
4. Descargar un área mayor al polígono de estudio para evitar efectos de borde.

================================================================================
