"""
Resumen de los indicadores reales de esta carpeta:
- CONEVAL: líneas de pobreza por ingresos (valor mensual por persona, nacional urbano/rural).
- INEGI Censo 2020: totales del municipio de Mérida.
Ejecutar desde esta carpeta: python explorar_siegy.py
"""
import pandas as pd


def mostrar_resumen():
    lp = pd.read_csv("coneval_lineas_pobreza_2018_2025.csv")
    ultimo = lp.iloc[-1]
    print(f"=== CONEVAL, líneas de pobreza por ingresos ({ultimo['periodo']}) ===")
    print(f"Canasta alimentaria urbana (LPEI): ${ultimo['lpei_canasta_alimentaria_urbana_mxn']:,.2f} MXN por persona al mes")
    print(f"Canasta alimentaria + no alimentaria urbana (LPI): ${ultimo['lpi_alimentaria_mas_no_alimentaria_urbana_mxn']:,.2f} MXN")

    m = pd.read_csv("censo2020_totales_municipio_merida.csv").iloc[0]
    print("\n=== INEGI Censo 2020, municipio de Mérida ===")
    print(f"Población total: {int(m['POBTOT']):,}")
    print(f"Población económicamente activa: {int(m['PEA']):,}")
    print(f"Sin afiliación a servicios de salud: {100 * m['PSINDER'] / m['POBTOT']:.1f}%")


if __name__ == "__main__":
    mostrar_resumen()
