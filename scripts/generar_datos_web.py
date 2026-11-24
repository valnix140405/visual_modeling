"""
Genera data/web/explorador_precios.json para el explorador con filtros de index.html.

Usa solo PROFECO QQP Mérida (mayo 2026) y los mismos criterios que los capítulos 2 y 3:
- Central de Abasto vs. supermercado: mediana por producto y presentación idénticos (139 pares).
- Conveniencia vs. supermercado: promedio por producto y presentación, con 3 o más registros
  en cada canal (93 pares). Conveniencia = giro "Tienda de Conveniencia" (Dunosusa, OXXO, 7 Eleven).

Uso: python scripts/generar_datos_web.py
"""
import json
import os

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFECO = os.path.join(ROOT, "data/fuente_a/02_datos_gob_profeco/profeco_merida_2026_real.csv")
SALIDA = os.path.join(ROOT, "data/web/explorador_precios.json")
K = ["producto", "presentacion"]


def main():
    d = pd.read_csv(PROFECO, dtype=str, encoding="utf-8-sig")
    d["precio"] = d.precio.astype(float)
    sup = d[d.giro == "Supermercado / Tienda de Autoservicio"]
    cat = d.groupby(K).categoria.agg(lambda s: s.mode().iat[0])

    filas = []

    ca = d[d.cadena_comercial == "Central de Abasto"]
    j = pd.concat([ca.groupby(K).precio.agg(["median", "count"]).add_suffix("_otro"),
                   sup.groupby(K).precio.agg(["median", "count"]).add_suffix("_super")], axis=1).dropna()
    for (prod, pres), r in j.iterrows():
        filas.append({"comparacion": "abasto", "producto": prod, "presentacion": pres,
                      "categoria": cat[(prod, pres)], "precio_otro": round(r.median_otro, 2),
                      "precio_super": round(r.median_super, 2), "n_otro": int(r.count_otro),
                      "n_super": int(r.count_super), "estadistico": "mediana"})

    conv = d[d.giro == "Tienda de Conveniencia"]
    j = conv.groupby(K).precio.agg(["mean", "count"]).add_suffix("_otro").join(
        sup.groupby(K).precio.agg(["mean", "count"]).add_suffix("_super"), how="inner")
    j = j[(j.count_otro >= 3) & (j.count_super >= 3)]
    for (prod, pres), r in j.iterrows():
        filas.append({"comparacion": "conveniencia", "producto": prod, "presentacion": pres,
                      "categoria": cat[(prod, pres)], "precio_otro": round(r.mean_otro, 2),
                      "precio_super": round(r.mean_super, 2), "n_otro": int(r.count_otro),
                      "n_super": int(r.count_super), "estadistico": "promedio"})

    for f in filas:  # diferencia calculada sin redondear antes
        f["dif_pct"] = round(100 * (f["precio_super"] / f["precio_otro"] - 1), 1) if f["comparacion"] == "abasto" \
            else round(100 * (f["precio_otro"] / f["precio_super"] - 1), 1)

    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    meta = {"fuente": "PROFECO Quién es Quién en los Precios, Mérida, mayo 2026 (data/fuente_a/02_datos_gob_profeco)",
            "nota_dif_pct": "abasto: súper / Central − 1 (positivo = súper más caro). "
                            "conveniencia: conveniencia / súper − 1 (positivo = conveniencia más cara).",
            "pares": {c: sum(f["comparacion"] == c for f in filas) for c in ("abasto", "conveniencia")}}
    with open(SALIDA, "w", encoding="utf-8") as fh:
        json.dump({"meta": meta, "filas": filas}, fh, ensure_ascii=False, separators=(",", ":"))
    print(f"[ok] {os.path.relpath(SALIDA, ROOT)}: {meta['pares']}")


if __name__ == "__main__":
    main()
