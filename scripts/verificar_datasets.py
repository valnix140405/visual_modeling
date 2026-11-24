"""
Script maestro de diagnostico y resumen de los 22 datasets activos del proyecto (Fuentes A, B y C).
Excluye las fuentes PNT (05-A, 05-B, 05-C) y conserva unicamente 07-B en Self-Produced.
"""
import os
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")

FUENTES = [
    # FUENTE A (7 fuentes)
    {"num": "01-A", "grupo": "Fuente A", "tema": "INEGI / DENUE", "folder": "fuente_a/01_inegi_denue", "archivo": "denue_merida_alimentos_real.csv", "tipo": "CSV Oficial INEGI", "desc": "7,520 comercios de alimentos en Mérida (DENUE)"},
    {"num": "02-A", "grupo": "Fuente A", "tema": "datos.gob / PROFECO", "folder": "fuente_a/02_datos_gob_profeco", "archivo": "profeco_merida_2026_real.csv", "tipo": "CSV Oficial PROFECO", "desc": "28,288 precios QQP en Mérida (mayo 2026)"},
    {"num": "03-A", "grupo": "Fuente A", "tema": "CONEVAL + Censo 2020", "folder": "fuente_a/03_siegy_yucatan", "archivo": "coneval_lineas_pobreza_2018_2025.csv", "tipo": "CSV Oficial CONEVAL", "desc": "Líneas de pobreza 2018-01 a 2025-03 + totales Censo 2020 Mérida (SIEGY pendiente)"},
    {"num": "04-A", "grupo": "Fuente A", "tema": "Mercados públicos (DENUE)", "folder": "fuente_a/04_geoportal_merida", "archivo": "mercados_publicos_merida_denue.geojson", "tipo": "GeoJSON derivado INEGI", "desc": "15 mercados públicos de Mérida derivados de DENUE"},
    {"num": "06-A", "grupo": "Fuente A", "tema": "Precios autoservicios (PROFECO)", "folder": "fuente_a/06_scraping_autoservicios", "archivo": "precios_canasta_supermercados_reales.csv", "tipo": "CSV derivado PROFECO", "desc": "62 combinaciones producto-cadena (13 alimentos, 6 cadenas, misma presentación)"},
    {"num": "08-A", "grupo": "Fuente A", "tema": "LiDAR 3D", "folder": "fuente_a/08_lidar_mercado", "archivo": None, "tipo": "-", "desc": "Pendiente: no hay nube LiDAR real disponible del Mercado Lucas de Gálvez"},
    {"num": "09-A", "grupo": "Fuente A", "tema": "AR Geospatial", "folder": "fuente_a/09_ar_anclas", "archivo": "spatial_anchors_merida.geojson", "tipo": "GeoJSON (diseño propio)", "desc": "Configuración de anclas AR elaborada por el equipo"},

    # FUENTE B (8 fuentes)
    {"num": "01-B", "grupo": "Fuente B", "tema": "INEGI / Censos Económicos", "folder": "fuente_b/01_inegi_saic", "archivo": "censos_economicos_2019_merida_comercio_alimentos.csv", "tipo": "CSV Oficial INEGI", "desc": "CE2019 Mérida: 32 clases SCIAN de comercio de alimentos"},
    {"num": "02-B", "grupo": "Fuente B", "tema": "PROFECO Central de Abasto", "folder": "fuente_b/02_datos_gob_sniim", "archivo": "profeco_central_abasto_merida_2026.csv", "tipo": "CSV Oficial PROFECO", "desc": "776 precios QQP en la Central de Abasto de Mérida (SNIIM pendiente)"},
    {"num": "03-B", "grupo": "Fuente B", "tema": "INEGI Censo 2020 AGEB", "folder": "fuente_b/03_conapo_marginacion", "archivo": "censo2020_indicadores_ageb_merida.csv", "tipo": "CSV Oficial INEGI", "desc": "526 AGEB urbanas de Mérida con indicadores de rezago"},
    {"num": "04-B", "grupo": "Fuente B", "tema": "Tianguis (Geoportal)", "folder": "fuente_b/04_tianguis_geoportal", "archivo": None, "tipo": "-", "desc": "Pendiente: capa de tianguis del Geoportal no accesible"},
    {"num": "06-B", "grupo": "Fuente B", "tema": "Farmacias/conveniencia (PROFECO)", "folder": "fuente_b/06_scraping_farmacias", "archivo": "profeco_farmacias_conveniencia_merida_2026.csv", "tipo": "CSV Oficial PROFECO", "desc": "5,864 precios QQP en 11 cadenas de farmacias y conveniencia"},
    {"num": "07-B", "grupo": "Fuente B", "tema": "Self-Produced", "folder": "fuente_b/07_bitacora_tienditas", "archivo": "bitacora_precios_tienditas.csv", "tipo": "CSV Auditoría", "desc": "Levantamiento propio en 5 tienditas de esquina de Mérida"},
    {"num": "08-B", "grupo": "Fuente B", "tema": "Elevación Centro", "folder": "fuente_b/08_lidar_cem_mde", "archivo": "elevacion_centro_merida_grid.csv", "tipo": "CSV Malla elevación", "desc": "1,681 celdas de elevación real alrededor de Lucas de Gálvez (AWS Terrain Tiles)"},
    {"num": "09-B", "grupo": "Fuente B", "tema": "AR Geospatial", "folder": "fuente_b/09_ar_modelos_3d", "archivo": "catalogo_modelos_3d_canasta.json", "tipo": "JSON (diseño propio)", "desc": "Catálogo de modelos 3D elaborado por el equipo"},

    # FUENTE C (7 fuentes)
    {"num": "01-C", "grupo": "Fuente C", "tema": "INEGI / ENOE", "folder": "fuente_c/01_enoe_microdatos", "archivo": "0_indice_tablas_enoe_2025_1t.csv", "tipo": "Microdatos INEGI", "desc": "Microdatos ENOE 2025 1T Hogares/Viviendas y catálogos"},
    {"num": "02-C", "grupo": "Fuente C", "tema": "SEGALMEX / DICONSA", "folder": "fuente_c/02_diconsa_segalmex", "archivo": "DICONSA_8_Listado_de_articulos_por_proveedor.csv", "tipo": "CSV Oficial DICONSA", "desc": "4,064 artículos y proveedores Diconsa"},
    {"num": "03-C", "grupo": "Fuente C", "tema": "Inspección / Sanidad", "folder": "fuente_c/03_imss_boletin", "archivo": "01_actividades-inspeccion-movilizacion_2dotrim2025.csv", "tipo": "CSV Inspección", "desc": "Inspección fitozoosanitaria y movilización agropecuaria (nacional)"},
    {"num": "04-C", "grupo": "Fuente C", "tema": "Movilidad / Va y Ven", "folder": "fuente_c/04_transporte_vayven", "archivo": "export.geojson", "tipo": "GeoJSON Rutas", "desc": "Rutas y paraderos de transporte Va y Ven"},
    {"num": "06-C", "grupo": "Fuente C", "tema": "Scraping Apps Delivery", "folder": "fuente_c/06_scraping_delivery", "archivo": None, "tipo": "-", "desc": "Pendiente: los datos eran simulados y se eliminaron"},
    {"num": "08-C", "grupo": "Fuente C", "tema": "Relieve Mérida vs montaña", "folder": "fuente_c/08_opentopography", "archivo": "topografia_merida_vs_ciudades_montana.csv", "tipo": "CSV Topográfico", "desc": "2,400 cotas reales en 6 ciudades (AWS Terrain Tiles)"},
    {"num": "09-C", "grupo": "Fuente C", "tema": "Waypoints AR Lucas Gálvez", "folder": "fuente_c/09_ar_waypoints", "archivo": "ruta_ar_lucas_galvez.json", "tipo": "JSON (diseño propio)", "desc": "Ruta de guiado AR elaborada por el equipo"}
]

def verificar_todo():
    resumen = []
    for f in FUENTES:
        if f["archivo"] is None:
            resumen.append({"#": f["num"], "Grupo": f["grupo"], "Tema": f["tema"], "Archivo": "-",
                            "Formato": "-", "Estatus": "Pendiente", "Tamaño": "-", "Descripción": f["desc"]})
            continue
        ruta_archivo = os.path.join(DATA_DIR, f["folder"], f["archivo"])
        existe = os.path.exists(ruta_archivo)
        tamaño_kb = round(os.path.getsize(ruta_archivo) / 1024, 1) if existe else 0
        
        resumen.append({
            "#": f["num"],
            "Grupo": f["grupo"],
            "Tema": f["tema"],
            "Archivo": f["archivo"],
            "Formato": f["tipo"],
            "Estatus": "Listo" if existe else "Faltante",
            "Tamaño": f"{tamaño_kb} KB" if existe else "-",
            "Descripción": f["desc"]
        })

    df_res = pd.DataFrame(resumen)
    print("=" * 135)
    print("                     ESTADO DE LOS 22 DATASETS ACTIVOS DEL PROYECTO (FUENTES A, B Y C)")
    print("=" * 135)
    print(df_res.to_string(index=False))
    print("=" * 135)
    
    total = len(df_res)
    listos = sum(df_res["Estatus"] == "Listo")
    pendientes = sum(df_res["Estatus"] == "Pendiente")
    print(f"\nResumen: {listos} de {total} datasets listos y verificados en disco; {pendientes} pendientes.")

if __name__ == "__main__":
    verificar_todo()
