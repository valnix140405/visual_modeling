# Auditoría cifra por cifra del dashboard (2026-11-24)

Cada cifra se recalculó desde los archivos de `data/` con Python, sin usar `reports/metricas_analisis.json`. Los porcentajes y promedios coinciden dentro del redondeo.

**Abreviaturas:**
- PROFECO = `data/fuente_a/02_datos_gob_profeco/profeco_merida_2026_real.csv`
- CA = cadena «Central de Abasto»
- Súper = giro «Supermercado / Tienda de Autoservicio»
- Conv = giro «Tienda de Conveniencia» (OXXO, 7 Eleven y Dunosusa, según PROFECO)
- Comparable = mismo `producto` + `presentacion`

| HTML | Texto / cifra | Valor recalculado | Archivo origen | Estado | Acción |
|---|---|---|---|---|---|
| index | 19 FUENTES CON DATO REAL · 3 PENDIENTES (encabezado y catálogo) | 16 con dato real + 3 prototipos AR + 3 pendientes | FUENTES_DE_DATOS.md | No coincide | Corregido a «16 con dato real · 3 prototipos AR · 3 pendientes» |
| index | PROFECO mayo 2026 | Fechas 02/05/2026 a 29/05/2026 | PROFECO | Coincide | — |
| index | 139 productos comparables; 103 (74.1%) más caros en súper; mediana +19.0% | 139; 103; 74.1%; +19.0% | PROFECO | Coincide | — |
| index | Cebolla $10.90 Abasto / $29.90 súper (+174% y +174.3%); n=7 y n=47 | 10.90 (n=7) / 29.90 (n=47); +174.3% | PROFECO | Coincide | — |
| index | 1 kg en súper = 2.7 kg en Abasto | 29.90 / 10.90 = 2.74 | PROFECO | Coincide | — |
| index | Arroz 900 g $15.40 → $32.00 (+107.8%), 2.1 bolsas | 15.40 / 32.00; +107.8%; 2.08 | PROFECO | Coincide | — |
| index | Limón persa $21.90 → $35.00 (+59.8%), 1.6 kg | 21.90 / 35.00; +59.8%; 1.60 | PROFECO | Coincide | — |
| index | Frijol negro 900 g +35.3% (gráfica capítulo 2) | 17.00 / 23.00; +35.3% | PROFECO | Coincide | — |
| index | Tortilla 1 kg $28.00 → $13.00 (−53.6%, «54% más barata») | 28.00 / 13.00; −53.6% | PROFECO | Coincide | — |
| index | Papa +11.5%, jitomate −13.5%, pollo −23.5% (gráficas) | 43.00/47.95; 52.00/45.00; 51.00/39.00 | PROFECO | Coincide | — |
| index | 7,520 comercios | 7,520 filas | 01_inegi_denue/denue_merida_alimentos_real.csv | Coincide | — |
| index | 28,288 registros / precios | 28,288 filas | PROFECO | Coincide | — |
| index | 302,092 registros ENOE (hogares + viviendas) | 151,570 + 150,522 = 302,092 | fuente_c/01_enoe_microdatos/*/conjunto_de_datos/*.csv | Coincide | — |
| index | 151,570 hogares | 151,570 filas | conjunto_de_datos_hog_enoe_2025_1t.csv | Coincide | — |
| index | CSV ENOE hogares «15.5 MB» | 15,941,863 bytes = 15.9 MB | mismo | No coincide | Corregido a 15.9 MB |
| index | Conveniencia vs. súper: 93 comparables, 49 más caros, mediana +1.3%, 44 iguales o más baratos | 93; 49; +1.3% (promedios, ≥3 registros); 44 | PROFECO | Coincide | — |
| index | «Donde más se nota»: agua 1 L, yoghurt, agua 600 ml, sopa instantánea | El mayor es suero oral 625 ml (+56.4%: $37.67 vs $24.08, n=3/18); la sopa (+35.1%) es el 5.º | PROFECO | No coincide (lista incompleta) | Se agregó suero oral, se quitó la sopa |
| index | Agua 1 L $19.56 vs $12.76 (+53.3%) | 19.56 / 12.76; +53.3% | PROFECO | Coincide | — |
| index | Yoghurt bebible 220 g $18.30 vs $12.29 (+48.9%) | +48.8% con los promedios sin redondear | PROFECO | No coincide (redondeo) | Corregido a +48.8% |
| index | Agua 600 ml $14.50 vs $10.60 (+36.8%) | 14.50 / 10.60; +36.8% | PROFECO | Coincide | — |
| index | Tortilla $29.50/kg en tortillería | Mediana de 76 registros «Tortillerías», 1 kg a granel = 29.50 | PROFECO | Coincide | — |
| index, looker | Salario mínimo general 2025 $278.80/día | No está en ningún archivo de data/ | Externo: CONASAMI / DOF | No trazable | Marcado «Supuesto:… verificar en CONASAMI/DOF» (3 lugares) |
| index, looker | 3.27 personas por hogar (Censo 2020) | PROM_OCUP = 3.27 (no estaba en data/; sí en el ZIP INEGI) | Censo 2020 AGEB, fila municipal | Antes no trazable; ahora coincide | Se agregaron OCUPVIVPAR y PROM_OCUP a `fuente_a/03_siegy_yucatan/censo2020_totales_municipio_merida.csv` (generar_datos_reales.py); texto ajustado a «ocupantes por vivienda» |
| index, looker | Canasta CONEVAL urbana $2,379.47 (mar 2025) | 2,379.47 | 03_siegy_yucatan/coneval_lineas_pobreza_2018_2025.csv | Coincide | — |
| index, looker | Canasta del hogar $7,780.87 | 2,379.47 × 3.27 = 7,780.87 | derivado | Coincide (depende del supuesto 3.27 ✓) | — |
| index | $8,364/mes | 278.80 × 30 | derivado del supuesto | Coincide (aritmética) | — |
| index, looker | 27.9 días ≈ «28 días»; «17.9 días más» | 7,780.87 / 278.80 = 27.91 | derivado del supuesto | Coincide (aritmética) | — |
| index | 8.5 días (canasta individual) | 2,379.47 / 278.80 = 8.53 | derivado | Coincide (aritmética) | — |
| index | 93.0% del sueldo | 7,780.87 / 8,364 = 93.03% | derivado | Coincide (aritmética) | — |
| index | Sobran $583 = 19.8 kg de tortilla | 583.13; 583.13 / 29.50 = 19.77 | derivado | Coincide | — |
| index | Pollo $39.00/kg, 1.1 h de trabajo | Mediana súper pollo entero = 39.00; 39 / (278.80 / 8) = 1.12 h | PROFECO | Coincide | — |
| index | Tienditas: AUD-01 tortilla $26, huevo kg $50, Bimbo $55; AUD-02 leche $25, panal $80, Bimbo $58; AUD-03 leche $28, huevo kg $48, Bimbo $60; AUD-04 leche $25, panal $88, Bimbo $60; AUD-05 tortilla $27, panal $85, Bimbo $60 | Idénticos | fuente_b/07_bitacora_tienditas/bitacora_precios_tienditas.csv | Coincide | — (AUD-04 «leche» es NUTRI, no LALA: el texto dice solo «Leche») |
| index | Panal Mercedes Barrera $88 = 3.4 kg tortilla; Bimbo $60 = 2.3 kg | 88 / 26 = 3.38; 60 / 26 = 2.31 (tortilla de tiendita AUD-01) | bitácora | Coincide | — |
| index | Mérida 17 × 17 km: 1.8 m a 18 m, desnivel 16 m, pendiente mediana 0.07° | 1.83; 18.0; 16.17; 0.07 | fuente_c/08_opentopography/topografia_merida_vs_ciudades_montana.csv | Coincide | — |
| index | Desniveles: San Cristóbal 1,413; Monterrey 1,292; Guanajuato 853; Toluca 457; CDMX 243; Mérida 16 m | 1,413; 1,292; 853; 457.4; 243; 16.17 | mismo | Coincide | — |
| index | «87 veces menor» | 1,413 / 16.17 = 87.4 | mismo | Coincide | — |
| index | Centro: Lucas de Gálvez 11.3 m; malla 7.8 a 12.7 m | 11.31; 7.77; 12.74 | fuente_b/08_lidar_cem_mde/elevacion_centro_merida_grid.csv | Coincide | — |
| index | 1,681 puntos (08-B); 2,500 puntos (08-C, .ply); 2,400 puntos en 6 ciudades | 1,681; 2,500; 2,400 | .ply y CSV de 08-B y 08-C | Coincide | — |
| index | Va y Ven: 565 elementos = 500 paradas, 18 rutas, 47 otros | 565; 500 highway=bus_stop; 18 type=route; 47 sin etiquetas | fuente_c/04_transporte_vayven/export.geojson | Coincide | — |
| index | Lucas de Gálvez 817 establecimientos (443 de alimentos) | 817 / 443 | fuente_a/04_geoportal_merida/mercados_publicos_merida_denue.geojson | Coincide | — |
| index | 15 mercados públicos; radio 800 m | 15 elementos; 800 m es parámetro de diseño del visor | mismo | Coincide | — |
| index | 06-A «69 combinaciones producto-cadena» | 62 filas (tras unificar la presentación) | fuente_a/06_scraping_autoservicios/precios_canasta_supermercados_reales.csv | No coincide | Corregido a 62 |
| index | 09-A 4 anclas; 09-B 4 modelos | 4 elementos; 4 .glb | 09_ar_anclas, 09_ar_modelos_3d | Coincide (prototipo) | — |
| index | 01-B 32 clases SCIAN | 32 filas | fuente_b/01_inegi_saic/censos_economicos_2019_merida_comercio_alimentos.csv | Coincide | — |
| index | 02-B 776 precios | 776 filas | fuente_b/02_datos_gob_sniim/profeco_central_abasto_merida_2026.csv | Coincide | — |
| index | 03-B 526 AGEB | 526 filas | fuente_b/03_conapo_marginacion/censo2020_indicadores_ageb_merida.csv | Coincide | — |
| index | 06-B 5,864 precios | 5,864 filas | fuente_b/06_scraping_farmacias/profeco_farmacias_conveniencia_merida_2026.csv | Coincide | — |
| index | 02-C «4,064 artículos» | 4,063 filas de datos | fuente_c/02_diconsa_segalmex/DICONSA_8_Listado_de_articulos_por_proveedor.csv | No coincide | Corregido a 4,063 |
| index | Conteos del catálogo: Todas (22), A (7), B (8), C (7) | 22 / 7 / 8 / 7 | FUENTES_DE_DATOS.md | Coincide | — |
| looker | Encabezado «19 fuentes con dato real y 3 pendientes» / «ESTADO: 19 CON DATO REAL» | 16 + 3 prototipos + 3 pendientes | FUENTES_DE_DATOS.md | No coincide | Corregido (2 lugares) |
| looker | 7,520; 28,288; +19.0%; 139; 74.1% | igual que en index | DENUE, PROFECO | Coincide | — |
| looker | Mercados: 1,661 establecimientos DENUE | 1,661 (suma de 15 mercados) | mercados_publicos_merida_denue.geojson | Coincide | — |
| looker | Gráfica rango Abasto → súper (8 productos) | Cebolla 10.9/29.9; col blanca 10.0/23.9 (+139%); arroz; limón; frijol; papa; jitomate 52/45; tortilla 28/13 | PROFECO | Coincide | Las barras son flotantes [mín, máx]; el signo lo da la etiqueta |
| looker | Censos Económicos 2019, ingresos (mdp): súper 15,338.6 (78); minisúper 6,290.4 (700); cerveza 1,498.5 (1,476); abarrotes 1,291.7 (3,113); carnes 1,288.8 (671); frutas y verduras 632.6 (764) | Idénticos | 01_inegi_saic/censos_economicos_2019_merida_comercio_alimentos.csv | Coincide | — |
| looker | Tiendita vs. súper: leche LALA $26 (n=4) vs $37 (n=24) −29.7% | Tiendita LALA 26, 25, 28, 26 → mediana 26, n=4; súper «Caja 1 Lt. Entera» LALA mediana 37, n=24 | bitácora + PROFECO | Coincide | — |
| looker | Frijol $28 (n=5) vs $25.56 (n=39) +9.6% | Mediana 28, n=5; súper 23.00 / 0.9 kg = 25.56, n=39 | bitácora + PROFECO | Coincide | — |
| looker | Pan Bimbo $60 (n=5) vs $43 (n=41) +39.5% | 60, n=5; «Paquete Grande 620 Gr. Rebanado Blanco» 43, n=41 | bitácora + PROFECO | Coincide | — |
| looker | Tortilla $26.50 (n=2) vs $13 (n=43) +103.8% | 26.5, n=2; 13, n=43 | bitácora + PROFECO | Coincide | — |
| looker | Mapa: 65 nodos | 65 puntos embebidos = 65 filas | reports/looker_studio/looker_02_territorio_geo.csv | Coincide | — |
| looker | Serie CONEVAL 2018–2025 (87 meses, urbana y rural); +57.1% | Arreglos idénticos al CSV; 2,379.47 / 1,514.91 − 1 = 57.1% | coneval_lineas_pobreza_2018_2025.csv | Coincide | — |
| looker | Censo 2020 Mérida: 995,129; PEA 527,424; sin afiliación 22.2%; internet 76.3% | 995,129; 527,424; 22.16%; 76.29% | censo2020_totales_municipio_merida.csv | Coincide | — |
| looker | 12 de 520 AGEB con más de 40% sin afiliación | 12 (de 515 con dato; 520 con población) | censo2020_indicadores_ageb_merida.csv | Coincide | — |
| looker | Bitácora embebida (25 filas) | Idéntica al CSV | bitácora 07-B | Coincide | — |
| visor relieve | Exageración ×40 (Centro) y ×150 (Mérida) | Parámetros de visualización explicados en pantalla | — | No aplica (parámetro) | — |
| visor mercados | 1,661 establecimientos; 813 de alimentos y bebidas | 1,661; 813 | mercados_publicos_merida_denue.geojson | Coincide | — |
| visores AR (4) | Precios y ahorros de demo ($1,420, $520, etc.) | Ilustrativos | — | Prototipo marcado | Los 4 visores llevan la nota «Prototipo de diseño… no datos de una fuente oficial» |
| visor_ar_unificado | Jitomate $52.00 y limón $21.90 (PROFECO) | 52.00 y 21.90 en CA | PROFECO | Coincide | Observación: el texto los cita dentro del recorrido por Lucas de Gálvez, pero son precios de la Central de Abasto (el texto lo aclara) |
| visor_ar_unificado | Huevo $48/kg, «ahorra hasta $14 por kilo» | 48 = tiendita AUD-03, no un puesto del mercado; $14 sin origen | — | Ilustrativo bajo nota de prototipo | Sin cambio (dentro del prototipo) |

## Resumen

- Cifras o grupos de cifras auditados: 92 cifras individuales en 65 filas.
- Coinciden: 82.
- Corregidas: 9 (19 → 16 fuentes con dato real, en 4 lugares; 69 → 62; 15.5 → 15.9 MB; 4,064 → 4,063; lista de conveniencia sin el suero oral; yoghurt +48.9 → +48.8%).
- No trazables a un archivo de data/:
  - Salario mínimo $278.80: marcado como Supuesto con la fuente que hay que verificar (CONASAMI/DOF).
  - 3.27 ocupantes: ahora trazable porque se agregó PROM_OCUP al CSV municipal.
- Prototipos AR: ilustrativos y marcados.
