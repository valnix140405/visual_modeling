"""
Ilustraciones narrativas (con humor) para el sitio, el PDF y Looker Studio (como imagen).

Genera en reports/figuras/narrativas/ (PNG 1600x900 y SVG):
    n1_merida_plana_precios_no   Perfil real de Mérida vs. "montaña" de sobreprecios súper/Abasto
    n2_calendario_canasta        Días de salario mínimo que se lleva la canasta de un hogar
    n3_tortillometro             Kilos de tortilla que compra un día de salario mínimo
    n4_cebolla_llorona           Cebolla en la Central de Abasto vs. en el súper
    n5_impuesto_flojera          Conveniencia vs. súper, los 6 productos con mayor diferencia
    n6_david_vs_goliat           Tiendita vs. súper en 4 productos equivalentes

Todas las cifras se calculan aquí a partir de archivos del repositorio.
Uso: python scripts/generar_graficas_narrativas.py
"""
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib import patches  # noqa: E402
from matplotlib import text as mtext  # noqa: E402

# Los precios llevan "$": sin esto matplotlib los interpreta como fórmulas (mathtext).
_texto_init = mtext.Text.__init__


def _texto_sin_mathtext(self, *a, **k):
    k.setdefault("parse_math", False)
    _texto_init(self, *a, **k)


mtext.Text.__init__ = _texto_sin_mathtext

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, *p)  # noqa: E731
OUT = D("reports", "figuras", "narrativas")
os.makedirs(OUT, exist_ok=True)

MORADO, ORO, GRIS, GRIS_CLARO, TINTA = "#600d8b", "#ed9f22", "#8a8a8a", "#e6e6e6", "#1a1a1a"
plt.rcParams.update({"font.family": ["Inter", "DejaVu Sans"], "font.size": 13, "svg.fonttype": "none"})

# Salario mínimo general diario por año (CONASAMI), leído del CSV común del booklet.
_sm = pd.read_csv(D("booklet/datos/unidad-salario-minimo.csv")).set_index("anio").salario_minimo_diario_mxn
# Los precios de PROFECO son de mayo 2026 y la canasta de INEGI de 2026: se usa el salario de 2026.
SALARIO_MINIMO = float(_sm.loc[2026])
CORTE = "Corte de datos: 24 nov 2026"

# ----------------------------------------------------------------------------- datos
comp = pd.read_csv(D("reports/looker_studio/looker_05_comparables_por_canal.csv"))
abasto = comp[comp.canal_comparado == "Central de Abasto"].sort_values("diferencia_pct", ascending=False)
conv = comp[comp.canal_comparado == "Conveniencia"].sort_values("diferencia_pct", ascending=False)
tiend = pd.read_csv(D("reports/looker_studio/looker_08_tienditas_vs_super.csv"))
coneval = pd.read_csv(D("data/fuente_a/03_siegy_yucatan/inegi_lineas_pobreza_2025_2026.csv"))  # INEGI, último mes
censo = pd.read_csv(D("data/fuente_a/03_siegy_yucatan/censo2020_totales_municipio_merida.csv")).iloc[0]
profeco = pd.read_csv(D("data/fuente_a/02_datos_gob_profeco/profeco_merida_2026_real.csv"), encoding="utf-8-sig")
relieve = pd.read_csv(D("data/fuente_c/08_opentopography/topografia_merida_vs_ciudades_montana.csv"))

ocupantes = float(censo.PROM_OCUP)                                   # 3.27 (Censo 2020)
ult = coneval.iloc[-1]
canasta_persona = float(ult.lpei_canasta_alimentaria_urbana_mxn)    # INEGI, último mes publicado
canasta_hogar = canasta_persona * ocupantes
dias_canasta = canasta_hogar / SALARIO_MINIMO
tortilla = profeco[(profeco.producto == "Tortilla de Maíz") & (profeco.giro == "Tortillerías")]
precio_tortilla = float(tortilla.precio.median())                   # $29.50/kg
kg_tortilla_dia = SALARIO_MINIMO / precio_tortilla
merida = relieve[relieve.ciudad == "Mérida"]
desnivel_merida = merida.elevacion_m_snm.max() - merida.elevacion_m_snm.min()
cebolla = abasto[(abasto.producto == "Cebolla") & (abasto.presentacion.str.contains("Sin Rabo"))].iloc[0]
mediana_abasto = abasto.diferencia_pct.median()
pct_mas_caro = 100 * (abasto.diferencia_pct > 0).mean()

CIFRAS = {
    "canasta_persona": canasta_persona, "ocupantes": ocupantes, "canasta_hogar": canasta_hogar,
    "dias_canasta": dias_canasta, "precio_tortilla": precio_tortilla, "kg_tortilla_dia": kg_tortilla_dia,
    "desnivel_merida": desnivel_merida, "cebolla_abasto": cebolla.precio_canal_comparado_mxn,
    "cebolla_super": cebolla.precio_supermercado_mxn, "cebolla_dif": cebolla.diferencia_pct,
    "mediana_abasto": mediana_abasto, "pct_mas_caro": pct_mas_caro, "pares_abasto": len(abasto),
}


def mx(v, d=2):
    return f"${v:,.{d}f}"


def lienzo():
    fig = plt.figure(figsize=(16, 9), dpi=100, facecolor="white")
    return fig


def encabezado(fig, titulo, subtitulo, pie):
    fig.text(0.05, 0.92, titulo, fontsize=34, fontweight="bold", color=TINTA, va="top")
    fig.text(0.05, 0.835, subtitulo, fontsize=16, color="#404040", va="top", wrap=True)
    import textwrap
    pie_txt = "\n".join(textwrap.wrap(f"Fuente: {pie}. {CORTE}.", 150))
    fig.text(0.05, 0.03, pie_txt, fontsize=10.5, color=GRIS, va="bottom", linespacing=1.4)
    fig.text(0.95, 0.075, "Del Mundo a la Esquina · UPY", fontsize=11, color=MORADO, ha="right", va="bottom",
             fontweight="bold")


def guardar(fig, nombre):
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, f"{nombre}.{ext}"), dpi=100, facecolor="white")
    plt.close(fig)
    print(f"[ok] reports/figuras/narrativas/{nombre}.png/.svg")


# ----------------------------------------------------------------------------- n1
def n1():
    fig = lienzo()
    encabezado(fig, "Mérida es plana. Sus precios, no.",
               f"El terreno sube {desnivel_merida:.1f} m en 17 km. En el súper, el mismo producto sube hasta "
               f"+{cebolla.diferencia_pct:.0f} % frente a la Central de Abasto.",
               "AWS Terrain Tiles (relieve de Mérida, 08-C); PROFECO QQP Mérida, mayo 2026 (139 productos)")
    ax = fig.add_axes([0.05, 0.12, 0.9, 0.66])
    # "Montaña" de diferencias (solo las positivas, ordenadas de menor a mayor y reflejadas como cerro)
    pos = abasto[abasto.diferencia_pct > 0].sort_values("diferencia_pct").reset_index(drop=True)
    n = len(pos)
    izq = pos.iloc[::2].diferencia_pct.tolist()
    der = pos.iloc[1::2].diferencia_pct.tolist()[::-1]
    cerro = izq + der
    xs = [i / (len(cerro) - 1) * 100 for i in range(len(cerro))]
    ax.fill_between(xs, 0, cerro, color=MORADO, alpha=0.88, linewidth=0)
    # perfil real de Mérida: elevación promedio por columna de la malla (oeste -> este), en la misma escala (m = %)
    perfil = merida.groupby("longitud").elevacion_m_snm.mean().sort_index()
    base = perfil - perfil.min()
    xp = [i / (len(base) - 1) * 100 for i in range(len(base))]
    ax.fill_between(xp, 0, base.values, color=GRIS, alpha=0.9, linewidth=0, zorder=3)
    ax.plot(xp, base.values, color="#555555", linewidth=2, zorder=4)
    # etiquetas de picos
    top = pos.sort_values("diferencia_pct", ascending=False).head(3)
    for k, (_, r) in enumerate(top.iterrows()):
        i = cerro.index(r.diferencia_pct)
        ax.annotate(f"{r.producto} +{r.diferencia_pct:.0f} %", (xs[i], r.diferencia_pct),
                    xytext=(64, 192 - k * 17), textcoords="data", ha="left", va="center", fontsize=14,
                    fontweight="bold", color=MORADO,
                    arrowprops=dict(arrowstyle="-", color=MORADO, lw=1, shrinkA=2, shrinkB=3))
    ax.annotate(f"Mérida de verdad: {desnivel_merida:.1f} m de desnivel\n(apenas se ve)", (6, base.max()),
                xytext=(6, 55), textcoords="data", fontsize=14, color="#333333",
                arrowprops=dict(arrowstyle="->", color="#333333"))
    ax.text(97, 120, f"El «cerro» del súper:\n{n} de {len(abasto)} productos más caros\nque en la Central de Abasto\n"
                     f"(mediana +{mediana_abasto:.1f} %)", ha="right", va="top", fontsize=14, color=MORADO)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, max(cerro) * 1.2)
    ax.set_xticks([])
    ax.set_ylabel("metros de desnivel  ·  % de sobreprecio", color=GRIS)
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=GRIS)
    guardar(fig, "n1_merida_plana_precios_no")


# ----------------------------------------------------------------------------- n2
def n2():
    fig = lienzo()
    libres = 30 - dias_canasta
    encabezado(fig, f"Te quedan {libres:.0f} días… para todo lo demás",
               f"Alimentar a un hogar de Mérida ({ocupantes:.2f} personas) con la canasta de INEGI cuesta "
               f"{mx(canasta_hogar)} al mes: {dias_canasta:.1f} días de salario mínimo.",
               f"INEGI, Líneas de Pobreza, canasta alimentaria urbana {ult.periodo} ({mx(canasta_persona)} por persona); INEGI Censo 2020; "
               f"CONASAMI, salario mínimo 2026 ({mx(SALARIO_MINIMO)}/día)")
    ax = fig.add_axes([0.05, 0.1, 0.62, 0.68])
    ax.set_xlim(0, 7)
    ax.set_ylim(-5, 0.6)
    ax.axis("off")
    dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    for j, d in enumerate(dias):
        ax.text(j + 0.5, 0.3, d, ha="center", fontsize=13, color=GRIS, fontweight="bold")
    for k in range(30):
        f, c = divmod(k, 7)
        relleno = min(1.0, max(0.0, dias_canasta - k))  # fracción del día que se va en comida
        x0, y0 = c + 0.06, -f - 0.94
        ax.add_patch(patches.FancyBboxPatch((x0, y0), 0.88, 0.88, boxstyle="round,pad=0,rounding_size=0.08",
                                            facecolor=ORO, edgecolor="white", linewidth=2))
        if relleno > 0:
            ax.add_patch(patches.FancyBboxPatch((x0, y0), 0.88 * relleno, 0.88,
                                                boxstyle="round,pad=0,rounding_size=0.08",
                                                facecolor=MORADO, edgecolor="white", linewidth=2))
        ax.text(x0 + 0.1, y0 + 0.72, str(k + 1), fontsize=12, color="white", fontweight="bold")
    fig.text(0.71, 0.66, f"{dias_canasta:.1f}", fontsize=80, fontweight="bold", color=MORADO, va="center")
    fig.text(0.71, 0.55, "días para la comida del hogar", fontsize=17, color=MORADO)
    fig.text(0.71, 0.42, f"{libres:.1f}", fontsize=56, fontweight="bold", color=ORO, va="center")
    fig.text(0.71, 0.29, "días para renta, luz, transporte,\nescuela, salud…", fontsize=15, color="#7a5208")
    guardar(fig, "n2_calendario_canasta")


# ----------------------------------------------------------------------------- n3
def n3():
    fig = lienzo()
    encabezado(fig, "Tu sueldo, en kilos de tortilla",
               f"Un día de salario mínimo ({mx(SALARIO_MINIMO)}) alcanza para {kg_tortilla_dia:.1f} kg de "
               f"tortilla de tortillería ({mx(precio_tortilla)}/kg).",
               "PROFECO QQP Mérida, mayo 2026 (mediana en tortillerías); CONASAMI, salario mínimo 2026")
    ax = fig.add_axes([0.05, 0.1, 0.5, 0.7])
    ax.set_xlim(-3, 3)
    enteros = int(kg_tortilla_dia)
    frac = kg_tortilla_dia - enteros
    alto = 0.55
    ax.set_ylim(-0.6, (enteros + 2) * alto)
    ax.axis("off")
    for k in range(enteros + (1 if frac > 0 else 0)):
        ancho = 4.2 if k < enteros else 4.2 * frac
        y = k * alto
        ax.add_patch(patches.Ellipse((0, y), ancho, 0.62, facecolor="#f1d48a", edgecolor="#b8862b", linewidth=2.5))
        ax.add_patch(patches.Ellipse((0, y + 0.05), ancho * 0.8, 0.4, facecolor="none", edgecolor="#d9b56a",
                                     linewidth=1.2, linestyle=(0, (2, 3))))
        ax.text(2.4, y, f"{k + 1} kg" if k < enteros else f"+{frac:.1f}", va="center", fontsize=13, color=GRIS)
    ax.text(0, -0.55, "(cada disco = 1 kg)", ha="center", fontsize=12, color=GRIS)
    # comparativa: canasta del hogar en kilos de tortilla
    kg_canasta = canasta_hogar / precio_tortilla
    fig.text(0.6, 0.66, f"{kg_tortilla_dia:.1f} kg", fontsize=72, fontweight="bold", color=ORO, va="center")
    fig.text(0.6, 0.56, "de tortilla por un día de trabajo", fontsize=17, color="#7a5208")
    fig.text(0.6, 0.42, f"La canasta mensual de un hogar\nequivale a {kg_canasta:,.0f} kg de tortilla.",
             fontsize=19, color=MORADO, fontweight="bold", va="top")
    fig.text(0.6, 0.27, "Suficiente para envolver muchos tacos…\npero no para pagar la renta.", fontsize=15,
             color="#404040", va="top")
    guardar(fig, "n3_tortillometro")


# ----------------------------------------------------------------------------- n4
def dibujar_cebolla(ax, cx, cy, r, color_cuerpo, lagrimas):
    ax.add_patch(patches.Ellipse((cx, cy), 2 * r, 2.15 * r, facecolor=color_cuerpo, edgecolor="#8c6a9e",
                                 linewidth=3))
    for dx in (-0.45, 0, 0.45):
        ax.plot([cx + dx * r * 0.6, cx + dx * r], [cy - r, cy + r * 0.95], color="#b79cc6", linewidth=1.5)
    ax.add_patch(patches.Polygon([[cx - 0.12 * r, cy + r * 1.02], [cx, cy + r * 1.55], [cx + 0.12 * r, cy + r * 1.02]],
                                 facecolor="#6aa84f", edgecolor="#4a7f35"))
    # ojos
    for dx in (-0.32, 0.32):
        ax.add_patch(patches.Circle((cx + dx * r, cy + 0.2 * r), 0.07 * r, color=TINTA))
    # lágrimas: una gota por cada 25 % de diferencia (mínimo 0)
    for k in range(lagrimas):
        lado = -1 if k % 2 == 0 else 1
        y = cy + 0.05 * r - (k // 2) * 0.33 * r
        x = cx + lado * 0.42 * r
        ax.add_patch(patches.Ellipse((x, y), 0.1 * r, 0.18 * r, color="#4aa3df", alpha=0.85))


def n4():
    fig = lienzo()
    kg_abasto = SALARIO_MINIMO / cebolla.precio_canal_comparado_mxn
    kg_super = SALARIO_MINIMO / cebolla.precio_supermercado_mxn
    encabezado(fig, "Hasta la cebolla llora",
               f"El mismo kilo de cebolla blanca: {mx(cebolla.precio_canal_comparado_mxn)} en la Central de Abasto, "
               f"{mx(cebolla.precio_supermercado_mxn)} en el súper (+{cebolla.diferencia_pct:.1f} %).",
               f"PROFECO QQP Mérida, mayo 2026 (medianas: {int(cebolla.registros_canal_comparado)} registros en el "
               f"Abasto, {int(cebolla.registros_supermercado)} en súper); CONASAMI, salario mínimo 2026")
    ax = fig.add_axes([0.05, 0.1, 0.9, 0.7])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 7)
    ax.set_aspect("equal")
    ax.axis("off")
    dibujar_cebolla(ax, 4, 3.6, 1.7, "#f3e9f7", 0)
    dibujar_cebolla(ax, 12, 3.6, 1.7, "#e9d7f3", min(10, round(cebolla.diferencia_pct / 25)))
    for cx, lbl, precio, kg, col in ((4, "Central de Abasto", cebolla.precio_canal_comparado_mxn, kg_abasto, ORO),
                                     (12, "Supermercado", cebolla.precio_supermercado_mxn, kg_super, MORADO)):
        ax.text(cx, 6.65, lbl, ha="center", fontsize=20, fontweight="bold", color=col)
        ax.text(cx, 1.15, f"{mx(precio)}/kg", ha="center", fontsize=26, fontweight="bold", color=col)
        ax.text(cx, 0.45, f"Un día de salario mínimo = {kg:.1f} kg", ha="center", fontsize=15, color="#404040")
    ax.text(8, 3.6, f"+{cebolla.diferencia_pct:.0f} %", ha="center", va="center", fontsize=34, fontweight="bold",
            color=MORADO)
    ax.annotate("", xy=(9.9, 3.0), xytext=(6.1, 3.0), arrowprops=dict(arrowstyle="-|>", color=MORADO, lw=3))
    ax.text(8, 2.4, "(una lágrima por cada 25 %)", ha="center", fontsize=12, color=GRIS)
    guardar(fig, "n4_cebolla_llorona")


# ----------------------------------------------------------------------------- n5
def n5():
    top = conv.head(6).iloc[::-1]
    fig = lienzo()
    mejor = conv.iloc[0]
    encabezado(fig, "El impuesto a la flojera",
               f"Lo que cuesta no caminar dos cuadras más: el suero oral cuesta +{mejor.diferencia_pct:.1f} % en la tienda "
               f"de conveniencia.\nPero en la mediana de {len(conv)} productos la diferencia es de solo "
               f"+{conv.diferencia_pct.median():.1f} %.",
               "PROFECO QQP Mérida, mayo 2026. Conveniencia = OXXO, 7 Eleven y Dunosusa; promedios con 3 o más registros")
    ax = fig.add_axes([0.36, 0.17, 0.58, 0.55])
    for i, (_, r) in enumerate(top.iterrows()):
        ax.plot([r.precio_supermercado_mxn, r.precio_canal_comparado_mxn], [i, i], color=GRIS_CLARO, lw=8,
                solid_capstyle="round", zorder=1)
        ax.scatter(r.precio_supermercado_mxn, i, s=380, color=MORADO, zorder=3)
        ax.scatter(r.precio_canal_comparado_mxn, i, s=380, color=ORO, zorder=3)
        ax.text(r.precio_supermercado_mxn - 0.6, i, mx(r.precio_supermercado_mxn), ha="right", va="center",
                fontsize=12, color=MORADO)
        ax.text(r.precio_canal_comparado_mxn + 0.6, i, f"{mx(r.precio_canal_comparado_mxn)}  (+{r.diferencia_pct:.0f} %)",
                ha="left", va="center", fontsize=13, color="#7a5208", fontweight="bold")
        etiqueta = f"{r.producto}\n{r.presentacion[:46]}"
        fig.text(0.05, 0.17 + (i + 0.5) / len(top) * 0.55, etiqueta, fontsize=12, va="center", color=TINTA)
    ax.set_ylim(-0.5, len(top) - 0.5)
    ax.set_xlim(top.precio_supermercado_mxn.min() - 5, top.precio_canal_comparado_mxn.max() + 12)
    ax.set_yticks([])
    ax.set_xlabel("Precio promedio (MXN)", color=GRIS)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=GRIS)
    fig.text(0.36, 0.735, "●", color=MORADO, fontsize=16)
    fig.text(0.38, 0.738, "Supermercado", fontsize=13, color=MORADO)
    fig.text(0.50, 0.735, "●", color=ORO, fontsize=16)
    fig.text(0.52, 0.738, "Tienda de conveniencia", fontsize=13, color="#7a5208")
    guardar(fig, "n5_impuesto_flojera")


# ----------------------------------------------------------------------------- n6
def n6():
    fig = lienzo()
    gana = tiend[tiend.diferencia_pct_tiendita_vs_super < 0]
    encabezado(fig, "David contra Goliat en la esquina",
               f"La tiendita le gana al súper en {len(gana)} de {len(tiend)} productos: "
               + ", ".join(f"{p.split(' ')[0].lower()} {d:+.1f} %" for p, d in
                           zip(gana.producto, gana.diferencia_pct_tiendita_vs_super))
               + ". En lo demás, el gigante cobra menos.",
               "Bitácora propia 07-B (5 tienditas, 26 sep–1 oct 2026) y PROFECO QQP mayo 2026. "
               "Muestra pequeña: 2 a 5 precios por producto en tienditas")
    ax = fig.add_axes([0.05, 0.08, 0.9, 0.72])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.axis("off")
    # David: tiendita
    ax.add_patch(patches.Rectangle((0.4, 4.6), 2.2, 1.6, facecolor="#fdf3e3", edgecolor=ORO, lw=3))
    ax.add_patch(patches.Polygon([[0.2, 6.2], [1.5, 7.0], [2.8, 6.2]], facecolor=ORO))
    ax.add_patch(patches.Rectangle((1.2, 4.6), 0.6, 0.9, facecolor=ORO))
    ax.text(1.5, 4.2, "Tiendita", ha="center", fontsize=16, fontweight="bold", color="#7a5208")
    # Goliat: súper
    ax.add_patch(patches.Rectangle((13.0, 3.7), 2.8, 3.4, facecolor="#efe3f6", edgecolor=MORADO, lw=3))
    ax.add_patch(patches.Rectangle((13.0, 6.7), 2.8, 0.5, facecolor=MORADO))
    ax.text(14.4, 6.93, "SÚPER", ha="center", va="center", fontsize=15, fontweight="bold", color="white")
    for x in (13.3, 14.1, 14.9):
        ax.add_patch(patches.Rectangle((x, 5.2), 0.6, 0.8, facecolor="white", edgecolor=MORADO))
    ax.add_patch(patches.Rectangle((14.0, 3.7), 0.8, 1.1, facecolor=MORADO))
    ax.text(14.4, 3.3, "Supermercado", ha="center", fontsize=16, fontweight="bold", color=MORADO)
    # marcador por producto
    filas = tiend.reset_index(drop=True)
    for i, r in filas.iterrows():
        y = 6.6 - i * 1.55
        gana_t = r.diferencia_pct_tiendita_vs_super < 0
        col = ORO if gana_t else MORADO
        ax.text(8, y + 0.32, r.producto, ha="center", fontsize=15, fontweight="bold", color=TINTA)
        ax.text(5.2, y - 0.25, mx(r.mediana_tiendita_mxn), ha="center", fontsize=17, color="#7a5208",
                fontweight="bold" if gana_t else "normal")
        ax.text(10.8, y - 0.25, mx(r.mediana_supermercado_mxn), ha="center", fontsize=17, color=MORADO,
                fontweight="normal" if gana_t else "bold")
        veredicto = "gana la tiendita" if gana_t else "gana el súper"
        ax.text(8, y - 0.25, f"{r.diferencia_pct_tiendita_vs_super:+.1f} %  ·  {veredicto}", ha="center",
                fontsize=13, color=col)
        ax.text(8, y - 0.68, f"({int(r.registros_tiendita)} precios en tienditas, {int(r.registros_supermercado)} en súper)",
                ha="center", fontsize=10.5, color=GRIS)
    guardar(fig, "n6_david_vs_goliat")


if __name__ == "__main__":
    for k, v in CIFRAS.items():
        print(f"  {k}: {v:,.2f}")
    n1(); n2(); n3(); n4(); n5(); n6()
