"""
Generador de Archivos 3D Reales (.glb y .ply) para LiDAR y Realidad Aumentada (AR)
Proyecto: "Del Mundo a la Esquina: ¿Cuánto Cuesta Comer?" (UPY)
Colores del Proyecto: #ed9f22 (Oro), #600d8b (Púrpura), #ffffff (Blanco), #0d0d0d (Negro)
"""

import os
import struct
import json
import pandas as pd
import numpy as np

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")

# ==============================================================================
# 1. GENERACIÓN DE NUBES DE PUNTOS LIDAR REALES (.PLY COMPATIBLES CON MESHLAB/CLOUDCOMPARE)
# ==============================================================================
def generar_ply_lidar_domo():
    """Genera archivo .ply oficial de la nube de puntos LiDAR del Mercado Lucas de Gálvez"""
    csv_path = os.path.join(DATA_DIR, "fuente_a/08_lidar_mercado/lidar_mercado_merida_sample.csv")
    out_ply = os.path.join(DATA_DIR, "fuente_a/08_lidar_mercado/domo_mercado_lucas_galvez_lidar.ply")
    df = pd.read_csv(csv_path)

    col_x = 'easting_x' if 'easting_x' in df.columns else 'X_m'
    col_y = 'northing_y' if 'northing_y' in df.columns else 'Y_m'
    col_z = 'elevation_z' if 'elevation_z' in df.columns else 'Z_m'
    col_code = 'classification_code' if 'classification_code' in df.columns else 'Clasificacion_ASPRS'

    # Normalizar coordenadas locales relativas
    min_x, min_y = df[col_x].min(), df[col_y].min()

    with open(out_ply, 'w', encoding='utf-8') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write("comment Nube de puntos LiDAR 3D Mercado Lucas de Gálvez - Proyecto UPY\n")
        f.write(f"element vertex {len(df)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")

        for _, r in df.iterrows():
            lx = r[col_x] - min_x
            ly = r[col_y] - min_y
            lz = r[col_z]
            # Paleta de colores oficial: Suelo en púrpura (#600d8b), Domo en oro (#ed9f22)
            if r[col_code] == 2:
                r_c, g_c, b_c = 96, 13, 139   # #600d8b
            else:
                r_c, g_c, b_c = 237, 159, 34  # #ed9f22
            f.write(f"{lx:.3f} {ly:.3f} {lz:.3f} {r_c} {g_c} {b_c}\n")

    print(f"[OK] Archivo LiDAR .ply generado: {out_ply}")

def generar_ply_lidar_cem():
    """Genera archivo .ply oficial de la malla de elevación continua CEM 3.0 de INEGI"""
    csv_path = os.path.join(DATA_DIR, "fuente_b/08_lidar_cem_mde/inegi_cem_mde_merida_grid.csv")
    out_ply = os.path.join(DATA_DIR, "fuente_b/08_lidar_cem_mde/inegi_cem_mde_merida_grid.ply")
    df = pd.read_csv(csv_path)

    min_x, min_y = df['utm_easting_x'].min(), df['utm_northing_y'].min()

    with open(out_ply, 'w', encoding='utf-8') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write("comment Malla de elevacion LiDAR CEM 3.0 INEGI Merida - Proyecto UPY\n")
        f.write(f"element vertex {len(df)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")

        for _, r in df.iterrows():
            lx = (r['utm_easting_x'] - min_x) / 100.0
            ly = (r['utm_northing_y'] - min_y) / 100.0
            lz = r['elevacion_m_snm']
            f.write(f"{lx:.3f} {ly:.3f} {lz:.3f} 237 159 34\n")

    print(f"[OK] Archivo generado: {out_ply}")

def generar_ply_lidar_gedi():
    """Genera archivo .ply de la nube de puntos del LiDAR espacial NASA GEDI"""
    csv_path = os.path.join(DATA_DIR, "fuente_c/08_opentopography/topografia_srtm_nasadem_merida_vs_montanas.csv")
    out_ply = os.path.join(DATA_DIR, "fuente_c/08_opentopography/nasa_gedi_dosel_merida_lidar.ply")
    df = pd.read_csv(csv_path).head(500) # Muestra de 500 puntos para visualización limpia

    with open(out_ply, 'w', encoding='utf-8') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write("comment Nube LiDAR Espacial NASA GEDI - Altura de Dosel y Suelo - Proyecto UPY\n")
        f.write(f"element vertex {len(df)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")

        min_lat, min_lon = df['Latitud'].min(), df['Longitud'].min()
        for _, r in df.iterrows():
            lx = (r['Longitud'] - min_lon) * 111000.0 # Aproximación en metros
            ly = (r['Latitud'] - min_lat) * 111000.0
            lz = r['Elevacion_SRTM_m'] + r['GEDI_Altura_Dosel_m']
            f.write(f"{lx:.2f} {ly:.2f} {lz:.2f} 96 13 139\n")

    print(f"[OK] Archivo LiDAR NASA GEDI .ply generado: {out_ply}")


# ==============================================================================
# 2. GENERADOR DE ARCHIVOS .GLB BINARIOS REALES (ESTÁNDAR GLTF 2.0 PARA AR)
# ==============================================================================
def crear_glb_cubo(nombre_archivo, color_rgb=(237, 159, 34), escala=(1.0, 1.0, 1.0)):
    """
    Construye un archivo binario .glb estándar y válido según la especificación Khronos glTF 2.0.
    """
    # Vértices de un cubo centrado (8 vértices, 3 componentes float32 cada uno)
    sx, sy, sz = escala[0]/2.0, escala[1]/2.0, escala[2]/2.0
    vertices = np.array([
        [-sx, -sy, -sz], [ sx, -sy, -sz], [ sx,  sy, -sz], [-sx,  sy, -sz],
        [-sx, -sy,  sz], [ sx, -sy,  sz], [ sx,  sy,  sz], [-sx,  sy,  sz]
    ], dtype=np.float32)

    # 12 triángulos (36 índices uint16)
    indices = np.array([
        0, 1, 2,  0, 2, 3, # Cara trasera
        4, 6, 5,  4, 7, 6, # Cara frontal
        0, 4, 5,  0, 5, 1, # Cara inferior
        3, 2, 6,  3, 6, 7, # Cara superior
        0, 3, 7,  0, 7, 4, # Cara izquierda
        1, 5, 6,  1, 6, 2  # Cara derecha
    ], dtype=np.uint16)

    # Construir buffer binario
    indices_bytes = indices.tobytes()
    # Padding a 4 bytes para alineación
    while len(indices_bytes) % 4 != 0:
        indices_bytes += b'\x00'

    vertices_bytes = vertices.tobytes()
    while len(vertices_bytes) % 4 != 0:
        vertices_bytes += b'\x00'

    bin_data = indices_bytes + vertices_bytes
    bin_length = len(bin_data)

    # Estructura JSON glTF
    gltf_dict = {
        "asset": {
            "version": "2.0",
            "generator": "UPY Data Engineering - AR Asset Builder"
        },
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": "Asset_Canasta_Basica_AR"}],
        "meshes": [{
            "primitives": [{
                "attributes": {"POSITION": 1},
                "indices": 0,
                "material": 0
            }]
        }],
        "materials": [{
            "pbrMetallicRoughness": {
                "baseColorFactor": [color_rgb[0]/255.0, color_rgb[1]/255.0, color_rgb[2]/255.0, 1.0],
                "metallicFactor": 0.2,
                "roughnessFactor": 0.6
            }
        }],
        "buffers": [{"byteLength": bin_length}],
        "bufferViews": [
            {
                "buffer": 0,
                "byteOffset": 0,
                "byteLength": len(indices_bytes),
                "target": 34963 # ELEMENT_ARRAY_BUFFER
            },
            {
                "buffer": 0,
                "byteOffset": len(indices_bytes),
                "byteLength": len(vertices_bytes),
                "target": 34962 # ARRAY_BUFFER
            }
        ],
        "accessors": [
            {
                "bufferView": 0,
                "byteOffset": 0,
                "componentType": 5123, # UNSIGNED_SHORT
                "count": len(indices),
                "type": "SCALAR",
                "max": [int(indices.max())],
                "min": [int(indices.min())]
            },
            {
                "bufferView": 1,
                "byteOffset": 0,
                "componentType": 5126, # FLOAT
                "count": len(vertices),
                "type": "VEC3",
                "max": [float(vertices[:, 0].max()), float(vertices[:, 1].max()), float(vertices[:, 2].max())],
                "min": [float(vertices[:, 0].min()), float(vertices[:, 1].min()), float(vertices[:, 2].min())]
            }
        ]
    }

    json_str = json.dumps(gltf_dict, separators=(',', ':'))
    json_bytes = json_str.encode('utf-8')
    # Alinear JSON a 4 bytes con espacios
    while len(json_bytes) % 4 != 0:
        json_bytes += b' '

    json_length = len(json_bytes)
    total_length = 12 + 8 + json_length + 8 + bin_length

    # Encabezado GLB (12 bytes)
    header = struct.pack('<4sII', b'glTF', 2, total_length)
    # Chunk 0: JSON
    chunk0_header = struct.pack('<I4s', json_length, b'JSON')
    # Chunk 1: BIN
    chunk1_header = struct.pack('<I4s', bin_length, b'BIN\x00')

    with open(nombre_archivo, 'wb') as f:
        f.write(header)
        f.write(chunk0_header)
        f.write(json_bytes)
        f.write(chunk1_header)
        f.write(bin_data)

    print(f"[OK] Archivo AR 3D binario .glb generado: {nombre_archivo} ({os.path.getsize(nombre_archivo)} bytes)")

def generar_assets_ar():
    models_dir_b = os.path.join(DATA_DIR, "fuente_b/09_ar_modelos_3d/models")
    models_dir_a = os.path.join(DATA_DIR, "fuente_a/09_ar_anclas/models")
    os.makedirs(models_dir_b, exist_ok=True)
    os.makedirs(models_dir_a, exist_ok=True)

    # 1. Canasta Básica de Víveres (Oro #ed9f22)
    f1 = os.path.join(models_dir_b, "canasta_basica_lowpoly.glb")
    crear_glb_cubo(f1, color_rgb=(237, 159, 34), escala=(0.5, 0.35, 0.4))

    # 2. Cono de Huevo con Precio AR (Púrpura #600d8b)
    f2 = os.path.join(models_dir_b, "cono_huevo_precio.glb")
    crear_glb_cubo(f2, color_rgb=(96, 13, 139), escala=(0.3, 0.15, 0.3))

    # 3. Pack Lácteo y Abarrotes (Blanco #ffffff)
    f3 = os.path.join(models_dir_b, "leche_abarrotes_pack.glb")
    crear_glb_cubo(f3, color_rgb=(240, 240, 240), escala=(0.2, 0.28, 0.18))

    # 4. Tarjeta HUD Holográfica de Precios para Fachada
    f4 = os.path.join(models_dir_b, "card_mercado_precios.glb")
    crear_glb_cubo(f4, color_rgb=(237, 159, 34), escala=(1.2, 0.8, 0.05))

    # Copiar también a fuente_a para las anclas
    f5 = os.path.join(models_dir_a, "card_mercado_precios.glb")
    crear_glb_cubo(f5, color_rgb=(237, 159, 34), escala=(1.2, 0.8, 0.05))

if __name__ == "__main__":
    print("Iniciando generación de archivos físicos 3D y LiDAR...")
    generar_ply_lidar_domo()
    generar_ply_lidar_cem()
    generar_ply_lidar_gedi()
    generar_assets_ar()
    print("\n¡Todos los archivos físicos .ply (LiDAR) y .glb (AR 3D) creados exitosamente!")
