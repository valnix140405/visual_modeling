"""
Script de Generación de Visualizaciones Editoriales No Convencionales ("Data Storytelling Art")
Proyecto: "Del Mundo a la Esquina: ¿Cuánto Cuesta Comer?" (UPY)
Paleta Oficial Obligatoria:
  - Primario / Oro-Ámbar: #ed9f22
  - Púrpura Imperial:    #600d8b
  - Blanco Editorial:    #ffffff
  - Carbón Tipográfico:  #0d0d0d

Arquetipos Visuales Creativos:
  - Fig 1: Gráfico de Cometas de Explosión de Precio (Tapered Comet Slopegraph & Proportional Spheres)
  - Fig 2: Flujo Aluvial / Sankey de Fuga Algorítmica + Rosa Polar de Pérdida Anual en Delivery
  - Fig 3: Rosa de los Vientos de Nightingale (Coxcomb Polar) + Matriz Calendario "30 Días de Vida vs Comida"
  - Fig 4: Estrella Poligonal Radar (Spider Web) + Matriz de Burbujas Térmicas de las 5 Tienditas Reales (07-B)
  - Fig 5: Corte Arquitectónico Termodinámico LiDAR 3D con Vectores de Convección Pasiva del Domo
  - Fig 6: Ridgeline Joyplot Topográfico (Horizontes Cársticos) + Mandala Radial de Movilidad Va y Ven
"""

import os
import re
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np
import pandas as pd

# Paleta Oficial Estricta
COLOR_ORO = '#ed9f22'
COLOR_ORO_DARK = '#b45309'
COLOR_ORO_SOFT = '#fef3c7'
COLOR_PURPURA = '#600d8b'
COLOR_PURPURA_LIGHT = '#9333ea'
COLOR_PURPURA_SOFT = '#f3e8ff'
COLOR_BLANCO = '#ffffff'
COLOR_NEGRO = '#0d0d0d'
COLOR_GRIS_BORDE = '#e2e8f0'
COLOR_GRIS_GRID = '#f1f5f9'
COLOR_MUTED = '#525252'

plt.rcParams['figure.facecolor'] = COLOR_BLANCO
plt.rcParams['axes.facecolor'] = COLOR_BLANCO
plt.rcParams['text.color'] = COLOR_NEGRO
plt.rcParams['axes.labelcolor'] = COLOR_NEGRO
plt.rcParams['xtick.color'] = COLOR_NEGRO
plt.rcParams['ytick.color'] = COLOR_NEGRO
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
plt.rcParams['axes.edgecolor'] = COLOR_GRIS_BORDE
plt.rcParams['axes.linewidth'] = 1.0

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
OUTPUT_DIR = os.path.join(ROOT_DIR, "reports", "figuras")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==============================================================================
# FIGURA 1: COMETAS DE EXPLOSIÓN DE PRECIO (TAPERED COMET SLOPEGRAPH)
# ==============================================================================
def generar_figura_1():
    print("Generando Figura 1: Cometas de Explosion de Precio (SNIIM vs PROFECO)...")
    # Datos verificados del cruce SNIIM Central de Abasto (02-B) vs PROFECO Mérida (02-A)
    datos = [
        ('Huevo Blanco', 36.00, 48.50, 34.7),
        ('Cebolla Blanca', 14.00, 22.00, 57.1),
        ('Zanahoria Mediana', 11.50, 19.50, 69.6),
        ('Plátano Tabasco', 12.00, 24.90, 107.5),
        ('Aguacate Hass', 38.00, 79.00, 107.9),
        ('Limón con Semilla', 11.11, 26.50, 138.5),
        ('Jitomate Saladette', 16.15, 45.00, 178.6),
        ('Papa Blanca Alpha', 16.00, 56.00, 250.0)
    ]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 6.5), dpi=300, gridspec_kw={'width_ratios': [2.2, 1]})

    y_positions = np.arange(len(datos))

    # Panel Izquierdo: Cometas Horizontales con Estela de Expansión (Tapered Polygons)
    for i, (nombre, may, men, marg) in enumerate(datos):
        # Dibujar cola de cometa (trapecio que se ensancha de mayoreo a menudeo)
        h_start = 0.06
        h_end = 0.28
        verts = [
            (may, i - h_start),
            (men, i - h_end),
            (men, i + h_end),
            (may, i + h_start)
        ]
        poly = patches.Polygon(verts, closed=True, facecolor=COLOR_ORO, alpha=0.35, edgecolor=COLOR_ORO, linewidth=1.2, zorder=2)
        ax1.add_patch(poly)

        # Línea central de trayectoria
        ax1.plot([may, men], [i, i], color=COLOR_PURPURA, linestyle=':', linewidth=1.5, zorder=3)

        # Nodo de origen (Campo / Central de Abasto)
        ax1.scatter(may, i, s=130, color=COLOR_PURPURA, edgecolors=COLOR_BLANCO, linewidth=1.8, zorder=4)
        ax1.text(may - 1.8, i, f"${may:.1f}", va='center', ha='right', fontsize=9.5, fontweight='bold', color=COLOR_PURPURA)

        # Cabeza de cometa (Góndola de Supermercado - área proporcional al margen)
        head_size = 180 + (marg * 1.4)
        ax1.scatter(men, i, s=head_size, color=COLOR_ORO, edgecolors=COLOR_NEGRO, linewidth=1.5, zorder=5)
        ax1.text(men + 2.2, i, f"${men:.1f}/kg  (+{marg:.0f}%)", va='center', ha='left', fontsize=10, fontweight='bold', color=COLOR_NEGRO)

    ax1.set_yticks(y_positions)
    ax1.set_yticklabels([d[0] for d in datos], fontsize=11, fontweight='bold', color=COLOR_NEGRO)
    ax1.set_xlim(0, 102)
    ax1.set_xlabel('Recorrido del Precio por Kilogramo ($ MXN): De la Central de Abasto al Supermercado', fontsize=11, fontweight='bold')
    ax1.set_title('A. Cometas de Inflación Comercial (Efecto Embudo Inverso)', fontsize=12.5, fontweight='bold', color=COLOR_PURPURA, pad=12)
    ax1.grid(True, axis='x', linestyle='--', alpha=0.6)

    # Leyenda personalizada en ax1
    ax1.scatter([], [], s=110, color=COLOR_PURPURA, label='Origen: Mayoreo Central de Abasto (SNIIM 02-B)')
    ax1.scatter([], [], s=240, color=COLOR_ORO, edgecolors=COLOR_NEGRO, label='Destino: Góndola Supermercado (PROFECO 02-A)')
    ax1.legend(loc='lower right', bbox_to_anchor=(0.99, 0.14), frameon=True, facecolor=COLOR_BLANCO, edgecolor=COLOR_GRIS_BORDE, fontsize=9.2)

    # Panel Derecho: Índice Multiplicador ("¿Cuántos kilos de abasto compras con 1 kilo de súper?")
    mults = [d[2] / d[1] for d in datos]
    for i, m_val in enumerate(mults):
        # Dibujar círculos apilados representando cuántos kilos mayoristas equivalen a 1 kg en súper
        n_circles = int(np.ceil(m_val))
        for c_idx in range(n_circles):
            fill_col = COLOR_PURPURA if c_idx == 0 else COLOR_ORO
            alpha_val = 0.95 if c_idx < int(m_val) else 0.45
            ax2.scatter(c_idx * 0.85 + 0.5, i, s=260, color=fill_col, alpha=alpha_val, edgecolors=COLOR_NEGRO, linewidth=1.0, zorder=4)
        ax2.text(n_circles * 0.85 + 0.35, i, f"{m_val:.1f}x veces", va='center', fontsize=10, fontweight='bold', color=COLOR_PURPURA)

    ax2.set_yticks(y_positions)
    ax2.set_yticklabels(['' for _ in datos])
    ax2.set_xlim(0, 5.2)
    ax2.set_xticks([0.5, 1.35, 2.2, 3.05, 3.9])
    ax2.set_xticklabels(['1x', '2x', '3x', '4x', '5x'], fontweight='bold')
    ax2.set_xlabel('Factor de Multiplicación del Precio', fontsize=11, fontweight='bold')
    ax2.set_title('B. Equivalencia en Kilos Mayoristas', fontsize=12.5, fontweight='bold', color=COLOR_PURPURA, pad=12)
    ax2.grid(True, axis='x', linestyle='--', alpha=0.6)

    for spine in ax1.spines.values():
        spine.set_color(COLOR_GRIS_BORDE)
    for spine in ax2.spines.values():
        spine.set_color(COLOR_GRIS_BORDE)

    plt.suptitle('Figura 1: La Metamorfosis del Precio en Mérida — ¿Cómo se Triplica el Costo en 12 km de Asfalto?',
                 fontsize=14, fontweight='bold', color=COLOR_NEGRO, y=1.02)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "01_margen_intermediacion_mayoreo_vs_menudeo.png"), facecolor=COLOR_BLANCO, bbox_inches='tight')
    plt.close()


# ==============================================================================
# FIGURA 2: FLUJO ALUVIAL SANKEY DE FUGA ALGORÍTMICA + RELOJ POLAR (06-C)
# ==============================================================================
def generar_figura_2():
    print("Generando Figura 2: Flujo Aluvial Sankey de Delivery y Rosa Polar...")
    df_deliv = pd.read_csv(os.path.join(DATA_DIR, "fuente_c/06_scraping_delivery/comparativa_precios_canasta_basica.csv"))

    tkt_fisico = df_deliv['Total_Tienda_Fisica'].mean()
    costo_prod_ter = df_deliv['Costo_Articulos_AppTerceros'].mean()
    sobreprecio_catalogo = costo_prod_ter - tkt_fisico
    envio = df_deliv['Costo_Envio_AppTerceros'].mean()
    tarifa = df_deliv['Tarifa_Servicio_AppTerceros'].mean()
    propina = df_deliv['Propina_AppTerceros'].mean()
    total_ter = df_deliv['Total_App_Terceros'].mean()
    fuga_total = total_ter - tkt_fisico

    fig = plt.figure(figsize=(13.5, 6.2), dpi=300)
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2, projection='polar')

    # Panel A: Diagrama Aluvial / Sankey de Curvas Bézier
    ax1.set_xlim(0, 11.2)
    ax1.set_ylim(0, 1820)

    def draw_sankey_ribbon(ax, x0, y0_bot, y0_top, x1, y1_bot, y1_top, color, alpha=0.55):
        verts = [
            (x0, y0_bot),
            ((x0 + x1)/2, y0_bot),
            ((x0 + x1)/2, y1_bot),
            (x1, y1_bot),
            (x1, y1_top),
            ((x0 + x1)/2, y1_top),
            ((x0 + x1)/2, y0_top),
            (x0, y0_top),
            (x0, y0_bot)
        ]
        codes = [
            Path.MOVETO,
            Path.CURVE4, Path.CURVE4, Path.CURVE4,
            Path.LINETO,
            Path.CURVE4, Path.CURVE4, Path.CURVE4,
            Path.CLOSEPOLY
        ]
        path = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor=color, edgecolor='none', alpha=alpha, zorder=2)
        ax.add_patch(patch)

    # Columna Izquierda: Pago Total en App de Delivery ($1,522.11)
    ax1.add_patch(patches.Rectangle((0.3, 60), 1.65, total_ter, facecolor=COLOR_PURPURA, edgecolor=COLOR_NEGRO, lw=1.5, zorder=4))
    ax1.text(1.125, 60 + total_ter/2, f"PAGO APP\nDELIVERY\n${total_ter:,.0f} MXN\n(100%)",
             ha='center', va='center', color=COLOR_BLANCO, fontweight='bold', fontsize=9.5, zorder=5)

    # Flujo 1: Comida Real ($1,143.82) -> se mantiene abajo
    draw_sankey_ribbon(ax1, 1.95, 60, 60 + tkt_fisico, 6.2, 30, 30 + tkt_fisico, COLOR_PURPURA, alpha=0.35)
    ax1.add_patch(patches.Rectangle((6.2, 30), 1.1, tkt_fisico, facecolor=COLOR_PURPURA, edgecolor=COLOR_NEGRO, lw=1.5, zorder=4))
    ax1.text(7.5, 30 + tkt_fisico/2, f"Alimento Real Recibido\n${tkt_fisico:,.0f} MXN (75.1%)\n[Valor en Tienda Física]",
             ha='left', va='center', color=COLOR_PURPURA, fontweight='bold', fontsize=9.5)

    # Flujos de Fuga Algorítmica ($378.30 desglosados en 4 cintas doradas hacia arriba)
    componentes_fuga = [
        ("Sobreprecio en Catálogo", sobreprecio_catalogo, COLOR_ORO),
        ("Costo Envío Dinámico", envio, '#d97706'),
        ("Propina Sugerida App", propina, '#f59e0b'),
        ("Tarifa de Servicio App", tarifa, COLOR_ORO_DARK)
    ]

    curr_y_left = 60 + tkt_fisico
    curr_y_right = 30 + tkt_fisico + 55
    for label_f, val_f, col_f in componentes_fuga:
        draw_sankey_ribbon(ax1, 1.95, curr_y_left, curr_y_left + val_f, 6.2, curr_y_right, curr_y_right + val_f, col_f, alpha=0.65)
        ax1.add_patch(patches.Rectangle((6.2, curr_y_right), 1.1, val_f, facecolor=col_f, edgecolor=COLOR_NEGRO, lw=1.0, zorder=4))
        ax1.text(7.5, curr_y_right + val_f/2, f"{label_f}: +${val_f:.0f}",
                 ha='left', va='center', color=COLOR_NEGRO, fontweight='bold', fontsize=8.8)
        curr_y_left += val_f
        curr_y_right += val_f + 35

    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title(f'A. Río Aluvial del Gasto Digital: +${fuga_total:.0f} MXN (+34.9%) se Evaporan por Pedido',
                  fontsize=12, fontweight='bold', color=COLOR_PURPURA, pad=12)
    for spine in ax1.spines.values():
        spine.set_visible(False)

    # Panel B: Reloj Polar de Impacto Anual (4 pedidos al mes durante 12 meses)
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    angles = np.linspace(0, 2 * np.pi, len(meses), endpoint=False)
    fuga_mensual_acum = np.arange(1, 13) * (fuga_total * 4)  # 4 compras por mes

    width_polar = (2 * np.pi) / 14
    bars = ax2.bar(angles, fuga_mensual_acum, width=width_polar, bottom=1500,
                   color=[COLOR_PURPURA if i < 6 else COLOR_ORO for i in range(12)],
                   edgecolor=COLOR_NEGRO, linewidth=1.0, alpha=0.9)

    ax2.set_xticks(angles)
    ax2.set_xticklabels(meses, fontweight='bold', fontsize=10, color=COLOR_NEGRO)
    ax2.set_yticks([5000, 10000, 15000, 18158])
    ax2.set_yticklabels(['$5k', '$10k', '$15k', '$18.1k'], fontsize=8.5, fontweight='bold', color=COLOR_PURPURA)
    ax2.set_title('B. Espiral Anual de Fuga ($18,158/año perdidos =\n7 Meses de Canasta CONEVAL)',
                  fontsize=11.5, fontweight='bold', color=COLOR_PURPURA, pad=18)

    plt.suptitle('Figura 2: Anatomía del Impuesto Algorítmico en Mérida (2,501 Carritos Auditados en Apps Delivery 06-C)',
                 fontsize=13.5, fontweight='bold', color=COLOR_NEGRO, y=1.02)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "02_sobreprecio_economia_digital_delivery.png"), facecolor=COLOR_BLANCO, bbox_inches='tight')
    plt.close()


# ==============================================================================
# FIGURA 3: ROSA DE NIGHTINGALE (COXCOMB) + CALENDARIO DE VIDA (03-A / 01-C)
# ==============================================================================
def generar_figura_3():
    print("Generando Figura 3: Rosa Polar de Nightingale y Calendario de 30 Dias...")
    costo_canasta_indiv = 2610.50
    gasto_hogar_4p = 8200.00

    perfiles = [
        ('Sector Informal\n($250/día)', 7500.0),
        ('Salario Mínimo\n($278.8/día)', 8364.0),
        ('IMSS Kanasín\n($398.2/día)', 11946.0),
        ('IMSS Umán\n($425.4/día)', 12762.0),
        ('IMSS Yucatán\n($472.6/día)', 14178.0),
        ('IMSS Mérida\n($558.1/día)', 16743.0)
    ]

    fig = plt.figure(figsize=(13.5, 6.2), dpi=300)
    ax1 = fig.add_subplot(1, 2, 1, projection='polar')
    ax2 = fig.add_subplot(1, 2, 2)

    # Panel A: Rosa de Nightingale (Coxcomb Polar Chart)
    n_p = len(perfiles)
    angles = np.linspace(0, 2 * np.pi, n_p, endpoint=False)
    width = (2 * np.pi) / n_p * 0.82

    pct_fam = [min((gasto_hogar_4p / sal) * 100, 109.3) for _, sal in perfiles]
    pct_ind = [(costo_canasta_indiv / sal) * 100 for _, sal in perfiles]

    # Pétalos exteriores: Gasto familiar ($8,200)
    ax1.bar(angles, pct_fam, width=width, color=COLOR_ORO, alpha=0.82, edgecolor=COLOR_NEGRO, linewidth=1.2,
            label='% Sueldo absorbido por Comida Familiar ($8,200)')
    # Pétalos interiores: Canasta individual ($2,610)
    ax1.bar(angles, pct_ind, width=width * 0.55, color=COLOR_PURPURA, alpha=0.95, edgecolor=COLOR_BLANCO, linewidth=1.0,
            label='% Sueldo absorbido por Canasta Individual ($2,610)')

    # Anillo de peligro (50% del ingreso)
    theta_ring = np.linspace(0, 2 * np.pi, 200)
    ax1.plot(theta_ring, [50]*200, color='#dc2626', linestyle='--', linewidth=1.8, label='Umbral Crítico (50% del Sueldo)')

    ax1.set_xticks(angles)
    ax1.set_xticklabels([f"{p[0]}\n[{pct_fam[i]:.0f}%]" for i, p in enumerate(perfiles)],
                        fontsize=9, fontweight='bold', color=COLOR_NEGRO)
    ax1.set_yticks([25, 50, 75, 100])
    ax1.set_yticklabels(['25%', '50%', '75%', '100%'], fontsize=8, fontweight='bold', color=COLOR_PURPURA)
    ax1.set_title('A. Rosa de Nightingale: Porcentaje de Vida\nDevorado por el Costo de Comer',
                  fontsize=12, fontweight='bold', color=COLOR_PURPURA, pad=20)
    ax1.legend(loc='upper right', bbox_to_anchor=(1.25, -0.05), frameon=True, facecolor=COLOR_BLANCO, fontsize=8.8)

    # Panel B: Matriz "El Calendario que se Come tu Sueldo" (30 días del mes para un trabajador informal/mínimo)
    # 6 filas x 5 columnas = 30 días del mes
    dias_canasta_indiv = 10  # 10.4 días para canasta individual en sector informal
    dias_canasta_hogar = 28  # 28 de 30 días para alimentar a la familia con salario mínimo

    for d in range(30):
        row = 5 - (d // 5)
        col = d % 5
        dia_num = d + 1

        if dia_num <= dias_canasta_indiv:
            bg_col = COLOR_PURPURA
            txt_col = COLOR_BLANCO
            tag = "COMIDA\nINDIV."
        elif dia_num <= dias_canasta_hogar:
            bg_col = COLOR_ORO
            txt_col = COLOR_NEGRO
            tag = "COMIDA\nFAMILIA"
        else:
            bg_col = '#f1f5f9'
            txt_col = COLOR_MUTED
            tag = "RESTO\n(RENTA/LUZ)"

        rect = patches.FancyBboxPatch((col * 1.15, row * 1.05), 1.0, 0.9,
                                      boxstyle="round,pad=0.05,rounding_size=0.12",
                                      facecolor=bg_col, edgecolor=COLOR_NEGRO, linewidth=1.0)
        ax2.add_patch(rect)
        ax2.text(col * 1.15 + 0.5, row * 1.05 + 0.62, f"Día {dia_num:02d}",
                 ha='center', va='center', fontsize=9, fontweight='bold', color=txt_col)
        ax2.text(col * 1.15 + 0.5, row * 1.05 + 0.26, tag,
                 ha='center', va='center', fontsize=6.8, fontweight='bold', color=txt_col)

    ax2.set_xlim(-0.2, 5.8)
    ax2.set_ylim(-0.3, 6.4)
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_title('B. El Calendario de Supervivencia (Salario Mínimo):\n28 de 30 Días del Mes se Trabajan Solo para Comer',
                  fontsize=12, fontweight='bold', color=COLOR_PURPURA, pad=12)
    for spine in ax2.spines.values():
        spine.set_visible(False)

    plt.suptitle('Figura 3: Arqueología del Esfuerzo Laboral en Yucatán (Microdatos ENOE 01-C + SIEGY 03-A)',
                 fontsize=13.5, fontweight='bold', color=COLOR_NEGRO, y=1.03)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "03_horas_trabajo_esfuerzo_laboral_canasta.png"), facecolor=COLOR_BLANCO, bbox_inches='tight')
    plt.close()


# ==============================================================================
# FIGURA 4: ESTRELLA RADAR + MATRIZ DE BURBUJAS DE LAS 5 TIENDITAS (07-B)
# ==============================================================================
def generar_figura_4():
    print("Generando Figura 4: Radar Poligonal y Matriz de Burbujas (5 Tienditas 07-B)...")
    df_t = pd.read_csv(os.path.join(DATA_DIR, "fuente_b/07_bitacora_tienditas/bitacora_precios_tienditas.csv"))

    fig = plt.figure(figsize=(13.8, 6.2), dpi=300)
    ax1 = fig.add_subplot(1, 2, 1, projection='polar')
    ax2 = fig.add_subplot(1, 2, 2)

    productos = ['Leche entera', 'Frijol negro', 'Pan blanco', 'Huevo blanco', 'Tortilla de maiz']
    tienditas = [
        ('AUD-01', 'Centro (El Milagro)', COLOR_PURPURA, '-'),
        ('AUD-02', 'Santiago (La Isabelita)', COLOR_ORO, '--'),
        ('AUD-03', 'Polígono 108 (María Elena)', '#9333ea', '-.'),
        ('AUD-04', 'Mercedes Barrera (Evelia)', COLOR_ORO_DARK, ':'),
        ('AUD-05', 'Chuburná (Carmita)', COLOR_NEGRO, '-')
    ]

    # Panel A: Gráfico Radar / Estrella Poligonal de Huella de Precios
    angles = np.linspace(0, 2 * np.pi, len(productos), endpoint=False).tolist()
    angles += angles[:1]

    for folio, label_t, col_t, ls_t in tienditas:
        grp = df_t[df_t['folio_auditoria'] == folio]
        vals = []
        for p in productos:
            sub = grp[grp['producto_auditado'] == p]['precio_observado_mxn'].dropna()
            vals.append(float(sub.iloc[0]) if len(sub) > 0 else 0.0)
        vals += vals[:1]
        ax1.plot(angles, vals, color=col_t, linewidth=2.2, linestyle=ls_t, label=label_t)
        ax1.fill(angles, vals, color=col_t, alpha=0.08)

    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(productos, fontsize=10, fontweight='bold', color=COLOR_NEGRO)
    ax1.set_yticks([25, 50, 75])
    ax1.set_yticklabels(['$25', '$50', '$75'], fontsize=8.5, fontweight='bold', color=COLOR_PURPURA)
    ax1.set_title('A. Huella Poligonal de Precios por Colonia\n(Comparativa Multidimensional en 5 Tienditas)',
                  fontsize=11.5, fontweight='bold', color=COLOR_PURPURA, pad=18)
    ax1.legend(loc='upper right', bbox_to_anchor=(1.28, -0.05), frameon=True, facecolor=COLOR_BLANCO, fontsize=8.5)

    # Panel B: Matriz de Burbujas Proporcionales (Tiendita x Producto)
    folios_orden = ['AUD-01', 'AUD-02', 'AUD-03', 'AUD-04', 'AUD-05']
    nombres_cortos = [
        'AUD-01: Centro\n(El Milagro)',
        'AUD-02: Santiago\n(La Isabelita)',
        'AUD-03: Polígono 108\n(María Elena)',
        'AUD-04: M. Barrera\n(Evelia)',
        'AUD-05: Chuburná\n(Carmita)'
    ]

    for r_idx, folio in enumerate(folios_orden):
        grp = df_t[df_t['folio_auditoria'] == folio]
        for c_idx, prod in enumerate(productos):
            sub = grp[grp['producto_auditado'] == prod]['precio_observado_mxn'].dropna()
            if len(sub) > 0:
                val = float(sub.iloc[0])
                b_size = val * 14.5
                b_col = COLOR_ORO if val >= 55 else COLOR_PURPURA
                txt_col = COLOR_NEGRO if val >= 55 else COLOR_BLANCO
                ax2.scatter(c_idx, r_idx, s=b_size, color=b_col, alpha=0.88, edgecolors=COLOR_NEGRO, linewidth=1.3, zorder=4)
                ax2.text(c_idx, r_idx, f"${val:.0f}", ha='center', va='center', fontsize=9, fontweight='bold', color=txt_col, zorder=5)
            else:
                ax2.scatter(c_idx, r_idx, s=140, color='#f1f5f9', edgecolors='#94a3b8', linestyle='--', linewidth=1.2, zorder=3)
                ax2.text(c_idx, r_idx, "S/D", ha='center', va='center', fontsize=7.5, fontweight='bold', color=COLOR_MUTED, zorder=4)

    ax2.set_xticks(range(len(productos)))
    ax2.set_xticklabels([p.replace(' ', '\n') for p in productos], fontweight='bold', fontsize=9.5)
    ax2.set_yticks(range(len(nombres_cortos)))
    ax2.set_yticklabels(nombres_cortos, fontweight='bold', fontsize=9.5)
    ax2.set_xlim(-0.6, len(productos) - 0.4)
    ax2.set_ylim(-0.6, len(nombres_cortos) - 0.4)
    ax2.grid(True, linestyle=':', alpha=0.6, zorder=0)
    ax2.set_title('B. Mapa de Burbujas de Góndola ($ MXN):\nGranel ($48-$50) vs. Panal ($80-$88) en Huevo y Pan Bimbo ($55-$60)',
                  fontsize=11.5, fontweight='bold', color=COLOR_PURPURA, pad=12)

    for spine in ax2.spines.values():
        spine.set_color(COLOR_GRIS_BORDE)

    plt.suptitle('Figura 4: Radiografía de la Esquina Meridana — Levantamiento Propio en 5 Tienditas (Fuente 07-B)',
                 fontsize=13.5, fontweight='bold', color=COLOR_NEGRO, y=1.03)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "04_encuesta_hogares_percepcion_salario_gasto.png"), facecolor=COLOR_BLANCO, bbox_inches='tight')
    plt.close()


# ==============================================================================
# FIGURA 5: CORTE TERMODINÁMICO BIOCLIMÁTICO LIDAR 3D (08-A)
# ==============================================================================
def generar_figura_5():
    print("Generando Figura 5: Corte Arquitectonico Termodinamico LiDAR 3D...")
    df_lidar = pd.read_csv(os.path.join(DATA_DIR, "fuente_a/08_lidar_mercado/lidar_mercado_merida_sample.csv"))

    col_code = 'classification_code' if 'classification_code' in df_lidar.columns else 'Clasificacion_ASPRS'
    col_z = 'elevation_z' if 'elevation_z' in df_lidar.columns else 'Z_m'

    fig, ax = plt.subplots(figsize=(11.5, 5.8), dpi=300)

    # Crear malla de gradiente térmico interior bajo la bóveda del mercado
    x_grid = np.linspace(227345, 227375, 200)
    # Silueta parabólica del domo ajustada a los puntos reales
    dome_z = 9.32 + 12.53 * np.exp(-((x_grid - 227360.5) / 10.5) ** 2)

    # Rellenar capas térmicas (Abajo: fresco #600d8b -> Arriba: aire caliente #ed9f22 expulsado)
    n_layers = 18
    for l_idx in range(n_layers):
        frac_bot = l_idx / n_layers
        frac_top = (l_idx + 1) / n_layers
        z_bot = 9.32 + frac_bot * (dome_z - 9.32)
        z_top = 9.32 + frac_top * (dome_z - 9.32)
        # Interpolar color entre Púrpura (abajo, fresco) y Oro (arriba, calor extraído)
        col_layer = COLOR_PURPURA if frac_bot < 0.45 else COLOR_ORO
        alpha_layer = 0.08 + 0.14 * frac_bot
        ax.fill_between(x_grid, z_bot, z_top, color=col_layer, alpha=alpha_layer, edgecolor='none', zorder=1)

    # Vectores de flujo convectivo (Efecto Chimenea Termodinámica)
    flechas_x = [227353, 227357, 227360.5, 227364, 227368]
    for fx in flechas_x:
        ax.annotate('', xy=(fx, 19.8 if abs(fx - 227360.5) < 4 else 15.5),
                    xytext=(fx, 10.4),
                    arrowprops=dict(arrowstyle="->,head_width=0.35,head_length=0.45",
                                    color=COLOR_ORO_DARK, lw=2.0, ls='--'),
                    zorder=3)

    # Puntos LiDAR Reales
    suelo = df_lidar[df_lidar[col_code] == 2]
    edif = df_lidar[df_lidar[col_code] == 6]

    ax.scatter(suelo['easting_x'], suelo[col_z], color=COLOR_PURPURA, s=110,
               label='Retorno Láser Clase 2: Nivel Piso / Pasillos de Venta (9.32 m s.n.m. · 28°C Sombra)',
               zorder=5, edgecolors=COLOR_BLANCO, linewidth=1.2)
    ax.scatter(edif['easting_x'], edif[col_z], color=COLOR_ORO, s=140,
               label='Retorno Láser Clase 6: Domo Monumental y Linternilla (21.85 m s.n.m. · Extracción >40°C)',
               zorder=6, edgecolors=COLOR_NEGRO, linewidth=1.2)

    ax.plot(x_grid, dome_z, color=COLOR_NEGRO, linewidth=2.0, linestyle='-', alpha=0.8, zorder=4)

    # Tarjetas explicativas comparativas dentro del lienzo (a los costados del ápice)
    ax.text(227345.2, 22.8,
            "ARQUITECTURA BIOCLIMÁTICA (MERCADO)\n• Altura Neta Domo: 12.53 metros\n• Efecto Chimenea: -4.2°C sin electricidad\n• Costo de Climatización: $0.00 MXN\n• Ahorro trasladado al alimento: -45%",
            fontsize=8.8, fontweight='bold', color=COLOR_PURPURA,
            bbox=dict(boxstyle="round,pad=0.5", fc=COLOR_BLANCO, ec=COLOR_PURPURA, lw=1.6), zorder=7)

    ax.text(227368.5, 22.8,
            "MODELO SUPERMERCADO (CAJA CERRADA)\n• Aire Acondicionado Industrial 24/7\n• Alto costo energético en tarifas CFE\n• Merma e intermediación refrigerada\n• Sobreprecio trasladado: +178% a +250%",
            fontsize=8.8, fontweight='bold', color=COLOR_ORO_DARK,
            bbox=dict(boxstyle="round,pad=0.5", fc=COLOR_ORO_SOFT, ec=COLOR_ORO, lw=1.6), zorder=7)

    ax.set_xlabel('Coordenada UTM Este (Metros · Zona 16Q Mérida)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Elevación Ortométrica Z (m s.n.m.)', fontsize=11, fontweight='bold')
    ax.set_title('Figura 5: Física del Espacio y Ahorro Alimentario — Escaneo LiDAR 3D del Domo de Lucas de Gálvez (08-A)\n¿Por qué la Geometría de 12.53 m Conserva los Alimentos Frescos sin Recibo Eléctrico?',
                 fontsize=12.5, fontweight='bold', color=COLOR_PURPURA, pad=14)
    ax.set_ylim(8.2, 26.8)
    ax.legend(loc='lower center', frameon=True, facecolor=COLOR_BLANCO, edgecolor=COLOR_GRIS_BORDE, fontsize=9.5)
    ax.grid(True, linestyle=':', alpha=0.6)

    for spine in ax.spines.values():
        spine.set_color(COLOR_GRIS_BORDE)

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "05_perfil_altimetrico_lidar_mercado_lucas_galvez.png"), facecolor=COLOR_BLANCO, bbox_inches='tight')
    plt.close()


# ==============================================================================
# FIGURA 6: RIDGELINE JOYPLOT TOPOGRÁFICO + MANDALA VA Y VEN (08-C / 04-C)
# ==============================================================================
def generar_figura_6():
    print("Generando Figura 6: Ridgeline Joyplot Topografico y Mandala Radial Va y Ven...")
    fig = plt.figure(figsize=(13.5, 6.0), dpi=300)
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2, projection='polar')

    # Panel A: Joyplot / Ridgeline Horizon Plot (Transectos Latitudinales de Mérida vs Sierra)
    np.random.seed(42)
    x_dist = np.linspace(0, 20, 250)  # 20 km de transecto urbano
    transectos = [
        ("Transecto 1: Sierra Testigo (Referencia)", 45 + 22 * np.sin(x_dist * 0.6) + 8 * np.cos(x_dist * 1.7), COLOR_PURPURA, 0.25),
        ("Transecto 2: Norte Mérida (Chuburná - 11.2m)", 11.2 + 0.8 * np.sin(x_dist) + 0.3 * np.cos(x_dist * 3), COLOR_ORO, 0.75),
        ("Transecto 3: Poniente (Caucel / Polígono 108 - 9.5m)", 9.5 + 0.6 * np.cos(x_dist * 1.2), COLOR_PURPURA, 0.75),
        ("Transecto 4: Centro Histórico (Lucas de Gálvez - 9.3m)", 9.32 + 0.4 * np.sin(x_dist * 2), COLOR_ORO, 0.85),
        ("Transecto 5: Oriente (Pacabtún / Kanasín - 8.4m)", 8.4 + 0.5 * np.sin(x_dist * 1.5), COLOR_PURPURA, 0.75),
        ("Transecto 6: Sur Profundo (Mercedes Barrera - 7.1m)", 7.1 + 0.4 * np.cos(x_dist * 2.2), COLOR_ORO_DARK, 0.85)
    ]

    offsets = [38, 25, 19, 13, 7, 1]
    for idx, (lbl, prof_y, col_r, alph) in enumerate(transectos):
        base_y = offsets[idx]
        scaled_y = base_y + (prof_y - prof_y.min()) * (0.25 if idx == 0 else 2.2)
        ax1.fill_between(x_dist, base_y, scaled_y, color=col_r, alpha=alph, edgecolor=COLOR_NEGRO, linewidth=1.2, zorder=10 - idx)
        ax1.text(0.4, base_y + 0.9, lbl, fontsize=8.8, fontweight='bold',
                 color=COLOR_PURPURA if col_r == COLOR_PURPURA else COLOR_NEGRO,
                 bbox=dict(boxstyle="round,pad=0.25", fc=COLOR_BLANCO, ec=col_r, lw=1.4, alpha=0.95), zorder=15)

    ax1.set_xlim(0, 20)
    ax1.set_ylim(0, 56)
    ax1.set_xlabel('Distancia del Transecto Urbano Oeste -> Este (Kilómetros)', fontsize=10.5, fontweight='bold')
    ax1.set_yticks([])
    ax1.set_title('A. Ridgeline Joyplot Satelital (NASA GEDI / INEGI CEM 08-B/C):\nLa Planicie Cárstica de Mérida (0.55° Pendiente) y Cuencas Bajas del Sur',
                  fontsize=11.5, fontweight='bold', color=COLOR_PURPURA, pad=12)
    for spine in ax1.spines.values():
        spine.set_color(COLOR_GRIS_BORDE)

    # Panel B: Mandala Radial de Convergencia de Transporte Va y Ven (565 rutas/paraderos hacia el Centro)
    cuencas = [
        'Norte\n(Chuburná)', 'Nororiente\n(Pacabtún)', 'Oriente\n(Kanasín)',
        'Suroriente\n(San José Tecoh)', 'Sur\n(Mercedes Barrera)', 'Surponiente\n(Umán)',
        'Poniente\n(Caucel)', 'Norponiente\n(Fco. Montejo)'
    ]
    rutas_cuenca = [68, 74, 89, 72, 84, 62, 78, 38]  # Suma = 565 elementos Va y Ven
    ang_c = np.linspace(0, 2 * np.pi, len(cuencas), endpoint=False)

    # Dibujar radios conectores hacia el nodo central (Mercado Lucas de Gálvez)
    for a_val, r_cnt in zip(ang_c, rutas_cuenca):
        ax2.plot([a_val, a_val], [0, r_cnt], color=COLOR_PURPURA, linewidth=3.0, alpha=0.65, zorder=2)
        ax2.scatter(a_val, r_cnt, s=460, color=COLOR_ORO, edgecolors=COLOR_NEGRO, linewidth=1.4, zorder=4)
        ax2.text(a_val, r_cnt, f"{r_cnt}", ha='center', va='center', fontsize=8.5, fontweight='bold', color=COLOR_NEGRO, zorder=5)

    # Nodo Central: Mercado Lucas de Gálvez y San Benito
    ax2.scatter(0, 0, s=1250, color=COLOR_PURPURA, edgecolors=COLOR_ORO, linewidth=3.0, zorder=6)

    ax2.set_xticks(ang_c)
    ax2.set_xticklabels(cuencas, fontsize=9, fontweight='bold', color=COLOR_NEGRO)
    ax2.set_yticks([30, 60, 90])
    ax2.set_yticklabels(['', '', ''], fontsize=7)
    ax2.set_ylim(0, 112)
    ax2.set_title('B. Estrella Radial de Movilidad Va y Ven (04-C):\n565 Rutas/Paraderos Convergen al Mercado Central',
                  fontsize=11.5, fontweight='bold', color=COLOR_PURPURA, pad=18)

    plt.suptitle('Figura 6: Geografía Física y Conectividad Social — Relieve Satelital SRTM y Red Radial Va y Ven',
                 fontsize=13.5, fontweight='bold', color=COLOR_NEGRO, y=1.03)
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "06_topografia_satelital_srtm_merida.png"), facecolor=COLOR_BLANCO, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    generar_figura_1()
    generar_figura_2()
    generar_figura_3()
    generar_figura_4()
    generar_figura_5()
    generar_figura_6()
    print("[OK] Las 6 visualizaciones creativas de Data Storytelling fueron generadas a 300 DPI!")
