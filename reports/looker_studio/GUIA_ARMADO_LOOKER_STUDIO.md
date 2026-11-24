# Guía de armado en Looker Studio

**Proyecto:** Del Mundo a la Esquina: ¿Cuánto Cuesta Comer? (UPY)  
**Entregable:** informe de Looker Studio con 8 páginas. Usa solo las 16 fuentes con datos reales.

Todas las cifras de los textos de esta guía salen de los archivos del repositorio y se auditaron el 2026-11-24 (ver [`reports/validacion/`](../validacion/)). Si regeneras las tablas, revisa que los textos sigan coincidiendo con las tarjetas de KPI.

## 1. Tablas (fuentes de datos de Looker)

Se regeneran con:

```bash
python scripts/generar_datos_web.py           # looker_05
python scripts/generar_tablas_looker_studio.py # looker_01 a 04, 06 y 07
```

| Archivo | Filas | Contenido |
|---|---:|---|
| [`looker_01_precios_multicanal.csv`](looker_01_precios_multicanal.csv) | 26,281 | Un precio por fila: `canal` (Supermercado, Farmacia / Conveniencia, Central de Abasto, Mercado público, Tiendita de esquina), establecimiento, producto, presentación, marca, `precio_mxn`. PROFECO mayo 2026 + bitácora propia |
| [`looker_02_territorio_geo.csv`](looker_02_territorio_geo.csv) | 65 | 15 mercados públicos (DENUE) y establecimientos PROFECO con `coordenadas_looker` (`lat,lon`) |
| [`looker_03_lineas_pobreza_coneval.csv`](looker_03_lineas_pobreza_coneval.csv) | 87 | Líneas de pobreza CONEVAL mensuales, 2018-01 a 2025-03 |
| [`looker_04_ageb_censo2020_merida.csv`](looker_04_ageb_censo2020_merida.csv) | 520 | AGEB urbanas habitadas de Mérida (Censo 2020) con porcentajes ya calculados |
| [`looker_05_comparables_por_canal.csv`](looker_05_comparables_por_canal.csv) | 232 | Pares de producto y presentación idénticos: 139 Central de Abasto vs. súper y 93 conveniencia vs. súper, con `diferencia_pct` y `resultado` |
| [`looker_06_relieve_ciudades.csv`](looker_06_relieve_ciudades.csv) | 2,400 | Elevación real en mallas de 20 × 20 puntos para Mérida y 5 ciudades de montaña |
| [`looker_07_catalogo_fuentes.csv`](looker_07_catalogo_fuentes.csv) | 16 | Catálogo de las 16 fuentes usadas, con institución, archivo, registros y cobertura |

### Importar

1. En [lookerstudio.google.com](https://lookerstudio.google.com/) crea un **Informe vacío**.
2. Agrega cada CSV con **Agregar datos → Subir archivo**. Si `looker_01` (5.5 MB) da problemas, súbelo a Google Sheets y conéctalo desde ahí.
3. Ajusta los tipos de campo en cada fuente:
   - `looker_02.coordenadas_looker` → **Geo → Latitud, longitud**.
   - Los campos `precio_*`, `diferencia_pct` y `pct_*` → **Número**. `precio_*` en formato **Moneda (MXN)**.
   - `looker_03.periodo` → **Fecha → Año y mes**.
   - `looker_04.AGEB` → **Texto**, para no perder los ceros a la izquierda.
4. **Tema:** primario `#600d8b`, secundario `#ed9f22`, fondo `#ffffff`. **Navegación:** pestañas a la izquierda (Archivo → Configuración del informe → Navegación).

### Campos calculados

Créalos en la fuente indicada (Recurso → Administrar fuentes de datos → Editar → Agregar campo):

| Fuente | Nombre | Fórmula |
|---|---|---|
| looker_05 | `pct_mas_caro_super` | `SUM(CASE WHEN diferencia_pct > 0 THEN 1 ELSE 0 END) / COUNT(producto)` (formato porcentaje) |
| looker_05 | `mediana_diferencia` | `MEDIAN(diferencia_pct)` |
| looker_04 | `rango_sin_afiliacion` | `CASE WHEN pct_sin_afiliacion_salud < 15 THEN "0-15 %" WHEN pct_sin_afiliacion_salud < 20 THEN "15-20 %" WHEN pct_sin_afiliacion_salud < 25 THEN "20-25 %" WHEN pct_sin_afiliacion_salud < 30 THEN "25-30 %" WHEN pct_sin_afiliacion_salud < 40 THEN "30-40 %" ELSE "40 % o más" END` |
| looker_06 | `desnivel_m` | `MAX(elevacion_m_snm) - MIN(elevacion_m_snm)` |

## 2. Recorrido guiado

Looker Studio no tiene recorridos automáticos. El recorrido se arma así:

- Cada página es un **paso**, con un cuadro de texto arriba titulado «Paso N de 8», que cuenta el hallazgo en 2 o 3 líneas.
- Abajo a la derecha de cada página va un **botón** (Insertar → Botón → Acción: navegación a página) con el texto «Siguiente: …» que lleva a la página que sigue.
- Los textos de cada página están abajo, listos para copiar.

## 3. Páginas

### Página 1. La pregunta (portada)

- **Texto:** «Paso 1 de 8 · En Mérida, lo que pagas por comer depende de dónde compras. Cruzamos datos oficiales de PROFECO, INEGI y CONEVAL con una bitácora propia de cinco tienditas para medirlo.»
- **4 tarjetas de KPI:**
  - Registros de precios: `looker_01`, recuento de registros → 26,281.
  - Productos comparables Abasto–súper: `looker_05` con filtro `canal_comparado = Central de Abasto`, recuento → 139.
  - Mercados públicos: `looker_02` con filtro `tipo_nodo` = Mercado público (DENUE), recuento → 15.
  - Fuentes con dato real: `looker_07`, recuento → 16.
- **Botón:** «Siguiente: Abasto vs. súper».

### Página 2. Central de Abasto vs. supermercado (`looker_05`)

- **Filtro de página:** `canal_comparado` = Central de Abasto.
- **Texto:** «Paso 2 de 8 · En 139 productos con la misma presentación, el súper fue más caro en 103 (74.1 %). La diferencia mediana es +19.0 %. Ambos son precios al público, no de mayoreo.»
- **Tarjetas:** recuento de `producto`, `pct_mas_caro_super`, `mediana_diferencia`.
- **Gráfico de barras horizontal:** dimensión `producto`, métrica `diferencia_pct`, orden descendente, 15 barras.
- **Tabla:** `producto`, `presentacion`, `categoria`, `precio_canal_comparado_mxn`, `precio_supermercado_mxn`, `diferencia_pct` (con mapa de calor).
- **Controles de filtro:**
  - Lista desplegable `categoria`.
  - Lista desplegable `resultado`.
  - Cuadro de entrada `producto` (búsqueda).

### Página 3. Conveniencia vs. supermercado (`looker_05`)

- **Filtro de página:** `canal_comparado` = Conveniencia.
- **Texto:** «Paso 3 de 8 · Entre OXXO, 7 Eleven y Dunosusa y los supermercados hay 93 productos comparables. La conveniencia fue más cara en 49, pero la diferencia mediana es de apenas +1.3 %: la prisa se paga en bebidas y botanas, no en todo.»
- **Gráfico y controles:** los mismos que en la página 2. Agrega un gráfico de barras de `categoria` con métrica `mediana_diferencia`.

### Página 4. Precios por canal (`looker_01`)

- **Texto:** «Paso 4 de 8 · Mismo producto, cinco lugares de compra. La bitácora de tienditas tiene pocos precios (22), así que úsala como ilustración, no como promedio.»
- **Tabla dinámica:** filas `producto`, columnas `canal`, métrica `precio_mxn` con agregación **Mediana**.
- **Controles:**
  - Lista desplegable `canal`.
  - Lista desplegable `producto` (búsqueda activada).
  - Lista desplegable `presentacion`.
  - Lista desplegable `fuente`.

### Página 5. Cuánto sueldo se come la canasta (`looker_03`)

- **Texto:** «Paso 5 de 8 · La canasta alimentaria urbana de CONEVAL pasó de $1,514.91 (ene 2018) a $2,379.47 por persona (mar 2025), +57.1 %. Para un hogar típico de Mérida (3.27 ocupantes, Censo 2020) son $7,780.87 al mes: 27.9 días de salario mínimo general 2025 ($278.80 diarios, CONASAMI).»
- **Serie temporal:** dimensión `periodo`; métricas `lpei_canasta_alimentaria_urbana_mxn`, `lpei_canasta_alimentaria_rural_mxn` y `lpi_alimentaria_mas_no_alimentaria_urbana_mxn`.
- **Control:** periodo (rango de fechas).
- **Tarjeta:** último valor de `lpei_canasta_alimentaria_urbana_mxn`.

### Página 6. Territorio y desigualdad (`looker_02` y `looker_04`)

- **Texto:** «Paso 6 de 8 · Mérida tiene 15 mercados públicos registrados en el DENUE, con 1,661 establecimientos; Lucas de Gálvez concentra 817. Por AGEB, la población sin afiliación a salud va de 16.6 % (percentil 10) a 31.0 % (percentil 90), y 12 AGEB pasan del 40 %.»
- **Mapa de burbujas de Google** (`looker_02`): ubicación `coordenadas_looker`, color `tipo_nodo`, tamaño `establecimientos_denue`.
- **Barras** (`looker_04`): dimensión `rango_sin_afiliacion`, métrica recuento de `AGEB`.
- **Tarjetas** (`looker_04`): mediana de `pct_sin_afiliacion_salud` (21.6 %) y mediana de `pct_viviendas_con_internet` (73.3 %).
- **Control:** lista desplegable `tipo_nodo`.

### Página 7. Relieve (`looker_06`)

- **Texto:** «Paso 7 de 8 · En 17 km, Mérida tiene 16.2 m de desnivel; San Cristóbal de las Casas, 1,413 m. Una ciudad plana se camina sin esfuerzo, pero el agua de lluvia no escurre sola. Datos de elevación real (AWS Terrain Tiles), no LiDAR.»
- **Barras:** dimensión `ciudad`, métrica `desnivel_m`.
- **Tabla:** `ciudad`, elevación promedio, mínima y máxima.
- **Opcional:** componente **Insertar → Insertar URL** con el visor 3D publicado (`https://valnix140405.github.io/visual_modeling/data/visor_lidar_unificado.html`). Comprueba que cargue dentro de Looker.

### Página 8. Metodología y fuentes (`looker_07`)

- **Texto:** «Paso 8 de 8 · Solo se usan fuentes con dato real descargado de su origen. PROFECO cubre un mes (mayo 2026); CONEVAL es nacional, no de Mérida; la bitácora propia tiene de 2 a 5 precios por producto. Fórmulas: Abasto vs. súper = mediana por producto y presentación idénticos, súper / Central − 1; conveniencia vs. súper = promedio con 3 o más registros por canal.»
- **Tabla:** `id`, `tema`, `institucion`, `registros`, `cobertura`.
- **Control:** lista desplegable `bloque`.
- **Enlace al repositorio:** https://github.com/valnix140405/visual_modeling

## 4. Revisión antes de entregar

- [ ] Las tarjetas de KPI muestran los mismos valores que los textos (139, 103, 74.1 %, +19.0 %, 93, 49, +1.3 %, 15, 1,661).
- [ ] Cada gráfico dice su fuente y fecha de corte.
- [ ] Los controles de filtro afectan solo a los gráficos de su página.
- [ ] El informe se ve bien en **Ver → Modo de visualización** y se comparte con permiso de lectura.
