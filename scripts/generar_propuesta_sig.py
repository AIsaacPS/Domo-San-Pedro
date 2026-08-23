"""
generar_propuesta_sig.py
=========================
Genera el documento Word de propuesta de proyecto para la clase de SIG.

USO:
    python scripts/generar_propuesta_sig.py

SALIDA:
    outputs/Propuesta_Proyecto_SIG_Domo_San_Pedro.docx
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "Propuesta_Proyecto_SIG_Domo_San_Pedro.docx"

# Colores del documento
COLOR_UNAM_AZUL = RGBColor(0x00, 0x2B, 0x5C)  # Azul UNAM oscuro
COLOR_UNAM_ORO = RGBColor(0xB5, 0x85, 0x0B)   # Dorado UNAM
COLOR_GRIS = RGBColor(0x44, 0x44, 0x44)
COLOR_GRIS_CLARO = RGBColor(0x66, 0x66, 0x66)


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def set_cell_shading(cell, color_hex):
    """Aplica color de fondo a una celda."""
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), color_hex)
    shading.set(qn("w:val"), "clear")
    cell._tc.get_or_add_tcPr().append(shading)


def add_horizontal_rule(doc):
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "4")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "002B5C")
    pBdr.append(bottom)
    pPr.append(pBdr)


def styled_heading(doc, text, level=1, color=COLOR_UNAM_AZUL):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = color
    return h


# ---------------------------------------------------------------------------
# CONTENIDO DEL DOCUMENTO
# ---------------------------------------------------------------------------

def build_doc():
    doc = Document()

    # Márgenes
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)

    # ══════════════════════════════════════════════════════════════════════
    # PORTADA
    # ══════════════════════════════════════════════════════════════════════

    # Encabezado institucional
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO")
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = COLOR_UNAM_AZUL

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Facultad de Ingeniería")
    r.font.size = Pt(11)
    r.font.color.rgb = COLOR_UNAM_AZUL
    p.add_run("\n")
    r2 = p.add_run("Especialización en Exploración y Aprovechamiento\nde Recursos Geotérmicos")
    r2.font.size = Pt(10)
    r2.font.color.rgb = COLOR_GRIS

    doc.add_paragraph()
    add_horizontal_rule(doc)
    doc.add_paragraph()

    # Título del proyecto
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.space_after = Pt(6)
    r = p.add_run("PROPUESTA DE PROYECTO")
    r.font.size = Pt(10)
    r.font.color.rgb = COLOR_GRIS_CLARO
    r.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.space_after = Pt(4)
    r = p.add_run("Determinación de Zonas Favorables\npara Perforación Geotérmica")
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = COLOR_UNAM_AZUL

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Método Index Overlay Multi-Clase aplicado al\nDomo San Pedro, Nayarit, México")
    r.font.size = Pt(12)
    r.font.italic = True
    r.font.color.rgb = COLOR_GRIS

    doc.add_paragraph()
    doc.add_paragraph()

    # Datos del alumno y curso
    table = doc.add_table(rows=4, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    data = [
        ("Materia:", "Sistemas de Información Geográfica (SIG)"),
        ("Profesor:", "Dr. Marco Antonio Torres Vera"),
        ("Alumno:", "A. Isaac P.S."),
        ("Semestre:", "2026-2"),
    ]
    for i, (label, value) in enumerate(data):
        cell_l = table.cell(i, 0)
        cell_r = table.cell(i, 1)
        cell_l.paragraphs[0].runs.clear() if cell_l.paragraphs[0].runs else None
        rl = cell_l.paragraphs[0].add_run(label)
        rl.font.bold = True
        rl.font.size = Pt(10)
        rl.font.color.rgb = COLOR_UNAM_AZUL
        rr = cell_r.paragraphs[0].add_run(value)
        rr.font.size = Pt(10)
        rr.font.color.rgb = COLOR_GRIS

    doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════════
    # 1. INTRODUCCIÓN
    # ══════════════════════════════════════════════════════════════════════

    styled_heading(doc, "1. Introducción", level=1)

    doc.add_paragraph(
        "El campo geotérmico Domo San Pedro se localiza en el municipio de "
        "San Pedro Lagunillas, Nayarit, dentro del rift Tepic-Zacoalco en "
        "el extremo occidental de la Faja Volcánica Transmexicana. Este sistema "
        "geotérmico de temperatura intermedia-alta (200–240 °C estimados por "
        "geotermometría) presenta manifestaciones termales superficiales activas "
        "y ha sido objeto de exploración por parte de la CFE desde la década de 1980."
    )
    doc.add_paragraph(
        "A pesar de contar con múltiples estudios geocientíficos (geoquímica, "
        "geología estructural, magnetotelúrica, sismicidad), no se ha realizado "
        "una integración formal de estas capas de información mediante técnicas "
        "de análisis espacial en SIG para delimitar las zonas óptimas de perforación. "
        "Este proyecto busca llenar ese vacío aplicando el método Index Overlay "
        "Multi-Clase (Prol-Ledesma, 2000)."
    )

    # ══════════════════════════════════════════════════════════════════════
    # 2. OBJETIVOS
    # ══════════════════════════════════════════════════════════════════════

    styled_heading(doc, "2. Objetivos", level=1)

    styled_heading(doc, "2.1 Objetivo General", level=2)
    doc.add_paragraph(
        "Generar un mapa de favorabilidad geotérmica del área del Domo San Pedro "
        "mediante la integración de datos geocientíficos multi-capa en un SIG, "
        "aplicando el método Index Overlay Multi-Clase, con el fin de identificar "
        "y priorizar zonas para la perforación de pozos exploratorios."
    )

    styled_heading(doc, "2.2 Objetivos Particulares", level=2)
    objetivos = [
        "Compilar y homogeneizar las capas de información geocientífica disponibles "
        "(fallas, manifestaciones termales, geología, fracturamiento y resistividad) "
        "en un sistema de referencia común (EPSG:32613, UTM Zona 13N).",

        "Generar mapas de distancia euclidiana a los rasgos geológicos y "
        "geotérmicos relevantes (fallas, manifestaciones, contactos de domos).",

        "Reclasificar cada capa temática en tres categorías de favorabilidad "
        "(alta, moderada, no favorable) según los umbrales establecidos por el "
        "modelo conceptual del sistema.",

        "Aplicar la fórmula del Index Overlay ponderado para obtener un mapa "
        "continuo de favorabilidad (escala 0–1) que integre la contribución "
        "de cada evidencia según su peso relativo.",

        "Validar el resultado comparando las zonas de máxima favorabilidad "
        "con la ubicación de pozos exploratorios existentes y datos de "
        "gradiente geotérmico conocidos.",

        "Realizar un análisis de sensibilidad variando los pesos asignados "
        "a cada capa para evaluar la robustez del modelo.",
    ]
    for obj in objetivos:
        p = doc.add_paragraph(obj, style="List Bullet")
        p.paragraph_format.space_after = Pt(4)

    # ══════════════════════════════════════════════════════════════════════
    # 3. METODOLOGÍA
    # ══════════════════════════════════════════════════════════════════════

    styled_heading(doc, "3. Metodología", level=1)

    doc.add_paragraph(
        "Se empleará el método Index Overlay Multi-Clase (Prol-Ledesma, 2000), "
        "un enfoque knowledge-driven que integra múltiples capas de evidencia "
        "geocientífica. Cada capa recibe un peso (importancia relativa) y un "
        "puntaje por clase (proximidad a la evidencia). El puntaje de favorabilidad "
        "para cada píxel se calcula como:"
    )

    # Fórmula
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.space_before = Pt(8)
    p.space_after = Pt(8)
    r = p.add_run("S = Σ(Sᵢⱼ × wᵢ) / Σ(wᵢ)")
    r.font.size = Pt(12)
    r.font.italic = True
    r.font.color.rgb = COLOR_UNAM_AZUL

    # Tabla de capas y pesos
    styled_heading(doc, "3.1 Capas temáticas y pesos", level=2)

    table = doc.add_table(rows=6, cols=4)
    table.style = "Table Grid"
    headers = ["Capa", "Dominio", "Peso", "Fuente"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.paragraphs[0].add_run(h).bold = True
        set_cell_shading(cell, "002B5C")
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].runs[0].font.size = Pt(9)

    rows_data = [
        ("Resistividad eléctrica (MT)", "Profundidad", "9", "Corbo et al. (2026)"),
        ("Fallas principales", "Subsuperficial", "7", "Ferrari (2003), Corbo (2026)"),
        ("Manifestaciones termales", "Superficial", "5", "Viggiano-Guerra (1994)"),
        ("Geología (domos/intrusivos)", "Superficial", "5", "SGM + Ferrari (2003)"),
        ("Fracturamiento superficial", "Superficial", "5", "Interpretación satelital"),
    ]
    for i, row in enumerate(rows_data):
        for j, val in enumerate(row):
            cell = table.cell(i + 1, j)
            r = cell.paragraphs[0].add_run(val)
            r.font.size = Pt(9)

    doc.add_paragraph()

    # Flujo de trabajo
    styled_heading(doc, "3.2 Flujo de trabajo", level=2)
    fases = [
        "Recopilación y homogeneización de datos (CRS: EPSG:32613, resolución: 30 m)",
        "Cálculo de mapas de distancia euclidiana a cada rasgo geológico",
        "Reclasificación en tres clases: ≤100 m (Score 10), 100–200 m (Score 8), >200 m (Score 0)",
        "Cálculo del Index Overlay ponderado",
        "Generación de mapas de favorabilidad con umbrales de decisión (>0.6, >0.7)",
        "Validación y análisis de sensibilidad",
    ]
    for fase in fases:
        doc.add_paragraph(fase, style="List Number")

    # ══════════════════════════════════════════════════════════════════════
    # 4. ÁREA DE ESTUDIO
    # ══════════════════════════════════════════════════════════════════════

    styled_heading(doc, "4. Área de Estudio", level=1)

    doc.add_paragraph(
        "El área de estudio se define como un rectángulo de 15 × 20 km (300 km²) "
        "centrado en el Domo San Pedro, en el municipio de San Pedro Lagunillas, "
        "Nayarit. Las coordenadas en UTM Zona 13N son:"
    )

    table = doc.add_table(rows=5, cols=2)
    table.style = "Table Grid"
    coords = [
        ("XMIN (Easting)", "520,000 m"),
        ("XMAX (Easting)", "535,000 m"),
        ("YMIN (Northing)", "2,328,000 m"),
        ("YMAX (Northing)", "2,348,000 m"),
        ("CRS", "EPSG:32613 (WGS 84 / UTM Zona 13N)"),
    ]
    for i, (k, v) in enumerate(coords):
        table.cell(i, 0).paragraphs[0].add_run(k).bold = True
        table.cell(i, 0).paragraphs[0].runs[0].font.size = Pt(9)
        table.cell(i, 1).paragraphs[0].add_run(v).font.size = Pt(9)

    # ══════════════════════════════════════════════════════════════════════
    # 5. HERRAMIENTAS
    # ══════════════════════════════════════════════════════════════════════

    styled_heading(doc, "5. Software y Herramientas", level=1)

    table = doc.add_table(rows=4, cols=2)
    table.style = "Table Grid"
    tools = [
        ("QGIS 3.34", "Digitalización, análisis espacial, geoprocesamiento"),
        ("Python (NumPy, Rasterio)", "Automatización del pipeline y cálculo del modelo"),
        ("PyQGIS + Processing", "Scripts de preprocesamiento dentro de QGIS"),
        ("Git + GitHub", "Control de versiones y reproducibilidad"),
    ]
    for i, (tool, uso) in enumerate(tools):
        r1 = table.cell(i, 0).paragraphs[0].add_run(tool)
        r1.bold = True
        r1.font.size = Pt(9)
        table.cell(i, 1).paragraphs[0].add_run(uso).font.size = Pt(9)

    # ══════════════════════════════════════════════════════════════════════
    # 6. RESULTADOS ESPERADOS
    # ══════════════════════════════════════════════════════════════════════

    styled_heading(doc, "6. Resultados Esperados", level=1)

    resultados = [
        "Mapa continuo de favorabilidad geotérmica (escala 0–1) del área del Domo San Pedro.",
        "Delimitación de zonas prioritarias para perforación exploratoria (favorabilidad > 0.7).",
        "Análisis de sensibilidad de los pesos del modelo.",
        "Repositorio reproducible con código, documentación y pipeline automatizado.",
    ]
    for r in resultados:
        doc.add_paragraph(r, style="List Bullet")

    # ══════════════════════════════════════════════════════════════════════
    # 7. BIBLIOGRAFÍA
    # ══════════════════════════════════════════════════════════════════════

    doc.add_page_break()
    styled_heading(doc, "7. Bibliografía", level=1)

    categorias = [
        {
            "titulo": "Metodología GIS — Index Overlay",
            "refs": [
                "Prol-Ledesma, R.M. (2000). Evaluation of the reconnaissance results in geothermal exploration using GIS. Geothermics, 29, 83–103.",
                "Bonham-Carter, G.F. (1994). Geographical Information Systems for Geoscientists: Modelling with GIS. Pergamon, 398 pp.",
            ],
        },
        {
            "titulo": "Geoquímica — Manifestaciones Superficiales",
            "refs": [
                "Viggiano-Guerra, J.C. & Rocha-López, V.M. (1994). Geochemistry of thermal waters in the Domo San Pedro geothermal area. Geothermics, 23(2), 149–163.",
                "Tello-Hinojosa, E. (1992). Geochemical study of the San Pedro Lagunillas geothermal field. Proc. 17th Workshop on Geothermal Reservoir Engineering, Stanford.",
            ],
        },
        {
            "titulo": "Geología Estructural",
            "refs": [
                "Ferrari, L. et al. (2003). Late Miocene to Quaternary extensional tectonics and volcanic activity in the Tepic-Zacoalco rift. GSA Special Papers, 374, 275–297.",
                "Sieron, K. & Siebe, C. (2008). Revised stratigraphy and eruption rates of Ceboruco stratovolcano. J. Volcanol. Geotherm. Res., 176(2), 241–264.",
            ],
        },
        {
            "titulo": "Geofísica — Magnetotelúrica",
            "refs": [
                "Corbo-Camargo, F. et al. (2026). Magnetotelluric imaging of the Domo San Pedro geothermal system. GSA Books (en prensa).",
                "Arzate, J.A. et al. (2000). Magnetotelluric study of the San Pedro Lagunillas geothermal field. Proc. World Geothermal Congress 2000, pp. 1535–1540.",
                "Flores-Armenta, M. et al. (1995). Geophysical exploration of the San Pedro Lagunillas geothermal field. Proc. WGC 1995, pp. 895–900.",
            ],
        },
        {
            "titulo": "Sismicidad",
            "refs": [
                "Núñez-Cornú, F.J. et al. (2002). Seismicity in the region of Jalisco-Nayarit-Colima, Mexico. Seismol. Res. Lett., 73(6), 939–951.",
            ],
        },
        {
            "titulo": "Hidrogeología",
            "refs": [
                "CONAGUA (2015). Actualización de la disponibilidad media anual de agua en el acuífero San Pedro Lagunillas (1803). DOF, 20 de abril de 2015.",
            ],
        },
    ]

    for cat in categorias:
        p = doc.add_paragraph()
        p.space_before = Pt(10)
        r = p.add_run(cat["titulo"])
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_UNAM_AZUL

        for ref in cat["refs"]:
            p_ref = doc.add_paragraph(style="List Bullet")
            p_ref.paragraph_format.left_indent = Inches(0.3)
            p_ref.paragraph_format.space_after = Pt(2)
            r = p_ref.add_run(ref)
            r.font.size = Pt(9)
            r.font.color.rgb = COLOR_GRIS

    # ══════════════════════════════════════════════════════════════════════
    # GUARDAR
    # ══════════════════════════════════════════════════════════════════════

    doc.save(str(OUTPUT_FILE))
    print(f"Documento generado: {OUTPUT_FILE}")
    return OUTPUT_FILE


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    build_doc()
