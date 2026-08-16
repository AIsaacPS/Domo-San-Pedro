"""
extraer_resistividad_de_mapa.py
================================
Proyecto: Zonas Favorables de Perforación Geotérmica — Domo San Pedro

Extrae valores numéricos de resistividad (Ω·m) a partir de un mapa de
resistividad en formato imagen (JPG/PNG) y su barra de color asociada.

VERSIÓN 2: Detecta el grid del modelo MT y asigna UN SOLO valor de
resistividad por celda, sampleando el centro de cada celda.

USO:
    python scripts/extraer_resistividad_de_mapa.py

REQUISITOS:
    pip install numpy pillow rasterio matplotlib

AUTOR: Proyecto Domo San Pedro — Tesis A. Isaac P.S.
"""

import numpy as np
from pathlib import Path
from PIL import Image
import sys

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

PROJECT_DIR = Path(r"C:\Users\aisaa\OneDrive\Desktop\DOMO SAN PEDRO")
INPUT_DIR = PROJECT_DIR / "DATA INPUT" / "05_RESISTIVIDAD"

# Archivos de entrada
MAPA_PATH = INPUT_DIR / "d_clean.jpg"         # Mapa LIMPIO (350 mbsl)
COLORBAR_PATH = INPUT_DIR / "Rho_Escale.png"  # Barra de color

# Archivo de salida
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_TIFF = OUTPUT_DIR / "resistividad_350mbsl_UTM13N.tif"

# Coordenadas del mapa recortado (UTM 13N)
XMIN = 520000.0
XMAX = 534500.0
YMIN = 2328000.0
YMAX = 2348000.0

# CRS del proyecto
CRS_EPSG = 32613

# Resolución de salida (metros)
RESOLUCION = 30

# Rango de resistividad de la escala (Ω·m)
RHO_MIN = 1.0
RHO_MAX = 1000.0

# Tamaño de la zona de muestreo en el centro de cada celda (fracción)
# 0.5 = usar el 50% central de cada celda (evita bordes/grid)
SAMPLE_FRACTION = 0.5


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def rgb_to_hsv_array(rgb_array):
    """Convierte array RGB [0-1] a HSV [0-1] vectorizado."""
    r, g, b = rgb_array[..., 0], rgb_array[..., 1], rgb_array[..., 2]
    maxc = np.maximum(np.maximum(r, g), b)
    minc = np.minimum(np.minimum(r, g), b)
    v = maxc
    delta = maxc - minc
    delta_safe = np.where(delta == 0, 1.0, delta)
    s = np.where(maxc == 0, 0.0, delta / maxc)
    rc = (maxc - r) / delta_safe
    gc = (maxc - g) / delta_safe
    bc = (maxc - b) / delta_safe
    h = np.where(r == maxc, bc - gc,
         np.where(g == maxc, 2.0 + rc - bc, 4.0 + gc - rc))
    h = (h / 6.0) % 1.0
    h = np.where(delta == 0, 0.0, h)
    return np.stack([h, s, v], axis=-1)


# =============================================================================
# PASO 1: Construir LUT desde la barra de color
# =============================================================================

def construir_lut_desde_colorbar(colorbar_path, n_samples=256):
    """
    Lee la barra de color y construye un lookup table:
    color HSV → valor de resistividad (escala logarítmica).
    """
    print("=" * 60)
    print("PASO 1: Construyendo LUT desde la barra de color")
    print("=" * 60)

    img = Image.open(colorbar_path).convert("RGB")
    arr = np.array(img).astype(np.float64) / 255.0
    h, w, _ = arr.shape

    print(f"  Imagen colorbar: {w} x {h} píxeles")

    # Detectar columnas de la barra por saturación
    sat_por_col = np.max(arr, axis=2) - np.min(arr, axis=2)
    sat_media_col = np.mean(sat_por_col, axis=0)
    umbral_sat = np.max(sat_media_col) * 0.5
    cols_barra = np.where(sat_media_col > umbral_sat)[0]

    if len(cols_barra) == 0:
        raise ValueError("No se detectó la barra de color")

    col_centro = (cols_barra[0] + cols_barra[-1]) // 2
    ancho = max(3, (cols_barra[-1] - cols_barra[0]) // 3)

    # Perfil vertical promedio
    franja = arr[:, col_centro - ancho//2 : col_centro + ancho//2 + 1, :]
    perfil_rgb = np.mean(franja, axis=1)

    # Detectar rango vertical de la barra
    sat_perfil = np.max(perfil_rgb, axis=1) - np.min(perfil_rgb, axis=1)
    filas_barra = np.where(sat_perfil > np.max(sat_perfil) * 0.3)[0]
    fila_inicio, fila_fin = filas_barra[0], filas_barra[-1]

    # Samplear uniformemente
    filas_sample = np.linspace(fila_inicio, fila_fin, n_samples).astype(int)
    colores_rgb = perfil_rgb[filas_sample]

    # Convertir a HSV
    lut_hsv = rgb_to_hsv_array(colores_rgb.reshape(1, -1, 3)).reshape(-1, 3)

    # Resistividad: arriba=1000 (azul), abajo=1 (rojo)
    lut_rho = np.logspace(np.log10(RHO_MAX), np.log10(RHO_MIN), n_samples)

    print(f"  LUT: {n_samples} muestras")
    print(f"  Hue: {lut_hsv[0,0]:.3f} (azul) → {lut_hsv[-1,0]:.3f} (rojo)")
    print(f"  Rho: {lut_rho[0]:.0f} → {lut_rho[-1]:.0f} Ω·m")
    print()

    return lut_hsv, lut_rho


# =============================================================================
# PASO 2: Detectar el grid del modelo MT
# =============================================================================

def detectar_grid(arr_rgb):
    """
    Detecta las líneas del grid en la imagen analizando cambios abruptos
    de color (las líneas del grid son oscuras/grises sobre los colores
    de resistividad).
    
    Retorna las posiciones (en píxeles) de las líneas verticales y
    horizontales del grid.
    """
    print("=" * 60)
    print("PASO 2: Detectando grid del modelo MT")
    print("=" * 60)

    h, w, _ = arr_rgb.shape

    # Las líneas del grid son oscuras (Value bajo) o grises (Saturation baja)
    # Calcular "oscuridad" de cada pixel
    brightness = np.mean(arr_rgb, axis=2)  # brillo promedio
    saturation = np.max(arr_rgb, axis=2) - np.min(arr_rgb, axis=2)

    # Un pixel es "línea de grid" si es oscuro Y desaturado
    grid_mask = (brightness < 0.3) & (saturation < 0.15)

    # Detectar líneas verticales: columnas con alta densidad de píxeles grid
    grid_density_cols = np.mean(grid_mask, axis=0)  # fracción por columna
    # Detectar líneas horizontales: filas con alta densidad
    grid_density_rows = np.mean(grid_mask, axis=1)

    # Umbral: una línea de grid tiene >20% de sus píxeles como "grid"
    GRID_THRESHOLD = 0.15

    # Encontrar columnas que son líneas de grid
    cols_grid_mask = grid_density_cols > GRID_THRESHOLD
    rows_grid_mask = grid_density_rows > GRID_THRESHOLD

    # Agrupar píxeles contiguos (una línea puede tener 2-3 px de ancho)
    v_lines = _agrupar_lineas(cols_grid_mask)
    h_lines = _agrupar_lineas(rows_grid_mask)

    print(f"  Imagen: {w} x {h} píxeles")
    print(f"  Líneas verticales detectadas: {len(v_lines)}")
    print(f"  Líneas horizontales detectadas: {len(h_lines)}")

    if len(v_lines) > 1 and len(h_lines) > 1:
        # Calcular tamaño de celda
        v_spacing = np.diff([l[0] for l in v_lines])
        h_spacing = np.diff([l[0] for l in h_lines])
        print(f"  Espaciado V medio: {np.mean(v_spacing):.0f} px")
        print(f"  Espaciado H medio: {np.mean(h_spacing):.0f} px")
        cell_w_m = 14000 / (len(v_lines) - 1) if len(v_lines) > 1 else 0
        cell_h_m = 20000 / (len(h_lines) - 1) if len(h_lines) > 1 else 0
        print(f"  Tamaño de celda: ~{cell_w_m:.0f} x {cell_h_m:.0f} m")
    print()

    return v_lines, h_lines, grid_mask


def _agrupar_lineas(mask_1d):
    """
    Agrupa píxeles contiguos marcados como True en clusters.
    Retorna lista de (centro, inicio, fin) para cada línea.
    """
    lines = []
    in_line = False
    start = 0

    for i in range(len(mask_1d)):
        if mask_1d[i] and not in_line:
            start = i
            in_line = True
        elif not mask_1d[i] and in_line:
            center = (start + i - 1) // 2
            lines.append((center, start, i - 1))
            in_line = False

    if in_line:
        center = (start + len(mask_1d) - 1) // 2
        lines.append((center, start, len(mask_1d) - 1))

    return lines


# =============================================================================
# PASO 3: Samplear centro de cada celda y asignar resistividad
# =============================================================================

def samplear_celdas(arr_rgb, v_lines, h_lines, grid_mask, lut_hsv, lut_rho):
    """
    Para cada celda del grid:
    1. Identifica la región central (evitando bordes/grid)
    2. Extrae el color MEDIANO de esa región
    3. Busca en la LUT el valor de resistividad más cercano
    4. Asigna ESE ÚNICO valor a toda la celda
    """
    print("=" * 60)
    print("PASO 3: Sampleando centro de cada celda del grid")
    print("=" * 60)

    h_img, w_img, _ = arr_rgb.shape

    # Si no se detectó grid, usar grid uniforme estimado
    if len(v_lines) < 2 or len(h_lines) < 2:
        print("  ADVERTENCIA: Grid no detectado, usando conteo manual")
        # Conteo manual del grid: 38 columnas x 52 filas
        n_cols_manual = 38
        n_rows_manual = 52
        cell_w_px = w_img / n_cols_manual
        cell_h_px = h_img / n_rows_manual
        v_positions = [int(round(i * cell_w_px)) for i in range(n_cols_manual + 1)]
        h_positions = [int(round(i * cell_h_px)) for i in range(n_rows_manual + 1)]
        print(f"  Usando grid manual: {n_cols_manual} cols x {n_rows_manual} filas")
        print(f"  Celda: {cell_w_px:.1f} x {cell_h_px:.1f} px")
        print(f"  Celda en terreno: ~{14000/n_cols_manual:.0f} x {20000/n_rows_manual:.0f} m")
    else:
        v_positions = [0] + [l[0] for l in v_lines] + [w_img]
        h_positions = [0] + [l[0] for l in h_lines] + [h_img]

    n_cols = len(v_positions) - 1
    n_rows = len(h_positions) - 1

    print(f"  Grid: {n_cols} columnas x {n_rows} filas = {n_cols*n_rows} celdas")

    # Crear mapa de resistividad con un valor por celda
    rho_map = np.full((h_img, w_img), np.nan, dtype=np.float64)

    # LUT para búsqueda
    lut_h = lut_hsv[:, 0]
    lut_s = lut_hsv[:, 1]
    lut_v = lut_hsv[:, 2]
    W_HUE, W_SAT, W_VAL = 4.0, 1.0, 0.5

    celdas_validas = 0
    celdas_vacias = 0

    for row in range(n_rows):
        y0 = h_positions[row]
        y1 = h_positions[row + 1]

        # Zona central en Y (evitar bordes)
        margin_y = int((y1 - y0) * (1 - SAMPLE_FRACTION) / 2)
        cy0 = y0 + margin_y
        cy1 = y1 - margin_y

        for col in range(n_cols):
            x0 = v_positions[col]
            x1 = v_positions[col + 1]

            # Zona central en X
            margin_x = int((x1 - x0) * (1 - SAMPLE_FRACTION) / 2)
            cx0 = x0 + margin_x
            cx1 = x1 - margin_x

            if cx1 <= cx0 or cy1 <= cy0:
                celdas_vacias += 1
                continue

            # Extraer región central
            region = arr_rgb[cy0:cy1, cx0:cx1]

            # Excluir píxeles de grid dentro de la región
            region_grid = grid_mask[cy0:cy1, cx0:cx1]
            valid_pixels = region[~region_grid]

            if len(valid_pixels) < 3:
                celdas_vacias += 1
                continue

            # Calcular color MEDIANO (robusto ante outliers)
            median_rgb = np.median(valid_pixels, axis=0)

            # Convertir a HSV
            hsv = rgb_to_hsv_array(median_rgb.reshape(1, 1, 3))[0, 0]
            px_h, px_s, px_v = hsv

            # Filtrar si no es color válido
            if px_s < 0.05 or px_v < 0.1:
                celdas_vacias += 1
                continue

            # Buscar en LUT
            dh = np.minimum(np.abs(lut_h - px_h), 1.0 - np.abs(lut_h - px_h))
            ds = np.abs(lut_s - px_s)
            dv = np.abs(lut_v - px_v)
            dist = W_HUE * dh**2 + W_SAT * ds**2 + W_VAL * dv**2
            idx = np.argmin(dist)
            rho_val = lut_rho[idx]

            # Asignar MISMO valor a toda la celda (no solo el centro)
            rho_map[y0:y1, x0:x1] = rho_val
            celdas_validas += 1

    print(f"  Celdas con valor: {celdas_validas}")
    print(f"  Celdas vacías/inválidas: {celdas_vacias}")
    print()

    return rho_map, n_cols, n_rows


# =============================================================================
# PASO 4: Exportar como GeoTIFF
# =============================================================================

def exportar_geotiff(rho_array, output_path, xmin, xmax, ymin, ymax, epsg, resolucion):
    """Exporta el array de resistividad como GeoTIFF georreferenciado."""
    print("=" * 60)
    print("PASO 4: Exportando GeoTIFF")
    print("=" * 60)

    import rasterio
    from rasterio.transform import from_bounds
    from rasterio.crs import CRS

    width_m = xmax - xmin
    height_m = ymax - ymin
    cols_out = int(width_m / resolucion)
    rows_out = int(height_m / resolucion)

    print(f"  Extensión: {width_m/1000:.1f} x {height_m/1000:.1f} km")
    print(f"  Resolución: {resolucion} m")
    print(f"  Dimensiones salida: {cols_out} x {rows_out} píxeles")

    # Resamplear al tamaño de salida (nearest para preservar valores discretos)
    nodata_val = -9999.0
    rho_for_resize = np.where(np.isnan(rho_array), nodata_val, rho_array)
    img_rho = Image.fromarray(rho_for_resize.astype(np.float32), mode='F')
    img_resized = img_rho.resize((cols_out, rows_out), Image.NEAREST)
    rho_resampled = np.array(img_resized)
    rho_resampled[rho_resampled == nodata_val] = np.nan

    transform = from_bounds(xmin, ymin, xmax, ymax, cols_out, rows_out)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with rasterio.open(
        str(output_path), 'w', driver='GTiff',
        height=rows_out, width=cols_out, count=1,
        dtype='float32', crs=CRS.from_epsg(epsg),
        transform=transform, nodata=np.nan, compress='LZW',
    ) as dst:
        dst.write(rho_resampled.astype(np.float32), 1)
        dst.update_tags(
            DESCRIPTION="Resistividad electrica (Ohm-m) - Corte 350 mbsl",
            SOURCE="Corbo et al. (2026) - Modelo MT 3D, Domo San Pedro",
            METHOD="Reverse color-mapping con muestreo por celda de grid",
            UNITS="Ohm-m", SCALE="Logarithmic (1-1000)",
            CRS="EPSG:32613 - WGS 84 / UTM Zone 13N",
        )

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"  Guardado: {output_path}")
    print(f"  Tamaño: {size_mb:.2f} MB")
    print()
    return output_path


# =============================================================================
# PASO 5: Estadísticas y preview
# =============================================================================

def generar_estadisticas(rho_array):
    """Imprime estadísticas del mapa generado."""
    print("=" * 60)
    print("PASO 5: Estadísticas")
    print("=" * 60)

    valid = rho_array[~np.isnan(rho_array)]
    if len(valid) == 0:
        print("  ERROR: No se encontraron valores válidos")
        return

    print(f"  Píxeles con dato: {len(valid):,}")
    print(f"  Mínimo: {np.min(valid):.1f} Ω·m")
    print(f"  Máximo: {np.max(valid):.1f} Ω·m")
    print(f"  Mediana: {np.median(valid):.1f} Ω·m")
    print(f"  Media geométrica: {10**np.mean(np.log10(valid)):.1f} Ω·m")
    print(f"  Valores únicos: {len(np.unique(valid))}")
    print()

    alta = np.sum(valid <= 10)
    media = np.sum((valid > 10) & (valid <= 20))
    baja = np.sum(valid > 20)
    total = len(valid)

    print("  Clasificación Index Overlay:")
    print(f"    ≤ 10 Ω·m (Score 10): {alta:,} px ({100*alta/total:.1f}%)")
    print(f"    10–20 Ω·m (Score 8): {media:,} px ({100*media/total:.1f}%)")
    print(f"    > 20 Ω·m (Score 0):  {baja:,} px ({100*baja/total:.1f}%)")
    print()


def guardar_preview(rho_array, output_path):
    """Genera PNG de verificación visual."""
    print("=" * 60)
    print("PASO 6: Preview de verificación")
    print("=" * 60)

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.colors import LogNorm
    except ImportError:
        print("  matplotlib no disponible, saltando")
        return

    fig, ax = plt.subplots(1, 1, figsize=(10, 12))
    im = ax.imshow(
        rho_array, cmap='jet_r',
        norm=LogNorm(vmin=RHO_MIN, vmax=RHO_MAX),
        aspect='equal', extent=[XMIN, XMAX, YMIN, YMAX],
    )
    ax.set_xlabel("Easting (m)")
    ax.set_ylabel("Northing (m)")
    ax.set_title("Resistividad extraída (1 valor/celda) - 350 mbsl")
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Resistividad (Ω·m)")

    preview_path = output_path.parent / f"{output_path.stem}_PREVIEW.png"
    plt.savefig(str(preview_path), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Guardado: {preview_path}")
    print()


# =============================================================================
# MAIN
# =============================================================================

def main():
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  EXTRACCIÓN DE RESISTIVIDAD — VERSIÓN 2 (POR CELDA)       ║")
    print("║  Proyecto: Domo San Pedro — Tesis A. Isaac P.S.            ║")
    print("║  Fuente: Corbo et al. (2026) — Modelo MT 3D               ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    if not MAPA_PATH.exists():
        print(f"ERROR: No se encontró: {MAPA_PATH}")
        sys.exit(1)
    if not COLORBAR_PATH.exists():
        print(f"ERROR: No se encontró: {COLORBAR_PATH}")
        sys.exit(1)

    # Paso 1: LUT
    lut_hsv, lut_rho = construir_lut_desde_colorbar(COLORBAR_PATH)

    # Leer mapa
    img = Image.open(MAPA_PATH).convert("RGB")
    arr_rgb = np.array(img).astype(np.float64) / 255.0
    print(f"  Mapa: {MAPA_PATH.name} ({arr_rgb.shape[1]}x{arr_rgb.shape[0]} px)")
    print()

    # Paso 2: Detectar grid
    v_lines, h_lines, grid_mask = detectar_grid(arr_rgb)

    # Paso 3: Samplear una resistividad por celda
    rho_map, n_cols, n_rows = samplear_celdas(
        arr_rgb, v_lines, h_lines, grid_mask, lut_hsv, lut_rho
    )

    # Paso 4: Exportar GeoTIFF
    exportar_geotiff(rho_map, OUTPUT_TIFF, XMIN, XMAX, YMIN, YMAX,
                     CRS_EPSG, RESOLUCION)

    # Paso 5: Estadísticas
    generar_estadisticas(rho_map)

    # Paso 6: Preview
    guardar_preview(rho_map, OUTPUT_TIFF)

    print("=" * 60)
    print("  COMPLETADO")
    print("=" * 60)
    print(f"  Grid del modelo: {n_cols} x {n_rows} celdas")
    print(f"  GeoTIFF: {OUTPUT_TIFF}")
    print(f"  → Cada celda tiene UN SOLO valor de resistividad")
    print(f"  → Las líneas de grid se eliminaron")
    print()


if __name__ == "__main__":
    main()
