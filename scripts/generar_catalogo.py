"""Genera el catálogo de visualizaciones de los 9 equipos.

Entrada:  catalogo/catalogo_visualizaciones.json (única fuente de verdad)
Salidas:  catalogo/index.html        despliegue web con filtros
          catalogo/imprimible.html   versión para imprimir (carta)
          catalogo/catalogo_visualizaciones.pdf  (si se pasa --pdf; requiere Node + Playwright)

Uso:
    python scripts/generar_catalogo.py [--pdf]
"""
import html
import json
import os
import subprocess
import sys
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(RAIZ, "catalogo")
URL_CATALOGO = "https://valnix140405.github.io/visual_modeling/catalogo/"

TIPOS = ["Barras", "Línea", "Mapa", "Heatmap", "Distribución", "Radar", "Red / flujo", "KPI / tabla", "3D / AR"]
ESTADOS = ["imagen", "interactivo", "texto", "candidato"]
DATOS = ["real", "fijo", "simulado", "sin_datos"]
ETQ_ESTADO = {"imagen": "Imagen", "interactivo": "Interactiva", "texto": "Solo texto", "candidato": "Candidato"}
ETQ_DATOS = {"real": "Datos del repo", "fijo": "Cifras fijas", "simulado": "Simulados", "sin_datos": "Sin datos"}

e = html.escape


def cargar():
    with open(os.path.join(DIR, "catalogo_visualizaciones.json"), encoding="utf-8") as f:
        cat = json.load(f)
    equipos = {t["n"]: t for t in cat["equipos"]}
    for v in cat["visuales"]:
        assert v["tipo"] in TIPOS, v
        assert v["estado"] in ESTADOS, v
        assert v["datos"] in DATOS, v
        if v.get("img"):
            assert os.path.exists(os.path.join(DIR, v["img"])), v["img"]
        v["url"] = equipos[v["eq"]]["repo"] + "/blob/main/" + v["ref"]
    return cat, equipos


def qr_svg(url):
    try:
        import segno
    except ImportError:
        return '<div class="qr-falta">QR pendiente (pip install segno)</div>'
    import io
    buf = io.BytesIO()
    segno.make(url, error="m").save(buf, kind="svg", scale=4, border=2, xmldecl=False, svgns=True, dark="#1a1a1a")
    return buf.getvalue().decode("utf-8")


def resumen(cat):
    vis = cat["visuales"]
    por_eq = {t["n"]: Counter() for t in cat["equipos"]}
    for v in vis:
        c = por_eq[v["eq"]]
        c["total"] += 1
        c[v["estado"]] += 1
        c["d_" + v["datos"]] += 1
        c["t_" + v["tipo"]] += 1
    tot = Counter()
    for v in vis:
        tot["total"] += 1
        tot[v["estado"]] += 1
        tot["d_" + v["datos"]] += 1
        tot["t_" + v["tipo"]] += 1
    return por_eq, tot


CSS_BASE = """
:root{--bg:#f8f9fa;--card:#fff;--text:#0d0d0d;--muted:#555;--line:#e5e7eb;
--purple:#600d8b;--purple-soft:rgba(96,13,139,.06);--gold:#ed9f22;--gold-dark:#b45309;
--ok:#15803d;--ok-bg:#dcfce7;--warn:#a16207;--warn-bg:#fef3c7;--bad:#b91c1c;--bad-bg:#fee2e2;--na:#4b5563;--na-bg:#e5e7eb}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:'Outfit',system-ui,sans-serif;line-height:1.45;-webkit-font-smoothing:antialiased}
a{color:var(--purple)}
.badge{display:inline-block;font-size:11.5px;font-weight:600;padding:2px 8px;border-radius:999px;white-space:nowrap}
.d-real{background:var(--ok-bg);color:var(--ok)}.d-fijo{background:var(--warn-bg);color:var(--warn)}
.d-simulado{background:var(--bad-bg);color:var(--bad)}.d-sin_datos{background:var(--na-bg);color:var(--na)}
.s-imagen,.s-interactivo,.s-texto,.s-candidato{background:var(--purple-soft);color:var(--purple)}
"""


def pagina_web(cat, equipos):
    por_eq, tot = resumen(cat)
    meta = cat["meta"]
    datos_js = json.dumps({"equipos": cat["equipos"], "visuales": cat["visuales"], "tipos": TIPOS,
                           "etqEstado": ETQ_ESTADO, "etqDatos": ETQ_DATOS}, ensure_ascii=False)

    # Matriz equipo x tipo
    filas = []
    for t in cat["equipos"]:
        c = por_eq[t["n"]]
        celdas = "".join(
            f'<td class="m{min(c["t_" + tp], 4)}">{c["t_" + tp] or ""}</td>' for tp in TIPOS)
        filas.append(f'<tr><th scope="row"><a href="#eq{t["n"]}">E{t["n"]} · {e(t["proyecto"])}</a></th>{celdas}'
                     f'<td class="tot">{c["total"]}</td></tr>')
    pie = "".join(f'<td class="tot">{tot["t_" + tp]}</td>' for tp in TIPOS)
    matriz = (f'<table class="matriz"><thead><tr><th>Equipo</th>{"".join(f"<th>{e(tp)}</th>" for tp in TIPOS)}<th>Total</th></tr></thead>'
              f'<tbody>{"".join(filas)}</tbody><tfoot><tr><th>Total</th>{pie}<td class="tot">{tot["total"]}</td></tr></tfoot></table>')

    opts_eq = "".join(f'<option value="{t["n"]}">Equipo {t["n"]} · {e(t["proyecto"])}</option>' for t in cat["equipos"])
    chips = lambda grupo, items, etq: "".join(
        f'<button type="button" class="chip" data-grupo="{grupo}" data-valor="{e(i)}" aria-pressed="false">{e(etq.get(i, i))}</button>' for i in items)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catálogo de visualizaciones</title>
<meta name="description" content="Gráficas, mapas y escenas 3D/AR propuestas por los 9 equipos de Visual Modeling UPY, con su estado y procedencia de datos.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS_BASE}
.wrap{{max-width:1240px;margin:0 auto;padding:28px 16px 64px}}
header.top{{display:flex;flex-wrap:wrap;gap:16px;justify-content:space-between;align-items:flex-end;border-bottom:3px solid var(--purple);padding-bottom:18px}}
.eyebrow{{font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--gold-dark)}}
h1{{font-size:clamp(26px,4vw,38px);line-height:1.1;margin:6px 0 8px;font-weight:800}}
.lead{{color:var(--muted);max-width:760px;margin:0}}
.acciones{{display:flex;gap:8px;flex-wrap:wrap}}
.btn{{display:inline-block;padding:9px 14px;border-radius:10px;border:1px solid var(--line);background:var(--card);font-weight:600;font-size:14px;text-decoration:none;color:var(--text)}}
.btn.primario{{background:var(--purple);border-color:var(--purple);color:#fff}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:22px 0}}
.kpi{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}}
.kpi b{{display:block;font-size:30px;font-weight:800;line-height:1.1}}
.kpi span{{color:var(--muted);font-size:13.5px}}
section.bloque{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;margin:18px 0}}
h2{{font-size:20px;margin:0 0 4px}}
.nota{{color:var(--muted);font-size:13.5px;margin:0 0 12px}}
.scroll{{overflow-x:auto}}
.matriz{{border-collapse:collapse;width:100%;font-size:13.5px;min-width:820px}}
.matriz th,.matriz td{{border-bottom:1px solid var(--line);padding:7px 8px;text-align:center}}
.matriz thead th{{font-size:12px;color:var(--muted);font-weight:600}}
.matriz tbody th,.matriz tfoot th{{text-align:left;font-weight:600;white-space:nowrap}}
.matriz tbody th a{{text-decoration:none;color:var(--text)}}
.m1{{background:rgba(96,13,139,.08)}}.m2{{background:rgba(96,13,139,.18)}}.m3{{background:rgba(96,13,139,.30)}}.m4{{background:rgba(96,13,139,.45);color:#fff}}
.tot{{font-weight:700}}
.filtros{{display:grid;gap:10px;grid-template-columns:minmax(0,1fr)}}
.fila-f{{display:flex;flex-wrap:wrap;gap:6px;align-items:center}}
.fila-f > span{{font-size:12.5px;font-weight:700;color:var(--muted);min-width:84px}}
select{{font:inherit;padding:7px 10px;border-radius:10px;border:1px solid var(--line);background:var(--card);max-width:100%;min-width:0;flex:1 1 220px}}
.chip{{font:inherit;font-size:13px;padding:5px 11px;border-radius:999px;border:1px solid var(--line);background:var(--card);cursor:pointer}}
.chip[aria-pressed="true"]{{background:var(--purple);border-color:var(--purple);color:#fff}}
.vista{{display:flex;gap:6px;margin:4px 0 0}}
#conteo{{font-size:13.5px;color:var(--muted);margin-top:4px}}
.equipo{{margin:26px 0 10px;scroll-margin-top:12px}}
.eq-head{{display:grid;grid-template-columns:1fr auto;gap:12px;align-items:start;border-left:5px solid var(--gold);padding:4px 0 4px 14px}}
.eq-head h3{{margin:0;font-size:21px}}
.eq-head p{{margin:2px 0;color:var(--muted);font-size:14px}}
.eq-links{{display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:14px;margin-top:12px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column}}
.thumb{{aspect-ratio:16/9;background:#f3f0f6;display:flex;align-items:center;justify-content:center;border-bottom:1px solid var(--line)}}
.thumb img{{width:100%;height:100%;object-fit:contain;background:#fff;cursor:zoom-in}}
.thumb .ph{{font-size:13px;font-weight:700;color:var(--purple);letter-spacing:.06em;text-transform:uppercase;opacity:.65;text-align:center;padding:0 12px}}
.body{{padding:12px 14px 14px;display:flex;flex-direction:column;gap:6px;flex:1}}
.body .id{{font-size:12px;color:var(--muted);font-weight:600}}
.body h4{{margin:0;font-size:15.5px;line-height:1.3}}
.body .met{{font-size:13.5px}}
.body .fue{{font-size:12.5px;color:var(--muted)}}
.body .aviso{{font-size:12.5px;color:var(--bad);margin:0}}
.badges{{display:flex;gap:6px;flex-wrap:wrap;margin-top:auto;padding-top:6px;align-items:center}}
.badges a{{font-size:12.5px;margin-left:auto}}
.vacio{{padding:30px;text-align:center;color:var(--muted)}}
dialog{{border:none;border-radius:14px;padding:0;max-width:min(1100px,94vw)}}
dialog img{{display:block;max-width:100%;max-height:82vh}}
dialog::backdrop{{background:rgba(0,0,0,.6)}}
dialog p{{margin:0;padding:10px 14px;font-size:14px}}
footer{{margin-top:40px;color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding-top:16px}}
@media (max-width:640px){{.eq-head{{grid-template-columns:1fr}}.eq-links{{justify-content:flex-start}}.fila-f > span{{flex-basis:100%}}}}
</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <div>
    <div class="eyebrow">Data Visualization Team · Visual Modeling UPY</div>
    <h1>Catálogo de visualizaciones de los 9 equipos</h1>
    <p class="lead">Cada gráfica, mapa o escena 3D/AR que propuso cada equipo, con su fuente y su estado. Sirve para decidir qué entra al dashboard integrado y a la versión impresa. Corte: <b>{e(meta["fecha_corte"])}</b>.</p>
  </div>
  <div class="acciones">
    <a class="btn primario" href="catalogo_visualizaciones.pdf">Descargar PDF (borrador)</a>
    <a class="btn" href="imprimible.html">Versión imprimible</a>
    <a class="btn" href="../index.html">Proyecto del Equipo 2</a>
  </div>
</header>

<div class="kpis">
  <div class="kpi"><b>9</b><span>equipos revisados</span></div>
  <div class="kpi"><b>{tot["total"]}</b><span>visuales propuestos</span></div>
  <div class="kpi"><b>{tot["imagen"]}</b><span>ya tienen imagen generada</span></div>
  <div class="kpi"><b>{tot["interactivo"]}</b><span>son interactivos en código</span></div>
  <div class="kpi"><b>{tot["d_real"]}</b><span>usan datos de un archivo del repo</span></div>
</div>

<section class="bloque" aria-labelledby="t-matriz">
  <h2 id="t-matriz">Qué tipo de gráfica propone cada equipo</h2>
  <p class="nota">Número de visuales por tipo. Las columnas con varios equipos son candidatas a una sección común del dashboard integrado.</p>
  <div class="scroll">{matriz}</div>
</section>

<section class="bloque" aria-labelledby="t-filtros">
  <h2 id="t-filtros">Explorar</h2>
  <div class="filtros">
    <div class="fila-f"><span>Equipo</span><select id="f-eq"><option value="">Todos</option>{opts_eq}</select></div>
    <div class="fila-f"><span>Tipo</span>{chips("tipo", TIPOS, {})}</div>
    <div class="fila-f"><span>Estado</span>{chips("estado", ESTADOS, ETQ_ESTADO)}</div>
    <div class="fila-f"><span>Datos</span>{chips("datos", DATOS, ETQ_DATOS)}</div>
    <div class="fila-f"><span>Agrupar</span><div class="vista">
      <button type="button" class="chip" id="v-eq" aria-pressed="true">Por equipo</button>
      <button type="button" class="chip" id="v-tipo" aria-pressed="false">Por tipo de gráfica</button></div></div>
    <div id="conteo" aria-live="polite"></div>
  </div>
</section>

<main id="lista"></main>

<footer>
  <p><b>Cómo se hizo.</b> {e(meta["metodo"])}</p>
  <p><b>Datos:</b> «Datos del repo» = la gráfica lee un archivo del repositorio del equipo. «Cifras fijas» = los números están escritos a mano en el código o el README. «Simulados» = generados al azar o marcados como simulados. «Sin datos» = el equipo aún no tiene los datos.</p>
  <p>Las imágenes y capturas pertenecen a cada equipo y se muestran con crédito y enlace a su repositorio. Se generó con <code>scripts/generar_catalogo.py</code> desde <code>catalogo/catalogo_visualizaciones.json</code>.</p>
</footer>
</div>

<dialog id="zoom"><img alt=""><p></p></dialog>

<script>
const D = {datos_js};
const eqs = Object.fromEntries(D.equipos.map(t => [t.n, t]));
const f = {{eq: "", tipo: new Set(), estado: new Set(), datos: new Set(), vista: "eq"}};
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}}[c]));

function card(v) {{
  const t = eqs[v.eq];
  const th = v.img
    ? `<img src="${{esc(v.img)}}" alt="${{esc(v.titulo)}}" loading="lazy" data-cap="E${{v.eq}} · ${{esc(v.titulo)}}">`
    : `<div class="ph">${{esc(v.tipo)}}<br><small>${{esc(D.etqEstado[v.estado])}}</small></div>`;
  return `<article class="card"><div class="thumb">${{th}}</div><div class="body">
    <div class="id">Equipo ${{v.eq}} · ${{esc(v.id)}}${{f.vista === "tipo" ? " · " + esc(t.proyecto) : " · " + esc(v.tipo)}}</div>
    <h4>${{esc(v.titulo)}}</h4>
    <div class="met">${{esc(v.metrica)}}</div>
    <div class="fue">Fuente: ${{esc(v.fuente)}}</div>
    ${{v.nota ? `<p class="aviso">${{esc(v.nota)}}</p>` : ""}}
    <div class="badges"><span class="badge s-${{v.estado}}">${{esc(D.etqEstado[v.estado])}}</span>
      <span class="badge d-${{v.datos}}">${{esc(D.etqDatos[v.datos])}}</span>
      <a href="${{esc(v.url)}}" target="_blank" rel="noopener">Ver archivo</a></div>
  </div></article>`;
}}

function cabeceraEquipo(t, n) {{
  const links = [`<a class="btn" href="${{esc(t.repo)}}" target="_blank" rel="noopener">Repositorio</a>`];
  if (t.sitio) links.push(`<a class="btn" href="${{esc(t.sitio)}}" target="_blank" rel="noopener">Sitio publicado</a>`);
  return `<div class="eq-head"><div><h3>Equipo ${{t.n}} · ${{esc(t.proyecto)}}</h3>
    <p>${{esc(t.tema)}}</p><p>${{esc(t.integrantes)}} · Revisado en commit ${{esc(t.commit)}} · ${{n}} visuales</p></div>
    <div class="eq-links">${{links.join("")}}</div></div>`;
}}

function pasa(v) {{
  return (!f.eq || String(v.eq) === f.eq) && (!f.tipo.size || f.tipo.has(v.tipo))
    && (!f.estado.size || f.estado.has(v.estado)) && (!f.datos.size || f.datos.has(v.datos));
}}

function render() {{
  const vs = D.visuales.filter(pasa);
  document.getElementById("conteo").textContent = `${{vs.length}} de ${{D.visuales.length}} visuales`;
  const out = [];
  if (f.vista === "eq") {{
    for (const t of D.equipos) {{
      const g = vs.filter(v => v.eq === t.n);
      if (!g.length) continue;
      out.push(`<section class="equipo" id="eq${{t.n}}">${{cabeceraEquipo(t, g.length)}}<div class="grid">${{g.map(card).join("")}}</div></section>`);
    }}
  }} else {{
    for (const tp of D.tipos) {{
      const g = vs.filter(v => v.tipo === tp);
      if (!g.length) continue;
      const nEq = new Set(g.map(v => v.eq)).size;
      out.push(`<section class="equipo"><div class="eq-head"><div><h3>${{esc(tp)}}</h3><p>${{g.length}} visuales de ${{nEq}} equipo${{nEq > 1 ? "s" : ""}}</p></div></div><div class="grid">${{g.map(card).join("")}}</div></section>`);
    }}
  }}
  document.getElementById("lista").innerHTML = out.join("") || '<p class="vacio">Ningún visual cumple los filtros.</p>';
}}

document.getElementById("f-eq").addEventListener("change", ev => {{ f.eq = ev.target.value; render(); }});
document.querySelectorAll(".chip[data-grupo]").forEach(b => b.addEventListener("click", () => {{
  const s = f[b.dataset.grupo], val = b.dataset.valor;
  s.has(val) ? s.delete(val) : s.add(val);
  b.setAttribute("aria-pressed", s.has(val));
  render();
}}));
for (const [id, vista] of [["v-eq", "eq"], ["v-tipo", "tipo"]]) {{
  document.getElementById(id).addEventListener("click", () => {{
    f.vista = vista;
    document.getElementById("v-eq").setAttribute("aria-pressed", vista === "eq");
    document.getElementById("v-tipo").setAttribute("aria-pressed", vista === "tipo");
    render();
  }});
}}
const dlg = document.getElementById("zoom");
document.getElementById("lista").addEventListener("click", ev => {{
  const img = ev.target.closest(".thumb img");
  if (!img) return;
  dlg.querySelector("img").src = img.src;
  dlg.querySelector("img").alt = img.alt;
  dlg.querySelector("p").textContent = img.dataset.cap;
  dlg.showModal();
}});
dlg.addEventListener("click", () => dlg.close());
render();
</script>
</body>
</html>
"""


def pagina_imprimible(cat, equipos):
    por_eq, tot = resumen(cat)
    meta = cat["meta"]
    vis = cat["visuales"]

    filas_res = "".join(
        f'<tr><td>{t["n"]}</td><td><b>{e(t["proyecto"])}</b><br><span class="mut">{e(t["integrantes"])}</span></td>'
        f'<td>{por_eq[t["n"]]["total"]}</td><td>{por_eq[t["n"]]["imagen"]}</td><td>{por_eq[t["n"]]["interactivo"]}</td>'
        f'<td>{por_eq[t["n"]]["texto"] + por_eq[t["n"]]["candidato"]}</td><td>{por_eq[t["n"]]["d_real"]}</td></tr>'
        for t in cat["equipos"])

    tipos_txt = " · ".join(f"{tp}: {tot['t_' + tp]}" for tp in TIPOS if tot["t_" + tp])

    secciones = []
    for t in cat["equipos"]:
        g = [v for v in vis if v["eq"] == t["n"]]
        figs = [v for v in g if v.get("img") and v["datos"] == "real"]
        resto = [v for v in g if v not in figs]
        bloques_fig = "".join(
            f'<figure><img src="{e(v["img"])}" alt="{e(v["titulo"])}">'
            f'<figcaption><b>Equipo {t["n"]} · {e(v["id"])}. {e(v["titulo"])}.</b> {e(v["metrica"])}. '
            f'Fuente: {e(v["fuente"])}.</figcaption></figure>' for v in figs)
        if not figs:
            if t.get("captura"):
                bloques_fig = (f'<figure><img src="{e(t["captura"])}" alt="Captura del sitio del equipo {t["n"]}">'
                               f'<figcaption><b>Captura del sitio publicado del equipo {t["n"]}</b> ({e(t["sitio"])}), '
                               f'tomada el {e(meta["fecha_corte"])}. Se incluye como referencia de diseño; '
                               f'sus cifras no salen de un archivo de datos del repositorio.</figcaption></figure>')
            else:
                bloques_fig = '<p class="sinfig">El equipo todavía no tiene gráficas generadas. Abajo están las que propone y los indicadores con datos listos.</p>'
        tabla = ""
        if resto:
            tabla = ('<table class="lista"><thead><tr><th>Id</th><th>Visual propuesto</th><th>Tipo</th><th>Estado</th><th>Datos</th></tr></thead><tbody>'
                     + "".join(f'<tr><td>{e(v["id"])}</td><td>{e(v["titulo"])}<br><span class="mut">{e(v["metrica"])} · {e(v["fuente"])}</span></td>'
                               f'<td>{e(v["tipo"])}</td><td>{ETQ_ESTADO[v["estado"]]}</td><td><span class="badge d-{v["datos"]}">{ETQ_DATOS[v["datos"]]}</span></td></tr>'
                               for v in resto)
                     + "</tbody></table>")
        secciones.append(f"""
<section class="equipo">
  <div class="eq-tit"><span>Equipo {t["n"]}</span><h2>{e(t["proyecto"])}</h2></div>
  <p class="tema">{e(t["tema"])}</p>
  <p class="mut">{e(t["integrantes"])} · Repositorio: {e(t["repo"])} · Commit revisado: {e(t["commit"])}</p>
  <div class="figs">{bloques_fig}</div>
  {tabla}
</section>""")

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catálogo imprimible</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS_BASE}
@page{{size:letter;margin:16mm 15mm 18mm}}
body{{background:#fff;font-size:10.5pt}}
.hoja{{max-width:186mm;margin:0 auto;padding:0 16px}}
.mut{{color:var(--muted);font-size:9pt}}
.portada{{min-height:240mm;display:flex;flex-direction:column;justify-content:space-between;break-after:page;padding-top:18mm}}
.portada .eyebrow{{font-size:10pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-dark)}}
.portada h1{{font-size:32pt;line-height:1.05;margin:8mm 0 4mm;font-weight:800;color:var(--purple)}}
.portada .sub{{font-size:14pt;color:var(--muted);max-width:150mm}}
.borrador{{display:inline-block;border:2px solid var(--gold);color:var(--gold-dark);font-weight:800;padding:2mm 4mm;border-radius:3mm;letter-spacing:.1em;margin-top:6mm}}
.pie-portada{{display:flex;justify-content:space-between;align-items:flex-end;gap:10mm;border-top:3px solid var(--purple);padding-top:6mm}}
.qr{{text-align:center;font-size:8.5pt;color:var(--muted)}}
.qr svg{{width:32mm;height:32mm;display:block;margin:0 auto 2mm}}
h2{{font-size:17pt;margin:0}}
h3{{font-size:12.5pt;margin:6mm 0 2mm;color:var(--purple)}}
.resumen{{break-after:page}}
table{{border-collapse:collapse;width:100%;font-size:9.5pt}}
th,td{{border-bottom:1px solid var(--line);padding:1.8mm 2mm;text-align:left;vertical-align:top}}
thead th{{font-size:8.5pt;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}}
.res td:nth-child(n+3){{text-align:center}}
.equipo{{break-before:page}}
.eq-tit{{border-left:4mm solid var(--gold);padding-left:4mm}}
.eq-tit span{{font-size:9pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--gold-dark)}}
.tema{{font-size:11.5pt;margin:3mm 0 1mm}}
figure{{margin:5mm 0;break-inside:avoid}}
figure img{{width:100%;max-height:105mm;object-fit:contain;border:1px solid var(--line);border-radius:2mm}}
figcaption{{font-size:9pt;color:#333;margin-top:1.5mm}}
.sinfig{{background:#f6f3f8;border-radius:2mm;padding:4mm;color:var(--muted)}}
.lista{{margin-top:4mm}}
.lista td:first-child,.lista td:nth-child(3){{white-space:nowrap}}
.lista tr{{break-inside:avoid}}
.badge{{font-size:8pt}}
.metodo{{break-before:page}}
.metodo li{{margin:1.5mm 0}}
.supuesto{{background:var(--warn-bg);border-radius:2mm;padding:3mm 4mm;font-size:9.5pt}}
@media screen{{body{{background:#e9e9ee}}.hoja{{background:#fff;padding:16mm 15mm;margin:16px auto;box-shadow:0 4px 24px rgba(0,0,0,.08)}}}}
@media screen and (max-width:700px){{.hoja{{padding:16px}}.pie-portada{{flex-direction:column;align-items:flex-start}}}}
</style>
</head>
<body>
<div class="hoja">

<section class="portada">
  <div>
    <div class="eyebrow">Visual Modeling · UPY · Data Visualization Team</div>
    <h1>Catálogo de visualizaciones de los 9 equipos</h1>
    <p class="sub">Gráficas, mapas y escenas 3D/AR propuestas por cada equipo, con su fuente y la procedencia de sus datos. Base para la narrativa común del dashboard y de la versión impresa.</p>
    <div class="borrador">BORRADOR v0.1 · NO ES LA VERSIÓN FINAL</div>
  </div>
  <div class="pie-portada">
    <div>
      <p><b>Fecha de corte:</b> {e(meta["fecha_corte"])}<br>
      <b>Visuales registrados:</b> {tot["total"]} de 9 equipos<br>
      <b>Responsable del catálogo:</b> {e(meta["responsable"])}</p>
    </div>
    <div class="qr">{qr_svg(URL_CATALOGO)}Versión digital<br>{e(URL_CATALOGO.replace("https://", ""))}</div>
  </div>
</section>

<section class="resumen">
  <h2>Resumen</h2>
  <p>De {tot["total"]} visuales propuestos, <b>{tot["imagen"]}</b> ya tienen imagen generada, <b>{tot["interactivo"]}</b> son interactivos en código y <b>{tot["texto"] + tot["candidato"]}</b> solo están descritos o son indicadores con datos listos. <b>{tot["d_real"]}</b> usan datos de un archivo del repositorio del equipo; {tot["d_fijo"]} tienen cifras escritas a mano, {tot["d_simulado"]} usan datos simulados y {tot["d_sin_datos"]} aún no tienen datos.</p>
  <table class="res">
    <thead><tr><th>#</th><th>Proyecto</th><th>Visuales</th><th>Con imagen</th><th>Interactivos</th><th>Texto o candidato</th><th>Datos del repo</th></tr></thead>
    <tbody>{filas_res}</tbody>
  </table>
  <h3>Por tipo de gráfica</h3>
  <p>{e(tipos_txt)}</p>
  <h3>Cómo leer este documento</h3>
  <p>Cada equipo tiene su sección. Arriba van las gráficas que ya existen como imagen y usan datos reales; abajo, la tabla con el resto de sus propuestas. La columna «Datos» indica de dónde salen los números:</p>
  <p><span class="badge d-real">Datos del repo</span> lee un archivo del repositorio · <span class="badge d-fijo">Cifras fijas</span> números escritos a mano · <span class="badge d-simulado">Simulados</span> aleatorios o marcados como simulados · <span class="badge d-sin_datos">Sin datos</span> pendiente.</p>
</section>

{"".join(secciones)}

<section class="metodo">
  <h2>Método y pendientes</h2>
  <h3>Cómo se armó</h3>
  <p>{e(meta["metodo"])} El catálogo completo, con filtros, está en la versión digital (QR de la portada).</p>
  <h3>Pendientes para la versión final</h3>
  <ul>
    <li>Confirmar con el profesor el formato: reporte o póster, y el tamaño de impresión.</li>
    <li>Elegir con los equipos 1 y 2 de datos (Structured y Spatial) las gráficas que entran a la narrativa común, con sus KPI, filtros, unidades y fuentes.</li>
    <li>Regenerar las gráficas seleccionadas desde la misma versión aprobada del data warehouse que use el dashboard.</li>
    <li>Agregar contexto, metodología por indicador y conclusiones.</li>
    <li>Revisar la legibilidad a tamaño real impreso.</li>
    <li>Confirmar que se autoriza el QR al producto digital.</li>
  </ul>
  <p class="supuesto"><b>Supuestos de este borrador:</b> tamaño carta vertical; el QR apunta a {e(URL_CATALOGO)}, que solo funciona cuando este cambio se publique en la rama <code>main</code>; la fecha de corte es el día en que se revisaron los repositorios, no la fecha de los datos de cada gráfica.</p>
</section>

</div>
</body>
</html>
"""


def generar_pdf():
    js = os.path.join(RAIZ, "scripts", "imprimir_pdf.js")
    entrada = os.path.join(DIR, "imprimible.html")
    salida = os.path.join(DIR, "catalogo_visualizaciones.pdf")
    subprocess.run(["node", js, entrada, salida], check=True)
    print("PDF:", os.path.relpath(salida, RAIZ))


def main():
    cat, equipos = cargar()
    with open(os.path.join(DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina_web(cat, equipos))
    with open(os.path.join(DIR, "imprimible.html"), "w", encoding="utf-8") as f:
        f.write(pagina_imprimible(cat, equipos))
    _, tot = resumen(cat)
    print(f"{tot['total']} visuales · {tot['imagen']} con imagen · {tot['d_real']} con datos del repo")
    if "--pdf" in sys.argv:
        generar_pdf()


if __name__ == "__main__":
    main()
