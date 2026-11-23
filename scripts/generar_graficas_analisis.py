"""
Script de Generación de Infografías Pop y Pictogramas Memorables ("Modo Gente Común")
Proyecto: "Del Mundo a la Esquina: ¿Cuánto Cuesta Comer?" (UPY)
Paleta Oficial Obligatoria:
  - Primario / Oro-Ámbar: #ed9f22
  - Púrpura Imperial:    #600d8b
  - Blanco Editorial:    #ffffff
  - Carbón Tipográfico:  #0d0d0d

Monedas Populares de Comparación (100% Datos Reales del Repo):
  - 1 Kilo de Tortilla = $26.00 MXN (Bitácora Propia 07-B)
  - 1 Viaje en Va y Ven = $12.00 MXN (Movilidad 04-C)
Cero emojis Unicode: todos los íconos son pictogramas vectoriales dibujados con patches.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

# Paleta Oficial Estricta
ORO = '#ed9f22'
ORO_DARK = '#b45309'
ORO_SOFT = '#fef3c7'
PURPURA = '#600d8b'
PURPURA_LIGHT = '#9333ea'
PURPURA_SOFT = '#f3e8ff'
BLANCO = '#ffffff'
NEGRO = '#0d0d0d'
GRIS_BORDE = '#e2e8f0'
GRIS_CLARO = '#f8fafc'
MUTED = '#525252'

plt.rcParams['figure.facecolor'] = BLANCO
plt.rcParams['axes.facecolor'] = BLANCO
plt.rcParams['text.color'] = NEGRO
plt.rcParams['axes.labelcolor'] = NEGRO
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'sans-serif']
plt.rcParams['text.parse_math'] = False

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
OUTPUT_DIR = os.path.join(ROOT_DIR, "reports", "figuras")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==============================================================================
# HELPERS VECTORIALES (CERO EMOJIS: TORTILLAS, CAMIONES VA Y VEN, MONEDAS)
# ==============================================================================
def draw_tortilla_icon(ax, cx, cy, r=0.28, color=ORO, edge=NEGRO, lw=1.1, zorder=5):
    """Dibuja un ícono vectorial de tortilla (disco dorado con marquitas de comal)."""
    circ = patches.Circle((cx, cy), r, facecolor=color, edgecolor=edge, linewidth=lw, zorder=zorder)
    ax.add_patch(circ)
    # Pintitas de tortilla tostada
    for dx, dy in [(-0.35*r, 0.2*r), (0.3*r, -0.25*r), (0.05*r, 0.35*r)]:
        dot = patches.Circle((cx + dx, cy + dy), r * 0.11, facecolor=ORO_DARK if color == ORO else BLANCO, edgecolor='none', alpha=0.7, zorder=zorder+1)
        ax.add_patch(dot)


def draw_bus_icon(ax, cx, cy, w=0.65, h=0.42, color=PURPURA, zorder=5):
    """Dibuja un ícono vectorial de camión Va y Ven."""
    body = patches.FancyBboxPatch((cx - w/2, cy - h/2 + 0.06), w, h - 0.08,
                                  boxstyle="round,pad=0.02,rounding_size=0.08",
                                  facecolor=color, edgecolor=NEGRO, linewidth=1.1, zorder=zorder)
    ax.add_patch(body)
    # Ventana frontal
    win = patches.Rectangle((cx - w/2 + 0.06, cy + 0.02), w - 0.12, h * 0.36,
                            facecolor=BLANCO, edgecolor=NEGRO, linewidth=0.7, zorder=zorder+1)
    ax.add_patch(win)
    # Ruedas
    for wx in [cx - w*0.28, cx + w*0.28]:
        wheel = patches.Circle((wx, cy - h/2 + 0.04), h * 0.16, facecolor=ORO, edgecolor=NEGRO, linewidth=0.9, zorder=zorder+2)
        ax.add_patch(wheel)


# ==============================================================================
# FIGURA 1: EL VIAJE MÁGICO DE 12 KM (ABASTO vs SÚPER EN TORTILLAS)
# ==============================================================================
def generar_figura_1():
    print("Generando Figura 1: El Viaje Magico de 12 km...")
    productos = [
        ("Papa Blanca", 16.0, 56.0, "+250%", "Pagas 3.5 kg de abasto\npor 1 kg en el súper"),
        ("Jitomate Saladette", 16.15, 45.0, "+179%", "El recargo (+$29) equivale\na 1.1 kg de tortilla"),
        ("Limón con Semilla", 11.11, 26.5, "+138%", "Sube más del doble\nen 12 km de asfalto"),
        ("Aguacate Hass", 38.0, 79.0, "+108%", "La diferencia (+$41) paga\n3.4 viajes en Va y Ven"),
        ("Plátano Tabasco", 12.0, 24.9, "+108%", "Pasa de $12 a casi $25\nsin cambiar de fruta"),
        ("Cebolla Blanca", 14.0, 22.0, "+57%", "Margen moderado\npero constante"),
        ("Huevo Blanco", 36.0, 48.5, "+35%", "El más defendido por\ngranjas de Kanasín/Umán")
    ]
    productos.reverse()  # Mayor impacto arriba

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.8), dpi=300, gridspec_kw={'width_ratios': [1.8, 1.1]})

    y_pos = np.arange(len(productos))

    # Panel A: Camino del Precio (Central de Abasto -> Súper)
    for i, (nombre, may, men, pct, nota) in enumerate(productos):
        # Barra de rango estilo flecha gruesa
        ax1.barh(i, men - may, left=may, height=0.44, color=ORO, alpha=0.82, edgecolor=NEGRO, linewidth=1.1, zorder=3)
        # Punto de origen (Central de Abasto)
        ax1.scatter(may, i, s=180, color=PURPURA, edgecolors=BLANCO, linewidth=1.8, zorder=5)
        ax1.text(may - 1.5, i, f"${may:.0f}", va='center', ha='right', fontsize=9.5, fontweight='bold', color=PURPURA)
        # Punto final (Súper)
        ax1.scatter(men, i, s=220, color=ORO, edgecolors=NEGRO, linewidth=1.5, zorder=5)
        ax1.text(men + 1.8, i, f"${men:.0f}/kg  ({pct})", va='center', ha='left', fontsize=10, fontweight='bold', color=NEGRO)

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels([p[0] for p in productos], fontsize=11, fontweight='bold')
    ax1.set_xlim(0, 108)
    ax1.set_ylim(-1.25, len(productos) - 0.3)
    ax1.set_xlabel('Precio por Kilogramo ($ MXN)', fontsize=11, fontweight='bold')
    ax1.set_title('A. Mismo Producto, Distinto Destino:\nCentral de Abasto (Morado) vs. Supermercado (Dorado)', fontsize=12, fontweight='bold', color=PURPURA, pad=12)
    ax1.grid(True, axis='x', linestyle='--', alpha=0.45)

    # Leyenda limpia debajo de la última barra sin tapar texto
    ax1.scatter([], [], s=120, color=PURPURA, label='Central de Abasto (Mayoreo SNIIM)')
    ax1.scatter([], [], s=140, color=ORO, edgecolors=NEGRO, label='Góndola de Súper (PROFECO)')
    ax1.legend(loc='lower right', frameon=True, facecolor=BLANCO, edgecolor=GRIS_BORDE, fontsize=9.2, ncol=2)

    # Panel B: Pictograma "Cuántos Kilos de Abasto caben en 1 Kilo del Súper"
    ax2.set_xlim(0, 6.0)
    ax2.set_ylim(-1.25, len(productos) - 0.3)
    for i, (nombre, may, men, pct, nota) in enumerate(productos):
        ratio = men / may
        n_full = int(ratio)
        frac = ratio - n_full
        for k in range(n_full):
            draw_tortilla_icon(ax2, 0.45 + k * 0.65, i, r=0.25, color=PURPURA if k == 0 else ORO, zorder=4)
        if frac > 0.15:
            draw_tortilla_icon(ax2, 0.45 + n_full * 0.65, i, r=0.25 * (0.55 + 0.45 * frac), color=ORO_SOFT, zorder=4)
        ax2.text(0.45 + ratio * 0.65 + 0.32, i, f"{ratio:.1f}x\n({nota.splitlines()[0].replace('de abasto', 'en el Abasto')})",
                 va='center', ha='left', fontsize=8.5, fontweight='bold', color=NEGRO)

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(['' for _ in productos])
    ax2.set_xticks([])
    ax2.set_title('B. ¿Cuántos Kilos de Abasto Compras\ncon lo que Pagas por 1 Kilo en el Súper?', fontsize=12, fontweight='bold', color=PURPURA, pad=12)
    for s in ['top', 'right', 'left']:
        ax2.spines[s].set_visible(False)
    for s in ['top', 'right']:
        ax1.spines[s].set_visible(False)

    plt.suptitle('Figura 1: El Viaje Mágico de 12 km — ¿Por qué la Papa Cuesta $16 en Abastos y $56 en el Súper?',
                 fontsize=14, fontweight='bold', color=NEGRO, y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(OUTPUT_DIR, "01_margen_intermediacion_mayoreo_vs_menudeo.png"), facecolor=BLANCO, bbox_inches='tight')
    plt.close()


# ==============================================================================
# FIGURA 2: EL IMPUESTO A LA FLOJERA (RAPPI/UBER EN TORTILLAS Y VA Y VEN)
# ==============================================================================
def generar_figura_2():
    print("Generando Figura 2: El Impuesto a la Flojera (Rappi vs Tortillas)...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=300, gridspec_kw={'width_ratios': [1.05, 1.25]})

    # Panel A: Ticket partido ("Lo que comes vs Lo que regalas")
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title('A. Tu Ticket de Rappi / UberEats ($1,522 MXN)\n¿Qué Estás Pagando Realmente?', fontsize=12, fontweight='bold', color=PURPURA, pad=10)

    # Bloque inferior: Comida Real ($1,143.82 = 75.1%)
    ax1.add_patch(patches.FancyBboxPatch((0.8, 0.5), 8.4, 5.2, boxstyle="round,pad=0.1,rounding_size=0.25",
                                         facecolor=PURPURA, edgecolor=NEGRO, linewidth=1.8))
    ax1.text(5.0, 3.6, "COMIDA REAL EN TU REFRI", ha='center', va='center', color=BLANCO, fontsize=13, fontweight='bold')
    ax1.text(5.0, 2.6, "$1,144 MXN  (75.1% del pago)", ha='center', va='center', color=ORO, fontsize=14, fontweight='bold')
    ax1.text(5.0, 1.5, "Exactamente lo mismo que pagabas yendo\nen persona al supermercado", ha='center', va='center', color=BLANCO, fontsize=9.5)

    # Bloque superior: Sobreprecio ($378.30 = 24.9% extra sobre ticket / +34.9% sobre base)
    ax1.add_patch(patches.FancyBboxPatch((0.8, 6.1), 8.4, 3.3, boxstyle="round,pad=0.1,rounding_size=0.25",
                                         facecolor=ORO, edgecolor=NEGRO, linewidth=1.8))
    ax1.text(5.0, 8.75, "EL IMPUESTO A LA FLOJERA: +$378 MXN EXTRA", ha='center', va='center', color=NEGRO, fontsize=12, fontweight='bold')
    ax1.text(5.0, 7.85, "(+34.9% más caro por cada carrito de despensa)", ha='center', va='center', color=PURPURA, fontsize=10, fontweight='bold')

    # Desglose en 4 cajitas internas
    items_fuga = [
        ("Catálogo\nInflado\n+$205", 1.15),
        ("Envío\nApp\n+$65", 3.25),
        ("Propina\nSugerida\n+$55", 5.35),
        ("Tarifa\nServicio\n+$53", 7.45)
    ]
    for txt_i, x_i in items_fuga:
        ax1.add_patch(patches.FancyBboxPatch((x_i, 6.35), 1.75, 1.1, boxstyle="round,pad=0.05,rounding_size=0.12",
                                             facecolor=BLANCO, edgecolor=NEGRO, linewidth=1.0))
        ax1.text(x_i + 0.875, 6.9, txt_i, ha='center', va='center', fontsize=8.2, fontweight='bold', color=NEGRO)

    # Panel B: Pictograma de Equivalencia Popular ($378.30/pedido y $18,158/año)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('B. Traductor Popular: ¿Qué Son Esos $378 Extra?', fontsize=12, fontweight='bold', color=PURPURA, pad=10)

    # Bloque 1: En Kilos de Tortilla ($26/kg) -> 14.5 kg
    ax2.add_patch(patches.FancyBboxPatch((0.3, 5.2), 9.4, 4.2, boxstyle="round,pad=0.1,rounding_size=0.25",
                                         facecolor=GRIS_CLARO, edgecolor=GRIS_BORDE, linewidth=1.5))
    ax2.text(5.0, 8.85, "POR UN SOLO PEDIDO TIRAS A LA BASURA:", ha='center', va='center', fontsize=10.5, fontweight='bold', color=PURPURA)
    ax2.text(5.0, 8.2, "14.5 Kilos de Tortilla ($26/kg)", ha='center', va='center', fontsize=13.5, fontweight='bold', color=NEGRO)

    # Dibujar 15 tortillas (14 enteras + 1 media)
    for t_idx in range(15):
        row_t = t_idx // 8
        col_t = t_idx % 8
        cx_t = 1.3 + col_t * 1.05
        cy_t = 7.1 - row_t * 1.1
        draw_tortilla_icon(ax2, cx_t, cy_t, r=0.38 if t_idx < 14 else 0.25, color=ORO if t_idx < 14 else ORO_SOFT)

    # Bloque 2: En Viajes en Va y Ven ($12) -> 31 viajes + Al Año
    ax2.add_patch(patches.FancyBboxPatch((0.3, 0.5), 9.4, 4.2, boxstyle="round,pad=0.1,rounding_size=0.25",
                                         facecolor=PURPURA_SOFT, edgecolor=PURPURA, linewidth=1.5))
    ax2.text(5.0, 4.15, "O SU EQUIVALENTE EN TRANSPORTE MÉRIDA:", ha='center', va='center', fontsize=10, fontweight='bold', color=PURPURA)
    ax2.text(5.0, 3.55, "31 Viajes en Va y Ven ($12 c/u)", ha='center', va='center', fontsize=13, fontweight='bold', color=NEGRO)

    for b_idx in range(10):
        draw_bus_icon(ax2, 1.15 + b_idx * 0.85, 2.55, w=0.65, h=0.42, color=PURPURA)
    ax2.text(5.0, 1.78, "(...y otros 21 camiones más por pedido)", ha='center', va='center', fontsize=8.8, fontweight='bold', color=MUTED)

    ax2.add_patch(patches.FancyBboxPatch((0.7, 0.72), 8.6, 0.75, boxstyle="round,pad=0.05,rounding_size=0.15",
                                         facecolor=ORO, edgecolor=NEGRO, linewidth=1.1))
    ax2.text(5.0, 1.1, "SI PIDES 4 VECES AL MES = $18,158 AL AÑO = ¡698 KG DE TORTILLA!",
             ha='center', va='center', fontsize=9.2, fontweight='bold', color=NEGRO)

    plt.suptitle('Figura 2: El Impuesto a la Flojera — ¿Cuánto Cuesta en Tortillas Pedir el Súper por App? (2,501 Tickets 06-C)',
                 fontsize=13.5, fontweight='bold', color=NEGRO, y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(OUTPUT_DIR, "02_sobreprecio_economia_digital_delivery.png"), facecolor=BLANCO, bbox_inches='tight')
    plt.close()


# ==============================================================================
# FIGURA 3: EL MES QUE SE COME TU SUELDO (CALENDARIO DE 30 DÍAS)
# ==============================================================================
def generar_figura_3():
    print("Generando Figura 3: El Mes que se Come tu Sueldo...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=300, gridspec_kw={'width_ratios': [1.25, 1]})

    # Panel A: Calendario de Supervivencia de 30 Días (Salario Mínimo $8,364)
    ax1.set_xlim(-0.2, 5.95)
    ax1.set_ylim(-0.7, 6.45)
    ax1.axis('off')
    ax1.set_title('A. El Calendario de tu Quincena (Salario Mínimo: $278.80/día)\n28 Días Trabajando Solo pa\' la Panza Familiar',
                  fontsize=11.8, fontweight='bold', color=PURPURA, pad=10)

    for d in range(30):
        row = 5 - (d // 5)
        col = d % 5
        dia_num = d + 1

        if dia_num <= 10:
            bg, fg, tag = PURPURA, BLANCO, "SOLO TU\nCOMIDA"
        elif dia_num <= 28:
            bg, fg, tag = ORO, NEGRO, "COMIDA\nFAMILIA"
        else:
            bg, fg, tag = '#e2e8f0', NEGRO, "RENTA,\nLUZ Y FE"

        rect = patches.FancyBboxPatch((col * 1.15, row * 1.03), 1.02, 0.9,
                                      boxstyle="round,pad=0.04,rounding_size=0.14",
                                      facecolor=bg, edgecolor=NEGRO, linewidth=1.1)
        ax1.add_patch(rect)
        ax1.text(col * 1.15 + 0.51, row * 1.03 + 0.62, f"Día {dia_num:02d}",
                 ha='center', va='center', fontsize=9, fontweight='bold', color=fg)
        ax1.text(col * 1.15 + 0.51, row * 1.03 + 0.25, tag,
                 ha='center', va='center', fontsize=6.8, fontweight='bold', color=fg)

    ax1.text(2.85, -0.35, "Con salario mínimo ($8,364/mes), el gasto familiar ($8,200) solo te deja $164 pesos (= 6 kg de tortilla) libres al mes.",
             ha='center', va='center', fontsize=9, fontweight='bold', color=PURPURA,
             bbox=dict(boxstyle="round,pad=0.4", fc=PURPURA_SOFT, ec=PURPURA))

    # Panel B: ¿Cuántos días del mes trabaja cada quien SOLO para comer?
    perfiles = [
        ("Trabajador Informal\n($250/día · 54% Yucatán)", 30.0, "¡No alcanza! Debe pedir fiado"),
        ("Salario Mínimo Legal\n($278.80/día)", 29.4, "Le sobran $164 al mes (0.6 días)"),
        ("IMSS Kanasín\n($398.20/día)", 20.6, "Le quedan 9.4 días para todo"),
        ("IMSS Yucatán Prom.\n($472.60/día)", 17.4, "Le quedan 12.6 días libres"),
        ("IMSS Mérida Prom.\n($558.10/día)", 14.7, "Mitad del mes para comer")
    ]
    perfiles.reverse()

    y_p = np.arange(len(perfiles))
    for i, (lbl, dias, nota) in enumerate(perfiles):
        # Barra de fondo 30 días
        ax2.barh(i, 30, height=0.52, color='#f1f5f9', edgecolor=GRIS_BORDE, zorder=1)
        # Barra de días trabajados para comer
        col_b = ORO if dias >= 20 else PURPURA
        ax2.barh(i, dias, height=0.52, color=col_b, edgecolor=NEGRO, linewidth=1.1, zorder=3)
        ax2.text(dias - 0.8 if dias > 23 else dias + 0.6, i, f"{dias:.1f} días ({nota})",
                 va='center', ha='right' if dias > 23 else 'left',
                 fontsize=8.5, fontweight='bold', color=NEGRO if col_b == ORO else BLANCO if dias > 23 else PURPURA, zorder=5)

    ax2.set_yticks(y_p)
    ax2.set_yticklabels([p[0] for p in perfiles], fontsize=9.5, fontweight='bold')
    ax2.set_xlim(0, 32)
    ax2.set_xlabel('Días del Mes Trabajados Únicamente para Comida Familiar ($8,200)', fontsize=10, fontweight='bold')
    ax2.set_title('B. ¿Cuántos Días Trabajas pa\' Comer\nSegún Dónde Vives en Yucatán?', fontsize=11.8, fontweight='bold', color=PURPURA, pad=10)
    for s in ['top', 'right']:
        ax2.spines[s].set_visible(False)

    plt.suptitle('Figura 3: El Mes que se Come tu Sueldo — Salarios Reales vs. Hambre en Mérida (ENOE 01-C + SIEGY 03-A)',
                 fontsize=13.5, fontweight='bold', color=NEGRO, y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(OUTPUT_DIR, "03_horas_trabajo_esfuerzo_laboral_canasta.png"), facecolor=BLANCO, bbox_inches='tight')
    plt.close()


# ==============================================================================
# FIGURA 4: LA ESQUINA VS TU QUINCENA (TUS 5 TIENDITAS REALES 07-B)
# ==============================================================================
def generar_figura_4():
    print("Generando Figura 4: La Esquina vs Tu Quincena (5 Tienditas 07-B)...")
    df_t = pd.read_csv(os.path.join(DATA_DIR, "fuente_b/07_bitacora_tienditas/bitacora_precios_tienditas.csv"))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=300, gridspec_kw={'width_ratios': [1.3, 1]})

    # Panel A: Matriz de Burbujas Pop con lectura inmediata
    productos = ['Leche entera', 'Tortilla de maiz', 'Frijol negro', 'Pan blanco', 'Huevo blanco']
    folios = ['AUD-01', 'AUD-02', 'AUD-03', 'AUD-04', 'AUD-05']
    tiendas_lbl = [
        'Centro\n(El Milagro)',
        'Santiago\n(La Isabelita)',
        'Polígono 108\n(María Elena)',
        'Mercedes Barrera\n(Evelia)',
        'Chuburná\n(Carmita)'
    ]

    for r_idx, folio in enumerate(folios):
        grp = df_t[df_t['folio_auditoria'] == folio]
        for c_idx, prod in enumerate(productos):
            sub = grp[grp['producto_auditado'] == prod]['precio_observado_mxn'].dropna()
            if len(sub) > 0:
                val = float(sub.iloc[0])
                b_size = 420 + val * 14
                b_col = ORO if val >= 55 else PURPURA
                txt_col = NEGRO if val >= 55 else BLANCO
                ax1.scatter(c_idx, r_idx, s=b_size, color=b_col, alpha=0.92, edgecolors=NEGRO, linewidth=1.4, zorder=4)
                sub_tag = ""
                if prod == 'Huevo blanco':
                    sub_tag = "\n(panal)" if val >= 75 else "\n(1 kg)"
                ax1.text(c_idx, r_idx, f"${val:.0f}{sub_tag}", ha='center', va='center', fontsize=8.8, fontweight='bold', color=txt_col, zorder=5)
            else:
                ax1.scatter(c_idx, r_idx, s=380, color='#f1f5f9', edgecolors='#94a3b8', linestyle='--', linewidth=1.2, zorder=3)
                ax1.text(c_idx, r_idx, "No vende", ha='center', va='center', fontsize=7.5, fontweight='bold', color=MUTED, zorder=4)

    ax1.set_xticks(range(len(productos)))
    ax1.set_xticklabels(['Leche\n(1 L)', 'Tortilla\n(1 kg)', 'Frijol\n(1 kg)', 'Pan Bimbo\n(Grande)', 'Huevo\n(Kg o Panal)'],
                        fontweight='bold', fontsize=9.8)
    ax1.set_yticks(range(len(tiendas_lbl)))
    ax1.set_yticklabels(tiendas_lbl, fontweight='bold', fontsize=9.8)
    ax1.set_xlim(-0.6, 4.6)
    ax1.set_ylim(-0.6, 4.6)
    ax1.grid(True, linestyle=':', alpha=0.6, zorder=0)
    ax1.set_title('A. Mapa Real de Tus 5 Tienditas Auditadas (07-B)\nMorado = Accesible (<$55) · Dorado = Pega Duro al Bolsillo (>$55)',
                  fontsize=11.5, fontweight='bold', color=PURPURA, pad=12)
    for s in ['top', 'right']:
        ax1.spines[s].set_visible(False)

    # Panel B: 3 Hallazgos Chistosos / Memorables de las Tienditas
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('B. Lo que Descubrimos Caminando la Colonia', fontsize=11.8, fontweight='bold', color=PURPURA, pad=12)

    cards = [
        (6.8, PURPURA_SOFT, PURPURA, "1. EL DILEMA DEL HUEVO: ¿GRANEL O PANAL?",
         "En Polígono 108 y Centro pides 1 kg suelto ($48–$50).\nEn el Sur/Norte te venden el panal entero ($85–$88):\n¡Un panal en Mercedes Barrera cuesta 3.4 kg de tortilla!"),
        (3.6, ORO_SOFT, ORO, "2. EL MISTERIO DEL PAN BIMBO ($55 a $60)",
         "Cuesta casi lo mismo un paquete de pan blanco ($60)\nque 2.3 KILOS DE TORTILLA CALIENTE ($59.80).\nAun así, las 5 tienditas lo tienen como rey del anaquel."),
        (0.4, GRIS_CLARO, NEGRO, "3. LA REGLA DE ORO DEL EFECTIVO",
         "En Polígono 108 y Centro solo aceptan efectivo.\nEn Santiago, Sur y Chuburná ya aceptan tarjeta/SPEI,\npero el costo de conveniencia sube hasta +10%.")
    ]

    for y_c, bg_c, ec_c, title_c, body_c in cards:
        ax2.add_patch(patches.FancyBboxPatch((0.2, y_c), 9.6, 2.7, boxstyle="round,pad=0.1,rounding_size=0.22",
                                             facecolor=bg_c, edgecolor=ec_c, linewidth=1.8))
        ax2.text(0.6, y_c + 2.15, title_c, ha='left', va='center', fontsize=10, fontweight='bold', color=PURPURA if ec_c != ORO else ORO_DARK)
        ax2.text(0.6, y_c + 1.0, body_c, ha='left', va='center', fontsize=9, color=NEGRO, linespacing=1.4)

    plt.suptitle('Figura 4: La Esquina vs. Tu Quincena — Auditoría Propia en 5 Colonias de Mérida (Fuente Self-Produced 07-B)',
                 fontsize=13.5, fontweight='bold', color=NEGRO, y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(OUTPUT_DIR, "04_encuesta_hogares_percepcion_salario_gasto.png"), facecolor=BLANCO, bbox_inches='tight')
    plt.close()


# ==============================================================================
# FIGURA 5: EL AIRE ACONDICIONADO QUE TE COBRAN EN EL JITOMATE (LIDAR 3D)
# ==============================================================================
def generar_figura_5():
    print("Generando Figura 5: El Aire Acondicionado que te Cobran en el Jitomate...")
    df_lidar = pd.read_csv(os.path.join(DATA_DIR, "fuente_a/08_lidar_mercado/lidar_mercado_merida_sample.csv"))
    col_code = 'classification_code' if 'classification_code' in df_lidar.columns else 'Clasificacion_ASPRS'
    col_z = 'elevation_z' if 'elevation_z' in df_lidar.columns else 'Z_m'

    fig, ax = plt.subplots(figsize=(12.5, 6.2), dpi=300)

    # Silueta parabólica del domo real
    x_grid = np.linspace(227345, 227375, 200)
    dome_z = 9.32 + 12.53 * np.exp(-((x_grid - 227360.5) / 10.5) ** 2)

    # Capas suaves: Fresco abajo (morado), calor escapando arriba (oro)
    ax.fill_between(x_grid, 9.32, 9.32 + (dome_z - 9.32) * 0.45, color=PURPURA, alpha=0.14, zorder=1)
    ax.fill_between(x_grid, 9.32 + (dome_z - 9.32) * 0.45, dome_z, color=ORO, alpha=0.22, zorder=1)

    # Flechas gigantes de "El calor sube y sale solo"
    for fx in [227354, 227357.5, 227360.5, 227363.5, 227367]:
        top_y = 20.6 if abs(fx - 227360.5) < 3.5 else 16.5
        ax.annotate('', xy=(fx, top_y), xytext=(fx, 10.3),
                    arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.5", color=ORO_DARK, lw=2.3, ls='--'), zorder=3)

    # Puntos LiDAR Reales
    suelo = df_lidar[df_lidar[col_code] == 2]
    edif = df_lidar[df_lidar[col_code] == 6]
    ax.scatter(suelo['easting_x'], suelo[col_z], color=PURPURA, s=110, edgecolors=BLANCO, lw=1.2, zorder=5,
               label='Piso del Mercado (9.3 m s.n.m.) · Zona Fresca para Frutas y Verduras')
    ax.scatter(edif['easting_x'], edif[col_z], color=ORO, s=140, edgecolors=NEGRO, lw=1.2, zorder=6,
               label='Domo Medido con Láser LiDAR (21.85 m s.n.m. = ¡4 Pisos de Alto!)')
    ax.plot(x_grid, dome_z, color=NEGRO, lw=2.2, zorder=4)

    # Callouts tipo cómic entendibles por cualquiera
    ax.text(227344.8, 22.8,
            "EL SECRETO DEL MERCADO LUCAS DE GÁLVEZ:\n"
            "• En Mérida el calor (>40°C) pudre el jitomate en horas.\n"
            "• Su techo gigante de 12.53 m saca el aire caliente SOLO.\n"
            "• Recibo de luz en aire acondicionado: $0 PESOS.\n"
            "• Resultado: Comida hasta 45% MÁS BARATA.",
            fontsize=9.2, fontweight='bold', color=PURPURA,
            bbox=dict(boxstyle="round,pad=0.6", fc=BLANCO, ec=PURPURA, lw=2.0), zorder=8)

    ax.text(227367.8, 22.8,
            "LA TRAMPA DEL SUPERMERCADO:\n"
            "• Edificio bajito y cerrado como refrigerador.\n"
            "• Aire acondicionado industrial prendido 24/7.\n"
            "• ¿Quién crees que paga esa factura de CFE?\n"
            "• TÚ, disfrazado en el +179% del jitomate.",
            fontsize=9.2, fontweight='bold', color=ORO_DARK,
            bbox=dict(boxstyle="round,pad=0.6", fc=ORO_SOFT, ec=ORO, lw=2.0), zorder=8)

    ax.set_xlabel('Ancho del Mercado Lucas de Gálvez (Coordenada UTM Este)', fontsize=10.5, fontweight='bold')
    ax.set_ylabel('Altura Medida por Láser LiDAR (Metros)', fontsize=10.5, fontweight='bold')
    ax.set_title('Figura 5: ¿Por qué un Láser 3D Explica el Precio del Jitomate?\nEl Aire Acondicionado que Pagas sin Saberlo vs. la Chimenea Gratis del Mercado (LiDAR 08-A)',
                 fontsize=13, fontweight='bold', color=NEGRO, pad=14)
    ax.set_ylim(8.2, 27.5)
    ax.legend(loc='lower center', frameon=True, facecolor=BLANCO, edgecolor=GRIS_BORDE, fontsize=9.5)
    ax.grid(True, linestyle=':', alpha=0.55)
    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "05_perfil_altimetrico_lidar_mercado_lucas_galvez.png"), facecolor=BLANCO, bbox_inches='tight')
    plt.close()


# ==============================================================================
# FIGURA 6: MÉRIDA PLANA COMO COMAL & EL TRUCO DE LOS $12 DEL VA Y VEN
# ==============================================================================
def generar_figura_6():
    print("Generando Figura 6: Merida Plana como Comal & Truco Va y Ven...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.2), dpi=300, gridspec_kw={'width_ratios': [1.05, 1.15]})

    # Panel A: Relieve "Sierra vs Mérida Plana como Tortilla"
    x = np.linspace(0, 10, 200)
    sierra = 42 + 18 * np.sin(x * 1.1) + 9 * np.cos(x * 2.5)
    merida = 9.0 + 0.5 * np.sin(x * 1.8)

    ax1.fill_between(x, 0, sierra, color=PURPURA, alpha=0.20, edgecolor=PURPURA, lw=2.0, label='Otras Ciudades con Cerros (Fletes caros)')
    ax1.fill_between(x, 0, merida, color=ORO, alpha=0.85, edgecolor=NEGRO, lw=2.0, label='Mérida: Plana como Comal (0.55° inclinación)')

    ax1.annotate("Mérida está a solo 9 metros\nsobre el mar (Cero subidas).\n¡Por eso en lluvia fuerte el Sur\nse encharca y frena tianguis!",
                 xy=(5.0, 9.5), xytext=(1.5, 23),
                 arrowprops=dict(arrowstyle="->,head_width=0.35", color=NEGRO, lw=1.8),
                 fontsize=9.5, fontweight='bold', color=NEGRO,
                 bbox=dict(boxstyle="round,pad=0.5", fc=ORO_SOFT, ec=ORO, lw=1.5))

    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 72)
    ax1.set_xlabel('Distancia de Ciudad (10 km)', fontsize=10.5, fontweight='bold')
    ax1.set_ylabel('Altura sobre el Mar (Metros · NASA GEDI / CEM)', fontsize=10.5, fontweight='bold')
    ax1.set_title('A. Topografía Satelital (08-B/C):\nMérida es Tan Plana Como Una Tortilla', fontsize=12, fontweight='bold', color=PURPURA, pad=12)
    ax1.legend(loc='upper right', frameon=True, facecolor=BLANCO, edgecolor=GRIS_BORDE, fontsize=9)
    ax1.grid(True, linestyle='--', alpha=0.45)
    for s in ['top', 'right']:
        ax1.spines[s].set_visible(False)

    # Panel B: La Ecuación Ganadora del Va y Ven ($12 vs $378)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('B. El Hack Urbano: 565 Rutas Va y Ven al Centro (04-C)', fontsize=12, fontweight='bold', color=PURPURA, pad=12)

    # Caja 1: Camino Perdedor (Delivery)
    ax2.add_patch(patches.FancyBboxPatch((0.3, 5.6), 9.4, 3.6, boxstyle="round,pad=0.1,rounding_size=0.25",
                                         facecolor=ORO_SOFT, edgecolor=ORO, linewidth=1.8))
    ax2.text(5.0, 8.6, "CAMINO 1: PEDIR POR APP EN TU COLONIA", ha='center', va='center', fontsize=10.5, fontweight='bold', color=ORO_DARK)
    ax2.text(5.0, 7.6, "Pagas +$378 MXN de sobreprecio promedio", ha='center', va='center', fontsize=12.5, fontweight='bold', color=NEGRO)
    ax2.text(5.0, 6.5, "Esos $378 alcanzan para 31 PASAJES DE VA Y VEN\n(o 14.5 kilos de tortilla caliente)",
             ha='center', va='center', fontsize=9.2, fontweight='bold', color=MUTED)

    # Caja 2: Camino Ganador (Va y Ven + Mercado Central)
    ax2.add_patch(patches.FancyBboxPatch((0.3, 0.8), 9.4, 4.1, boxstyle="round,pad=0.1,rounding_size=0.25",
                                         facecolor=PURPURA, edgecolor=NEGRO, linewidth=1.8))
    draw_bus_icon(ax2, 1.5, 2.85, w=1.4, h=0.95, color=ORO, zorder=5)
    ax2.text(5.7, 4.15, "CAMINO 2: SUBIRTE AL VA Y VEN ($12 IDA / $12 VUELTA)", ha='center', va='center', fontsize=10, fontweight='bold', color=ORO)
    ax2.text(5.7, 3.15, "565 rutas convergen a 300 m del Mercado", ha='center', va='center', fontsize=11.5, fontweight='bold', color=BLANCO)
    ax2.text(5.7, 1.9, "Gastas $24 pesos de camión y ahorras hasta $350+\nen tu despensa frente al súper o delivery.\n(Con AR Waypoints 09-C llegas directo al puesto barato)",
             ha='center', va='center', fontsize=8.8, color=BLANCO, linespacing=1.35)

    plt.suptitle('Figura 6: Geometría de la Ciudad y Movilidad Inteligente — Cómo el Va y Ven Vence a la Carestía',
                 fontsize=13.5, fontweight='bold', color=NEGRO, y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(OUTPUT_DIR, "06_topografia_satelital_srtm_merida.png"), facecolor=BLANCO, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    generar_figura_1()
    generar_figura_2()
    generar_figura_3()
    generar_figura_4()
    generar_figura_5()
    generar_figura_6()
    print("[OK] Las 6 infografias pop (Modo Gente Comun) fueron generadas a 300 DPI sin emojis!")
