"""
LABORATORIO #7 - ALGORITMO A

Complejidad teorica: O(n² log n)

Codigo original en C:

void function(int n) {
    int i, j, k, counter = 0;
    for (i = n/2; i <= n; i++) {
        for (j = 1; j+n/2 <= n; j++) {
            for (k = 1; k <= n; k = k*2) {
                counter++;
            }
        }
    }
}
"""

import sys
import time

NOMBRE = "(a)  O(n² log n)"
COMPLEJIDAD = "O(n² log n)"


def algoritmo_a(n: int) -> int:
    counter = 0

    for i in range(n // 2, n + 1):
        for j in range(1, (n - n // 2) + 1):
            k = 1
            while k <= n:
                counter += 1
                k *= 2
    return counter


def contar_operaciones_instrumentado(n: int) -> int:
    """
    - Cada verificacion de condicion del ciclo cuesta 1
    - Cada incremento y sentencia del cuerpo cuesta 1
    """
    ops = 2
    i = n // 2
    while True:
        ops += 1
        if not (i <= n):
            break
        j = 1
        while True:
            ops += 1
            if not (j + n // 2 <= n):
                break
            k = 1
            while True:
                ops += 1
                if not (k <= n):
                    break
                ops += 1
                k *= 2
            j += 1
        i += 1
    return ops


def contar_operaciones_formula(n: int) -> int:
    """
    - ni = n - n//2 + 1
    - nj = n - n//2 
    - nk = floor(log2(n)) + 1 = n.bit_length()
    """
    ni = n - n // 2 + 1
    nj = n - n // 2
    nk = n.bit_length()
    return 2 + (ni + 1) + ni * (nj + 1) + ni * nj * (nk + 1) + ni * nj * nk


def total_iteraciones_interiores(n: int) -> int:
    ni = n - n // 2 + 1
    nj = n - n // 2
    nk = n.bit_length()
    return ni * nj * nk


def medir_tiempo(n: int, reps: int = None) -> float:
    it = total_iteraciones_interiores(n)
    if reps is None:
        reps = max(1, int(2e6 / max(it, 1))) if it < 2e6 else 1
    
    t0 = time.perf_counter_ns()
    for _ in range(reps):
        algoritmo_a(n)
    t1 = time.perf_counter_ns()
    return (t1 - t0) / 1e9 / reps

contar_operaciones_a = contar_operaciones_instrumentado
formula_operaciones_a = contar_operaciones_formula

def main():
    sizes = [1, 10, 100, 1000]
    if len(sys.argv) > 1:
        sizes = [int(arg) for arg in sys.argv[1:]]

    print(f"""
    === Algoritmo {NOMBRE} ===
    {'n':>10} | {'Operaciones':>15} | {'Tiempo (s)':>15} | {'Counter':>15}
    {"-" * 62}
    """)

    for n in sizes:
        ops = contar_operaciones_formula(n)
        inst = contar_operaciones_instrumentado(n) if n <= 1000 else "N/A"
        t = medir_tiempo(n)
        cnt = algoritmo_a(n)
        print(f"{n:>10} | {ops:>15} | {t:>15.8f} | {cnt:>15}")


if __name__ == "__main__":
    main()
