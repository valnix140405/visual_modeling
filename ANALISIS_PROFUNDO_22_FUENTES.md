# Análisis de las 22 fuentes de datos

## Proyecto: "Del Mundo a la Esquina: ¿Cuánto Cuesta Comer?"

**Equipo:** Valeria Nicol Hernández León (Fuente A) · Jorge Ramiro Chay Koyoc (Fuente B) · Isaac René Andrade Sánchez (Fuente C)

Todas las cifras de este documento se calculan con [`scripts/analisis_profundo_22_fuentes.py`](scripts/analisis_profundo_22_fuentes.py), que guarda los resultados en [`reports/metricas_analisis.json`](reports/metricas_analisis.json). Para reproducirlas:

```bash
python scripts/analisis_profundo_22_fuentes.py
python scripts/generar_graficas_analisis.py
```

**Estado de las fuentes:** 16 de 22 con datos reales en el repositorio; solo esas se usan en el análisis y en el dashboard. Pendientes: 04-B tianguis, 06-C apps de delivery y 08-A LiDAR (`python scripts/verificar_datasets.py`). Las fuentes 09-A, 09-B y 09-C son configuraciones de realidad aumentada diseñadas por el equipo, no datos de una fuente externa.

---

## 1. Hallazgos principales

1. **El supermercado es más caro que la Central de Abasto en 3 de cada 4 productos comparables.** De 139 pares de producto y presentación que PROFECO registró en ambos canales, el supermercado tiene mediana más alta en el 74.1 % de los casos; la diferencia mediana es de +19.0 %. Las brechas mayores están en productos a granel: cebolla blanca +174 % ($10.90 vs. $29.90 por kg), garbanzo +167 % y col +139 %.
2. **La canasta alimentaria urbana subió 57.1 % entre enero de 2018 y marzo de 2025.** Según CONEVAL, pasó de $1,514.91 a $2,379.47 mensuales por persona. La línea de pobreza por ingresos urbana (canasta alimentaria más no alimentaria) llegó a $4,680.15 en marzo de 2025.
3. **El comercio de alimentos de Mérida es de tiendas pequeñas, pero las ventas están en los supermercados.** En el DENUE, el 92.5 % de los 7,520 establecimientos de alimentos tiene de 0 a 5 personas ocupadas. En los Censos Económicos 2019 (año de referencia 2018), las 3,113 tiendas de abarrotes reportan $1,291.7 millones de ingresos, mientras que 78 supermercados reportan $15,338.6 millones.
4. **Comprar en la tiendita no siempre es más caro, pero sí en pan y tortilla.** Con la bitácora propia (5 tiendas, muestras pequeñas) frente a PROFECO: el pan Bimbo grande cuesta 39.5 % más en la tiendita y el frijol por kilo 9.6 % más; la leche LALA de 1 L salió 29.7 % más barata en la tiendita que la mediana de supermercado.
5. **Mérida es plana: 16 m de desnivel en 17 km.** En la malla de elevación, Mérida promedia 9.6 m s. n. m. con pendiente mediana de 0.1°, frente a desniveles de 853 m en Guanajuato y 1,413 m en San Cristóbal de las Casas.

---

## 2. Módulo 1: la realidad económica

### 01. Directorios y censos de empresas (INEGI)

| Indicador | Valor | Archivo |
|---|---:|---|
| Establecimientos de alimentos en Mérida (DENUE) | 7,520 | `data/fuente_a/01_inegi_denue/denue_merida_alimentos_real.csv` |
| Tiendas de abarrotes, ultramarinos y misceláneas | 3,798 | ídem |
| Fruterías y verdulerías | 870 | ídem |
| Carnicerías (carnes rojas) | 669 | ídem |
| Minisupers | 631 | ídem |
| Establecimientos con 0 a 5 personas | 92.5 % | ídem |
| Abarrotes (SCIAN 461110): unidades / personal / ingresos | 3,113 / 5,657 / $1,291.7 mdp | `data/fuente_b/01_inegi_saic/censos_economicos_2019_merida_comercio_alimentos.csv` |
| Supermercados (SCIAN 462111): unidades / personal / ingresos | 78 / 6,838 / $15,338.6 mdp | ídem |

El DENUE (edición 2026) y los Censos Económicos 2019 miden universos y años distintos, así que sus conteos no deben sumarse ni restarse entre sí.

### 02. Precios (PROFECO)

- 28,288 registros de precios del programa Quién es Quién en los Precios en Mérida, capturados entre el 2 y el 29 de mayo de 2026, en 63 establecimientos de 34 cadenas (`data/fuente_a/02_datos_gob_profeco/profeco_merida_2026_real.csv`).
- Central de Abasto contra supermercado: ver hallazgo 1 y la figura [`02_central_abasto_vs_supermercados_profeco.png`](reports/figuras/02_central_abasto_vs_supermercados_profeco.png). Ambos precios son al consumidor según PROFECO; no son precios de mayoreo del SNIIM.
- Farmacias y tiendas de conveniencia: 5,864 registros en 11 cadenas (`data/fuente_b/06_scraping_farmacias/profeco_farmacias_conveniencia_merida_2026.csv`). Los productos con más cadenas comparables son medicamentos, por ejemplo ibuprofeno 400 mg caja con 10 y omeprazol 20 mg caja con 14 (9 cadenas cada uno).
- Precio por cadena con la misma presentación: figura [`01_precios_canasta_por_cadena_profeco.png`](reports/figuras/01_precios_canasta_por_cadena_profeco.png).
- DICONSA: 4,063 registros de artículos y proveedores (`data/fuente_c/02_diconsa_segalmex/`).

### 03. Salario, pobreza y canasta

| Indicador | Valor | Archivo |
|---|---:|---|
| Canasta alimentaria urbana, ene 2018 | $1,514.91 | `data/fuente_a/03_siegy_yucatan/coneval_lineas_pobreza_2018_2025.csv` |
| Canasta alimentaria urbana, mar 2025 | $2,379.47 | ídem |
| Aumento acumulado | 57.1 % | ídem |
| Línea de pobreza por ingresos urbana, mar 2025 | $4,680.15 | ídem |
| Población de Mérida (Censo 2020) | 995,129 | `data/fuente_a/03_siegy_yucatan/censo2020_totales_municipio_merida.csv` |
| Población económicamente activa | 527,424 | ídem |
| Población ocupada | 520,438 | ídem |
| Población sin afiliación a servicios de salud | 22.2 % | ídem |
| Grado promedio de escolaridad | 11.4 años | ídem |
| Viviendas con internet | 71.5 % | ídem (sobre el total de viviendas particulares habitadas) |

Los valores de CONEVAL son nacionales (urbano y rural), no específicos de Mérida. Los indicadores de SIEGY originalmente planeados siguen pendientes de descarga.

---

## 3. Módulo 2: mercados públicos y territorio

- **Mercados públicos:** 15 centros identificados en el DENUE como "Mercado público" en Mérida, con 1,661 establecimientos en total. Los más grandes son Lucas de Gálvez (817) y San Benito (486) (`data/fuente_a/04_geoportal_merida/mercados_publicos_merida_denue.geojson`). La coordenada de cada mercado es la mediana de sus establecimientos.
- **Desigualdad por AGEB:** en las 520 AGEB urbanas habitadas, la mediana de población sin afiliación a salud es 21.6 % (percentil 10: 16.6 %; percentil 90: 31.0 %). 12 AGEB superan el 40 %. La mediana de viviendas con internet es 73.3 % (`data/fuente_b/03_conapo_marginacion/censo2020_indicadores_ageb_merida.csv`, figura [`05_indicadores_ageb_censo2020_merida.png`](reports/figuras/05_indicadores_ageb_censo2020_merida.png)). No es el índice de marginación de CONAPO, sino sus insumos del Censo.
- **Transporte Va y Ven:** 565 elementos geográficos, de los cuales 500 son paradas de autobús y 18 son rutas (`data/fuente_c/04_transporte_vayven/export.geojson`).
- **Tianguis (04-B):** pendiente.

---

## 4. Módulo 3: levantamiento digital y de campo

- **Bitácora propia de tienditas (07-B):** 5 tiendas, 25 renglones y 22 precios capturados (3 renglones de tortilla sin precio). La comparación con supermercados está en la figura [`04_tienditas_vs_supermercados.png`](reports/figuras/04_tienditas_vs_supermercados.png) e incluye el número de observaciones por barra. Con 2 a 5 precios por producto, los resultados son indicativos, no estadísticamente concluyentes.
- **Scraping:** el scraping simulado se eliminó. 06-A y 06-B usan ahora registros de PROFECO; 06-C (apps de delivery) está pendiente.

---

## 5. Módulo 4: relieve y tecnologías visuales

| Ciudad | Elevación media (m) | Desnivel en la malla (m) | Pendiente mediana (°) |
|---|---:|---:|---:|
| Mérida | 9.6 | 16.2 | 0.1 |
| Monterrey | 651.4 | 1,292.0 | 1.4 |
| Guanajuato | 2,243.2 | 853.0 | 3.9 |
| Ciudad de México | 2,251.0 | 243.0 | 0.2 |
| San Cristóbal de las Casas | 2,317.6 | 1,413.0 | 5.0 |
| Toluca | 2,683.7 | 457.4 | 0.8 |

Fuente: `data/fuente_c/08_opentopography/topografia_merida_vs_ciudades_montana.csv`, malla de 20 x 20 puntos por ciudad tomada de AWS Terrain Tiles. Figura: [`06_relieve_merida_vs_ciudades_montana.png`](reports/figuras/06_relieve_merida_vs_ciudades_montana.png).

En el Centro (malla de 1,681 celdas alrededor del Mercado Lucas de Gálvez, `data/fuente_b/08_lidar_cem_mde/elevacion_centro_merida_grid.csv`) la elevación va de 7.77 a 12.74 m y la pendiente mediana es 0.41°. La resolución efectiva de esa fuente no permite modelar edificios ni el domo del mercado; para eso se requiere LiDAR (08-A, pendiente).

---

## 6. Limitaciones

- PROFECO registra precios en los establecimientos que visita; no es una muestra representativa de todos los comercios de Mérida.
- Las comparaciones de precios usan medianas del mismo producto y presentación; marcas distintas pueden explicar parte de las diferencias.
- La bitácora de tienditas tiene muestras muy pequeñas.
- Los datos de CONEVAL son nacionales y terminan en marzo de 2025.
