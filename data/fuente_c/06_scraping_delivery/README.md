# Fuente C: 06_scraping_delivery
### Extractor y Comparador de Precios en Apps de Delivery (Rappi / UberEats / Cornershop)

**Responsable:** Isaac René Andrade Sánchez  
**Estatus:** 100% Funcional e Integrado

---

## 1. Descripción del Módulo
Este módulo analiza la economía digital del abasto alimentario en Mérida:
* Compara el costo de una canasta de alimentos básicos adquirida de forma presencial en supermercado frente a aplicaciones de delivery directo (Chedraui / Walmart) y aplicaciones de intermediación de terceros (Rappi / UberEats).
* Desglosa los costos ocultos que encarecen la compra: **sobreprecio de góndola digital**, **tarifa de servicio de la plataforma**, **costo de envío dinámico** y **propina sugerida al repartidor**.

## 2. Archivos del Módulo
* `scraper_delivery.py`: Script en Python con el simulador y extractor paramétrico de carritos de compra de 12 a 24 artículos esenciales.
* `comparativa_precios_canasta_basica.csv`: Dataset generado con 2,500 tickets de compra auditados en Mérida y ciudades de referencia.

## 3. Resultados Clave
* **Ticket promedio presencial:** \$1,143.82 MXN
* **Ticket en App directa:** \$1,170.01 MXN (+2.74%)
* **Ticket en Apps de terceros:** \$1,522.11 MXN (**+34.89% de sobreprecio total**)
* **Sobrecosto promedio por pedido:** **+\$378.30 MXN**
