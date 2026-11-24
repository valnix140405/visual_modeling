# Guía de armado en Looker Studio

Proyecto: "Del Mundo a la Esquina: ¿Cuánto Cuesta Comer?" (UPY)

Las tablas de esta carpeta son planas (una fila por registro) y se generan solo con datos reales del repositorio:

```bash
python scripts/generar_tablas_looker_studio.py
```

## Tablas

| Archivo | Filas | Contenido | Fuentes |
|---|---:|---|---|
| [`looker_01_precios_multicanal.csv`](looker_01_precios_multicanal.csv) | 26,281 | Un precio por fila con `canal` (Tiendita de esquina, Supermercado, Central de Abasto, Farmacia / Conveniencia, Mercado público), establecimiento, producto, presentación, marca y `precio_mxn` | Bitácora propia 07-B y PROFECO QQP mayo 2026 (02-A) |
| [`looker_02_territorio_geo.csv`](looker_02_territorio_geo.csv) | 65 | Nodos con coordenadas: 15 mercados públicos (DENUE) y establecimientos de alimentos y farmacias monitoreados por PROFECO. Campo `coordenadas_looker` en formato `lat,lon` | INEGI DENUE (04-A) y PROFECO (02-A) |
| [`looker_03_lineas_pobreza_coneval.csv`](looker_03_lineas_pobreza_coneval.csv) | 87 | Serie mensual 2018-01 a 2025-03 de las líneas de pobreza por ingresos, rural y urbana | CONEVAL (03-A) |
| [`looker_04_ageb_censo2020_merida.csv`](looker_04_ageb_censo2020_merida.csv) | 520 | AGEB urbanas habitadas de Mérida con población, PEA, afiliación a salud, escolaridad e indicadores de vivienda | INEGI Censo 2020 (03-B) |

Notas:

- La bitácora de tienditas tiene 22 precios capturados en 5 tiendas; compárala con PROFECO solo en productos y presentaciones equivalentes.
- Las tienditas no tienen coordenadas, por eso no aparecen en la tabla territorial.
- Los tianguis (04-B), el scraping de apps de delivery (06-C) y el LiDAR (08-A) están pendientes y no se incluyen.

## Pasos para importar

1. En [lookerstudio.google.com](https://lookerstudio.google.com/) crea un **Informe vacío**.
2. Usa el conector **Subir archivo** o sube los CSV a Google Sheets. `looker_01` pesa unos 5.5 MB; si el conector lo rechaza, súbelo a Google Sheets.
3. Paleta del proyecto: primario `#600d8b`, secundario `#ed9f22`, fondo `#ffffff`.

## Páginas sugeridas

1. **Precios por canal**: tabla dinámica de `producto` por `canal` con la mediana de `precio_mxn`; filtros de `producto` y `presentacion`.
2. **Territorio**: mapa de Google con `coordenadas_looker`, color por `tipo_nodo` y tamaño por `establecimientos_denue` o `registros_profeco`.
3. **Costo de la canasta**: serie temporal de `looker_03` con las cuatro líneas.
4. **Desigualdad urbana**: histogramas o tabla de `looker_04` (`pct_sin_afiliacion_salud`, `pct_viviendas_con_internet`, `pct_desocupacion`).
