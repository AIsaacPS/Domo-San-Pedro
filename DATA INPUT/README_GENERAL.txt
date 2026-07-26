================================================================================
                    DATA INPUT — GUÍA GENERAL
            Proyecto: Zonas Favorables de Perforación - Domo San Pedro
            Método: Index Overlay Multi-Clase (Prol-Ledesma, 2000)
================================================================================

ORGANIZACIÓN DE CARPETAS
========================

Los datos se organizan según su DOMINIO DE PROFUNDIDAD:

  [SUPERFICIAL]  → Datos observables directamente en superficie (0 m)
  [SUBSUPERFICIAL] → Datos que representan condiciones someras (0–500 m)
  [PROFUNDIDAD]  → Datos que representan condiciones del reservorio (500–3000 m)

Esta clasificación es importante porque el modelo Index Overlay integra
evidencia de diferentes profundidades para inferir la favorabilidad del
reservorio geotérmico en profundidad.


REQUISITOS GENERALES PARA TODOS LOS DATOS
==========================================

1. SISTEMA DE COORDENADAS: Todos los datos deben estar en EPSG:32613
   (WGS 84 / UTM Zona 13N). Este es el CRS DEFINITIVO del proyecto.
   No se aceptan datos en otro sistema para el análisis; reproyectar
   antes de ingresar al modelo.
   - El Domo San Pedro está a ~0.28° del meridiano central (105°W),
     lo que garantiza distorsión mínima.
   - Las unidades en metros son indispensables para los cálculos de
     distancia euclidiana del Index Overlay.

2. EXTENSIÓN ESPACIAL: Todos los mapas deben cubrir la misma área de estudio.
   Definir un rectángulo envolvente (bounding box) común antes de procesar.

3. RESOLUCIÓN RASTER: Para el análisis final, todas las capas raster deben
   tener la misma resolución de celda. Se recomienda 30 m (compatible con
   Landsat y ASTER).

4. FORMATOS ACEPTADOS:
   - Vector: Shapefile (.shp), GeoPackage (.gpkg), GeoJSON
   - Raster: GeoTIFF (.tif), ASCII Grid (.asc)
   - Tabular: CSV con columnas de coordenadas (Lon, Lat o X_UTM, Y_UTM)

5. METADATOS: Cada archivo debe documentar su fuente, fecha de adquisición,
   método de obtención y escala original.

6. CALIDAD: Verificar que no haya gaps, valores nulos sin justificación,
   o artefactos en los datos antes de ingresarlos al modelo.


CAPAS REQUERIDAS PARA EL MODELO INDEX OVERLAY
==============================================

Capa                          | Dominio         | Peso Sugerido | Carpeta
------------------------------|-----------------|---------------|---------------------------
Fallas principales            | SUBSUPERFICIAL  | 7             | 01_FALLAS_PRINCIPALES/
Manifestaciones termales      | SUPERFICIAL     | 5             | 02_MANIFESTACIONES_TERMALES/
Geología (domos/intrusivos)   | SUPERFICIAL     | 5             | 03_GEOLOGIA_FUENTE_CALOR/
Fracturamiento superficial    | SUPERFICIAL     | 5             | 04_FRACTURAMIENTO/
Resistividad eléctrica        | PROFUNDIDAD     | 9             | 05_RESISTIVIDAD/


CAPAS COMPLEMENTARIAS (OPCIONALES)
===================================

Capa                          | Dominio         | Carpeta
------------------------------|-----------------|---------------------------
Modelo Digital de Elevación   | SUPERFICIAL     | 06_DEM_TOPOGRAFIA/
Anomalías térmicas satelitales| SUPERFICIAL     | 07_ANOMALIAS_TERMICAS/
Geoquímica de fluidos         | SUBSUPERFICIAL  | 08_GEOQUIMICA/
Gradiente geotérmico          | PROFUNDIDAD     | 09_GRADIENTE_GEOTERMICO/
Gravimetría y magnetometría   | PROFUNDIDAD     | 10_GRAVIMETRIA_MAGNETOMETRIA/


================================================================================
Última actualización: Julio 2026
================================================================================
