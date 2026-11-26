// Escena 3 · Tienda de conveniencia contra súper («el impuesto a la flojera»).
// Los 7 productos con mayor sobreprecio en conveniencia, con la mediana de todos como contexto.
// Datos: ../datos/escena-3.csv (93 productos con 3 o más registros por canal).

import { d3, fmt, cargar, marco } from "./estilo.js";
import { pesas } from "./pesas.js";

export async function escena3(selector, ruta = "../datos/escena-3.csv") {
  const todas = (await cargar(ruta)).sort((a, b) => b.diferencia_pct - a.diferencia_pct);
  const mediana = d3.median(todas, (d) => d.diferencia_pct);
  const masCara = todas.filter((d) => d.diferencia_pct > 0).length;
  const top = todas.slice(0, 7);

  const titulo = `El impuesto a la flojera: hasta ${fmt.pctEntero(top[0].diferencia_pct)} por no caminar al súper`;
  const subtitulo =
    `Precio promedio en tiendas de conveniencia (OXXO, 7 Eleven, Dunosusa) contra supermercados, misma presentación. ` +
    `Los 7 productos con mayor diferencia. En los ${todas.length} productos comparables la conveniencia fue más cara en ` +
    `${masCara}, pero la diferencia mediana es de apenas ${fmt.pctSigno(mediana)}. Mérida.`;
  const fuente = `Fuente: ${top[0].fuente} (02-A y 06-B), promedios con 3 o más registros por canal · Corte: ${top[0].corte}`;

  const ancho = 760, alto = 470;
  const svg = marco(selector, { titulo, subtitulo, fuente, ancho, alto });
  pesas(svg, top, {
    ancho, alto, precioFoco: "precio_conveniencia_mxn", precioComp: "precio_super_mxn",
    nombre: "producto", detalle: (d) => recortarTexto(d.presentacion, 34),
    nombreFoco: "Tienda de conveniencia", nombreComp: "Supermercado",
  });
}

function recortarTexto(t, n) { return t.length > n ? `${t.slice(0, n - 1)}…` : t; }
