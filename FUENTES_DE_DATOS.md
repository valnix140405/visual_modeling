# Catálogo de las 22 fuentes de datos

**Proyecto:** Del Mundo a la Esquina: ¿Cuánto Cuesta Comer?  
**Última revisión de procedencia:** 2026-11-24

**Estado:** 12 completas con datos reales · 3 con dato real parcial · 3 pendientes sin dato · 1 por revisar · 3 prototipos de diseño (AR).

Cada carpeta tiene un `README.md` con la URL de origen, fecha de extracción, licencia, estado y observaciones de cada archivo. Los datasets nuevos se regeneran con:

```bash
python scripts/generar_datos_reales.py   # descarga los originales a .cache_descargas/ (ignorada por git)
python scripts/verificar_datasets.py     # comprueba qué hay en disco
```

## Tabla maestra

| # | Responsable | Fuente real usada | Archivo | Estado | Nota |
|---|---|---|---|---|---|
| [01-A](data/fuente_a/01_inegi_denue/) | Valeria | INEGI DENUE | `denue_merida_alimentos_real.csv` | Completo | 7,520 comercios de alimentos en Mérida |
| [01-B](data/fuente_b/01_inegi_saic/) | Ramiro | INEGI Censos Económicos 2019 | `censos_economicos_2019_merida_comercio_alimentos.csv` | Completo | Reemplaza cifras sin origen |
| [01-C](data/fuente_c/01_enoe_microdatos/) | Isaac | INEGI ENOE 2025 1T | `conjunto_de_datos_hog/viv_enoe_2025_1t/` | Completo | Faltan las tablas COE1, COE2 y SDEM |
| [02-A](data/fuente_a/02_datos_gob_profeco/) | Valeria | PROFECO QQP | `profeco_merida_2026_real.csv` | Completo | Registros de mayo 2026 |
| [02-B](data/fuente_b/02_datos_gob_sniim/) | Ramiro | PROFECO QQP, Central de Abasto | `profeco_central_abasto_merida_2026.csv` | Pendiente parcial | Precios al consumidor; falta el mayoreo del SNIIM |
| [02-C](data/fuente_c/02_diconsa_segalmex/) | Isaac | DICONSA (datos.gob.mx) | `DICONSA_8_Listado_de_articulos_por_proveedor.csv` | Completo | |
| [03-A](data/fuente_a/03_siegy_yucatan/) | Valeria | CONEVAL + INEGI Censo 2020 | `coneval_lineas_pobreza_2018_2025.csv`, `censo2020_totales_municipio_merida.csv` | Pendiente parcial | Sustituye a SIEGY; falta un dato propio de SIEGY |
| [03-B](data/fuente_b/03_conapo_marginacion/) | Ramiro | INEGI Censo 2020 por AGEB | `censo2020_indicadores_ageb_merida.csv` | Pendiente parcial | Insumos del índice; falta el índice CONAPO |
| [03-C](data/fuente_c/03_imss_boletin/) | Isaac | SENASICA (datos.gob.mx) | `01_actividades-inspeccion-movilizacion_2dotrim2025.csv` | Completo | Cobertura nacional |
| [04-A](data/fuente_a/04_geoportal_merida/) | Valeria | INEGI DENUE (mercados públicos) | `mercados_publicos_merida_denue.geojson` | Completo | Falta la capa oficial del Geoportal |
| [04-B](data/fuente_b/04_tianguis_geoportal/) | Ramiro | — | — | **Pendiente** | Geoportal respondió 403 |
| [04-C](data/fuente_c/04_transporte_vayven/) | Isaac | OpenStreetMap (Overpass) | `export.geojson` | Completo | Licencia ODbL |
| [06-A](data/fuente_a/06_scraping_autoservicios/) | Valeria | PROFECO QQP (supermercados) | `precios_canasta_supermercados_reales.csv` | Completo | No es scraping; falta un scraping real |
| [06-B](data/fuente_b/06_scraping_farmacias/) | Ramiro | PROFECO QQP (farmacias y conveniencia) | `profeco_farmacias_conveniencia_merida_2026.csv` | Completo | No es scraping; falta un scraping real |
| [06-C](data/fuente_c/06_scraping_delivery/) | Isaac | — | — | **Pendiente** | Los datos anteriores eran aleatorios |
| [07-B](data/fuente_b/07_bitacora_tienditas/) | Ramiro | Levantamiento propio | `bitacora_precios_tienditas.csv` | Revisar | Confirmar las direcciones de AUD-01 |
| [08-A](data/fuente_a/08_lidar_mercado/) | Valeria | — | — | **Pendiente** | No hay LiDAR público del mercado |
| [08-B](data/fuente_b/08_lidar_cem_mde/) | Ramiro | AWS Terrain Tiles | `elevacion_centro_merida_grid.csv` + `.ply` | Completo | Elevación, no LiDAR; falta el CEM de INEGI |
| [08-C](data/fuente_c/08_opentopography/) | Isaac | AWS Terrain Tiles | `topografia_merida_vs_ciudades_montana.csv` + `.ply` | Completo | Mérida frente a 5 ciudades de montaña |
| [09-A](data/fuente_a/09_ar_anclas/) | Valeria | Diseño del equipo | `spatial_anchors_merida.geojson` | Prototipo | No es dato de fuente |
| [09-B](data/fuente_b/09_ar_modelos_3d/) | Ramiro | Diseño del equipo | `catalogo_modelos_3d_canasta.json` | Prototipo | No es dato de fuente |
| [09-C](data/fuente_c/09_ar_waypoints/) | Isaac | Diseño del equipo | `ruta_ar_lucas_galvez.json` | Prototipo | No es dato de fuente |

## Cambios del 2026-11-24

Se eliminaron los datasets simulados (generados con números aleatorios o escritos a mano sin fuente). Donde existía un equivalente oficial descargable, se reemplazó; donde no, la fuente quedó **Pendiente**. El detalle de cada caso está en el README de su carpeta.

| Eliminado | Motivo | Reemplazo |
|---|---|---|
| `precios_canasta_scraping.csv` y su scraper (06-A) | Precios generados con `random` | Resumen real de PROFECO por cadena |
| `precios_farmacias_conveniencia_merida.csv` y su scraper (06-B) | Precios generados con `random` | PROFECO real de farmacias, OXXO y 7-Eleven |
| `comparativa_precios_canasta_basica.csv` y su scraper (06-C) | 2,501 tickets aleatorios | — (pendiente) |
| `censos_economicos_saic_merida.csv` (01-B) | Cifras sin origen; no hubo Censo Económico 2024 | INEGI Censos Económicos 2019 |
| `sniim_mayoreo_central_abasto_merida.csv` (02-B) | Sin origen verificable | PROFECO en la Central de Abasto (parcial) |
| `indicadores_socioeconomicos_merida_siegy.csv` (03-A) | Sin tabla de origen | CONEVAL + Censo 2020 |
| `marginacion_urbana_colonias_merida.csv` (03-B) | CONAPO no publica el índice por colonia | Censo 2020 por AGEB |
| `mercados_municipales_merida.geojson` (04-A) | Atributos inventados (locales, afluencia) | Mercados públicos desde DENUE |
| `tianguis_comercio_via_publica_merida.geojson` (04-B) | Polígonos sin fuente | — (pendiente) |
| `lidar_mercado_merida_sample.csv` y `.ply` (08-A) | 20 puntos escritos a mano | — (pendiente) |
| `inegi_cem_mde_merida_grid.csv` y `.ply` (08-B) | 15 celdas escritas a mano | Elevación real (AWS Terrain Tiles) |
| `topografia_srtm_nasadem_merida_vs_montanas.csv` y `nasa_gedi_dosel_merida_lidar.ply` (08-C) | Puntos generados | Elevación real (AWS Terrain Tiles) |
| `denue_merida_canasta_basica.csv`, `profeco_qqp_merida_sample.csv` | Muestras sintéticas duplicadas de datos reales | Ya existían los archivos reales |
