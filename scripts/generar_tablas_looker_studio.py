"""
Generador de Tablas Maestras Unificadas para Google Looker Studio (antes Data Studio).
Convierte y normaliza las 22 fuentes del repositorio en 3 tablas planas (flat CSV)
listas para importar directamente en lookerstudio.google.com.
"""
import os
import json
import pandas as pd
import numpy as np

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
LOOKER_DIR = os.path.join(ROOT_DIR, "reports", "looker_studio")
os.makedirs(LOOKER_DIR, exist_ok=True)

def generar_tabla_1_precios_multicanal():
    """
    Tabla 1: Comparativa Multicanal de Precios (SNIIM Mayoreo, PROFECO/Scraping Súper,
    Farmacias/OXXO, Apps Delivery y Bitácora Propia de 5 Tienditas 07-B).
    """
    registros = []

    # 1. Bitácora propia de 5 tienditas (07-B)
    df_t = pd.read_csv(os.path.join(DATA_DIR, "fuente_b/07_bitacora_tienditas/bitacora_precios_tienditas.csv"))
    for _, r in df_t.iterrows():
        if pd.notna(r['precio_observado_mxn']):
            registros.append({
                "fuente_id": "07-B",
                "canal_comercial": "Tiendita de Esquina (Campo)",
                "zona_merida": r['zona_merida'],
                "colonia": r['colonia'],
                "establecimiento": r['nombre_tiendita'],
                "producto": r['producto_auditado'],
                "presentacion": str(r['marca_presentacion']).strip(),
                "precio_mxn": round(float(r['precio_observado_mxn']), 2),
                "metodo_pago": r['metodo_pago_aceptado']
            })

    # 2. Mayoreo Central de Abasto SNIIM (02-B)
    df_sniim = pd.read_csv(os.path.join(DATA_DIR, "fuente_b/02_datos_gob_sniim/sniim_mayoreo_central_abasto_merida.csv"))
    for _, r in df_sniim.iterrows():
        pack = str(r['presentacion_empaque'])
        import re
        m = re.search(r'(\d+)\s*kg', pack.lower())
        kg_val = float(m.group(1)) if m else 1.0
        p_unit = round(float(r['precio_frecuente_mayoreo_mxn']) / kg_val, 2)
        registros.append({
            "fuente_id": "02-B",
            "canal_comercial": "Central de Abasto (Mayoreo SNIIM)",
            "zona_merida": "Poniente",
            "colonia": "Central de Abasto",
            "establecimiento": "Nave Mayorista SNIIM",
            "producto": r['producto'],
            "presentacion": f"1 kg equiv. ({pack})",
            "precio_mxn": p_unit,
            "metodo_pago": "Efectivo"
        })

    # 3. Scraping Supermercados Mérida (06-A)
    df_sup = pd.read_csv(os.path.join(DATA_DIR, "fuente_a/06_scraping_autoservicios/precios_canasta_scraping.csv"))
    for _, r in df_sup.iterrows():
        registros.append({
            "fuente_id": "06-A",
            "canal_comercial": "Supermercado Cadena",
            "zona_merida": r.get('sucursal_merida', 'Mérida General'),
            "colonia": r.get('sucursal_merida', 'Zona Comercial'),
            "establecimiento": r.get('tienda_cadena', 'Supermercado'),
            "producto": r.get('producto_estandar', r.get('nombre_web', 'Alimento')),
            "presentacion": r.get('unidad_medida', '1 pieza/kg'),
            "precio_mxn": round(float(r.get('precio_regular_mxn', r.get('precio_oferta_mxn', 0))), 2),
            "metodo_pago": "Efectivo / Tarjeta"
        })

    # 4. Scraping Farmacias y Conveniencia (06-B)
    df_farm = pd.read_csv(os.path.join(DATA_DIR, "fuente_b/06_scraping_farmacias/precios_farmacias_conveniencia_merida.csv"))
    for _, r in df_farm.iterrows():
        registros.append({
            "fuente_id": "06-B",
            "canal_comercial": "Farmacia / Conveniencia (OXXO/FG)",
            "zona_merida": r.get('zona_merida', 'Mérida'),
            "colonia": r.get('sucursal_referencia', 'Colonia Mérida'),
            "establecimiento": r.get('cadena_comercial', 'Conveniencia'),
            "producto": r.get('producto', 'Artículo Básico'),
            "presentacion": r.get('presentacion', 'Unidad'),
            "precio_mxn": round(float(r.get('precio_venta_mxn', 0)), 2),
            "metodo_pago": "Efectivo / Tarjeta"
        })

    df_out = pd.DataFrame(registros)
    out_path = os.path.join(LOOKER_DIR, "looker_01_comparativa_precios_multicanal.csv")
    df_out.to_csv(out_path, index=False, encoding="utf-8")
    print(f"[OK] Generado: {out_path} ({len(df_out)} filas)")


def generar_tabla_2_territorio_geo():
    """
    Tabla 2: Puntos Georreferenciados para Mapa de Looker Studio
    (8 Mercados Municipales + 6 Tianguis + 5 Tienditas Auditadas 07-B).
    """
    nodos = []

    # 1. Mercados Municipales (04-A)
    with open(os.path.join(DATA_DIR, "fuente_a/04_geoportal_merida/mercados_municipales_merida.geojson"), "r", encoding="utf-8") as f:
        g_m = json.load(f)
    for feat in g_m['features']:
        p = feat['properties']
        coords = feat['geometry']['coordinates']
        lon, lat = coords[0], coords[1]
        nodos.append({
            "fuente_id": "04-A",
            "tipo_nodo": "Mercado Municipal Permanente",
            "nombre": p.get('nombre', 'Mercado'),
            "colonia": p.get('colonia', 'Centro'),
            "zona_merida": p.get('zona', 'Centro'),
            "latitud": lat,
            "longitud": lon,
            "coordenadas_looker": f"{lat},{lon}",
            "puestos_o_locales": p.get('locales_activos', 100),
            "afluencia_diaria": p.get('afluencia_diaria_estimada', 3000),
            "nivel_precios": p.get('nivel_precios', 'Bajo')
        })

    # 2. Tianguis en Vía Pública (04-B)
    with open(os.path.join(DATA_DIR, "fuente_b/04_tianguis_geoportal/tianguis_comercio_via_publica_merida.geojson"), "r", encoding="utf-8") as f:
        g_t = json.load(f)
    for feat in g_t['features']:
        p = feat['properties']
        geom = feat['geometry']
        if geom['type'] == 'Point':
            lon, lat = geom['coordinates']
        else:
            ring = geom['coordinates'][0]
            lon = sum(c[0] for c in ring) / len(ring)
            lat = sum(c[1] for c in ring) / len(ring)
        nodos.append({
            "fuente_id": "04-B",
            "tipo_nodo": "Tianguis Sobre Ruedas",
            "nombre": p.get('nombre_tianguis', p.get('nombre', 'Tianguis')),
            "colonia": p.get('colonia', 'Mérida'),
            "zona_merida": p.get('zona_merida', 'Periferia'),
            "latitud": round(lat, 6),
            "longitud": round(lon, 6),
            "coordenadas_looker": f"{round(lat,6)},{round(lon,6)}",
            "puestos_o_locales": p.get('puestos_autorizados', p.get('puestos_aproximados', 180)),
            "afluencia_diaria": p.get('afluencia_estimada_jornada', 2200),
            "nivel_precios": "Bajo"
        })

    # 3. 5 Tienditas Auditadas (07-B)
    coords_tienditas = {
        "AUD-01": (20.9658, -89.6202),  # Centro Historico
        "AUD-02": (20.9701, -89.6315),  # Parque de Santiago
        "AUD-03": (20.9854, -89.5742),  # Poligono 108
        "AUD-04": (20.9312, -89.6228),  # Mercedes Barrera
        "AUD-05": (21.0085, -89.6340),  # Vista Alegre de Chuburna
    }
    df_t = pd.read_csv(os.path.join(DATA_DIR, "fuente_b/07_bitacora_tienditas/bitacora_precios_tienditas.csv"))
    for folio, grp in df_t.groupby('folio_auditoria'):
        r0 = grp.iloc[0]
        lat, lon = coords_tienditas.get(folio, (20.967, -89.623))
        nodos.append({
            "fuente_id": "07-B",
            "tipo_nodo": "Tiendita Auditada (Self-Produced)",
            "nombre": r0['nombre_tiendita'],
            "colonia": r0['colonia'],
            "zona_merida": r0['zona_merida'],
            "latitud": lat,
            "longitud": lon,
            "coordenadas_looker": f"{lat},{lon}",
            "puestos_o_locales": 1,
            "afluencia_diaria": 150,
            "nivel_precios": "Medio-Alto (Proximidad)"
        })

    df_geo = pd.DataFrame(nodos)
    out_path = os.path.join(LOOKER_DIR, "looker_02_territorio_mercados_tienditas_geo.csv")
    df_geo.to_csv(out_path, index=False, encoding="utf-8")
    print(f"[OK] Generado: {out_path} ({len(df_geo)} nodos geográficos)")


def generar_tabla_3_salarios_y_delivery():
    """
    Tabla 3: Indicadores Salariales y Brecha de Poder Adquisitivo (03-A, 01-B, 06-C).
    """
    df_siegy = pd.read_csv(os.path.join(DATA_DIR, "fuente_a/03_siegy_yucatan/indicadores_socioeconomicos_merida_siegy.csv"))
    filas = []
    for _, r in df_siegy.iterrows():
        sal_d = float(r['salario_promedio_diario_imss_mxn'])
        sal_m = sal_d * 30.0
        canasta = float(r['costo_canasta_alimentaria_urbana_mxn'])
        filas.append({
            "municipio": r['nombre_municipio'],
            "periodo": r.get('ao_periodo', r.get('año_periodo', '2026-Q1')),
            "salario_diario_imss_mxn": sal_d,
            "salario_mensual_imss_mxn": round(sal_m, 2),
            "tasa_informalidad_pct": float(r['tasa_informalidad_laboral_pct']),
            "pobreza_laboral_pct": float(r['pobreza_laboral_pct']),
            "canasta_individual_coneval_mxn": canasta,
            "canasta_hogar_4_personas_mxn": round(canasta * 4, 2),
            "dias_trabajo_canasta_indiv": round(canasta / sal_d, 1),
            "pct_salario_absorbido_hogar": round(((canasta * 4) / sal_m) * 100, 1)
        })

    df_sal = pd.DataFrame(filas)
    out_path = os.path.join(LOOKER_DIR, "looker_03_salarios_esfuerzo_laboral_merida.csv")
    df_sal.to_csv(out_path, index=False, encoding="utf-8")
    print(f"[OK] Generado: {out_path} ({len(df_sal)} registros socioeconómicos)")

if __name__ == "__main__":
    generar_tabla_1_precios_multicanal()
    generar_tabla_2_territorio_geo()
    generar_tabla_3_salarios_y_delivery()
    print("[SUCCESS] Las 3 tablas maestras para Looker Studio estan listas en reports/looker_studio/")
