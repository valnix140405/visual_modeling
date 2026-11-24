"""
Genera las figuras de reports/figuras/ a partir de datos reales del repositorio.
Cada figura indica su fuente en el pie. Paleta del proyecto: oro #ed9f22, púrpura #600d8b.

Uso:
    python scripts/generar_graficas_analisis.py
"""
import glob
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ORO, PURPURA, NEGRO, GRIS, BLANCO = "#ed9f22", "#600d8b", "#0d0d0d", "#9ca3af", "#ffffff"
plt.rcParams.update({"figure.facecolor": BLANCO, "axes.facecolor": BLANCO, "font.family": "DejaVu Sans",
                     "axes.spines.top": False, "axes.spines.right": False, "text.parse_math": False})

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "reports", "figuras")
os.makedirs(OUT, exist_ok=True)

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analisis_profundo_22_fuentes import cargar_profeco, central_vs_super, comparar_tienditas  # noqa: E402


def guardar(fig, nombre, fuente):
    fig.text(0.01, 0.01, f"Fuente: {fuente}", fontsize=8, color="#525252")
    fig.savefig(os.path.join(OUT, nombre), dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[ok] reports/figuras/{nombre}")


CANASTA_FIG = {"Huevo": "Huevo", "Leche entera": "Leche Ultrapasteurizada", "Frijol": "Frijol", "Arroz": "Arroz",
               "Aceite": "Aceite", "Tortilla de maíz": "Tortilla de Maíz"}
CADENAS = ["Wal-mart", "Hipermercado Soriana", "Chedraui", "Bodega Aurrera", "Super Aki Xtra", "Dunosusa"]


def tabla_canasta_misma_presentacion():
    """Mediana por cadena usando, para cada producto, la misma presentación (la más frecuente en todo PROFECO)."""
    d = cargar_profeco()
    d = d[d.cadena_comercial.isin(CADENAS)]
    filas = []
    for item, prod in CANASTA_FIG.items():
        sub = d[d.producto == prod]
        pres = sub.presentacion.value_counts().index[0]
        for cad, g in sub[sub.presentacion == pres].groupby("cadena_comercial"):
            filas.append({"item": f"{item}\n{pres[:24]}", "cadena": cad, "mediana": g.precio.median(), "n": len(g)})
    return pd.DataFrame(filas)


def fig_canasta_cadenas():
    d = tabla_canasta_misma_presentacion()
    tabla = d.pivot_table(index="item", columns="cadena", values="mediana", sort=False)
    fig, ax = plt.subplots(figsize=(12, 5.5))
    colores = [PURPURA, ORO, "#9333ea", "#b45309", "#525252", "#d8b4fe"]
    tabla.plot.bar(ax=ax, color=colores[:tabla.shape[1]], width=0.8)
    ax.set_title("Mediana de precio por cadena en Mérida, misma presentación por producto (mayo 2026)", loc="left", fontsize=13)
    ax.set_ylabel("MXN"); ax.set_xlabel(""); ax.tick_params(axis="x", rotation=0, labelsize=8)
    ax.legend(frameon=False, fontsize=8, ncol=3)
    guardar(fig, "01_precios_canasta_por_cadena_profeco.png",
            "PROFECO QQP mayo 2026 (data/fuente_a/02_datos_gob_profeco/profeco_merida_2026_real.csv). Barra ausente = sin registro")


def fig_central_vs_super():
    j = central_vs_super(cargar_profeco())
    j = j[j.presentacion.str.contains("1 Kg")].sort_values("dif_pct", ascending=False).head(15)
    j["etiqueta"] = j.producto + " (" + j.presentacion.str.slice(0, 28) + ")"
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.barh(j.etiqueta[::-1], j.dif_pct[::-1], color=[ORO if v > 0 else PURPURA for v in j.dif_pct[::-1]])
    for y, (v, c, s) in enumerate(zip(j.dif_pct[::-1], j.central[::-1], j.super[::-1])):
        ax.text(v + 2, y, f"+{v:.0f}%  (${c:.1f} -> ${s:.1f})", va="center", fontsize=8)
    ax.set_title("Productos por kilo: cuánto más caro es el supermercado que la Central de Abasto", loc="left", fontsize=13)
    ax.set_xlabel("Diferencia de la mediana (%)")
    guardar(fig, "02_central_abasto_vs_supermercados_profeco.png",
            "PROFECO QQP mayo 2026, mismo producto y presentación (data/fuente_a/02_datos_gob_profeco/)")


def fig_coneval():
    lp = pd.read_csv(os.path.join(DATA, "fuente_a/03_siegy_yucatan/coneval_lineas_pobreza_2018_2025.csv"))
    lp["fecha"] = pd.to_datetime(lp.periodo)
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(lp.fecha, lp.lpei_canasta_alimentaria_urbana_mxn, color=ORO, lw=2.5, label="Canasta alimentaria urbana")
    ax.plot(lp.fecha, lp.lpi_alimentaria_mas_no_alimentaria_urbana_mxn, color=PURPURA, lw=2.5,
            label="Canasta alimentaria + no alimentaria urbana")
    for col, c in [("lpei_canasta_alimentaria_urbana_mxn", ORO), ("lpi_alimentaria_mas_no_alimentaria_urbana_mxn", PURPURA)]:
        ax.annotate(f"${lp[col].iloc[-1]:,.2f}", (lp.fecha.iloc[-1], lp[col].iloc[-1]), xytext=(5, 0),
                    textcoords="offset points", color=c, fontsize=9, va="center")
    ax.set_title("Valor mensual por persona de las líneas de pobreza por ingresos (zona urbana)", loc="left", fontsize=13)
    ax.set_ylabel("MXN por persona al mes"); ax.legend(frameon=False)
    guardar(fig, "03_lineas_pobreza_coneval_2018_2025.png",
            "CONEVAL, Líneas de pobreza por ingresos, ene 2018 a mar 2025 (data/fuente_a/03_siegy_yucatan/)")


def fig_tienditas():
    filas = pd.DataFrame(comparar_tienditas(cargar_profeco()))
    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(filas))
    ax.bar([i - 0.2 for i in x], filas.mediana_tiendita_mxn, 0.4, color=ORO, label="Tiendita de esquina (bitácora 07-B)")
    ax.bar([i + 0.2 for i in x], filas.mediana_supermercado_mxn, 0.4, color=PURPURA, label="Supermercado (PROFECO)")
    for i, r in filas.iterrows():
        ax.text(i - 0.2, r.mediana_tiendita_mxn + 1, f"n={r.registros_tiendita}", ha="center", fontsize=8)
        ax.text(i + 0.2, r.mediana_supermercado_mxn + 1, f"n={r.registros_supermercado}", ha="center", fontsize=8)
    ax.set_xticks(list(x)); ax.set_xticklabels(filas.producto, fontsize=9)
    ax.set_ylabel("Mediana MXN"); ax.legend(frameon=False)
    ax.set_title("Tiendita de esquina vs. supermercado: mediana de precio en Mérida", loc="left", fontsize=13)
    guardar(fig, "04_tienditas_vs_supermercados.png",
            "Bitácora propia 07-B (sep-oct 2026, 5 tiendas) y PROFECO QQP mayo 2026. Muestras de tienditas pequeñas")


def fig_ageb():
    ag = pd.read_csv(os.path.join(DATA, "fuente_b/03_conapo_marginacion/censo2020_indicadores_ageb_merida.csv"))
    ag = ag[ag.POBTOT > 0]
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.8))
    axs[0].hist(ag.pct_sin_afiliacion_salud.dropna(), bins=30, color=PURPURA)
    axs[0].set_title("% de población sin afiliación a servicios de salud", loc="left", fontsize=11)
    axs[1].hist(ag.pct_viviendas_con_internet.dropna(), bins=30, color=ORO)
    axs[1].set_title("% de viviendas con internet", loc="left", fontsize=11)
    for a in axs:
        a.set_ylabel("Número de AGEB")
    fig.suptitle(f"Distribución en las {len(ag)} AGEB urbanas habitadas de Mérida (Censo 2020)", x=0.01, ha="left", fontsize=13)
    guardar(fig, "05_indicadores_ageb_censo2020_merida.png",
            "INEGI, Censo de Población y Vivienda 2020, AGEB urbanas (data/fuente_b/03_conapo_marginacion/)")


def fig_relieve():
    t = pd.read_csv(os.path.join(DATA, "fuente_c/08_opentopography/topografia_merida_vs_ciudades_montana.csv"))
    orden = t.groupby("ciudad").elevacion_m_snm.median().sort_values().index
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.boxplot([t[t.ciudad == c].elevacion_m_snm for c in orden], tick_labels=list(orden), patch_artist=True,
               boxprops=dict(facecolor=ORO, color=NEGRO), medianprops=dict(color=PURPURA, lw=2), showfliers=False)
    ax.set_ylabel("Elevación (m s. n. m.)")
    ax.set_title("Elevación en una malla de 20 x 20 puntos (~17 km) alrededor de cada ciudad", loc="left", fontsize=13)
    guardar(fig, "06_relieve_merida_vs_ciudades_montana.png",
            "AWS Terrain Tiles (Tilezen) (data/fuente_c/08_opentopography/topografia_merida_vs_ciudades_montana.csv)")


if __name__ == "__main__":
    for viejo in glob.glob(os.path.join(OUT, "*.png")):
        os.remove(viejo)
    fig_canasta_cadenas(); fig_central_vs_super(); fig_coneval(); fig_tienditas(); fig_ageb(); fig_relieve()
