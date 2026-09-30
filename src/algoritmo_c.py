"""
LABORATORIO #7 - ALGORITMO (c)
Complejidad teorica: O(n²)

Codigo original en C:
void function(int n) {
    int i, j;
    for (i = 1; i <= n/3; i++) {
        for (j = 1; j <= n; j += 4) {
            printf("Sequence\n");
        }
    }
}
"""

import os
import sys
import time

NOMBRE = "(c)  O(n²)"
COMPLEJIDAD = "O(n²)"

DEVNULL = open(os.devnull, "w", buffering=1 << 16)


def algoritmo_c(n: int, sink=DEVNULL) -> None:
    for i in range(1, n // 3 + 1):
        for j in range(1, n + 1, 4):
            sink.write("Sequence\n")


def contar_operaciones_instrumentado(n: int) -> int:
    ops = 2
    i = 1
    while True:
        ops += 1
        if not (i <= n // 3):
            break
        j = 1
        while True:
            ops += 1
            if not (j <= n):
                break
            ops += 1
            j += 4
        i += 1
    return ops


def contar_operaciones_formula(n: int) -> int:
    """
    - ni = n // 3 
    - nj = (n + 3) // 4 
    Total = 2 + (ni + 1) + ni * (nj + 1) + ni * nj
    """
    ni = n // 3
    nj = (n + 3) // 4
    return 2 + (ni + 1) + ni * (nj + 1) + ni * nj


def total_iteraciones_interiores(n: int) -> int:
    return (n // 3) * ((n + 3) // 4)


def medir_tiempo(n: int, reps: int = None, sink=DEVNULL) -> float:
    it = total_iteraciones_interiores(n)
    if reps is None:
        reps = max(1, int(2e6 / max(it, 1))) if it < 2e6 else 1
    
    t0 = time.perf_counter_ns()
    for _ in range(reps):
        algoritmo_c(n, sink=sink)
    sink.flush()
    t1 = time.perf_counter_ns()
    return (t1 - t0) / 1e9 / reps

contar_operaciones_c = contar_operaciones_instrumentado
formula_operaciones_c = contar_operaciones_formula

def main():
    sizes = [1, 10, 100, 1000, 10000]
    if len(sys.argv) > 1:
        sizes = [int(arg) for arg in sys.argv[1:]]

    print(f"""
    === Algoritmo {NOMBRE} ===
    {'n':>10} | {'Operaciones':>15} | {'Tiempo (s)':>15}
    {"-" * 46}
    """)

    for n in sizes:
        ops = contar_operaciones_formula(n)
        t = medir_tiempo(n)
        print(f"{n:>10} | {ops:>15} | {t:>15.8f}")


if __name__ == "__main__":
    main()
