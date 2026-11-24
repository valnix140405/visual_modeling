# 02-A · PROFECO Quién es Quién en los Precios (Mérida, 2026)

**Responsable:** Valeria Hernández  
**Última revisión de procedencia:** 2026-11-24

Precios de productos registrados por inspectores de PROFECO en establecimientos de Mérida.

| Archivo | Tamaño | URL de origen | Fecha de extracción | Licencia | Estado | Observaciones |
|---|---|---|---|---|---|---|
| [`profeco_merida_2026_real.csv`](profeco_merida_2026_real.csv) | 28,288 filas | https://datos.profeco.gob.mx/index.php (archivo `docs/qqp/QQP_2026.rar`) | Incorporado 2026-10-01 (registros de mayo 2026) | No indicada en los metadatos de PROFECO (verificar) | Completo | Todos los registros tienen `fecha_registro` de mayo de 2026, en formato `dd/mm/aaaa` (el archivo oficial usa `aaaa/mm/dd`). Contraste 2026-11-24: el `QQP_2026.rar` oficial no se pudo leer después de marzo (error de integridad); contra enero–marzo, 45 de 63 establecimientos y 2,151 de 2,634 productos coinciden, y 23 de 24 precios de una muestra están a ±20 %. |
| [`consultar_datos_gob.py`](consultar_datos_gob.py) | — | https://datos.gob.mx | — | — | Script | Explora el catálogo CKAN de datos.gob.mx. |

## Pendientes y cambios

- Se eliminó `profeco_qqp_merida_sample.csv` (muestra sintética de 20 filas).

**Estados:** Completo = el recurso descrito está en el repositorio. Revisar = hay un problema por confirmar. Prototipo = material de diseño elaborado por el equipo. Pendiente = no hay dato real todavía.
