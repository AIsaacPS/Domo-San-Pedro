"""
config.py — Configuración centralizada del proyecto Domo San Pedro
===================================================================
Todos los scripts importan rutas y parámetros desde aquí.

USO:
    from config import PROJECT_DIR, CRS_PROYECTO, AREA_ESTUDIO
    # o desde otro directorio:
    import sys; sys.path.insert(0, str(Path(__file__).parent))
    from config import *
"""

from pathlib import Path

# =============================================================================
# RUTAS DEL PROYECTO
# =============================================================================

# Directorio raíz (detectado automáticamente desde la ubicación de config.py)
PROJECT_DIR = Path(__file__).parent.parent

# Datos de entrada (fuentes originales)
DATA_INPUT_DIR = PROJECT_DIR / "DATA INPUT"

# Carpetas temáticas de datos de entrada
FALLAS_DIR = DATA_INPUT_DIR / "01_FALLAS_PRINCIPALES"
MANIFESTACIONES_DIR = DATA_INPUT_DIR / "02_MANIFESTACIONES_TERMALES"
GEOLOGIA_DIR = DATA_INPUT_DIR / "03_GEOLOGIA_FUENTE_CALOR"
FRACTURAMIENTO_DIR = DATA_INPUT_DIR / "04_FRACTURAMIENTO"
RESISTIVIDAD_DIR = DATA_INPUT_DIR / "05_RESISTIVIDAD"
DEM_DIR = DATA_INPUT_DIR / "06_DEM_TOPOGRAFIA"
ANOMALIAS_DIR = DATA_INPUT_DIR / "07_ANOMALIAS_TERMICAS"
GEOQUIMICA_DIR = DATA_INPUT_DIR / "08_GEOQUIMICA"
GRADIENTE_DIR = DATA_INPUT_DIR / "09_GRADIENTE_GEOTERMICO"
GRAVIMETRIA_DIR = DATA_INPUT_DIR / "10_GRAVIMETRIA_MAGNETOMETRIA"

# Datos procesados (salidas intermedias)
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

# Resultados finales
OUTPUTS_DIR = PROJECT_DIR / "outputs"

# =============================================================================
# SISTEMA DE REFERENCIA ESPACIAL
# =============================================================================

CRS_PROYECTO = "EPSG:32613"  # WGS 84 / UTM Zona 13N
CRS_EPSG = 32613

# =============================================================================
# ÁREA DE ESTUDIO
# =============================================================================

# Bounding box en UTM 13N (metros)
AREA_ESTUDIO = {
    "xmin": 520000.0,
    "xmax": 535000.0,
    "ymin": 2328000.0,
    "ymax": 2348000.0,
}

# Dimensiones
AREA_WIDTH_M = AREA_ESTUDIO["xmax"] - AREA_ESTUDIO["xmin"]   # 15,000 m
AREA_HEIGHT_M = AREA_ESTUDIO["ymax"] - AREA_ESTUDIO["ymin"]  # 20,000 m
AREA_KM2 = (AREA_WIDTH_M * AREA_HEIGHT_M) / 1e6              # 300 km²

# =============================================================================
# PARÁMETROS DEL MODELO INDEX OVERLAY
# =============================================================================

# Resolución raster del análisis (metros)
RESOLUCION = 30

# Pesos de cada capa temática (definidos por criterio experto)
PESOS = {
    "resistividad": 9,
    "fallas": 7,
    "manifestaciones": 5,
    "geologia": 5,
    "fracturamiento": 5,
}

# Umbrales de distancia para reclasificación (metros)
UMBRALES_DISTANCIA = {
    "alta": 100,      # ≤ 100 m → Score 10
    "moderada": 200,  # 100–200 m → Score 8
    # > 200 m → Score 0
}

# Umbrales de resistividad (Ω·m)
UMBRALES_RESISTIVIDAD = {
    "alta": 10,   # ≤ 10 → Score 10
    "moderada": 20,  # 10–20 → Score 8
    # > 20 → Score 0
}

# Scores
SCORE_ALTO = 10
SCORE_MODERADO = 8
SCORE_NULO = 0

# Umbrales de favorabilidad para el mapa final
UMBRAL_FAVORABLE = 0.7
UMBRAL_MODERADO = 0.6
