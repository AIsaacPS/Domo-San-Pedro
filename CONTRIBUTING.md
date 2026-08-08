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
por tamaño. Después de clonar, coloca los datos en las carpetas correspondientes
dentro de `DATA INPUT/`:

| Carpeta | Contenido |
|---------|-----------|
| `DATA INPUT/01_FALLAS_PRINCIPALES/` | Shapefiles de fallas (Ferrari 2003, Corbo 2026) |
| `DATA INPUT/03_GEOLOGIA_FUENTE_CALOR/` | Litología SGM + Ferrari 2003 |
| `DATA INPUT/05_RESISTIVIDAD/` | Mapas MT de Corbo 2026 (JPG + clean) |
| `DATA INPUT/06_DEM_TOPOGRAFIA/` | DEM INEGI CEM 15m (18_Nayarit_r15m_v4.tif) |
| `DATA INPUT/08_GEOQUIMICA/` | Geoquímica SGM |

Consulta el `README.txt` de cada carpeta para detalles de cada capa.
Consulta `INVENTARIO.md` en la raíz para ver el estado completo de los datos.

## Ejecutar el pipeline

Los scripts se ejecutan en orden. Hay dos entornos:

```
scripts/config.py                          → Importar para rutas y parámetros
01_cargar_datos_y_area_estudio.py          → desde consola QGIS
extraer_resistividad_de_mapa.py            → desde terminal
02_calculo_distancias.py                   → desde consola QGIS (pendiente)
03_reclasificacion.py                      → desde consola QGIS (pendiente)
04_index_overlay.py                        → desde terminal (pendiente)
05_visualizacion.py                        → desde terminal (pendiente)
```

## Qué SÍ va a Git

- Código Python (`scripts/`)
- Documentación (`README.md`, `INVENTARIO.md`, `CONTRIBUTING.md`)
- READMEs de datos (`DATA INPUT/*/README.txt`)
- Archivos de proyección `.prj` (texto plano)
- Textos extraídos de artículos (`docs/extracted-text/`)
- `requirements.txt`, `.gitignore`
- GeoJSON (texto plano, versionable)

## Qué NO va a Git (excluido por `.gitignore`)

- Archivos raster (`.tif`, `.img`, `.asc`)
- Shapefiles binarios (`.shp`, `.shx`, `.dbf`)
- PDFs, imágenes (`.pdf`, `.png`, `.jpg`)
- Proyecto QGIS (`.qgz`) — contiene rutas absolutas locales
- Carpeta `outputs/` — se regenera ejecutando los scripts
- Carpeta `data/processed/` — se regenera ejecutando los scripts
