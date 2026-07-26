================================================================================
  CAPA 03: GEOLOGÍA — CONTACTOS CON FUENTE DE CALOR
  Dominio de profundidad: SUPERFICIAL a SUBSUPERFICIAL
                          (contactos visibles en superficie que implican
                          cuerpos intrusivos/volcánicos como fuente de calor
                          en profundidad, 0–5 km)
  Peso en el modelo: 5/10 (importancia media)
================================================================================

DESCRIPCIÓN
===========
Mapa geológico del área del Domo San Pedro con énfasis en la identificación
de los contactos entre las unidades volcánicas más recientes (domos, flujos,
intrusivos someros) y las rocas encajonantes. Estos cuerpos volcánicos
jóvenes son el MOTOR TÉRMICO del sistema geotérmico: la proximidad a sus
contactos indica mayor probabilidad de un gradiente geotérmico elevado.

QUÉ DATOS COLOCAR AQUÍ
========================
- Mapa geológico en formato vectorial (polígonos de unidades litológicas).
- Líneas de contacto entre unidades volcánicas recientes y rocas más antiguas.
- Opcional: mapa solo con los contactos de interés ya extraídos como líneas.

UNIDADES DE INTERÉS PARA EL DOMO SAN PEDRO
============================================
- El domo principal (riolítico/dacítico): su contacto es prioritario
- Otros domos o flujos volcánicos recientes en la zona
- Intrusivos someros inferidos (si hay evidencia geofísica)
- Flujos de lava recientes (< 1 Ma)
- Depósitos piroclásticos asociados a actividad reciente

ATRIBUTOS DESEABLES
====================
- Nombre de la unidad litológica
- Composición (riolita, dacita, andesita, basalto)
- Edad (absoluta K-Ar/Ar-Ar si disponible, o relativa)
- Tipo de contacto (intrusivo, depositacional, falla)
- Fuente del dato

CONSIDERACIONES PARA QUE EL DATO SEA VÁLIDO
============================================
1. Solo incluir unidades JÓVENES (idealmente < 1–2 Ma) como proxy de fuente
   de calor. Un intrusivo de 10 Ma ya se enfrió y no contribuye al sistema
   geotérmico actual.

2. El contacto relevante es el BORDE del cuerpo volcánico reciente, no su
   centro. La distancia se calcula al contacto más cercano.

3. Si el Domo San Pedro es efectivamente un domo volcánico reciente, su
   perímetro completo debe digitalizarse con precisión como la fuente de
   calor principal.

4. La escala del mapa geológico debe ser al menos 1:50,000. Idealmente
   1:25,000 o mejor para un estudio a nivel de campo geotérmico.

5. IMPORTANTE: En el modelo, se calculará la DISTANCIA EUCLIDIANA desde cada
   píxel hasta el contacto volcánico reciente más cercano:
   - ≤ 100 m → Score 10
   - 100–200 m → Score 8
   - > 200 m → Score 0

6. Si existen MÚLTIPLES domos/cuerpos recientes, todos deben incluirse.
   El cálculo de distancia encontrará automáticamente el más cercano.

FUENTES SUGERIDAS
=================
- Cartas geológico-mineras del SGM escala 1:50,000
- Tesis de licenciatura/maestría sobre la geología del área
- Publicaciones en revistas (buscar: "Domo San Pedro" + geología)
- Carta geológica de la Serie Vulcanológica (si existe)
- Interpretación de imágenes satelitales + verificación de campo
- Base GeoInfoMex del SGM (datos descargables en línea)

================================================================================
