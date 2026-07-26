================================================================================
  CAPA 07 (COMPLEMENTARIA): ANOMALÍAS TÉRMICAS SATELITALES
  Dominio de profundidad: SUPERFICIAL (temperatura de superficie, 0 m)
                          Indicador indirecto de flujo de calor desde
                          profundidad
  Peso en el modelo: No participa directamente (complemento/validación)
================================================================================

DESCRIPCIÓN
===========
Mapas de temperatura superficial derivados de imágenes satelitales en el
infrarrojo térmico. Las anomalías térmicas positivas (zonas más calientes
que el entorno) pueden indicar flujo de calor conductivo o convectivo desde
el reservorio geotérmico.

QUÉ DATOS COLOCAR AQUÍ
========================
- Imágenes de temperatura superficial (Land Surface Temperature, LST)
- Mapas de anomalía térmica (residuos después de corregir por elevación)
- Imágenes nocturnas preferidas (menor efecto de insolación)

SENSORES RECOMENDADOS
======================
| Sensor | Banda térmica | Resolución | Acceso |
|--------|---------------|------------|--------|
| ASTER TIR | 10.6–11.3 μm | 90 m | USGS EarthExplorer |
| Landsat 8/9 Band 10 | 10.6–11.2 μm | 100 m | USGS EarthExplorer |
| ECOSTRESS (ISS) | 8–12.5 μm | 70 m | NASA AppEEARS |
| Sentinel-3 SLSTR | 10.8–12 μm | 1 km | Copernicus |

CONSIDERACIONES
===============
1. Usar imágenes NOCTURNAS para minimizar el efecto de la radiación solar.
2. Corregir por ELEVACIÓN (la temperatura disminuye ~6.5°C/km de altitud).
   La anomalía es el residuo después de esta corrección.
3. Usar múltiples fechas y promediar para reducir ruido estacional.
4. Época seca preferida (menor efecto de humedad del suelo).
5. Resolución de 90–100 m es suficiente para identificar anomalías a
   escala de campo geotérmico.
6. Las anomalías térmicas son SUTILES (1–5°C sobre el fondo). Se necesita
   procesamiento cuidadoso para detectarlas.

UTILIDAD PARA EL PROYECTO
==========================
- Validación independiente del modelo Index Overlay
- Identificación de manifestaciones termales no reportadas
- Posible inclusión como capa adicional si se demuestra correlación
  con las zonas de producción

================================================================================
