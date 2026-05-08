#include <bits/stdc++.h>
using namespace std;

// Usamos vector en lugar de set porque iterar sobre vectores es mucho más rápido
// y la memoria es contigua.
using Subset = vector<int>;
using Subsets = vector<Subset>;

// ==============================
// BACKTRACKING BASE (Sin Copias)
// ==============================

bool exact_cover(int n, const Subsets& S, const vector<vector<int>>& subsets_with_element, 
                      vector<bool>& covered, int covered_count, vector<int>& solution) {
    // Caso base: Si hemos cubierto todos los elementos, terminamos.
    if (covered_count == n) return true;

    // Buscar el primer elemento no cubierto
    int x = 1;
    while (x <= n && covered[x]) x++;

    if (x > n) return false; 

    // Probar solo los subconjuntos que sabemos que contienen 'x'
    for (int subset_idx : subsets_with_element[x]) {
        const auto& subset = S[subset_idx];
        
        // Verificar si el subconjunto es válido (ningún elemento está ya cubierto)
        bool valid = true;
        for (int elem : subset) {
            if (covered[elem]) {
                valid = false;
                break;
            }
        }

        if (valid) {
            // AVANZAR: Marcar elementos como cubiertos
            for (int elem : subset) covered[elem] = true;
            solution.push_back(subset_idx);

            // Llamada recursiva
            if (exact_cover(n, S, subsets_with_element, covered, covered_count + subset.size(), solution))
                return true;

            // BACKTRACKING: Desmarcar elementos para intentar otra rama
            solution.pop_back();
            for (int elem : subset) covered[elem] = false;
        }
    }

    return false;
}


// ==============================
// HEURÍSTICA (Sin Copias)
// ==============================

bool exact_cover_heur(int n, const Subsets& S, const vector<vector<int>>& subsets_with_element, 
                           vector<bool>& covered, int covered_count, vector<int>& solution) {
    if (covered_count == n) return true;

    int best_x = -1;
    int min_count = INT_MAX;

    // Buscar el elemento no cubierto con la menor cantidad de subconjuntos VÁLIDOS
    for (int i = 1; i <= n; i++) {
        if (!covered[i]) {
            int count = 0;
            for (int subset_idx : subsets_with_element[i]) {
                bool valid = true;
                for (int elem : S[subset_idx]) {
                    if (covered[elem]) {
                        valid = false;
                        break;
                    }
                }
                if (valid) count++;
            }
            
            if (count < min_count) {
                min_count = count;
                best_x = i;
            }
            
            // PODA FUERTE: Si un elemento no puede ser cubierto por ningún 
            // subconjunto disponible, esta rama es un callejón sin salida inmediato.
            if (min_count == 0) return false; 
        }
    }

    if (best_x == -1) return false;

    // Probar los subconjuntos válidos que contienen 'best_x'
    for (int subset_idx : subsets_with_element[best_x]) {
        const auto& subset = S[subset_idx];
        
        bool valid = true;
        for (int elem : subset) {
            if (covered[elem]) {
                valid = false;
                break;
            }
        }

        if (valid) {
            // AVANZAR
            for (int elem : subset) covered[elem] = true;
            solution.push_back(subset_idx);

            if (exact_cover_heur(n, S, subsets_with_element, covered, covered_count + subset.size(), solution))
                return true;

            // BACKTRACKING
            solution.pop_back();
            for (int elem : subset) covered[elem] = false;
        }
    }

    return false;
}


// ==============================
// FUNCIONES WRAPPER
// ==============================
// Estas funciones preparan las estructuras optimizadas antes de lanzar la recursión.

bool solve_base(int n, const Subsets& S, vector<int>& solution_indices) {
    // Crear lista de adyacencia: para cada elemento, qué índices de S lo contienen.
    vector<vector<int>> subsets_with_element(n + 1);
    for (size_t i = 0; i < S.size(); i++) {
        for (int elem : S[i]) {
            subsets_with_element[elem].push_back(i);
        }
    }
    vector<bool> covered(n + 1, false);
    return exact_cover(n, S, subsets_with_element, covered, 0, solution_indices);
}

bool solve_heuristic(int n, const Subsets& S, vector<int>& solution_indices) {
    vector<vector<int>> subsets_with_element(n + 1);
    for (size_t i = 0; i < S.size(); i++) {
        for (int elem : S[i]) {
            subsets_with_element[elem].push_back(i);
        }
    }
    vector<bool> covered(n + 1, false);
    return exact_cover_heur(n, S, subsets_with_element, covered, 0, solution_indices);
}


// ==============================
// IMPRIMIR SOLUCIÓN
// ==============================

void print_solution(const Subsets& S, const vector<int>& sol_indices) {
    if (sol_indices.empty()) {
        cout << "No existe solución\n";
        return;
    }

    cout << "{ ";
    for (int idx : sol_indices) {
        cout << "{";
        for (size_t i = 0; i < S[idx].size(); i++) {
            cout << S[idx][i];
            if (i + 1 < S[idx].size()) cout << ",";
        }
        cout << "} ";
    }
    cout << "}\n";
}


// ==============================
// CASOS DETERMINÍSTICOS
// ==============================

void test_cases() {
    cout << "===== CASOS DETERMINÍSTICOS =====\n";

    // Caso 1
    int n1 = 4;
    Subsets S1 = {{1,2}, {2,3}, {3,4}, {1,4}};
    vector<int> sol1;

    solve_base(n1, S1, sol1);
    cout << "Caso 1 (Base): "; print_solution(S1, sol1);

    sol1.clear();
    solve_heuristic(n1, S1, sol1);
    cout << "Caso 1 (Heur): "; print_solution(S1, sol1);


    // Caso 2 (sin solución)
    int n2 = 3;
    Subsets S2 = {{1,2}, {2,3}};
    vector<int> sol2;

    solve_base(n2, S2, sol2);
    cout << "Caso 2 (Base): "; print_solution(S2, sol2);

    sol2.clear();
    solve_heuristic(n2, S2, sol2);
    cout << "Caso 2 (Heur): "; print_solution(S2, sol2);


    // Caso 3 (múltiples soluciones)
    int n3 = 4;
    Subsets S3 = {{1,2}, {3,4}, {1,3}, {2,4}};
    vector<int> sol3;

    solve_base(n3, S3, sol3);
    cout << "Caso 3 (Base): "; print_solution(S3, sol3);

    sol3.clear();
    solve_heuristic(n3, S3, sol3);
    cout << "Caso 3 (Heur): "; print_solution(S3, sol3);

    cout << endl;
}


// ==============================
// GENERADOR ALEATORIO
// ==============================

pair<int, Subsets> generate_instance(int n, int num_subsets) {
    Subsets S;
    for (int i = 0; i < num_subsets; i++) {
        int size = 2 + rand() % 2;
        set<int> subset;
        while ((int)subset.size() < size) {
            subset.insert((rand() % n) + 1);
        }
        // Pasamos el set a vector
        S.push_back(vector<int>(subset.begin(), subset.end()));
    }
    return {n, S};
}


// ==============================
// TIEMPOS
// ==============================

double run_base(int n, const Subsets& S) {
    vector<int> solution;
    auto start = chrono::high_resolution_clock::now();
    solve_base(n, S, solution);
    auto end = chrono::high_resolution_clock::now();
    return chrono::duration<double>(end - start).count();
}

double run_heuristic(int n, const Subsets& S) {
    vector<int> solution;
    auto start = chrono::high_resolution_clock::now();
    solve_heuristic(n, S, solution);
    auto end = chrono::high_resolution_clock::now();
    return chrono::duration<double>(end - start).count();
}


// ==============================
// MAIN
// ==============================

int main() {
    srand(time(0));

    // 🔹 1. Casos determinísticos
    test_cases();

    // 🔹 2. Experimentos aleatorios
    cout << "===== EXPERIMENTOS =====\n";

    vector<int> sizes = {6, 8, 10, 12, 14, 16, 18, 20, 40};
    int repetitions = 5;

    ofstream file("results_cpp.csv");
    file << "n,base,heur\n";

    for (int n : sizes) {
        double base_total = 0;
        double heur_total = 0;

        for (int i = 0; i < repetitions; i++) {
            auto [universe_n, S] = generate_instance(n, n * 2);

            base_total += run_base(universe_n, S);
            heur_total += run_heuristic(universe_n, S);
        }

        double avg_base = base_total / repetitions;
        double avg_heur = heur_total / repetitions;

        cout << "n=" << n 
             << " | Base=" << fixed << setprecision(6) << avg_base 
             << " | Heur=" << avg_heur << endl;

        file << n << "," << avg_base << "," << avg_heur << "\n";
    }

    file.close();

    cout << "\nResultados guardados en results_cpp.csv\n";

    return 0;
}
