# Reporte ejecutivo: análisis de las 22 fuentes

## *Del Mundo a la Esquina: ¿Cuánto Cuesta Comer?*

**Institución:** Universidad Politécnica de Yucatán (UPY)  
**Equipo:** Valeria Nicol Hernández León (Fuente A) · Jorge Ramiro Chay Koyoc (Fuente B) · Isaac René Andrade Sánchez (Fuente C)  
**Alcance:** el análisis usa solo las 16 fuentes con datos reales descargados de su origen (PROFECO, INEGI, CONEVAL, DICONSA, SENASICA, OpenStreetMap, elevación AWS Terrain Tiles y la bitácora propia de tienditas). Detalle en [`FUENTES_DE_DATOS.md`](FUENTES_DE_DATOS.md).

El detalle y la procedencia de cada cifra están en [`ANALISIS_PROFUNDO_22_FUENTES.md`](ANALISIS_PROFUNDO_22_FUENTES.md) y en [`reports/metricas_analisis.json`](reports/metricas_analisis.json).

## Cifras clave

| Pregunta | Respuesta | Fuente |
|---|---|---|
| ¿Cuánto cuesta la canasta alimentaria urbana? | $2,379.47 por persona al mes (mar 2025), +57.1 % desde ene 2018 | CONEVAL |
| ¿Y la línea de pobreza por ingresos urbana? | $4,680.15 por persona al mes (mar 2025) | CONEVAL |
| ¿Cuánto más caro es el supermercado que la Central de Abasto? | Más caro en 74.1 % de 139 productos comparables; diferencia mediana +19.0 % | PROFECO QQP mayo 2026 |
| ¿Cómo es el comercio de alimentos en Mérida? | 7,520 establecimientos; 92.5 % con 0 a 5 personas | INEGI DENUE |
| ¿Quién vende más? | 3,113 abarrotes: $1,291.7 mdp; 78 supermercados: $15,338.6 mdp (año de referencia 2018) | INEGI Censos Económicos 2019 |
| ¿Cuántos mercados públicos hay? | 15 en el DENUE, con 1,661 establecimientos; Lucas de Gálvez tiene 817 | INEGI DENUE |
| ¿Qué tan desigual es la ciudad? | Sin afiliación a salud: 21.6 % mediana por AGEB, 31.0 % en el percentil 90; 12 AGEB arriba de 40 % | INEGI Censo 2020 |
| ¿Tiendita o supermercado? | Pan Bimbo +39.5 % y frijol +9.6 % en tiendita; leche LALA −29.7 % (muestras de 2 a 5 precios, solo orientativo) | Bitácora 07-B y PROFECO |
| ¿Qué tan plano es Mérida? | 9.6 m de elevación media y 16.2 m de desnivel en 17 km | AWS Terrain Tiles |

## Figuras

| Figura | Qué muestra |
|---|---|
| [`01_precios_canasta_por_cadena_profeco.png`](reports/figuras/01_precios_canasta_por_cadena_profeco.png) | Mediana de precio por cadena para 6 productos, con la misma presentación en todas |
| [`02_central_abasto_vs_supermercados_profeco.png`](reports/figuras/02_central_abasto_vs_supermercados_profeco.png) | Los 15 productos por kilo con mayor diferencia entre supermercado y Central de Abasto |
| [`03_lineas_pobreza_coneval_2018_2025.png`](reports/figuras/03_lineas_pobreza_coneval_2018_2025.png) | Evolución mensual de las líneas de pobreza urbanas |
| [`04_tienditas_vs_supermercados.png`](reports/figuras/04_tienditas_vs_supermercados.png) | Mediana de 4 productos en tienditas vs. supermercados, con número de observaciones |
| [`05_indicadores_ageb_censo2020_merida.png`](reports/figuras/05_indicadores_ageb_censo2020_merida.png) | Distribución por AGEB de la población sin afiliación a salud y de las viviendas con internet |
| [`06_relieve_merida_vs_ciudades_montana.png`](reports/figuras/06_relieve_merida_vs_ciudades_montana.png) | Elevación de Mérida frente a cinco ciudades de montaña |
