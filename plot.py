#!/usr/bin/env python3
"""Laboratorio #7 - Grafica y tabla a partir de resultados de algoritmos (a), (b) y (c).

Uso:
  python3 plot.py                                           # Usa o genera resultados_lab7_python.csv y crea grafica.png
  python3 plot.py resultados.csv grafica.png [--titulo "Python"]
  python3 plot.py --run                                     # Fuerza re-ejecucion de profiling desde src/

El archivo CSV contiene las columnas:
  algoritmo,n,conteo_operaciones,tiempo_real_s,origen_tiempo,origen_conteo
Los tiempos con origen_tiempo == "extrapolado" se dibujan con un circulo vacio.
Ademas de la imagen PNG, imprime las tablas de resultados en formato Markdown.
"""

import argparse
import csv
import os
import sys
from typing import Dict, List, Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NOMBRES = {
    "a": "(a)  O(n² log n)",
    "b": "(b)  O(n)",
    "c": "(c)  O(n²)",
}


def fmt_tiempo(s: float) -> str:
    """Formatea el tiempo en segundos a unidades legibles (ns, µs, ms, s, h)."""
    if s < 1e-6:
        return f"{s * 1e9:.0f} ns"
    if s < 1e-3:
        return f"{s * 1e6:.1f} µs"
    if s < 1:
        return f"{s * 1e3:.2f} ms"
    if s < 3600:
        return f"{s:.2f} s"
    return f"{s / 3600:.2f} h"


def generar_grafica(
    rows: List[Dict[str, any]],
    png_path: str,
    titulo: str = "Python",
) -> None:
    """Genera la figura de 3 paneles (escala log-log) comparando tiempo real vs operaciones."""
    algs = [x for x in "abc" if any(r["algoritmo"] == x for r in rows)]
    if not algs:
        raise ValueError("No se encontraron algoritmos válidos ('a', 'b', 'c') en las filas proporcionadas.")

    fig, axs = plt.subplots(1, len(algs), figsize=(5.4 * len(algs), 4.8), squeeze=False)

    for ax, alg in zip(axs[0], algs):
        R = [r for r in rows if r["algoritmo"] == alg]
        ns = [int(r["n"]) for r in R]
        t = [float(r["tiempo_real_s"]) for r in R]
        ops = [int(r["conteo_operaciones"]) for r in R]

        ax2 = ax.twinx()  # Eje secundario (derecho): conteo de operaciones
        (l1,) = ax.plot(ns, t, "-o", color="#1f77b4", label="Tiempo real (s)")
        (l2,) = ax2.plot(ns, ops, "-s", color="#d62728", label="Conteo de operaciones")
        handles = [l1, l2]

        # Resaltar puntos extrapolados con círculo hueco
        ex = [r for r in R if r.get("origen_tiempo") == "extrapolado"]
        if ex:
            (p,) = ax.plot(
                [int(r["n"]) for r in ex],
                [float(r["tiempo_real_s"]) for r in ex],
                "o",
                mfc="white",
                color="#1f77b4",
                ms=10,
                label="Tiempo extrapolado",
            )
            handles.append(p)

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax2.set_yscale("log")

        ax.set_xlabel("n")
        ax.set_ylabel("Tiempo real (s)", color="#1f77b4")
        ax2.set_ylabel("Operaciones", color="#d62728")
        ax.set_title(NOMBRES.get(alg, alg))
        ax.grid(alpha=0.3, which="both")
        ax.legend(handles, [h.get_label() for h in handles], loc="upper left", fontsize=8)

    subtitulo = f" ({titulo})" if titulo else ""
    fig.suptitle(f"Laboratorio #7{subtitulo}: tiempo real vs. conteo de operaciones (escala log-log)")
    plt.tight_layout()
    plt.savefig(png_path, dpi=150)
    plt.close(fig)
    print(f"[OK] Gráfica guardada en: {png_path}")


def imprimir_tablas_markdown(rows: List[Dict[str, any]]) -> None:
    """Imprime en la terminal las tablas formateadas en Markdown."""
    algs = [x for x in "abc" if any(r["algoritmo"] == x for r in rows)]
    for alg in algs:
        print(f"\n### {NOMBRES.get(alg, alg)}")
        print("| n | Operaciones | Tiempo real | Origen tiempo |")
        print("|---|---|---|---|")
        for r in [r for r in rows if r["algoritmo"] == alg]:
            t_num = float(r["tiempo_real_s"])
            t_fmt = fmt_tiempo(t_num)
            origen = r.get("origen_tiempo", "medido")
            print(f"| {int(r['n']):,} | {int(r['conteo_operaciones']):,} | {t_fmt} | {origen} |")


def main():
    ap = argparse.ArgumentParser(
        description="Genera la gráfica y tablas del Laboratorio #7 adaptando los algoritmos de src/."
    )
    ap.add_argument("csv_pos", nargs="?", default=None, help="Ruta al archivo CSV de entrada (opcional)")
    ap.add_argument("png_pos", nargs="?", default=None, help="Ruta a la imagen PNG de salida (opcional)")
    ap.add_argument("--csv", default=None, help="Ruta al archivo CSV (por defecto: resultados_lab7_python.csv)")
    ap.add_argument("--png", default=None, help="Ruta a la imagen PNG (por defecto: grafica.png)")
    ap.add_argument("--titulo", default="Python", help="Título/lenguaje para la gráfica")
    ap.add_argument("--run", action="store_true", help="Fuerza re-ejecutar el profiling desde src/")
    ap.add_argument("--limit", type=float, default=1e8, help="Límite de iteraciones reales antes de extrapolar")
    args = ap.parse_args()

    default_csv = "resultados.csv" if os.path.exists("resultados.csv") else "resultados_lab7_python.csv"
    csv_path = args.csv_pos or args.csv or default_csv
    png_path = args.png_pos or args.png or "grafica.png"

    # Si se pide --run o si el CSV no existe, ejecutamos el profiling desde src/
    if args.run or not os.path.exists(csv_path):
        print(f"[*] Ejecutando profiling desde 'src/' (límite={args.limit:.1e} iteraciones)...")
        # Asegurar que el directorio raíz esté en sys.path
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        if repo_dir not in sys.path:
            sys.path.insert(0, repo_dir)
        from src.profiler import ejecutar_profiling, guardar_csv

        rows = ejecutar_profiling(limit_iters=args.limit, verbose=True)
        guardar_csv(rows, csv_path)
        print(f"[OK] CSV generado y guardado en: {csv_path}")
    else:
        print(f"[*] Leyendo resultados existentes de: {csv_path}")
        with open(csv_path, "r", newline="") as f:
            rows = list(csv.DictReader(f))

    generar_grafica(rows, png_path, titulo=args.titulo)
    imprimir_tablas_markdown(rows)


if __name__ == "__main__":
    main()
