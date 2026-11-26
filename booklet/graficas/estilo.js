// Booklet · Equipo 2 · estilo común de las escenas (D3 v7, versión fija).
// Paleta y formatos del Plan del Booklet (sección 3): morado = foco, oro = comparación,
// oro oscuro = anotaciones, gris = contexto. Números a la mexicana.
// Ninguna cifra vive aquí: todas se leen de ../datos/*.csv.

import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7.9.0/+esm";

export { d3 };

export const color = {
  morado: "#600d8b",
  oro: "#ed9f22",
  oroOscuro: "#b45309",
  gris: "#9ca3af",
  grisTexto: "#555555",
  tinta: "#0d0d0d",
  borde: "#e5e7eb",
  blanco: "#ffffff",
};

const mx = d3.formatLocale({ decimal: ".", thousands: ",", grouping: [3], currency: ["$", ""] });

export const fmt = {
  num: mx.format(",.0f"),
  dec: mx.format(",.1f"),
  dec2: mx.format(",.2f"),
  pesos: mx.format("$,.2f"),
  pct: (v) => `${mx.format(".1f")(v)} %`,
  pctSigno: (v) => `${v < 0 ? "−" : "+"}${mx.format(".1f")(Math.abs(v))} %`,
  pctEntero: (v) => `${v < 0 ? "−" : "+"}${mx.format(".0f")(Math.abs(v))} %`,
};

// Carga un CSV relativo a la página de la escena (../datos/archivo.csv).
export async function cargar(ruta) {
  const filas = await d3.csv(new URL(ruta, document.baseURI), d3.autoType);
  if (!filas.length) throw new Error(`${ruta} está vacío`);
  return filas;
}

// Marco común: título-hallazgo, subtítulo, SVG con viewBox y pie con fuente y corte.
export function marco(selector, { titulo, subtitulo, fuente, ancho = 760, alto = 420 }) {
  const raiz = d3.select(selector).html("");
  raiz.append("p").attr("class", "grafica-titulo").text(titulo);
  raiz.append("p").attr("class", "grafica-subtitulo").text(subtitulo);
  const svg = raiz.append("svg")
    .attr("viewBox", [0, 0, ancho, alto])
    .attr("role", "img")
    .attr("aria-label", `${titulo}. ${subtitulo}`);
  raiz.append("p").attr("class", "grafica-fuente").text(fuente);
  return svg;
}

export function mostrarError(selector, error) {
  d3.select(selector).html("").append("p").attr("class", "grafica-error")
    .text(`No se pudo dibujar esta escena: ${error.message}`);
  console.error(error);
}

// Señal para capturas e impresión: todas las escenas de la página terminaron.
export async function listo(promesas) {
  await Promise.allSettled(promesas);
  if (document.fonts) await document.fonts.ready;
  document.body.dataset.listo = "si";
}
