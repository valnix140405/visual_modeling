# El salario mínimo como unidad común del booklet

El Plan del Booklet (V4) dice que del Equipo 2 se rescata **«el salario mínimo como unidad que pueden usar los demás capítulos»**. Esta nota explica cómo usarla para que todos los capítulos midan con la misma regla.

## La idea

Un monto en pesos dice poco; en **días de trabajo** se entiende de inmediato. «La renta cuesta $4,500» se lee distinto que «la renta se lleva 16 días de salario mínimo».

```text
días de salario mínimo = monto en pesos ÷ salario mínimo diario
```

## Los datos

Archivo: [`datos/unidad-salario-minimo.csv`](datos/unidad-salario-minimo.csv)

| anio | salario_minimo_diario_mxn | salario_minimo_mensual_mxn | fuente |
|---:|---:|---:|---|
| 2025 | 278.80 | 8,364.00 | CONASAMI, Tabla de Salarios Mínimos 2025 |
| 2026 | 315.04 | 9,451.20 | CONASAMI, Tabla de Salarios Mínimos 2026 |

- Es el salario mínimo **general**, el que aplica en Yucatán; la zona libre de la frontera norte tiene otro valor.
- El mes se cuenta de **30 días**, igual que en nuestro capítulo.

Enlace directo al CSV, para leerlo desde otro repositorio:  
`https://raw.githubusercontent.com/valnix140405/visual_modeling/main/booklet/datos/unidad-salario-minimo.csv`

## Reglas para usarlo bien

1. **Empata el año.** Usa el salario del mismo año que tu dato: un precio de 2025 se divide entre $278.80 y uno de 2026 entre $315.04. Si tu dato es de otro año, dilo en el subtítulo.
2. **Pesos nominales.** El salario está en pesos corrientes de su año; no lo mezcles con montos deflactados sin decirlo.
3. **Es una unidad, no el ingreso real.** Muchos hogares ganan más que el mínimo y otros menos. Escríbelo en «Lo que estos datos no dicen» la primera vez que lo uses.
4. **Copia el CSV a tu carpeta.** El plan pide que cada cifra salga de un archivo de **tu** repositorio: copia este CSV a tu `booklet/datos/` y cítalo en tu `FUENTES.md` como «CONASAMI vía Equipo 2».

## En D3

```js
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7.9.0/+esm";

const salarios = await d3.csv("datos/unidad-salario-minimo.csv", d3.autoType);
const diario = salarios.find((d) => d.anio === 2026).salario_minimo_diario_mxn;

const dias = (pesos) => pesos / diario;              // días de salario mínimo
const texto = (pesos) => `${d3.format(",.1f")(dias(pesos))} días de salario mínimo`;
```

## Ejemplo del Equipo 2

Un mes de canasta alimentaria urbana para un hogar de Mérida (3.27 personas) cuesta $7,780.87 (CONEVAL, marzo 2025). Dividido entre $278.80 da **27.9 días** de salario mínimo 2025 (`datos/escena-1.csv`).
