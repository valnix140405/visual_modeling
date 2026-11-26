// Sitio web · cifras y gráficas D3 desde CSV.
// 1. Carga data/web/cifras_sitio.csv y rellena cada <span data-cifra="clave">.
// 2. Arranca los contadores, el simulador y el selector de productos con esas cifras.
// 3. Dibuja las escenas en D3 (las del booklet y las propias del sitio).
// Ninguna cifra vive en este archivo.

import { d3 } from "../../booklet/graficas/estilo.js";
import { escena1 } from "../../booklet/graficas/escena-1.js";
import { escena2 } from "../../booklet/graficas/escena-2.js";
import { escena3 } from "../../booklet/graficas/escena-3.js";
import { escena4 } from "../../booklet/graficas/escena-4.js";
import { cebolla, relieve, vayven } from "./graficas.js";

const mx = d3.formatLocale({ decimal: ".", thousands: ",", grouping: [3], currency: ["$", ""] });
const signo = (v, dec) => `${v < 0 ? "−" : "+"}${mx.format(`,.${dec}f`)(Math.abs(v))}%`;
const FORMATOS = {
  num: mx.format(",.0f"),
  dec: mx.format(",.1f"),
  dec2: mx.format(",.2f"),
  pesos: mx.format("$,.2f"),
  pesosEnteros: mx.format("$,.0f"),
  pct: (v) => `${mx.format(",.1f")(v)}%`,
  pctEntero: (v) => `${mx.format(",.0f")(v)}%`,
  pctSigno: (v) => signo(v, 1),
  pctSignoEntero: (v) => signo(v, 0),
  texto: (v) => `${v}`,
};

const base = (ruta) => new URL(ruta, document.baseURI);

async function cargarCifras() {
  const filas = await d3.csv(base("data/web/cifras_sitio.csv"));
  const mapa = new Map(filas.map((f) => [f.clave, f]));
  const valor = (k) => (mapa.has(k) ? Number(mapa.get(k).valor) : undefined);
  const texto = (k) => {
    const f = mapa.get(k);
    if (!f) return `⚠ falta «${k}»`;
    const fn = FORMATOS[f.formato];
    return fn ? fn(f.formato === "texto" ? f.valor : Number(f.valor)) : f.valor;
  };
  window.CIFRA = Object.fromEntries(filas.map((f) => [f.clave, Number(f.valor)]));
  window.cifraTexto = texto;

  const faltan = new Set();
  document.querySelectorAll("[data-cifra]").forEach((el) => {
    const k = el.dataset.cifra;
    if (!mapa.has(k)) {
      faltan.add(k);
      el.classList.add("cifra-faltante");
      el.title = `Falta la cifra «${k}» en data/web/cifras_sitio.csv`;
    }
    el.textContent = texto(k);
  });
  if (faltan.size) console.warn("Cifras sin dato en data/web/cifras_sitio.csv:", [...faltan]);
  return { valor, texto };
}

function arrancarContadores(valor) {
  const kpis = [["kpiComercios", "denue_comercios", false], ["kpiPrecios", "profeco_registros", false],
    ["kpiDelivery", "abasto_mediana", true], ["kpiEnoe", "enoe_registros", false]];
  for (const [id, clave, pct] of kpis) {
    const v = valor(clave);
    if (v !== undefined && window.animateCount) window.animateCount(id, v, pct);
  }
}

function arrancarSimulador(valor) {
  const mensual = valor("salario_mensual");
  const slider = document.getElementById("wageSlider");
  if (!mensual || !slider) return;
  slider.value = mensual;
  if (window.runWageCalc) window.runWageCalc(mensual);
}

// Selector del capítulo 2: etiquetas de los botones → producto y presentación en escena-2.csv.
const SELECTOR = {
  Cebolla: ["Cebolla", /Blanca Sin Rabo/, "Cebolla blanca sin rabo, 1 kg a granel", "/kg"],
  Arroz: ["Arroz", /900 Gr/, "Arroz súper extra, bolsa de 900 g", ""],
  Frijol: ["Frijol", /900 Gr/, "Frijol negro, bolsa de 900 g", ""],
  Limon: ["Limón", /Persa/, "Limón agrio sin semilla o persa, 1 kg a granel", "/kg"],
  Papa: ["Papa", /Alfa/, "Papa alfa o blanca, 1 kg a granel", "/kg"],
  Jitomate: ["Jitomate", /Saladette/, "Jitomate saladette, 1 kg a granel", "/kg"],
  Tortilla: ["Tortilla de Maíz", /Granel/, "Tortilla de maíz, 1 kg a granel", "/kg"],
  Pollo: ["Carne Pollo", /Entero/, "Pollo entero, 1 kg a granel", "/kg"],
};

async function prepararSelector() {
  const filas = await d3.csv(base("booklet/datos/escena-2.csv"), d3.autoType);
  for (const [clave, [prod, pres, desc, unidad]] of Object.entries(SELECTOR)) {
    const r = filas.find((d) => d.producto === prod && pres.test(d.presentacion));
    if (!r) { console.warn(`Selector: no se encontró ${prod} en escena-2.csv`); continue; }
    const barato = r.diferencia_pct < 0 ? " Aquí el súper es más barato." : "";
    window.productData[clave] = {
      mayoreo: FORMATOS.pesos(r.precio_central_mxn) + unidad,
      menudeo: FORMATOS.pesos(r.precio_super_mxn) + unidad,
      margen: FORMATOS.pctSigno(r.diferencia_pct),
      desc: `${desc}.${barato} Mediana de ${r.registros_central} registros en la Central de Abasto y ` +
        `${r.registros_super} en supermercados (PROFECO, ${r.corte}).`,
    };
  }
  const d = window.productData.Cebolla;
  if (d) {
    document.getElementById("prodMayoreo").textContent = d.mayoreo;
    document.getElementById("prodMenudeo").textContent = d.menudeo;
    document.getElementById("prodMargen").textContent = d.margen;
    document.getElementById("prodDesc").textContent = d.desc;
  }
}

// Conteos de los filtros del catálogo: se cuentan las filas de la tabla.
function contarFiltrosCatalogo() {
  const filas = [...document.querySelectorAll("#matrixTable tbody tr")];
  const cuenta = (fn) => filas.filter(fn).length;
  const n = {
    all: filas.length,
    fuente_a: cuenta((r) => r.dataset.block === "fuente_a"),
    fuente_b: cuenta((r) => r.dataset.block === "fuente_b"),
    fuente_c: cuenta((r) => r.dataset.block === "fuente_c"),
    "3d": cuenta((r) => r.dataset.cat === "3d"),
    scrapers: cuenta((r) => r.dataset.cat === "scrapers"),
  };
  document.querySelectorAll(".filter-btn").forEach((b) => {
    const m = b.getAttribute("onclick")?.match(/filterTable\('([^']+)'\)/);
    if (m && n[m[1]] !== undefined) b.textContent = b.textContent.replace(/\(\d+\)/, `(${n[m[1]]})`);
  });
}

// Escenas D3: contenedor del sitio → función que la dibuja.
const ESCENAS = [
  ["#d3-svg-escena-1", (s) => cebolla(s)],
  ["#d3-svg-escena-1b", (s) => escena2(s, "booklet/datos/escena-2.csv")],
  ["#d3-svg-escena-2", (s) => escena3(s, "booklet/datos/escena-3.csv")],
  ["#d3-svg-escena-3", (s) => escena1(s, "booklet/datos/escena-1.csv")],
  ["#d3-svg-escena-4", (s) => escena4(s, "booklet/datos/escena-4.csv")],
  ["#d3-svg-escena-5", (s) => relieve(s)],
  ["#d3-svg-escena-6", (s) => vayven(s)],
];

async function dibujarEscenas() {
  return Promise.allSettled(ESCENAS.map(async ([sel, fn]) => {
    const el = document.querySelector(sel);
    if (!el) return;
    try {
      await fn(sel);
      const svg = el.querySelector("svg");
      if (svg) {
        svg.id = el.dataset.svgId; // lo usan los botones PNG/Zoom y el recorrido guiado
        svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
        // Tamaño intrínseco para zoom y PNG (en pantalla manda el CSS: ancho 100 %).
        const vb = svg.viewBox.baseVal;
        if (vb && vb.width) { svg.setAttribute("width", vb.width); svg.setAttribute("height", vb.height); }
      }
    } catch (e) {
      el.innerHTML = `<p class="grafica-error">No se pudo dibujar esta gráfica: ${e.message}</p>`;
      console.error(sel, e);
    }
  }));
}

async function iniciar() {
  try {
    const { valor } = await cargarCifras();
    arrancarContadores(valor);
    arrancarSimulador(valor);
  } catch (e) {
    console.error("No se pudieron cargar las cifras del sitio:", e);
    document.querySelectorAll("[data-cifra]").forEach((el) => el.classList.add("cifra-faltante"));
  }
  contarFiltrosCatalogo();
  await Promise.allSettled([prepararSelector(), dibujarEscenas()]);
  document.body.dataset.listo = "si";
}

iniciar();
