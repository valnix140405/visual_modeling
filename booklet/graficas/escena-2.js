// Escena 2 · Central de Abasto contra súper.
// Barras horizontales con la diferencia de precio del súper frente a la Central de Abasto
// (misma presentación). Se muestran los 10 productos que más suben y los 3 que más bajan,
// con la mediana de todos los productos como referencia.
// Datos: ../datos/escena-2.csv (139 productos).

import { d3, color, fmt, cargar, marco } from "./estilo.js";

export async function escena2(selector, ruta = "../datos/escena-2.csv") {
  const todas = (await cargar(ruta)).sort((a, b) => b.diferencia_pct - a.diferencia_pct);
  const mediana = d3.median(todas, (d) => d.diferencia_pct);
  const masCaro = todas.filter((d) => d.diferencia_pct > 0).length;
  const top = todas.slice(0, 10), bajan = todas.slice(-3);
  const foco = top[0];

  const titulo = `Mismo producto, otro pasillo: la ${foco.producto.toLowerCase()} cuesta ${fmt.pctEntero(foco.diferencia_pct).replace("+", "")} más en el súper`;
  const subtitulo =
    `Diferencia de precio del supermercado frente a la Central de Abasto, misma presentación (mediana por producto). ` +
    `El súper fue más caro en ${masCaro} de ${todas.length} productos. Se muestran los 10 que más suben y los 3 que más bajan. Mérida.`;
  const fuente = `Fuente: ${foco.fuente} (02-A y 02-B), precios al público · Corte: ${foco.corte}`;

  const filas = [...top, null, ...bajan]; // null = separador
  const ancho = 760, fila = 28, m = { arriba: 34, derecha: 150, abajo: 26, izquierda: 250 };
  const alto = m.arriba + filas.length * fila + m.abajo;
  const svg = marco(selector, { titulo, subtitulo, fuente, ancho, alto });

  const y = (i) => m.arriba + i * fila;
  const x = d3.scaleLinear(d3.extent([...todas.map((d) => d.diferencia_pct), 0]), [m.izquierda, ancho - m.derecha]).nice();

  svg.append("g").selectAll("line").data(x.ticks(6)).join("line")
    .attr("x1", x).attr("x2", x).attr("y1", m.arriba - 6).attr("y2", alto - m.abajo)
    .attr("stroke", color.borde);
  svg.append("g").attr("transform", `translate(0,${alto - m.abajo})`)
    .call(d3.axisBottom(x).ticks(6).tickFormat((v) => fmt.pctEntero(v)).tickSizeOuter(0))
    .call((g) => g.select(".domain").remove())
    .call((g) => g.selectAll("text").attr("font-size", 12).style("fill", color.grisTexto));

  // Mediana de todos los productos.
  svg.append("line").attr("x1", x(mediana)).attr("x2", x(mediana)).attr("y1", m.arriba - 10).attr("y2", alto - m.abajo)
    .attr("stroke", color.oroOscuro).attr("stroke-dasharray", "4 3").attr("stroke-width", 1.5);
  svg.append("text").attr("x", x(mediana) + 6).attr("y", m.arriba - 14).attr("font-size", 12.5).attr("font-weight", 700)
    .style("fill", color.oroOscuro).text(`Mediana de ${todas.length} productos: ${fmt.pctSigno(mediana)}`);

  const g = svg.append("g").selectAll("g").data(filas).join("g").attr("transform", (_, i) => `translate(0,${y(i)})`);
  const barras = g.filter((d) => d);
  barras.append("rect")
    .attr("x", (d) => x(Math.min(0, d.diferencia_pct))).attr("y", 4)
    .attr("width", (d) => Math.abs(x(d.diferencia_pct) - x(0))).attr("height", fila - 8).attr("rx", 3)
    .attr("fill", (d) => (d === foco ? color.morado : color.gris));
  barras.append("text").attr("x", m.izquierda - 10).attr("y", fila / 2).attr("dy", "0.35em")
    .attr("text-anchor", "end").attr("font-size", 12.5)
    .attr("font-weight", (d) => (d === foco ? 800 : 400))
    .text((d) => recortar(`${d.producto} · ${d.presentacion}`, 38))
    .append("title").text((d) => `${d.producto} · ${d.presentacion}`);
  barras.append("text").attr("x", (d) => x(Math.max(0, d.diferencia_pct)) + 6).attr("y", fila / 2).attr("dy", "0.35em")
    .attr("font-size", 12.5).attr("font-weight", 700)
    .attr("stroke", color.blanco).attr("stroke-width", 4).attr("paint-order", "stroke")
    .style("fill", (d) => (d === foco ? color.morado : color.grisTexto))
    .text((d) => fmt.pctSigno(d.diferencia_pct));
  g.filter((d) => !d).append("text").attr("x", m.izquierda - 10).attr("y", fila / 2).attr("dy", "0.35em")
    .attr("text-anchor", "end").attr("font-size", 12).attr("font-style", "italic").style("fill", color.grisTexto)
    .text("… y los que más bajan en el súper");

  // Anotación del foco con sus dos precios.
  svg.append("text").attr("x", x(foco.diferencia_pct) + 62).attr("y", y(0) + fila / 2).attr("dy", "0.35em")
    .attr("font-size", 12).style("fill", color.oroOscuro)
    .text(`${fmt.pesos(foco.precio_central_mxn)} → ${fmt.pesos(foco.precio_super_mxn)}`);
}

function recortar(t, n) { return t.length > n ? `${t.slice(0, n - 1)}…` : t; }
