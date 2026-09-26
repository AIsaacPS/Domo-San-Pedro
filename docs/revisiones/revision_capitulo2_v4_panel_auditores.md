# Revisión del Capítulo II (v4) — Panel de 7 auditores especializados

**Documento revisado:** `BIBLIOGRAFIA/capitulo_2_descripcion_zona_estudio-v4.txt`
**Tesina:** "Determinación de nuevas zonas favorables para la expansión del Campo Geotérmico Domo San Pedro, Nayarit, México"
**Método:** cada auditor verificó las afirmaciones contra la bibliografía real del proyecto (`docs/extracted-text/`) y pudo buscar referencias reales en web.

> Este es un informe de **revisión** (no una reescritura). Cada hallazgo trae la cita, qué dice la fuente real y una corrección concreta. El autor decide qué aplicar.

---

## RESUMEN EJECUTIVO

El capítulo tiene una estructura sólida y buena cobertura. Sin embargo, el panel detectó **varios errores críticos consistentes entre auditores** (lo que les da alta confiabilidad). Los más graves son geocronológicos, de atribución de citas y de sobreafirmación de la fuente de calor.

### Hallazgos de CONSENSO (detectados por 2+ auditores — máxima prioridad)

| # | Hallazgo | Detectado por |
|---|----------|---------------|
| A | **Fuente de calor magmática presentada como hecho**, cuando Corbo (2026) dice que es desconocida. Reformular como inferencia. | Geofísica, Vulcanología, Geología, Geotermia |
| B | **Edad del colapso caldérico mal fechada** (~1.1 Ma). Las fuentes acotan ~450–283 ka (Petrone 2006; Ferrari 2003). El 1.1 Ma es un dato viejo/descartado. | Vulcanología, Geología |
| C | **Cerro Las Tetillas (~2.3 Ma) mal clasificado como post-caldera**: es pre-caldera (el domo más antiguo), y además hay redatación a ~0.45 Ma (Frey 2004). | Vulcanología, Geología |
| D | **Ubicación errónea:** dice "sector noroccidental" del graben; Corbo (2026) lo sitúa en el **límite nororiental** (falla Milpillas-Cerro Grande). | Geofísica, Geología, Geotermia |
| E | **Rango de resistividad del reservorio (30–100 Ω·m)** bien citado de Corbo, pero contradice la ventana **20–50 Ω·m** del README/modelo. Reconciliar. | Geofísica, SIG |
| F | **Tensor de esfuerzos σ₃ NNE-SSW mal atribuido a Muñoz-Burbano (2024)**, que es un estudio de sismicidad/dv-v, no de paleoesfuerzos. | Geofísica, Vulcanología, (Estructural relacionado) |
| G | **Wairakita mal atribuida**: el capítulo la pone en el basamento profundo como "alta temperatura"; Gómez-Cruz (2019) la reporta solo en SP05 (~800–1000 m) y como zeolita de temperatura INTERMEDIA. | Geoquímica, (coincide con revisión previa) |
| H | **Expansión al centro/SE**: el capítulo la usa como continuidad del reservorio; Corbo distingue dos reservorios (GR-1 Domo San Pedro vs. GR-2 Amado Nervo), y parte del conductor profundo puede ser mineralización magnética, no reservorio. | Geofísica, Geotermia |

---

## HALLAZGOS POR AUDITOR

### Auditor 1 — Geología de México

- **[CRÍTICO]** Equipara Graben de Compostela = Graben de San Pedro-Ceboruco. Ferrari (2003) y Corbo (2026): Compostela es solo el segmento occidental del SPC (que tiene 3 segmentos).
- **[CRÍTICO]** Ubica el campo en "sector noroccidental"; Corbo lo sitúa en el límite **nororiental** (falla Milpillas-Cerro Grande).
- **[CRÍTICO]** Omite la edad Oligoceno–Mioceno temprano (~34–19 Ma) de la SMO; usa edades del batolito (75–56 Ma / >85 Ma) no atribuibles a Ferrari 2003, que reporta U-Pb ~100–90 Ma (Schaaf) y K-Ar 90–50 Ma.
- **[MAYOR]** Mezcla dos referencias "Ferrari et al. 2003" y atribuye mal el modelo "slab window".
- **[MAYOR]** Cerro Las Tetillas solo como ~2.3 Ma (Gastil 1979), ignorando la redatación ⁴⁰Ar/³⁹Ar de 0.45±0.19 Ma (Frey en Ferrari 2003).
- **[MAYOR]** La "Etapa Pre-Caldera" mezcla estratigrafía regional con el edificio SCVC cuaternario.
- **Correctos:** edades San Pedro 0.041 Ma, Los Ocotes 0.1 Ma, Amado Nervo 0.22 Ma, subsidencia 1,100 m central.
- **Referencias sugeridas:** Petrone et al. 2006 (GSA SP 402, VERIFICADA, falta en la lista); Ferrari/Petrone/Francalanci JVGR 126 2003 (para desambiguar slab window); Schaaf et al. 1995 (edades U-Pb del batolito).

### Auditor 2 — Geotermia en México

- **[CRÍTICO]** La clasificación "play híbrido CV1/CV3" es contradictoria en Moeck: CV3 (dominio extensional) es por definición NO magmático; CV1 es magmático (ramas opuestas). Los códigos CV1/CV3 provienen de Moeck & Beardsmore (2014, WGC), referencia ausente. Propuesta: reclasificar como play magmático CV1 con el control extensional como mecanismo de permeabilidad secundaria.
- **[CRÍTICO]** La justificación de expansión tergiversa a Corbo: la anomalía al S/SE corresponde a un reservorio SEPARADO (GR-2, Amado Nervo), distinto del DSP (GR-1). El paper no sustenta expansión del DSP hacia el SE; GR-2 probablemente cae fuera de la concesión.
- **[MAYOR]** Ubicación "noroccidental" errónea → nororiental.
- **[MAYOR]** Ausencia del marco legal/comercial/operativo (Grupo Dragón, concesión SENER 129.18 km², 35.5 MW, potencial ~200 MW). Propone añadir subsección 2.4.
- **[MAYOR]** No distingue área de estudio SIG (300 km²) de área concesionada (129.18 km²), ni define CRS/resolución.
- **[MENOR]** Yacimiento somero ~280 °C sobreestimado (SP06 ~260 °C). Precisar "explotación" vs "exploración" en el objeto de concesión.
- **Referencias sugeridas (VERIFICADAS):** Moeck & Beardsmore (2014, SGP-TR-202); Moeck et al. (2015, WGC Melbourne). SUGERENCIA: "Mexican Geothermal Plays" (WGC 2015, 11078).

### Auditor 3 — Geoquímica aplicada a la geotermia

- **[CRÍTICO]** Wairakita mal atribuida: el capítulo la pone en el basamento profundo (>1,300 m) como "alta temperatura >240–300 °C". Gómez-Cruz (2019): solo en SP05 (~800–1000 m), zeolita de temperatura **intermedia**, asociada a anhidrita (indicador de permeabilidad, no de alta T). El ensamble propilítico profundo real: epidota + clorita + cuarzo + calcita + pirita/pirrotita (± anfíbol).
- **[CRÍTICO]** La capa sello no es "argílica" según Gómez-Cruz (2019), que la define como subpropilítica (sin argílica bien definida); Reyes-Orozco (2019) sí la llama "clay cap". Reconocer la discrepancia o usar "capa sello arcillosa (esmectita-illita)".
- **[MAYOR]** Yacimiento somero "~280 °C" no verificable: SP06 mide 260 °C; geotermómetros de gas ~225–250 °C.
- **[MAYOR]** "Dos yacimientos interconectados" de igual jerarquía → reformular como "reservorio de líquido dominante con zona bifásica somera/oriental menor" (Rodríguez 2019).
- **[MAYOR]** Precisar que 850–1200 ppm Cl es concentración de RESERVORIO, no de descarga (SP05 en separador ~1658 ppm).
- **[MENOR]** Matices de trazabilidad (domo antiguo SP05-SP06 más frío; epidota bajo isoterma 240 °C; calcita/epidota por ebullición); ambivalencia de ebullición por inclusiones fluidas.
- **Referencias sugeridas (VERIFICADAS):** Liou (1970) estabilidad de wairakita; Zandanel et al. (2025) formación analcima-wairakita 200-300 °C — ambas para sustentar que la wairakita es de temperatura intermedia.

### Auditor 4 — Geofísica aplicada a la geotermia

- **[CRÍTICO]** Fuente de calor magmática presentada como hecho; Corbo (2026) la declara desconocida. Reformular como inferencia.
- **[CRÍTICO]** Rangos de resistividad mal citados: reservorio ~30–<100 Ω·m (no 30–100); propilítico 30–80; techo del basamento ~150 Ω·m (no >1000); bloques compactos >1000 solo al W/NW.
- **[MAYOR]** Ubicación "noroccidental" → nororiental (falla Milpillas-Cerro Grande).
- **[MAYOR]** σ₃ NNE-SSW mal atribuido a Muñoz-Burbano (2024), que es estudio de dv/v, no de tensor de esfuerzos.
- **[MAYOR]** Microsismicidad: solo el clúster somero (0.5–2.5 km) se asocia a operaciones; del profundo (2.5–7 km) los autores no establecen causalidad.
- **[MAYOR]** Expansión al centro/SE: omite que parte del conductor profundo coincide con anomalía magnética (mineralización magnetítica, no necesariamente reservorio) y que Corbo distingue GR-1 vs GR-2 (Amado Nervo). Este matiz refuerza la necesidad del SIG multicriterio.
- **Referencias sugeridas (VERIFICADAS):** completar fichas de Corbo 2026 (DOI 10.1130/2026.2566(04)) y Muñoz-Burbano 2024 (Geothermics 120, 103010); Hering et al. 2021 (MT 3D Ceboruco). SUGERENCIA: Cumming (2009), Ussher et al. (2000) para rangos de resistividad clay cap-reservorio.

### Auditor 5 — SIG aplicado a la geotermia

- **[CRÍTICO]** Ausencia total de marco espacial: no define el área de estudio SIG (rectángulo 300 km², 15×20 km, EPSG:32613, res 30 m) ni la concesión (129.18 km², 7 vértices) como clipping mask, ni distingue ambos dominios. Propone añadir apartado **"2.4 Marco Espacial"**.
- **[CRÍTICO]** Incoherencia de resistividad: capítulo 30–100 Ω·m (correcto de la fuente) vs README 20–50 Ω·m. Reconciliar antes de reclasificar la capa.
- **[MAYOR]** Falta figura de localización (Figura 2.1) con rectángulo, concesión, pozos, fallas, domos, manantiales en UTM 13N.
- **[MAYOR]** Los rasgos que serán capas SIG carecen de ubicación espacial (coordenadas/sector).
- **[MAYOR]** El argumento de expansión centro/SE no se conecta espacialmente con el interior/contigüidad de la concesión (vértices SE en 536557/2341933 y 536736/2335981) ni con la infraestructura.
- **[MENOR]** CRS nunca declarado en el texto; sigla SCVC→SPCG; distancia al Ceboruco inconsistente (10 km SW en el cap. vs 17.5 km NW en concesión).
- **[SUGERENCIA]** Tabla-puente "rasgo descrito → capa SIG futura → geometría → atributo → fuente"; precisar la elevación de cada corte de resistividad.

### Auditor 6 — Vulcanología y neotectónica

- **[CRÍTICO]** Colapso caldérico mal fechado (~1.1 Ma) → ~450–283 ka (Petrone 2006; Ferrari 2003). El 1.1 Ma es hipótesis vieja descartada (correspondía a Amado Nervo peri-caldera).
- **[CRÍTICO]** Cerro Las Tetillas (~2.3 Ma) mal clasificado como post-caldera → es pre-caldera (domo más antiguo); doble datación 2.3 Ma K-Ar vs ~0.45 Ma ⁴⁰Ar/³⁹Ar (Frey 2004).
- **[CRÍTICO]** Diámetro caldérico: 7–10 km (Ferrari 2003) vs ~4 km (Petrone 2006). Declarar la discrepancia, no dar solo una cifra.
- **[CRÍTICO]** Fuente de calor magmática sobreafirmada; "define con precisión" (Corbo 2026) es incorrecto — el propio paper la declara incógnita. Suavizar a inferencia.
- **[MAYOR]** σ₃ NNE-SSW mal atribuido a Muñoz-Burbano (2024).
- **[MAYOR]** Relación esfuerzos-dilatación: bajo σ₃ NNE-SSW, las que más dilatan son las WNW-ESE/NW-SE (perpendiculares a σ₃), no las E-W; separar ese argumento del rol de conductos E-W por reactivación.
- **[MENOR]** Errata "continental continentalmente amplio"; declarar el esquema de etapas adoptado; Amado Nervo Na-alcalino (carácter bimodal).
- **Referencias sugeridas:** Frey et al. (2004, GSA Bulletin 116, fuente ⁴⁰Ar/³⁹Ar de casi todas las edades modernas) — SUGERENCIA a confirmar por el autor; falta en las referencias del capítulo.

### Auditor 7 — Geología estructural del Bloque de Jalisco y Nayarit

- **[CRÍTICO]** Atribuye a Corbo (2026) las fallas E-W Ocotes/Ávalos/Guásimas y la profundidad de 2.5 km, que son de Reyes-Orozco (2019). Corbo nombra Milpillas-Cerro Grande, Borbollón, Amado Nervo y las interpreta como BARRERAS, no conductos.
- **[CRÍTICO]** El modelo núcleo (barrera) / zona de daño (conducto) se atribuye implícitamente a Corbo, cuando es de Caine et al. (1996). Corregir el anclaje conceptual.
- **[CRÍTICO]** Verificar que en ningún punto se afirme el RTZ como dextral activo: Ferrari (1994, 2003) concluye que desde el Mioceno tardío NO hay transcurrencia dextral mayor (extensión pura, σ₃ NNE-SSW). El texto 2.1.2 es correcto, solo confirmar coherencia.
- **[MAYOR]** Inconsistencia MCG: NW-SE/barrera (Corbo) vs "Falla Cerro Grande" E-W (Reyes-Orozco). Compostela/Pedernales son de Reyes-Orozco, no de Corbo.
- **[MAYOR]** Contradicción aparente conducto vs barrera del sistema NW-SE: resolver con el concepto de anisotropía conducto-barrera de Caine.
- **[MENOR]** Los umbrales geométricos de damage zone (>100 m, longitud ≥1 km) son de Guillou-Frottier (2024); atribuir bien. Jerarquía graben Compostela vs SPC.
- **Referencias sugeridas:** Curewitz & Karson (1997, VERIFICADA); Faulds & Hinz (2015, SUGERENCIA); Rowland & Sibson (2004, SUGERENCIA).

---

## PLAN DE ACCIÓN CONSOLIDADO (orden sugerido)

### Prioridad 1 — Críticos de consenso (corregir sí o sí antes de defensa)
1. **Fuente de calor:** reformular como inferencia en toda mención; corregir "define con precisión" (Corbo declara la fuente desconocida). [A]
2. **Geocronología volcánica:** colapso caldérico ~450–283 ka (no 1.1 Ma); Cerro Las Tetillas a pre-caldera con doble datación; declarar discrepancia de diámetro (7–10 vs ~4 km). [B, C]
3. **Ubicación:** cambiar "noroccidental" → "límite nororiental del graben" sobre la falla Milpillas-Cerro Grande. [D]
4. **Atribuciones de cita:** σ₃ NNE-SSW no es de Muñoz-Burbano; fallas E-W/2.5 km son de Reyes-Orozco (no Corbo); modelo core/damage zone es de Caine (no Corbo). [F, Auditor 7]

### Prioridad 2 — Mayores (rigor y coherencia)
5. **Wairakita y capa sello:** reubicar wairakita (SP05, ~800–1000 m, temperatura intermedia); matizar "argílica" vs subpropilítica. [G]
6. **Resistividad:** reconciliar 30–100 Ω·m (fuente) vs 20–50 Ω·m (modelo); precisar techo de basamento ~150 Ω·m. [E]
7. **Expansión centro/SE:** distinguir GR-1 (DSP) de GR-2 (Amado Nervo); advertir anomalía magnética; anclar espacialmente a la concesión e infraestructura. [H]
8. **Play type:** revisar la clasificación CV1/CV3 (son ramas opuestas en Moeck); citar Moeck & Beardsmore (2014).
9. **Marco espacial (SIG):** añadir apartado 2.4 con CRS, área de estudio (300 km²) vs concesión (129.18 km², 7 vértices) como clipping mask.
10. **Marco legal/operativo:** añadir contexto de concesión (Grupo Dragón, SENER, 35.5 MW, potencial ~200 MW).
11. **Temperatura somera:** 280 °C → ~260 °C (SP06) o rango de gases 225–250 °C.

### Prioridad 3 — Menores y sugerencias
12. Figura 2.1 de localización; geolocalizar rasgos; tabla-puente rasgo→capa SIG.
13. Erratas y consistencia: "continental continentalmente amplio", sigla SCVC→SPCG, distancia al Ceboruco (10 km SW vs 17.5 km NW).
14. Completar/corregir fichas bibliográficas: Corbo 2026 (DOI), Muñoz-Burbano 2024 (Geothermics 120, 103010), añadir Frey et al. (2004), Petrone et al. (2006), Moeck & Beardsmore (2014).

---

## REFERENCIAS NUEVAS SUGERIDAS POR EL PANEL

> Marcadas según nivel de confianza. Confirmar datos completos antes de citar.

**Ya deberían estar y faltan en la lista del capítulo:**
- Petrone, C.M. et al. (2006). *The San Pedro-Cerro Grande volcanic complex, Nayarit.* GSA Special Paper 402. (VERIFICADA — está en tu bibliografía)
- Frey, H.M., Lange, R.A., Hall, C.M., Delgado-Granados, H. (2004). *Magma eruption rates... Ceboruco-San Pedro volcanic field.* GSA Bulletin 116(3-4), 259–276. (SUGERENCIA a confirmar — fuente ⁴⁰Ar/³⁹Ar de las edades modernas)
- Moeck, I.S. & Beardsmore, G. (2014). *A new 'geothermal play type' catalog.* Stanford Geothermal Workshop, SGP-TR-202. (VERIFICADA — origen de los códigos CV1/CV3)

**Para reforzar secciones específicas:**
- Hering et al. (2021), MT 3D Ceboruco (VERIFICADA, ya en carpeta 03_GEOFISICA) — análogo regional.
- Moeck et al. (2015), WGC Melbourne (VERIFICADA) — clasificación de plays.
- Liou (1970) y Zandanel et al. (2025) — estabilidad térmica de wairakita (temperatura intermedia).
- Curewitz & Karson (1997) — control estructural de manantiales en zonas de daño / intersecciones de falla.
- Cumming (2009), Ussher et al. (2000) — modelo de resistividad clay cap-reservorio (SUGERENCIA a confirmar).
- Schaaf et al. (1995) — edades U-Pb del batolito de Jalisco (SUGERENCIA a confirmar).

---

*Informe generado por el panel de 7 auditores especializados del proyecto. Fecha: septiembre 2026.*
