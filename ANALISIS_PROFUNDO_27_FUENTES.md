# Análisis Profundo Multiescalar de las 22 Fuentes de Datos
## Proyecto: "Del Mundo a la Esquina: ¿Cuánto Cuesta Comer?"
### Radiografía del Salario, la Canasta Básica y el Territorio Urbano en Mérida, Yucatán

**Equipo de Investigación:**
* **Valeria Nicol Hernández León** — *Responsable de Fuente A (7 fuentes)*
* **Jorge Ramiro Chay Koyoc** — *Responsable de Fuente B (8 fuentes, incluye bitácora propia de tienditas)*
* **Isaac René Andrade Sánchez** — *Responsable de Fuente C (7 fuentes)*

---

## 1. Resumen Ejecutivo y Hallazgos Clave

Este informe condensa el procesamiento estadístico, económico y espacial cruzado de los **22 datasets oficiales, levantamiento primario en tienditas y sensores tridimensionales** del proyecto. La investigación sigue un modelo de embudo multiescalar (**Internacional $\rightarrow$ México $\rightarrow$ Yucatán $\rightarrow$ Mérida**) y revela cinco hallazgos estructurales:

1. **Hiperconcentración Comercial del Alimento:** En Mérida operan **12,621 unidades económicas** dedicadas a la venta de alimentos. Sin embargo, apenas **84 grandes supermercados** (el **0.67%** de los comercios) concentran **\$8,920.5 millones de pesos**, lo que representa el **40.98%** de toda la facturación comercial de alimentos del municipio (INEGI SAIC).
2. **El Costo de la Intermediación (Mayoreo vs. Menudeo):** La diferencia entre el precio mayorista en la Central de Abasto de Mérida (SNIIM) y el precio minorista en góndola de supermercados (PROFECO) alcanza márgenes de hasta **+250.0% en papa blanca** (de \$16.00/kg a \$56.00/kg) y **+178.6% en jitomate saladette** (de \$16.15/kg a \$45.00/kg), lo que evidencia que el encarecimiento no ocurre en el campo sino en los eslabones logísticos y comerciales.
3. **El "Impuesto Digital" de las Apps de Delivery:** Comprar la canasta básica mediante aplicaciones de terceros (Rappi / UberEats) impone un **sobreprecio promedio del +34.89%** respecto a la compra presencial. Por un ticket promedio de \$1,143.82 MXN en tienda física, el usuario digital termina pagando **\$1,522.11 MXN**, acumulando **\$378.30 MXN en costos adicionales** entre tarifas de envío (\$64.72), costos de servicio de plataforma (\$53.23), propinas (\$55.49) y márgenes inflados sobre el producto.
4. **La Brecha Salarial Frente a la Canasta Básica:** La canasta alimentaria urbana de CONEVAL en Yucatán cuesta **\$2,610.50 MXN mensuales por persona**. Para un hogar meridano promedio de 4 integrantes, se requieren **\$10,442.00 MXN mensuales únicamente para comer**. Mientras que el salario formal IMSS en Mérida promedia \$558.10/día (\$16,743/mes), en la periferia metropolitana (Kanasín y Umán) el salario promedio cae a \$398.20/día y la informalidad escala al 56.3%, dejando a más del 38% de los trabajadores en pobreza laboral.
5. **El Centro Histórico como Refugio de Abasto Popular:** Los dos grandes mercados nodales del Centro (Lucas de Gálvez y San Benito) concentran **2,140 locales comerciales** y reciben a más de **60,000 personas al día**. La red de transporte metropolitano **Va y Ven (565 rutas y paraderos)** converge de forma radial a menos de 300 metros de sus puertas, convirtiendo al corazón de la ciudad en la válvula de escape contra la carestía para las familias del sur y oriente de Mérida.

---

## 2. Eje 1: Economía del Alimento y Concentración del Mercado

### 2.1. Censo Económico SAIC (01-B) vs. Directorio DENUE (01-A)

Al cruzar los 7,520 comercios georreferenciados de DENUE con el censo del Sistema Automatizado de Información Censal (SAIC) de INEGI, se observa una estructura profundamente asimétrica:

```text
┌──────────────────────────────────────────────┬──────────────┬──────────────┬─────────────────────────┐
│ Tipo de Establecimiento Comercial            │ Unidades     │ Personal     │ Ingresos Totales (MDP)  │
├──────────────────────────────────────────────┼──────────────┼──────────────┼─────────────────────────┤
│ Tiendas de abarrotes, ultramarinos y miscel. │ 5,120        │ 8,940        │ $ 2,415.8 MDP           │
│ Fruterías y verdulerías de barrio            │ 890          │ 1,650        │ $   515.0 MDP           │
│ Carnicerías (rojas y aves)                   │ 1,220        │ 2,530        │ $ 1,245.3 MDP           │
│ Tortillerías y molinos de nixtamal           │ 730          │ 1,980        │ $   650.1 MDP           │
│ Hipermercados y Supermercados de cadena      │ 84 (0.67%)   │ 6,420        │ $ 8,920.5 MDP (40.98%)  │
├──────────────────────────────────────────────┼──────────────┼──────────────┼─────────────────────────┤
│ Total Comercio de Alimentos en Mérida        │ 12,621       │ 27,940       │ $ 21,767.3 MDP          │
└──────────────────────────────────────────────┴──────────────┴──────────────┴─────────────────────────┘
```

* **Conclusión analítica:** Cada sucursal de supermercado en Mérida factura en promedio **\$106.2 millones de pesos al año**, mientras que una tiendita de esquina factura en promedio **\$471,000 pesos anuales**.

---

## 3. Eje 2: La Cadena de Precios y el Margen de Intermediación

### 3.1. Mayoreo Central de Abasto (02-B) vs. Góndola de Supermercados (02-A)

| Producto de la Canasta Básica | Origen de la Mercancía | Mayoreo Central Abasto (SNIIM) | Menudeo Supermercado (PROFECO) | Diferencia Absoluta | Margen de Intermediación |
|---|---|:---:|:---:|:---:|:---:|
| **Jitomate Saladette** | Puebla / Hidalgo | **\$16.15 / kg** | **\$45.00 / kg** | +\$28.85 / kg | **+178.6%** |
| **Cebolla Blanca** | Chihuahua / Puebla | **\$14.00 / kg** | **\$22.00 / kg** | +\$ 8.00 / kg | **+57.1%** |
| **Papa Blanca Alpha** | Sonora / Sinaloa | **\$16.00 / kg** | **\$56.00 / kg** | +\$40.00 / kg | **+250.0%** |
| **Limón con Semilla** | Yucatán / Colima | **\$11.11 / kg** | **\$26.50 / kg** | +\$15.39 / kg | **+138.5%** |
| **Plátano Tabasco** | Chiapas / Tabasco | **\$12.00 / kg** | **\$24.90 / kg** | +\$12.90 / kg | **+107.5%** |
| **Aguacate Hass** | Michoacán | **\$38.00 / kg** | **\$79.00 / kg** | +\$41.00 / kg | **+107.9%** |
| **Huevo Blanco** | Granjas Yucatán | **\$36.00 / kg** | **\$48.50 / kg** | +\$12.50 / kg | **+34.7%** |

---

## 4. Eje 3: El Costo Oculto de la Economía Digital (Delivery Scraping 06-C)

A partir del scraper que simuló **2,500 carritos de compra de canasta básica** en Mérida comparando tres canales de adquisición:

```text
        CANAL DE COMPRA                      COSTO TOTAL PROMEDIO       SOBREPRECIO
┌──────────────────────────────────────────────┬────────────────────────┬─────────────┐
│ 1. Tienda Física (Compra Presencial)         │ $ 1,143.82 MXN         │      Base   │
│ 2. App Directa Supermercado (Akí/Chedraui)   │ $ 1,170.01 MXN         │   +  2.74%  │
│ 3. Apps de Terceros (Rappi / UberEats)       │ $ 1,522.11 MXN         │   + 34.89%  │
└──────────────────────────────────────────────┴────────────────────────┴─────────────┘
```

---

## 5. Eje 4: Auditoría de Campo en Tienditas de Esquina (Self-Produced 07-B)

El levantamiento primario del equipo (`bitacora_precios_tienditas.csv`) auditó **5 tienditas de abarrotes** en distintos cuadrantes de Mérida:
1. **AUD-01 — Centro Histórico:** *Abarrotes El Milagro* (Tortilla \$26/kg, Huevo a granel \$50/kg, Leche Lala \$26/L, Frijol La Sierra \$25/kg, Pan Bimbo grande \$55).
2. **AUD-02 — Parque de Santiago:** *Tienda "La Isabelita"* (Leche Lala \$25/L, Huevo San Juan panal \$80, Frijol Grano de Oro \$30/kg, Pan Bimbo grande \$58).
3. **AUD-03 — Polígono 108:** *Abarrotes "María Elena"* (Huevo a granel \$48/kg, Leche Lala \$28/L, Frijol Grano de Oro \$31/kg, Pan Bimbo grande \$60).
4. **AUD-04 — Mercedes Barrera:** *Frutería y Abarrotes "Evelia"* (Huevo San Juan panal \$88, Leche Nutri \$25/L, Frijol La Sierra \$28/kg, Pan Bimbo grande \$60).
5. **AUD-05 — Vista Alegre de Chuburná:** *Abarrotes "Carmita"* (Tortilla \$27/kg, Huevo San Juan panal \$85, Leche Lala \$26/L, Pan Bimbo grande \$60, Frijol La Sierra \$26/kg).

---

## 6. Matriz de Síntesis Analítica de las 22 Fuentes Activas

```text
┌──────┬───────────────────────────────┬───────────────────────────────┬────────────────────────────────┐
│ TIPO │ FUENTE A (Valeria Hernández)  │ FUENTE B (Jorge Chay)         │ FUENTE C (Isaac Andrade)       │
├──────┼───────────────────────────────┼───────────────────────────────┼────────────────────────────────┤
│  01  │ DENUE: 7,520 tiendas Mérida   │ SAIC: 84 súper = 41% ventas   │ ENOE: Microdatos salariales    │
│  02  │ PROFECO: 28k precios reales   │ SNIIM: Mayoreo Central Abasto │ DICONSA: 4k ítems subsidiados  │
│  03  │ SIEGY: Canasta $2,610 urbana  │ CONAPO: Marginación Norte/Sur │ SENASICA: Inspección alimentos │
│  04  │ GEOPORTAL: 8 mercados (2.5k l)│ TIANGUIS: 6 tianguis (1.2k p) │ VA Y VEN: 565 rutas al Centro  │
│  06  │ SCRAPER: Súper Akí / Chedraui │ SCRAPER: Farmacias OXXO       │ DELIVERY: +35% sobreprecio app │
│  07  │ [Consolidado en 07-B]         │ BITÁCORA: 5 tienditas Mérida  │ [Consolidado en 07-B]          │
│  08  │ LIDAR: Domo mdo altura 12.5m  │ CEM MDE: Pendiente 0.5° INEGI │ OPENTOPOGRAPHY: Cota 8.97 msnm │
│  09  │ AR VPS: 4 anclas fachadas     │ ASSETS 3D: Catálogo canasta   │ AR ROUTE: 6 waypoints guiado   │
└──────┴───────────────────────────────┴───────────────────────────────┴────────────────────────────────┘
```
