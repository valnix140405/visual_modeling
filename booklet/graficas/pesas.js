// Gráfica de pesas (dumbbell): dos precios del mismo producto unidos por una barra.
// Morado = el canal que se analiza (foco); oro = el súper (comparación).
// La usan las escenas 3 y 4.

import { d3, color, fmt } from "./estilo.js";

export function pesas(svg, filas, { ancho, alto, precioFoco, precioComp, nombre, detalle, nombreFoco, nombreComp }) {
  const m = { arriba: 46, derecha: 130, abajo: 30, izquierda: 260 };
  const fila = (alto - m.arriba - m.abajo) / filas.length;
  const y = (i) => m.arriba + i * fila + fila / 2;
  const valores = filas.flatMap((d) => [d[precioFoco], d[precioComp]]);
  const x = d3.scaleLinear([0, d3.max(valores)], [m.izquierda, ancho - m.derecha]).nice();

  svg.append("g").selectAll("line").data(x.ticks(5)).join("line")
    .attr("x1", x).attr("x2", x).attr("y1", m.arriba - 10).attr("y2", alto - m.abajo).attr("stroke", color.borde);
  svg.append("g").attr("transform", `translate(0,${alto - m.abajo})`)
    .call(d3.axisBottom(x).ticks(5).tickFormat(fmt.pesos).tickSizeOuter(0))
    .call((g) => g.select(".domain").remove())
    .call((g) => g.selectAll("text").attr("font-size", 12).style("fill", color.grisTexto));

  // Leyenda escrita (dos colores con significado).
  const ley = svg.append("g").attr("transform", `translate(${m.izquierda},16)`);
  [[nombreFoco, color.morado], [nombreComp, color.oro]].forEach(([t, c], i) => {
    ley.append("circle").attr("cx", i * 210 + 7).attr("cy", 0).attr("r", 7).attr("fill", c);
    ley.append("text").attr("x", i * 210 + 20).attr("y", 0).attr("dy", "0.35em").attr("font-size", 13)
      .attr("font-weight", 700).style("fill", c === color.oro ? color.oroOscuro : c).text(t);
  });

  const g = svg.append("g").selectAll("g").data(filas).join("g").attr("transform", (_, i) => `translate(0,${y(i)})`);
  g.append("line").attr("x1", (d) => x(d[precioComp])).attr("x2", (d) => x(d[precioFoco]))
    .attr("stroke", color.borde).attr("stroke-width", 8).attr("stroke-linecap", "round");
  g.append("circle").attr("cx", (d) => x(d[precioComp])).attr("r", 9).attr("fill", color.oro);
  g.append("circle").attr("cx", (d) => x(d[precioFoco])).attr("r", 9).attr("fill", color.morado);

  g.append("text").attr("x", m.izquierda - 14).attr("y", detalle ? -7 : 0).attr("dy", "0.35em")
    .attr("text-anchor", "end").attr("font-size", 13).attr("font-weight", 700).text((d) => d[nombre]);
  if (detalle) {
    g.append("text").attr("x", m.izquierda - 14).attr("y", 10).attr("dy", "0.35em").attr("text-anchor", "end")
      .attr("font-size", 12).style("fill", color.grisTexto).text((d) => detalle(d));
  }

  // Precio y diferencia escritos junto al punto que quede más a la derecha.
  g.append("text")
    .attr("x", (d) => x(Math.max(d[precioFoco], d[precioComp])) + 16).attr("dy", "0.35em").attr("font-size", 12.5)
    .call((t) => t.append("tspan").attr("font-weight", 800).style("fill", color.morado).text((d) => fmt.pesos(d[precioFoco])))
    .call((t) => t.append("tspan").style("fill", color.grisTexto).text((d) => ` vs ${fmt.pesos(d[precioComp])}`));
  g.append("text")
    .attr("x", (d) => (x(d[precioFoco]) + x(d[precioComp])) / 2).attr("y", -14).attr("text-anchor", "middle")
    .attr("font-size", 12).attr("font-weight", 800).style("fill", color.oroOscuro)
    .text((d) => fmt.pctSigno(d.diferencia_pct));
  return { x, m };
}
