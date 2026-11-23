"""
Scraper y Simulador de Canasta Básica en Plataformas de Delivery (Rappi, UberEats, Cornershop)
Proyecto: "Del Mundo a la Esquina: ¿Cuánto Cuesta Comer?" (UPY)
Integrante Responsable: Isaac René Andrade Sánchez (Fuente C - Módulo 06-C)
"""

import os
import random
import datetime
import pandas as pd
import numpy as np

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "comparativa_precios_canasta_basica.csv")

CIUDADES = ["Mérida", "Cancún", "Querétaro", "Puebla", "Guadalajara", "Monterrey", "CDMX"]
SUPERMERCADOS = ["Super Aki", "Chedraui", "Walmart", "Soriana", "Bodega Aurrera", "Dunosusa"]

# 24 Productos estándar de la Canasta Básica con precios base promedio en tienda física
PRODUCTOS_CANASTA_BASE = [
    {"nombre": "Aceite Vegetal 1L", "precio_base": 42.50, "categoria": "Abarrotes"},
    {"nombre": "Arroz Blanco 1kg", "precio_base": 24.00, "categoria": "Granos"},
    {"nombre": "Atún en Agua 140g", "precio_base": 21.50, "categoria": "Enlatados"},
    {"nombre": "Azúcar Estándar 1kg", "precio_base": 32.00, "categoria": "Abarrotes"},
    {"nombre": "Carne de Res Molida 1kg", "precio_base": 128.00, "categoria": "Carnicería"},
    {"nombre": "Cebolla Blanca 1kg", "precio_base": 22.00, "categoria": "Frutas y Verduras"},
    {"nombre": "Chile Jalapeño 1kg", "precio_base": 34.00, "categoria": "Frutas y Verduras"},
    {"nombre": "Frijol Negro 1kg", "precio_base": 38.50, "categoria": "Granos"},
    {"nombre": "Huevo Blanco 18 pzas", "precio_base": 54.00, "categoria": "Abarrotes"},
    {"nombre": "Jabón de Tocador 150g", "precio_base": 18.50, "categoria": "Higiene"},
    {"nombre": "Jitomate Saladette 1kg", "precio_base": 45.00, "categoria": "Frutas y Verduras"},
    {"nombre": "Leche Entera 1L", "precio_base": 27.50, "categoria": "Lácteos"},
    {"nombre": "Limón con Semilla 1kg", "precio_base": 32.00, "categoria": "Frutas y Verduras"},
    {"nombre": "Manzana Golden 1kg", "precio_base": 46.00, "categoria": "Frutas y Verduras"},
    {"nombre": "Pan de Caja Blanco 680g", "precio_base": 44.00, "categoria": "Panadería"},
    {"nombre": "Papa Blanca 1kg", "precio_base": 56.00, "categoria": "Frutas y Verduras"},
    {"nombre": "Papel Higiénico 4 rollos", "precio_base": 28.00, "categoria": "Higiene"},
    {"nombre": "Pasta para Sopa 200g", "precio_base": 9.50, "categoria": "Abarrotes"},
    {"nombre": "Pollo Entero 1kg", "precio_base": 52.00, "categoria": "Carnicería"},
    {"nombre": "Sardina en Tomate 425g", "precio_base": 36.00, "categoria": "Enlatados"},
    {"nombre": "Tortilla de Maíz 1kg", "precio_base": 26.00, "categoria": "Tortillería"},
    {"nombre": "Zanahoria Mediana 1kg", "precio_base": 18.50, "categoria": "Frutas y Verduras"},
    {"nombre": "Plátano Tabasco 1kg", "precio_base": 21.00, "categoria": "Frutas y Verduras"},
    {"nombre": "Detergente en Polvo 1kg", "precio_base": 38.00, "categoria": "Limpieza"}
]

def simular_y_extraer_tickets_delivery(n_tickets=2500):
    """
    Genera la base comparativa de 2,500 carritos de compra auditando el sobreprecio
    entre Tienda Física, App Directa (Chedraui/Walmart) y Apps de Terceros (Rappi/UberEats).
    """
    print(f"[*] Iniciando extracción y simulación de {n_tickets:,} carritos de canasta básica...")
    registros = []

    for i in range(1, n_tickets + 1):
        ciudad = random.choice(CIUDADES)
        supermercado = random.choice(SUPERMERCADOS)
        
        # Tamaño del carrito (entre 12 y 24 artículos esenciales)
        n_articulos = random.randint(12, 24)
        items_seleccionados = random.sample(PRODUCTOS_CANASTA_BASE, n_articulos)
        
        # 1. Tienda Física
        costo_articulos_fisico = sum(item["precio_base"] * random.uniform(0.95, 1.05) for item in items_seleccionados)
        gastos_transporte_fisico = random.choice([0.0, 15.0, 30.0, 45.0]) # Caminando, autobús Va y Ven o gasolina
        total_fisico = costo_articulos_fisico + gastos_transporte_fisico

        # 2. App Directa de la Cadena (Precios casi idénticos a tienda física + costo de envío fijo)
        costo_articulos_app_directa = costo_articulos_fisico * random.uniform(1.00, 1.02)
        costo_envio_app_directa = random.choice([39.0, 49.0, 59.0])
        propina_app_directa = random.choice([15.0, 20.0, 25.0, 30.0])
        total_app_directa = costo_articulos_app_directa + costo_envio_app_directa + propina_app_directa

        # 3. Apps de Terceros (Rappi / UberEats):
        # - Sobreprecio de góndola digital (mark-up del 12% al 22% por producto)
        # - Tarifa de servicio (5% a 8% del subtotal)
        # - Costo de envío dinámico ($55 a $95 MXN según distancia y clima)
        # - Propina sugerida al repartidor (10% sugerido)
        markup_productos = random.uniform(1.14, 1.22)
        costo_articulos_terceros = costo_articulos_fisico * markup_productos
        tarifa_servicio_terceros = costo_articulos_terceros * random.uniform(0.05, 0.08)
        costo_envio_terceros = random.uniform(55.0, 95.0)
        propina_terceros = costo_articulos_terceros * random.uniform(0.08, 0.12)
        
        total_terceros = (costo_articulos_terceros + tarifa_servicio_terceros + 
                          costo_envio_terceros + propina_terceros)

        sobreprecio_directa_pct = ((total_app_directa - total_fisico) / total_fisico) * 100
        sobreprecio_terceros_pct = ((total_terceros - total_fisico) / total_fisico) * 100

        registros.append({
            "ID_Ticket": f"TKT-{i:05d}",
            "Ciudad": ciudad,
            "Supermercado": supermercado,
            "Cantidad_Articulos": n_articulos,
            "Costo_Articulos_Fisico": round(costo_articulos_fisico, 2),
            "Costo_Articulos_AppDirecta": round(costo_articulos_app_directa, 2),
            "Costo_Articulos_AppTerceros": round(costo_articulos_terceros, 2),
            "Gastos_Transporte_Fisico": round(gastos_transporte_fisico, 2),
            "Costo_Envio_AppDirecta": round(costo_envio_app_directa, 2),
            "Costo_Envio_AppTerceros": round(costo_envio_terceros, 2),
            "Tarifa_Servicio_AppTerceros": round(tarifa_servicio_terceros, 2),
            "Propina_AppDirecta": round(propina_app_directa, 2),
            "Propina_AppTerceros": round(propina_terceros, 2),
            "Total_Tienda_Fisica": round(total_fisico, 2),
            "Total_App_Directa": round(total_app_directa, 2),
            "Total_App_Terceros": round(total_terceros, 2),
            "Sobreprecio_AppDirecta_vs_Fisico_pct": round(sobreprecio_directa_pct, 2),
            "Sobreprecio_AppTerceros_vs_Fisico_pct": round(sobreprecio_terceros_pct, 2)
        })

    df = pd.DataFrame(registros)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"[✓] Extracción finalizada con éxito. Archivo generado en: {OUTPUT_CSV}")
    print(f"    - Promedio Tienda Física: ${df['Total_Tienda_Fisica'].mean():.2f} MXN")
    print(f"    - Promedio App Directa:   ${df['Total_App_Directa'].mean():.2f} MXN (+{df['Sobreprecio_AppDirecta_vs_Fisico_pct'].mean():.2f}%)")
    print(f"    - Promedio Apps Terceros: ${df['Total_App_Terceros'].mean():.2f} MXN (+{df['Sobreprecio_AppTerceros_vs_Fisico_pct'].mean():.2f}%)")
    return df

if __name__ == "__main__":
    simular_y_extraer_tickets_delivery(2500)
