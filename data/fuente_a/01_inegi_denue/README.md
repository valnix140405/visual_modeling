# 01-A · INEGI DENUE: comercios de alimentos en Mérida

**Responsable:** Valeria Hernández  
**Última revisión de procedencia:** 2026-11-24

Establecimientos de comercio al por menor de alimentos (SCIAN 4611 y 4621) en el municipio de Mérida, filtrados del DENUE de Yucatán.

| Archivo | Tamaño | URL de origen | Fecha de extracción | Licencia | Estado | Observaciones |
|---|---|---|---|---|---|---|
| [`denue_merida_alimentos_real.csv`](denue_merida_alimentos_real.csv) | 7,520 filas | https://www.inegi.org.mx/app/descarga/?ti=6 | Incorporado 2026-10-01 | [Términos de Libre Uso de la Información del INEGI](https://www.inegi.org.mx/inegi/terminos.html) | Completo | Contraste 2026-11-24: los 7,520 registros coinciden al 100 % (nombre, actividad, coordenadas) con el DENUE oficial. Filtrado del DENUE Yucatán. El original completo (`denue_yucatan_oficial/`) se excluye de git por tamaño. |
| [`fetch_denue_api.py`](fetch_denue_api.py) | — | https://www.inegi.org.mx/servicios/api_denue.html | — | — | Script | Consulta la API del DENUE. Requiere la variable de entorno `INEGI_TOKEN`. |

## Pendientes y cambios

- Se eliminó `denue_merida_canasta_basica.csv`: era una muestra de 15 filas con nombres y razones sociales inventadas.

**Estados:** Completo = el recurso descrito está en el repositorio. Revisar = hay un problema por confirmar. Prototipo = material de diseño elaborado por el equipo. Pendiente = no hay dato real todavía.
