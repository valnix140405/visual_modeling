# Del Mundo a la Esquina: ¿Cuánto Cuesta Comer?
### Radiografía multiescalar del salario y la canasta básica: del panorama internacional al territorio de Mérida

**Sitio web:** https://valnix140405.github.io/visual_modeling/ (se publica con GitHub Pages desde `main`; ver [Publicación](#publicación))

Equipo 2 · Visual Modeling, UPY. Este repositorio reúne los datasets, scripts y visores del proyecto, organizados en un embudo **Internacional → México → Yucatán → Mérida**.

| Documento | Para qué sirve |
|---|---|
| [`FUENTES_DE_DATOS.md`](FUENTES_DE_DATOS.md) | Tabla maestra de las 22 fuentes: archivo, fuente real, estado y pendientes |
| `data/**/README.md` | Procedencia de cada archivo: URL de origen, fecha de extracción, licencia, estado |
| [`GUIA_FUENTES_Y_EQUIPO.md`](GUIA_FUENTES_Y_EQUIPO.md) | Título, subtemas y reparto del equipo |
| [`PROTOCOLO_INTEGRACION_PERSONA_B.md`](PROTOCOLO_INTEGRACION_PERSONA_B.md) | Reglas para subir cambios a la Fuente B |

## Estado de las fuentes

**12 completas con datos reales · 3 con dato real parcial · 3 pendientes sin dato · 1 por revisar · 3 prototipos de diseño (AR).**

El 2026-11-24 se eliminaron todos los datos simulados (generados con números aleatorios o escritos a mano sin fuente). Donde había un equivalente oficial descargable se reemplazaron (INEGI, PROFECO, CONEVAL, AWS Terrain Tiles); donde no, la fuente quedó como **Pendiente**. El detalle está en [`FUENTES_DE_DATOS.md`](FUENTES_DE_DATOS.md#cambios-del-2026-11-24).

Pendientes sin dato: **04-B** tianguis, **06-C** precios en apps de delivery y **08-A** LiDAR del Mercado Lucas de Gálvez.

## Estructura

```text
visual_modeling/
├── index.html                      # Presentación web principal
├── data/
│   ├── fuente_a/  (Valeria)        # 01-A DENUE · 02-A PROFECO · 03-A CONEVAL+Censo · 04-A Mercados · 06-A Súper · 08-A LiDAR · 09-A AR
│   ├── fuente_b/  (Ramiro)         # 01-B Censos Económicos · 02-B Central de Abasto · 03-B AGEB · 04-B Tianguis · 06-B Farmacias · 07-B Tienditas · 08-B Elevación · 09-B AR
│   ├── fuente_c/  (Isaac)          # 01-C ENOE · 02-C DICONSA · 03-C SENASICA · 04-C Transporte · 06-C Delivery · 08-C Relieve · 09-C AR
│   ├── visor_lidar_unificado.html  # Visor 3D de elevación
│   └── visor_ar_unificado.html     # Prototipo de recorrido AR
├── reports/
│   ├── figuras/                    # Gráficas generadas con datos reales
│   └── looker_studio/              # Tablas listas para Looker Studio
├── scripts/                        # Generación de datos, análisis y verificación
├── .github/workflows/pages.yml     # Publicación automática en GitHub Pages
└── requirements.txt
```

## Reproducir

```bash
pip install -r requirements.txt
python scripts/generar_datos_reales.py   # descarga originales (INEGI, CONEVAL, teselas de elevación) y regenera los datasets
python scripts/verificar_datasets.py     # lista fuentes listas y pendientes
python scripts/verificar_links_index.py  # comprueba que los enlaces de index.html existen
```

Los originales descargados se guardan en `.cache_descargas/`, que git ignora. El DENUE completo de Yucatán pesa unos 70 MB descomprimido.

## Visores

Abre los archivos desde el sitio publicado o con un servidor local (`python -m http.server`); algunos visores no cargan los `.ply` si se abren con doble clic.

| Visor | Datos |
|---|---|
| [`index.html`](index.html) | Presentación del proyecto |
| [`catalogo/index.html`](catalogo/index.html) | Catálogo de visualizaciones de los 9 equipos, con filtros; PDF imprimible en `catalogo/catalogo_visualizaciones.pdf` (`python scripts/generar_catalogo.py --pdf`) |
| [`data/fuente_a/04_geoportal_merida/visor_mercados_municipales.html`](data/fuente_a/04_geoportal_merida/visor_mercados_municipales.html) | Mercados públicos de Mérida (DENUE) |
| [`data/visor_lidar_unificado.html`](data/visor_lidar_unificado.html) | Elevación del Centro y relieve de Mérida (AWS Terrain Tiles). No es LiDAR |
| [`data/visor_ar_unificado.html`](data/visor_ar_unificado.html) | Prototipo de diseño AR, sin datos de fuente |

## Publicación

El workflow [`.github/workflows/pages.yml`](.github/workflows/pages.yml) publica la raíz del repositorio en cada push a `main`. Se activa una sola vez en **Settings → Pages → Build and deployment → Source: GitHub Actions**.

## Equipo

* **Valeria Nicol Hernández León**: Fuente A
* **Jorge Ramiro Chay Koyoc**: Fuente B
* **Isaac René Andrade Sánchez**: Fuente C
