# Protocolo de Integración y Colaboración: Fuente B
### Guía Técnica para Jorge Ramiro Chay Koyoc (Responsable de Fuente B)

Este documento explica cómo está organizada la **Fuente B**, qué contiene cada una de sus 8 carpetas activas y las instrucciones para mantener los datos sincronizados en Git sin conflictos.

---

## 1. Dónde se encuentra tu trabajo: `data/fuente_b/`

Todo el contenido de la Fuente B vive de forma aislada dentro de la carpeta `data/fuente_b/`:

```text
data/fuente_b/
├── 01_inegi_saic/                 # Censos Económicos (Ingresos, personal y salarios en alimentos)
├── 02_datos_gob_sniim/            # Precios PROFECO en la Central de Abasto (falta mayoreo SNIIM)
├── 03_conapo_marginacion/         # Indicadores del Censo 2020 por AGEB (falta índice CONAPO)
├── 04_tianguis_geoportal/         # PENDIENTE: tianguis (Geoportal no accesible)
├── 06_scraping_farmacias/         # Precios PROFECO en farmacias y conveniencia
├── 07_bitacora_tienditas/         # Levantamiento propio en 5 tienditas de la esquina de Mérida
├── 08_lidar_cem_mde/              # Malla de elevación real del Centro (AWS Terrain Tiles)
└── 09_ar_modelos_3d/              # Catálogo y especificaciones de assets 3D glTF/GLB para AR
```

---

## 2. Reglas de Colaboración en Git sin Conflictos

1. **Trabaja dentro de `data/fuente_b/`:**  
   Al mantener tus cambios dentro de tu carpeta asignada, Git permite hacer `pull` y `push` sin conflictos de fusión con `fuente_a` o `fuente_c`.
2. **Conserva los nombres de columnas estándar:**  
   Mantén los encabezados de los archivos CSV (`folio_auditoria`, `colonia`, `nombre_tiendita`, `producto_auditado`, `precio_observado_mxn`, etc.) para que los scripts analíticos lean los datos automáticamente.
3. **Valida antes de subir:**  
   Antes de hacer `git push`, corre en la terminal:
   ```bash
   python scripts/verificar_datasets.py
   ```
   El script lista qué fuentes están listas y cuáles siguen pendientes.
4. **Documenta la procedencia:** al agregar un archivo, completa su fila en el `README.md` de la carpeta (URL, fecha de extracción, licencia, estado).

---

## 3. Comandos rápidos de Git para subir avances

```bash
git pull origin main  # trabaja en una rama propia si el cambio es grande
git add data/fuente_b/
git commit -m "feat(fuente_b): actualizacion de datasets de la Fuente B"
git push origin main
```
