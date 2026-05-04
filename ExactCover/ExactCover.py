# -*- coding: utf-8 -*-

import time
import random
import matplotlib.pyplot as plt


# ==============================
# ALGORITMO BASE (BACKTRACKING)
# ==============================

def exact_cover(X, S, solution):
    if not X:
        return solution

    x = next(iter(X))

    for subset in S:
        if x in subset:
            new_X = X.copy()
            new_S = []

            for elem in subset:
                new_X.discard(elem)

            for s in S:
                if s.isdisjoint(subset):
                    new_S.append(s)

            result = exact_cover(new_X, new_S, solution + [subset])
            if result is not None:
                return result

    return None


def run_base(X, S):
    start = time.time()
    result = exact_cover(set(X), S, [])
    end = time.time()
    return result, end - start


# ==============================
# HEURÍSTICA
# ==============================

def choose_best_element(X, S):
    count = {x: sum(1 for s in S if x in s) for x in X}
    return min(count, key=count.get)


def exact_cover_heuristic(X, S, solution):
    if not X:
        return solution

    x = choose_best_element(X, S)

    for subset in S:
        if x in subset:
            new_X = X.copy()
            new_S = []

            for elem in subset:
                new_X.discard(elem)

            for s in S:
                if s.isdisjoint(subset):
                    new_S.append(s)

            result = exact_cover_heuristic(new_X, new_S, solution + [subset])
            if result is not None:
                return result

    return None


def run_heuristic(X, S):
    start = time.time()
    result = exact_cover_heuristic(set(X), S, [])
    end = time.time()
    return result, end - start


# ==============================
# CASOS DETERMINÍSTICOS
# ==============================

def test_cases():
    print("=== CASOS DETERMINÍSTICOS ===")

    X1 = {1,2,3,4}
    S1 = [{1,2}, {2,3}, {3,4}, {1,4}]
    print("Caso 1:", exact_cover(set(X1), S1, []))

    X2 = {1,2,3}
    S2 = [{1,2}, {2,3}]
    print("Caso 2:", exact_cover(set(X2), S2, []))

    X3 = {1,2,3,4}
    S3 = [{1,2}, {3,4}, {1,3}, {2,4}]
    print("Caso 3:", exact_cover(set(X3), S3, []))

    print()


# ==============================
# GENERACIÓN DE INSTANCIAS
# ==============================

def generate_instance(n, num_subsets, max_subset_size=3):
    X = list(range(1, n + 1))
    S = []

    for _ in range(num_subsets):
        size = random.randint(2, max_subset_size)
        subset = set(random.sample(X, size))
        S.append(subset)

    return X, S


# ===================
# EXPERIMENTOS
# ===================

def run_experiments(sizes, repetitions=5):
    results = []

    print("=== EJECUTANDO EXPERIMENTOS ===\n")

    for n in sizes:
        base_total = 0
        heur_total = 0

        for _ in range(repetitions):
            X, S = generate_instance(n, n * 2)

            _, t_base = run_base(X, S)
            _, t_heur = run_heuristic(X, S)

            base_total += t_base
            heur_total += t_heur

        avg_base = base_total / repetitions
        avg_heur = heur_total / repetitions

        results.append((n, avg_base, avg_heur))

        print(f"n={n} | Base={avg_base:.6f}s | Heurística={avg_heur:.6f}s")

    return results


# ==============================
# GRÁFICOS
# ==============================

def plot_results(results):
    n = [r[0] for r in results]
    base = [r[1] for r in results]
    heur = [r[2] for r in results]

    plt.figure()
    plt.plot(n, base, marker='o', label="Backtracking Base")
    plt.plot(n, heur, marker='o', label="Backtracking + Heurística")

    plt.xlabel("Tamaño del problema (n)")
    plt.ylabel("Tiempo de ejecución (segundos)")
    plt.title("Comparación de algoritmos - Exact Cover")
    plt.legend()
    plt.grid()

    plt.show()


# ==============================
# MAIN
# ==============================

def main():
    print("===== TEST DE CORRECTITUD =====")
    test_cases()

    print("===== EXPERIMENTOS =====")

    sizes = [6, 8, 10, 12, 14, 16, 18, 20, 40]
    # puedes agregar 60 si quieres probar límite

    results = run_experiments(sizes, repetitions=5)

    print("\n===== RESULTADOS =====")
    for r in results:
        print(f"n={r[0]} -> Base={r[1]:.6f}s | Heurística={r[2]:.6f}s")

    print("\n===== GRÁFICO =====")
    plot_results(results)


# Ejecutar
main()


# ==============================
# DATOS
# ==============================

n = [6, 8, 10, 12, 14, 16, 18, 20, 40]

# Python
py_base = [0.000005,0.000015,0.000023,0.000038,0.000064,0.000081,0.000171,0.000361,0.084130]
py_heur = [0.000012,0.000016,0.000021,0.000036,0.000054,0.000077,0.000079,0.000157,0.000521]

# C++
cpp_base = [0.00011858,0.0002228,0.00081554,0.00177346,0.0064581,0.00799656,0.0152688,0.0242039,23.2886]
cpp_heur = [9.888e-05,0.00019332,0.00049408,0.00081942,0.00157924,0.00231396,0.00323436,0.0043537,0.0629136]

# Java
java_base = [9.943e-5,1.19902e-4,3.16322e-4,2.5341e-4,1.43126e-4,3.64962e-4,8.507298e-4,0.001590648,0.091146715]
java_heur = [8.3086e-5,1.40688e-4,2.06116e-4,1.84514e-4,1.64656e-4,1.29818e-4,1.3704e-4,2.98452e-4,0.001194444]


# ==============================
# 📊 GRAFICO 1: TODO JUNTO
# ==============================

fig, ax = plt.subplots()

ax.plot(n, py_base, label="Python Base", marker='o')
ax.plot(n, py_heur, label="Python Heurística", marker='o')

ax.plot(n, cpp_base, label="C++ Base", marker='o')
ax.plot(n, cpp_heur, label="C++ Heurística", marker='o')

ax.plot(n, java_base, label="Java Base", marker='o')
ax.plot(n, java_heur, label="Java Heurística", marker='o')

ax.set_yscale("log")
ax.set_title("Comparación completa: Base vs Heurística")
ax.set_xlabel("Tamaño del problema (n)")
ax.set_ylabel("Tiempo (s)")
ax.legend()
ax.grid()

plt.show()


# ==============================
# 📊 GRAFICO 2: SOLO BASE
# ==============================

fig, ax = plt.subplots()

ax.plot(n, py_base, label="Python", marker='o')
ax.plot(n, cpp_base, label="C++", marker='o')
ax.plot(n, java_base, label="Java", marker='o')

ax.set_yscale("log")
ax.set_title("Comparación de lenguajes (Backtracking Base)")
ax.set_xlabel("n")
ax.set_ylabel("Tiempo (s)")
ax.legend()
ax.grid()

plt.show()


# ==============================
# 📊 GRAFICO 3: SOLO HEURÍSTICA
# ==============================

fig, ax = plt.subplots()

ax.plot(n, py_heur, label="Python", marker='o')
ax.plot(n, cpp_heur, label="C++", marker='o')
ax.plot(n, java_heur, label="Java", marker='o')

ax.set_yscale("log")
ax.set_title("Comparación de lenguajes (Heurística)")
ax.set_xlabel("n")
ax.set_ylabel("Tiempo (s)")
ax.legend()
ax.grid()

plt.show()


# ==============================
# 📊 GRAFICO 4: CRECIMIENTO BASE
# ==============================

fig, ax = plt.subplots()

ax.plot(n, py_base, label="Python Base", marker='o')
ax.plot(n, cpp_base, label="C++ Base", marker='o')
ax.plot(n, java_base, label="Java Base", marker='o')

ax.set_yscale("log")
ax.set_title("Crecimiento exponencial (escala logarítmica)")
ax.set_xlabel("n")
ax.set_ylabel("Tiempo (log s)")
ax.legend()
ax.grid()

plt.show()


# ==============================
# 📊 GRAFICOS INDIVIDUALES
# ==============================

def plot_individual(title, base, heur):
    fig, ax = plt.subplots()

    ax.plot(n, base, marker='o', label="Base")
    ax.plot(n, heur, marker='o', label="Heurística")

    ax.set_yscale("log")
    ax.set_title(title)
    ax.set_xlabel("n")
    ax.set_ylabel("Tiempo (s)")
    ax.legend()
    ax.grid()

    plt.show()


plot_individual("Python: Base vs Heurística", py_base, py_heur)
plot_individual("C++: Base vs Heurística", cpp_base, cpp_heur)
plot_individual("Java: Base vs Heurística", java_base, java_heur)