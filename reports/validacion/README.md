# Validación del 2026-11-24

| Reporte | Qué revisa | Resultado |
|---|---|---|
| [01_auditoria_cifras_dashboard.md](01_auditoria_cifras_dashboard.md) | Cada cifra de `index.html`, `looker_studio_borrador.html` y los visores, recalculada desde `data/` | 92 cifras: 82 coincidían, 9 se corrigieron y 1 dato externo (salario mínimo) se verificó con CONASAMI |
| [02_contraste_fuentes_oficiales.md](02_contraste_fuentes_oficiales.md) | Datos del repo contra la descarga oficial | DENUE 100 %, ENOE idéntica (SHA-256), OSM 20/20. PROFECO de mayo no verificable (archivo oficial ilegible después de marzo), con plausibilidad alta. DICONSA y SENASICA no verificables (403) |
| [03_comparacion_companeros.md](03_comparacion_companeros.md) | Sitio final frente a los de Russel, Rivaldo y la documentación de Lorena | Único sitio cuyas cifras salen de datos reales; pendientes de interacción y versión impresa |
