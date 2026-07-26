"""
convertir_pdf_a_png.py
=======================
Convierte cualquier PDF a PNG de alta resolución para georreferenciar en QGIS.

Resuelve el problema de que QGIS/GDAL rasteriza PDFs a 150 DPI por defecto,
produciendo imágenes pixeladas o negras en el georreferenciador.

USO:
    python convertir_pdf_a_png.py <ruta_al_pdf> [dpi] [pagina]

EJEMPLOS:
    python convertir_pdf_a_png.py "BIBLIOGRAFIA COMPLEMENTARIA/mapa.pdf"
    python convertir_pdf_a_png.py "BIBLIOGRAFIA COMPLEMENTARIA/mapa.pdf" 600
    python convertir_pdf_a_png.py "BIBLIOGRAFIA COMPLEMENTARIA/mapa.pdf" 600 2

PARÁMETROS:
    ruta_al_pdf  : Ruta al archivo PDF (relativa o absoluta)
    dpi          : Resolución de salida en DPI (default: 600)
    pagina       : Número de página a convertir, empezando en 1 (default: 1)

REQUISITOS:
    pip install pymupdf

NOTAS:
    - Ejecutar desde cmd o PowerShell, NO desde la consola de Python de QGIS
    - El PNG se guarda en la misma carpeta del PDF con sufijo _HQ
    - Usa fondo blanco explícito para evitar imágenes negras
    - 600 DPI es óptimo para georreferenciar. 300 es mínimo aceptable.
"""

import sys
from pathlib import Path


def convertir_pdf_a_png(pdf_path, dpi=600, pagina=1):
    """
    Convierte una página de un PDF a PNG de alta resolución.

    Parámetros:
        pdf_path : Path o str — ruta al archivo PDF
        dpi      : int — resolución de salida (default: 600)
        pagina   : int — número de página a convertir, base 1 (default: 1)

    Retorna:
        Path — ruta al archivo PNG generado
    """
    pdf_path = Path(pdf_path).resolve()

    if not pdf_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"El archivo no es un PDF: {pdf_path}")

    # Nombre de salida: mismo nombre con sufijo _HQ.png (en el mismo directorio)
    png_path = pdf_path.parent.resolve() / f"{pdf_path.stem}_HQ.png"

    # Importar PyMuPDF
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("ERROR: PyMuPDF no está instalado.")
        print("Instálalo con: pip install pymupdf")
        print()
        print("Si usas el Python de QGIS:")
        print('  &"C:\\Program Files\\QGIS 3.34.13\\apps\\Python312\\python.exe" -m pip install pymupdf')
        sys.exit(1)

    # Abrir PDF
    print(f"Abriendo: {pdf_path.name}")
    doc = fitz.open(str(pdf_path))

    # Validar número de página
    total_paginas = len(doc)
    if pagina < 1 or pagina > total_paginas:
        doc.close()
        raise ValueError(
            f"Página {pagina} fuera de rango. El PDF tiene {total_paginas} página(s)."
        )

    page = doc[pagina - 1]  # fitz usa índice base 0

    # Calcular zoom: PDF usa 72 DPI internamente
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)

    print(f"Página: {pagina} de {total_paginas}")
    print(f"Tamaño de página: {page.rect.width:.0f} x {page.rect.height:.0f} puntos")
    print(f"Renderizando a {dpi} DPI (zoom: {zoom:.2f}x)...")

    # Renderizar con fondo blanco (alpha=False evita fondo negro)
    pix = page.get_pixmap(matrix=mat, alpha=False)

    print(f"Imagen resultante: {pix.width} x {pix.height} píxeles")
    print(f"Guardando: {png_path.name}")

    pix.save(str(png_path))
    doc.close()

    size_mb = png_path.stat().st_size / (1024 * 1024)
    print(f"Tamaño: {size_mb:.1f} MB")

    return png_path


# =============================================================================
# EJECUCIÓN DESDE LÍNEA DE COMANDOS
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  PDF -> PNG de alta resolucion")
    print("  Para georreferenciar en QGIS sin pérdida de calidad")
    print("=" * 60)
    print()

    # Parsear argumentos
    if len(sys.argv) < 2:
        print("USO:")
        print("  python convertir_pdf_a_png.py <ruta_al_pdf> [dpi] [pagina]")
        print()
        print("EJEMPLOS:")
        print('  python convertir_pdf_a_png.py "mapa_geologico.pdf"')
        print('  python convertir_pdf_a_png.py "mapa_geologico.pdf" 600')
        print('  python convertir_pdf_a_png.py "mapa_geologico.pdf" 600 2')
        sys.exit(0)

    pdf_input = Path(sys.argv[1]).resolve()
    dpi = int(sys.argv[2]) if len(sys.argv) > 2 else 600
    pagina = int(sys.argv[3]) if len(sys.argv) > 3 else 1

    # Validar DPI
    if dpi < 72:
        print("ADVERTENCIA: DPI muy bajo. Mínimo recomendado: 300")
    elif dpi > 1200:
        print(f"ADVERTENCIA: DPI muy alto ({dpi}). El archivo será muy pesado.")
        print("Recomendado: 600 para georreferenciar.")

    print(f"Archivo: {pdf_input}")
    print(f"DPI: {dpi}")
    print(f"Página: {pagina}")
    print()

    try:
        resultado = convertir_pdf_a_png(pdf_input, dpi=dpi, pagina=pagina)
        print()
        print("=" * 60)
        print("ÉXITO!")
        print(f"PNG listo para georreferenciar: {resultado}")
        print("=" * 60)
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)
