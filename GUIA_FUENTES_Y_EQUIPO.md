# Guía Maestra del Proyecto: Título, Subtemas y 22 Fuentes de Datos

## Proyecto: Análisis Multiescalar del Salario, la Canasta Básica y el Territorio

### Enfoque de Embudo: Internacional $\rightarrow$ México $\rightarrow$ Yucatán $\rightarrow$ Mérida

Este documento es la **guía oficial para el equipo**. Explica el título elegido, los subtemas redactados de forma clara y la **matriz completa de 22 fuentes de datos activas** (con las fuentes PNT retiradas y conservando como única fuente *Self-Produced* la bitácora real de tienditas de la esquina `07-B`).

---

## 1. El Título del Proyecto

### Título Oficial:

> **"Del Mundo a la Esquina: ¿Cuánto Cuesta Comer?"**

## ¿Por qué elegimos este título?

1. **Es directo y humano:** Le da la vuelta al dicho clásico *"trabajar para comer o comer para trabajar"*. Plantea una postura clara: el objetivo del trabajo no es la simple supervivencia biológica, sino el bienestar y la dignidad.
2. **Es multiescalar:** El subtítulo aclara que no es un proyecto cerrado solo a Mérida; toma como base los estándares internacionales y nacionales, y usa a Mérida como el laboratorio de validación en la calle.

---

## 2. Los Subtemas del Proyecto

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        ESTRUCTURA DEL PROYECTO                         │
├────────────────────────────────────────────────────────────────────────┤
│  MÓDULO 1: LA REALIDAD ECONÓMICA (¿Dónde compramos y cuánto ganamos?)  │
│    1. El Mapa del Comercio: Dónde están las tiendas y supermercados    │
│    2. El Costo de la Comida: Cómo cambian los precios en la ciudad     │
│    3. Sueldo vs. Canasta Básica: ¿Para qué alcanza el salario hoy?     │
│                                                                        │
│  MÓDULO 2: LOS MERCADOS PÚBLICOS Y LA MOVILIDAD                        │
│    4. Mercados Tradicionales, Tianguis y Transporte Va y Ven           │
│                                                                        │
│  MÓDULO 3: LEVANTAMIENTO DE DATOS EN LA ERA DIGITAL Y EN CAMPO         │
│    6. Rastreo Web: Extracción automática de precios y apps delivery    │
│    7. Auditoría de Campo (Self-Produced): Precios en 5 tienditas       │
│                                                                        │
│  MÓDULO 4: TECNOLOGÍA VISUAL Y EL FUTURO DE LAS COMPRAS                │
│    8. Escaneo Láser en 3D: Conociendo la forma y altura del mercado    │
│    9. Realidad Aumentada: Ver precios y ahorros flotando en la calle   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Matriz Maestra: Las 22 Fuentes de Datos Activas

* **Fuente A (7 datasets):** Integrados y verificados en el repositorio (`01-A`, `02-A`, `03-A`, `04-A`, `06-A`, `08-A`, `09-A`).
* **Fuente B (8 datasets):** Integrados y verificados en el repositorio (`01-B`, `02-B`, `03-B`, `04-B`, `06-B`, `07-B`, `08-B`, `09-B`).
* **Fuente C (7 datasets):** Integrados y verificados en el repositorio (`01-C`, `02-C`, `03-C`, `04-C`, `06-C`, `08-C`, `09-C`).

---

### MÓDULO 1: LA REALIDAD ECONÓMICA

#### 01. Tipo: INEGI / DENUE (Directorios y Censos de Empresas)
* **Fuente A (`01-A`):** [`denue_merida_alimentos_real.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_a/01_inegi_denue/denue_merida_alimentos_real.csv) — 7,520 comercios de canasta básica en Mérida.
* **Fuente B (`01-B`):** [`censos_economicos_saic_merida.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_b/01_inegi_saic/censos_economicos_saic_merida.csv) — Ingresos totales, sueldos promedio pagados y personal ocupado (SAIC INEGI).
* **Fuente C (`01-C`):** [`0_indice_tablas_enoe_2025_1t.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_c/01_enoe_microdatos/0_indice_tablas_enoe_2025_1t.csv) — Microdatos ENOE 2025 1T de ocupación, empleo e informalidad en Yucatán.

#### 02. Tipo: datos.gob.mx (Datos Abiertos Federales / Precios)
* **Fuente A (`02-A`):** [`profeco_merida_2026_real.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_a/02_datos_gob_profeco/profeco_merida_2026_real.csv) — 28,288 precios reales de alimentos en Mérida durante 2026.
* **Fuente B (`02-B`):** [`sniim_mayoreo_central_abasto_merida.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_b/02_datos_gob_sniim/sniim_mayoreo_central_abasto_merida.csv) — Precios diarios de mayoreo en la Central de Abasto de Mérida (SNIIM).
* **Fuente C (`02-C`):** [`DICONSA_8_Listado_de_articulos_por_proveedor.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_c/02_diconsa_segalmex/DICONSA_8_Listado_de_articulos_por_proveedor.csv) — Catálogo de 4,064 productos con precio subsidiado DICONSA / SEGALMEX.

#### 03. Tipo: SIEGY - Yucatán (Estadísticas Estatales y Municipales)
* **Fuente A (`03-A`):** [`indicadores_socioeconomicos_merida_siegy.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_a/03_siegy_yucatan/indicadores_socioeconomicos_merida_siegy.csv) — Datos de PEA, salarios IMSS y pobreza laboral para Mérida y zona conurbada.
* **Fuente B (`03-B`):** [`marginacion_urbana_colonias_merida.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_b/03_conapo_marginacion/marginacion_urbana_colonias_merida.csv) — Nivel de marginación socioeconómica por colonia dentro de Mérida (CONAPO).
* **Fuente C (`03-C`):** [`01_actividades-inspeccion-movilizacion_2dotrim2025.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_c/03_imss_boletin/01_actividades-inspeccion-movilizacion_2dotrim2025.csv) — Inspección fitozoosanitaria y movilización agropecuaria en Yucatán.

---

### MÓDULO 2: LOS MERCADOS PÚBLICOS Y LA MOVILIDAD

#### 04. Tipo: Geoportal Mérida y Movilidad (SIG Municipal)
* **Fuente A (`04-A`):** [`mercados_municipales_merida.geojson`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_a/04_geoportal_merida/mercados_municipales_merida.geojson) — Polígonos y puntos de los 8 mercados públicos de la ciudad.
* **Fuente B (`04-B`):** [`tianguis_comercio_via_publica_merida.geojson`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_b/04_tianguis_geoportal/tianguis_comercio_via_publica_merida.geojson) — Polígonos de tianguis sobre ruedas autorizados en colonias.
* **Fuente C (`04-C`):** [`export.geojson`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_c/04_transporte_vayven/export.geojson) — 565 rutas y paraderos del sistema Va y Ven hacia el Centro Histórico.

---

### MÓDULO 3: LEVANTAMIENTO DE DATOS EN LA ERA DIGITAL Y EN CAMPO

#### 06. Tipo: Web Scraping (Monitoreo Automatizado de Precios)
* **Fuente A (`06-A`):** [`precios_canasta_scraping.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_a/06_scraping_autoservicios/precios_canasta_scraping.csv) — Catálogo de 18 artículos en autoservicios locales (Súper Akí, Dunosusa, Chedraui).
* **Fuente B (`06-B`):** [`precios_farmacias_conveniencia_merida.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_b/06_scraping_farmacias/precios_farmacias_conveniencia_merida.csv) — Precios de productos de higiene y canasta complementaria en Farmacias Guadalajara y OXXO.
* **Fuente C (`06-C`):** [`comparativa_precios_canasta_basica.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_c/06_scraping_delivery/comparativa_precios_canasta_basica.csv) — Comparativa de 2,501 carritos de canasta básica en tienda física vs. apps de delivery (Rappi / UberEats).

#### 07. Tipo: Self-Produced Data (Datos Producidos por el Equipo)
* **Fuente B (`07-B` — Única Fuente Self-Produced Activa):** [`bitacora_precios_tienditas.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_b/07_bitacora_tienditas/bitacora_precios_tienditas.csv)
  * *Dinámica:* Levantamiento propio en 5 tienditas de esquina de Mérida (*Centro Histórico, Parque de Santiago, Polígono 108, Mercedes Barrera y Vista Alegre de Chuburná*) auditando tortilla, huevo, leche, frijol y pan blanco.

---

### MÓDULO 4: TECNOLOGÍAS VISUALES Y EL FUTURO DE LAS COMPRAS

#### 08. Tipo: Datos LiDAR (Nube de Puntos 3D y Elevaciones)
* **Fuente A (`08-A`):** [`lidar_mercado_merida_sample.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_a/08_lidar_mercado/lidar_mercado_merida_sample.csv) — Nube de puntos clasificada ASPRS de la techumbre y suelo del Mercado Lucas de Gálvez.
* **Fuente B (`08-B`):** [`inegi_cem_mde_merida_grid.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_b/08_lidar_cem_mde/inegi_cem_mde_merida_grid.csv) — Malla de elevación continua CEM 3.0 de INEGI para la ciudad de Mérida.
* **Fuente C (`08-C`):** [`topografia_srtm_nasadem_merida_vs_montanas.csv`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_c/08_opentopography/topografia_srtm_nasadem_merida_vs_montanas.csv) — 2,401 cotas satelitales SRTM/NASADEM comparando Mérida frente a zonas montañosas.

#### 09. Tipo: AR Geospatial (Realidad Aumentada / 3D)
* **Fuente A (`09-A`):** [`spatial_anchors_merida.geojson`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_a/09_ar_anclas/spatial_anchors_merida.geojson) — 4 anclas espaciales VPS georreferenciadas frente a fachadas de tiendas y mercados.
* **Fuente B (`09-B`):** [`catalogo_modelos_3d_canasta.json`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_b/09_ar_modelos_3d/catalogo_modelos_3d_canasta.json) — Modelos 3D `.glb` optimizados para web/AR de alimentos esenciales.
* **Fuente C (`09-C`):** [`ruta_ar_lucas_galvez.json`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/data/fuente_c/09_ar_waypoints/ruta_ar_lucas_galvez.json) — Ruta de 6 waypoints secuenciales para guiar en Realidad Aumentada hacia el pasillo más barato del Mercado Lucas de Gálvez.

---

## 4. Reparto Oficial de Fuentes por Integrante (22 Fuentes Activas)

* **Valeria Nicol Hernández León — Responsable de Fuente A (7 fuentes):**
  * `01-A` INEGI / DENUE (7,520 comercios de canasta básica en Mérida).
  * `02-A` datos.gob.mx / PROFECO (28,288 precios reales QQP Mérida 2026).
  * `03-A` SIEGY Yucatán (PEA, salario IMSS y costo de canasta urbana).
  * `04-A` Geoportal Mérida (Capa SIG de los 8 mercados públicos municipales).
  * `06-A` Web Scraping (18 productos básicos en autoservicios locales Akí/Dunosusa).
  * `08-A` LiDAR 3D (Nube de puntos ASPRS clasificada del Mercado Lucas de Gálvez).
  * `09-A` AR Geospatial (Anclas espaciales VPS para semáforos de precios en fachadas).

* **Jorge Ramiro Chay Koyoc — Responsable de Fuente B (8 fuentes):**
  * `01-B` INEGI / Censos Económicos SAIC (Ingresos, personal y salarios en alimentos).
  * `02-B` datos.gob.mx / SNIIM (Precios de mayoreo diarios en la Central de Abasto).
  * `03-B` CONAPO / SIEGY (Índice de marginación urbana por colonias en Mérida).
  * `04-B` Geoportal Mérida (Capa SIG de tianguis y comercio rodante autorizado).
  * `06-B` Web Scraping (Monitoreo en Farmacias Guadalajara y tiendas OXXO).
  * `07-B` Self-Produced (Auditoría de campo en 5 tienditas de la esquina de Mérida).
  * `08-B` LiDAR / CEM (Malla de elevación continua CEM 3.0 de INEGI para drenaje).
  * `09-B` AR Geospatial (Catálogo y especificación de modelos 3D glTF/GLB para AR).

* **Isaac René Andrade Sánchez — Responsable de Fuente C (7 fuentes):**
  * `01-C` INEGI / ENOE (Microdatos 1T-2025 de hogares, viviendas y 45 catálogos).
  * `02-C` SEGALMEX / DICONSA (Catálogo oficial de artículos y proveedores DICONSA).
  * `03-C` SENASICA / SEDER (Inspección fitozoosanitaria y movilización agropecuaria).
  * `04-C` IMDUT / Va y Ven (565 rutas y paraderos de transporte conectando al Centro).
  * `06-C` Web Scraping (2,501 tickets comparando compra física vs delivery Rappi/Uber).
  * `08-C` OpenTopography (2,401 cotas satelitales SRTM/NASADEM Mérida vs montañas).
  * `09-C` AR Geospatial (Ruta de 6 waypoints AR hacia el pasillo más barato del mercado).

---

**Repositorio GitHub:** [IsaacRAS05/Visualization_data_sources](https://github.com/IsaacRAS05/Visualization_data_sources)
