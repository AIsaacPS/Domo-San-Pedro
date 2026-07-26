# Guía de Contribución y Configuración

## Clonar el repositorio

```bash
git clone https://github.com/<usuario>/domo-san-pedro.git
cd domo-san-pedro
```

## Configurar el entorno Python

```bash
pip install -r requirements.txt
```

## Obtener los datos (no están en Git)

Los archivos binarios (`.tif`, `.shp`, `.pdf`) están excluidos del repositorio
por tamaño. Después de clonar, coloca los datos en las carpetas correspondientes:

| Carpeta | Contenido |
|---------|-----------|
| `data/raw/01_fallas_principales/` | Shapefile de fallas (Fallas.shp, etc.) |
| `data/raw/03_geologia_fuente_calor/` | Litología SGM + Ferrari 2003 |
| `data/raw/06_dem_topografia/` | DEM INEGI CEM 15m (18_Nayarit_r15m_v4.tif) |
| `data/raw/08_geoquimica/` | Geoquímica SGM |

Consulta el `README.txt` de cada carpeta para detalles de cada capa.

## Ejecutar el pipeline

Los scripts se ejecutan en orden desde la consola de Python de QGIS,
excepto `convertir_pdf_a_png.py` que se ejecuta desde terminal:

```
01_cargar_datos_y_area_estudio.py  → desde consola QGIS
02_calculo_distancias.py           → desde consola QGIS
03_reclasificacion.py              → desde consola QGIS
04_index_overlay.py                → desde terminal
05_visualizacion.py                → desde terminal
```

## Qué SÍ va a Git

- Código Python (`scripts/`)
- Documentación (`README.md`, `docs/`, `data/raw/*/README.txt`)
- Archivos de proyección `.prj` (texto plano)
- Textos extraídos de artículos (`docs/extracted-text/`)
- `requirements.txt`, `.gitignore`

## Qué NO va a Git (excluido por `.gitignore`)

- Archivos raster (`.tif`, `.img`, `.asc`)
- Shapefiles binarios (`.shp`, `.shx`, `.dbf`)
- PDFs, imágenes (`.pdf`, `.png`, `.jpg`)
- Proyecto QGIS (`.qgz`) — contiene rutas absolutas locales
- Carpeta `outputs/` — se regenera ejecutando los scripts
