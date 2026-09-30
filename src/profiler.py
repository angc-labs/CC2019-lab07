#!/usr/bin/env python3
"""Laboratorio #7 - Profiler unificado para algoritmos (a), (b) y (c).
Ejecuta las pruebas con los tamaños requeridos por el laboratorio:
{1, 10, 100, 1000, 10000, 100000, 1000000}
"""

import csv
import sys
from typing import Dict, List, Optional

from .algoritmo_a import (
    algoritmo_a,
    contar_operaciones_instrumentado as ops_a_inst,
    contar_operaciones_formula as ops_a_form,
    medir_tiempo as medir_a,
    total_iteraciones_interiores as iter_a,
    NOMBRE as NOMBRE_A,
)
from .algoritmo_b import (
    algoritmo_b,
    contar_operaciones_instrumentado as ops_b_inst,
    contar_operaciones_formula as ops_b_form,
    medir_tiempo as medir_b,
    total_iteraciones_interiores as iter_b,
    NOMBRE as NOMBRE_B,
)
from .algoritmo_c import (
    algoritmo_c,
    contar_operaciones_instrumentado as ops_c_inst,
    contar_operaciones_formula as ops_c_form,
    medir_tiempo as medir_c,
    total_iteraciones_interiores as iter_c,
    NOMBRE as NOMBRE_C,
)

SIZES = [1, 10, 100, 1000, 10000, 100000, 1000000]

ALGORITMOS = {
    "a": {
        "nombre": NOMBRE_A,
        "func": algoritmo_a,
        "ops_inst": ops_a_inst,
        "ops_form": ops_a_form,
        "medir": medir_a,
        "iters": iter_a,
    },
    "b": {
        "nombre": NOMBRE_B,
        "func": algoritmo_b,
        "ops_inst": ops_b_inst,
        "ops_form": ops_b_form,
        "medir": medir_b,
        "iters": iter_b,
    },
    "c": {
        "nombre": NOMBRE_C,
        "func": algoritmo_c,
        "ops_inst": ops_c_inst,
        "ops_form": ops_c_form,
        "medir": medir_c,
        "iters": iter_c,
    },
}


def ejecutar_profiling(
    algs: Optional[List[str]] = None,
    sizes: Optional[List[int]] = None,
    limit_iters: float = 1e8,
    verbose: bool = True,
) -> List[Dict[str, any]]:
    if algs is None:
        algs = ["a", "b", "c"]
    if sizes is None:
        sizes = SIZES

    rows = []
    for alg in algs:
        meta = ALGORITMOS[alg]
        last_per_op = 0.0
        if verbose:
            print(f"\n--- Profiling {meta['nombre']} ---")

        for n in sizes:
            closed_ops = meta["ops_form"](n)
            it = meta["iters"](n)

            # Verificar conteo instrumentado vs fórmula para tamaños manejables
            if it <= 1e7:
                inst_ops = meta["ops_inst"](n)
                assert inst_ops == closed_ops, f"Discrepancia en {alg} n={n}: {inst_ops} vs {closed_ops}"
                src_c = "instrumentado"
            else:
                src_c = "formula (verificada en n menores)"

            if it <= limit_iters:
                secs = meta["medir"](n)
                src_t = "medido"
                last_per_op = secs / closed_ops if closed_ops > 0 else 0.0
            else:
                secs = last_per_op * closed_ops
                src_t = "extrapolado"

            row = {
                "algoritmo": alg,
                "n": n,
                "conteo_operaciones": closed_ops,
                "tiempo_real_s": f"{secs:.9f}",
                "origen_tiempo": src_t,
                "origen_conteo": src_c,
            }
            rows.append(row)

            if verbose:
                tag = " (extrapolado)" if src_t == "extrapolado" else ""
                print(f"  n={n:<8} | Ops={closed_ops:<15} | Tiempo={secs:.6e}s{tag}")

    return rows


def guardar_csv(rows: List[Dict[str, any]], path: str) -> None:
    if not rows:
        return
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    rows = ejecutar_profiling(limit_iters=1e8, verbose=True)
    guardar_csv(rows, "resultados.csv")
    print("\nResultados guardados exitosamente en resultados.csv")


if __name__ == "__main__":
    main()
