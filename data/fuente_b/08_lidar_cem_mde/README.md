# 08-B · Elevación del Centro de Mérida

**Responsable:** Jorge Ramiro Chay  
**Última revisión de procedencia:** 2026-11-24

Malla de 41 × 41 puntos (~1.6 km por lado) alrededor del Mercado Lucas de Gálvez, con elevación real y pendiente calculada.

| Archivo | Tamaño | URL de origen | Fecha de extracción | Licencia | Estado | Observaciones |
|---|---|---|---|---|---|---|
| [`elevacion_centro_merida_grid.csv`](elevacion_centro_merida_grid.csv) | 1,681 filas | https://registry.opendata.aws/terrain-tiles/ | 2026-11-24 | Verificar atribución requerida por Tilezen/AWS Terrain Tiles | Completo | Teselas Terrarium, zoom 15. Supuesto: para México combinan SRTM y otras fuentes de resolución ~30 m, por lo que no capturan edificios. |
| [`elevacion_centro_merida.ply`](elevacion_centro_merida.ply) | 1,681 puntos | — | 2026-11-24 | — | Completo | La misma malla como nube de puntos para Three.js. **No es LiDAR.** |
| [`visor_3d_terreno_mde.html`](visor_3d_terreno_mde.html) | — | — | — | — | Visor |  |

## Pendientes y cambios

- Pendiente: el Continuo de Elevaciones Mexicano (CEM) de INEGI. Se descarga desde https://www.inegi.org.mx/app/geo2/elevacionesmex/, que requiere selección manual.
- Se eliminaron `inegi_cem_mde_merida_grid.csv` y `.ply`: eran 15 celdas con valores escritos a mano.

**Estados:** Completo = el recurso descrito está en el repositorio. Revisar = hay un problema por confirmar. Prototipo = material de diseño elaborado por el equipo. Pendiente = no hay dato real todavía.
