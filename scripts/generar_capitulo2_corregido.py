"""
generar_capitulo2_corregido.py
==============================
Genera el CAPÍTULO II (Descripción de la zona de estudio) con las correcciones
del panel de 7 auditores aplicadas, en Word (.docx) y Markdown (.md).

Correcciones inequívocas aplicadas directamente. Donde las fuentes se contradicen
o el dato requiere confirmación del autor, se deja una marca [VERIFICAR: ...] en
rojo, sin inventar valores.

USO:
    python scripts/generar_capitulo2_corregido.py

SALIDA:
    outputs/Capitulo2_Descripcion_Zona_Estudio_CORREGIDO.docx
    outputs/Capitulo2_Descripcion_Zona_Estudio_CORREGIDO.md
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DOCX = OUTPUT_DIR / "Capitulo2_Descripcion_Zona_Estudio_CORREGIDO.docx"
OUTPUT_MD = OUTPUT_DIR / "Capitulo2_Descripcion_Zona_Estudio_CORREGIDO.md"

COLOR_UNAM_AZUL = RGBColor(0x00, 0x2B, 0x5C)
COLOR_GRIS = RGBColor(0x44, 0x44, 0x44)
COLOR_GRIS_CLARO = RGBColor(0x66, 0x66, 0x66)
COLOR_VERIFICAR = RGBColor(0xB0, 0x30, 0x30)

TITULO = "CAPÍTULO II. DESCRIPCIÓN DE LA ZONA DE ESTUDIO"
SUBTITULO = ("Tesina: Determinación de nuevas zonas favorables para la expansión del "
             "Campo Geotérmico Domo San Pedro, Nayarit, México")

# ===========================================================================
# CONTENIDO (bloques). Tipos:
#   ("h1"|"h2"|"h3", texto)
#   ("p", texto)
#   ("verificar", texto)        marca de verificación (rojo)
#   ("tabla", encabezados, filas)
#   ("lista", [items])
#   ("refs", [referencias])
# Las marcas [VERIFICAR: ...] dentro de un párrafo se resaltan automáticamente.
# ===========================================================================

CONTENIDO = [
    ("verificar",
     "Este documento incorpora las correcciones del panel de 7 auditores sobre la versión v4. "
     "Las correcciones inequívocas (respaldadas sin ambigüedad por las fuentes) fueron aplicadas. "
     "Los puntos marcados [VERIFICAR] requieren que el autor confirme el dato o elija entre "
     "fuentes en conflicto antes de la versión final."),

    ("h1", "2.1 Marco tectónico"),
    ("p",
     "El Campo Geotérmico Domo San Pedro (DSP) se localiza en el suroeste del estado de Nayarit, "
     "dentro del municipio de San Pedro Lagunillas, aproximadamente a 40 km al sureste de la ciudad "
     "de Tepic. [VERIFICAR: la distancia y dirección al volcán Ceboruco difieren entre el borrador "
     "(10 km al SW) y el resumen de concesión (17.5 km al NW); confirmar y unificar.] "
     "Fisiográficamente, el área de estudio se sitúa en una zona de transición neotectónica compleja "
     "donde convergen tres provincias geológicas y fisiográficas mayores de México: el Cinturón "
     "Volcánico Transmexicano (CVTM) al este y sur, la Provincia Volcánica de la Sierra Madre "
     "Occidental (SMO) al norte, y el Bloque de Jalisco al suroeste (Ferrari et al., 2003; "
     "Reyes-Orozco et al., 2019)."),
    ("p",
     "El CVTM es un arco volcánico continental neógeno-cuaternario asociado a la subducción oblicua "
     "de las placas de Cocos y Rivera bajo la Placa Norteamericana. El DSP se emplaza en el segmento "
     "más occidental de este arco, donde la dinámica tectónica está influenciada por la "
     "discontinuidad de la placa en subducción (ventana de losa o slab window) y la divergencia del "
     "Bloque de Jalisco respecto al continente (Petrone et al., 2001; Ferrari et al., 2003). "
     "La Sierra Madre Occidental adyacente corresponde a una secuencia ignimbrítica del "
     "Oligoceno-Mioceno temprano (~34-19 Ma), lo que la distingue temporalmente del vulcanismo del "
     "CVTM."),

    ("h2", "2.1.1 Estructuras geológicas regionales y locales"),
    ("p",
     "El campo geotérmico DSP se ubica en el límite nororiental del Graben de Compostela, sobre la "
     "traza de la Falla Milpillas-Cerro Grande, que constituye el borde norte del graben "
     "(Corbo-Camargo et al., 2026). El Graben de Compostela es el segmento occidental (terminal, en "
     "el extremo WNW) del sistema del Rift Tepic-Zacoalco (RTZ); en la literatura se le ha "
     "denominado también, en un sentido más amplio, graben de San Pedro-Ceboruco (Ferrari et al., "
     "2003). El RTZ es uno de los tres sistemas de grabens mayores que delimitan el Bloque de "
     "Jalisco respecto al resto del continente (Ferrari et al., 1994; Ruiz Mendoza, 2022)."),
    ("p",
     "El Graben de Compostela sobreyace el contacto geológico entre el basamento plutónico "
     "cristalino del Bloque de Jalisco al sur —granodioritas y dioritas del Cretácico Tardío al "
     "Paleoceno— y la secuencia ignimbrítica de la SMO al norte. "
     "[VERIFICAR: las edades del batolito del Bloque de Jalisco (el borrador citaba 75-56 Ma y "
     ">85 Ma atribuidas a Ferrari 2003) deben reconciliarse con las fuentes: Ferrari et al. (2003) "
     "reporta edades U-Pb ~100-90 Ma (Schaaf et al., 1995) y K-Ar 90-50 Ma; Reyes-Orozco et al. "
     "(2019) usa 75-56 Ma. Confirmar cuál se adopta y citarla correctamente.]"),
    ("p",
     "A nivel local, la subsidencia tectónica acumulada en el basamento supera los 1,100 m en el "
     "sector caldérico central y más de 2,000 m a escala regional (Ferrari et al., 2003; Ruiz "
     "Mendoza, 2022). La arquitectura estructural se organiza en tres familias principales de "
     "fallas:"),
    ("lista",
     [
      "Sistema NW-SE a WNW-ESE: fallas normales regionales subverticales (60°-80°) paralelas al RTZ "
      "(p. ej. Falla Milpillas-Cerro Grande, Falla Compostela, Falla Pedernales). Acomodan el mayor "
      "desplazamiento vertical del basamento. La Falla Milpillas-Cerro Grande, en particular, actúa "
      "como barrera de retención hidrotermal del campo (Corbo-Camargo et al., 2026); el sellado por "
      "arcillas en el núcleo de falla (fault core) que explica este comportamiento de barrera "
      "corresponde al modelo de arquitectura de zonas de falla de Caine et al. (1996). Las fallas "
      "Compostela y Pedernales, que delimitan el graben, se describen en Reyes-Orozco et al. (2019).",
      "Sistema transversal secundario E-W: fallas profundas (p. ej. Ocotes, Ávalos, Guásimas) que "
      "se extienden hasta ~2.5 km en el granito basamental y actúan como los canales de mayor "
      "conductividad hidráulica vertical (Reyes-Orozco et al., 2019).",
      "Sistema ortogonal N-S a NE-SW: fallas secundarias que actúan predominantemente como barreras "
      "estructurales y límites laterales del reservorio (Reyes-Orozco et al., 2019).",
     ]),

    ("h2", "2.1.2 Estado de esfuerzos neotectónicos y tectónica activa"),
    ("p",
     "El análisis cinemático y microtectónico en el sector occidental del RTZ indica que la "
     "deformación neotectónica activa está regida por un tensor de esfuerzos extensional, con una "
     "dirección del eje de extensión principal (sigma-3) orientada NNE-SSW a NE-SW (Ruiz Mendoza, "
     "2022). Desde el Mioceno tardío no se reconoce transcurrencia dextral mayor activa en el RTZ; "
     "la deformación plio-cuaternaria es esencialmente extensional (Ferrari et al., 1994). "
     "[VERIFICAR: la orientación de sigma-3 (NNE-SSW a NE-SW) NO debe atribuirse a Muñoz-Burbano et "
     "al. (2024), que es un estudio de sismicidad/variación de velocidad sísmica y no de "
     "paleoesfuerzos. Confirmar la página exacta en Ruiz Mendoza (2022) o citar el trabajo "
     "microtectónico regional correspondiente (p. ej. Ferrari & Rosas-Elguera, 2000).]"),
    ("p",
     "Bajo este campo de esfuerzos, las estructuras óptimamente orientadas para la dilatación y "
     "apertura mecánica son las de rumbo WNW-ESE a NW-SE (aproximadamente perpendiculares a "
     "sigma-3). De forma complementaria, las fallas transversales E-W actúan como conductos "
     "verticales de alta permeabilidad por reactivación e intersección estructural (Reyes-Orozco et "
     "al., 2019; Corbo-Camargo et al., 2026). La tectónica activa y la preservación de la "
     "permeabilidad secundaria en el basamento cristalino se evidencian por la sismicidad inducida "
     "por operaciones geotérmicas, que reactiva la red de fracturas en las zonas de daño de las "
     "fallas en el intervalo somero de 0.5 a 2.5 km de profundidad (Muñoz-Burbano et al., 2024). "
     "El concepto de zona de daño (damage zone) como dominio de permeabilidad, distinto del núcleo "
     "de falla impermeable, procede de Caine et al. (1996) y Guillou-Frottier et al. (2024)."),

    ("h1", "2.2 Marco geológico"),
    ("p",
     "La historia geológica local abarca la evolución del Complejo Volcánico San Pedro-Cerro Grande "
     "(SPCG), estructurada en etapas eruptivas principales (Petrone et al., 2001, 2006; Ferrari et "
     "al., 2003; Ruiz Mendoza, 2022):"),
    ("lista",
     [
      "Etapa pre-caldera: incluye el domo más antiguo del complejo, Cerro Las Tetillas. "
      "[VERIFICAR: la edad de Cerro Las Tetillas está en disputa entre fuentes: 2.3 ± 0.5 Ma por "
      "K-Ar (Gastil et al., 1979, en Petrone et al., 2001) y ~0.45 Ma por 40Ar/39Ar (Frey et al., "
      "2004, en Petrone et al., 2006; Ferrari et al., 2003). En ambos casos es PRE-caldera. Elegir "
      "la edad a adoptar y justificarla; el consenso reciente favorece la datación 40Ar/39Ar más "
      "joven.] Se emplazan además secuencias de lava andesíticas y dacíticas que constituyen el "
      "edificio ancestral y albergan las unidades que hoy conforman la capa sello.",
      "Etapa de colapso caldérico: formación de la estructura caldérica de San Pedro, acompañada de "
      "tobas e ignimbritas de colapso. [VERIFICAR: la edad del colapso NO está precisamente "
      "determinada; las fuentes recientes la acotan entre ~450 y ~283 ka (Petrone et al., 2006; "
      "Ferrari et al., 2003), NO en ~1.1 Ma como se indicaba en la v4. Asimismo, el diámetro "
      "caldérico difiere entre fuentes: 7-10 km (Ferrari et al., 2003) frente a ~4 km (Petrone et "
      "al., 2006); declarar la discrepancia o elegir con justificación.]",
      "Etapa post-caldera silícica y máfica (Cuaternario al Holoceno): efusión de domos "
      "dacíticos-riolíticos y coladas asociadas. Destacan el domo riolítico Los Ocotes (~0.1 Ma / "
      "100 ka) y el complejo de domos dacíticos del Cerro San Pedro (Domo San Pedro s.s.), fechado "
      "en ~0.041 Ma (41 ka). Se registran también emisiones basálticas de intraplaca, de afinidad "
      "Na-alcalina/transicional, como el cono Amado Nervo (~0.22 Ma), que confieren carácter "
      "bimodal al complejo (Petrone et al., 2001, 2006; Ruiz Mendoza, 2022). "
      "[VERIFICAR: las edades 40Ar/39Ar modernas (Domo San Pedro 41 ka, Los Ocotes 100 ka, Amado "
      "Nervo 220 ka) provienen de Frey et al. (2004); citar esa fuente directamente y añadirla a "
      "las referencias.]",
     ]),
    ("p",
     "La presencia de vulcanismo silícico tan reciente (~41 ka) sugiere la persistencia de una "
     "fuente de calor cortical joven —probablemente un cuerpo intrusivo o subvolcánico— como motor "
     "térmico plausible del sistema. No obstante, la fuente de calor específica del DSP no ha sido "
     "delimitada geofísicamente y permanece poco constreñida: Corbo-Camargo et al. (2026) señalan "
     "explícitamente que se conoce muy poco sobre ella, pues los pozos (<3 km) y la cobertura MT "
     "actual no alcanzan a resolverla. Su geometría y profundidad quedan como una incógnita abierta."),

    ("h2", "2.2.1 Descripción litológica y estratigráfica de muestras de perforación en pozos"),
    ("p",
     "La caracterización mineralógica y petrográfica de recortes de perforación (cuttings) y núcleos "
     "en los pozos profundos del campo (p. ej. SP01, SP02, SP04, SP05, SP06, SP07, SP08) permite "
     "definir la columna litológica tipo del yacimiento (Gómez-Cruz, 2019; Corbo-Camargo et al., "
     "2026):"),
    ("lista",
     [
      "Depósitos volcánicos recientes (0 a ~700 m de profundidad): lavas dacíticas y riolíticas, "
      "tobas piroclásticas, pumicita, vidrio volcánico y coluvión dacítico del Pleistoceno-Holoceno "
      "(~0.6 a 0.1 Ma).",
      "Secuencia volcánica pliocénica (~700 a ~850 m): intercalaciones de lavas andesíticas y "
      "dacíticas con alteración hidrotermal moderada.",
      "Secuencia volcánica miocénica (~850 a ~1,300 m) — capa sello (clay cap): andesitas y basaltos "
      "alterados hidrotermalmente, con esmectita e interestratificados illita/esmectita. Esta franja "
      "de ~500 m de espesor sella hidráulicamente el reservorio a presión. [VERIFICAR: el carácter "
      "de la alteración de la capa sello difiere entre fuentes. Reyes-Orozco et al. (2019) y "
      "Corbo-Camargo et al. (2026) la describen funcionalmente como capa sello arcillosa (clay "
      "cap); Gómez-Cruz (2019) concluye que no se define una alteración argílica propiamente dicha, "
      "sino un ambiente subpropilítico/propilítico de baja temperatura. Se recomienda usar el "
      "término descriptivo 'capa sello arcillosa (esmectita-illita)' y reconocer la discrepancia.]",
      "Basamento cristalino del Bloque de Jalisco (>1,300 m a >3.7 km) — roca almacén: intrusivos "
      "plutónicos de granodiorita y diorita con diques asociados. Porosidad primaria prácticamente "
      "nula; la permeabilidad es secundaria, por fracturamiento tectónico e hidrotermal. Presenta "
      "alteración propilítica profunda caracterizada por cuarzo, plagioclasa, clorita, epidota "
      "abundante, calcita, anfíbol y pirita/pirrotita (Gómez-Cruz, 2019).",
     ]),
    ("p",
     "De forma puntual, en el pozo SP05 (intervalo ~800-1000 m) se identificó wairakita, una zeolita "
     "índice de temperatura intermedia asociada a anhidrita, interpretada por Gómez-Cruz (2019) como "
     "evidencia de alta permeabilidad local (no como indicador de alta temperatura ni como parte del "
     "ensamble propilítico profundo del basamento)."),

    ("h1", "2.3 Modelos conceptuales del Campo Geotérmico Domo San Pedro"),

    ("h2", "2.3.1 Tipo de play geotérmico"),
    ("p",
     "Con base en el catálogo de tipos de play geotérmico guiado por controles geológicos (Moeck, "
     "2014; Moeck & Beardsmore, 2014), el Campo Domo San Pedro se clasifica como un play geotérmico "
     "dominado por convección de tipo volcánico/magmático (CV1), en el que la fuente de calor es de "
     "afinidad magmática asociada al vulcanismo silícico reciente. Su rasgo distintivo es que la "
     "roca almacén no es un acuífero volcánico poroso, sino el basamento plutónico granítico denso "
     "del Bloque de Jalisco; por ello el almacenamiento y las vías de circulación del fluido "
     "dependen de la permeabilidad secundaria generada en las zonas de daño de fallas extensionales "
     "activas del Graben de Compostela. "
     "[VERIFICAR: en la clasificación de Moeck, los tipos volcánico (CV1) y de dominio extensional "
     "(CV3) son ramas distintas —CV3 es explícitamente no magmático—, por lo que la etiqueta "
     "'híbrido CV1/CV3' de la v4 es contradictoria. Se propone clasificarlo como CV1 (magmático) "
     "señalando el control estructural extensional como el mecanismo de permeabilidad; confirmar "
     "esta decisión y citar Moeck & Beardsmore (2014) como origen de los códigos.]"),

    ("h2", "2.3.2 Modelo geoquímico e hidrogeoquímico"),
    ("p",
     "El modelo hidrogeoquímico (Rodríguez et al., 2019; Reyes-Orozco et al., 2019) indica que el "
     "fluido geotérmico es de origen meteórico, con recarga regional desde las zonas de mayor "
     "elevación al noroeste, oeste y suroeste. La interacción fluido-roca a alta temperatura produce "
     "un agua de tipo clorurada sódica (Na-Cl) madura, con pH neutro a ligeramente ácido y "
     "concentraciones de cloruros estimadas en el reservorio de ~850 a 1,200 ppm (distintas de las "
     "concentraciones medidas en separador, que son mayores)."),
    ("p",
     "El sistema corresponde a un reservorio de líquido dominante (líquido comprimido, a presión "
     "hidrostática superior a la de saturación), con una zona bifásica somera y oriental de menor "
     "extensión y temperatura, generada por ebullición y enfriamiento durante la migración lateral "
     "del fluido:"),
    ("lista",
     [
      "Reservorio profundo: dominado por líquido, a temperaturas de ~330 a 340 °C en el basamento "
      "granítico fracturado (p. ej. SP01 ~344 °C).",
      "Zona bifásica somera/oriental: agua-vapor, con temperatura de ~260 °C medida en SP06 y "
      "equilibrio de geotermómetros de gas del orden de 225-250 °C. [VERIFICAR: el valor de ~280 °C "
      "indicado en la v4 no se localiza en las fuentes; usar ~260 °C (SP06) o el rango de "
      "geotermómetros, o confirmar la fuente del 280 °C.]",
     ]),
    ("p",
     "La zona principal de ascenso de fluidos (upflow) se sitúa en la vecindad de los pozos SP05 y "
     "SP06 (con la mayor descarga de gases no condensables), mientras que el flujo de salida lateral "
     "(outflow) se dirige hacia el este y sureste a través de fallas E-W y NW-SE, alimentando "
     "manantiales termales periféricos (p. ej. Agua Caliente, Agua Tibia) (Rodríguez et al., 2019)."),

    ("h2", "2.3.3 Modelos geofísico y geomecánico"),
    ("p",
     "El modelo de resistividad eléctrica tridimensional obtenido por magnetotelúrica 3D (MT 3D), "
     "integrado con datos de pozos, aporta la geometría del sistema (Corbo-Camargo et al., 2026):"),
    ("lista",
     [
      "Capa sello (clay cap): horizonte conductor de baja resistividad (<10 Ohm-m) ubicado cerca del "
      "nivel del mar (~0 msnm), con espesor calibrado de ~500 m (alteración con esmectita).",
      "Reservorio geotérmico: resistividad intermedia dentro del basamento granítico fracturado y "
      "saturado con salmuera caliente. Corbo-Camargo et al. (2026) reportan ~30 a <100 Ohm-m para "
      "las vías porosas de almacenamiento y 30-80 Ohm-m para la alteración propilítica. "
      "[VERIFICAR: existe una diferencia entre este rango observado (30-100 Ohm-m, Corbo 2026) y la "
      "ventana operativa del modelo de favorabilidad adoptada en el proyecto (20-50 Ohm-m, criterio "
      "de la Dra. Prol-Ledesma). Documentar y justificar esta elección en el capítulo de "
      "metodología para mantener la coherencia entre la descripción y la reclasificación SIG.]",
      "Techo del basamento granítico: se define con el umbral ~150 Ohm-m; los bloques compactos no "
      "fracturados hacia el oeste y noroeste alcanzan >1,000 Ohm-m.",
     ]),
    ("p",
     "El modelo MT 3D muestra que el basamento granítico se vuelve menos resistivo y menos denso "
     "hacia el centro y sureste del Graben de Compostela, lo que Corbo-Camargo et al. (2026) "
     "interpretan como una posible extensión del reservorio y una fuente regional de fluidos "
     "mineralizados. Debe precisarse, no obstante, que el estudio distingue dos reservorios "
     "potenciales: GR-1 (Domo San Pedro, en producción) y GR-2 (asociado al volcán Amado Nervo, al "
     "sur), y que parte de la anomalía conductora profunda (~1,800 m) coincide con una anomalía "
     "magnética alta, atribuible a mineralización magnetítica/ferromagnesiana, por lo que no todo el "
     "conductor equivale a reservorio explotable. Esta distinción, lejos de debilitar la propuesta "
     "de expansión, justifica el análisis SIG multicriterio para discriminar las zonas "
     "efectivamente favorables. [VERIFICAR: relacionar espacialmente esta anomalía del centro/SE "
     "con el interior o la contigüidad del polígono de concesión (cuyos vértices SE se ubican en "
     "536,557 / 2,341,933 y 536,736 / 2,335,981 UTM 13N) y con la infraestructura existente.]"),
    ("p",
     "Geomecánicamente, las operaciones de extracción e inyección inducen cambios en la presión de "
     "poros que activan microsismicidad en enjambres en el intervalo somero de 0.5 a 2.5 km de "
     "profundidad, asociada probablemente a las operaciones (Muñoz-Burbano et al., 2024). Un clúster "
     "sísmico más profundo (2.5-7 km) coexiste temporalmente, aunque los autores no establecen su "
     "origen causal. La interferometría de ruido sísmico (dv/v) revela variaciones de velocidad "
     "correlacionadas con los ciclos de reinyección, coherentes con la apertura transitoria de "
     "fracturas en las zonas de daño y con la alta sensibilidad dinámica del reservorio "
     "(Muñoz-Burbano et al., 2024)."),

    ("h1", "2.4 Marco espacial y delimitación del área de estudio"),
    ("p",
     "El proyecto emplea como sistema de referencia el EPSG:32613 (WGS 84 / UTM Zona 13N, unidades "
     "en metros), adecuado para los cálculos de distancia euclidiana del análisis SIG. Se distinguen "
     "dos dominios espaciales:"),
    ("lista",
     [
      "Área de estudio (marco de cómputo del SIG): rectángulo de análisis de 15 x 20 km = 300 km2, "
      "definido por las coordenadas XMIN 520,000 m, XMAX 535,000 m, YMIN 2,328,000 m, YMAX "
      "2,348,000 m (UTM 13N), con resolución de celda de 30 m.",
      "Área concesionada (frontera legal y dominio prioritario): polígono de 129.18 km2 (12,918 ha) "
      "otorgado por la SENER a Geotérmica para el Desarrollo, S.A.P.I. de C.V. (Grupo Dragón) el 30 "
      "de octubre de 2015, definido por siete vértices. Este polígono actúa como máscara de recorte "
      "(clipping mask): las nuevas zonas favorables deben caer dentro de él o ser contiguas, para "
      "aprovechar la infraestructura existente (caminos, subestación eléctrica en Chapalilla a ~10 "
      "km, derechos de agua otorgados por CONAGUA).",
     ]),
    ("tabla",
     ["Vértice", "UTM X (m)", "UTM Y (m)"],
     [
      ["1 (P.P.)", "528,815", "2,346,693"],
      ["2", "534,695", "2,346,778"],
      ["3", "536,557", "2,341,933"],
      ["4", "536,736", "2,335,981"],
      ["5", "522,796", "2,335,906"],
      ["6", "522,936", "2,344,192"],
      ["7", "528,610", "2,344,310"],
     ]),
    ("p",
     "El Campo Geotérmico Domo San Pedro cuenta con una capacidad instalada de 35.5 MW, frente a un "
     "potencial estimado de hasta ~200 MW, lo que sustenta técnica y legalmente el objetivo de "
     "expansión de este trabajo. [VERIFICAR: confirmar cifras de capacidad y potencial con la fuente "
     "oficial de la concesión y precisar que el objeto del título es la explotación del recurso.]"),

    ("h1", "Referencias bibliográficas (formato APA 7a edición)"),
    ("refs",
     [
      "Caine, J. S., Evans, J. P., & Forster, C. B. (1996). Fault zone architecture and permeability "
      "structure. Geology, 24(11), 1025-1028.",
      "Corbo-Camargo, F., Arzate-Flores, J. A., Díaz-Navarro, M. K., Castro-Soto, C. D., "
      "Ávila-Vargas, O., & Reyes-Galmichi, I. (2026). The geothermal system of the San Pedro Dome "
      "constrained by magnetotelluric and lithological information. Geological Society of America "
      "Special Paper 566, 53-67. https://doi.org/10.1130/2026.2566(04)",
      "Ferrari, L., Pasquarè, G., Venegas, S., Castillo, D., & Romero, F. (1994). Regional tectonics "
      "of western Mexico and its implications for the northern boundary of the Jalisco block. "
      "Geofísica Internacional, 33(1), 139-151.",
      "Ferrari, L., Petrone, C. M., Francalanci, L., Tagami, T., Eguchi, M., Conticelli, S., "
      "Manetti, P., & Venegas-Salgado, S. (2003). Geology of the San Pedro-Ceboruco graben, western "
      "Trans-Mexican Volcanic Belt. Revista Mexicana de Ciencias Geológicas, 20(3), 165-181.",
      "Frey, H. M., Lange, R. A., Hall, C. M., & Delgado-Granados, H. (2004). Magma eruption rates "
      "constrained by 40Ar/39Ar chronology and GIS for the Ceboruco-San Pedro volcanic field, "
      "western Mexico. GSA Bulletin, 116(3-4), 259-276. [VERIFICAR datos completos]",
      "Gómez-Cruz, A. (2019). Caracterización mineralógica y geotermométrica de muestras de pozo del "
      "campo geotérmico Domo San Pedro, Nayarit [Tesis]. Universidad Nacional Autónoma de México.",
      "Guillou-Frottier, L., et al. (2024). On the hydro-thermal conditions required for spontaneous "
      "convection in fault damage zones. Comptes Rendus Géoscience.",
      "Moeck, I. S. (2014). Catalog of geothermal play types based on geologic controls. Renewable "
      "and Sustainable Energy Reviews, 37, 867-882.",
      "Moeck, I. S., & Beardsmore, G. (2014). A new 'geothermal play type' catalog: Streamlining "
      "exploration decision making. 39th Workshop on Geothermal Reservoir Engineering, Stanford "
      "University, SGP-TR-202.",
      "Muñoz-Burbano, F., et al. (2024). Using time-lapse seismic velocity changes to monitor the "
      "Domo de San Pedro geothermal field, Mexico. Geothermics, 120, 103010. "
      "https://doi.org/10.1016/j.geothermics.2024.103010",
      "Petrone, C. M., Francalanci, L., Ferrari, L., & Schaaf, P. (2001). Volcanic systems in the "
      "San Pedro-Ceboruco graben (western Trans-Mexican Volcanic Belt). Journal of Volcanology and "
      "Geothermal Research, 110(1-2), 35-64.",
      "Petrone, C. M., et al. (2006). The San Pedro-Cerro Grande volcanic complex (Nayarit, Mexico). "
      "Geological Society of America Special Paper 402. [VERIFICAR datos completos]",
      "Reyes-Orozco, A., et al. (2019). Preliminary conceptual model of the Domo San Pedro "
      "geothermal field, Nayarit, Mexico. 44th Workshop on Geothermal Reservoir Engineering, "
      "Stanford University.",
      "Rodríguez, et al. (2019). Preliminary geochemical model of the Domo San Pedro geothermal "
      "field, Nayarit, Mexico. 44th Workshop on Geothermal Reservoir Engineering, Stanford "
      "University.",
      "Ruiz Mendoza, V. (2022). Geología, geoquímica y geocronología del área de Compostela, "
      "Nayarit: implicaciones en la evolución del Rift Tepic-Zacoalco [Tesis]. Universidad Nacional "
      "Autónoma de México.",
      "Schaaf, P., et al. (1995). [Edades U-Pb del batolito de Jalisco — VERIFICAR cita completa].",
     ]),
]


# ---------------------------------------------------------------------------
# HELPERS WORD
# ---------------------------------------------------------------------------

def set_cell_shading(cell, color_hex):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), color_hex)
    shd.set(qn("w:val"), "clear")
    cell._tc.get_or_add_tcPr().append(shd)


def add_run_with_marks(paragraph, texto, base_color=COLOR_GRIS, size=11):
    """Escribe un párrafo resaltando en rojo los tramos [VERIFICAR: ...]."""
    i = 0
    while i < len(texto):
        ini = texto.find("[VERIFICAR", i)
        if ini == -1:
            r = paragraph.add_run(texto[i:])
            r.font.size = Pt(size); r.font.color.rgb = base_color
            break
        # texto normal antes de la marca
        if ini > i:
            r = paragraph.add_run(texto[i:ini])
            r.font.size = Pt(size); r.font.color.rgb = base_color
        fin = texto.find("]", ini)
        if fin == -1:
            fin = len(texto) - 1
        r = paragraph.add_run(texto[ini:fin + 1])
        r.font.size = Pt(size); r.font.italic = True; r.font.color.rgb = COLOR_VERIFICAR
        i = fin + 1


def render_docx():
    doc = Document()
    for s in doc.sections:
        s.top_margin = Cm(2.5); s.bottom_margin = Cm(2.5)
        s.left_margin = Cm(3.0); s.right_margin = Cm(2.5)

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(TITULO); r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = COLOR_UNAM_AZUL
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(SUBTITULO); r.font.size = Pt(10); r.font.color.rgb = COLOR_GRIS_CLARO
    doc.add_paragraph()

    for b in CONTENIDO:
        t = b[0]
        if t in ("h1", "h2", "h3"):
            lvl = {"h1": 1, "h2": 2, "h3": 3}[t]
            h = doc.add_heading(b[1], level=lvl)
            for run in h.runs:
                run.font.color.rgb = COLOR_UNAM_AZUL
        elif t == "p":
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            add_run_with_marks(p, b[1])
        elif t == "verificar":
            p = doc.add_paragraph()
            r = p.add_run("NOTA DE TRABAJO — " + b[1])
            r.font.size = Pt(9); r.font.italic = True; r.font.color.rgb = COLOR_VERIFICAR
        elif t == "lista":
            for item in b[1]:
                p = doc.add_paragraph(style="List Bullet"); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                add_run_with_marks(p, item)
        elif t == "tabla":
            _tabla(doc, b[1], b[2]); doc.add_paragraph()
        elif t == "refs":
            for ref in b[1]:
                p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.left_indent = Cm(0.75)
                p.paragraph_format.first_line_indent = Cm(-0.75)
                add_run_with_marks(p, ref, size=10)

    doc.save(str(OUTPUT_DOCX))
    print(f"Word generado:     {OUTPUT_DOCX}")


def _tabla(doc, encabezados, filas):
    tb = doc.add_table(rows=1, cols=len(encabezados))
    tb.style = "Light Grid Accent 1"
    hdr = tb.rows[0].cells
    for i, h in enumerate(encabezados):
        hdr[i].text = ""
        rr = hdr[i].paragraphs[0].add_run(h)
        rr.font.bold = True; rr.font.size = Pt(10); rr.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_shading(hdr[i], "002B5C")
    for fila in filas:
        celdas = tb.add_row().cells
        for i, val in enumerate(fila):
            celdas[i].text = ""
            rr = celdas[i].paragraphs[0].add_run(str(val))
            rr.font.size = Pt(10); rr.font.color.rgb = COLOR_GRIS


def render_md():
    L = [f"# {TITULO}", "", f"*{SUBTITULO}*", "", "---", ""]
    for b in CONTENIDO:
        t = b[0]
        if t == "h1":
            L += [f"## {b[1]}", ""]
        elif t == "h2":
            L += [f"### {b[1]}", ""]
        elif t == "h3":
            L += [f"#### {b[1]}", ""]
        elif t == "p":
            L += [b[1], ""]
        elif t == "verificar":
            L += [f"> **NOTA DE TRABAJO —** {b[1]}", ""]
        elif t == "lista":
            for item in b[1]:
                L.append(f"- {item}")
            L.append("")
        elif t == "tabla":
            enc, filas = b[1], b[2]
            L.append("| " + " | ".join(enc) + " |")
            L.append("| " + " | ".join(["---"] * len(enc)) + " |")
            for fila in filas:
                L.append("| " + " | ".join(str(v) for v in fila) + " |")
            L.append("")
        elif t == "refs":
            for ref in b[1]:
                L.append(f"- {ref}")
            L.append("")
    OUTPUT_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"Markdown generado: {OUTPUT_MD}")


def main():
    render_docx()
    render_md()


if __name__ == "__main__":
    main()
