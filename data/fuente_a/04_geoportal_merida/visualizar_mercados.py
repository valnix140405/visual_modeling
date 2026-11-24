"""
Lee y resume la capa GeoJSON de mercados públicos de Mérida derivada del DENUE de INEGI
(generada por scripts/generar_datos_reales.py).
"""
import json
import os

import pandas as pd


def listar_mercados():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    geojson_path = os.path.join(current_dir, "mercados_publicos_merida_denue.geojson")
    with open(geojson_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    filas = []
    for feat in data["features"]:
        props = feat["properties"]
        lon, lat = feat["geometry"]["coordinates"]
        filas.append({
            "id": props["id"],
            "nombre": props["nombre"],
            "colonia": props["colonia_principal"],
            "codigo_postal": props["codigo_postal"],
            "establecimientos_denue": props["establecimientos_denue"],
            "alimentos_bebidas": props["establecimientos_alimentos_bebidas"],
            "longitud": lon,
            "latitud": lat,
        })

    df = pd.DataFrame(filas)
    print("=== Mercados públicos de Mérida (INEGI DENUE) ===")
    print(df.to_string(index=False))
    print(f"\nTotal de establecimientos: {df.establecimientos_denue.sum():,}")
    print(f"\n[INFO] Mapa interactivo con radios de 800 m:")
    print(f"       -> {os.path.join(current_dir, 'visor_mercados_municipales.html')}")
    return df


if __name__ == "__main__":
    listar_mercados()
