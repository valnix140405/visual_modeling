# Ficha del capítulo · Equipo 2 · Del Mundo a la Esquina

**Acto 2 · Vivir aquí**  
**Integrantes:** Valeria Nicol Hernández León, Jorge Ramiro Chay Koyoc, Isaac René Andrade Sánchez  
**Repositorio:** https://github.com/valnix140405/visual_modeling (carpeta `booklet/`)  
**Escenas en D3:** [`graficas/index.html`](graficas/index.html) (capítulo completo) y una página por escena en [`graficas/`](graficas/)

---

## Título-hallazgo

**El mes que se come tu sueldo: 28 días pa' la panza**

## Pregunta del capítulo

¿Alcanza el salario para comer en Mérida?

## Entrada

Con el salario mínimo, alimentar a un hogar típico de Mérida se lleva casi todo el mes de trabajo. Y lo que pagas en la caja depende de dónde compras: por el mismo producto, el súper cobra en mediana 19 % más que la Central de Abasto. La tienda de conveniencia y la tiendita de la esquina no siempre son las más caras, pero el sobreprecio aparece donde menos se espera.

## La historia en 10 segundos: 3 cifras

| Cifra | Qué dice | Fuente y corte | Archivo |
|---|---|---|---|
| **27.9 días** | de salario mínimo general 2025 ($278.80 diarios) cuesta un mes de canasta alimentaria urbana para un hogar de 3.27 personas ($7,780.87) | CONEVAL (canasta, marzo 2025); INEGI Censo 2020 (ocupantes por vivienda); CONASAMI (salario mínimo 2025) | `datos/escena-1.csv`: `dias_canasta` |
| **+19.0 %** | diferencia mediana del súper frente a la Central de Abasto en 139 productos con la misma presentación; el súper fue más caro en 103 de ellos | PROFECO, Quién es Quién en los Precios, Mérida · mayo 2026 | `datos/escena-2.csv`: mediana de `diferencia_pct` |
| **+174.3 %** | más cara la cebolla blanca en el súper ($29.90/kg) que en la Central de Abasto ($10.90/kg) | PROFECO, Quién es Quién en los Precios, Mérida · mayo 2026 | `datos/escena-2.csv`: fila «Cebolla · 1 Kg. Granel. Blanca Sin Rabo» |

## Escenas

| # | Título-hallazgo (se arma con los datos) | Tipo | Datos | Página D3 |
|---|---|---|---|---|
| 1 | El mes que se come tu sueldo: 28 días pa' la panza | Calendario de 30 días | `datos/escena-1.csv` | `graficas/escena-1.html` |
| 2 | Mismo producto, otro pasillo: la cebolla cuesta 174 % más en el súper | Barras horizontales con mediana (10 que más suben y 3 que más bajan) | `datos/escena-2.csv` | `graficas/escena-2.html` |
| 3 | El impuesto a la flojera: hasta +56 % por no caminar al súper | Pesas (conveniencia contra súper), 7 productos | `datos/escena-3.csv` | `graficas/escena-3.html` |
| 4 | David contra Goliat: la tiendita solo le gana al súper en la leche (−29.7 %) | Pesas (tiendita contra súper), 4 productos | `datos/escena-4.csv` | `graficas/escena-4.html` |

Los títulos y subtítulos de las gráficas se escriben con las cifras que leen de su CSV; si el CSV cambia, el texto cambia con él. Colores: morado = lo que se analiza (súper en la escena 2, conveniencia en la 3, tiendita en la 4); oro = contra qué se compara; gris = contexto; oro oscuro = anotaciones.

### Lectura de cada escena

1. **Calendario.** De 30 días del mes, 27.9 se van en la comida del hogar y quedan 2.1 para renta, luz, transporte, escuela y salud.
2. **Central de Abasto contra súper.** Las verduras y los granos a granel son los que más se encarecen en el súper; en 36 de 139 productos el súper sale más barato.
3. **Conveniencia contra súper.** En 93 productos comparables la conveniencia fue más cara en 49, con una diferencia mediana de +1.3 %. El sobreprecio grande se concentra en bebidas (suero oral +56.4 %, agua de 1 L +53.3 %, yoghurt bebible +48.9 %) y sopas instantáneas.
4. **Tiendita contra súper.** En 5 tienditas, la leche LALA de 1 L estaba 29.7 % más barata que en el súper; el pan Bimbo, 39.5 % más caro; la tortilla, el doble (+103.8 %, con solo 2 precios). **Es una muestra chica:** de 2 a 5 precios por producto en tienditas, así que ilustra, no generaliza.

## Lo que estos datos no dicen

- **Muestra chica en la escena 4:** la bitácora propia es de 5 tienditas, con 2 a 5 precios por producto y visitas del 26 de septiembre al 1 de octubre de 2026. No representa a todas las tienditas de Mérida.
- **Un solo mes de precios:** PROFECO es de mayo de 2026 y solo cubre las sucursales que visitan sus inspectores. No muestra cómo cambian los precios en el año.
- **Precios al público, no de mayoreo:** la Central de Abasto también es precio al consumidor; no dice lo que recibe el productor ni el margen del intermediario.
- **La canasta es nacional:** la línea de CONEVAL es urbana nacional, no específica de Mérida, y está en pesos corrientes de marzo de 2025 (sin deflactar).
- **Salario mínimo como unidad:** se usa el salario mínimo general 2025 para empatar con el último dato de CONEVAL; no es el ingreso real de los hogares. En 2026 el mínimo general es de $315.04 diarios (CONASAMI).
- **Lo que cuesta llegar:** no se incluye el tiempo ni el transporte para ir a la Central de Abasto o al súper.
- **Promedio y mediana:** la escena 2 usa medianas; la escena 3, promedios con 3 o más registros por canal; la escena 4, medianas. Se indica en cada subtítulo.

## Frase puente

**Al siguiente capítulo (Equipo 5, Acto 2):** «Si comer se lleva casi todo el mes, ¿cómo se siente vivir aquí? El siguiente capítulo pregunta qué tan seguros nos sentimos en Mérida.»

**Material puente al Acto 4 (Plana sobre el agua):** «Mérida es plana: 16.2 m de desnivel en 17 km, contra 1,413 m en San Cristóbal de las Casas. Aquí caminar al mercado no cuesta esfuerzo, pero el agua de lluvia no tiene a dónde escurrir.»
- Datos: `datos/puente-relieve.csv` (malla de 20 × 20 puntos por ciudad).
- Imagen fija del visor 3D: [`img/relieve_merida_3d.png`](img/relieve_merida_3d.png), con QR al visor: [`img/qr_visor_relieve_3d.png`](img/qr_visor_relieve_3d.png) → https://valnix140405.github.io/visual_modeling/data/visor_relieve_3d.html
- Nota: el visor usa una malla más fina (50 × 50 puntos) y muestra de 1.0 a 21.0 m; la cifra del texto (16.2 m) sale de la malla de 20 × 20 del CSV. Ambas son elevación de AWS Terrain Tiles, no LiDAR.

## Fallas del repositorio (sección 6 del plan)

| Falla | Estado |
|---|---|
| Gráficas en matplotlib y cifras escritas en el HTML | **Corregida para el booklet:** las 4 escenas están en D3 v7 (`d3@7.9.0`) y todas sus cifras se leen de `datos/*.csv`, que genera `scripts/generar_datos_booklet.py` desde los archivos del repositorio. **El sitio web** (`index.html`) sigue siendo un complemento con cifras escritas en el HTML; se auditaron una por una el 2026-11-24 (`reports/validacion/`), pero no se reescribió en D3 por tiempo. |
| `data/visor_lidar_unificado.html` no es LiDAR | **Corregida:** se renombró a `data/visor_relieve_3d.html` y se actualizaron los enlaces. Las carpetas `data/fuente_a/08_lidar_mercado/` y `data/fuente_b/08_lidar_cem_mde/` conservan su nombre original de la matriz de fuentes; sus README aclaran que es elevación, no LiDAR. |
| Prototipo AR sin datos | **Fuera del booklet.** No aparece en ninguna escena; ya se había retirado del sitio. |
| La bitácora es de 5 tienditas | **Corregida:** se dice en el subtítulo y en una nota de la escena 4, y en «Lo que estos datos no dicen». |
| Título de la página en inglés («UPY Data Engineering») | **Corregida:** «Del Mundo a la Esquina: ¿Cuánto Cuesta Comer? · Ingeniería de Datos UPY». |

## Cómo verlo y regenerarlo

```bash
python scripts/generar_datos_booklet.py   # regenera booklet/datos/*.csv desde el repositorio
python -m http.server 8000                # desde la raíz del repositorio
# abrir http://localhost:8000/booklet/graficas/index.html
```

Los módulos de JavaScript no cargan si el HTML se abre con doble clic; hace falta el servidor local o el sitio publicado.
