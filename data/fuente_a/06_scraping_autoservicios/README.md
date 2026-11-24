# 06-A · Precios de canasta en autoservicios (PROFECO)

**Responsable:** Valeria Hernández  
**Última revisión de procedencia:** 2026-11-24

Resumen por producto y cadena de los precios reales de PROFECO QQP en supermercados de Mérida (Walmart, Soriana, Chedraui, Bodega Aurrera, Súper Akí Xtra y Dunosusa).

| Archivo | Tamaño | URL de origen | Fecha de extracción | Licencia | Estado | Observaciones |
|---|---|---|---|---|---|---|
| [`precios_canasta_supermercados_reales.csv`](precios_canasta_supermercados_reales.csv) | 69 filas | https://datos.profeco.gob.mx/datos_abiertos/qqp.php | 2026-11-24 (registros de mayo 2026) | Libre Uso MX de datos.gob.mx (verificar en la ficha del dataset) | Completo | Promedio, mínimo y máximo por cadena, usando para cada producto la misma presentación en todas las cadenas (la más frecuente en el conjunto). Se genera con `python scripts/generar_datos_reales.py`. |

## Pendientes y cambios

- Pendiente: un scraping real de tiendas en línea. El scraper anterior generaba precios con números aleatorios y se eliminó junto con `precios_canasta_scraping.csv`.

**Estados:** Completo = el recurso descrito está en el repositorio. Revisar = hay un problema por confirmar. Prototipo = material de diseño elaborado por el equipo. Pendiente = no hay dato real todavía.
