# Fuentes de los CSV del capítulo

Todos los CSV se generan con `python scripts/generar_datos_booklet.py` a partir de archivos del repositorio. Las columnas están en español, en minúsculas y con guion bajo. Cada CSV trae también sus columnas `fuente` y `corte`.

## escena-1.csv · Calendario de la canasta (1 fila)

| Columna | Origen |
|---|---|
| `canasta_persona_mxn` | CONEVAL, Líneas de pobreza por ingresos, línea de pobreza extrema por ingresos (canasta alimentaria), urbana, marzo 2025: $2,379.47. https://www.coneval.org.mx/Medicion/Documents/Lineas_de_Pobreza_por_Ingresos/Lineas_de_Pobreza_por_Ingresos.zip → `data/fuente_a/03_siegy_yucatan/coneval_lineas_pobreza_2018_2025.csv` |
| `ocupantes_por_vivienda` | INEGI, Censo de Población y Vivienda 2020, resultados por AGEB y manzana urbana, columna `PROM_OCUP` del total municipal de Mérida (31050): 3.27. https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/ageb_manzana/ageb_mza_urbana_31_cpv2020_csv.zip → `data/fuente_a/03_siegy_yucatan/censo2020_totales_municipio_merida.csv` |
| `salario_minimo_diario_mxn` | CONASAMI, Tabla de Salarios Mínimos Generales y Profesionales 2025, zona del salario mínimo general: $278.80 diarios (verificado el 2026-11-24 contra la tabla oficial en gob.mx/conasami). Es la única constante y está documentada en el script |
| `canasta_hogar_mxn` | Cálculo: `canasta_persona_mxn × ocupantes_por_vivienda` = $7,780.87 |
| `dias_canasta` | Cálculo: `canasta_hogar_mxn ÷ salario_minimo_diario_mxn` = 27.9 días |
| `dias_libres` | Cálculo: `dias_mes − dias_canasta` = 2.1 (mes de 30 días) |

**Corte:** marzo 2025 (último dato publicado por CONEVAL en el archivo descargado).

## escena-2.csv · Central de Abasto contra súper (139 filas)

- **Fuente:** PROFECO, Quién es Quién en los Precios (QQP), registros de Mérida de mayo de 2026. https://datos.profeco.gob.mx/index.php (archivo `docs/qqp/QQP_2026.rar`) → `data/fuente_a/02_datos_gob_profeco/profeco_merida_2026_real.csv`.
- **Cálculo:** para cada par producto-presentación con registros en la Central de Abasto (`cadena_comercial = Central de Abasto`) y en supermercados (`giro = Supermercado / Tienda de Autoservicio`), se toma la **mediana** de precio en cada canal. `diferencia_pct = (precio_super_mxn ÷ precio_central_mxn − 1) × 100`. Positivo = el súper es más caro.
- **Ruta en el repositorio:** `scripts/generar_datos_web.py` → `reports/looker_studio/looker_05_comparables_por_canal.csv` → este CSV.
- **Corte:** mayo 2026.

## escena-3.csv · Tienda de conveniencia contra súper (93 filas)

- **Fuente:** la misma de la escena 2 (PROFECO QQP, Mérida, mayo 2026).
- **Cálculo:** conveniencia = `giro = Tienda de Conveniencia` (Dunosusa, OXXO y 7 Eleven). Se toma el **promedio** por producto y presentación, solo si hay **3 o más registros en cada canal**. `diferencia_pct = (precio_conveniencia_mxn ÷ precio_super_mxn − 1) × 100`. Positivo = la conveniencia es más cara.
- **Corte:** mayo 2026.

## escena-4.csv · Tiendita contra súper (4 filas)

- **Fuentes:**
  - Bitácora propia de precios en 5 tienditas de Mérida (fuente 07-B), visitas del 26 de septiembre al 1 de octubre de 2026 → `data/fuente_b/07_bitacora_tienditas/bitacora_precios_tienditas.csv`. No contiene datos personales: solo nombre comercial de la tienda, colonia y precio.
  - PROFECO QQP, supermercados de Mérida, mayo 2026.
- **Cálculo:** 4 productos equivalentes entre la bitácora y PROFECO (leche entera LALA 1 L, pan blanco Bimbo grande, tortilla de maíz 1 kg y frijol negro por kg). **Mediana** de precio en cada canal. `diferencia_pct = (precio_tiendita_mxn ÷ precio_super_mxn − 1) × 100`. `registros_tiendita` y `registros_super` dicen cuántos precios hay detrás de cada mediana; `numero_tienditas` = folios distintos de la bitácora (5).
- **Ruta en el repositorio:** `scripts/analisis_profundo_22_fuentes.py` → `reports/metricas_analisis.json` → `reports/looker_studio/looker_08_tienditas_vs_super.csv` → este CSV.
- **Advertencia:** muestra chica (2 a 5 precios por producto en tienditas).

## puente-relieve.csv · Relieve de Mérida frente a ciudades de montaña (6 filas)

- **Fuente:** AWS Terrain Tiles (Tilezen, formato Terrarium, zoom 12). https://registry.opendata.aws/terrain-tiles/ → `data/fuente_c/08_opentopography/topografia_merida_vs_ciudades_montana.csv` (malla de 20 × 20 puntos, unos 17 km por lado, por ciudad).
- **Cálculo:** elevación mínima, máxima y promedio por ciudad; `desnivel_m = elevacion_maxima_m − elevacion_minima_m`. Mérida: 16.2 m.
- **Advertencia:** es elevación de un modelo de terreno con resolución aproximada de 30 m, **no LiDAR**. Verificar la atribución que pide Tilezen antes de publicar.
- **Corte:** noviembre 2026 (fecha de descarga de las teselas).
