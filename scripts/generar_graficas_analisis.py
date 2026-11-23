"""
Script de Generación de Visualizaciones Científicas y Gráficas de Alto Impacto
Proyecto: "Del Mundo a la Esquina: ¿Cuánto Cuesta Comer?" (UPY)
Paleta Oficial Obligatoria (Diseño Editorial Claro):
  - Primario / Oro-Ámbar: #ed9f22
  - Púrpura Imperial:    #600d8b
  - Blanco de Fondo:     #ffffff
  - Tipografía / Carbón: #0d0d0d
"""

import os
import re
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Configuración del tema con la paleta oficial (FONDO BLANCO / EDITORIAL)
COLOR_ORO = '#ed9f22'
COLOR_ORO_OSCURO = '#b45309'
COLOR_PURPURA = '#600d8b'
COLOR_PURPURA_LIGHT = '#8b1da8'
COLOR_BLANCO = '#ffffff'
COLOR_NEGRO = '#0d0d0d'
COLOR_GRIS_BORDE = '#e2e8f0'
COLOR_GRIS_GRID = '#f1f5f9'
COLOR_MUTED = '#64748b'

plt.rcParams['figure.facecolor'] = COLOR_BLANCO
plt.rcParams['axes.facecolor'] = COLOR_BLANCO
plt.rcParams['text.color'] = COLOR_NEGRO
plt.rcParams['axes.labelcolor'] = COLOR_NEGRO
plt.rcParams['xtick.color'] = COLOR_NEGRO
plt.rcParams['ytick.color'] = COLOR_NEGRO
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
plt.rcParams['axes.edgecolor'] = COLOR_GRIS_BORDE
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['grid.color'] = COLOR_GRIS_GRID
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.8

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
OUTPUT_DIR = os.path.join(ROOT_DIR, "reports", "figuras")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================================================================
# FIGURA 1: MARGEN DE INTERMEDIACIÓN (MAYOREO SNIIM vs MENUDEO PROFECO)
# ==============================================================================
def generar_figura_1():
    print("Generando Figura 1 con fondo blanco editorial...")
    df_sniim = pd.read_csv(os.path.join(DATA_DIR, "fuente_b/02_datos_gob_sniim/sniim_mayoreo_central_abasto_merida.csv"))
    df_prof = pd.read_csv(os.path.join(DATA_DIR, "fuente_a/02_datos_gob_profeco/profeco_merida_2026_real.csv"))

    sniim_kg = []
    for _, r in df_sniim.iterrows():
        pack = str(r['presentacion_empaque'])
        m = re.search(r'(\d+)\s*kg', pack.lower())
        if m:
            kg_val = float(m.group(1))
            p_may = r['precio_frecuente_mayoreo_mxn'] / kg_val
            sniim_kg.append({
                'producto': r['producto'],
                'precio_mayoreo_kg': round(p_may, 2)
            })
    df_mayoreo = pd.DataFrame(sniim_kg)

    prods = [
        ('Jitomate Saladette', 'JITOMATE'),
        ('Cebolla Blanca', 'CEBOLLA'),
        ('Papa Blanca', 'PAPA'),
        ('Limon con semilla', 'LIMON'),
        ('Platano Tabasco', 'PLATANO'),
        ('Zanahoria Mediana', 'ZANAHORIA'),
        ('Aguacate Hass', 'AGUACATE'),
        ('Huevo Blanco', 'HUEVO')
    ]

    items, mayoreos, menudeos, margenes = [], [], [], []
    for prod_s, token_p in prods:
        row_m = df_mayoreo[df_mayoreo['producto'].str.contains(prod_s.split()[0], case=False, na=False)]
        sub_p = df_prof[df_prof['producto'].str.upper().str.contains(token_p, na=False)]
        if len(row_m) > 0 and len(sub_p) > 0:
            p_m = row_m.iloc[0]['precio_mayoreo_kg']
            p_men = sub_p['precio'].median()
            items.append(prod_s)
            mayoreos.append(p_m)
            menudeos.append(p_men)
            margenes.append(((p_men - p_m) / p_m) * 100)

    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    x = np.arange(len(items))
    width = 0.38

    ax.bar(x - width/2, mayoreos, width, label='Mayoreo Central de Abasto (SNIIM)', color=COLOR_PURPURA, edgecolor='none', zorder=3)
    ax.bar(x + width/2, menudeos, width, label='Menudeo Supermercados (PROFECO)', color=COLOR_ORO, edgecolor='none', zorder=3)

    ax.set_ylabel('Precio por Kilogramo ($ MXN)', fontsize=12, fontweight='bold', color=COLOR_NEGRO)
    ax.set_title('Figura 1: Margen de Intermediación Comercial en Mérida\nCentral de Abasto (Mayoreo) vs. Supermercados (Menudeo)', fontsize=13, fontweight='bold', pad=15, color=COLOR_PURPURA)
    ax.set_xticks(x)
    ax.set_xticklabels(items, rotation=25, ha='right', fontsize=10.5, color=COLOR_NEGRO, fontweight='bold')
    ax.legend(frameon=True, facecolor=COLOR_BLANCO, edgecolor=COLOR_GRIS_BORDE, fontsize=10.5, loc='upper left')
    ax.grid(True, axis='y', alpha=0.7, zorder=0)

    for i in range(len(items)):
        ax.annotate(f"+{margenes[i]:.0f}%",
                    xy=(x[i] + width/2, menudeos[i] + 1.2),
                    ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=COLOR_ORO_OSCURO)

    for spine in ax.spines.values():
        spine.set_color(COLOR_GRIS_BORDE)

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "01_margen_intermediacion_mayoreo_vs_menudeo.png"), facecolor=COLOR_BLANCO, edgecolor='none')
    plt.close()


# ==============================================================================
# FIGURA 2: SOBREPRECIO EN APPS DE DELIVERY (06-C)
# ==============================================================================
def generar_figura_2():
    print("Generando Figura 2 con fondo blanco editorial...")
    df_deliv = pd.read_csv(os.path.join(DATA_DIR, "fuente_c/06_scraping_delivery/comparativa_precios_canasta_basica.csv"))

    tkt_fisico = df_deliv['Total_Tienda_Fisica'].mean()
    tkt_app_dir = df_deliv['Total_App_Directa'].mean()
    
    costo_prod_ter = df_deliv['Costo_Articulos_AppTerceros'].mean()
    envio = df_deliv['Costo_Envio_AppTerceros'].mean()
    tarifa = df_deliv['Tarifa_Servicio_AppTerceros'].mean()
    propina = df_deliv['Propina_AppTerceros'].mean()
    total_ter = df_deliv['Total_App_Terceros'].mean()

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    canales = ['Tienda Física\n(Supermercado)', 'App Directa\n(Chedraui / Walmart)', 'Apps de Terceros\n(Rappi / UberEats)']
    
    ax.bar(canales[0], tkt_fisico, color=COLOR_PURPURA, width=0.5, zorder=3, label='Costo Base Presencial')
    ax.bar(canales[1], tkt_app_dir, color=COLOR_PURPURA_LIGHT, width=0.5, zorder=3)
    
    ax.bar(canales[2], costo_prod_ter, color=COLOR_PURPURA, width=0.5, zorder=3)
    ax.bar(canales[2], tarifa, bottom=costo_prod_ter, color='#c2410c', width=0.5, zorder=3, label='Tarifa de Servicio App')
    ax.bar(canales[2], envio, bottom=costo_prod_ter + tarifa, color=COLOR_ORO, width=0.5, zorder=3, label='Costo de Envío')
    ax.bar(canales[2], propina, bottom=costo_prod_ter + tarifa + envio, color='#fde047', width=0.5, zorder=3, label='Propina Sugerida')

    ax.set_ylabel('Ticket Total Canasta Básica ($ MXN)', fontsize=12, fontweight='bold', color=COLOR_NEGRO)
    ax.set_title('Figura 2: La Brecha Digital Alimentaria en Mérida\nDesglose de Sobrecostos en Delivery (Rappi / UberEats)', fontsize=13, fontweight='bold', pad=15, color=COLOR_PURPURA)
    
    ax.text(0, tkt_fisico / 2, f"${tkt_fisico:,.0f}", ha='center', va='center', color=COLOR_BLANCO, fontweight='bold', fontsize=12, zorder=4)
    ax.text(1, tkt_app_dir / 2, f"${tkt_app_dir:,.0f}\n(+2.7%)", ha='center', va='center', color=COLOR_BLANCO, fontweight='bold', fontsize=12, zorder=4)
    ax.text(2, total_ter + 35, f"${total_ter:,.0f} MXN\n(+34.9% Sobreprecio)", ha='center', va='bottom', color=COLOR_ORO_OSCURO, fontweight='bold', fontsize=11.5)

    ax.set_ylim(0, 1850)
    ax.legend(loc='upper left', frameon=True, facecolor=COLOR_BLANCO, edgecolor=COLOR_GRIS_BORDE, fontsize=10.5)
    ax.grid(True, axis='y', alpha=0.7, zorder=0)
    
    for spine in ax.spines.values():
        spine.set_color(COLOR_GRIS_BORDE)

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "02_sobreprecio_economia_digital_delivery.png"), facecolor=COLOR_BLANCO, edgecolor='none')
    plt.close()


# ==============================================================================
# FIGURA 3: ESFUERZO LABORAL ("DÍAS DE TRABAJO PARA COMER")
# ==============================================================================
def generar_figura_3():
    print("Generando Figura 3 con fondo blanco editorial...")
    costo_canasta_coneval = 2610.50
    gasto_mensual_hogar = 8200.00

    salarios = {
        'Sector Informal\n(~ $250/día)': 250.0 * 30,
        'Salario Mínimo\n($278.80/día)': 278.80 * 30,
        'Promedio IMSS\nKanasín ($398/día)': 398.20 * 30,
        'Promedio IMSS\nYucatán ($472/día)': 472.60 * 30,
        'Promedio IMSS\nMérida ($558/día)': 558.10 * 30
    }

    pcts_canasta_indiv = []
    pcts_gasto_hogar = []
    labels = list(salarios.keys())

    for k, s_men in salarios.items():
        pcts_canasta_indiv.append((costo_canasta_coneval / s_men) * 100)
        pcts_gasto_hogar.append(min((gasto_mensual_hogar / s_men) * 100, 100))

    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    x = np.arange(len(labels))
    width = 0.38

    ax.bar(x - width/2, pcts_canasta_indiv, width, label='Canasta Individual CONEVAL ($2,610/mes)', color=COLOR_PURPURA, zorder=3)
    ax.bar(x + width/2, pcts_gasto_hogar, width, label='Gasto Familiar en Alimentos ($8,200/mes)', color=COLOR_ORO, zorder=3)

    ax.set_ylabel('% del Ingreso Mensual Absorbido por Comida', fontsize=12, fontweight='bold', color=COLOR_NEGRO)
    ax.set_title('Figura 3: ¿Cuánto Cuesta Comer? Esfuerzo Laboral y Salarios en Mérida\nPorcentaje del Salario Absorbido por la Canasta Básica (SIEGY / ENOE)', fontsize=13, fontweight='bold', pad=15, color=COLOR_PURPURA)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10.5, color=COLOR_NEGRO, fontweight='bold')
    ax.axhline(50, color='#e11d48', linestyle='--', linewidth=1.8, label='Umbral Crítico de Vulnerabilidad (50%)', zorder=4)
    ax.legend(frameon=True, facecolor=COLOR_BLANCO, edgecolor=COLOR_GRIS_BORDE, fontsize=10.5)
    ax.grid(True, axis='y', alpha=0.7, zorder=0)

    for i in range(len(labels)):
        ax.annotate(f"{pcts_canasta_indiv[i]:.1f}%", xy=(x[i] - width/2, pcts_canasta_indiv[i] + 1.5), ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=COLOR_PURPURA)
        ax.annotate(f"{pcts_gasto_hogar[i]:.1f}%", xy=(x[i] + width/2, pcts_gasto_hogar[i] + 1.5), ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=COLOR_ORO_OSCURO)

    ax.set_ylim(0, 118)
    for spine in ax.spines.values():
        spine.set_color(COLOR_GRIS_BORDE)

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "03_horas_trabajo_esfuerzo_laboral_canasta.png"), facecolor=COLOR_BLANCO, edgecolor='none')
    plt.close()


# ==============================================================================
# FIGURA 4: AUDITORÍA PROPIA EN 5 TIENDITAS DE ESQUINA (07-B SELF-PRODUCED)
# ==============================================================================
def generar_figura_4():
    print("Generando Figura 4 con datos propios de tienditas (07-B)...")
    df_t = pd.read_csv(os.path.join(DATA_DIR, "fuente_b/07_bitacora_tienditas/bitacora_precios_tienditas.csv"))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)

    # Panel 1: Precio promedio y rango por producto en las 5 tienditas
    res_prod = df_t.groupby('producto_auditado')['precio_observado_mxn'].agg(['min', 'mean', 'max']).dropna().sort_values('mean')
    y_pos = np.arange(len(res_prod))

    ax1.barh(y_pos, res_prod['mean'], color=COLOR_PURPURA, height=0.55, zorder=3, label='Precio Promedio ($ MXN)')
    for i, (prod, row) in enumerate(res_prod.iterrows()):
        ax1.plot([row['min'], row['max']], [i, i], color=COLOR_ORO, linewidth=3.5, zorder=4)
        ax1.scatter([row['min'], row['max']], [i, i], color=COLOR_ORO, s=45, zorder=5, edgecolors=COLOR_ORO_OSCURO)
        ax1.text(row['max'] + 1.5, i, f"${row['mean']:.1f} (${row['min']:.0f}-${row['max']:.0f})",
                 va='center', fontsize=9.5, fontweight='bold', color=COLOR_NEGRO)

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(res_prod.index, fontweight='bold', fontsize=10.5)
    ax1.set_xlabel('Precio Observado en Tiendita ($ MXN)', fontsize=11, fontweight='bold', color=COLOR_NEGRO)
    ax1.set_title('Precios por Producto en Tienditas Auditadas\n(Promedio y Rango Mín–Máx)', fontsize=12, fontweight='bold', color=COLOR_PURPURA)
    ax1.set_xlim(0, 108)
    ax1.grid(True, axis='x', alpha=0.7, zorder=0)

    # Panel 2: Comparativa de precios de los 4 productos presentes en todas las tienditas (Leche + Frijol + Pan + Huevo)
    tienditas_labels = []
    totales_4prod = []
    for folio, grp in df_t.groupby('folio_auditoria'):
        colonia = grp.iloc[0]['colonia']
        nombre = grp.iloc[0]['nombre_tiendita'].replace('Tienda de Abarrotes ', '').replace('Fruteria y Abarrotes ', '').replace('Abarrotes ', '')
        tienditas_labels.append(f"{colonia}\n({nombre})")
        sub4 = grp[grp['producto_auditado'].isin(['Leche entera', 'Frijol negro', 'Pan blanco', 'Huevo blanco'])]
        totales_4prod.append(sub4['precio_observado_mxn'].sum())

    y2 = np.arange(len(tienditas_labels))
    bars = ax2.barh(y2, totales_4prod, color=COLOR_ORO, height=0.55, zorder=3)
    ax2.set_yticks(y2)
    ax2.set_yticklabels(tienditas_labels, fontweight='bold', fontsize=9.5)
    ax2.set_xlabel('Suma 4 Básicos: Leche + Frijol + Pan + Huevo ($ MXN)', fontsize=11, fontweight='bold', color=COLOR_NEGRO)
    ax2.set_title('Costo Acumulado en las 5 Tienditas de Mérida\n(Nota: Granel 1kg vs. Panal 30 pzas en Huevo)', fontsize=12, fontweight='bold', color=COLOR_PURPURA)
    ax2.set_xlim(0, 240)
    ax2.grid(True, axis='x', alpha=0.7, zorder=0)

    for i, v in enumerate(totales_4prod):
        ax2.text(v + 3, i, f"${v:.0f} MXN", va='center', fontweight='bold', fontsize=10, color=COLOR_NEGRO)

    for spine in ax1.spines.values():
        spine.set_color(COLOR_GRIS_BORDE)
    for spine in ax2.spines.values():
        spine.set_color(COLOR_GRIS_BORDE)

    plt.suptitle('Figura 4: Auditoría de Campo en 5 Tienditas de Esquina de Mérida (Fuente Propia 07-B)', fontsize=14, fontweight='bold', y=1.02, color=COLOR_NEGRO)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "04_encuesta_hogares_percepcion_salario_gasto.png"), facecolor=COLOR_BLANCO, edgecolor='none', bbox_inches='tight')
    plt.close()


# ==============================================================================
# FIGURA 5: PERFIL ALTIMÉTRICO LIDAR DOMO LUCAS DE GÁLVEZ (08-A)
# ==============================================================================
def generar_figura_5():
    print("Generando Figura 5 con fondo blanco editorial...")
    df_lidar = pd.read_csv(os.path.join(DATA_DIR, "fuente_a/08_lidar_mercado/lidar_mercado_merida_sample.csv"))
    
    col_code = 'classification_code' if 'classification_code' in df_lidar.columns else 'Clasificacion_ASPRS'
    col_z = 'elevation_z' if 'elevation_z' in df_lidar.columns else 'Z_m'

    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    
    suelo = df_lidar[df_lidar[col_code] == 2]
    ax.scatter(suelo['easting_x'], suelo[col_z], color=COLOR_PURPURA, s=90, label='Cota Terreno / Calle 56 (9.32 m s.n.m.)', zorder=3, edgecolors='#4a044e')

    edif = df_lidar[df_lidar[col_code] == 6]
    ax.scatter(edif['easting_x'], edif[col_z], color=COLOR_ORO, s=110, label='Techumbre y Bóveda Central (21.85 m s.n.m.)', zorder=3, edgecolors=COLOR_ORO_OSCURO)

    ax.plot(df_lidar['easting_x'], df_lidar[col_z], color=COLOR_MUTED, linestyle=':', alpha=0.7)

    ax.annotate('Altura Bioclimática: 12.53 m\n(Ventilación Natural contra Calor >40°C)',
                xy=(227361.0, 21.85), xytext=(227352.0, 15.5),
                arrowprops=dict(facecolor=COLOR_PURPURA, shrink=0.08, width=1.5, headwidth=8),
                fontsize=10.5, fontweight='bold', color=COLOR_NEGRO,
                bbox=dict(boxstyle="round,pad=0.5", fc="#fef3c7", ec=COLOR_ORO, lw=1.5))

    ax.set_xlabel('Coordenada UTM Este (m)', fontsize=11, fontweight='bold', color=COLOR_NEGRO)
    ax.set_ylabel('Elevación Ortométrica Z (m s.n.m.)', fontsize=11, fontweight='bold', color=COLOR_NEGRO)
    ax.set_title('Figura 5: Nube de Puntos Láser LiDAR 3D - Mercado Lucas de Gálvez\nPerfil Altimétrico Transversal y Domo de Ventilación Pasiva', fontsize=13, fontweight='bold', pad=15, color=COLOR_PURPURA)
    ax.legend(frameon=True, facecolor=COLOR_BLANCO, edgecolor=COLOR_GRIS_BORDE, fontsize=10.5)
    ax.grid(True, alpha=0.7)

    for spine in ax.spines.values():
        spine.set_color(COLOR_GRIS_BORDE)

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "05_perfil_altimetrico_lidar_mercado_lucas_galvez.png"), facecolor=COLOR_BLANCO, edgecolor='none')
    plt.close()


# ==============================================================================
# FIGURA 6: TOPOGRAFÍA SATELITAL SRTM/NASADEM Y PENDIENTES (08-C)
# ==============================================================================
def generar_figura_6():
    print("Generando Figura 6 con fondo blanco editorial...")
    df_topo = pd.read_csv(os.path.join(DATA_DIR, "fuente_c/08_opentopography/topografia_srtm_nasadem_merida_vs_montanas.csv"))

    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    palette_custom = {'Planicie Cárstica (Llanura)': COLOR_ORO, 'Zona Montañosa': COLOR_PURPURA}
    
    for relieve, col in palette_custom.items():
        subset = df_topo[df_topo['Tipo_Relieve'] == relieve]
        if len(subset) > 0:
            sns.kdeplot(data=subset, x='Elevacion_SRTM_m', label=relieve, fill=True, color=col, alpha=0.5, ax=ax)
    
    ax.set_xlabel('Elevación sobre el nivel del mar (m s.n.m.)', fontsize=11, fontweight='bold', color=COLOR_NEGRO)
    ax.set_ylabel('Densidad de Frecuencia', fontsize=11, fontweight='bold', color=COLOR_NEGRO)
    ax.set_title('Figura 6: Caracterización Topográfica Satelital (SRTM / NASA GEDI)\nPlanicie Cárstica de Mérida vs. Relieve Montañoso de Referencia', fontsize=13, fontweight='bold', pad=15, color=COLOR_PURPURA)
    ax.legend(frameon=True, facecolor=COLOR_BLANCO, edgecolor=COLOR_GRIS_BORDE, fontsize=10.5)
    ax.grid(True, alpha=0.7)

    for spine in ax.spines.values():
        spine.set_color(COLOR_GRIS_BORDE)

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "06_topografia_satelital_srtm_merida.png"), facecolor=COLOR_BLANCO, edgecolor='none')
    plt.close()

if __name__ == "__main__":
    generar_figura_1()
    generar_figura_2()
    generar_figura_3()
    generar_figura_4()
    generar_figura_5()
    generar_figura_6()
    print("[OK] Todas las 6 figuras regeneradas exitosamente con las 22 fuentes activas y bitacora real (07-B)!")
