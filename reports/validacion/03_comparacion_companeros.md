# Comparación del dashboard final con los compañeros

**Fecha:** 2026-11-24.

> **Actualización:** después de esta comparación ya se corrigieron el desbordamiento del encabezado en móvil (390 px sin scroll horizontal) y la falta de metodología (nuevo capítulo 08 en `index.html`). Las capturas citadas no se guardaron en el repositorio.

**Fuentes de la evidencia:**
- Sitios publicados, abiertos con Playwright en escritorio (1440×900) y móvil (390×844). Las capturas están en `comparacion/`.
- Repos actualizados con `git pull`:

| Repo | Commit | Fecha |
|---|---|---|
| Russel | `1a546bd` | 2026-10-07 |
| Rivaldo | `59902e9` | 2026-10-19 |
| Lorena | `78699f0` | 2026-11-17 |

## Tabla comparativa

| Criterio (plan del profesor) | Valeria | Russel | Rivaldo | Lorena |
|---|---|---|---|---|
| **Los datos mostrados son reales** | ✅ Cifras calculadas de archivos oficiales del repo (PROFECO, DENUE, CONEVAL, Censo). Los visores cargan los `.ply` y el GeoJSON reales. | ❌ Todo está escrito a mano en `js/data/viewsData.js` (35 KB); el sitio no lee ningún archivo de datos. Los datos del repo son `sample_*`. La nube LiDAR 3D se genera con `Math.random` (`threeVisuals.js:186-190`). | ❌ Igual que Russel (es la misma plantilla). Además, `charts.js:74` multiplica los datos por un factor aleatorio de 0.92 a 1.16 cada vez que se pulsa «Actualizar». El mapa de un tema peatonal muestra «Mérida (2,150 un.) … hospitales de tercer nivel», texto copiado de la plantilla de salud. El repo no tiene ningún CSV. | — (sin sitio) |
| **Sitio publicado y sin errores** | ✅ 0 errores de consola y 0 peticiones fallidas; carga en 1.2 s, ~86 KB. | ✅ 0 errores; carga en 2.3 s, ~680 KB. | ✅ 0 errores; carga en 1.3 s, ~470 KB. | ❌ Sin sitio. |
| **Narrativa común (overview y secciones conectadas)** | ✅ 7 capítulos con una pregunta guía («¿Por qué comer cuesta más donde menos se gana?») y modo presentación o matriz completa. | ✅ «Hilo narrativo» de 4 actos y 9 vistas, auto-tour y narración por voz. | ✅ Misma estructura que Russel. | ❌ |
| **KPIs con unidad y fuente** | ✅ Tarjetas con unidad y una línea «Fuente: PROFECO QQP, Mérida, mayo 2026 (02-A)» bajo las gráficas. | ⚠️ Muestran fuente principal y complementarias, pero las cifras (p. ej. «2,150 unidades médicas») no tienen respaldo en datos. | ⚠️ Igual que Russel. | — |
| **Filtros e interacción** | ⚠️ 1 control de filtro en la página principal; la interacción está en los visores (3D y mapa). | ✅ Filtros por capa en el mapa (Todos, Hospitales, Clínicas, Farmacias) y pasos guiados que enfocan el mapa. | ✅ Modos Mapa/Histograma y pasos guiados. | — |
| **Procedencia y fecha de corte visibles** | ✅ 7 menciones de fecha de corte (mayo 2026, marzo 2025) y 7 líneas «Fuente:» en modo matriz. | ⚠️ Botón «Metodología & Datos», pero no muestra fechas reales de extracción. | ⚠️ Igual que Russel. | ✅ Cada recurso con URL original y estado. |
| **Metodología explicada** | ❌ La palabra «metodología» no aparece en el sitio. Hay notas sueltas (p. ej. «mediana, misma presentación») pero no una sección de método. | ✅ Botón dedicado «Metodología & Datos». | ✅ Igual que Russel. | ⚠️ Solo en los README. |
| **Honestidad sobre pendientes** | ✅ 13 menciones de «Pendiente» en el sitio. Los visores AR están marcados como prototipo y el de relieve aclara que no es LiDAR. | ❌ No avisa que los datos son de muestra. | ❌ No avisa; los datos además cambian al azar. | ✅ Ejemplar: tabla completo / parcial / pendiente con motivo, p. ej. «es un CAPTCHA», «no es LiDAR». |
| **Mapas y 3D funcionales** | ✅ Mapa Leaflet con 15 mercados del DENUE; relieve 3D con elevación real. | ✅ El mapa Leaflet funciona; el 3D es aleatorio. | ⚠️ El mapa es un SVG esquemático, no un mapa base; el 3D es aleatorio. | — |
| **Responsive móvil** | ❌ **El encabezado desborda a 675 px en un viewport de 390 px**: `.header-actions` y `.view-switch` no se acomodan. Los visores sí caben (390 px). | ✅ Sin desborde (390 px). | ✅ Sin desborde (390 px). | — |
| **Accesibilidad básica** | ✅ `lang="es"`, 1 h1 y 6 h2, imágenes con `alt`. | ⚠️ 12 imágenes sin `alt` (teselas del mapa) y 0 h2. | ⚠️ 0 h2. | — |
| **Reproducibilidad** | ✅ `scripts/generar_datos_reales.py`, `requirements.txt` y verificadores. | ⚠️ El workflow de Pages es reproducible, pero los datos no se generan desde la fuente. | ⚠️ Scripts en `scripts/`, pero el sitio no consume sus salidas. | ⚠️ Los originales están guardados, sin scripts. |
| **Catálogo con estado por recurso (estilo Lorena)** | ✅ 22 README de carpeta con URL, fecha de extracción, licencia, estado y observaciones, más la tabla maestra. | ⚠️ README por carpeta, pero sin estado ni fecha. | ⚠️ Igual que Russel. | ✅ Referencia del grupo. |

### Conclusión

Por veracidad y documentación, el repo de Valeria ya está a la par de Lorena o por encima, porque además tiene sitio y scripts reproducibles. Es el único de los tres sitios cuyas cifras salen de datos reales. Los de Russel y Rivaldo se ven más pulidos como producto, pero sus datos están escritos a mano o son aleatorios. Donde todavía pierde Valeria: experiencia móvil, una sección de metodología y la interacción en la página principal.

## Lo que le falta al dashboard de Valeria (priorizado)

1. **Arreglar el encabezado en móvil** (esfuerzo bajo). En 390 px la página se desborda a 675 px; hay que hacer que `.header-actions` y `.view-switch` bajen a otra línea o se oculten tras un menú. Hoy es el único fallo visible frente a Russel y Rivaldo.
2. **Agregar una sección «Metodología y datos»** (bajo). Un botón o capítulo con fuentes, fecha de corte, cálculos (mediana, misma presentación, pares comparables), limitaciones y enlace a `FUENTES_DE_DATOS.md`. Russel y Rivaldo la tienen y el plan la pide.
3. **Agregar filtros en la página principal** (medio). Por ejemplo, selector de producto o cadena en la comparación Abasto vs. súper, o de AGEB en los indicadores del Censo. El plan pide filtros acordados con los equipos 1 y 2.
4. **Agregar un mapa base en la página principal** (medio). Russel muestra el mapa Leaflet en la portada; en Valeria el mapa solo está en un visor aparte.
5. **Hacer que la página lea los CSV en lugar de tener las cifras escritas en el HTML** (medio). Hoy las cifras son correctas, pero están fijas en `index.html`; si cambian los datos, quedan desactualizadas.
6. **Agregar un recorrido guiado o narración** (medio). El auto-tour es el principal atractivo del producto de Russel.
7. **Mostrar la tabla de estado de fuentes dentro del sitio** (bajo). Completo, parcial, pendiente y prototipo, como Lorena pero visible en el dashboard; hoy solo está en el repo.
8. **Exportar a PDF o versión impresa** (alto). El plan pide una versión estática con fecha de corte y QR al producto digital; ningún equipo la tiene todavía.
