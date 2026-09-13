"""
generar_borrador_metodologia.py
================================
Genera un BORRADOR del capítulo de Metodología para la tesina del Domo San Pedro,
fundamentado en Prol-Ledesma (2000) y adaptado a los datos y parámetros actuales
del proyecto (buffer de fallas 100 m, ventana de resistividad 20-50 Ohm·m,
exclusión del borde de caldera inferido).

USO:
    python scripts/generar_borrador_metodologia.py

SALIDA:
    outputs/Borrador_Metodologia_Domo_San_Pedro.docx   (Word, con estilo institucional)
    outputs/Borrador_Metodologia_Domo_San_Pedro.md      (Markdown, legible para revisión/auditores)

DISEÑO:
    El contenido vive en UNA sola estructura de datos (CONTENIDO). Desde ahí se
    renderizan ambos formatos, de modo que Word y Markdown nunca se desincronizan.

NOTA: Es un BORRADOR. Los bloques tipo "nota" (marcados [REVISAR/COMPLETAR])
      requieren la revisión y datos del autor antes de la versión final.
"""

from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ---------------------------------------------------------------------------
# CONFIGURACIÓN Y ESTILO (consistente con generar_propuesta_sig.py)
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DOCX = OUTPUT_DIR / "Borrador_Metodologia_Domo_San_Pedro.docx"
OUTPUT_MD = OUTPUT_DIR / "Borrador_Metodologia_Domo_San_Pedro.md"

COLOR_UNAM_AZUL = RGBColor(0x00, 0x2B, 0x5C)
COLOR_UNAM_ORO = RGBColor(0xB5, 0x85, 0x0B)
COLOR_GRIS = RGBColor(0x44, 0x44, 0x44)
COLOR_GRIS_CLARO = RGBColor(0x66, 0x66, 0x66)
COLOR_REVISAR = RGBColor(0xB0, 0x30, 0x30)

TITULO = ("Determinación de Zonas Favorables para Perforación Geotérmica "
          "en el Domo San Pedro, Nayarit, mediante un Sistema de Información Geográfica")
SUBTITULO = "Borrador de tesina — Capítulo de Metodología"


# ===========================================================================
# CONTENIDO ÚNICO
# ---------------------------------------------------------------------------
# Cada bloque es una tupla (tipo, *datos). Tipos:
#   ("h1"|"h2", texto)
#   ("p", texto)                     párrafo normal
#   ("nota", texto)                  nota de revisión para el autor
#   ("formula", texto)               ecuación centrada
#   ("tabla", encabezados, filas)    tabla
#   ("lista_num", [pasos])           lista numerada
#   ("refs", [referencias])          bibliografía
# ===========================================================================

CONTENIDO = [
    ("nota",
     "Este documento es un BORRADOR generado para agilizar la redacción. Ajusta la "
     "redacción, verifica cifras y completa las secciones marcadas antes de la versión "
     "final. Las referencias siguen el estilo autor-año."),

    ("h1", "1. Enfoque metodológico"),
    ("p",
     "La localización de zonas favorables para la perforación geotérmica exploratoria en el "
     "Domo San Pedro se aborda mediante la integración de evidencia geocientífica en un "
     "Sistema de Información Geográfica (SIG), siguiendo la metodología propuesta por "
     "Prol-Ledesma (2000) para el campo geotérmico de Los Azufres. Dicho enfoque demostró que "
     "las técnicas de integración de datos desarrolladas originalmente para la exploración "
     "minera pueden adaptarse a la exploración geotérmica, dado que en ambos casos la "
     "evidencia clave (estructuras, geología, geoquímica y geofísica) es de naturaleza "
     "similar."),
    ("p",
     "El método se basa en modelos guiados por conocimiento experto (knowledge-driven), en los "
     "que no se requiere información previa de pozos productores para calibrar el modelo, sino "
     "que los pesos y puntajes de cada capa de evidencia se asignan a partir de un modelo "
     "conceptual del yacimiento. Esta característica es idónea para el Domo San Pedro, un campo "
     "en etapa de reconocimiento donde la información de subsuelo es limitada. El contenido de "
     "esta sección fue reformulado y adaptado a partir de Prol-Ledesma (2000) para cumplir con "
     "las restricciones de derechos de autor."),

    ("h1", "2. Modelo conceptual del yacimiento"),
    ("p",
     "El modelo conceptual es el fundamento que justifica qué capas de evidencia son "
     "relevantes y con qué importancia relativa participan en la predicción. Para el Domo San "
     "Pedro se asume un sistema hidrotermal alojado en rocas volcánicas de baja porosidad "
     "primaria, en el que la permeabilidad es fundamentalmente secundaria, es decir, controlada "
     "por el fracturamiento y las fallas activas. En consecuencia, las zonas productivas se "
     "esperan asociadas a las estructuras que permiten el ascenso de fluidos calientes desde "
     "el reservorio."),
    ("p",
     "De acuerdo con este modelo, la ocurrencia de un reservorio explotable se caracteriza por "
     "la coincidencia espacial de: (i) evidencia superficial de permeabilidad y ascenso de "
     "fluidos (fallas activas, alta densidad de fracturamiento, manifestaciones termales y "
     "contactos con cuerpos volcánicos recientes que actúan como fuente de calor); y (ii) "
     "condiciones en profundidad favorables, expresadas por anomalías de resistividad eléctrica "
     "asociadas a fluidos salinos calientes y a minerales de alteración."),
    ("nota",
     "Describir aquí el modelo conceptual específico del Domo San Pedro con base en Corbo et "
     "al. (2026) y Prol-Ledesma et al. (2019): geometría del sistema, capa sello arcillosa, "
     "profundidad estimada del reservorio (1000-2000 m) y fuente de calor."),

    ("h1", "3. Red de inferencia"),
    ("p",
     "La lógica que combina la evidencia se expresa mediante una red de inferencia. Las "
     "condiciones superficiales indicadoras de permeabilidad se agrupan con el operador de "
     "unión (OR), pues cualquiera de ellas puede señalar una zona de ascenso de fluidos; el "
     "resultado se combina con la condición de resistividad en profundidad mediante el operador "
     "de intersección (AND), ya que se considera necesaria la ocurrencia simultánea de "
     "evidencia superficial y de subsuelo:"),
    ("formula",
     "Favorabilidad = Resistividad ∩ [ (Fallas ∪ Fracturamiento) ∪ (Fuente de calor ∪ Manifestaciones) ]"),
    ("p",
     "El resultado se expresa en una escala de favorabilidad de 0 a 1, donde 0 indica las áreas "
     "menos favorables y 1 las más favorables. Cabe precisar que esta escala no representa una "
     "probabilidad en sentido estricto, sino un índice relativo de favorabilidad "
     "(Prol-Ledesma, 2000)."),

    ("h1", "4. Datos de entrada (capas temáticas)"),
    ("p",
     "Cada capa temática se procesa como un mapa raster con tamaño de celda de 30 m en el "
     "sistema de referencia EPSG:32613 (WGS 84 / UTM Zona 13N). Para las capas de rasgos "
     "lineales o poligonales se calcula la distancia euclidiana de cada celda al rasgo más "
     "cercano, de modo que la favorabilidad se establece en función de la proximidad a la "
     "evidencia. La tabla siguiente resume las capas consideradas."),
    ("tabla",
     ["Capa temática", "Dominio", "Rol en el modelo", "Fuente (Domo San Pedro)"],
     [
         ["Resistividad (MT)", "Profundidad", "Fluidos/alteración del reservorio", "Corbo et al. (2026)"],
         ["Fallas principales", "Subsuperficial", "Permeabilidad secundaria", "Ferrari (2003), Corbo (2026), Muñoz (2024)"],
         ["Manifestaciones termales", "Superficial", "Ascenso de fluidos", "[COMPLETAR]"],
         ["Geología (domos/intrusivos)", "Superficial", "Fuente de calor", "SGM, Ferrari (2003)"],
         ["Densidad de fracturamiento", "Superficial", "Permeabilidad secundaria", "[COMPLETAR]"],
     ]),
    ("nota",
     "Estado actual del proyecto: el modelo se ha ejecutado con las capas de fallas y "
     "resistividad. Las capas de manifestaciones, geología y fracturamiento están pendientes "
     "de digitalización/integración. Indicar en la versión final qué capas se incluyeron "
     "efectivamente."),

    ("h2", "4.1 Tratamiento de las fallas y el borde de caldera"),
    ("p",
     "Las trazas de fallas provienen de tres fuentes cartográficas (Ferrari, 2003; Corbo et "
     "al., 2026; Muñoz, 2024). Siguiendo el criterio de Prol-Ledesma (2000) de emplear "
     "únicamente las estructuras activas o recientes que aportan permeabilidad, se excluyó del "
     "análisis el borde de caldera inferido, catalogado como tal en la tabla de atributos, por "
     "no constituir una falla con permeabilidad demostrada. De este modo la capa de fallas "
     "conserva solamente las fallas normales y laterales."),

    ("h1", "5. Modelos de integración de datos"),
    ("p",
     "Se implementan modelos guiados por conocimiento experto. En este trabajo se emplean el "
     "modelo booleano y el modelo Index Overlay multi-clase; se describe además el esquema "
     "difuso (fuzzy) como marco conceptual del tratamiento continuo de la favorabilidad."),

    ("h2", "5.1 Modelo booleano"),
    ("p",
     "En el modelo booleano cada capa se reclasifica de forma binaria: se asigna el valor 1 a "
     "las celdas que cumplen la condición de favorabilidad (por ejemplo, distancia menor o "
     "igual a 100 m del rasgo) y 0 al resto. Las capas se combinan con los operadores lógicos "
     "AND y OR de la red de inferencia. El resultado delimita únicamente las áreas donde se "
     "satisfacen todas las condiciones simultáneamente. Este modelo es útil para la ubicación "
     "directa de pozos por ser conservador, aunque tiende a ser demasiado restrictivo y puede "
     "omitir zonas productivas (errores de omisión)."),

    ("h2", "5.2 Modelo Index Overlay multi-clase"),
    ("p",
     "El modelo Index Overlay flexibiliza el esquema booleano al permitir clases intermedias. "
     "Cada capa temática recibe un peso según su relevancia para indicar la presencia del "
     "reservorio, y cada clase dentro de la capa recibe un puntaje. La favorabilidad de cada "
     "celda es el promedio ponderado de los puntajes:"),
    ("formula", "S = Σ (S_ij · w_i) / Σ (w_i)"),
    ("p",
     "donde S es el puntaje ponderado de la celda, w_i es el peso de la i-ésima capa temática y "
     "S_ij es el puntaje de la j-ésima clase de la i-ésima capa (Bonham-Carter, 1994; "
     "Prol-Ledesma, 2000). Los pesos y puntajes empleados se resumen en la tabla siguiente."),
    ("tabla",
     ["Capa temática", "Peso (w_i)", "Clases (condición)", "Puntaje (S_ij)"],
     [
         ["Resistividad (modelo MT)", "9", "20–50 Ω·m / 15–20 y 50–55 Ω·m / <15 o >55 Ω·m", "10 / 8 / 0"],
         ["Fallas principales", "7", "≤100 m / 100–200 m / >200 m", "10 / 8 / 0"],
         ["Manifestaciones termales", "5", "≤100 m / 100–200 m / >200 m", "10 / 8 / 0"],
         ["Geología (domos recientes)", "5", "≤100 m / 100–200 m / >200 m", "10 / 8 / 0"],
         ["Densidad de fracturamiento", "5", "≤100 m / 100–200 m / >200 m", "10 / 8 / 0"],
     ]),

    ("h2", "5.3 Adaptación de los umbrales al Domo San Pedro"),
    ("p",
     "Los umbrales de distancia se conservan respecto a Prol-Ledesma (2000): favorabilidad "
     "alta hasta 100 m del rasgo y favorabilidad moderada entre 100 y 200 m, distancia esta "
     "última observada por los ingenieros de campo como el radio típico de los pozos "
     "productores respecto de las fallas principales."),
    ("p",
     "El criterio de resistividad, en cambio, se redefinió para el Domo San Pedro. Mientras que "
     "en Los Azufres los valores más favorables correspondían a la resistividad más baja (menor "
     "o igual a 10 Ω·m), en el Domo San Pedro dichos valores muy bajos se interpretan como la "
     "capa sello arcillosa (esmectita) que cubre el reservorio y no como el reservorio mismo. Por "
     "ello el yacimiento se asocia a una ventana de resistividad intermedia de 20 a 50 Ω·m, valor "
     "adoptado siguiendo el criterio experto de la Dra. R.M. Prol-Ledesma. La clase de "
     "favorabilidad moderada se define como un halo de transición simétrico alrededor de esa "
     "ventana (15–20 y 50–55 Ω·m), en lugar del rango bajo 10–20 Ω·m, que corresponde al techo "
     "del sello arcilloso; los valores menores a 15 Ω·m (sello) y mayores a 55 Ω·m (roca fría o "
     "basamento resistivo) se consideran no favorables."),
    ("nota",
     "La ventana de resistividad del reservorio (20–50 Ω·m) se adopta siguiendo el criterio "
     "experto de la Dra. R.M. Prol-Ledesma (seminario del 29 de agosto de 2026). Conviene "
     "respaldarla además con literatura publicada sobre la zonación de alteración esmectita→"
     "illita/clorita en clay caps geotérmicos. IMPORTANTE: la clasificación de resistividad debe "
     "aplicarse al corte del intervalo objetivo del reservorio (1000–2000 m de profundidad); el "
     "corte somero de 350 mbsl usado en las corridas iniciales puede estar midiendo el sello "
     "arcilloso y no el reservorio (a verificar por el autor)."),

    ("h2", "5.4 Tratamiento continuo (favorabilidad difusa)"),
    ("p",
     "Para evitar transiciones abruptas propias de la reclasificación en clases discretas, la "
     "favorabilidad se calcula además de forma continua mediante funciones de pertenencia "
     "(fuzzy membership) en el rango [0, 1], en línea con el esquema difuso de Prol-Ledesma "
     "(2000). En la capa de fallas la pertenencia vale 1 dentro de la zona de daño (≤100 m) y "
     "decae de manera continua hasta 0 en los 200 m. En la capa de resistividad la pertenencia "
     "vale 1 dentro de la ventana del reservorio (20–50 Ω·m) y decae linealmente hasta 0 en un "
     "halo simétrico de 5 Ω·m a cada lado (15–20 y 50–55 Ω·m). Este tratamiento produce mapas de "
     "gradiente suave y refleja la incertidumbre inherente a los umbrales."),

    ("h1", "6. Umbrales de decisión e interpretación"),
    ("p",
     "Sobre el mapa continuo de favorabilidad (0–1) se aplican umbrales de decisión. De acuerdo "
     "con Prol-Ledesma (2000), un valor de 0.6 es el umbral más bajo que en Los Azufres incluyó "
     "a la totalidad de los pozos productores dejando fuera a los no productores, por lo que se "
     "adopta como límite inferior de las zonas de interés:"),
    ("tabla",
     ["Rango de favorabilidad", "Interpretación"],
     [
         ["> 0.7", "Máxima prioridad para perforación exploratoria"],
         ["0.6 – 0.7", "Favorabilidad moderada; candidata a exploración detallada"],
         ["< 0.6", "No prioritaria"],
     ]),
    ("p",
     "Los modelos booleano y de bajo riesgo resultan más adecuados para la ubicación directa de "
     "pozos, por su carácter conservador, mientras que el Index Overlay y los esquemas de alto "
     "riesgo son más apropiados para planificar exploración detallada previa a la perforación "
     "(Prol-Ledesma, 2000)."),

    ("h1", "7. Flujo de trabajo (pipeline)"),
    ("p", "El procedimiento se organiza en las siguientes fases:"),
    ("lista_num",
     [
         "Recopilación y homogeneización de datos al CRS EPSG:32613 (resolución 30 m).",
         "Preparación: digitalización vectorial, reproyección, conversión vector→raster y "
         "cálculo de mapas de distancia euclidiana.",
         "Reclasificación de cada capa (clases discretas 0/8/10 y funciones de pertenencia "
         "continuas).",
         "Asignación de pesos por criterio experto según el modelo conceptual.",
         "Cálculo del Index Overlay y generación del mapa continuo de favorabilidad (0–1).",
         "Interpretación con umbrales (0.6 y 0.7) y elaboración de mapas finales.",
         "Validación contra pozos y datos conocidos, y análisis de sensibilidad de pesos.",
     ]),

    ("h1", "8. Referencias"),
    ("refs",
     [
         "Bonham-Carter, G.F. (1994). Geographic Information Systems for Geoscientists: "
         "Modelling with GIS. Pergamon, 398 pp.",
         "Corbo-Camargo, F. et al. (2026). Magnetotelluric imaging of the Domo San Pedro "
         "geothermal system. GSA Books (en prensa).",
         "Ferrari, L. et al. (2003). Geology of the San Pedro–Ceboruco graben. [COMPLETAR cita].",
         "Prol-Ledesma, R.M. (2000). Evaluation of the reconnaissance results in geothermal "
         "exploration using GIS. Geothermics, 29, 83–103.",
         "Saaty, T.L. (1977). A scaling method for priorities in hierarchical structures. "
         "Journal of Mathematical Psychology, 15, 234–281.",
     ]),
]


# ---------------------------------------------------------------------------
# HELPERS WORD
# ---------------------------------------------------------------------------

def set_cell_shading(cell, color_hex):
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


# ---------------------------------------------------------------------------
# RENDER A WORD
# ---------------------------------------------------------------------------

def render_docx():
    doc = Document()
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.5)

    # Encabezado
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO")
    r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = COLOR_UNAM_AZUL

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(SUBTITULO)
    r.font.size = Pt(10); r.font.color.rgb = COLOR_GRIS_CLARO

    doc.add_paragraph(); add_horizontal_rule(doc)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(TITULO)
    r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = COLOR_UNAM_AZUL
    add_horizontal_rule(doc); doc.add_paragraph()

    for bloque in CONTENIDO:
        tipo = bloque[0]
        if tipo == "h1":
            h = doc.add_heading(bloque[1], level=1)
            for run in h.runs:
                run.font.color.rgb = COLOR_UNAM_AZUL
        elif tipo == "h2":
            h = doc.add_heading(bloque[1], level=2)
            for run in h.runs:
                run.font.color.rgb = COLOR_UNAM_AZUL
        elif tipo == "p":
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            r = p.add_run(bloque[1]); r.font.size = Pt(11); r.font.color.rgb = COLOR_GRIS
        elif tipo == "nota":
            p = doc.add_paragraph()
            r = p.add_run("[REVISAR/COMPLETAR] " + bloque[1])
            r.font.size = Pt(10); r.font.italic = True; r.font.color.rgb = COLOR_REVISAR
        elif tipo == "formula":
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(bloque[1]); r.font.size = Pt(12); r.font.italic = True
            r.font.color.rgb = COLOR_UNAM_AZUL
        elif tipo == "tabla":
            _tabla_docx(doc, bloque[1], bloque[2])
            doc.add_paragraph()
        elif tipo == "lista_num":
            for paso in bloque[1]:
                p = doc.add_paragraph(style="List Number")
                r = p.add_run(paso); r.font.size = Pt(11); r.font.color.rgb = COLOR_GRIS
        elif tipo == "refs":
            for ref in bloque[1]:
                p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.left_indent = Cm(0.75)
                p.paragraph_format.first_line_indent = Cm(-0.75)
                r = p.add_run(ref); r.font.size = Pt(10); r.font.color.rgb = COLOR_GRIS

    doc.save(str(OUTPUT_DOCX))
    print(f"Word generado:     {OUTPUT_DOCX}")


def _tabla_docx(doc, encabezados, filas):
    t = doc.add_table(rows=1, cols=len(encabezados))
    t.style = "Light Grid Accent 1"
    hdr = t.rows[0].cells
    for i, h in enumerate(encabezados):
        hdr[i].text = ""
        run = hdr[i].paragraphs[0].add_run(h)
        run.font.bold = True; run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_shading(hdr[i], "002B5C")
    for fila in filas:
        celdas = t.add_row().cells
        for i, val in enumerate(fila):
            celdas[i].text = ""
            run = celdas[i].paragraphs[0].add_run(str(val))
            run.font.size = Pt(10); run.font.color.rgb = COLOR_GRIS
    return t


# ---------------------------------------------------------------------------
# RENDER A MARKDOWN
# ---------------------------------------------------------------------------

def render_md():
    lineas = []
    lineas.append(f"# {TITULO}")
    lineas.append("")
    lineas.append(f"*{SUBTITULO}*")
    lineas.append("")
    lineas.append("---")
    lineas.append("")

    for bloque in CONTENIDO:
        tipo = bloque[0]
        if tipo == "h1":
            lineas.append(f"## {bloque[1]}")
            lineas.append("")
        elif tipo == "h2":
            lineas.append(f"### {bloque[1]}")
            lineas.append("")
        elif tipo == "p":
            lineas.append(bloque[1])
            lineas.append("")
        elif tipo == "nota":
            lineas.append(f"> **[REVISAR/COMPLETAR]** {bloque[1]}")
            lineas.append("")
        elif tipo == "formula":
            lineas.append("$$")
            lineas.append(bloque[1])
            lineas.append("$$")
            lineas.append("")
        elif tipo == "tabla":
            encabezados, filas = bloque[1], bloque[2]
            lineas.append("| " + " | ".join(encabezados) + " |")
            lineas.append("| " + " | ".join(["---"] * len(encabezados)) + " |")
            for fila in filas:
                lineas.append("| " + " | ".join(str(v) for v in fila) + " |")
            lineas.append("")
        elif tipo == "lista_num":
            for i, paso in enumerate(bloque[1], start=1):
                lineas.append(f"{i}. {paso}")
            lineas.append("")
        elif tipo == "refs":
            for ref in bloque[1]:
                lineas.append(f"- {ref}")
            lineas.append("")

    OUTPUT_MD.write_text("\n".join(lineas), encoding="utf-8")
    print(f"Markdown generado: {OUTPUT_MD}")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    render_docx()
    render_md()


if __name__ == "__main__":
    main()
