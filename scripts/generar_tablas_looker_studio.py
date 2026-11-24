"""
Genera tablas planas (CSV) para Looker Studio en reports/looker_studio/, solo con datos reales.

    looker_01_precios_multicanal.csv     Tienditas (07-B) + Supermercados, Central de Abasto y
                                         Farmacias/Conveniencia (PROFECO QQP mayo 2026)
    looker_02_territorio_geo.csv         Mercados públicos (DENUE) y establecimientos PROFECO con coordenadas
    looker_03_lineas_pobreza_coneval.csv Serie mensual CONEVAL 2018-01 a 2025-03
    looker_04_ageb_censo2020_merida.csv  Indicadores por AGEB urbana de Mérida (Censo 2020)

Uso:
    python scripts/generar_tablas_looker_studio.py
"""
import json
import os
import sys

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "reports", "looker_studio")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analisis_profundo_22_fuentes import cargar_profeco  # noqa: E402


def guardar(df, nombre):
    df.to_csv(os.path.join(OUT, nombre), index=False, encoding="utf-8")
    print(f"[ok] reports/looker_studio/{nombre}: {len(df)} filas")


def tabla_precios():
    t = pd.read_csv(os.path.join(DATA, "fuente_b/07_bitacora_tienditas/bitacora_precios_tienditas.csv"))
    t = t.dropna(subset=["precio_observado_mxn"])
    tiend = pd.DataFrame({
        "canal": "Tiendita de esquina", "fuente": "Bitácora propia 07-B",
        "fecha": t.fecha_visita.str.slice(0, 10), "establecimiento": t.nombre_tiendita, "colonia_o_direccion": t.colonia,
        "producto": t.producto_auditado, "presentacion": t.marca_presentacion, "marca": "",
        "precio_mxn": t.precio_observado_mxn.astype(float)})
    p = cargar_profeco()
    canal = pd.Series("Otro", index=p.index)
    canal[p.giro == "Supermercado / Tienda de Autoservicio"] = "Supermercado"
    canal[p.cadena_comercial == "Central de Abasto"] = "Central de Abasto"
    canal[p.giro.isin(["Farmacias", "Tienda de Conveniencia"])] = "Farmacia / Conveniencia"
    canal[p.giro == "Mercados"] = "Mercado público"
    fecha = pd.to_datetime(p.fecha_registro, format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
    prof = pd.DataFrame({
        "canal": canal, "fuente": "PROFECO QQP mayo 2026", "fecha": fecha,
        "establecimiento": p.nombre_comercial, "colonia_o_direccion": p.direccion, "producto": p.producto,
        "presentacion": p.presentacion, "marca": p.marca, "precio_mxn": p.precio})
    prof = prof[prof.canal != "Otro"]
    guardar(pd.concat([tiend, prof], ignore_index=True), "looker_01_precios_multicanal.csv")


def tabla_territorio():
    filas = []
    g = json.load(open(os.path.join(DATA, "fuente_a/04_geoportal_merida/mercados_publicos_merida_denue.geojson"), encoding="utf-8"))
    for f in g["features"]:
        pr, (lon, lat) = f["properties"], f["geometry"]["coordinates"]
        filas.append({"tipo_nodo": "Mercado público (DENUE)", "nombre": pr["nombre"], "latitud": lat, "longitud": lon,
                      "establecimientos_denue": pr["establecimientos_denue"], "registros_profeco": None,
                      "fuente": "INEGI DENUE"})
    p = cargar_profeco()
    p = p[p.giro.isin(["Supermercado / Tienda de Autoservicio", "Central de Abasto", "Farmacias", "Tienda de Conveniencia",
                       "Mercados", "Tortillerías", "Panaderías", "Pescaderías"])]
    for (nom, gir, la, lo), grp in p.groupby(["nombre_comercial", "giro", "latitud", "longitud"]):
        filas.append({"tipo_nodo": f"Establecimiento PROFECO: {gir}", "nombre": nom, "latitud": la, "longitud": lo,
                      "establecimientos_denue": None, "registros_profeco": len(grp), "fuente": "PROFECO QQP mayo 2026"})
    d = pd.DataFrame(filas)
    d["coordenadas_looker"] = d.latitud.astype(str) + "," + d.longitud.astype(str)
    guardar(d, "looker_02_territorio_geo.csv")


def tabla_coneval():
    guardar(pd.read_csv(os.path.join(DATA, "fuente_a/03_siegy_yucatan/coneval_lineas_pobreza_2018_2025.csv")),
            "looker_03_lineas_pobreza_coneval.csv")


def tabla_ageb():
    ag = pd.read_csv(os.path.join(DATA, "fuente_b/03_conapo_marginacion/censo2020_indicadores_ageb_merida.csv"),
                     dtype={"LOC": str, "AGEB": str})
    guardar(ag[ag.POBTOT > 0], "looker_04_ageb_censo2020_merida.csv")


if __name__ == "__main__":
    for viejo in ["looker_01_comparativa_precios_multicanal.csv", "looker_02_territorio_mercados_tienditas_geo.csv",
                  "looker_03_salarios_esfuerzo_laboral_merida.csv"]:
        if os.path.exists(os.path.join(OUT, viejo)):
            os.remove(os.path.join(OUT, viejo))
    tabla_precios(); tabla_territorio(); tabla_coneval(); tabla_ageb()
