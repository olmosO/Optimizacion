# -*- coding: utf-8 -*-

import time
import random
import matplotlib.pyplot as plt

# ==============================
# ALGORITMO BASE (IN-PLACE)
# ==============================

def exact_cover(n, S, subsets_with_element, covered, covered_count, solution_indices):
    # Caso base: todos los elementos cubiertos
    if covered_count == n:
        return True

    # Buscar el primer elemento que NO está cubierto (Fuerza Bruta)
    x = 1
    while x <= n and covered[x]:
        x += 1

    if x > n:
        return False

    # Probar solo los subconjuntos que contienen 'x'
    for subset_idx in subsets_with_element[x]:
        subset = S[subset_idx]
        
        # Verificar si es válido (ningún elemento está ya cubierto)
        valid = True
        for elem in subset:
            if covered[elem]:
                valid = False
                break
        
        if valid:
            # AVANZAR: Marcar elementos como cubiertos
            for elem in subset:
                covered[elem] = True
            solution_indices.append(subset_idx)

            # Llamada recursiva
            if exact_cover(n, S, subsets_with_element, covered, covered_count + len(subset), solution_indices):
                return True

            # BACKTRACKING: Desmarcar elementos
            solution_indices.pop()
            for elem in subset:
                covered[elem] = False

    return False


# ==============================
# HEURÍSTICA (IN-PLACE)
# ==============================

def exact_cover_heur(n, S, subsets_with_element, covered, covered_count, solution_indices):
    if covered_count == n:
        return True

    best_x = -1
    min_count = float('inf')

    # Buscar el elemento no cubierto con menor cantidad de subconjuntos válidos
    for i in range(1, n + 1):
        if not covered[i]:
            count = 0
            for subset_idx in subsets_with_element[i]:
                subset = S[subset_idx]
                valid = True
                for elem in subset:
                    if covered[elem]:
                        valid = False
                        break
                if valid:
                    count += 1
            
            if count < min_count:
                min_count = count
                best_x = i
                
            # PODA: Si un elemento no tiene subconjuntos válidos, esta rama no tiene salida
            if min_count == 0:
                return False

    if best_x == -1:
        return False

    for subset_idx in subsets_with_element[best_x]:
        subset = S[subset_idx]
        
        valid = True
        for elem in subset:
            if covered[elem]:
                valid = False
                break
                
        if valid:
            # AVANZAR
            for elem in subset:
                covered[elem] = True
            solution_indices.append(subset_idx)

            if exact_cover_heur(n, S, subsets_with_element, covered, covered_count + len(subset), solution_indices):
                return True

            # BACKTRACKING
            solution_indices.pop()
            for elem in subset:
                covered[elem] = False

    return False


# ==============================
# WRAPPERS Y UTILIDADES
# ==============================

def build_adjacency_list(n, S):
    adj = [[] for _ in range(n + 1)]
    for i, subset in enumerate(S):
        for elem in subset:
            adj[elem].append(i)
    return adj

def solve_base(n, S):
    subsets_with_element = build_adjacency_list(n, S)
    covered = [False] * (n + 1)
    solution_indices = []
    
    start = time.time()
    success = exact_cover(n, S, subsets_with_element, covered, 0, solution_indices)
    end = time.time()
    
    solution = [S[i] for i in solution_indices] if success else None
    return solution, end - start

def solve_heuristic(n, S):
    subsets_with_element = build_adjacency_list(n, S)
    covered = [False] * (n + 1)
    solution_indices = []
    
    start = time.time()
    success = exact_cover_heur(n, S, subsets_with_element, covered, 0, solution_indices)
    end = time.time()
    
    solution = [S[i] for i in solution_indices] if success else None
    return solution, end - start


# ==============================
# CASOS DETERMINÍSTICOS
# ==============================

def test_cases():
    print("=== CASOS DETERMINÍSTICOS ===")

    # Caso 1
    n1 = 4
    S1 = [[1,2], [2,3], [3,4], [1,4]]
    sol1_base, _ = solve_base(n1, S1)
    sol1_heur, _ = solve_heuristic(n1, S1)
    print("Caso 1 (Base):", sol1_base)
    print("Caso 1 (Heur):", sol1_heur)

    # Caso 2 (sin solución)
    n2 = 3
    S2 = [[1,2], [2,3]]
    sol2_base, _ = solve_base(n2, S2)
    sol2_heur, _ = solve_heuristic(n2, S2)
    print("Caso 2 (Base):", sol2_base)
    print("Caso 2 (Heur):", sol2_heur)

    # Caso 3 (múltiple soluciones)
    n3 = 4
    S3 = [[1,2], [3,4], [1,3], [2,4]]
    sol3_base, _ = solve_base(n3, S3)
    sol3_heur, _ = solve_heuristic(n3, S3)
    print("Caso 3 (Base):", sol3_base)
    print("Caso 3 (Heur):", sol3_heur)

    print()


# ==============================
# GENERACIÓN DE INSTANCIAS
# ==============================

def generate_instance(n, num_subsets):
    S = []
    for _ in range(num_subsets):
        size = random.randint(2, 3)
        subset = random.sample(range(1, n + 1), size)
        S.append(subset)
    return n, S


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
            # n * 2 subconjuntos para garantizar densidad
            universe_n, S = generate_instance(n, n * 2)

            _, t_base = solve_base(universe_n, S)
            _, t_heur = solve_heuristic(universe_n, S)

            base_total += t_base
            heur_total += t_heur

        avg_base = base_total / repetitions
        avg_heur = heur_total / repetitions

        results.append((n, avg_base, avg_heur))
        print(f"n={n:2} | Base={avg_base:.6f}s | Heurística={avg_heur:.6f}s")

    return results


# ==============================
# GENERADOR DE GRÁFICOS FINALES
# ==============================
def generar_graficos_finales():
    print("\n===== GENERANDO GRÁFICOS FINALES =====")
    
    n_vals = [6, 8, 10, 12, 14, 16, 18, 20, 40]

    # Python (eliminado el dato de n=30 para que calce con los demás)
    py_base = [0.002, 0.008, 0.015, 0.025, 0.020, 0.075, 0.102, 0.328, 49.350]
    py_heur = [0.008, 0.009, 0.014, 0.032, 0.022, 0.039, 0.050, 0.079, 0.298]

    # C++
    cpp_base = [0.0104, 0.01478, 0.0189, 0.02738, 0.0355, 0.07246, 0.18116, 0.43162, 5.22098]
    cpp_heur = [0.0131, 0.0177, 0.02402, 0.03214, 0.04702, 0.0572, 0.05174, 0.09192, 0.20422]

    # Java
    java_base = [0.05778, 0.0297, 0.04926, 0.01774, 0.02358, 0.03758, 0.3631, 0.06482, 2.68356]
    java_heur = [0.0398, 0.0473, 0.05696, 0.07606, 0.03558, 0.02796, 0.04138, 0.03472, 0.18826]

    # 📊 GRAFICO 1: TODO JUNTO
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(n_vals, py_base, label="Python Base", marker='o')
    ax.plot(n_vals, py_heur, label="Python Heurística", marker='o')
    ax.plot(n_vals, cpp_base, label="C++ Base", marker='o')
    ax.plot(n_vals, cpp_heur, label="C++ Heurística", marker='o')
    ax.plot(n_vals, java_base, label="Java Base", marker='o')
    ax.plot(n_vals, java_heur, label="Java Heurística", marker='o')
    ax.set_yscale("log")
    ax.set_title("Comparación completa: Base vs Heurística")
    ax.set_xlabel("Tamaño del problema (n)")
    ax.set_ylabel("Tiempo (ms)")
    ax.legend()
    ax.grid()
    plt.show()

    # 📊 GRAFICO 2: SOLO BASE
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(n_vals, py_base, label="Python", marker='o')
    ax.plot(n_vals, cpp_base, label="C++", marker='o')
    ax.plot(n_vals, java_base, label="Java", marker='o')
    ax.set_yscale("log")
    ax.set_title("Comparación de lenguajes (Backtracking Base)")
    ax.set_xlabel("n")
    ax.set_ylabel("Tiempo (ms)")
    ax.legend()
    ax.grid()
    plt.show()

    # 📊 GRAFICO 3: SOLO HEURÍSTICA
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(n_vals, py_heur, label="Python", marker='o')
    ax.plot(n_vals, cpp_heur, label="C++", marker='o')
    ax.plot(n_vals, java_heur, label="Java", marker='o')
    ax.set_yscale("log")
    ax.set_title("Comparación de lenguajes (Heurística)")
    ax.set_xlabel("n")
    ax.set_ylabel("Tiempo (ms)")
    ax.legend()
    ax.grid()
    plt.show()

    # 📊 GRAFICO 4: CRECIMIENTO BASE
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(n_vals, py_base, label="Python Base", marker='o')
    ax.plot(n_vals, cpp_base, label="C++ Base", marker='o')
    ax.plot(n_vals, java_base, label="Java Base", marker='o')
    ax.set_yscale("log")
    ax.set_title("Crecimiento exponencial (escala logarítmica)")
    ax.set_xlabel("n")
    ax.set_ylabel("Tiempo (log ms)")
    ax.legend()
    ax.grid()
    plt.show()

    # 📊 GRAFICOS INDIVIDUALES
    def plot_individual(title, base, heur):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(n_vals, base, marker='o', label="Base")
        ax.plot(n_vals, heur, marker='o', label="Heurística")
        ax.set_yscale("log")
        ax.set_title(title)
        ax.set_xlabel("n")
        ax.set_ylabel("Tiempo (ms)")
        ax.legend()
        ax.grid()
        plt.show()

    plot_individual("Python: Base vs Heurística", py_base, py_heur)
    plot_individual("C++: Base vs Heurística", cpp_base, cpp_heur)
    plot_individual("Java: Base vs Heurística", java_base, java_heur)


# ==============================
# MAIN
# ==============================

def main():
    random.seed(42)  # Semilla fija para reproducibilidad

    print("===== TEST DE CORRECTITUD =====")
    test_cases()

    print("===== EXPERIMENTOS =====")
    sizes = [6, 8, 10, 12, 14, 16, 18, 20, 30, 40]
    results = run_experiments(sizes, repetitions=5)

    print("\n===== GUARDANDO RESULTADOS =====")
    with open("results_python.csv", "w") as f:
        f.write("n,base,heur\n")
        for r in results:
            f.write(f"{r[0]},{r[1]:.6f},{r[2]:.6f}\n")
    print("Resultados guardados en results_python.csv")

    # Llamar a la función que genera todos los gráficos
    generar_graficos_finales()


if __name__ == "__main__":
    main()
