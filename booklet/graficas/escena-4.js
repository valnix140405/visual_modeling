// Escena 4 · Tiendita contra súper («David contra Goliat»).
// Los productos equivalentes de la bitácora propia contra la mediana del súper.
// Es una muestra chica: el número de precios va escrito en cada fila.
// Datos: ../datos/escena-4.csv.

import { cargar, marco, fmt, color } from "./estilo.js";
import { pesas } from "./pesas.js";

export async function escena4(selector, ruta = "../datos/escena-4.csv") {
  const filas = (await cargar(ruta)).sort((a, b) => a.diferencia_pct - b.diferencia_pct);
  const gana = filas.filter((d) => d.diferencia_pct < 0);
  const quien = gana.length === 1
    ? `en la ${gana[0].producto.split(" ")[0].toLowerCase()} (${fmt.pctSigno(gana[0].diferencia_pct)})`
    : `en ${gana.length} de ${filas.length} productos`;
  const titulo = `David contra Goliat: la tiendita solo le gana al súper ${quien}`;
  const minN = Math.min(...filas.map((d) => d.registros_tiendita));
  const maxN = Math.max(...filas.map((d) => d.registros_tiendita));
  const subtitulo =
    `Mediana del precio en ${filas[0].numero_tienditas} tienditas de Mérida (bitácora propia) contra la mediana en supermercados (PROFECO), ` +
    `en ${filas.length} productos equivalentes. Muestra chica: de ${minN} a ${maxN} precios por producto en tienditas; ` +
    `sirve para ilustrar, no para generalizar.`;
  const fuente = `Fuente: ${filas[0].fuente} · Corte: ${filas[0].corte}`;

  const ancho = 760, alto = 340;
  const svg = marco(selector, { titulo, subtitulo, fuente, ancho, alto });
  pesas(svg, filas, {
    ancho, alto, precioFoco: "precio_tiendita_mxn", precioComp: "precio_super_mxn", nombre: "producto",
    detalle: (d) => `${d.registros_tiendita} precios en tienditas · ${d.registros_super} en súper`,
    nombreFoco: `Tiendita (${filas[0].numero_tienditas} tiendas)`, nombreComp: "Supermercado",
  });
  svg.append("text").attr("x", 8).attr("y", alto - 8).attr("text-anchor", "start").attr("font-size", 11.5)
    .attr("font-style", "italic").style("fill", color.oroOscuro).text("Muestra chica: tómese como ilustración");
}
