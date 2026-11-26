"""
Genera tablas planas (CSV) para Looker Studio en reports/looker_studio/, solo con datos reales.

    looker_01_precios_multicanal.csv     Tienditas (07-B) + Supermercados, Central de Abasto y
                                         Farmacias/Conveniencia (PROFECO QQP mayo 2026)
    looker_02_territorio_geo.csv         Mercados públicos (DENUE) y establecimientos PROFECO con coordenadas
    looker_03_lineas_pobreza.csv         Serie mensual CONEVAL 2018-01 a 2025-03 + INEGI 2025-07 en adelante
    looker_04_ageb_censo2020_merida.csv  Indicadores por AGEB urbana de Mérida (Censo 2020)
    looker_05_comparables_por_canal.csv  Lo genera scripts/generar_datos_web.py (pares PROFECO por canal)
    looker_06_relieve_ciudades.csv       Elevación real de Mérida y 5 ciudades de montaña (08-C)
    looker_07_catalogo_fuentes.csv       Las 16 fuentes con dato real usadas en el dashboard
    looker_08_tienditas_vs_super.csv     4 productos equivalentes: bitácora 07-B vs. supermercados PROFECO

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
    # Serie continua: CONEVAL (2018-01 a 2025-03) + INEGI (2025-07 en adelante). Abril a junio de 2025 no tienen
    # boletín publicado; quedan como hueco, no se interpolan.
    con = pd.read_csv(os.path.join(DATA, "fuente_a/03_siegy_yucatan/coneval_lineas_pobreza_2018_2025.csv"))
    con["fuente"] = "CONEVAL"
    ine = pd.read_csv(os.path.join(DATA, "fuente_a/03_siegy_yucatan/inegi_lineas_pobreza_2025_2026.csv"))
    ine = ine[con.columns.drop("fuente").tolist()].assign(fuente="INEGI")
    guardar(pd.concat([con, ine], ignore_index=True), "looker_03_lineas_pobreza.csv")


def tabla_ageb():
    ag = pd.read_csv(os.path.join(DATA, "fuente_b/03_conapo_marginacion/censo2020_indicadores_ageb_merida.csv"),
                     dtype={"LOC": str, "AGEB": str})
    guardar(ag[ag.POBTOT > 0], "looker_04_ageb_censo2020_merida.csv")


def tabla_relieve():
    t = pd.read_csv(os.path.join(DATA, "fuente_c/08_opentopography/topografia_merida_vs_ciudades_montana.csv"))
    guardar(t, "looker_06_relieve_ciudades.csv")


FUENTES = [  # (id, tema, institución, archivo en data/, cobertura)
    ("01-A", "Comercios de alimentos", "INEGI DENUE", "fuente_a/01_inegi_denue/denue_merida_alimentos_real.csv", "Mérida, edición 2026"),
    ("01-B", "Censos Económicos (comercio de alimentos)", "INEGI", "fuente_b/01_inegi_saic/censos_economicos_2019_merida_comercio_alimentos.csv", "Mérida, año de referencia 2018"),
    ("01-C", "Microdatos de ocupación y empleo", "INEGI ENOE", "fuente_c/01_enoe_microdatos/conjunto_de_datos_hog_enoe_2025_1t/conjunto_de_datos/conjunto_de_datos_hog_enoe_2025_1t.csv", "Nacional, 2025 1T (tabla de hogares)"),
    ("02-A", "Precios al consumidor", "PROFECO QQP", "fuente_a/02_datos_gob_profeco/profeco_merida_2026_real.csv", "Mérida, mayo 2026"),
    ("02-B", "Precios en la Central de Abasto", "PROFECO QQP", "fuente_b/02_datos_gob_sniim/profeco_central_abasto_merida_2026.csv", "Mérida, mayo 2026"),
    ("02-C", "Artículos y proveedores", "DICONSA", "fuente_c/02_diconsa_segalmex/DICONSA_8_Listado_de_articulos_por_proveedor.csv", "Nacional, 1er semestre 2018"),
    ("03-A", "Líneas de pobreza por ingresos", "INEGI (antes CONEVAL)", "fuente_a/03_siegy_yucatan/inegi_lineas_pobreza_2025_2026.csv", "Nacional, 2025-07 a 2026-10 (CONEVAL 2018-2025 en serie aparte)"),
    ("03-B", "Indicadores por AGEB urbana", "INEGI Censo 2020", "fuente_b/03_conapo_marginacion/censo2020_indicadores_ageb_merida.csv", "Mérida, 2020"),
    ("03-C", "Inspección fitozoosanitaria", "SENASICA", "fuente_c/03_imss_boletin/01_actividades-inspeccion-movilizacion_2dotrim2025.csv", "Nacional, 2025 2T"),
    ("04-A", "Mercados públicos", "INEGI DENUE", "fuente_a/04_geoportal_merida/mercados_publicos_merida_denue.geojson", "Mérida, edición 2026"),
    ("04-C", "Rutas y paradas de transporte", "OpenStreetMap", "fuente_c/04_transporte_vayven/export.geojson", "Mérida, 2026-10-01"),
    ("06-A", "Precios de canasta por cadena", "PROFECO QQP", "fuente_a/06_scraping_autoservicios/precios_canasta_supermercados_reales.csv", "Mérida, mayo 2026"),
    ("06-B", "Precios en farmacias y conveniencia", "PROFECO QQP", "fuente_b/06_scraping_farmacias/profeco_farmacias_conveniencia_merida_2026.csv", "Mérida, mayo 2026"),
    ("07-B", "Bitácora de precios en tienditas", "Levantamiento propio", "fuente_b/07_bitacora_tienditas/bitacora_precios_tienditas.csv", "5 tienditas, sep-oct 2026"),
    ("08-B", "Elevación del Centro", "AWS Terrain Tiles", "fuente_b/08_lidar_cem_mde/elevacion_centro_merida_grid.csv", "Centro de Mérida"),
    ("08-C", "Relieve Mérida vs. ciudades de montaña", "AWS Terrain Tiles", "fuente_c/08_opentopography/topografia_merida_vs_ciudades_montana.csv", "6 ciudades"),
]


def tabla_tienditas():
    m = json.load(open(os.path.join(ROOT, "reports", "metricas_analisis.json"), encoding="utf-8"))
    t = pd.DataFrame(m["tienditas_vs_super"])
    t["fuente"] = "Bitácora propia 07-B (sep-oct 2026) y PROFECO QQP mayo 2026"
    guardar(t, "looker_08_tienditas_vs_super.csv")


def tabla_fuentes():
    filas = []
    for fid, tema, inst, archivo, cob in FUENTES:
        ruta = os.path.join(DATA, archivo)
        if archivo.endswith(".geojson"):
            n = len(json.load(open(ruta, encoding="utf-8"))["features"])
        else:
            with open(ruta, encoding="utf-8-sig", errors="ignore") as f:
                n = sum(1 for _ in f) - 1
        filas.append({"id": fid, "bloque": "Fuente " + fid[-1], "tema": tema, "institucion": inst,
                      "archivo": archivo.split("/")[-1], "registros": n, "cobertura": cob})
    guardar(pd.DataFrame(filas), "looker_07_catalogo_fuentes.csv")


if __name__ == "__main__":
    for viejo in ["looker_03_lineas_pobreza_coneval.csv", "looker_01_comparativa_precios_multicanal.csv", "looker_02_territorio_mercados_tienditas_geo.csv",
                  "looker_03_salarios_esfuerzo_laboral_merida.csv"]:
        if os.path.exists(os.path.join(OUT, viejo)):
            os.remove(os.path.join(OUT, viejo))
    tabla_precios(); tabla_territorio(); tabla_coneval(); tabla_ageb(); tabla_relieve(); tabla_fuentes(); tabla_tienditas()
