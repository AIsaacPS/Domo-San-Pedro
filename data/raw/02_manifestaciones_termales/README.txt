================================================================================
  CAPA 02: MANIFESTACIONES TERMALES SUPERFICIALES
  Dominio de profundidad: SUPERFICIAL (observaciones directas en superficie, 0 m)
  Peso en el modelo: 5/10 (importancia media)
================================================================================

DESCRIPCIÓN
===========
Inventario georreferenciado de todas las manifestaciones hidrotermales
visibles en superficie en el área del Domo San Pedro. Estas manifestaciones
son indicadores directos del flujo ascendente de fluidos desde el reservorio
geotérmico hacia la superficie.

QUÉ DATOS COLOCAR AQUÍ
========================
- Archivos vectoriales con la ubicación de manifestaciones termales.
- Pueden ser puntos (manifestaciones puntuales) o polígonos (zonas extensas
  de alteración, suelo vaporante, etc.)

TIPOS DE MANIFESTACIONES A INCLUIR
====================================
- Manantiales calientes (hot springs) — indicar temperatura
- Fumarolas (emisiones de vapor y gases)
- Suelo vaporante (steaming ground)
- Pozas de lodo (mud pools)
- Zonas de alteración hidrotermal visible (caolinización, silicificación)
- Depósitos de sínter o travertino
- Zonas con vegetación anómala por calor en el suelo
- Emanaciones de CO2 o H2S

ATRIBUTOS DESEABLES
====================
- Tipo de manifestación
- Coordenadas (GPS, precisión < 10 m)
- Temperatura medida (°C)
- pH del fluido (si aplica)
- Caudal estimado (L/s, si aplica)
- Composición química básica (si disponible)
- Extensión aproximada (m²)
- Fecha de observación
- Fuente/referencia

CONSIDERACIONES PARA QUE EL DATO SEA VÁLIDO
============================================
1. Incluir TODAS las manifestaciones, sin importar su tamaño. Una pequeña
   fumarola puede indicar una zona de alta permeabilidad en profundidad.

2. No asignar valores diferentes a los distintos tipos de manifestación.
   Según el modelo conceptual (topografía abrupta, sistema dominado por vapor),
   todas las manifestaciones están igualmente relacionadas con el flujo
   ascendente del sistema.

3. Verificar que las coordenadas sean precisas. Un error de 100 m en la
   ubicación puede cambiar significativamente el resultado del modelo.

4. Si se usan polígonos (zonas de alteración), calcular la distancia al
   borde del polígono, no al centroide.

5. IMPORTANTE: En el modelo, se calculará la DISTANCIA EUCLIDIANA desde cada
   píxel hasta la manifestación más cercana:
   - ≤ 100 m → Score 10
   - 100–200 m → Score 8
   - > 200 m → Score 0

6. Las manifestaciones EXTINTAS o relictas (sin actividad actual) deben
   marcarse como tales. Pueden indicar auto-sellado y NO necesariamente
   favorabilidad actual.

FUENTES SUGERIDAS
=================
- Trabajo de campo con GPS
- Inventario Nacional de Manifestaciones Termales (SGM/UNAM)
- Publicaciones sobre el Domo San Pedro
- Imágenes satelitales térmicas nocturnas (ASTER TIR, Landsat Band 10)
- Reportes de exploración de CFE o empresas privadas

================================================================================
