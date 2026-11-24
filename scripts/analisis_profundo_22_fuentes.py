"""
Análisis cruzado de las 22 fuentes del proyecto "Del Mundo a la Esquina: ¿Cuánto Cuesta Comer?".

Solo usa archivos reales del repositorio (ver data/*/README.md para la procedencia de cada uno).
No genera datos: calcula métricas y las guarda en reports/metricas_analisis.json, que es la
fuente de todas las cifras citadas en ANALISIS_PROFUNDO_22_FUENTES.md y
REPORTE_ANALISIS_PROFUNDO_22_FUENTES.md.

Uso:
    python scripts/analisis_profundo_22_fuentes.py
"""
import json
import os

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "reports", "metricas_analisis.json")


def ruta(*p):
    return os.path.join(DATA, *p)


def cargar_profeco():
    d = pd.read_csv(ruta("fuente_a/02_datos_gob_profeco/profeco_merida_2026_real.csv"), encoding="utf-8-sig")
    d["precio"] = d["precio"].astype(float)
    return d


# Productos comparables entre la bitácora de tienditas (07-B) y PROFECO (02-A).
# (etiqueta, producto PROFECO, presentación PROFECO, marca PROFECO o None, kg por unidad PROFECO,
#  producto en bitácora, texto que debe contener la marca/presentación en bitácora o None)
COMPARABLES_TIENDITA = [
    ("Leche entera LALA 1 L", "Leche Ultrapasteurizada", "Caja 1 Lt. Entera", "Lala", 1.0, "Leche entera", "LALA"),
    ("Pan blanco Bimbo grande", "Pan de Caja", "Paquete Grande 620 Gr. Rebanado Blanco", "Bimbo", 1.0, "Pan blanco", "BIMBO"),
    ("Tortilla de maíz 1 kg", "Tortilla de Maíz", "1 Kg. Granel", None, 1.0, "Tortilla de maiz", None),
    ("Frijol negro (precio por kg)", "Frijol", "Bolsa 900 Gr. Negro", None, 0.9, "Frijol negro", None),
]


def comparar_tienditas(prof):
    t = pd.read_csv(ruta("fuente_b/07_bitacora_tienditas/bitacora_precios_tienditas.csv"))
    sup = prof[prof.giro == "Supermercado / Tienda de Autoservicio"]
    filas = []
    for etiqueta, prod, pres, marca, k_prof, txt, marca_t in COMPARABLES_TIENDITA:
        f_sup = (sup.producto == prod) & (sup.presentacion == pres)
        if marca:
            f_sup &= sup.marca == marca
        p_sup = sup[f_sup].precio
        tt = t[t.producto_auditado == txt]
        if marca_t:
            tt = tt[tt.marca_presentacion.fillna("").str.contains(marca_t)]
        p_t = tt.precio_observado_mxn.dropna().astype(float)
        if p_sup.empty or p_t.empty:
            continue
        ms, mt = p_sup.median() / k_prof, p_t.median()
        filas.append({"producto": etiqueta, "mediana_tiendita_mxn": round(mt, 2),
                      "registros_tiendita": int(len(p_t)), "mediana_supermercado_mxn": round(ms, 2),
                      "registros_supermercado": int(len(p_sup)),
                      "diferencia_pct_tiendita_vs_super": round(100 * (mt / ms - 1), 1)})
    return filas


def central_vs_super(prof):
    ca = prof[prof.cadena_comercial == "Central de Abasto"]
    sup = prof[prof.giro == "Supermercado / Tienda de Autoservicio"]
    k = ["producto", "presentacion"]
    j = pd.concat([ca.groupby(k).precio.median().rename("central"),
                   sup.groupby(k).precio.median().rename("super")], axis=1).dropna().reset_index()
    j["dif_pct"] = 100 * (j.super / j.central - 1)
    return j


def main():
    m = {}
    prof = cargar_profeco()

    # 01-A DENUE
    denue = pd.read_csv(ruta("fuente_a/01_inegi_denue/denue_merida_alimentos_real.csv"), encoding="utf-8-sig")
    m["denue"] = {"establecimientos": int(len(denue)),
                  "top_actividades": denue.nombre_act.value_counts().head(5).to_dict(),
                  "pct_0_a_5_personas": round(100 * (denue.per_ocu == "0 a 5 personas").mean(), 1)}

    # 02-A PROFECO
    m["profeco"] = {"registros": int(len(prof)), "cadenas": int(prof.cadena_comercial.nunique()),
                    "establecimientos": int(prof.nombre_comercial.nunique()),
                    "fechas": sorted(prof.fecha_registro.unique().tolist())[:1] + sorted(prof.fecha_registro.unique().tolist())[-1:]}

    # 02-B Central de Abasto vs supermercados (ambos PROFECO, mismo producto y presentación)
    j = central_vs_super(prof)
    m["central_vs_super"] = {"pares_comparables": int(len(j)),
                             "pct_pares_super_mas_caro": round(100 * (j.dif_pct > 0).mean(), 1),
                             "mediana_dif_pct": round(j.dif_pct.median(), 1),
                             "mayores_diferencias": j.sort_values("dif_pct", ascending=False).head(5)
                             .assign(dif_pct=lambda x: x.dif_pct.round(1)).to_dict("records")}

    # 06-A canasta por cadena
    sc = pd.read_csv(ruta("fuente_a/06_scraping_autoservicios/precios_canasta_supermercados_reales.csv"))
    m["canasta_cadenas"] = {"combinaciones": int(len(sc)), "items": int(sc.item_canasta.nunique()),
                            "cadenas": sorted(sc.cadena_comercial.unique().tolist())}

    # 06-B farmacias y conveniencia
    fa = pd.read_csv(ruta("fuente_b/06_scraping_farmacias/profeco_farmacias_conveniencia_merida_2026.csv"))
    m["farmacias"] = {"registros": int(len(fa)), "cadenas": fa.cadena_comercial.value_counts().to_dict()}

    # 07-B tienditas vs supermercados
    m["tienditas_vs_super"] = comparar_tienditas(prof)

    # 03-A CONEVAL y Censo 2020 municipal
    lp = pd.read_csv(ruta("fuente_a/03_siegy_yucatan/coneval_lineas_pobreza_2018_2025.csv"))
    ini, fin = lp.iloc[0], lp.iloc[-1]
    col = "lpei_canasta_alimentaria_urbana_mxn"
    m["coneval"] = {"periodo_inicial": ini.periodo, "canasta_alimentaria_urbana_inicial": ini[col],
                    "periodo_final": fin.periodo, "canasta_alimentaria_urbana_final": fin[col],
                    "aumento_pct": round(100 * (fin[col] / ini[col] - 1), 1),
                    "lpi_urbana_final": fin.lpi_alimentaria_mas_no_alimentaria_urbana_mxn}
    mun = pd.read_csv(ruta("fuente_a/03_siegy_yucatan/censo2020_totales_municipio_merida.csv")).iloc[0]
    m["censo_municipio"] = {"poblacion": int(mun.POBTOT), "pea": int(mun.PEA), "ocupada": int(mun.POCUPADA),
                            "pct_sin_afiliacion_salud": round(100 * mun.PSINDER / mun.POBTOT, 1),
                            "grado_promedio_escolaridad": float(mun.GRAPROES),
                            "viviendas_habitadas": int(mun.VIVPAR_HAB),
                            "pct_viviendas_con_internet": round(100 * mun.VPH_INTER / mun.VIVPAR_HAB, 1)}

    # 03-B AGEB
    ag = pd.read_csv(ruta("fuente_b/03_conapo_marginacion/censo2020_indicadores_ageb_merida.csv"))
    ag = ag[ag.POBTOT > 0]
    s = ag.pct_sin_afiliacion_salud.dropna()
    m["ageb"] = {"ageb_con_poblacion": int(len(ag)), "sin_afiliacion_mediana": round(s.median(), 1),
                 "sin_afiliacion_p10": round(s.quantile(.1), 1), "sin_afiliacion_p90": round(s.quantile(.9), 1),
                 "ageb_mas_de_40pct_sin_afiliacion": int((s > 40).sum()),
                 "internet_mediana": round(ag.pct_viviendas_con_internet.dropna().median(), 1)}

    # 01-B Censos Económicos 2019
    ce = pd.read_csv(ruta("fuente_b/01_inegi_saic/censos_economicos_2019_merida_comercio_alimentos.csv"),
                     dtype={"codigo_scian": str})
    ab = ce[ce.codigo_scian == "461110"].iloc[0]
    su = ce[ce.codigo_scian == "462111"]
    m["censos_economicos"] = {
        "abarrotes_unidades": int(ab.unidades_economicas), "abarrotes_personal": int(ab.personal_ocupado_total),
        "abarrotes_ingresos_mdp": float(ab.ingresos_suministro_bienes_servicios_millones_mxn),
        "supermercados_unidades": int(su.unidades_economicas.iloc[0]) if len(su) else None,
        "supermercados_personal": int(su.personal_ocupado_total.iloc[0]) if len(su) else None,
        "supermercados_ingresos_mdp": float(su.ingresos_suministro_bienes_servicios_millones_mxn.iloc[0]) if len(su) else None,
    }

    # 04-A mercados públicos
    mer = json.load(open(ruta("fuente_a/04_geoportal_merida/mercados_publicos_merida_denue.geojson"), encoding="utf-8"))
    mp = [f["properties"] for f in mer["features"]]
    m["mercados"] = {"mercados": len(mp), "establecimientos_total": sum(p["establecimientos_denue"] for p in mp),
                     "top": [(p["nombre"], p["establecimientos_denue"]) for p in mp[:3]]}

    # 04-C Va y Ven (OSM)
    vv = json.load(open(ruta("fuente_c/04_transporte_vayven/export.geojson"), encoding="utf-8"))
    m["vayven"] = {"elementos": len(vv["features"]),
                   "paradas": sum(1 for f in vv["features"] if f["properties"].get("highway") == "bus_stop"),
                   "rutas": sum(1 for f in vv["features"] if f["properties"].get("route") == "bus")}

    # 02-C DICONSA
    di = pd.read_csv(ruta("fuente_c/02_diconsa_segalmex/DICONSA_8_Listado_de_articulos_por_proveedor.csv"),
                     encoding="utf-8-sig", encoding_errors="replace")
    m["diconsa"] = {"registros": int(len(di))}

    # 08-B / 08-C relieve
    el = pd.read_csv(ruta("fuente_b/08_lidar_cem_mde/elevacion_centro_merida_grid.csv"))
    m["elevacion_centro"] = {"celdas": int(len(el)), "min_m": float(el.elevacion_m_snm.min()),
                             "max_m": float(el.elevacion_m_snm.max()),
                             "pendiente_mediana_grados": float(el.pendiente_grados.median())}
    to = pd.read_csv(ruta("fuente_c/08_opentopography/topografia_merida_vs_ciudades_montana.csv"))
    g = to.groupby("ciudad").agg(elev_media=("elevacion_m_snm", "mean"), desnivel=("elevacion_m_snm", lambda x: x.max() - x.min()),
                                 pendiente_mediana=("pendiente_grados", "median")).round(1)
    m["relieve_ciudades"] = g.reset_index().to_dict("records")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print(json.dumps(m, ensure_ascii=False, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    print(f"\n[ok] Métricas guardadas en {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
