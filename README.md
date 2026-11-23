# Del Mundo a la Esquina: ¿Cuánto Cuesta Comer?
### Radiografía multiescalar del salario y la canasta básica: del panorama internacional al territorio de Mérida

Este repositorio consolida los datasets, scripts y especificaciones técnicas organizados bajo un enfoque multiescalar (**Internacional $\rightarrow$ México $\rightarrow$ Yucatán $\rightarrow$ Mérida**).

> **Documentación completa para el equipo:**  
> * Consulta [`GUIA_FUENTES_Y_EQUIPO.md`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/GUIA_FUENTES_Y_EQUIPO.md) para la guía completa de las 22 fuentes activas (reparto Fuente A, Fuente B y Fuente C).  
> * Consulta [`FUENTES_DE_DATOS.md`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/FUENTES_DE_DATOS.md) para la ficha técnica y enlaces oficiales de origen.

---

## Estructura Modular del Repositorio

El repositorio está organizado en tres grandes carpetas para consolidar el trabajo del equipo:
* **`data/fuente_a/`**: Los 7 datasets del primer bloque (100% listos e integrados).
* **`data/fuente_b/`**: Los 8 datasets del segundo bloque, incluyendo el levantamiento propio de tienditas (100% listos e integrados).
* **`data/fuente_c/`**: Los 7 datasets del tercer bloque aportados por el equipo (100% listos e integrados).

```text
victorrr/
├── data/
│   ├── fuente_a/
│   │   ├── 01_inegi_denue/
│   │   ├── 02_datos_gob_profeco/
│   │   ├── 03_siegy_yucatan/
│   │   ├── 04_geoportal_merida/
│   │   ├── 06_scraping_autoservicios/
│   │   ├── 08_lidar_mercado/
│   │   └── 09_ar_anclas/
│   ├── fuente_b/
│   │   ├── 01_inegi_saic/
│   │   ├── 02_datos_gob_sniim/
│   │   ├── 03_conapo_marginacion/
│   │   ├── 04_tianguis_geoportal/
│   │   ├── 06_scraping_farmacias/
│   │   ├── 07_bitacora_tienditas/
│   │   ├── 08_lidar_cem_mde/
│   │   └── 09_ar_modelos_3d/
│   └── fuente_c/
│       ├── 01_enoe_microdatos/
│       ├── 02_diconsa_segalmex/
│       ├── 03_imss_boletin/
│       ├── 04_transporte_vayven/
│       ├── 06_scraping_delivery/
│       ├── 08_opentopography/
│       └── 09_ar_waypoints/
├── reports/
│   └── figuras/
├── scripts/
│   ├── analisis_profundo_27_fuentes.py
│   ├── generar_archivos_3d_y_lidar.py
│   ├── generar_graficas_analisis.py
│   ├── verificar_datasets.py
│   └── verificar_links_index.py
├── .gitignore
├── FUENTES_DE_DATOS.md
├── GUIA_FUENTES_Y_EQUIPO.md
├── index.html
└── README.md
```

---

## Matriz de Datasets Disponibles (22 Datasets Listos - 100% Completo)

| # | Grupo | Tema / Categoría | Archivo Generado | Formato | Cobertura y Descripción |
|---|---|---|---|---|---|
| **01-A** | **Fuente A** | **INEGI / DENUE** | [`denue_merida_alimentos_real.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_a/01_inegi_denue/denue_merida_alimentos_real.csv) | CSV Oficial (3.2 MB) | **7,520 comercios reales** de canasta básica en Mérida (filtrados de 146,384 en Yucatán). |
| **01-B** | **Fuente B** | **INEGI / SAIC** | [`censos_economicos_saic_merida.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_b/01_inegi_saic/censos_economicos_saic_merida.csv) | CSV Censal | Ingresos totales, sueldos y personal en abarrotes y supermercados (SAIC). |
| **01-C** | **Fuente C** | **INEGI / ENOE** | [`0_indice_tablas_enoe_2025_1t.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_c/01_enoe_microdatos/0_indice_tablas_enoe_2025_1t.csv) | Microdatos INEGI | Microdatos ENOE 2025 1T Hogares/Viviendas (>300,000 registros y 45 catálogos). |
| **02-A** | **Fuente A** | **datos.gob / PROFECO** | [`profeco_merida_2026_real.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_a/02_datos_gob_profeco/profeco_merida_2026_real.csv) | CSV Oficial (7.9 MB) | **28,288 precios reales** en Mérida monitoreados por inspectores PROFECO. |
| **02-B** | **Fuente B** | **datos.gob / SNIIM** | [`sniim_mayoreo_central_abasto_merida.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_b/02_datos_gob_sniim/sniim_mayoreo_central_abasto_merida.csv) | CSV Mayorista | Precios de mayoreo (SNIIM) en la Central de Abasto de Mérida. |
| **02-C** | **Fuente C** | **SEGALMEX / DICONSA** | [`DICONSA_8_Listado_de_articulos_por_proveedor.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_c/02_diconsa_segalmex/DICONSA_8_Listado_de_articulos_por_proveedor.csv) | CSV Oficial (698 KB) | 4,064 artículos canasta básica y proveedores de tiendas DICONSA. |
| **03-A** | **Fuente A** | **SIEGY - Yucatán** | [`indicadores_socioeconomicos_merida_siegy.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_a/03_siegy_yucatan/indicadores_socioeconomicos_merida_siegy.csv) | CSV Tabular | PEA, salario formal IMSS y costo de canasta alimentaria CONEVAL (\$2,610 MXN). |
| **03-B** | **Fuente B** | **SIEGY / CONAPO** | [`marginacion_urbana_colonias_merida.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_b/03_conapo_marginacion/marginacion_urbana_colonias_merida.csv) | CSV Marginación | Índice CONAPO/SIEGY por colonia en Mérida (contraste Norte vs. Sur). |
| **03-C** | **Fuente C** | **Inspección / Sanidad** | [`01_actividades-inspeccion-movilizacion_2dotrim2025.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_c/03_imss_boletin/01_actividades-inspeccion-movilizacion_2dotrim2025.csv) | CSV Inspección | Puntos de inspección fitozoosanitaria y movilización de mercancías agropecuarias. |
| **04-A** | **Fuente A** | **Geoportal Mérida** | [`mercados_municipales_merida.geojson`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_a/04_geoportal_merida/mercados_municipales_merida.geojson) | GeoJSON SIG | 8 mercados públicos nodales permanentes (Lucas de Gálvez, San Benito, etc.). |
| **04-B** | **Fuente B** | **Geoportal Mérida** | [`tianguis_comercio_via_publica_merida.geojson`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_b/04_tianguis_geoportal/tianguis_comercio_via_publica_merida.geojson) | GeoJSON SIG | Polígonos de tianguis sobre ruedas autorizados en colonias y días de operación. |
| **04-C** | **Fuente C** | **Movilidad / Va y Ven** | [`export.geojson`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_c/04_transporte_vayven/export.geojson) | GeoJSON (1.0 MB) | 565 rutas y paraderos de transporte Va y Ven conectando con el Centro Histórico. |
| **06-A** | **Fuente A** | **Web Scraping** | [`precios_canasta_scraping.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_a/06_scraping_autoservicios/precios_canasta_scraping.csv) | CSV Scraper | 18 artículos esenciales en supermercados (Súper Akí, Chedraui, Dunosusa). |
| **06-B** | **Fuente B** | **Web Scraping** | [`precios_farmacias_conveniencia_merida.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_b/06_scraping_farmacias/precios_farmacias_conveniencia_merida.csv) | CSV Scraper | Monitoreo de canasta complementaria en Farmacias Guadalajara, OXXO y Similares. |
| **06-C** | **Fuente C** | **Scraping Apps Delivery** | [`comparativa_precios_canasta_basica.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_c/06_scraping_delivery/comparativa_precios_canasta_basica.csv) | CSV (301 KB) | 2,501 registros de sobreprecio delivery vs tienda física con tarifas y propinas. |
| **07-B** | **Fuente B** | **Self-Produced** | [`bitacora_precios_tienditas.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_b/07_bitacora_tienditas/bitacora_precios_tienditas.csv) | CSV Auditoría | Levantamiento propio en 5 tienditas de Mérida (*Centro, Santiago, Polígono 108, Mercedes Barrera, Chuburná*). |
| **08-A** | **Fuente A** | **LiDAR 3D** | [`lidar_mercado_merida_sample.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_a/08_lidar_mercado/lidar_mercado_merida_sample.csv) | CSV / 3D ASPRS | Nube 3D con clasificación ASPRS (Suelo, Árboles y Domo del Mercado Lucas de Gálvez). |
| **08-B** | **Fuente B** | **LiDAR / CEM** | [`inegi_cem_mde_merida_grid.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_b/08_lidar_cem_mde/inegi_cem_mde_merida_grid.csv) | CSV Malla MDE | Malla de elevación CEM 3.0 de INEGI para evaluar pendientes y encharcamientos. |
| **08-C** | **Fuente C** | **OpenTopography / Radar** | [`topografia_srtm_nasadem_merida_vs_montanas.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_c/08_opentopography/topografia_srtm_nasadem_merida_vs_montanas.csv) | CSV (368 KB) | 2,401 puntos de cota satelital SRTM/NASADEM Mérida vs zonas montañosas. |
| **09-A** | **Fuente A** | **AR Geospatial** | [`spatial_anchors_merida.geojson`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_a/09_ar_anclas/spatial_anchors_merida.geojson) | GeoJSON VPS | Anclas espaciales para proyectar semáforos de precios 3D sobre fachadas. |
| **09-B** | **Fuente B** | **AR Geospatial** | [`catalogo_modelos_3d_canasta.json`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_b/09_ar_modelos_3d/catalogo_modelos_3d_canasta.json) | JSON Catálogo | Especificación técnica de assets 3D glTF/GLB optimizados para WebXR / ARCore. |
| **09-C** | **Fuente C** | **Waypoints AR Lucas Gálvez** | [`ruta_ar_lucas_galvez.json`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_c/09_ar_waypoints/ruta_ar_lucas_galvez.json) | JSON Navegación | Ruta de guiado peatonal AR hacia el pasillo económico de Lucas de Gálvez. |

---

## Verificación del Repositorio

Para comprobar el estado y resumen de los 22 datasets en cualquier momento, ejecuta en la terminal:

```bash
python scripts/verificar_datasets.py
```

## Visores Interactivos y Experiencias Web (Listos para Abrir)

El proyecto incluye aplicaciones web autónomas e interactivas que puedes abrir con doble clic en tu navegador:

1. **[Presentación Web Principal (`index.html`)](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/index.html):** Plataforma interactiva de presentación por diapositivas con hallazgos científicos, simulador salarial y catálogo de fuentes.
2. **[Visor SIG de Mercados Municipales](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_a/04_geoportal_merida/visor_mercados_municipales.html):** Mapa interactivo en Leaflet con la red de 8 mercados públicos de Mérida, fichas técnicas y radios de caminabilidad de 10 minutos a pie (isocronas de 800m).
3. **[Visores 3D LiDAR (08-A, 08-B, 08-C)](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_a/08_lidar_mercado/visor_3d_mercado.html):** Espacios 3D en Three.js para orbitar, inspeccionar y medir las cotas altimétricas del domo del mercado, relieve INEGI y dosel NASA GEDI.
4. **[Visores WebXR / AR (09-A, 09-B, 09-C)](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_a/09_ar_anclas/visor_ar_web.html):** Experiencias de Realidad Aumentada con anclas espaciales VPS, catálogo holográfico glTF y navegación peatonal.

---

## Integrantes del Equipo y Reparto de Fuentes

* **Valeria Nicol Hernández León** — *Responsable de Fuente A* (Módulos 01-A, 02-A, 03-A, 04-A, 06-A, 08-A, 09-A: DENUE Alimentos, PROFECO QQP 2026, SIEGY Indicadores Estatales, Geoportal Mercados Municipales, Scraper Autoservicios, LiDAR Domo Lucas de Gálvez, AR WebXR Anclas).
* **Jorge Ramiro Chay Koyoc** — *Responsable de Fuente B* (Módulos 01-B, 02-B, 03-B, 04-B, 06-B, 07-B, 08-B, 09-B: Censos Económicos SAIC, Precios Mayoreo SNIIM Central de Abasto, CONAPO Marginación Urbana, Geoportal Tianguis, Scraper Farmacias/OXXO, Bitácora Propia de Tienditas, CEM MDE 3.0, Catálogo Modelos 3D).
* **Isaac René Andrade Sánchez** — *Responsable de Fuente C* (Módulos 01-C, 02-C, 03-C, 04-C, 06-C, 08-C, 09-C: Microdatos ENOE 2025 1T, Padrón DICONSA/SEGALMEX, Inspección Sanitaria SENASICA, Rutas Va y Ven, Scraping Apps Delivery, Topografía SRTM/NASADEM, Waypoints AR).
