# Protocolo de Integración y Colaboración: Fuente B
### Guía Técnica para Jorge Ramiro Chay Koyoc (Responsable de Fuente B)

Este documento explica cómo está organizada la **Fuente B**, qué contiene cada una de sus 8 carpetas activas y las instrucciones para mantener los datos sincronizados en Git sin conflictos.

---

## 1. Dónde se encuentra tu trabajo: `data/fuente_b/`

Todo el contenido de la Fuente B vive de forma aislada dentro de la carpeta `data/fuente_b/`:

```text
data/fuente_b/
├── 01_inegi_saic/                 # Censos Económicos (Ingresos, personal y salarios en alimentos)
├── 02_datos_gob_sniim/            # Precios mayoristas Central de Abasto (Secretaría de Economía)
├── 03_conapo_marginacion/         # Índice de Marginación Urbana por colonia (CONAPO / SIEGY)
├── 04_tianguis_geoportal/         # Tianguis en vía pública autorizados (GeoJSON de comercio rodante)
├── 06_scraping_farmacias/         # Scraper de farmacias y tiendas de conveniencia (OXXO, Guadalajara)
├── 07_bitacora_tienditas/         # Levantamiento propio en 5 tienditas de la esquina de Mérida
├── 08_lidar_cem_mde/              # Malla de elevación CEM 3.0 de INEGI (Modelo Digital de Elevación)
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
   El script confirmará `22 de 22 datasets listos y verificados en disco`.

---

## 3. Comandos rápidos de Git para subir avances

```bash
git pull origin main
git add data/fuente_b/
git commit -m "feat(fuente_b): actualizacion de datasets de la Fuente B"
git push origin main
```
