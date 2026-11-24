# 08-C · Relieve de Mérida frente a ciudades de montaña

**Responsable:** Isaac Andrade  
**Última revisión de procedencia:** 2026-11-24

Elevación real en mallas de 20 × 20 puntos (~17 km por lado) para Mérida, CDMX, Monterrey, Toluca, San Cristóbal de las Casas y Guanajuato.

| Archivo | Tamaño | URL de origen | Fecha de extracción | Licencia | Estado | Observaciones |
|---|---|---|---|---|---|---|
| [`topografia_merida_vs_ciudades_montana.csv`](topografia_merida_vs_ciudades_montana.csv) | 2,400 filas | https://registry.opendata.aws/terrain-tiles/ | 2026-11-24 | Verificar atribución requerida por Tilezen/AWS Terrain Tiles | Completo | Teselas Terrarium, zoom 12. Incluye la pendiente calculada entre puntos vecinos. |
| [`relieve_merida_terrain_tiles.ply`](relieve_merida_terrain_tiles.ply) | 2,500 puntos | — | 2026-11-24 | — | Completo | Malla de 50 × 50 puntos de Mérida para el visor 3D. **No es LiDAR.** |
| [`visor_3d_topografia_satelital.html`](visor_3d_topografia_satelital.html) | — | — | — | — | Visor |  |

## Pendientes y cambios

- Se eliminaron `topografia_srtm_nasadem_merida_vs_montanas.csv` y `nasa_gedi_dosel_merida_lidar.ply`: eran puntos generados con columnas SRTM, NASADEM y GEDI sin descarga real.

**Estados:** Completo = el recurso descrito está en el repositorio. Revisar = hay un problema por confirmar. Prototipo = material de diseño elaborado por el equipo. Pendiente = no hay dato real todavía.
