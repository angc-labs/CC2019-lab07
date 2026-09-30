"""
LABORATORIO #7 - ALGORITMO B

Complejidad teorica: O(n)
Codigo original en C:

void function(int n) {
    if (n <= 1) return;
    int i, j;
    for (i = 1; i <= n; i++) {
        for (j = 1; j <= n; j++) {
            printf("Sequence\n");
            break;
        }
    }
}
"""

import os
import sys
import time

NOMBRE = "(b)  O(n)"
COMPLEJIDAD = "O(n)"
DEVNULL = open(os.devnull, "w", buffering=1 << 16)


def algoritmo_b(n: int, sink=DEVNULL) -> None:
    if n <= 1:
        return
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            sink.write("Sequence\n")
            break


def contar_operaciones_instrumentado(n: int) -> int:
    """
    - n <= 1:
        ops = 2
    - n > 1:
        ops = 2
        ops += 1
        ciclo i: se evalua i <= n (n + 1) veces
        cuerpo i (n veces):
            verificacion j <= n
            printf ("Sequence")
            break
    """
    ops = 2
    if n <= 1:
        return ops
    ops += 1
    i = 1
    while True:
        ops += 1
        if not (i <= n):
            break
        j = 1
        ops += 1
        ops += 2
        i += 1
    return ops


def contar_operaciones_formula(n: int) -> int:
    """
    - Si n <= 1: 2 operaciones.
    - Si n > 1: 3 + (n + 1) + 3*n = 4*n + 4 operaciones.
    """
    return 2 if n <= 1 else 4 * n + 4


def total_iteraciones_interiores(n: int) -> int:
    return 0 if n <= 1 else n


def medir_tiempo(n: int, reps: int = None, sink=DEVNULL) -> float:
    it = total_iteraciones_interiores(n)
    if reps is None:
        reps = max(1, int(2e6 / max(it, 1))) if it < 2e6 else 1
    
    t0 = time.perf_counter_ns()
    for _ in range(reps):
        algoritmo_b(n, sink=sink)
    sink.flush()
    t1 = time.perf_counter_ns()
    return (t1 - t0) / 1e9 / reps

contar_operaciones_b = contar_operaciones_instrumentado
formula_operaciones_b = contar_operaciones_formula

def main():
    sizes = [1, 10, 100, 1000, 10000, 100000, 1000000]
    if len(sys.argv) > 1:
        sizes = [int(arg) for arg in sys.argv[1:]]

    print(f"""
    === Algoritmo {NOMBRE} ===
    {'n':>10} | {'Operaciones':>15} | {'Tiempo (s)':>15}
    {"-" * 62}
    """)

    for n in sizes:
        ops = contar_operaciones_formula(n)
        t = medir_tiempo(n)
        print(f"{n:>10} | {ops:>15} | {t:>15.8f}")


if __name__ == "__main__":
    main()
