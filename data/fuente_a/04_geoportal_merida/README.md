# 04-A · Mercados públicos de Mérida (DENUE)

**Responsable:** Valeria Hernández  
**Última revisión de procedencia:** 2026-11-24

Ubicación de los mercados públicos de Mérida, construida con los establecimientos que el DENUE registra dentro de un centro comercial de tipo «Mercado público». La coordenada de cada mercado es la mediana de la de sus establecimientos.

| Archivo | Tamaño | URL de origen | Fecha de extracción | Licencia | Estado | Observaciones |
|---|---|---|---|---|---|---|
| [`mercados_publicos_merida_denue.geojson`](mercados_publicos_merida_denue.geojson) | 15 elementos | https://www.inegi.org.mx/contenidos/masiva/denue/denue_31_csv.zip | 2026-11-24 | [Términos de Libre Uso de la Información del INEGI](https://www.inegi.org.mx/inegi/terminos.html) | Completo | Se unificaron variantes de escritura del nombre (p. ej. «Lucas de Galve», «Lucaz de Galvez»). Las variantes originales se conservan en `variantes_nombre_denue`. |
| [`visor_mercados_municipales.html`](visor_mercados_municipales.html) | — | — | — | — | Visor | Mapa Leaflet de la capa. |
| [`consultar_geoportal_api.py`](consultar_geoportal_api.py) | — | https://geoportal.merida.gob.mx | — | — | Script | Referencia a los servicios del Geoportal. |

## Pendientes y cambios

- Pendiente: la capa oficial del Geoportal de Mérida. El dominio respondió 403 al intentar la descarga automática el 2026-11-24.
- Se eliminó `mercados_municipales_merida.geojson`: los nombres eran reales, pero los atributos (locales activos, afluencia diaria, nivel de precios) no tenían fuente.

**Estados:** Completo = el recurso descrito está en el repositorio. Revisar = hay un problema por confirmar. Prototipo = material de diseño elaborado por el equipo. Pendiente = no hay dato real todavía.
