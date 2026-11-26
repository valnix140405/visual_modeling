# Guía de armado en Looker Studio: informe narrativo

**Proyecto:** Del Mundo a la Esquina: ¿Cuánto Cuesta Comer? (UPY)  
**Entregable:** informe de Looker Studio de 8 páginas que cuenta una historia de principio a fin. Solo usa las 16 fuentes con datos reales.

Todas las cifras de esta guía salen de los archivos del repositorio y se auditaron el 2026-11-24 (ver [`reports/validacion/`](../validacion/)). Si regeneras las tablas, revisa que los títulos y textos sigan coincidiendo con las tarjetas de KPI.

---

## 1. La historia en una línea

> **En Mérida, lo que cuesta comer depende de dónde compras, y la diferencia se paga con días de trabajo.**

El informe avanza de lo general a la esquina. Cada página responde una pregunta y deja la siguiente:

| Página | Escena | Pregunta | Hallazgo (título de la página) |
|---|---|---|---|
| 1 | Portada | ¿Cuánto cuesta comer en Mérida? | Comer cuesta distinto según dónde compras |
| 2 | El pasillo | ¿Importa dónde compro? | El súper cobra más en 3 de cada 4 productos |
| 3 | La prisa | ¿Comprar en la tienda de conveniencia sale caro? | La prisa se paga en bebidas, no en todo |
| 4 | La esquina | ¿Y la tiendita de la colonia? | La tiendita no siempre es la más cara |
| 5 | El sueldo | ¿Cuánto trabajo cuesta la canasta? | Casi 28 días de salario mínimo para alimentar a un hogar |
| 6 | El territorio | ¿Dónde están los mercados y quién vive lejos de ellos? | El abasto popular se concentra en el Centro |
| 7 | La ciudad plana | ¿El terreno ayuda o estorba? | Mérida es plana: 16 m de desnivel en 17 km |
| 8 | Cierre | ¿Qué significa y de dónde salen los datos? | Dónde compras pesa tanto como cuánto ganas |

---

## 2. Plantilla de cada escena

Todas las páginas comparten el mismo esqueleto, para que la persona aprenda a leerlas desde la segunda:

```text
┌────────────────────────────────────────────────────────────────────┐
│ ESCENA N DE 8 · PREGUNTA (texto pequeño, morado, mayúsculas)       │
│ TÍTULO-HALLAZGO (grande, una afirmación con cifra)                 │
│ Bajada: 1 o 2 líneas que explican el título                        │
├───────────────────────────────────────────┬────────────────────────┤
│                                           │ 2 o 3 tarjetas de KPI  │
│   GRÁFICA PRINCIPAL                       │                        │
│   (con anotación sobre el dato clave)     │ ¿QUÉ SIGNIFICA?        │
│                                           │ (2-3 líneas)           │
├───────────────────────────────────────────┴────────────────────────┤
│ Controles de filtro (si aplican)                                   │
│ Fuente · fecha de corte                [ Siguiente: escena → ]     │
└────────────────────────────────────────────────────────────────────┘
```

**Cómo hacer cada pieza en Looker Studio**

| Pieza | Componente | Formato |
|---|---|---|
| Pregunta | Cuadro de texto | 11 px, mayúsculas, color `#600d8b` |
| Título-hallazgo | Cuadro de texto | 26-28 px, negrita, `#0d0d0d` |
| Bajada y «¿Qué significa?» | Cuadro de texto | 13-14 px, `#404040`; «¿Qué significa?» sobre fondo `#fdf3e3` |
| Anotación | Cuadro de texto + Línea (Insertar → Línea) | Texto corto con la cifra, flecha hacia la barra o el punto |
| Fuente y fecha de corte | Cuadro de texto | 10 px, gris |
| Botón «Siguiente» | Insertar → Botón → Navegación a una página | Fondo `#600d8b`, texto blanco |

**Reglas de estilo**

- **Color con significado:** morado `#600d8b` = supermercado o el dato protagonista; oro `#ed9f22` = el otro canal o lo que se compara; gris = contexto. Úsalo igual en todas las páginas.
- **Un mensaje por página:** si una gráfica no apoya el título, va en otra página o se elimina.
- **Títulos que afirman:** «El súper cobra más en 3 de cada 4 productos», no «Comparativa de precios».
- **Navegación:** Archivo → Configuración del informe → Navegación: **pestañas a la izquierda**, con nombres «1. Portada», «2. El pasillo», etc.

### Ilustraciones narrativas (el toque de humor)

Looker Studio no tiene gráficas ilustradas, así que estas 6 se generan con datos reales y se insertan como **imagen** (Insertar → Imagen → Subir), una por escena. Están en [`reports/figuras/narrativas/`](../figuras/narrativas/) y se regeneran con `python scripts/generar_graficas_narrativas.py`.

| Escena | Imagen | Chiste |
|---|---|---|
| 2 · El pasillo | `n4_cebolla_llorona.png` | Hasta la cebolla llora |
| 3 · La prisa | `n5_impuesto_flojera.png` | El impuesto a la flojera |
| 4 · La esquina | `n6_david_vs_goliat.png` | David contra Goliat en la esquina |
| 5 · El sueldo | `n2_calendario_canasta.png` y `n3_tortillometro.png` | Te quedan 2 días… para todo lo demás · Tu sueldo, en kilos de tortilla |
| 7 · La ciudad plana | `n1_merida_plana_precios_no.png` | Mérida es plana. Sus precios, no. |

Úsalas como **imagen protagonista** de su escena y deja la gráfica de Looker con filtros como apoyo para quien quiera explorar. En la portada puedes usar `n1` como imagen de cabecera, porque resume toda la historia.

---

## 3. Fuentes de datos

Se regeneran con:

```bash
python scripts/generar_datos_web.py            # looker_05
python scripts/generar_tablas_looker_studio.py # looker_01 a 04 y 06 a 08
```

| Archivo | Filas | Contenido | Escena |
|---|---:|---|---|
| [`looker_01_precios_multicanal.csv`](looker_01_precios_multicanal.csv) | 26,281 | Un precio por fila con `canal`, establecimiento, producto, presentación y `precio_mxn` | 1 |
| [`looker_02_territorio_geo.csv`](looker_02_territorio_geo.csv) | 65 | Mercados públicos (DENUE) y establecimientos PROFECO con `coordenadas_looker` | 6 |
| [`looker_03_lineas_pobreza_coneval.csv`](looker_03_lineas_pobreza_coneval.csv) | 87 | Líneas de pobreza CONEVAL, 2018-01 a 2025-03 | 5 |
| [`looker_04_ageb_censo2020_merida.csv`](looker_04_ageb_censo2020_merida.csv) | 520 | AGEB urbanas habitadas de Mérida (Censo 2020) | 6 |
| [`looker_05_comparables_por_canal.csv`](looker_05_comparables_por_canal.csv) | 232 | Pares de producto y presentación idénticos por canal, con `diferencia_pct` y `resultado` | 1, 2, 3 |
| [`looker_06_relieve_ciudades.csv`](looker_06_relieve_ciudades.csv) | 2,400 | Elevación real de Mérida y 5 ciudades de montaña | 7 |
| [`looker_07_catalogo_fuentes.csv`](looker_07_catalogo_fuentes.csv) | 16 | Catálogo de las 16 fuentes usadas | 1, 8 |
| [`looker_08_tienditas_vs_super.csv`](looker_08_tienditas_vs_super.csv) | 4 | Bitácora propia vs. supermercados en 4 productos equivalentes | 4 |

### Importar y ajustar tipos

1. En [lookerstudio.google.com](https://lookerstudio.google.com/) crea un **Informe vacío** y agrega cada CSV con **Agregar datos → Subir archivo**. Si `looker_01` (5.5 MB) da problemas, súbelo a Google Sheets.
2. Ajusta los tipos de campo en cada fuente:
   - `looker_02.coordenadas_looker` → **Geo → Latitud, longitud**.
   - `precio_*` y `mediana_*_mxn` → **Moneda (MXN)**.
   - `diferencia_pct`, `diferencia_pct_tiendita_vs_super` y `pct_*` → **Número**. Ya vienen en porcentaje (19.0 = 19 %), así que no uses el formato «Porcentaje» o se multiplicarán por 100.
   - `looker_03.periodo` → **Fecha → Año y mes**.
   - `looker_04.AGEB` → **Texto**.

### Campos calculados y parámetros

| Fuente | Nombre | Fórmula o configuración |
|---|---|---|
| looker_05 | `pct_mas_caro` | `SUM(CASE WHEN diferencia_pct > 0 THEN 1 ELSE 0 END) / COUNT(producto)`, formato Porcentaje |
| looker_05 | `mediana_diferencia` | `MEDIAN(diferencia_pct)` |
| looker_04 | `rango_sin_afiliacion` | `CASE WHEN pct_sin_afiliacion_salud < 15 THEN "0-15 %" WHEN pct_sin_afiliacion_salud < 20 THEN "15-20 %" WHEN pct_sin_afiliacion_salud < 25 THEN "20-25 %" WHEN pct_sin_afiliacion_salud < 30 THEN "25-30 %" WHEN pct_sin_afiliacion_salud < 40 THEN "30-40 %" ELSE "40 % o más" END` |
| looker_06 | `desnivel_m` | `MAX(elevacion_m_snm) - MIN(elevacion_m_snm)` |
| looker_03 | **Parámetro** `sueldo_mensual` | Recurso → Administrar fuentes → Editar `looker_03` → **Agregar un parámetro**. Tipo Número (decimal), valor predeterminado `8364` (salario mínimo general 2025: $278.80 × 30, CONASAMI), rango permitido de 1 a 200,000 |
| looker_03 | `canasta_hogar_mxn` | `SUM(lpei_canasta_alimentaria_urbana_mxn) * 3.27` (3.27 ocupantes por vivienda en Mérida, Censo 2020) |
| looker_03 | `dias_de_trabajo_canasta` | `SUM(lpei_canasta_alimentaria_urbana_mxn) * 3.27 / (sueldo_mensual / 30)` |
| looker_03 | `pct_sueldo_canasta` | `SUM(lpei_canasta_alimentaria_urbana_mxn) * 3.27 / sueldo_mensual`, formato Porcentaje |
| looker_03 | `kilos_tortilla` | `sueldo_mensual / 29.5` (tortilla de maíz: mediana PROFECO en tortillerías, $29.50/kg, mayo 2026) |

---

## 4. Las 8 escenas

### Escena 1 · Portada: «Comer cuesta distinto según dónde compras»

- **Pregunta:** ¿CUÁNTO CUESTA COMER EN MÉRIDA?
- **Bajada:** «Cruzamos precios oficiales de PROFECO, el Censo y el DENUE de INEGI y las líneas de pobreza de CONEVAL con una bitácora propia de cinco tienditas. Este informe sigue el dinero del pasillo del súper a la esquina.»
- **Hilo en 4 tarjetas grandes, en orden de lectura** (son la historia completa en una sola vista):
  1. «74.1 %»: productos donde el súper cobra más que la Central de Abasto (`looker_05`, filtro Central de Abasto, métrica `pct_mas_caro`).
  2. «+1.3 %»: lo que cobra de más, en mediana, la tienda de conveniencia (`looker_05`, filtro Conveniencia, `mediana_diferencia`).
  3. «27.9 días»: de salario mínimo para la canasta de un hogar (escena 5).
  4. «16»: fuentes con dato real (`looker_07`, recuento).
- **Debajo:** una línea por escena con su pregunta, como índice.
- **Fuente:** PROFECO QQP mayo 2026; CONEVAL mar 2025; INEGI Censo 2020 y DENUE.
- **Botón:** «Empezar: el pasillo →».

### Escena 2 · El pasillo: «El súper cobra más en 3 de cada 4 productos»

- **Fuente de datos:** `looker_05`, filtro de página `canal_comparado` = Central de Abasto.
- **Pregunta:** ¿IMPORTA DÓNDE COMPRO?
- **Bajada:** «Comparamos 139 productos con la misma presentación en la Central de Abasto y en supermercados. El súper fue más caro en 103.»
- **Gráfica principal:** barras horizontales con dimensión `producto` y métrica `diferencia_pct`, orden descendente, 15 barras. Color por `resultado` (morado = súper más caro, oro = súper más barato).
- **Anotación:** sobre la barra de cebolla, «Cebolla: $10.90 en el Abasto, $29.90 en el súper (+174 %)».
- **Imagen:** `n4_cebolla_llorona.png` a la derecha de la gráfica.
- **Tarjetas:** recuento de `producto` (139), `pct_mas_caro` (74.1 %), `mediana_diferencia` (+19.0 %).
- **¿Qué significa?** «Comprar en el súper cuesta, en mediana, 19 % más por el mismo producto. No todo: en 36 productos el súper sale más barato, así que conviene comparar antes de elegir dónde comprar.»
- **Controles:** lista desplegable `categoria`, lista desplegable `resultado`, cuadro de entrada `producto`.
- **Fuente:** PROFECO QQP Mérida, mayo 2026. Mediana por producto y presentación idénticos. Son precios al público, no de mayoreo.
- **Botón:** «Siguiente: la prisa →».

### Escena 3 · La prisa: «La prisa se paga en bebidas, no en todo»

- **Fuente de datos:** `looker_05`, filtro de página `canal_comparado` = Conveniencia.
- **Pregunta:** ¿COMPRAR EN LA TIENDA DE CONVENIENCIA SALE CARO?
- **Bajada:** «En 93 productos comparables, OXXO, 7 Eleven y Dunosusa fueron más caros que el súper en 49. Pero la diferencia mediana es de apenas +1.3 %.»
- **Gráfica principal:** barras con dimensión `categoria` y métrica `mediana_diferencia`, orden descendente. Muestra en qué tipo de producto se concentra el sobreprecio.
- **Segunda gráfica (pequeña):** los 5 productos con mayor `diferencia_pct`.
- **Imagen:** `n5_impuesto_flojera.png` como protagonista; la gráfica por categoría queda debajo.
- **Anotación:** sobre la barra del suero oral, «Suero oral 625 ml: $37.67 en conveniencia vs. $24.08 en el súper (+56.4 %)».
- **Tarjetas:** recuento (93), `pct_mas_caro` (52.7 %), `mediana_diferencia` (+1.3 %).
- **¿Qué significa?** «Comprar por comodidad no siempre sale caro. El sobreprecio se concentra en pocos productos: 4 de los 5 con mayor diferencia son bebidas (suero oral +56.4 %, agua de 1 L +53.3 %, yoghurt bebible +48.9 %, agua de 600 ml +36.8 %), y por categoría destacan galletas (+28.9 %) y refrescos (+13.9 %).»
- **Controles:** lista desplegable `categoria`, cuadro de entrada `producto`.
- **Fuente:** PROFECO QQP Mérida, mayo 2026. Promedio por producto y presentación, con 3 o más registros por canal.
- **Botón:** «Siguiente: la esquina →».

### Escena 4 · La esquina: «La tiendita no siempre es la más cara»

- **Fuente de datos:** `looker_08`.
- **Pregunta:** ¿Y LA TIENDITA DE LA COLONIA?
- **Bajada:** «Visitamos 5 tienditas de Mérida entre septiembre y octubre de 2026 y comparamos 4 productos equivalentes con los supermercados.»
- **Gráfica principal:** barras agrupadas con dimensión `producto` y métricas `mediana_tiendita_mxn` (oro) y `mediana_supermercado_mxn` (morado).
- **Anotaciones:**
  - Pan Bimbo: «+39.5 % en la tiendita».
  - Leche LALA: «−29.7 %: más barata en la tiendita».
- **Tabla:** `producto`, `diferencia_pct_tiendita_vs_super`, `registros_tiendita`, `registros_supermercado`.
- **Imagen:** `n6_david_vs_goliat.png` en lugar de las barras agrupadas, si prefieres la versión ilustrada.
- **¿Qué significa?** «El pan de marca sale más caro en la esquina; la leche, no. Es una muestra pequeña (2 a 5 precios por producto en tienditas): ilustra la experiencia de compra, no es un promedio de la ciudad.»
- **Fuente:** Bitácora propia 07-B (5 tienditas, 26 sep-1 oct 2026) y PROFECO QQP mayo 2026.
- **Botón:** «Siguiente: el sueldo →».

### Escena 5 · El sueldo: «Casi 28 días de salario mínimo para alimentar a un hogar»

- **Fuente de datos:** `looker_03`.
- **Pregunta:** ¿CUÁNTO TRABAJO CUESTA LA CANASTA?
- **Bajada:** «La canasta alimentaria urbana de CONEVAL subió 57.1 % entre enero de 2018 y marzo de 2025: de $1,514.91 a $2,379.47 por persona al mes.»
- **Gráfica principal:** serie temporal con dimensión `periodo` y métrica `lpei_canasta_alimentaria_urbana_mxn` en morado; agrega `lpi_alimentaria_mas_no_alimentaria_urbana_mxn` en gris.
- **Anotación:** en el último punto, «$2,379.47 por persona (mar 2025)».
- **Imágenes:** `n2_calendario_canasta.png` junto a la serie y `n3_tortillometro.png` junto al simulador.
- **Simulador** (bloque con fondo `#fdf3e3` y título «Prueba con tu sueldo»):
  - Control **Cuadro de entrada** ligado al parámetro `sueldo_mensual`, con la etiqueta «Tu sueldo mensual (MXN)».
  - Las tarjetas del simulador llevan un **filtro propio** `periodo` = marzo 2025, para que solo sumen el último mes.
  - Tarjeta `canasta_hogar_mxn` (con el filtro): «Canasta de un hogar de 3.27 personas» → $7,780.87.
  - Tarjeta `dias_de_trabajo_canasta` (con el filtro): «Días de trabajo para pagarla» → 27.9 con el valor predeterminado.
  - Tarjeta `pct_sueldo_canasta` (con el filtro): «Parte del sueldo que se va en comida».
  - Tarjeta `kilos_tortilla`: «Tu sueldo en kilos de tortilla».
- **¿Qué significa?** «Con el salario mínimo general de 2025 ($278.80 diarios), alimentar a un hogar típico de Mérida se lleva casi todo el mes de trabajo. Por eso pagar 19 % más en el súper pesa.»
- **Fuente:** CONEVAL, líneas de pobreza por ingresos (mar 2025); INEGI Censo 2020 (ocupantes por vivienda); CONASAMI, salario mínimo 2025; PROFECO (tortilla).
- **Botón:** «Siguiente: el territorio →».

### Escena 6 · El territorio: «El abasto popular se concentra en el Centro»

- **Fuentes de datos:** `looker_02` (mapa) y `looker_04` (AGEB).
- **Pregunta:** ¿DÓNDE ESTÁN LOS MERCADOS Y QUIÉN VIVE LEJOS DE ELLOS?
- **Bajada:** «Mérida tiene 15 mercados públicos registrados en el DENUE, con 1,661 establecimientos. Solo Lucas de Gálvez y San Benito suman 1,303.»
- **Gráfica principal:** mapa de burbujas de Google con ubicación `coordenadas_looker`, color `tipo_nodo` y tamaño `establecimientos_denue`.
- **Anotación:** junto al Centro, «Lucas de Gálvez: 817 establecimientos».
- **Segunda gráfica:** barras de `looker_04` con dimensión `rango_sin_afiliacion` y métrica recuento de `AGEB`.
- **Tarjetas** (`looker_04`): mediana de `pct_sin_afiliacion_salud` (21.6 %) y mediana de `pct_viviendas_con_internet` (73.3 %).
- **¿Qué significa?** «El abasto más barato está en el Centro. En las AGEB más vulnerables (12 pasan del 40 % de población sin afiliación a salud) llegar a él cuesta tiempo y transporte.»
- **Control:** lista desplegable `tipo_nodo`.
- **Fuente:** INEGI DENUE (edición 2026); INEGI Censo 2020 por AGEB; PROFECO.
- **Botón:** «Siguiente: la ciudad plana →».

### Escena 7 · La ciudad plana: «Mérida es plana: 16 m de desnivel en 17 km»

- **Fuente de datos:** `looker_06`.
- **Pregunta:** ¿EL TERRENO AYUDA O ESTORBA?
- **Bajada:** «Medimos la elevación real en mallas de 17 km por lado en Mérida y en cinco ciudades de montaña.»
- **Gráfica principal:** barras con dimensión `ciudad` y métrica `desnivel_m`, orden descendente. Mérida en morado y las demás en gris.
- **Anotación:** «Mérida: 16.2 m. San Cristóbal de las Casas: 1,413 m».
- **Imagen:** `n1_merida_plana_precios_no.png`, que conecta el relieve con la historia de precios.
- **Opcional:** Insertar → **Insertar URL** con el visor 3D publicado (`https://valnix140405.github.io/visual_modeling/data/visor_relieve_3d.html`). Comprueba que cargue dentro de Looker.
- **¿Qué significa?** «En Mérida caminar o pedalear al mercado no cuesta esfuerzo extra, pero el agua de lluvia no escurre sola. La distancia, no la pendiente, es la barrera para llegar al abasto barato.»
- **Fuente:** AWS Terrain Tiles (elevación, resolución aproximada de 30 m). No es LiDAR.
- **Botón:** «Siguiente: cierre →».

### Escena 8 · Cierre: «Dónde compras pesa tanto como cuánto ganas»

- **Fuente de datos:** `looker_07`.
- **Pregunta:** ¿QUÉ SIGNIFICA Y DE DÓNDE SALEN LOS DATOS?
- **Tres conclusiones** (cuadros de texto numerados):
  1. «El mismo producto cuesta, en mediana, 19 % más en el súper que en la Central de Abasto.»
  2. «La canasta de un hogar se lleva casi 28 días de salario mínimo.»
  3. «El abasto barato está concentrado en el Centro; la distancia es la barrera.»
- **Metodología** (cuadro de texto): «Solo se usan fuentes con dato real descargado de su origen. PROFECO cubre un mes (mayo 2026) y las sucursales que visitan sus inspectores; CONEVAL es nacional, no de Mérida; la bitácora propia tiene de 2 a 5 precios por producto. Abasto vs. súper = mediana por producto y presentación idénticos, súper / Central − 1. Conveniencia vs. súper = promedio con 3 o más registros por canal.»
- **Tabla:** `id`, `tema`, `institucion`, `registros`, `cobertura`, con el control `bloque`.
- **Enlaces:** repositorio (https://github.com/valnix140405/visual_modeling) y sitio con el recorrido interactivo (https://valnix140405.github.io/visual_modeling/).
- **Botón:** «Volver al inicio».

---

## 5. Revisión antes de entregar

- [ ] Cada escena tiene su ilustración y la ilustración dice lo mismo que el título.
- [ ] Recorre el informe en **Ver** sin tocar filtros: los 8 títulos, leídos seguidos, cuentan la historia.
- [ ] Las tarjetas coinciden con los textos: 139, 103, 74.1 %, +19.0 %, 93, 49, +1.3 %, $7,780.87, 27.9 días, 15 mercados, 1,661 establecimientos, 16.2 m.
- [ ] El simulador cambia al escribir otro sueldo; con 8,364 da 27.9 días.
- [ ] Cada página tiene su fuente y fecha de corte.
- [ ] Los colores significan lo mismo en todas las páginas: morado = súper o el protagonista, oro = el canal comparado.
- [ ] Los controles de filtro afectan solo a su página.
- [ ] El informe se comparte con permiso de lectura y se ve bien en una pantalla de 1366 px.
