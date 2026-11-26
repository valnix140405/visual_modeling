// Gráficas D3 propias del sitio (las que no tienen equivalente en el booklet).
// Usan el estilo común del booklet (paleta, formatos y marco) y leen CSV o GeoJSON del repositorio.

import { d3, color, fmt, cargar, marco } from "../../booklet/graficas/estilo.js";

// Portada: la misma cebolla, dos precios. Con lo que cuesta 1 kg en el súper,
// ¿cuántos kilos te llevas en la Central de Abasto? Datos: booklet/datos/escena-2.csv.
export async function cebolla(selector, ruta = "booklet/datos/escena-2.csv") {
  const filas = await cargar(ruta);
  const c = filas.find((d) => d.producto === "Cebolla" && /Blanca Sin Rabo/.test(d.presentacion));
  if (!c) throw new Error("no se encontró la cebolla blanca en escena-2.csv");
  const kg = c.precio_super_mxn / c.precio_central_mxn;
  const titulo = `Con lo que pagas 1 kg de cebolla en el súper, en el Abasto te llevas ${fmt.dec(kg)} kg`;
  const subtitulo = `Cebolla blanca sin rabo, 1 kg a granel: ${fmt.pesos(c.precio_central_mxn)} en la Central de Abasto ` +
    `(mediana de ${c.registros_central} registros) y ${fmt.pesos(c.precio_super_mxn)} en supermercados ` +
    `(mediana de ${c.registros_super}). Mérida.`;
  const fuente = `Fuente: ${c.fuente} (02-A y 02-B), precios al público · Corte: ${c.corte}`;
  const ancho = 760, alto = 300;
  const svg = marco(selector, { titulo, subtitulo, fuente, ancho, alto });

  const r = 44;
  const grupo = (x0, n, relleno, etiqueta, precio, colorTexto) => {
    const g = svg.append("g").attr("transform", `translate(${x0},0)`);
    g.append("text").attr("x", 0).attr("y", 30).attr("font-size", 15).attr("font-weight", 800)
      .style("fill", colorTexto).text(etiqueta);
    const enteros = Math.floor(n), parte = n - enteros;
    d3.range(Math.ceil(n)).forEach((i) => {
      const cx = r + i * (2 * r + 14), cy = 110;
      const frac = i < enteros ? 1 : parte;
      const id = `rec-${selector.replace(/\W/g, "")}-${x0}-${i}`;
      g.append("clipPath").attr("id", id).append("rect")
        .attr("x", cx - r).attr("y", cy - r - 20).attr("width", 2 * r * frac).attr("height", 2 * r + 40);
      g.append("circle").attr("cx", cx).attr("cy", cy).attr("r", r).attr("fill", "none")
        .attr("stroke", color.gris).attr("stroke-dasharray", "4 3");
      g.append("g").attr("clip-path", `url(#${id})`)
        .call((h) => h.append("circle").attr("cx", cx).attr("cy", cy).attr("r", r).attr("fill", relleno))
        .call((h) => h.append("path").attr("d", `M${cx - 7},${cy - r + 4} L${cx},${cy - r - 20} L${cx + 7},${cy - r + 4} Z`).attr("fill", relleno));
    });
    g.append("text").attr("x", 0).attr("y", 200).attr("font-size", 30).attr("font-weight", 800)
      .style("fill", colorTexto).text(`${fmt.dec(n)} kg`);
    g.append("text").attr("x", 0).attr("y", 224).attr("font-size", 14).style("fill", color.grisTexto)
      .text(`a ${fmt.pesos(precio)} el kilo`);
  };
  grupo(10, kg, color.oro, "En la Central de Abasto", c.precio_central_mxn, color.oroOscuro);
  grupo(480, 1, color.morado, "En el súper", c.precio_super_mxn, color.morado);
  svg.append("text").attr("x", 10).attr("y", 280).attr("font-size", 13).style("fill", color.oroOscuro)
    .text(`Mismo dinero (${fmt.pesos(c.precio_super_mxn)}), ${fmt.pctSigno(c.diferencia_pct)} de diferencia en el precio por kilo.`);
}

// Relieve: desnivel dentro de cada ciudad. Datos: booklet/datos/puente-relieve.csv.
export async function relieve(selector, ruta = "booklet/datos/puente-relieve.csv") {
  const filas = (await cargar(ruta)).sort((a, b) => b.desnivel_m - a.desnivel_m);
  const merida = filas.find((d) => d.ciudad === "Mérida");
  const mayor = filas[0];
  const veces = mayor.desnivel_m / merida.desnivel_m;
  const titulo = `Mérida, plana como comal: ${fmt.num(merida.desnivel_m)} m de desnivel; ${mayor.ciudad}, ${fmt.num(mayor.desnivel_m)} m`;
  const subtitulo = `Diferencia entre el punto más alto y el más bajo de una malla de 20 × 20 puntos por ciudad. ` +
    `El desnivel de ${mayor.ciudad} es ${fmt.num(veces)} veces el de Mérida.`;
  const fuente = `Fuente: ${merida.fuente} · Corte: ${merida.corte}. Es elevación de un modelo de terreno, no LiDAR.`;
  const ancho = 760, fila = 40, m = { arriba: 10, derecha: 90, abajo: 28, izquierda: 210 };
  const alto = m.arriba + filas.length * fila + m.abajo;
  const svg = marco(selector, { titulo, subtitulo, fuente, ancho, alto });
  const x = d3.scaleLinear([0, mayor.desnivel_m], [m.izquierda, ancho - m.derecha]).nice();
  svg.append("g").attr("transform", `translate(0,${alto - m.abajo})`)
    .call(d3.axisBottom(x).ticks(5).tickFormat((v) => `${fmt.num(v)} m`).tickSizeOuter(0))
    .call((g) => g.select(".domain").remove())
    .call((g) => g.selectAll("text").attr("font-size", 12).style("fill", color.grisTexto));
  const g = svg.append("g").selectAll("g").data(filas).join("g")
    .attr("transform", (_, i) => `translate(0,${m.arriba + i * fila})`);
  const esM = (d) => d.ciudad === "Mérida";
  g.append("rect").attr("x", x(0)).attr("y", 6).attr("height", fila - 12).attr("rx", 3)
    .attr("width", (d) => Math.max(2, x(d.desnivel_m) - x(0)))
    .attr("fill", (d) => (esM(d) ? color.morado : color.gris));
  g.append("text").attr("x", m.izquierda - 10).attr("y", fila / 2).attr("dy", "0.35em").attr("text-anchor", "end")
    .attr("font-size", 13).attr("font-weight", (d) => (esM(d) ? 800 : 400)).text((d) => d.ciudad);
  g.append("text").attr("x", (d) => x(d.desnivel_m) + 8).attr("y", fila / 2).attr("dy", "0.35em")
    .attr("font-size", 13).attr("font-weight", 700)
    .style("fill", (d) => (esM(d) ? color.morado : color.grisTexto)).text((d) => `${fmt.dec(d.desnivel_m)} m`);
}

// Va y Ven en OpenStreetMap: cuántos elementos son paradas, rutas u otros.
// Datos: data/fuente_c/04_transporte_vayven/export.geojson.
export async function vayven(selector, ruta = "data/fuente_c/04_transporte_vayven/export.geojson") {
  const geo = await d3.json(new URL(ruta, document.baseURI));
  const tipo = (p) => (p.highway === "bus_stop" ? "Paradas" : p.type === "route" ? "Rutas" : "Otros elementos");
  const conteo = d3.rollups(geo.features, (v) => v.length, (f) => tipo(f.properties))
    .map(([t, n]) => ({ t, n })).sort((a, b) => b.n - a.n);
  const total = d3.sum(conteo, (d) => d.n);
  const paradas = conteo.find((d) => d.t === "Paradas")?.n ?? 0;
  const titulo = `${fmt.num(paradas)} paradas del Va y Ven ya están mapeadas en OpenStreetMap`;
  const subtitulo = `Elementos del transporte público de Mérida exportados de OpenStreetMap (${fmt.num(total)} en total), por tipo.`;
  const stamp = geo.timestamp ? geo.timestamp.slice(0, 10) : "octubre 2026";
  const fuente = `Fuente: OpenStreetMap vía Overpass Turbo (04-C), licencia ODbL · Corte: ${stamp}`;
  const ancho = 760, fila = 46, m = { arriba: 10, derecha: 90, abajo: 28, izquierda: 170 };
  const alto = m.arriba + conteo.length * fila + m.abajo;
  const svg = marco(selector, { titulo, subtitulo, fuente, ancho, alto });
  const x = d3.scaleLinear([0, d3.max(conteo, (d) => d.n)], [m.izquierda, ancho - m.derecha]).nice();
  svg.append("g").attr("transform", `translate(0,${alto - m.abajo})`)
    .call(d3.axisBottom(x).ticks(5).tickFormat(fmt.num).tickSizeOuter(0))
    .call((g) => g.select(".domain").remove())
    .call((g) => g.selectAll("text").attr("font-size", 12).style("fill", color.grisTexto));
  const g = svg.append("g").selectAll("g").data(conteo).join("g")
    .attr("transform", (_, i) => `translate(0,${m.arriba + i * fila})`);
  g.append("rect").attr("x", x(0)).attr("y", 7).attr("height", fila - 14).attr("rx", 3)
    .attr("width", (d) => x(d.n) - x(0)).attr("fill", (d) => (d.t === "Paradas" ? color.morado : color.gris));
  g.append("text").attr("x", m.izquierda - 10).attr("y", fila / 2).attr("dy", "0.35em").attr("text-anchor", "end")
    .attr("font-size", 13.5).attr("font-weight", (d) => (d.t === "Paradas" ? 800 : 400)).text((d) => d.t);
  g.append("text").attr("x", (d) => x(d.n) + 8).attr("y", fila / 2).attr("dy", "0.35em").attr("font-size", 13.5)
    .attr("font-weight", 700).style("fill", (d) => (d.t === "Paradas" ? color.morado : color.grisTexto))
    .text((d) => fmt.num(d.n));
}
