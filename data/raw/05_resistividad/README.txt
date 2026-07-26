================================================================================
  CAPA 05: RESISTIVIDAD ELÉCTRICA
  Dominio de profundidad: PROFUNDIDAD (500–3000 m)
                          Representa condiciones del RESERVORIO geotérmico
  Peso en el modelo: 9/10 (MÁXIMA importancia)
================================================================================

DESCRIPCIÓN
===========
Mapa de resistividad eléctrica aparente del subsuelo a profundidades
correspondientes al reservorio geotérmico. Es la capa con MAYOR PESO en el
modelo porque la baja resistividad es el mejor indicador geofísico directo
de la presencia de fluidos geotérmicos calientes y/o minerales de alteración
hidrotermal en profundidad.

La baja resistividad (< 10–20 Ω·m) se asocia con:
- Agua salina caliente saturando los poros/fracturas de la roca
- Minerales arcillosos de alteración (esmectita, illita, clorita)
- Combinación de ambos (caso más común en reservorios geotérmicos)

QUÉ DATOS COLOCAR AQUÍ
========================
- Mapa de contornos de isoresistividad (formato vectorial: isolíneas)
- Mapa raster interpolado de resistividad aparente
- Datos puntuales de sondeos (SEV, MT) con coordenadas y valores

MÉTODOS GEOFÍSICOS VÁLIDOS (en orden de preferencia)
=====================================================

1. MAGNETOTELÚRICA (MT / AMT):
   - Profundidad de investigación: 500 m a > 10 km
   - Mejor resolución en profundidad para sistemas geotérmicos
   - Proporciona modelos 1D, 2D o 3D de resistividad
   - IDEAL para este proyecto

2. TRANSITORIO ELECTROMAGNÉTICO (TEM / TDEM):
   - Profundidad de investigación: 50–1500 m
   - Buena resolución del conductor somero (cap clay)
   - Complementario a MT

3. SONDEOS ELÉCTRICOS VERTICALES (SEV Schlumberger):
   - Profundidad de investigación: depende de AB/2
   - Para reservorios a 1–2 km se requiere AB/2 ≥ 1 km
   - Método usado por Prol-Ledesma (2000) en Los Azufres
   - Limitado en terrenos abruptos y con heterogeneidades laterales

4. CSAMT (Controlled Source Audio-frequency Magnetotellurics):
   - Profundidad: 200–2000 m
   - Buena opción intermedia

PROFUNDIDAD OBJETIVO
====================
El mapa de resistividad debe representar condiciones a la PROFUNDIDAD
ESTIMADA del reservorio. Para el Domo San Pedro, esto depende del modelo
geológico, pero típicamente:

- Si se usan SEV: usar AB/2 = 1–2 km (investiga ~500–1500 m)
- Si se usa MT: seleccionar el periodo que corresponda a 500–2000 m
  según el modelo de inversión
- Si se usa TEM: usar tiempos tardíos que representen > 500 m

UMBRALES DE CLASIFICACIÓN
==========================
Basados en la experiencia en campos geotérmicos mexicanos:

| Resistividad (Ω·m) | Interpretación | Score |
|---------------------|----------------|-------|
| ≤ 10                | Zona conductora: probable reservorio activo | 10 |
| 10–20               | Zona de transición: posible extensión del reservorio | 8 |
| > 20                | Zona resistiva: sin evidencia de fluidos calientes | 0 |

NOTA: Estos umbrales son orientativos y pueden ajustarse según el contexto
geológico local del Domo San Pedro. En algunos campos los umbrales son
diferentes (por ejemplo, ≤5 y 5–15 Ω·m).

CONSIDERACIONES PARA QUE EL DATO SEA VÁLIDO
============================================
1. PROFUNDIDAD CORRECTA: Asegurarse de que el mapa represente la profundidad
   del reservorio, NO la resistividad somera. Una capa de arcillas superficiales
   puede dar baja resistividad sin relación con el reservorio.

2. AMBIGÜEDAD: La baja resistividad puede indicar:
   a) Fluidos calientes ACTIVOS (favorable) ← lo que buscamos
   b) Alteración RELICTA de un sistema extinto (falso positivo)
   Para discriminar se necesita gradiente geotérmico (Capa 09, opcional).

3. COBERTURA ESPACIAL: El mapa debe cubrir toda el área de estudio.
   Si solo hay datos puntuales dispersos, la interpolación será menos
   confiable en las zonas sin mediciones.

4. Si se usan datos de MT, preferir los resultados de INVERSIÓN 2D o 3D
   sobre las curvas de resistividad aparente sin procesar.

5. Si solo hay datos de SEV, verificar que el espaciamiento entre sondeos
   sea adecuado para la resolución del modelo (idealmente < 500 m entre
   puntos de medición).

6. IMPORTANTE: A diferencia de las otras capas, aquí NO se calcula distancia.
   Se usa directamente el VALOR de resistividad en cada píxel:
   - ≤ 10 Ω·m → Score 10
   - 10–20 Ω·m → Score 8
   - > 20 Ω·m → Score 0

7. Si no se cuenta con datos de resistividad propios, explorar si existen
   estudios previos de CFE, universidades o empresas de consultoría.

FUENTES SUGERIDAS
=================
- Campañas geofísicas propias (MT, TEM, SEV)
- Gerencia de Geotermia de CFE (datos históricos)
- Publicaciones académicas sobre geofísica del Domo San Pedro
- Tesis de maestría/doctorado con datos de MT o SEV en la zona
- Datos de exploración minera que incluyan resistividad (a veces disponibles)
- Convenios con universidades (UNAM-IGF, CICESE, IPN)

NOTA CRÍTICA
============
Si NO se dispone de datos de resistividad, el modelo Index Overlay pierde
su capa de mayor peso. En ese caso se puede:
a) Ejecutar el modelo sin esta capa (con resultado degradado)
b) Sustituir por otra evidencia de profundidad (gradiente geotérmico,
   anomalías gravimétricas residuales)
c) Realizar una campaña geofísica antes de aplicar el modelo

La opción (c) es la más recomendable si se busca tomar decisiones de
perforación con alto nivel de confianza.

================================================================================
