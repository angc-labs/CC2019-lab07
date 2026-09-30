#!/usr/bin/env python3
"""Laboratorio #7 - Punto de entrada principal (CC2019 - Teoría de la Computación).

Ejecuta el profiling completo de los algoritmos (a), (b) y (c) implementados en src/,
genera el archivo CSV de resultados y crea la gráfica comparativa de tiempo real vs operaciones.
"""

import sys
from src.profiler import ejecutar_profiling, guardar_csv
from plot import generar_grafica, imprimir_tablas_markdown


def main():
    print("=" * 65)
    print(" Laboratorio #7 - Análisis y Profiling de Algoritmos (Python)")
    print("=" * 65)

    csv_path = "resultados.csv"
    png_path = "grafica.png"

    # Si se pasa --benchmark o --run, o por defecto si no hay CSV
    print(f"[*] Ejecutando suite de profiling para {csv_path}...")
    rows = ejecutar_profiling(limit_iters=1e8, verbose=True)
    guardar_csv(rows, csv_path)
    print(f"[OK] Datos guardados en {csv_path}")

    print(f"[*] Generando gráfica en {png_path}...")
    generar_grafica(rows, png_path, titulo="Python")

    imprimir_tablas_markdown(rows)
    print("\nProceso completado exitosamente.")


if __name__ == "__main__":
    main()
