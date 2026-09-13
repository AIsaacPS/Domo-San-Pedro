"""
05_visualizacion.py — Mapas del modelo Index Overlay (Domo San Pedro)
=====================================================================
Proyecto: Zonas Favorables de Perforación Geotérmica — Domo San Pedro
Autor: A. Isaac P.S.

Genera CUATRO mapas (PNG) del flujo de favorabilidad:

  1. fallas_zona_dano_UTM13N.png       → Fallas + zona de daño (buffer 100 m)
  2. resistividad_MT_350mbsl_UTM13N.png → Resistividad MT, corte 350 mbsl (referencia)
  3. index_overlay_gradiente_UTM13N.png → Favorabilidad continua Index Overlay (0–1)
  4. modelo_booleano_UTM13N.png         → Modelo booleano (favorable / no favorable)

ACTUALIZACIÓN 2026-09 (reunión Dra. Prol-Ledesma 2026-08-29):
  - Zona de daño de fallas: buffer de ALTA favorabilidad = 100 m (configurable en BUFFER_ALTA).
  - Se excluye el borde de caldera inferido (no es una falla con permeabilidad).
  - Resistividad: NUEVO criterio de VENTANA. El yacimiento está en 20–50 Ω·m;
    < 10 Ω·m es la capa sello de arcillas (no favorable), > 50 Ω·m roca fría.

USO:
    python scripts/05_visualizacion.py

REQUISITOS: numpy, scipy, rasterio, pyshp (shapefile), matplotlib
"""

import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, ListedColormap, BoundaryNorm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy import ndimage
import rasterio
import shapefile  # pyshp

# Importar configuración centralizada
sys.path.insert(0, str(Path(__file__).parent))
import config as C

# =============================================================================
# PARÁMETROS
# =============================================================================

RESISTIVIDAD_TIF = C.PROCESSED_DIR / "resistividad_350mbsl_UTM13N.tif"
OUTPUTS_DIR = C.OUTPUTS_DIR
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# Shapefiles de fallas (todos POLYLINE, EPSG:32613)
FALLAS_SHP = [
    C.FALLAS_DIR / "CORBO 2026" / "GEOLOGIA ESTRUCTURAL",
    C.FALLAS_DIR / "FERRARI 2003" / "Fallas",
    C.FALLAS_DIR / "MUÑOZ 2024" / "Fallas",
]

# Campos de la tabla de atributos que contienen el TIPO de rasgo estructural.
# (Corbo usa 'TIPO'; Ferrari y Muñoz usan 'Tipo'.)
CAMPOS_TIPO = ("TIPO", "Tipo")

# Tipos de rasgo a EXCLUIR del análisis de fallas.
# El borde de caldera inferido NO es una falla con permeabilidad, así que no
# debe generar zona de daño ni aportar favorabilidad. Comparación sin distinguir
# mayúsculas/acentos. (Ferrari 2003 lo cataloga como 'Borde Inferido' y 'Caldera'.)
TIPOS_EXCLUIDOS = ("borde inferido", "caldera")

# Buffers de la zona de daño de fallas (distancia euclidiana, metros)
BUFFER_ALTA = 100      # ≤ 100 m  → favorabilidad plena (zona de daño)
BUFFER_MODERADA = 200  # 100–200 m → decaimiento suave hacia 0
# > 200 m → favorabilidad 0 por fallas

# Umbrales de resistividad (ventana del yacimiento) desde config.py
RES_YAC_MIN = C.UMBRALES_RESISTIVIDAD["yacimiento_min"]  # 20
RES_YAC_MAX = C.UMBRALES_RESISTIVIDAD["yacimiento_max"]  # 50

# Ancho de la rampa/halo de transición a cada lado de la ventana (Ω·m).
# Score 8 = halo simétrico [20-rampa, 20) y (50, 50+rampa]; fuera de él la
# pertenencia cae a 0. Con rampa=5: halo = 15–20 y 50–55 Ω·m.
RES_RAMPA = C.UMBRALES_RESISTIVIDAD["rampa"]  # 5

# Rango de la escala de color de resistividad (para el plot continuo)
RHO_MIN, RHO_MAX = 1.0, 1000.0

# Suavizado del mapa de favorabilidad continua (sigma en metros).
# Reduce los escalones sin borrar la estructura. 0 = sin suavizar.
SUAVIZADO_M = 90.0

# Factor de sobre-muestreo para el render final (malla más fina => menos "pixel").
UPSAMPLE = 4

DPI = 220


# =============================================================================
# LECTURA DE DATOS
# =============================================================================

def leer_resistividad():
    """Lee el raster de resistividad y devuelve (array, transform, extent, meta)."""
    with rasterio.open(RESISTIVIDAD_TIF) as ds:
        rho = ds.read(1).astype(np.float64)
        transform = ds.transform
        bounds = ds.bounds
        shape = ds.shape
        nodata = ds.nodata
    if nodata is not None and not np.isnan(nodata):
        rho[rho == nodata] = np.nan
    extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
    return rho, transform, extent, shape, bounds


def _normaliza(texto):
    """Minúsculas y sin espacios extra, para comparar tipos de forma robusta."""
    return str(texto).strip().lower() if texto is not None else ""


def _tipo_del_registro(rec, fields):
    """Devuelve el valor del campo de tipo (TIPO/Tipo) del registro, o ''."""
    d = dict(zip(fields, list(rec)))
    for campo in CAMPOS_TIPO:
        if campo in d:
            return d[campo]
    return ""


def leer_lineas_fallas():
    """Lee las trazas de fallas de los shapefiles, EXCLUYENDO los tipos de
    TIPOS_EXCLUIDOS (borde de caldera inferido, etc.).
    Devuelve dict {fuente: [arrays Nx2 (x, y en UTM 13N)]}."""
    por_fuente = {}
    for shp in FALLAS_SHP:
        fuente = shp.parent.name
        lineas = []
        excluidas = 0
        try:
            r = shapefile.Reader(str(shp))
        except Exception as e:
            print(f"  ! No se pudo leer {fuente}: {e}")
            por_fuente[fuente] = []
            continue

        fields = [f[0] for f in r.fields[1:]]
        shapes = r.shapes()
        records = r.records()

        for shape_rec, rec in zip(shapes, records):
            tipo = _normaliza(_tipo_del_registro(rec, fields))
            if tipo in TIPOS_EXCLUIDOS:
                excluidas += 1
                continue  # ignorar borde de caldera inferido
            pts = np.asarray(shape_rec.points, dtype=np.float64)
            parts = list(shape_rec.parts) + [len(pts)]
            for i in range(len(parts) - 1):
                seg = pts[parts[i]:parts[i + 1]]
                if len(seg) >= 2:
                    lineas.append(seg)

        por_fuente[fuente] = lineas
        extra = f" ({excluidas} excluidas: borde/caldera)" if excluidas else ""
        print(f"  {fuente}: {len(lineas)} trazas{extra}")
    return por_fuente


# =============================================================================
# RASTERIZACIÓN Y DISTANCIAS
# =============================================================================

def world_to_pixel(x, y, transform):
    """Convierte coordenadas mundo a índices (col, row) de píxel."""
    col = (x - transform.c) / transform.a
    row = (y - transform.f) / transform.e
    return col, row


def rasterizar_lineas(por_fuente, shape, transform):
    """Quema las líneas de fallas en una máscara booleana (True = píxel con falla)."""
    nrows, ncols = shape
    mask = np.zeros((nrows, ncols), dtype=bool)

    for lineas in por_fuente.values():
        for seg in lineas:
            cols, rows = world_to_pixel(seg[:, 0], seg[:, 1], transform)
            # Rasterizar cada tramo con muestreo denso (algoritmo simple de línea)
            for k in range(len(seg) - 1):
                c0, r0 = cols[k], rows[k]
                c1, r1 = cols[k + 1], rows[k + 1]
                n = int(max(abs(c1 - c0), abs(r1 - r0)) * 2) + 1
                cc = np.linspace(c0, c1, n).round().astype(int)
                rr = np.linspace(r0, r1, n).round().astype(int)
                ok = (rr >= 0) & (rr < nrows) & (cc >= 0) & (cc < ncols)
                mask[rr[ok], cc[ok]] = True
    return mask


def distancia_a_fallas(mask, pixel_size):
    """Distancia euclidiana (en metros) de cada píxel a la falla más cercana."""
    # distance_transform_edt mide distancia a los píxeles False (fondo);
    # queremos distancia a los True (fallas), así que invertimos.
    dist_px = ndimage.distance_transform_edt(~mask)
    return dist_px * pixel_size


def remuestrear(arr, factor):
    """Sobre-muestrea un array por interpolación bilineal (spline orden 1).
       Produce una malla 'factor' veces más fina para un render sin escalones."""
    if factor is None or factor <= 1:
        return arr
    return ndimage.zoom(arr, factor, order=1, mode="nearest")


# =============================================================================
# FUNCIONES DE PERTENENCIA CONTINUA (FUZZY)  →  favorabilidad 0–1 suave
# =============================================================================
#
# En vez de reclasificar a scores discretos (0/8/10), cada capa devuelve un
# grado de favorabilidad CONTINUO en [0, 1]. Esto elimina los saltos abruptos
# y produce un gradiente físicamente interpretable.

def membresia_fallas(dist_m):
    """Favorabilidad continua por distancia a fallas.
       1.0 hasta BUFFER_ALTA (zona de daño), luego rampa lineal a 0 en BUFFER_MODERADA."""
    m = np.ones_like(dist_m, dtype=np.float64)
    # decaimiento lineal entre BUFFER_ALTA y BUFFER_MODERADA
    rampa = (BUFFER_MODERADA - dist_m) / (BUFFER_MODERADA - BUFFER_ALTA)
    zona_rampa = (dist_m > BUFFER_ALTA) & (dist_m <= BUFFER_MODERADA)
    m[zona_rampa] = rampa[zona_rampa]
    m[dist_m > BUFFER_MODERADA] = 0.0
    return np.clip(m, 0.0, 1.0)


def membresia_resistividad(rho):
    """Favorabilidad continua por resistividad (ventana suave del yacimiento).
       Vale 1 dentro de [20, 50] Ω·m y decae linealmente a 0 en ±RES_RAMPA.
       Devuelve NaN donde no hay dato."""
    m = np.full(rho.shape, np.nan, dtype=np.float64)
    valid = ~np.isnan(rho)
    r = rho.copy()

    val = np.zeros_like(r)
    # meseta central (yacimiento)
    dentro = (r >= RES_YAC_MIN) & (r <= RES_YAC_MAX)
    val[dentro] = 1.0
    # rampa inferior: de (RES_YAC_MIN - RES_RAMPA) hasta RES_YAC_MIN
    ramp_lo = (r < RES_YAC_MIN) & (r >= RES_YAC_MIN - RES_RAMPA)
    val[ramp_lo] = (r[ramp_lo] - (RES_YAC_MIN - RES_RAMPA)) / RES_RAMPA
    # rampa superior: de RES_YAC_MAX hasta (RES_YAC_MAX + RES_RAMPA)
    ramp_hi = (r > RES_YAC_MAX) & (r <= RES_YAC_MAX + RES_RAMPA)
    val[ramp_hi] = ((RES_YAC_MAX + RES_RAMPA) - r[ramp_hi]) / RES_RAMPA

    m[valid] = np.clip(val[valid], 0.0, 1.0)
    return m


# =============================================================================
# INDEX OVERLAY (continuo)
# =============================================================================

def calcular_index_overlay(memb_fallas, memb_resistividad, pixel_size):
    """Combina las membresías continuas ponderadas y normaliza a 0–1.

    S = Σ(mi · wi) / Σ wi        (mi ∈ [0,1])

    Con los datos disponibles hoy: fallas (w=7) y resistividad (w=9).
    Donde la resistividad es NaN, se usa solo la capa de fallas.
    Finalmente se aplica un suavizado gaussiano ligero para pulir escalones
    residuales del grid de resistividad.
    """
    w_f = C.PESOS["fallas"]
    w_r = C.PESOS["resistividad"]

    res_valida = ~np.isnan(memb_resistividad)

    num = np.where(res_valida,
                   memb_fallas * w_f + np.nan_to_num(memb_resistividad) * w_r,
                   memb_fallas * w_f)
    den = np.where(res_valida, float(w_f + w_r), float(w_f))

    favorabilidad = np.clip(num / den, 0.0, 1.0)

    if SUAVIZADO_M and SUAVIZADO_M > 0:
        sigma_px = SUAVIZADO_M / pixel_size
        favorabilidad = ndimage.gaussian_filter(favorabilidad, sigma=sigma_px, mode="nearest")
        favorabilidad = np.clip(favorabilidad, 0.0, 1.0)

    return favorabilidad


# =============================================================================
# MAPAS
# =============================================================================

def _fondo_area(ax, extent):
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])
    ax.set_xlabel("Easting (m) — UTM 13N")
    ax.set_ylabel("Northing (m) — UTM 13N")
    ax.ticklabel_format(style="plain")
    ax.set_aspect("equal")


def mapa_1_fallas_zona_dano(por_fuente, dist_m, extent):
    """Mapa 1: fallas + zona de daño (buffer configurable)."""
    print(f"Mapa 1: Fallas + zona de daño (buffer {BUFFER_ALTA:.0f} m)...")
    fig, ax = plt.subplots(figsize=(9, 11))

    # Zona de daño como campo de distancia clasificado
    zonas = np.full(dist_m.shape, 0, dtype=int)
    zonas[dist_m <= BUFFER_MODERADA] = 1  # halo transición BUFFER_ALTA–BUFFER_MODERADA
    zonas[dist_m <= BUFFER_ALTA] = 2      # zona de daño ≤ BUFFER_ALTA

    cmap = ListedColormap(["#f7f7f7", "#fdd0a2", "#e6550d"])
    norm = BoundaryNorm([0, 1, 2, 3], cmap.N)
    ax.imshow(zonas, cmap=cmap, norm=norm, extent=extent, origin="upper", alpha=0.85)

    # Trazas de fallas por fuente
    colores = {"CORBO 2026": "#08519c", "FERRARI 2003": "#54278f", "MUÑOZ 2024": "#006d2c"}
    for fuente, lineas in por_fuente.items():
        col = colores.get(fuente, "black")
        for i, seg in enumerate(lineas):
            ax.plot(seg[:, 0], seg[:, 1], color=col, lw=1.4,
                    label=fuente if i == 0 else None)

    _fondo_area(ax, extent)
    ax.set_title(f"Fallas principales y zona de daño (buffer {BUFFER_ALTA:.0f} m)\nDomo San Pedro")

    leg_zonas = [
        Patch(facecolor="#e6550d", label=f"Zona de daño ≤ {BUFFER_ALTA:.0f} m (Score 10)"),
        Patch(facecolor="#fdd0a2", label=f"Transición {BUFFER_ALTA:.0f}–{BUFFER_MODERADA:.0f} m (Score 8)"),
    ]
    leg_fallas = [Line2D([0], [0], color=colores[f], lw=1.6, label=f)
                  for f in por_fuente if por_fuente[f]]
    ax.legend(handles=leg_zonas + leg_fallas, loc="upper right", fontsize=8, framealpha=0.9)

    out = OUTPUTS_DIR / "fallas_zona_dano_UTM13N.png"
    fig.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Guardado: {out}")


def mapa_2_resistividad(rho, extent):
    """Mapa 2: resistividad MT, corte 350 mbsl (se mantiene igual)."""
    print("Mapa 2: Resistividad MT 350 mbsl — ventana del reservorio...")
    fig, ax = plt.subplots(figsize=(9, 11))

    # Fondo tenue en escala de grises con TODA la resistividad (contexto)
    ax.imshow(np.log10(np.where(np.isnan(rho), np.nan, rho)),
              cmap="Greys", extent=extent, origin="upper",
              vmin=np.log10(RHO_MIN), vmax=np.log10(RHO_MAX), alpha=0.35)

    # Resaltar SOLO la ventana del reservorio (20–50 Ω·m)
    ventana = (rho >= RES_YAC_MIN) & (rho <= RES_YAC_MAX)
    reservorio = np.where(ventana, rho, np.nan)
    im = ax.imshow(reservorio, cmap="autumn_r", extent=extent, origin="upper",
                   vmin=RES_YAC_MIN, vmax=RES_YAC_MAX)

    _fondo_area(ax, extent)
    ax.set_title(f"Resistividad MT — corte 350 mbsl\n"
                 f"Ventana del reservorio resaltada ({RES_YAC_MIN}–{RES_YAC_MAX} Ω·m)")
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label(f"Resistividad del reservorio ({RES_YAC_MIN}–{RES_YAC_MAX} Ω·m)")

    leg = [
        Patch(facecolor="#ff7f0e", label=f"Reservorio ({RES_YAC_MIN}–{RES_YAC_MAX} Ω·m)"),
        Patch(facecolor="#bdbdbd", label="Fuera de ventana (sello / roca fría)"),
    ]
    ax.legend(handles=leg, loc="upper right", fontsize=8, framealpha=0.9)

    out = OUTPUTS_DIR / "resistividad_MT_350mbsl_UTM13N.png"
    fig.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Guardado: {out}")


def mapa_3_index_overlay(favorabilidad, extent):
    """Mapa 3: favorabilidad continua Index Overlay (0–1)."""
    print("Mapa 3: Index Overlay — favorabilidad continua (0–1)...")
    fig, ax = plt.subplots(figsize=(9, 11))
    im = ax.imshow(favorabilidad, cmap="RdYlGn", vmin=0, vmax=1,
                   extent=extent, origin="upper", interpolation="bilinear")
    # Contornos de los umbrales de decisión (sobre la malla fina, ya suave)
    ny, nx = favorabilidad.shape
    xs = np.linspace(extent[0], extent[1], nx)
    ys = np.linspace(extent[3], extent[2], ny)
    X, Y = np.meshgrid(xs, ys)
    cs = ax.contour(X, Y, favorabilidad, levels=[C.UMBRAL_MODERADO, C.UMBRAL_FAVORABLE],
                    colors=["k", "k"], linewidths=[0.8, 1.4], linestyles=["--", "-"])
    ax.clabel(cs, fmt={C.UMBRAL_MODERADO: "0.6", C.UMBRAL_FAVORABLE: "0.7"}, fontsize=8)

    _fondo_area(ax, extent)
    ax.set_title("Favorabilidad geotérmica — Index Overlay (gradiente 0–1)\n"
                 f"Buffer fallas {BUFFER_ALTA:.0f} m | "
                 f"Resistividad yacimiento {RES_YAC_MIN:.0f}–{RES_YAC_MAX:.0f} Ω·m")
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Favorabilidad (0–1)")

    out = OUTPUTS_DIR / "index_overlay_gradiente_UTM13N.png"
    fig.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Guardado: {out}")


def mapa_4_booleano(favorabilidad, extent):
    """Mapa 4: modelo booleano (favorable / no favorable) con umbral 0.6."""
    print("Mapa 4: Modelo booleano de favorabilidad...")
    fig, ax = plt.subplots(figsize=(9, 11))

    boolean = np.zeros_like(favorabilidad, dtype=int)
    boolean[favorabilidad >= C.UMBRAL_MODERADO] = 1   # favorable ≥0.6
    boolean[favorabilidad >= C.UMBRAL_FAVORABLE] = 2  # alta prioridad ≥0.7

    cmap = ListedColormap(["#d9d9d9", "#a1d99b", "#238b45"])
    norm = BoundaryNorm([0, 1, 2, 3], cmap.N)
    ax.imshow(boolean, cmap=cmap, norm=norm, extent=extent, origin="upper",
              interpolation="nearest")

    _fondo_area(ax, extent)
    ax.set_title("Modelo booleano de favorabilidad geotérmica\n"
                 "Domo San Pedro (umbrales 0.6 / 0.7)")

    leg = [
        Patch(facecolor="#238b45", label=f"Alta prioridad (≥ {C.UMBRAL_FAVORABLE})"),
        Patch(facecolor="#a1d99b", label=f"Favorable ({C.UMBRAL_MODERADO}–{C.UMBRAL_FAVORABLE})"),
        Patch(facecolor="#d9d9d9", label=f"No favorable (< {C.UMBRAL_MODERADO})"),
    ]
    ax.legend(handles=leg, loc="upper right", fontsize=8, framealpha=0.9)

    out = OUTPUTS_DIR / "modelo_booleano_UTM13N.png"
    fig.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Guardado: {out}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 64)
    print("  GENERACIÓN DE MAPAS — Index Overlay Domo San Pedro")
    print(f"  Buffer fallas: {BUFFER_ALTA:.0f} m | "
          f"Resistividad yacimiento: {RES_YAC_MIN:.0f}–{RES_YAC_MAX:.0f} Ω·m")
    print("=" * 64)

    if not RESISTIVIDAD_TIF.exists():
        print(f"ERROR: no se encontró {RESISTIVIDAD_TIF}")
        sys.exit(1)

    print("\nLeyendo resistividad...")
    rho, transform, extent, shape, bounds = leer_resistividad()
    pixel_size = abs(transform.a)
    print(f"  Raster: {shape[1]}x{shape[0]} px | pixel {pixel_size:.1f} m")
    print(f"  Extent: E {bounds.left:.0f}-{bounds.right:.0f}, N {bounds.bottom:.0f}-{bounds.top:.0f}")

    print("\nLeyendo fallas...")
    por_fuente = leer_lineas_fallas()

    print("\nRasterizando fallas y calculando distancias...")
    mask = rasterizar_lineas(por_fuente, shape, transform)
    dist_m = distancia_a_fallas(mask, pixel_size)
    print(f"  Píxeles con falla: {mask.sum():,}")

    print("\nCalculando membresías continuas (fuzzy)...")
    memb_fallas = membresia_fallas(dist_m)
    memb_res = membresia_resistividad(rho)

    print("Calculando Index Overlay continuo...")
    favorabilidad = calcular_index_overlay(memb_fallas, memb_res, pixel_size)

    # Malla fina para render suave (interpolación bilineal)
    fav_fina = remuestrear(favorabilidad, UPSAMPLE)

    print("\nGenerando mapas...")
    mapa_1_fallas_zona_dano(por_fuente, dist_m, extent)
    mapa_2_resistividad(rho, extent)
    mapa_3_index_overlay(fav_fina, extent)
    mapa_4_booleano(fav_fina, extent)

    print("\n" + "=" * 64)
    print("  COMPLETADO — 4 mapas en:", OUTPUTS_DIR)
    print("=" * 64)


if __name__ == "__main__":
    main()
