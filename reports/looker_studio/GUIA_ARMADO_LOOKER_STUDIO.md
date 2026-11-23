# Guía de Armado y Borrador Ejecutivo en Google Looker Studio (Data Studio)
## Proyecto: "Del Mundo a la Esquina: ¿Cuánto Cuesta Comer?" (UPY)

Para que puedas presentar tanto el **Borrador Web Interactivo** como conectarlo en 2 minutos a **Google Looker Studio (`lookerstudio.google.com`)**, hemos preparado este paquete ejecutivo con las **22 fuentes activas** consolidadas.

---

## 1. Vista Previa Interactiva Lista en el Repositorio
Puedes abrir directamente en el navegador el tablero estilo Looker Studio:
* [**`looker_studio_borrador.html`**](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/looker_studio_borrador.html)
  * Incluye **3 páginas de informe**, filtros cruzados por **Zona de Mérida** y **Producto de Tiendita (07-B)**, tarjetas Scorecard, gráficos dinámicos y mapa SIG con las 5 tienditas reales auditadas y los mercados municipales.

---

## 2. Las 3 Tablas Maestras Planas (Flat CSV) para Subir a Looker Studio
Google Looker Studio requiere tablas planas normalizadas en CSV o Google Sheets. El script [`scripts/generar_tablas_looker_studio.py`](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/scripts/generar_tablas_looker_studio.py) ya generó las 3 fuentes listas en esta carpeta:

1. [**`looker_01_comparativa_precios_multicanal.csv`**](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/reports/looker_studio/looker_01_comparativa_precios_multicanal.csv) (`72 registros normalizados`):
   * Une **Bitácora de 5 Tienditas (`07-B`)**, **Central de Abasto SNIIM (`02-B`)**, **Supermercados (`06-A`)** y **Farmacias/OXXO (`06-B`)**.
   * *Dimensiones Looker:* `canal_comercial`, `zona_merida`, `colonia`, `establecimiento`, `producto`.
   * *Métrica Looker:* `precio_mxn` (Promedio, Mínimo, Máximo).
2. [**`looker_02_territorio_mercados_tienditas_geo.csv`**](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/reports/looker_studio/looker_02_territorio_mercados_tienditas_geo.csv) (`19 nodos geográficos`):
   * Une los **8 Mercados Municipales (`04-A`)**, **6 Tianguis (`04-B`)** y las **5 Tienditas Auditadas (`07-B`)**.
   * *Campo Geoespacial Looker:* `coordenadas_looker` (formato `lat,lon` directo para el widget de Google Maps de Looker Studio).
   * *Dimensión de Color:* `tipo_nodo`.
   * *Tamaño de Burbuja:* `afluencia_diaria` o `puestos_o_locales`.
3. [**`looker_03_salarios_esfuerzo_laboral_merida.csv`**](file:///c:/Users/nixle/Downloads/visual_folder/UPY/victorrr/reports/looker_studio/looker_03_salarios_esfuerzo_laboral_merida.csv) (`7 cortes metropolitanos`):
   * Une **SIEGY / CONEVAL (`03-A`)** con salarios diarios, informalidad, pobreza laboral y días de trabajo necesarios para pagar la canasta básica.

---

## 3. Pasos para Importar en `lookerstudio.google.com`

1. Entra a [lookerstudio.google.com](https://lookerstudio.google.com/) y haz clic en **Informe vacío (Blank Report)**.
2. Selecciona el conector **Subir archivo (File Upload)** o súbelos primero a una hoja de **Google Sheets**.
3. Carga los 3 archivos CSV ubicados en `reports/looker_studio/`.
4. En **Tema y diseño (Theme and layout)**, aplica la paleta oficial:
   * Color primario: `#600d8b` (Púrpura UPY)
   * Color secundario: `#ed9f22` (Oro)
   * Fondo de página: `#ffffff` (Blanco)
   * Texto: `#0d0d0d` (Carbón)
