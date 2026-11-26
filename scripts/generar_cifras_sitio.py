"""
Genera data/web/cifras_sitio.csv: cada cifra que muestra index.html, calculada desde los archivos
del repositorio. index.html la lee con D3 y rellena los <span data-cifra="clave">.

Columnas: clave, valor, formato, descripcion, fuente, archivo_origen
Formatos: num | dec | dec2 | pesos | pesosEnteros | pct | pctEntero | pctSigno | pctSignoEntero | texto

Uso: python scripts/generar_cifras_sitio.py
(Requiere haber corrido antes scripts/generar_datos_booklet.py y scripts/generar_datos_web.py.)
"""
import json
import os

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda *p: os.path.join(ROOT, *p)  # noqa: E731
OUT = R("data", "web", "cifras_sitio.csv")

PROFECO = "PROFECO, Quién es Quién en los Precios, Mérida, mayo 2026"
filas = []


def cifra(clave, valor, formato, descripcion, fuente, archivo):
    filas.append({"clave": clave, "valor": valor, "formato": formato, "descripcion": descripcion,
                  "fuente": fuente, "archivo_origen": archivo})


def contar_filas(ruta, encoding="utf-8-sig"):
    with open(R(ruta), encoding=encoding, errors="ignore") as f:
        return sum(1 for _ in f) - 1


def main():
    # --------------------------------------------------------------- salario mínimo (CONASAMI)
    sm_ruta = "booklet/datos/unidad-salario-minimo.csv"
    sm = pd.read_csv(R(sm_ruta)).set_index("anio")
    sm25, sm26 = float(sm.loc[2025, "salario_minimo_diario_mxn"]), float(sm.loc[2026, "salario_minimo_diario_mxn"])
    dias_mes = int(sm.loc[2025, "dias_por_mes"])
    fuente_sm = "CONASAMI, Tabla de Salarios Mínimos Generales y Profesionales"
    cifra("salario_minimo_2025", sm25, "pesos", "Salario mínimo general diario 2025", fuente_sm, sm_ruta)
    cifra("salario_minimo_2026", sm26, "pesos", "Salario mínimo general diario 2026", fuente_sm, sm_ruta)
    # --------------------------------------------------------------- canasta (escena 1)
    # El salario que se usa es el del mismo año que la canasta (escena-1.csv: INEGI, último mes publicado).
    e1 = pd.read_csv(R("booklet/datos/escena-1.csv")).iloc[0]
    sm_usado = float(e1.salario_minimo_diario_mxn)
    anio = str(e1.corte).split()[-1]
    cifra("salario_minimo", sm_usado, "pesos", f"Salario mínimo general diario {anio} (mismo año que la canasta)", fuente_sm, sm_ruta)
    cifra("anio_salario", anio, "texto", "Año del salario mínimo y de la canasta", fuente_sm, "booklet/datos/escena-1.csv")
    cifra("corte_canasta", e1.corte, "texto", "Mes de la canasta alimentaria", "INEGI, Líneas de Pobreza", "booklet/datos/escena-1.csv")
    mensual = sm_usado * dias_mes
    cifra("salario_mensual", mensual, "pesosEnteros", f"Salario mínimo {anio} × 30 días", fuente_sm, sm_ruta)
    cifra("salario_mensual_x2", 2 * mensual, "pesosEnteros", f"Dos salarios mínimos mensuales {anio}", fuente_sm, sm_ruta)
    f1 = "INEGI, Líneas de Pobreza; INEGI Censo 2020; CONASAMI"
    cifra("canasta_persona", e1.canasta_persona_mxn, "pesos", f"Canasta alimentaria urbana por persona, {e1.corte}",
          "INEGI, Líneas de Pobreza", "booklet/datos/escena-1.csv")
    cifra("ocupantes", e1.ocupantes_por_vivienda, "dec2", "Promedio de ocupantes por vivienda en Mérida",
          "INEGI, Censo 2020", "booklet/datos/escena-1.csv")
    cifra("canasta_hogar", e1.canasta_hogar_mxn, "pesos", "Canasta del hogar al mes", f1, "booklet/datos/escena-1.csv")
    cifra("dias_canasta", e1.dias_canasta, "dec", "Días de salario mínimo para la canasta del hogar", f1,
          "booklet/datos/escena-1.csv")
    cifra("dias_canasta_redondo", e1.dias_canasta, "num", "Días de salario mínimo (redondeado)", f1,
          "booklet/datos/escena-1.csv")
    cifra("dias_canasta_indiv", e1.canasta_persona_mxn / sm_usado, "dec", "Días de salario mínimo para la canasta de una persona",
          f1, "booklet/datos/escena-1.csv")
    cifra("pct_sueldo_canasta", 100 * e1.canasta_hogar_mxn / mensual, "pct",
          "Parte del salario mínimo mensual que se lleva la canasta del hogar", f1, "booklet/datos/escena-1.csv")
    sobrante = mensual - e1.canasta_hogar_mxn
    cifra("sobrante_canasta", sobrante, "pesosEnteros", "Lo que sobra del salario mínimo tras la canasta", f1,
          "booklet/datos/escena-1.csv")

    # --------------------------------------------------------------- PROFECO general
    prof_ruta = "data/fuente_a/02_datos_gob_profeco/profeco_merida_2026_real.csv"
    prof = pd.read_csv(R(prof_ruta), encoding="utf-8-sig")
    cifra("profeco_registros", len(prof), "num", "Registros de precios PROFECO en Mérida", PROFECO, prof_ruta)
    tort = prof[(prof.producto == "Tortilla de Maíz") & (prof.giro == "Tortillerías")]
    tortilla = float(tort.precio.median())
    cifra("tortilla_kg", tortilla, "pesos", "Tortilla de maíz 1 kg en tortillerías (mediana)", PROFECO, prof_ruta)
    cifra("sobrante_kg_tortilla", sobrante / tortilla, "dec", "Kilos de tortilla que compra lo que sobra", PROFECO,
          prof_ruta)
    e2 = pd.read_csv(R("booklet/datos/escena-2.csv"))
    pollo = e2[(e2.producto == "Carne Pollo") & e2.presentacion.str.contains("Entero")].iloc[0]
    cifra("pollo_kg", pollo.precio_super_mxn, "pesos", "Pollo entero 1 kg en súper (mediana)", PROFECO,
          "booklet/datos/escena-2.csv")
    cifra("horas_pollo", pollo.precio_super_mxn / (sm26 / 8), "dec", "Horas de salario mínimo para 1 kg de pollo",
          PROFECO + "; CONASAMI", "booklet/datos/escena-2.csv")

    # --------------------------------------------------------------- Abasto vs súper (escena 2)
    a2 = "booklet/datos/escena-2.csv"
    cifra("abasto_pares", len(e2), "num", "Productos comparables Central de Abasto–súper", PROFECO, a2)
    mas = int((e2.diferencia_pct > 0).sum())
    cifra("abasto_mas_caro", mas, "num", "Productos más caros en el súper", PROFECO, a2)
    cifra("abasto_pct_mas_caro", 100 * mas / len(e2), "pct", "Porcentaje de productos más caros en el súper", PROFECO, a2)
    cifra("abasto_mediana", e2.diferencia_pct.median(), "pctSigno", "Diferencia mediana súper vs. Abasto", PROFECO, a2)
    ceb = e2[(e2.producto == "Cebolla") & e2.presentacion.str.contains("Blanca Sin Rabo")].iloc[0]
    cifra("cebolla_central", ceb.precio_central_mxn, "pesos", "Cebolla blanca en la Central de Abasto", PROFECO, a2)
    cifra("cebolla_super", ceb.precio_super_mxn, "pesos", "Cebolla blanca en el súper", PROFECO, a2)
    cifra("cebolla_dif", ceb.diferencia_pct, "pctSigno", "Diferencia de la cebolla", PROFECO, a2)
    cifra("cebolla_dif_entero", ceb.diferencia_pct, "pctSignoEntero", "Diferencia de la cebolla (entero)", PROFECO, a2)
    cifra("cebolla_kg_equivalentes", ceb.precio_super_mxn / ceb.precio_central_mxn, "dec",
          "Kilos de cebolla en el Abasto por el precio de 1 kg en el súper", PROFECO, a2)
    tor = e2[(e2.producto == "Tortilla de Maíz")].iloc[0]
    cifra("tortilla_super_mas_barata", -tor.diferencia_pct, "pctEntero",
          "Cuánto más barata es la tortilla en el súper que en el Abasto", PROFECO, a2)

    # --------------------------------------------------------------- conveniencia (escena 3)
    e3 = pd.read_csv(R("booklet/datos/escena-3.csv"))
    a3 = "booklet/datos/escena-3.csv"
    cifra("conv_pares", len(e3), "num", "Productos comparables conveniencia–súper", PROFECO, a3)
    cifra("conv_mas_cara", int((e3.diferencia_pct > 0).sum()), "num", "Productos más caros en conveniencia", PROFECO, a3)
    cifra("conv_mediana", e3.diferencia_pct.median(), "pctSigno", "Diferencia mediana conveniencia vs. súper", PROFECO, a3)
    for clave, prod, pres in [("suero", "Sueros Orales", "625"), ("agua1l", "Agua Sin Gas", "1 Lt"),
                              ("yoghurt", "Yoghurt", "220"), ("agua600", "Agua Sin Gas", "600")]:
        r = e3[(e3.producto == prod) & e3.presentacion.str.contains(pres)].iloc[0]
        cifra(f"{clave}_conv", r.precio_conveniencia_mxn, "pesos", f"{prod} {pres} en conveniencia", PROFECO, a3)
        cifra(f"{clave}_super", r.precio_super_mxn, "pesos", f"{prod} {pres} en súper", PROFECO, a3)
        cifra(f"{clave}_dif", r.diferencia_pct, "pctSigno", f"Diferencia {prod} {pres}", PROFECO, a3)
        cifra(f"{clave}_dif_entero", r.diferencia_pct, "pctSignoEntero", f"Diferencia {prod} {pres} (entero)", PROFECO, a3)

    # --------------------------------------------------------------- tienditas (escena 4)
    e4 = pd.read_csv(R("booklet/datos/escena-4.csv"))
    a4 = "booklet/datos/escena-4.csv"
    cifra("tienditas_n", int(e4.numero_tienditas.iloc[0]), "num", "Tienditas de la bitácora propia",
          "Bitácora propia 07-B", a4)
    cifra("tienditas_min_precios", int(e4.registros_tiendita.min()), "num", "Mínimo de precios por producto en tienditas",
          "Bitácora propia 07-B", a4)
    cifra("tienditas_max_precios", int(e4.registros_tiendita.max()), "num", "Máximo de precios por producto en tienditas",
          "Bitácora propia 07-B", a4)

    # --------------------------------------------------------------- relieve
    rel = pd.read_csv(R("data/fuente_c/08_opentopography/topografia_merida_vs_ciudades_montana.csv"))
    ar = "data/fuente_c/08_opentopography/topografia_merida_vs_ciudades_montana.csv"
    fr = "AWS Terrain Tiles (Tilezen, Terrarium)"
    m = rel[rel.ciudad == "Mérida"]
    cifra("merida_elev_min", m.elevacion_m_snm.min(), "dec", "Elevación mínima de Mérida (m)", fr, ar)
    cifra("merida_elev_max", m.elevacion_m_snm.max(), "num", "Elevación máxima de Mérida (m)", fr, ar)
    desnivel = m.elevacion_m_snm.max() - m.elevacion_m_snm.min()
    cifra("merida_desnivel", desnivel, "num", "Desnivel de Mérida (m)", fr, ar)
    cifra("merida_pendiente_mediana", m.pendiente_grados.median(), "dec2", "Pendiente mediana de Mérida (grados)", fr, ar)
    km = ((m.latitud.max() - m.latitud.min()) * 111.32
          + (m.longitud.max() - m.longitud.min()) * 111.32 * 0.9338) / 2  # cos(21°) ≈ 0.9338
    cifra("malla_km", km, "num", "Lado aproximado de la malla por ciudad (km)", fr, ar)
    sc = rel[rel.ciudad == "San Cristóbal de las Casas"]
    sc_des = sc.elevacion_m_snm.max() - sc.elevacion_m_snm.min()
    cifra("sclc_desnivel", sc_des, "num", "Desnivel de San Cristóbal de las Casas (m)", fr, ar)
    cifra("ciudades_puntos", len(rel), "num", "Puntos de elevación en 6 ciudades", fr, ar)
    cen_ruta = "data/fuente_b/08_lidar_cem_mde/elevacion_centro_merida_grid.csv"
    cen = pd.read_csv(R(cen_ruta))
    cifra("centro_puntos", len(cen), "num", "Puntos de la malla del Centro", fr, cen_ruta)
    cifra("centro_elev_min", cen.elevacion_m_snm.min(), "dec", "Elevación mínima del Centro (m)", fr, cen_ruta)
    cifra("centro_elev_max", cen.elevacion_m_snm.max(), "dec", "Elevación máxima del Centro (m)", fr, cen_ruta)
    medio = cen[(cen.fila == cen.fila.max() // 2) & (cen.columna == cen.columna.max() // 2)].iloc[0]
    cifra("lucas_elev", medio.elevacion_m_snm, "dec", "Elevación en el centro de la malla (Mercado Lucas de Gálvez)", fr,
          cen_ruta)
    lado_centro = (cen.latitud.max() - cen.latitud.min()) * 111.32
    cifra("centro_malla_km", lado_centro, "dec", "Lado de la malla del Centro (km)", fr, cen_ruta)
    ply = "data/fuente_c/08_opentopography/relieve_merida_terrain_tiles.ply"
    with open(R(ply), encoding="utf-8") as f:
        vert = next(int(l.split()[-1]) for l in f if l.startswith("element vertex"))
    cifra("merida_ply_puntos", vert, "num", "Puntos de la malla 3D de Mérida", fr, ply)

    # --------------------------------------------------------------- Va y Ven (OSM)
    vv_ruta = "data/fuente_c/04_transporte_vayven/export.geojson"
    g = json.load(open(R(vv_ruta), encoding="utf-8"))["features"]
    paradas = sum(1 for x in g if x["properties"].get("highway") == "bus_stop")
    rutas = sum(1 for x in g if x["properties"].get("type") == "route")
    osm = "OpenStreetMap (Overpass), ODbL"
    cifra("vayven_elementos", len(g), "num", "Elementos OSM del Va y Ven", osm, vv_ruta)
    cifra("vayven_paradas", paradas, "num", "Paradas", osm, vv_ruta)
    cifra("vayven_rutas", rutas, "num", "Rutas", osm, vv_ruta)
    cifra("vayven_otros", len(g) - paradas - rutas, "num", "Otros elementos", osm, vv_ruta)

    # --------------------------------------------------------------- catálogo y KPI
    den = "data/fuente_a/01_inegi_denue/denue_merida_alimentos_real.csv"
    cifra("denue_comercios", contar_filas(den), "num", "Comercios de alimentos en Mérida", "INEGI DENUE", den)
    hog = "data/fuente_c/01_enoe_microdatos/conjunto_de_datos_hog_enoe_2025_1t/conjunto_de_datos/conjunto_de_datos_hog_enoe_2025_1t.csv"
    viv = "data/fuente_c/01_enoe_microdatos/conjunto_de_datos_viv_enoe_2025_1t/conjunto_de_datos/conjunto_de_datos_viv_enoe_2025_1t.csv"
    n_hog, n_viv = contar_filas(hog), contar_filas(viv)
    cifra("enoe_registros", n_hog + n_viv, "num", "Registros ENOE de hogares y viviendas", "INEGI ENOE 2025 1T", hog)
    cifra("enoe_hogares", n_hog, "num", "Registros ENOE de hogares", "INEGI ENOE 2025 1T", hog)
    cifra("enoe_hog_mb", os.path.getsize(R(hog)) / 1e6, "dec", "Tamaño del CSV ENOE de hogares (MB)", "INEGI ENOE 2025 1T", hog)
    merc = "data/fuente_a/04_geoportal_merida/mercados_publicos_merida_denue.geojson"
    mg = json.load(open(R(merc), encoding="utf-8"))["features"]
    cifra("mercados_n", len(mg), "num", "Mercados públicos en el DENUE", "INEGI DENUE", merc)
    lucas = next(x["properties"] for x in mg if "Lucas" in x["properties"]["nombre"])
    cifra("lucas_establecimientos", lucas["establecimientos_denue"], "num", "Establecimientos del Mercado Lucas de Gálvez",
          "INEGI DENUE", merc)
    cifra("lucas_alimentos", lucas["establecimientos_alimentos_bebidas"], "num",
          "Establecimientos de alimentos y bebidas en Lucas de Gálvez", "INEGI DENUE", merc)
    for clave, ruta, desc, fuente in [
        ("canasta_cadenas_filas", "data/fuente_a/06_scraping_autoservicios/precios_canasta_supermercados_reales.csv",
         "Combinaciones producto-cadena", PROFECO),
        ("saic_clases", "data/fuente_b/01_inegi_saic/censos_economicos_2019_merida_comercio_alimentos.csv",
         "Clases SCIAN de comercio de alimentos", "INEGI, Censos Económicos 2019"),
        ("central_abasto_precios", "data/fuente_b/02_datos_gob_sniim/profeco_central_abasto_merida_2026.csv",
         "Precios PROFECO en la Central de Abasto", PROFECO),
        ("ageb_n", "data/fuente_b/03_conapo_marginacion/censo2020_indicadores_ageb_merida.csv",
         "AGEB urbanas de Mérida", "INEGI, Censo 2020"),
        ("farmacias_precios", "data/fuente_b/06_scraping_farmacias/profeco_farmacias_conveniencia_merida_2026.csv",
         "Precios en farmacias y conveniencia", PROFECO),
        ("diconsa_articulos", "data/fuente_c/02_diconsa_segalmex/DICONSA_8_Listado_de_articulos_por_proveedor.csv",
         "Artículos DICONSA", "DICONSA (datos.gob.mx)"),
    ]:
        cifra(clave, contar_filas(ruta, "latin-1" if "DICONSA" in ruta else "utf-8-sig"), "num", desc, fuente, ruta)
    cat = pd.read_csv(R("reports/looker_studio/looker_07_catalogo_fuentes.csv"))
    cifra("fuentes_dato_real", len(cat), "num", "Fuentes con dato real", "Catálogo de fuentes del equipo",
          "reports/looker_studio/looker_07_catalogo_fuentes.csv")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    df = pd.DataFrame(filas)
    df["valor"] = [v if f == "texto" else round(float(v), 4) for v, f in zip(df.valor, df.formato)]
    df.to_csv(OUT, index=False, encoding="utf-8")
    print(f"[ok] data/web/cifras_sitio.csv: {len(df)} cifras")


if __name__ == "__main__":
    main()
