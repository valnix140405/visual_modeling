"""
Genera los datasets que reemplazan a los datos simulados del repositorio, a partir de
fuentes oficiales públicas. Todo es reproducible: el script descarga los originales a
una carpeta de caché (ignorada por git) y escribe los archivos derivados en data/.

Uso:
    python scripts/generar_datos_reales.py            # descarga (si falta) y genera todo
    python scripts/generar_datos_reales.py --cache /ruta/cache

Fuentes (URL oficial de descarga):
    INEGI DENUE Yucatán (edición 2026/05) ........ DENUE_URL
    INEGI Censos Económicos 2019, Yucatán ........ CE2019_URL
    INEGI Censo 2020, AGEB y manzana urbana ...... CENSO2020_URL
    CONEVAL Líneas de pobreza por ingresos ....... CONEVAL_URL
    AWS Terrain Tiles (Tilezen, formato Terrarium)  TERRAIN_URL
    PROFECO QQP (ya incluido en data/fuente_a/02_datos_gob_profeco/profeco_merida_2026_real.csv)
"""
import argparse
import csv
import io
import json
import math
import os
import urllib.request
import zipfile
from collections import Counter, defaultdict
from datetime import date

import pandas as pd
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

DENUE_URL = "https://www.inegi.org.mx/contenidos/masiva/denue/denue_31_csv.zip"
CE2019_URL = "https://www.inegi.org.mx/contenidos/programas/ce/2019/Datosabiertos/ce2019_yuc_csv.zip"
CENSO2020_URL = ("https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/"
                 "ageb_manzana/ageb_mza_urbana_31_cpv2020_csv.zip")
CONEVAL_URL = ("https://www.coneval.org.mx/Medicion/Documents/Lineas_de_Pobreza_por_Ingresos/"
               "Lineas_de_Pobreza_por_Ingresos.zip")
TERRAIN_URL = "https://elevation-tiles-prod.s3.amazonaws.com/terrarium/{z}/{x}/{y}.png"
PROFECO_CSV = os.path.join(DATA, "fuente_a/02_datos_gob_profeco/profeco_merida_2026_real.csv")

HOY = date.today().isoformat()


# ----------------------------------------------------------------------------- utilidades
def descargar(url, cache):
    os.makedirs(cache, exist_ok=True)
    destino = os.path.join(cache, url.rstrip("/").split("/")[-1])
    if not os.path.exists(destino):
        print(f"[descarga] {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (proyecto academico UPY)"})
        with urllib.request.urlopen(req, timeout=300) as r, open(destino, "wb") as f:
            f.write(r.read())
    return destino


def leer_csv_zip(ruta_zip, contiene, **kw):
    with zipfile.ZipFile(ruta_zip) as z:
        nombre = next(n for n in z.namelist() if contiene in n and n.endswith(".csv"))
        with z.open(nombre) as f:
            return pd.read_csv(f, dtype=str, index_col=False, **kw)


def escribir_geojson(ruta, nombre, features):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "name": nombre,
                   "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
                   "features": features}, f, ensure_ascii=False, indent=1)


def num(v):
    try:
        return float(str(v).strip())
    except (TypeError, ValueError):
        return None  # INEGI usa '*' o 'N/D' para valores reservados


def moda(valores):
    valores = [v for v in valores if v and str(v).strip() and str(v) != "nan"]
    return Counter(valores).most_common(1)[0][0] if valores else ""


# ----------------------------------------------------------------------------- DENUE
def cargar_denue_merida(cache):
    zp = descargar(DENUE_URL, cache)
    d = leer_csv_zip(zp, "denue_inegi_31", encoding="latin-1")
    d.columns = [c.strip() for c in d.columns]
    d = d[d["cve_mun"].astype(int) == 50].copy()
    d["lat"] = d["latitud"].astype(float)
    d["lon"] = d["longitud"].astype(float)
    return d


VARIANTES_MERCADO = [  # DENUE captura el nombre del centro a mano: se unifican variantes de escritura
    (("LUCAS", "LUCAZ"), "Mercado Lucas de Gálvez"), (("SAN BENITO",), "Mercado San Benito"),
    (("SANTIAGO",), "Mercado Santiago"), (("SEBASTIAN",), "Mercado de San Sebastián"),
    (("CHEN BECH", "CHENBECH"), "Mercado Chen Bech"), (("CHENKU",), "Mercado de Chenkú"),
    (("CHUBURNA",), "Mercado de Chuburná"), (("ALEMAN",), "Mercado de la Alemán"),
    (("MULSAY",), "Mercado Nueva Mulsay"), (("CORDEMEX",), "Mercado Cordemex"),
    (("GARCIA REJON",), "Mercado García Rejón"), (("CERVERA PACHECO",), "Mercado Víctor Cervera Pacheco"),
    (("CHETUMALITO",), "Mercado Ex Chetumalito"),
]


def normalizar_mercado(nombre):
    n = nombre.upper()
    for claves, canonico in VARIANTES_MERCADO:
        if any(c in n for c in claves):
            return canonico
    return nombre.title()


def capa_centros_comerciales(d, tipo, ruta, nombre_capa, etiqueta):
    sub = d[d["tipoCenCom"].fillna("").str.strip().str.upper() == tipo].copy()
    sub["nombre_norm"] = sub["nom_CenCom"].fillna("SIN NOMBRE").str.strip().map(normalizar_mercado)
    feats = []
    for i, (nom, g) in enumerate(sorted(sub.groupby("nombre_norm"),
                                        key=lambda t: -len(t[1])), start=1):
        alimentos = g["codigo_act"].str[:3].isin(["461", "311", "722"]).sum()
        feats.append({
            "type": "Feature",
            "properties": {
                "id": f"{etiqueta}-{i:02d}",
                "nombre": nom,
                "variantes_nombre_denue": "; ".join(sorted(g["nom_CenCom"].fillna("").str.strip().unique())),
                "tipo_centro_denue": tipo.title(),
                "colonia_principal": moda(g["nomb_asent"]).title(),
                "codigo_postal": moda(g["cod_postal"].str.replace(".0", "", regex=False)),
                "establecimientos_denue": int(len(g)),
                "establecimientos_alimentos_bebidas": int(alimentos),
                "giro_mas_frecuente": moda(g["nombre_act"]),
                "metodo_coordenada": "Mediana de las coordenadas de los establecimientos DENUE del centro",
                "fuente": "INEGI DENUE Yucatán, descarga masiva " + DENUE_URL,
                "fecha_extraccion": HOY,
            },
            "geometry": {"type": "Point",
                         "coordinates": [round(g["lon"].median(), 6), round(g["lat"].median(), 6)]},
        })
    escribir_geojson(ruta, nombre_capa, feats)
    print(f"[ok] {os.path.relpath(ruta, ROOT)}: {len(feats)} centros")


# ----------------------------------------------------------------------------- Censos Económicos
def saic_merida(cache, ruta):
    zp = descargar(CE2019_URL, cache)
    d = leer_csv_zip(zp, "conjunto_de_datos/ce2019_yuc", encoding="utf-8-sig")
    d.columns = [c.strip() for c in d.columns]
    for c in ["ENTIDAD", "MUNICIPIO", "CODIGO", "ID_ESTRATO"]:
        d[c] = d[c].fillna("").str.strip()
    d = d[(d.MUNICIPIO == "050") & (d.ID_ESTRATO == "")]
    d = d[d.CODIGO.str.match(r"^(461\d{3}|462\d{3}|4311\d{2})$")]
    with zipfile.ZipFile(zp) as z:
        cat_nombre = next(n for n in z.namelist() if "tc_codigo_actividad" in n)
        cat = pd.read_csv(z.open(cat_nombre), dtype=str, encoding="latin-1", index_col=False)
    cat.columns = [c.strip().upper() for c in cat.columns]
    col_cod = next(c for c in cat.columns if "CODIGO" in c)
    col_desc = next(c for c in cat.columns if c != col_cod)
    desc = dict(zip(cat[col_cod].str.strip(), cat[col_desc].str.strip()))
    out = pd.DataFrame({
        "cve_ent": "31", "cve_mun": "050", "municipio": "Mérida", "año_referencia_censo": "2018",
        "codigo_scian": d.CODIGO, "descripcion_actividad": d.CODIGO.map(desc),
        "unidades_economicas": d.UE, "personal_ocupado_total": d.H001A,
        "remuneraciones_totales_millones_mxn": d.J000A,
        "produccion_bruta_total_millones_mxn": d.A111A,
        "ingresos_suministro_bienes_servicios_millones_mxn": d.M000A,
    })
    out.to_csv(ruta, index=False, encoding="utf-8")
    print(f"[ok] {os.path.relpath(ruta, ROOT)}: {len(out)} clases SCIAN")


# ----------------------------------------------------------------------------- Censo 2020
COLS_AGEB = ["POBTOT", "PEA", "POCUPADA", "PDESOCUP", "PSINDER", "PDER_SS", "GRAPROES",
             "VIVPAR_HAB", "VPH_PISOTI", "VPH_NODREN", "VPH_REFRI", "VPH_AUTOM", "VPH_INTER"]


def censo_ageb_merida(cache, ruta_ageb, ruta_mun):
    zp = descargar(CENSO2020_URL, cache)
    d = leer_csv_zip(zp, "conjunto_de_datos_ageb_urbana", encoding="utf-8-sig")
    d = d[d.MUN == "050"]
    mun = d[(d.LOC == "0000") & (d.AGEB == "0000")]
    ageb = d[(d.AGEB != "0000") & (d.MZA == "000")].copy()
    out = ageb[["ENTIDAD", "MUN", "LOC", "NOM_LOC", "AGEB"] + COLS_AGEB].copy()
    for c in COLS_AGEB:
        out[c] = out[c].map(num)
    out["pct_sin_afiliacion_salud"] = (100 * out.PSINDER / out.POBTOT).round(2)
    out["pct_viviendas_piso_tierra"] = (100 * out.VPH_PISOTI / out.VIVPAR_HAB).round(2)
    out["pct_viviendas_sin_drenaje"] = (100 * out.VPH_NODREN / out.VIVPAR_HAB).round(2)
    out["pct_viviendas_con_internet"] = (100 * out.VPH_INTER / out.VIVPAR_HAB).round(2)
    out["pct_desocupacion"] = (100 * out.PDESOCUP / out.PEA).round(2)
    out.to_csv(ruta_ageb, index=False, encoding="utf-8")
    print(f"[ok] {os.path.relpath(ruta_ageb, ROOT)}: {len(out)} AGEB urbanas")
    m = mun[["ENTIDAD", "MUN", "NOM_MUN"] + COLS_AGEB].copy()
    m.to_csv(ruta_mun, index=False, encoding="utf-8")
    print(f"[ok] {os.path.relpath(ruta_mun, ROOT)}")


# ----------------------------------------------------------------------------- CONEVAL
def coneval_lineas(cache, ruta):
    import openpyxl
    zp = descargar(CONEVAL_URL, cache)
    with zipfile.ZipFile(zp) as z:
        nombre = next(n for n in z.namelist() if n.endswith(".xlsx"))
        wb = openpyxl.load_workbook(io.BytesIO(z.read(nombre)), read_only=True, data_only=True)
    ws = wb.worksheets[0]
    filas = []
    for row in ws.iter_rows(values_only=True):
        fecha = next((c for c in row if hasattr(c, "year")), None)
        if fecha is None:
            continue
        nums = [c for c in row[row.index(fecha) + 1:] if isinstance(c, (int, float))]
        if len(nums) >= 4 and fecha.year >= 2018:
            filas.append([fecha.strftime("%Y-%m"), *[round(v, 2) for v in nums[:4]]])
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["periodo", "lpei_canasta_alimentaria_rural_mxn", "lpei_canasta_alimentaria_urbana_mxn",
                    "lpi_alimentaria_mas_no_alimentaria_rural_mxn", "lpi_alimentaria_mas_no_alimentaria_urbana_mxn"])
        w.writerows(filas)
    print(f"[ok] {os.path.relpath(ruta, ROOT)}: {len(filas)} meses ({filas[0][0]} a {filas[-1][0]})")


# ----------------------------------------------------------------------------- PROFECO
def profeco_filtrado(ruta, cadenas=None, giros_contiene=None):
    d = pd.read_csv(PROFECO_CSV, dtype=str, encoding="utf-8-sig")
    m = pd.Series(False, index=d.index)
    if cadenas:
        m |= d.cadena_comercial.isin(cadenas)
    if giros_contiene:
        m |= d.giro.fillna("").str.contains(giros_contiene, case=False)
    d[m].to_csv(ruta, index=False, encoding="utf-8")
    print(f"[ok] {os.path.relpath(ruta, ROOT)}: {int(m.sum())} registros")


CANASTA = {  # item -> nombre exacto del producto en PROFECO QQP
    "Huevo": "Huevo", "Leche": "Leche Ultrapasteurizada", "Frijol": "Frijol", "Arroz": "Arroz",
    "Aceite": "Aceite", "Tortilla de maíz": "Tortilla de Maíz", "Pan de caja": "Pan de Caja",
    "Atún": "Atún", "Jitomate": "Jitomate", "Cebolla": "Cebolla", "Pollo": "Carne Pollo",
    "Carne de res": "Carne Res", "Manzana": "Manzana",
}


def resumen_supermercados(ruta):
    d = pd.read_csv(PROFECO_CSV, dtype=str, encoding="utf-8-sig")
    d["precio"] = d.precio.astype(float)
    cadenas = ["Wal-mart", "Hipermercado Soriana", "Chedraui", "Bodega Aurrera", "Super Aki Xtra", "Dunosusa"]
    filas = []
    for item, prod in CANASTA.items():
        sub = d[(d.producto == prod) & d.cadena_comercial.isin(cadenas)]
        for cad, g in sub.groupby("cadena_comercial"):
            pres = moda(g.presentacion)
            gp = g[g.presentacion == pres]
            filas.append([item, cad, "Mérida", prod, pres, round(gp.precio.mean(), 2), gp.precio.min(),
                          gp.precio.max(), len(gp), "PROFECO QQP mayo 2026 (registros de inspectores)"])
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["item_canasta", "cadena_comercial", "ciudad", "producto_profeco", "presentacion_mas_frecuente",
                    "precio_promedio_mxn", "precio_minimo_mxn", "precio_maximo_mxn", "registros", "fuente"])
        w.writerows(filas)
    print(f"[ok] {os.path.relpath(ruta, ROOT)}: {len(filas)} combinaciones producto-cadena")


# ----------------------------------------------------------------------------- Elevación
_tiles = {}


def _tile(z, x, y, cache):
    k = (z, x, y)
    if k not in _tiles:
        ruta = os.path.join(cache, "terrain", f"{z}_{x}_{y}.png")
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        if not os.path.exists(ruta):
            req = urllib.request.Request(TERRAIN_URL.format(z=z, x=x, y=y),
                                         headers={"User-Agent": "Mozilla/5.0 (proyecto academico UPY)"})
            with urllib.request.urlopen(req, timeout=60) as r, open(ruta, "wb") as f:
                f.write(r.read())
        _tiles[k] = Image.open(ruta).convert("RGB")
    return _tiles[k]


def elevacion(lat, lon, z, cache):
    n = 2 ** z
    xf = (lon + 180) / 360 * n
    yf = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    x, y = int(xf), int(yf)
    px, py = int((xf - x) * 256), int((yf - y) * 256)
    r, g, b = _tile(z, x, y, cache).getpixel((min(px, 255), min(py, 255)))
    return round(r * 256 + g + b / 256 - 32768, 2)


def malla(lat0, lat1, lon0, lon1, n, z, cache):
    pts = []
    for i in range(n):
        for j in range(n):
            la = lat0 + (lat1 - lat0) * i / (n - 1)
            lo = lon0 + (lon1 - lon0) * j / (n - 1)
            pts.append((i, j, la, lo, elevacion(la, lo, z, cache)))
    return pts


def pendientes(pts, n, lat0, lat1, lon0, lon1):
    dy = (lat1 - lat0) / (n - 1) * 111320
    dx = (lon1 - lon0) / (n - 1) * 111320 * math.cos(math.radians((lat0 + lat1) / 2))
    e = {(i, j): z for i, j, _, _, z in pts}
    res = {}
    for i, j, *_ in pts:
        gx = (e.get((i, j + 1), e[(i, j)]) - e.get((i, j - 1), e[(i, j)])) / (2 * dx)
        gy = (e.get((i + 1, j), e[(i, j)]) - e.get((i - 1, j), e[(i, j)])) / (2 * dy)
        res[(i, j)] = round(math.degrees(math.atan(math.hypot(gx, gy))), 2)
    return res


def escribir_ply(ruta, pts, lat0, lon0, comentario, z_exag=1.0):
    zs = [p[4] for p in pts]
    zmin, zmax = min(zs), max(zs)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("ply\nformat ascii 1.0\n")
        f.write(f"comment {comentario}\n")
        f.write("comment x,y en metros respecto a la esquina SO; z = elevacion real (m snm)\n")
        f.write(f"element vertex {len(pts)}\nproperty float x\nproperty float y\nproperty float z\n")
        f.write("property uchar red\nproperty uchar green\nproperty uchar blue\nend_header\n")
        for _, _, la, lo, z in pts:
            x = (lo - lon0) * 111320 * math.cos(math.radians(la))
            y = (la - lat0) * 111320
            t = 0 if zmax == zmin else (z - zmin) / (zmax - zmin)
            r, g, b = int(40 + 200 * t), int(120 + 80 * (1 - abs(t - 0.5) * 2)), int(200 * (1 - t) + 30)
            f.write(f"{x:.2f} {y:.2f} {z * z_exag:.2f} {r} {g} {b}\n")


def elevacion_centro(cache, ruta_csv, ruta_ply):
    # Malla de ~1.6 km x 1.6 km centrada en el Mercado Lucas de Gálvez (coordenada PROFECO/DENUE)
    lat_c, lon_c, n, z = 20.964175, -89.621197, 41, 15
    d = 0.0072
    lat0, lat1, lon0, lon1 = lat_c - d, lat_c + d, lon_c - d, lon_c + d
    pts = malla(lat0, lat1, lon0, lon1, n, z, cache)
    sl = pendientes(pts, n, lat0, lat1, lon0, lon1)
    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["celda_id", "fila", "columna", "latitud", "longitud", "elevacion_m_snm", "pendiente_grados",
                    "fuente", "zoom_tile"])
        for k, (i, j, la, lo, e) in enumerate(pts, 1):
            w.writerow([f"ELV-{k:04d}", i, j, round(la, 6), round(lo, 6), e, sl[(i, j)],
                        "AWS Terrain Tiles (Tilezen, Terrarium)", z])
    escribir_ply(ruta_ply, pts, lat0, lon0, "Elevacion real Centro de Merida (AWS Terrain Tiles) - Proyecto UPY")
    print(f"[ok] {os.path.relpath(ruta_csv, ROOT)} y .ply: {len(pts)} celdas")


CIUDADES = [  # bbox de ~17 km por lado alrededor de cada ciudad
    ("Mérida", "Yucatán", 20.8872, 21.0470, -89.7040, -89.5445),
    ("Ciudad de México", "CDMX", 19.3520, 19.5118, -99.2129, -99.0531),
    ("Monterrey", "Nuevo León", 25.6061, 25.7659, -100.3960, -100.2362),
    ("Toluca", "Estado de México", 19.2076, 19.3669, -99.7360, -99.5763),
    ("San Cristóbal de las Casas", "Chiapas", 16.6572, 16.8168, -92.7168, -92.5574),
    ("Guanajuato", "Guanajuato", 20.9391, 21.0989, -101.3369, -101.1770),
]


def topografia_ciudades(cache, ruta_csv, ruta_ply):
    n, z = 20, 12
    filas, pts_merida = [], None
    for ciudad, estado, la0, la1, lo0, lo1 in CIUDADES:
        pts = malla(la0, la1, lo0, lo1, n, z, cache)
        sl = pendientes(pts, n, la0, la1, lo0, lo1)
        for i, j, la, lo, e in pts:
            filas.append([ciudad, estado, round(la, 6), round(lo, 6), e, sl[(i, j)]])
        if ciudad == "Mérida":
            pts_merida = malla(la0, la1, lo0, lo1, 50, z, cache)
            bbox_m = (la0, lo0)
    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id_punto", "ciudad", "estado", "latitud", "longitud", "elevacion_m_snm", "pendiente_grados",
                    "fuente", "zoom_tile"])
        for k, r in enumerate(filas, 1):
            w.writerow([f"PNT-{k:05d}", *r, "AWS Terrain Tiles (Tilezen, Terrarium)", z])
    escribir_ply(ruta_ply, pts_merida, *bbox_m, "Relieve real de Merida 17 km x 17 km (AWS Terrain Tiles) - Proyecto UPY")
    print(f"[ok] {os.path.relpath(ruta_csv, ROOT)}: {len(filas)} puntos; .ply Mérida: {len(pts_merida)} puntos")


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=os.path.join(ROOT, ".cache_descargas"))
    a = ap.parse_args()
    p = lambda *x: os.path.join(DATA, *x)

    denue = cargar_denue_merida(a.cache)
    capa_centros_comerciales(denue, "MERCADO PUBLICO", p("fuente_a/04_geoportal_merida/mercados_publicos_merida_denue.geojson"),
                             "mercados_publicos_merida_denue", "MERC")
    saic_merida(a.cache, p("fuente_b/01_inegi_saic/censos_economicos_2019_merida_comercio_alimentos.csv"))
    censo_ageb_merida(a.cache, p("fuente_b/03_conapo_marginacion/censo2020_indicadores_ageb_merida.csv"),
                      p("fuente_a/03_siegy_yucatan/censo2020_totales_municipio_merida.csv"))
    coneval_lineas(a.cache, p("fuente_a/03_siegy_yucatan/coneval_lineas_pobreza_2018_2025.csv"))
    profeco_filtrado(p("fuente_b/02_datos_gob_sniim/profeco_central_abasto_merida_2026.csv"), cadenas=["Central de Abasto"])
    profeco_filtrado(p("fuente_b/06_scraping_farmacias/profeco_farmacias_conveniencia_merida_2026.csv"),
                     cadenas=["Oxxo", "7 Eleven"], giros_contiene="farmacia")
    resumen_supermercados(p("fuente_a/06_scraping_autoservicios/precios_canasta_supermercados_reales.csv"))
    elevacion_centro(a.cache, p("fuente_b/08_lidar_cem_mde/elevacion_centro_merida_grid.csv"),
                     p("fuente_b/08_lidar_cem_mde/elevacion_centro_merida.ply"))
    topografia_ciudades(a.cache, p("fuente_c/08_opentopography/topografia_merida_vs_ciudades_montana.csv"),
                        p("fuente_c/08_opentopography/relieve_merida_terrain_tiles.ply"))


if __name__ == "__main__":
    main()
