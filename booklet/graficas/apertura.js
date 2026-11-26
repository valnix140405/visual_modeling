// Ilustración de apertura · «Hasta la cebolla llora».
// Dos cebollas dibujadas en D3: la de la Central de Abasto (oro, comparación) y la del súper
// (morado, foco). La del súper llora una lágrima por cada 25 % de diferencia.
// Debajo, cuántos kilos compra un día de salario mínimo en cada lugar.
// Datos: ../datos/escena-2.csv (fila de cebolla) y ../datos/unidad-salario-minimo.csv.
// Se usa el salario mínimo del mismo año que los precios (PROFECO, mayo 2026 → salario 2026).

import { d3, color, fmt, cargar, marco } from "./estilo.js";

export async function apertura(selector, rutas = {}) {
  const comparables = await cargar(rutas.escena2 ?? "../datos/escena-2.csv");
  const salarios = await cargar(rutas.salario ?? "../datos/unidad-salario-minimo.csv");
  const d = comparables.sort((a, b) => b.diferencia_pct - a.diferencia_pct)[0];
  const anioPrecios = Number(String(d.corte).match(/\d{4}/)[0]);
  const salario = salarios.find((s) => s.anio === anioPrecios).salario_minimo_diario_mxn;
  const kgCentral = salario / d.precio_central_mxn, kgSuper = salario / d.precio_super_mxn;
  const lagrimas = Math.round(d.diferencia_pct / 25);

  const titulo = `Hasta la ${d.producto.toLowerCase()} llora: ${fmt.pesos(d.precio_central_mxn)} en el Abasto, ` +
    `${fmt.pesos(d.precio_super_mxn)} en el súper`;
  const subtitulo = `Mismo kilo de ${d.producto.toLowerCase()} (${d.presentacion.toLowerCase()}), mediana de precio por lugar. ` +
    `Con un día de salario mínimo ${anioPrecios} (${fmt.pesos(salario)}) alcanza para ${fmt.dec(kgCentral)} kg en la Central de Abasto ` +
    `o ${fmt.dec(kgSuper)} kg en el súper. Una lágrima por cada 25 % de diferencia. Mérida.`;
  const fuente = `Fuente: ${d.fuente} (02-A y 02-B), ${d.registros_central} registros en la Central y ${d.registros_super} en súper; ` +
    `CONASAMI, salario mínimo ${anioPrecios} · Corte: ${d.corte}`;

  const ancho = 760, alto = 380;
  const svg = marco(selector, { titulo, subtitulo, fuente, ancho, alto });

  const cebolla = (cx, tono, relleno, etiqueta, precio, kg, nLagrimas) => {
    const g = svg.append("g").attr("transform", `translate(${cx},170)`);
    g.append("path").attr("d", "M-10,-96 L0,-140 L10,-96 Z").attr("fill", "#5a8f3c");
    g.append("ellipse").attr("rx", 92).attr("ry", 98).attr("fill", relleno).attr("stroke", tono).attr("stroke-width", 4);
    [-46, 0, 46].forEach((x) => g.append("path")
      .attr("d", `M${x * 0.5},-94 Q${x * 1.15},0 ${x * 0.6},94`).attr("fill", "none")
      .attr("stroke", tono).attr("stroke-opacity", 0.35).attr("stroke-width", 2));
    [-28, 28].forEach((x) => g.append("circle").attr("cx", x).attr("cy", -14).attr("r", 7).attr("fill", color.tinta));
    g.append("path").attr("fill", "none").attr("stroke", color.tinta).attr("stroke-width", 3)
      .attr("d", nLagrimas ? "M-22,34 Q0,18 22,34" : "M-22,26 Q0,44 22,26");
    d3.range(nLagrimas).forEach((i) => {
      const lado = i % 2 ? 28 : -28, fila = Math.floor(i / 2);
      g.append("path").attr("fill", "#5b9bd5")
        .attr("d", `M${lado},${-2 + fila * 22} q -6,10 0,14 q 6,-4 0,-14 Z`).attr("transform", `translate(0,${fila * 2})`);
    });
    g.append("text").attr("y", 124).attr("text-anchor", "middle").attr("font-size", 15).attr("font-weight", 700)
      .style("fill", tono === color.oro ? color.oroOscuro : tono).text(etiqueta);
    g.append("text").attr("y", 158).attr("text-anchor", "middle").attr("font-size", 30).attr("font-weight", 800)
      .style("fill", tono === color.oro ? color.oroOscuro : tono).text(`${fmt.pesos(precio)}/kg`);
    g.append("text").attr("y", 186).attr("text-anchor", "middle").attr("font-size", 13).style("fill", color.grisTexto)
      .text(`1 día de salario mínimo = ${fmt.dec(kg)} kg`);
  };
  cebolla(170, color.oro, "#fdf3e3", "Central de Abasto", d.precio_central_mxn, kgCentral, 0);
  cebolla(590, color.morado, "#efe3f6", "Supermercado", d.precio_super_mxn, kgSuper, lagrimas);

  svg.append("text").attr("x", 380).attr("y", 150).attr("text-anchor", "middle").attr("font-size", 40)
    .attr("font-weight", 800).style("fill", color.morado).text(fmt.pctSigno(d.diferencia_pct));
  svg.append("path").attr("d", "M300,172 L452,172").attr("stroke", color.morado).attr("stroke-width", 3)
    .attr("marker-end", "url(#flecha-apertura)");
  svg.append("defs").append("marker").attr("id", "flecha-apertura").attr("viewBox", "0 0 10 10")
    .attr("refX", 8).attr("refY", 5).attr("markerWidth", 8).attr("markerHeight", 8).attr("orient", "auto")
    .append("path").attr("d", "M0,0 L10,5 L0,10 Z").attr("fill", color.morado);
}
