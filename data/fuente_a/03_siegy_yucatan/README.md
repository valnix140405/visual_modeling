# 03-A · Ingreso y canasta: CONEVAL + Censo 2020 (en sustitución de SIEGY)

**Responsable:** Valeria Hernández  
**Última revisión de procedencia:** 2026-11-24

Indicadores de poder adquisitivo. El archivo anterior atribuido a SIEGY no citaba tabla ni documento de origen y no pudo verificarse, por lo que se sustituyó por fuentes oficiales descargables.

| Archivo | Tamaño | URL de origen | Fecha de extracción | Licencia | Estado | Observaciones |
|---|---|---|---|---|---|---|
| [`coneval_lineas_pobreza_2018_2025.csv`](coneval_lineas_pobreza_2018_2025.csv) | 87 filas | https://www.coneval.org.mx/Medicion/Documents/Lineas_de_Pobreza_por_Ingresos/Lineas_de_Pobreza_por_Ingresos.zip | 2026-11-24 | Verificar términos de uso en coneval.org.mx | Completo | Valor mensual por persona, nivel nacional urbano y rural. El archivo publicado llega a marzo de 2025. |
| [`inegi_lineas_pobreza_2025_2026.csv`](inegi_lineas_pobreza_2025_2026.csv) | 16 filas | Boletines mensuales «Líneas de Pobreza» de INEGI: https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/lp/ (un PDF por mes; la URL de cada mes está en la columna `url_boletin`) | 2026-11-26 | [Términos de Libre Uso de la Información del INEGI](https://www.inegi.org.mx/inegi/terminos.html) | Completo | Julio 2025 a octubre 2026 (abril a junio de 2025 sin boletín publicado). Desde 2025 INEGI publica estas líneas en lugar de CONEVAL. La escena 1 del booklet usa el último mes. |
| [`censo2020_totales_municipio_merida.csv`](censo2020_totales_municipio_merida.csv) | 1 filas | https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/ageb_manzana/ageb_mza_urbana_31_cpv2020_csv.zip | 2026-11-24 | [Términos de Libre Uso de la Información del INEGI](https://www.inegi.org.mx/inegi/terminos.html) | Completo | Fila del total municipal de Mérida (población, PEA, afiliación a salud y vivienda). |
| [`explorar_siegy.py`](explorar_siegy.py) | — | — | — | — | Script | Imprime un resumen de ambos archivos. |

## Pendientes y cambios

- Pendiente: obtener indicadores propios de SIEGY (https://siegy.yucatan.gob.mx) con tabla y fecha citables.
- Se eliminó `indicadores_socioeconomicos_merida_siegy.csv` (7 filas sin origen verificable).

**Estados:** Completo = el recurso descrito está en el repositorio. Revisar = hay un problema por confirmar. Prototipo = material de diseño elaborado por el equipo. Pendiente = no hay dato real todavía.
