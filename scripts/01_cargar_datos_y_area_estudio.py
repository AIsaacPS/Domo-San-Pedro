"""
01_cargar_datos_y_area_estudio.py
=================================
Proyecto: Zonas Favorables de Perforación Geotérmica — Domo San Pedro
CRS del proyecto: EPSG:32613 (WGS 84 / UTM Zona 13N)

EJECUTAR DESDE: Consola de Python de QGIS (no requiere librerías externas)

Este script:
1. Define el área de estudio como un rectángulo en UTM 13N
2. Carga el DEM (CEM INEGI 15m), lo reproyecta a UTM 13N y lo recorta
3. Carga la geología (Litología SGM), la recorta al área de estudio
4. Agrega todas las capas al proyecto de QGIS
"""

import os
import processing
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsCoordinateReferenceSystem,
    QgsFeature,
    QgsGeometry,
    QgsRectangle,
    QgsField,
    QgsVectorFileWriter,
    QgsCoordinateTransformContext,
)
from qgis.PyQt.QtCore import QVariant
from pathlib import Path

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

# Directorio raíz del proyecto
PROJECT_DIR = Path(r"C:\Users\aisaa\OneDrive\Desktop\DOMO SAN PEDRO")

# Datos de entrada
DEM_INPUT = str(PROJECT_DIR / "DATA INPUT" / "06_DEM_TOPOGRAFIA" / "e18_cem_r15_v4_tif" / "conjunto_de_datos" / "18_Nayarit_r15m_v4.tif")
GEOLOGIA_INPUT = str(PROJECT_DIR / "DATA INPUT" / "03_GEOLOGIA_FUENTE_CALOR" / "GEOLOGIA-SGM" / "Litologia_F13_8.shp")

# Directorio de salida
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Archivos de salida
AREA_ESTUDIO_OUTPUT = str(OUTPUT_DIR / "area_estudio_UTM13N.shp")
DEM_REPROYECTADO = str(OUTPUT_DIR / "DEM_Nayarit_UTM13N_30m.tif")
DEM_RECORTADO = str(OUTPUT_DIR / "DEM_area_estudio_UTM13N.tif")
GEOLOGIA_RECORTADA = str(OUTPUT_DIR / "geologia_area_estudio_UTM13N.shp")

# CRS del proyecto
CRS_PROYECTO = "EPSG:32613"

# Área de estudio (UTM 13N, metros)
XMIN = 520000
XMAX = 534000
YMIN = 2328000
YMAX = 2346000

# Resolución del DEM de salida (metros)
RESOLUCION = 30

# =============================================================================
# PASO 1: Crear polígono del área de estudio
# =============================================================================
print("=" * 60)
print("PASO 1: Creando polígono del área de estudio")
print("=" * 60)

# Crear capa en memoria
crs = QgsCoordinateReferenceSystem(CRS_PROYECTO)
layer_area = QgsVectorLayer(f"Polygon?crs={CRS_PROYECTO}", "area_estudio", "memory")
provider = layer_area.dataProvider()

# Agregar campos
provider.addAttributes([
    QgsField("nombre", QVariant.String),
    QgsField("xmin", QVariant.Double),
    QgsField("xmax", QVariant.Double),
    QgsField("ymin", QVariant.Double),
    QgsField("ymax", QVariant.Double),
])
layer_area.updateFields()

# Crear el rectángulo
rect = QgsRectangle(XMIN, YMIN, XMAX, YMAX)
feat = QgsFeature()
feat.setGeometry(QgsGeometry.fromRect(rect))
feat.setAttributes(["Domo San Pedro", XMIN, XMAX, YMIN, YMAX])
provider.addFeature(feat)
layer_area.updateExtents()

# Guardar como shapefile
options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "ESRI Shapefile"
options.fileEncoding = "UTF-8"
QgsVectorFileWriter.writeAsVectorFormatV3(
    layer_area, AREA_ESTUDIO_OUTPUT, QgsCoordinateTransformContext(), options
)

print(f"  Extension X: {XMIN} - {XMAX} m ({(XMAX-XMIN)/1000:.0f} km)")
print(f"  Extension Y: {YMIN} - {YMAX} m ({(YMAX-YMIN)/1000:.0f} km)")
print(f"  Area: {(XMAX-XMIN)*(YMAX-YMIN)/1e6:.0f} km2")
print(f"  CRS: {CRS_PROYECTO}")
print(f"  Guardado: {AREA_ESTUDIO_OUTPUT}")
print()

# =============================================================================
# PASO 2: Reproyectar DEM a UTM 13N
# =============================================================================
print("=" * 60)
print("PASO 2: Reproyectando DEM a EPSG:32613 (30 m)")
print("=" * 60)

# Verificar CRS del DEM original
dem_layer = QgsRasterLayer(DEM_INPUT, "DEM_original")
if not dem_layer.isValid():
    raise Exception(f"No se pudo cargar el DEM: {DEM_INPUT}")

print(f"  Archivo: {Path(DEM_INPUT).name}")
print(f"  CRS original: {dem_layer.crs().authid()}")
print(f"  Dimensiones: {dem_layer.width()} x {dem_layer.height()} pixeles")

# Reproyectar usando gdal:warpreproject
result = processing.run("gdal:warpreproject", {
    'INPUT': DEM_INPUT,
    'SOURCE_CRS': dem_layer.crs(),
    'TARGET_CRS': QgsCoordinateReferenceSystem(CRS_PROYECTO),
    'RESAMPLING': 1,  # 1 = Bilinear
    'TARGET_RESOLUTION': RESOLUCION,
    'NODATA': -9999,
    'OPTIONS': 'COMPRESS=LZW',
    'DATA_TYPE': 0,  # 0 = usar tipo del input
    'OUTPUT': DEM_REPROYECTADO
})

print(f"  Reproyectado a: {CRS_PROYECTO}")
print(f"  Resolucion: {RESOLUCION} m")
print(f"  Guardado: {DEM_REPROYECTADO}")
print()

# =============================================================================
# PASO 3: Recortar DEM al área de estudio
# =============================================================================
print("=" * 60)
print("PASO 3: Recortando DEM al area de estudio")
print("=" * 60)

# Recortar usando gdal:cliprasterbyextent
extent_str = f"{XMIN},{XMAX},{YMIN},{YMAX} [{CRS_PROYECTO}]"

result = processing.run("gdal:cliprasterbyextent", {
    'INPUT': DEM_REPROYECTADO,
    'PROJWIN': extent_str,
    'NODATA': -9999,
    'OPTIONS': 'COMPRESS=LZW',
    'DATA_TYPE': 0,
    'OUTPUT': DEM_RECORTADO
})

print(f"  Extent: {extent_str}")
print(f"  Guardado: {DEM_RECORTADO}")
print()

# =============================================================================
# PASO 4: Recortar geología al área de estudio
# =============================================================================
print("=" * 60)
print("PASO 4: Recortando geologia al area de estudio")
print("=" * 60)

# Cargar geología
geo_layer = QgsVectorLayer(GEOLOGIA_INPUT, "geologia_original", "ogr")
if not geo_layer.isValid():
    raise Exception(f"No se pudo cargar la geologia: {GEOLOGIA_INPUT}")

print(f"  Archivo: {Path(GEOLOGIA_INPUT).name}")
print(f"  CRS: {geo_layer.crs().authid()}")
print(f"  Registros totales: {geo_layer.featureCount()}")

# La geología ya está en UTM 13N, solo recortar
# Usar el shapefile del área de estudio como máscara
result = processing.run("native:clip", {
    'INPUT': GEOLOGIA_INPUT,
    'OVERLAY': AREA_ESTUDIO_OUTPUT,
    'OUTPUT': GEOLOGIA_RECORTADA
})

# Contar registros resultantes
geo_recortada = QgsVectorLayer(GEOLOGIA_RECORTADA, "geologia_recortada", "ogr")
print(f"  Registros en area de estudio: {geo_recortada.featureCount()}")

# Listar unidades litológicas
campos = [f.name() for f in geo_recortada.fields()]
col_litologia = None
for candidato in ["CLAVE", "LITOLOGIA", "NOMBRE", "CLAVE_LITO", "TIPO"]:
    if candidato in campos:
        col_litologia = candidato
        break

if col_litologia:
    unidades = set()
    for feat in geo_recortada.getFeatures():
        unidades.add(feat[col_litologia])
    print(f"\n  Unidades litologicas ({col_litologia}):")
    for u in sorted(unidades):
        print(f"    - {u}")
else:
    print(f"  Campos disponibles: {campos}")

print(f"\n  Guardado: {GEOLOGIA_RECORTADA}")
print()

# =============================================================================
# PASO 5: Agregar capas al proyecto de QGIS
# =============================================================================
print("=" * 60)
print("PASO 5: Agregando capas al proyecto QGIS")
print("=" * 60)

# Configurar CRS del proyecto
QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(CRS_PROYECTO))
print(f"  CRS del proyecto configurado: {CRS_PROYECTO}")

# Agregar área de estudio
layer_ae = QgsVectorLayer(AREA_ESTUDIO_OUTPUT, "Area de Estudio", "ogr")
QgsProject.instance().addMapLayer(layer_ae)

# Agregar DEM recortado
layer_dem = QgsRasterLayer(DEM_RECORTADO, "DEM Area Estudio (30m)")
QgsProject.instance().addMapLayer(layer_dem)

# Agregar geología recortada
layer_geo = QgsVectorLayer(GEOLOGIA_RECORTADA, "Geologia (Litologia SGM)", "ogr")
QgsProject.instance().addMapLayer(layer_geo)

print("  Capas agregadas:")
print("    - Area de Estudio (poligono)")
print("    - DEM Area Estudio (30m)")
print("    - Geologia (Litologia SGM)")
print()

# =============================================================================
# RESUMEN FINAL
# =============================================================================
print("=" * 60)
print("  PROCESO COMPLETADO")
print("=" * 60)
print(f"  Area de estudio: {(XMAX-XMIN)/1000:.0f} x {(YMAX-YMIN)/1000:.0f} km = {(XMAX-XMIN)*(YMAX-YMIN)/1e6:.0f} km2")
print(f"  CRS: {CRS_PROYECTO} (WGS 84 / UTM Zona 13N)")
print(f"  DEM: reproyectado y recortado a 30 m")
print(f"  Geologia: recortada al area de estudio")
print(f"  Salidas en: {OUTPUT_DIR}")
print()
