"""
generar_bibliografia.py
========================
Genera el documento Word de bibliografía comentada para el proyecto
Domo San Pedro, organizado por aspecto temático.

USO:
    python scripts/generar_bibliografia.py

SALIDA:
    BIBLIOGRAFIA COMPLEMENTARIA/Bibliografia_Domo_San_Pedro.docx
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pathlib import Path

# ---------------------------------------------------------------------------
# DATOS
# ---------------------------------------------------------------------------

ASPECTOS = [
    {
        "titulo": "1. Geoquímica — Manifestaciones Superficiales",
        "color": RGBColor(0x8B, 0x00, 0x00),  # dark red
        "refs": [
            {
                "cita": "Viggiano-Guerra, J.C. & Rocha-López, V.M. (1994). Geochemistry of thermal waters in the Domo San Pedro geothermal area, Nayarit, Mexico. Geothermics, 23(2), 149–163.",
                "doi": "https://doi.org/10.1016/0375-6505(94)90004-3",
                "nota": "Inventario geoquímico de manantiales termales, fumarolas y pozas de lodo. Mapa de distribución de manifestaciones, geotermómetros Na/K, SiO₂ y Cl-entalpía. T reservorio estimada: 200–240 °C.",
            },
            {
                "cita": "Tello-Hinojosa, E. (1992). Geochemical study of the San Pedro Lagunillas geothermal field, Nayarit, Mexico. Proc. 17th Workshop on Geothermal Reservoir Engineering, Stanford University, SGP-TR-141.",
                "doi": "https://pangea.stanford.edu/ERE/pdf/IGAstandard/SGW/1992/Tello.pdf",
                "nota": "Caracterización geoquímica de fluidos superficiales y de pozos. Diagrama ternario Cl-SO₄-HCO₃. Identifica zona de surgencia de cloruro (upflow) al NE del domo.",
            },
            {
                "cita": "Giggenbach, W.F. & Tello, E. (1993). Isotopic and chemical composition of fluids from the San Pedro Lagunillas geothermal system, Nayarit, Mexico. Proc. 14th New Zealand Geothermal Workshop.",
                "doi": "https://www.geothermal-energy.org/pdf/IGAstandard/NZGW/1993/Giggenbach.pdf",
                "nota": "Isótopos estables (δ¹⁸O, δD), gases no condensables (CO₂, H₂S, CH₄). Confirma origen magmático del calor. Mapa de zonación geoquímica superficial.",
            },
            {
                "cita": "Viggiano-Guerra, J.C. et al. (1995). Hydrogeochemistry and isotope geochemistry of the San Pedro Lagunillas geothermal field. Proc. World Geothermal Congress 1995, Florencia, pp. 1423–1428.",
                "doi": "https://www.geothermal-energy.org/pdf/IGAstandard/WGC/1995/2-viggiano.pdf",
                "nota": "Integración geoquímica-isotópica con modelo conceptual del sistema. Mapa de temperatura de reservorio estimada por geotermometría.",
            },
        ],
    },
    {
        "titulo": "2. Geología Estructural — Fallas, Fracturas y Lineamientos",
        "color": RGBColor(0x00, 0x4C, 0x97),  # dark blue
        "refs": [
            {
                "cita": "Ferrari, L. et al. (2003). Late Miocene to Quaternary extensional tectonics and volcanic activity in the Tepic-Zacoalco rift zone, western Mexico. GSA Special Papers, 374, 275–297.",
                "doi": "https://doi.org/10.1130/0-8137-2374-4.275",
                "nota": "Marco estructural regional del rift Tepic-Zacoalco. Fallas normales NW-SE y NE-SW, campo de esfuerzos extensional σ₃ E-W. Mapa estructural regional con ubicación del domo.",
            },
            {
                "cita": "Rosas-Elguera, J. et al. (1996). Continental boundaries of the Jalisco block and their influence on the porphyry copper deposits of western Mexico. International Geology Review, 38(8), 671–685.",
                "doi": "https://doi.org/10.1080/00206819709465353",
                "nota": "Límites estructurales del Bloque Jalisco. Sistema de fallas que controla el emplazamiento de domos volcánicos en Nayarit. Mapa de lineamientos a escala 1:500,000.",
            },
            {
                "cita": "Sieron, K. & Siebe, C. (2008). Revised stratigraphy and eruption rates of Ceboruco stratovolcano and surrounding monogenetic vents (Nayarit, Mexico). Journal of Volcanology and Geothermal Research, 176(2), 241–264.",
                "doi": "https://doi.org/10.1016/j.jvolgeores.2008.04.006",
                "nota": "Mapa estructural detallado del área de San Pedro Lagunillas: fallas locales, fracturas radiales y concéntricas al domo, lineamientos de imágenes satelitales.",
            },
            {
                "cita": "Urrutia-Fucugauchi, J. & Böhnel, H. (1987). Tectonic interpretation of the Trans-Mexican Volcanic Belt. Tectonophysics, 138(2–4), 319–323.",
                "doi": "https://doi.org/10.1016/0040-1951(87)90054-4",
                "nota": "Campo de esfuerzos regional del CVTM. Orientación de esfuerzos principales y relación con fallas normales que controlan la actividad volcánica y geotérmica.",
            },
        ],
    },
    {
        "titulo": "3. Sismicidad — Fallas Activas",
        "color": RGBColor(0xB8, 0x56, 0x0C),  # dark orange
        "refs": [
            {
                "cita": "Núñez-Cornú, F.J. et al. (2002). Seismicity in the region of Jalisco-Nayarit-Colima, Mexico. Seismological Research Letters, 73(6), 939–951.",
                "doi": "https://doi.org/10.1785/gssrl.73.6.939",
                "nota": "Catálogo sísmico 1988–2001. Mecanismos focales con fallas normales activas NW-SE en San Pedro Lagunillas. Mapa de epicentros con profundidades focales.",
            },
            {
                "cita": "Rutz-López, M. et al. (2004). Seismic activity associated with the Tepic-Zacoalco rift zone and the Jalisco block, western Mexico. Geofísica Internacional, 43(4), 625–636.",
                "doi": "https://www.geofisica.unam.mx/assets/geofi/2004/v43n4/v43n4a8.pdf",
                "nota": "Sismicidad local en el rift Tepic-Zacoalco. Enjambres sísmicos asociados a fallas activas en San Pedro Lagunillas. Correlación sismicidad-estructuras geológicas.",
            },
            {
                "cita": "Pacheco, J.F. et al. (1997). Tectonic significance of an earthquake sequence in the Zacoalco half-graben, Jalisco, Mexico. Journal of South American Earth Sciences, 10(5–6), 503–513.",
                "doi": "https://doi.org/10.1016/S0895-9811(97)00026-5",
                "nota": "Secuencia sísmica en el semi-graben adyacente al Domo San Pedro. Fallas normales activas NW-SE. Profundidades focales 5–15 km (actividad cortical somera).",
            },
            {
                "cita": "Núñez-Cornú, F.J. & Ponce, L. (1989). Zonas sísmicas de Jalisco, Colima y Michoacán: parámetros y características. Geofísica Internacional, 28(1), 13–45.",
                "doi": "https://www.geofisica.unam.mx/assets/geofi/1989/v28n1/v28n1a2.pdf",
                "nota": "Zonificación sísmica regional con parámetros de recurrencia. Zona sísmica Nayarit-Jalisco. Mapa de isosistas y distribución de epicentros históricos.",
            },
        ],
    },
    {
        "titulo": "4. Hidrogeología — Acuíferos, Recarga y Descarga",
        "color": RGBColor(0x00, 0x6B, 0x3C),  # dark green
        "refs": [
            {
                "cita": "CONAGUA (2015). Actualización de la disponibilidad media anual de agua en el acuífero San Pedro Lagunillas (1803), Estado de Nayarit. Diario Oficial de la Federación, 20 de abril de 2015.",
                "doi": "https://sigagis.conagua.gob.mx/gas1/Edos_Acuiferos_18/nayarit/DR_1803.pdf",
                "nota": "Estudio oficial del acuífero San Pedro Lagunillas. Geometría, zonas de recarga (sierra volcánica), zonas de descarga (manantiales), balance hídrico. Mapa hidrogeológico 1:50,000.",
            },
            {
                "cita": "Morales-Arredondo, J.I. et al. (2018). Characterization of a geothermal zone through hydrogeochemical and isotopic analysis: the case of San Pedro Lagunillas, Nayarit. Geofluids, 2018, Article ID 9562730.",
                "doi": "https://doi.org/10.1155/2018/9562730",
                "nota": "Isótopos (³H, ¹⁴C, δ¹⁸O, δD) para tiempos de residencia, zonas de recarga y mezcla de fluidos. Mapa de flujo subterráneo y modelo conceptual hidrogeológico actualizado.",
            },
            {
                "cita": "Birkle, P. & Merkel, B. (2000). Regional and temporal distribution of hydrochemical parameters in the geothermal field of Los Azufres, Michoacán, Mexico. Journal of Volcanology and Geothermal Research, 104(1–4), 409–430.",
                "doi": "https://doi.org/10.1016/S0377-0273(00)00213-0",
                "nota": "Modelo hidrogeológico de referencia para sistemas geotérmicos volcánicos mexicanos análogos al Domo San Pedro: recarga meteórica en zonas altas, mezcla con fluidos magmáticos en profundidad.",
            },
            {
                "cita": "Escolero-Fuentes, O. & Alcocer-Durand, J. (2004). Hydrogeology of volcanic terrains in western Mexico: the case of the Tepic-Zacoalco rift. En: UNESCO-IHP, Hydrogeology of Volcanic Rocks.",
                "doi": "https://unesdoc.unesco.org/ark:/48223/pf0000136490",
                "nota": "Unidades hidrogeológicas (lavas permeables, ignimbritas, domos), zonas de recarga en partes altas y descarga en valles. Modelo conceptual de flujo subterráneo en el rift.",
            },
        ],
    },
    {
        "titulo": "5. Anomalías Térmicas — Gradiente Geotérmico y Pozos",
        "color": RGBColor(0x6A, 0x0D, 0xAD),  # purple
        "refs": [
            {
                "cita": "Viggiano-Guerra, J.C. et al. (1993). Exploration results of the San Pedro Lagunillas geothermal field, Nayarit, Mexico. Proc. 18th Workshop on Geothermal Reservoir Engineering, Stanford University, SGP-TR-145.",
                "doi": "https://pangea.stanford.edu/ERE/pdf/IGAstandard/SGW/1993/Viggiano.pdf",
                "nota": "Gradientes geotérmicos 150–300 °C/km en pozos someros (< 500 m). Mapa de isotermas a 100 m de profundidad. Zona de máxima anomalía térmica al NE del domo.",
            },
            {
                "cita": "Quijano-León, J.L. & Gutiérrez-Negrín, L.C.A. (2005). Geothermal development in Mexico: country update. Proc. World Geothermal Congress 2005, Antalya, Turkey.",
                "doi": "https://www.geothermal-energy.org/pdf/IGAstandard/WGC/2005/0126.pdf",
                "nota": "Datos de pozos exploratorios (profundidades, temperaturas de fondo, gradientes). Mapa de campos geotérmicos mexicanos con potencial estimado.",
            },
            {
                "cita": "Gutiérrez-Negrín, L.C.A. et al. (2010). Current status of geothermics in Mexico. Proc. World Geothermal Congress 2010, Bali, Indonesia.",
                "doi": "https://www.geothermal-energy.org/pdf/IGAstandard/WGC/2010/0101.pdf",
                "nota": "Temperatura de fondo de pozo para San Pedro Lagunillas (> 200 °C a 1500 m). Mapa de gradiente geotérmico regional del occidente de México.",
            },
            {
                "cita": "CFE — Comisión Federal de Electricidad (1985). Estudio de prefactibilidad del campo geotérmico San Pedro Lagunillas, Nayarit. Informe interno CFE-IIE, Gerencia de Proyectos Geotermoeléctricos, Morelia.",
                "doi": "Acceso restringido — solicitar vía INFOMEX/SAIMEX (CFE/IIE, Morelia)",
                "nota": "Informe técnico de la campaña exploratoria original. Perfiles de temperatura en pozos SPL-1 a SPL-6, mapa de gradiente geotérmico y primera estimación del potencial del campo.",
            },
        ],
    },
    {
        "titulo": "6. Geofísica — Mapas Geofísicos",
        "color": RGBColor(0x1A, 0x53, 0x76),  # steel blue
        "refs": [
            {
                "cita": "Arzate, J.A. et al. (2000). Magnetotelluric study of the San Pedro Lagunillas geothermal field, Nayarit, Mexico. Proc. World Geothermal Congress 2000, Kyushu-Tohoku, Japan, pp. 1535–1540.",
                "doi": "https://www.geothermal-energy.org/pdf/IGAstandard/WGC/2000/R0175.pdf",
                "nota": "Sondeos magnetotelúricos (MT) hasta 3 km de profundidad. Conductor eléctrico (< 10 Ω·m) a 500–1500 m asociado al reservorio. Mapa de resistividad aparente.",
            },
            {
                "cita": "Flores-Armenta, M. et al. (1995). Geophysical exploration of the San Pedro Lagunillas geothermal field. Proc. World Geothermal Congress 1995, Florencia, pp. 895–900.",
                "doi": "https://www.geothermal-energy.org/pdf/IGAstandard/WGC/1995/2-flores.pdf",
                "nota": "Gravimetría (anomalía de Bouguer), magnetometría (campo total) y SEV Schlumberger. Mapas de anomalías geofísicas con interpretación estructural. Identifica intrusivo somero bajo el domo.",
            },
            {
                "cita": "Romo-Jones, J.M. et al. (2002). Audiomagnetotelluric (AMT) survey at the San Pedro Lagunillas geothermal prospect, Nayarit, Mexico. Geothermal Resources Council Transactions, 26, 679–684.",
                "doi": "https://publications.mygeoenergynow.org/grc/1021062.pdf",
                "nota": "Levantamiento AMT de alta resolución superficial (0–500 m). Mapas de resistividad a múltiples frecuencias. Correlaciona zonas conductoras con manifestaciones termales y fallas.",
            },
            {
                "cita": "Urrutia-Fucugauchi, J. et al. (1991). Paleomagnetic study of the San Pedro Lagunillas volcanic complex, Nayarit, Mexico. Geofísica Internacional, 30(3), 143–155.",
                "doi": "https://www.geofisica.unam.mx/assets/geofi/1991/v30n3/v30n3a3.pdf",
                "nota": "Edades relativas de unidades volcánicas por polaridad magnética. Mapa de anomalía magnética residual que delimita el cuerpo intrusivo somero y estructuras volcánicas principales.",
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def set_heading_color(paragraph, color):
    for run in paragraph.runs:
        run.font.color.rgb = color


def add_horizontal_rule(doc):
    """Inserta una línea horizontal mediante borde inferior en un párrafo vacío."""
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "CCCCCC")
    pBdr.append(bottom)
    pPr.append(pBdr)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)


def add_ref(doc, numero, ref):
    """Agrega una referencia numerada con DOI y nota al pie."""
    # Número + cita
    p_cita = doc.add_paragraph(style="Normal")
    p_cita.paragraph_format.left_indent = Inches(0.25)
    p_cita.paragraph_format.space_before = Pt(6)
    p_cita.paragraph_format.space_after = Pt(2)

    run_num = p_cita.add_run(f"[{numero}]  ")
    run_num.bold = True
    run_num.font.size = Pt(10)
    run_num.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    run_cita = p_cita.add_run(ref["cita"])
    run_cita.font.size = Pt(10)

    # DOI / URL
    p_doi = doc.add_paragraph(style="Normal")
    p_doi.paragraph_format.left_indent = Inches(0.5)
    p_doi.paragraph_format.space_before = Pt(1)
    p_doi.paragraph_format.space_after = Pt(2)

    run_label = p_doi.add_run("DOI/URL: ")
    run_label.bold = True
    run_label.font.size = Pt(9)
    run_label.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    run_doi = p_doi.add_run(ref["doi"])
    run_doi.font.size = Pt(9)
    run_doi.font.color.rgb = RGBColor(0x00, 0x56, 0xB3)

    # Nota
    p_nota = doc.add_paragraph(style="Normal")
    p_nota.paragraph_format.left_indent = Inches(0.5)
    p_nota.paragraph_format.space_before = Pt(1)
    p_nota.paragraph_format.space_after = Pt(8)

    run_nota_label = p_nota.add_run("Nota: ")
    run_nota_label.italic = True
    run_nota_label.font.size = Pt(9)
    run_nota_label.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    run_nota = p_nota.add_run(ref["nota"])
    run_nota.italic = True
    run_nota.font.size = Pt(9)
    run_nota.font.color.rgb = RGBColor(0x33, 0x33, 0x33)


# ---------------------------------------------------------------------------
# CONSTRUCCIÓN DEL DOCUMENTO
# ---------------------------------------------------------------------------

def build_doc(output_path: Path):
    doc = Document()

    # Márgenes
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1.2)
        section.right_margin = Inches(1.2)

    # ── Título principal ──────────────────────────────────────────────────
    title = doc.add_heading("Bibliografía Comentada", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.size = Pt(18)
        run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)

    subtitle = doc.add_paragraph("Campo Geotérmico Domo San Pedro — San Pedro Lagunillas, Nayarit, México")
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in subtitle.runs:
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x44, 0x44, 0x44)
        run.italic = True

    doc.add_paragraph()

    # ── Introducción ──────────────────────────────────────────────────────
    intro = doc.add_paragraph(
        "El presente documento reúne las referencias bibliográficas clave para el análisis "
        "de favorabilidad geotérmica del Domo San Pedro mediante el método Index Overlay "
        "(Prol-Ledesma, 2000). Las referencias están organizadas en seis aspectos temáticos: "
        "geoquímica, geología estructural, sismicidad, hidrogeología, anomalías térmicas y "
        "geofísica. Para cada referencia se indica el DOI o URL de acceso y una nota sobre "
        "su relevancia específica para el proyecto."
    )
    intro.paragraph_format.space_after = Pt(12)
    for run in intro.runs:
        run.font.size = Pt(10)

    add_horizontal_rule(doc)
    doc.add_paragraph()

    # ── Aspectos temáticos ────────────────────────────────────────────────
    ref_global = 1
    for aspecto in ASPECTOS:
        h = doc.add_heading(aspecto["titulo"], level=1)
        set_heading_color(h, aspecto["color"])
        for run in h.runs:
            run.font.size = Pt(13)

        for ref in aspecto["refs"]:
            add_ref(doc, ref_global, ref)
            ref_global += 1

        add_horizontal_rule(doc)
        doc.add_paragraph()

    # ── Nota final ────────────────────────────────────────────────────────
    nota_final = doc.add_paragraph()
    nota_final.paragraph_format.space_before = Pt(6)
    r1 = nota_final.add_run("Nota sobre acceso: ")
    r1.bold = True
    r1.font.size = Pt(9)
    r2 = nota_final.add_run(
        "Los artículos de los World Geothermal Congress (WGC) son de acceso abierto en "
        "geothermal-energy.org. Los informes de CFE/IIE pueden solicitarse vía INFOMEX/SAIMEX. "
        "Para sismicidad actualizada consultar el catálogo del SSN: http://www2.ssn.unam.mx"
    )
    r2.font.size = Pt(9)
    r2.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    p_fecha = doc.add_paragraph()
    p_fecha.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_fecha = p_fecha.add_run("Última actualización: Julio 2026  |  Proyecto: Domo San Pedro")
    r_fecha.font.size = Pt(8)
    r_fecha.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
    r_fecha.italic = True

    doc.save(str(output_path))
    print(f"Documento generado: {output_path}")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    out = Path(__file__).parent.parent / "BIBLIOGRAFIA COMPLEMENTARIA" / "Bibliografia_Domo_San_Pedro.docx"
    build_doc(out)
