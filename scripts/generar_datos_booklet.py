"""
Genera los CSV finales del capítulo del booklet (Acto 2, «El mes que se come tu sueldo»)
en booklet/datos/, uno por escena, a partir de los archivos reales del repositorio.

    escena-1.csv          Calendario de la canasta: días de salario mínimo para la canasta de un hogar
    escena-2.csv          Central de Abasto contra súper (139 productos comparables)
    escena-3.csv          Tienda de conveniencia contra súper (93 productos comparables)
    escena-4.csv          Tiendita contra súper (4 productos de la bitácora propia)
    puente-relieve.csv    Desnivel de Mérida frente a 5 ciudades de montaña (puente al Acto 4)
    unidad-salario-minimo.csv  Salario mínimo general diario 2025 y 2026, unidad común para todo el booklet

Uso: python scripts/generar_datos_booklet.py
"""
import os

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda *p: os.path.join(ROOT, *p)  # noqa: E731
OUT = R("booklet", "datos")
os.makedirs(OUT, exist_ok=True)

# Salario mínimo general 2025, zona del salario mínimo general: $278.80 diarios.
# Fuente: CONASAMI, Tabla de Salarios Mínimos Generales y Profesionales 2025 (verificado el 2026-11-24).
SALARIO_MINIMO_2025 = 278.80
# 2026: $315.04 diarios en la zona del salario mínimo general (CONASAMI, Tabla de Salarios Mínimos 2026,
# verificada el 2026-11-24). Solo se usa en la tabla de unidad común.
SALARIO_MINIMO_2026 = 315.04
DIAS_MES = 30


def guardar(df, nombre):
    df.to_csv(os.path.join(OUT, nombre), index=False, encoding="utf-8")
    print(f"[ok] booklet/datos/{nombre}: {len(df)} filas")


MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
         "noviembre", "diciembre"]


def escena_1():
    # Canasta: último mes publicado por INEGI (Líneas de Pobreza 2026), con salario mínimo del mismo año.
    lineas = pd.read_csv(R("data/fuente_a/03_siegy_yucatan/inegi_lineas_pobreza_2025_2026.csv"))
    censo = pd.read_csv(R("data/fuente_a/03_siegy_yucatan/censo2020_totales_municipio_merida.csv")).iloc[0]
    ult = lineas.iloc[-1]
    anio, mes = (int(x) for x in ult.periodo.split("-"))
    salario = {2025: SALARIO_MINIMO_2025, 2026: SALARIO_MINIMO_2026}[anio]
    canasta_persona = float(ult.lpei_canasta_alimentaria_urbana_mxn)
    ocupantes = float(censo.PROM_OCUP)
    canasta_hogar = round(canasta_persona * ocupantes, 2)
    dias = round(canasta_hogar / salario, 1)
    guardar(pd.DataFrame([{
        "periodo": ult.periodo,
        "canasta_persona_mxn": canasta_persona,
        "ocupantes_por_vivienda": ocupantes,
        "canasta_hogar_mxn": canasta_hogar,
        "salario_minimo_diario_mxn": salario,
        "dias_mes": DIAS_MES,
        "dias_canasta": dias,
        "dias_libres": round(DIAS_MES - dias, 1),
        "fuente": f"INEGI, Líneas de Pobreza (canasta alimentaria urbana, boletín del {ult.fecha_publicacion}); "
                  f"INEGI, Censo 2020 (promedio de ocupantes por vivienda, Mérida); CONASAMI, salario mínimo general {anio}",
        "corte": f"{MESES[mes - 1]} {anio}",
    }]), "escena-1.csv")


def comparables(canal, nombre_otro):
    c = pd.read_csv(R("reports/looker_studio/looker_05_comparables_por_canal.csv"))
    c = c[c.canal_comparado == canal].sort_values("diferencia_pct", ascending=False)
    return pd.DataFrame({
        "producto": c.producto, "presentacion": c.presentacion, "categoria": c.categoria,
        f"precio_{nombre_otro}_mxn": c.precio_canal_comparado_mxn, "precio_super_mxn": c.precio_supermercado_mxn,
        "diferencia_pct": c.diferencia_pct, f"registros_{nombre_otro}": c.registros_canal_comparado,
        "registros_super": c.registros_supermercado, "estadistico": c.estadistico,
        "fuente": "PROFECO, Quién es Quién en los Precios, Mérida", "corte": "mayo 2026",
    })


def escena_4():
    t = pd.read_csv(R("reports/looker_studio/looker_08_tienditas_vs_super.csv"))
    bit = pd.read_csv(R("data/fuente_b/07_bitacora_tienditas/bitacora_precios_tienditas.csv"))
    guardar(pd.DataFrame({
        "producto": t.producto, "precio_tiendita_mxn": t.mediana_tiendita_mxn,
        "precio_super_mxn": t.mediana_supermercado_mxn, "diferencia_pct": t.diferencia_pct_tiendita_vs_super,
        "registros_tiendita": t.registros_tiendita, "registros_super": t.registros_supermercado,
        "estadistico": "mediana", "numero_tienditas": bit.folio_auditoria.nunique(),
        "fuente": "Bitácora propia de 5 tienditas de Mérida (07-B); PROFECO, Quién es Quién en los Precios, Mérida",
        "corte": "bitácora: 26 sep a 1 oct 2026; PROFECO: mayo 2026",
    }), "escena-4.csv")


def puente():
    r = pd.read_csv(R("data/fuente_c/08_opentopography/topografia_merida_vs_ciudades_montana.csv"))
    g = r.groupby("ciudad").elevacion_m_snm.agg(["min", "max", "mean"]).reset_index()
    guardar(pd.DataFrame({
        "ciudad": g.ciudad, "elevacion_minima_m": g["min"].round(1), "elevacion_maxima_m": g["max"].round(1),
        "elevacion_promedio_m": g["mean"].round(1), "desnivel_m": (g["max"] - g["min"]).round(1),
        "fuente": "AWS Terrain Tiles (Tilezen, Terrarium, zoom 12), malla de 20 x 20 puntos por ciudad",
        "corte": "noviembre 2026",
    }).sort_values("desnivel_m"), "puente-relieve.csv")


def unidad_salario():
    filas = []
    for anio, diario in ((2025, SALARIO_MINIMO_2025), (2026, SALARIO_MINIMO_2026)):
        filas.append({
            "anio": anio, "zona": "Salario mínimo general (resto del país, incluye Yucatán)",
            "salario_minimo_diario_mxn": diario, "salario_minimo_mensual_mxn": round(diario * DIAS_MES, 2),
            "dias_por_mes": DIAS_MES,
            "fuente": f"CONASAMI, Tabla de Salarios Mínimos Generales y Profesionales {anio}",
            "corte": f"vigente del 1 de enero de {anio}",
        })
    guardar(pd.DataFrame(filas), "unidad-salario-minimo.csv")


if __name__ == "__main__":
    escena_1()
    guardar(comparables("Central de Abasto", "central"), "escena-2.csv")
    guardar(comparables("Conveniencia", "conveniencia"), "escena-3.csv")
    escena_4()
    puente()
    unidad_salario()
