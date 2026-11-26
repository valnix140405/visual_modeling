// Escena 1 · El calendario de la canasta.
// Un mes de 30 cuadros: en morado, los días de salario mínimo que se lleva la canasta
// alimentaria de un hogar de Mérida; en oro, lo que queda para todo lo demás.
// Datos: ../datos/escena-1.csv (una fila).

import { d3, color, fmt, cargar, marco } from "./estilo.js";

export async function escena1(selector, ruta = "../datos/escena-1.csv") {
  const [d] = await cargar(ruta);
  const titulo = `El mes que se come tu sueldo: ${fmt.num(d.dias_canasta)} días pa' la panza`;
  const subtitulo =
    `Días de salario mínimo general ${String(d.corte).match(/\d{4}/)[0]} (${fmt.pesos(d.salario_minimo_diario_mxn)} diarios) que cuesta un mes de ` +
    `canasta alimentaria urbana (línea de pobreza extrema de INEGI, ${d.corte}) para un hogar de ${fmt.dec2(d.ocupantes_por_vivienda)} personas en Mérida: ` +
    `${fmt.pesos(d.canasta_hogar_mxn)}. Cada cuadro es un día del mes.`;
  const fuente = `Fuente: ${d.fuente} · Corte: ${d.corte}`;

  const ancho = 760, alto = 380;
  const svg = marco(selector, { titulo, subtitulo, fuente, ancho, alto });

  const cols = 7, lado = 56, sep = 8, x0 = 10, y0 = 36;
  const dias = d3.range(d.dias_mes);
  const semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"];

  svg.append("g").selectAll("text").data(semana).join("text")
    .attr("x", (_, i) => x0 + i * (lado + sep) + lado / 2).attr("y", y0 - 12)
    .attr("text-anchor", "middle").attr("font-size", 12).attr("font-weight", 700)
    .attr("fill", color.grisTexto).text((t) => t);

  const celda = svg.append("g").selectAll("g").data(dias).join("g")
    .attr("transform", (i) => `translate(${x0 + (i % cols) * (lado + sep)},${y0 + Math.floor(i / cols) * (lado + sep)})`);

  celda.append("rect").attr("width", lado).attr("height", lado).attr("rx", 7).attr("fill", color.oro);
  // Parte del día que se va en la canasta (el último día queda parcialmente pintado).
  celda.append("rect")
    .attr("width", (i) => lado * Math.max(0, Math.min(1, d.dias_canasta - i)))
    .attr("height", lado).attr("rx", 7).attr("fill", color.morado);
  celda.append("text").attr("x", 7).attr("y", 17).attr("font-size", 12).attr("font-weight", 700)
    .style("fill", color.blanco).text((i) => i + 1);

  // Cifras a la derecha (escritas, sin depender del cursor).
  const xr = x0 + cols * (lado + sep) + 34;
  svg.append("text").attr("x", xr).attr("y", 110).attr("font-size", 76).attr("font-weight", 800)
    .style("fill", color.morado).text(fmt.dec(d.dias_canasta));
  svg.append("text").attr("x", xr).attr("y", 140).attr("font-size", 16).style("fill", color.morado)
    .text("días de trabajo para la comida");
  svg.append("text").attr("x", xr).attr("y", 250).attr("font-size", 56).attr("font-weight", 800)
    .style("fill", color.oro).text(fmt.dec(d.dias_libres));
  svg.append("text").attr("x", xr).attr("y", 278).attr("font-size", 16).style("fill", color.oroOscuro)
    .text("días para renta, luz, transporte,");
  svg.append("text").attr("x", xr).attr("y", 300).attr("font-size", 16).style("fill", color.oroOscuro)
    .text("escuela, salud… todo lo demás");

  // Anotación sobre el último día de comida.
  const ultimo = Math.floor(d.dias_canasta);
  const xu = x0 + (ultimo % cols) * (lado + sep), yu = y0 + Math.floor(ultimo / cols) * (lado + sep);
  svg.append("path").attr("fill", "none").attr("stroke", color.oroOscuro).attr("stroke-width", 1.5)
    .attr("d", `M${xu + lado * 0.6},${yu + lado + 4} q 10,40 60,52`);
  svg.append("text").attr("x", xu + lado * 0.6 + 64).attr("y", yu + lado + 60).attr("font-size", 13)
    .style("fill", color.oroOscuro)
    .text(`Hasta el día ${ultimo + 1} se sigue pagando la canasta`);
}
