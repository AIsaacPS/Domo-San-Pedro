# Scripts — Proyecto Domo San Pedro

Scripts de apoyo para el análisis GIS de zonas favorables de perforación geotérmica.

## Entorno de ejecución

Los scripts de este proyecto se dividen en dos categorías:

| Tipo | Ejecutar desde | Dependencias |
|------|---------------|--------------|
| Scripts PyQGIS (`01_cargar_datos_*`) | Consola de Python de QGIS | Ninguna externa (usa PyQGIS + Processing) |
| Scripts de utilidad (`convertir_pdf_*`) | Terminal (cmd / PowerShell) | Ver `requirements.txt` en la raíz |

## Scripts disponibles

### `convertir_pdf_a_png.py`

Convierte un PDF a PNG de alta resolución para georreferenciar en QGIS sin pérdida de calidad.

**Problema que resuelve**: QGIS (vía GDAL) rasteriza PDFs a 150 DPI por defecto, lo que produce imágenes pixeladas o completamente negras en el georreferenciador.

**Solución**: Usa PyMuPDF para renderizar el PDF a la resolución deseada (600 DPI por defecto) con fondo blanco explícito.

**Instalación** (una sola vez):
```bash
pip install pymupdf
```

Si usas el Python de QGIS en Windows:
```powershell
& "C:\Program Files\QGIS 3.34.13\apps\Python312\python.exe" -m pip install pymupdf
```

**Uso**:
```bash
python scripts/convertir_pdf_a_png.py <ruta_al_pdf> [dpi] [pagina]
```

**Ejemplos**:
```bash
# Convertir un mapa a 600 DPI (primera página)
python scripts/convertir_pdf_a_png.py "BIBLIOGRAFIA COMPLEMENTARIA/mapa.pdf"

# Convertir a 900 DPI para máxima calidad
python scripts/convertir_pdf_a_png.py "BIBLIOGRAFIA COMPLEMENTARIA/mapa.pdf" 900

# Convertir la página 3 de un artículo
python scripts/convertir_pdf_a_png.py "BIBLIOGRAFIA COMPLEMENTARIA/articulo.pdf" 600 3
```

**Salida**: Se genera un PNG en la misma carpeta del PDF con sufijo `_HQ.png`.

**Recomendaciones de DPI**:

| DPI | Uso recomendado | Tamaño aprox. |
|-----|-----------------|---------------|
| 300 | Mínimo aceptable para georreferenciar | ~1 MB |
| 600 | Óptimo: buena calidad sin archivos enormes | ~2-5 MB |
| 900 | Máxima calidad para mapas con detalle fino | ~5-15 MB |

---

### `01_cargar_datos_y_area_estudio.py`

Carga el DEM y la geología al proyecto QGIS, define el área de estudio y reproyecta/recorta todo a EPSG:32613.

**Ejecutar desde**: Consola de Python de QGIS

```python
exec(Path('C:/Users/aisaa/OneDrive/Desktop/DOMO SAN PEDRO/scripts/01_cargar_datos_y_area_estudio.py').read_text())
```

**Qué hace**:
1. Crea el polígono del área de estudio (520000-534000 E, 2328000-2346000 N)
2. Reproyecta el DEM de INEGI (CEM 15m) a UTM 13N y lo resamplea a 30 m
3. Recorta el DEM al área de estudio
4. Recorta la geología (Litología SGM) al área de estudio
5. Agrega todas las capas al proyecto QGIS con CRS = EPSG:32613

**No requiere dependencias externas** — usa exclusivamente PyQGIS y Processing.

---

## CRS del proyecto

Todos los outputs se generan en **EPSG:32613 (WGS 84 / UTM Zona 13N)**.
