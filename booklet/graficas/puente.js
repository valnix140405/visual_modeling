// Gráfica puente al Acto 4 · «Mérida es plana».
// Desnivel (elevación máxima − mínima) en una malla de unos 17 km por lado para Mérida
// y 5 ciudades de montaña. Mérida en morado (foco); las demás en gris (contexto).
// Datos: ../datos/puente-relieve.csv.

import { d3, color, fmt, cargar, marco } from "./estilo.js";

export async function puente(selector, ruta = "../datos/puente-relieve.csv") {
  const filas = (await cargar(ruta)).sort((a, b) => a.desnivel_m - b.desnivel_m);
  const merida = filas.find((d) => d.ciudad === "Mérida");
  const mayor = filas[filas.length - 1];

  const titulo = `Mérida es plana: ${fmt.dec(merida.desnivel_m)} m de desnivel en 17 km, contra ` +
    `${fmt.num(mayor.desnivel_m)} m en ${mayor.ciudad}`;
  const subtitulo = `Diferencia entre el punto más alto y el más bajo de una malla de 20 × 20 puntos (unos 17 km por lado) ` +
    `en cada ciudad, en metros. Aquí caminar al mercado no cuesta esfuerzo, pero el agua de lluvia no tiene a dónde escurrir.`;
  const fuente = `Fuente: ${merida.fuente}. Es elevación de un modelo de terreno (~30 m), no LiDAR · Corte: ${merida.corte}`;

  const ancho = 760, fila = 40, m = { arriba: 10, derecha: 120, abajo: 30, izquierda: 210 };
  const alto = m.arriba + filas.length * fila + m.abajo;
  const svg = marco(selector, { titulo, subtitulo, fuente, ancho, alto });
  const x = d3.scaleLinear([0, d3.max(filas, (d) => d.desnivel_m)], [m.izquierda, ancho - m.derecha]).nice();
  const y = (i) => m.arriba + i * fila;

  svg.append("g").selectAll("line").data(x.ticks(5)).join("line")
    .attr("x1", x).attr("x2", x).attr("y1", m.arriba).attr("y2", alto - m.abajo).attr("stroke", color.borde);
  svg.append("g").attr("transform", `translate(0,${alto - m.abajo})`)
    .call(d3.axisBottom(x).ticks(5).tickFormat((v) => `${fmt.num(v)} m`).tickSizeOuter(0))
    .call((g) => g.select(".domain").remove())
    .call((g) => g.selectAll("text").attr("font-size", 12).style("fill", color.grisTexto));

  const g = svg.append("g").selectAll("g").data(filas).join("g").attr("transform", (_, i) => `translate(0,${y(i)})`);
  g.append("rect").attr("x", m.izquierda).attr("y", 7).attr("height", fila - 14).attr("rx", 3)
    .attr("width", (d) => Math.max(2, x(d.desnivel_m) - x(0)))
    .attr("fill", (d) => (d === merida ? color.morado : color.gris));
  g.append("text").attr("x", m.izquierda - 10).attr("y", fila / 2).attr("dy", "0.35em").attr("text-anchor", "end")
    .attr("font-size", 13.5).attr("font-weight", (d) => (d === merida ? 800 : 400)).text((d) => d.ciudad);
  g.append("text").attr("x", (d) => x(d.desnivel_m) + 8).attr("y", fila / 2).attr("dy", "0.35em")
    .attr("font-size", 13).attr("font-weight", 700)
    .style("fill", (d) => (d === merida ? color.morado : color.grisTexto))
    .text((d) => `${d === merida ? fmt.dec(d.desnivel_m) : fmt.num(d.desnivel_m)} m`);

  const i = filas.indexOf(merida);
  svg.append("text").attr("x", x(merida.desnivel_m) + 70).attr("y", y(i) + fila / 2).attr("dy", "0.35em")
    .attr("font-size", 13).style("fill", color.oroOscuro).text("← casi ni se ve");
}
