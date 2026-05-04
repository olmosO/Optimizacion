#include <bits/stdc++.h>
using namespace std;

using Set = set<int>;
using Subsets = vector<Set>;


// ==============================
// BACKTRACKING BASE
// ==============================

bool exact_cover(Set X, Subsets S, vector<Set>& solution) {
    if (X.empty()) return true;

    int x = *X.begin();

    for (auto& subset : S) {
        if (subset.count(x)) {
            Set newX = X;
            Subsets newS;

            for (int elem : subset) {
                newX.erase(elem);
            }

            for (auto& s : S) {
                bool disjoint = true;
                for (int e : s) {
                    if (subset.count(e)) {
                        disjoint = false;
                        break;
                    }
                }
                if (disjoint) newS.push_back(s);
            }

            solution.push_back(subset);

            if (exact_cover(newX, newS, solution))
                return true;

            solution.pop_back();
        }
    }

    return false;
}


// ==============================
// HEURÍSTICA
// ==============================

int choose_best_element(const Set& X, const Subsets& S) {
    int best = -1;
    int min_count = INT_MAX;

    for (int x : X) {
        int count = 0;
        for (auto& s : S) {
            if (s.count(x)) count++;
        }

        if (count < min_count) {
            min_count = count;
            best = x;
        }
    }

    return best;
}

bool exact_cover_heuristic(Set X, Subsets S, vector<Set>& solution) {
    if (X.empty()) return true;

    int x = choose_best_element(X, S);

    for (auto& subset : S) {
        if (subset.count(x)) {
            Set newX = X;
            Subsets newS;

            for (int elem : subset) {
                newX.erase(elem);
            }

            for (auto& s : S) {
                bool disjoint = true;
                for (int e : s) {
                    if (subset.count(e)) {
                        disjoint = false;
                        break;
                    }
                }
                if (disjoint) newS.push_back(s);
            }

            solution.push_back(subset);

            if (exact_cover_heuristic(newX, newS, solution))
                return true;

            solution.pop_back();
        }
    }

    return false;
}


// ==============================
// IMPRIMIR SOLUCIÓN
// ==============================

void print_solution(const vector<Set>& solution) {
    if (solution.empty()) {
        cout << "No existe solución\n";
        return;
    }

    cout << "{ ";
    for (auto& s : solution) {
        cout << "{";
        for (auto it = s.begin(); it != s.end(); ++it) {
            cout << *it;
            if (next(it) != s.end()) cout << ",";
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
    Set X1 = {1,2,3,4};
    Subsets S1 = {{1,2}, {2,3}, {3,4}, {1,4}};
    vector<Set> sol1;

    exact_cover(X1, S1, sol1);
    cout << "Caso 1 (Base): ";
    print_solution(sol1);

    sol1.clear();
    exact_cover_heuristic(X1, S1, sol1);
    cout << "Caso 1 (Heur): ";
    print_solution(sol1);


    // Caso 2 (sin solución)
    Set X2 = {1,2,3};
    Subsets S2 = {{1,2}, {2,3}};
    vector<Set> sol2;

    exact_cover(X2, S2, sol2);
    cout << "Caso 2 (Base): ";
    print_solution(sol2);

    sol2.clear();
    exact_cover_heuristic(X2, S2, sol2);
    cout << "Caso 2 (Heur): ";
    print_solution(sol2);


    // Caso 3 (múltiples soluciones)
    Set X3 = {1,2,3,4};
    Subsets S3 = {{1,2}, {3,4}, {1,3}, {2,4}};
    vector<Set> sol3;

    exact_cover(X3, S3, sol3);
    cout << "Caso 3 (Base): ";
    print_solution(sol3);

    sol3.clear();
    exact_cover_heuristic(X3, S3, sol3);
    cout << "Caso 3 (Heur): ";
    print_solution(sol3);

    cout << endl;
}


// ==============================
// GENERADOR ALEATORIO
// ==============================

pair<Set, Subsets> generate_instance(int n, int num_subsets) {
    Set X;
    for (int i = 1; i <= n; i++) X.insert(i);

    Subsets S;

    for (int i = 0; i < num_subsets; i++) {
        int size = 2 + rand() % 2;
        Set subset;

        while ((int)subset.size() < size) {
            int val = (rand() % n) + 1;
            subset.insert(val);
        }

        S.push_back(subset);
    }

    return {X, S};
}


// ==============================
// TIEMPOS
// ==============================

double run_base(Set X, Subsets S) {
    vector<Set> solution;

    auto start = chrono::high_resolution_clock::now();
    exact_cover(X, S, solution);
    auto end = chrono::high_resolution_clock::now();

    return chrono::duration<double>(end - start).count();
}

double run_heuristic(Set X, Subsets S) {
    vector<Set> solution;

    auto start = chrono::high_resolution_clock::now();
    exact_cover_heuristic(X, S, solution);
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
            auto [X, S] = generate_instance(n, n * 2);

            base_total += run_base(X, S);
            heur_total += run_heuristic(X, S);
        }

        double avg_base = base_total / repetitions;
        double avg_heur = heur_total / repetitions;

        cout << "n=" << n 
             << " | Base=" << avg_base 
             << " | Heur=" << avg_heur << endl;

        file << n << "," << avg_base << "," << avg_heur << "\n";
    }

    file.close();

    cout << "\nResultados guardados en results_cpp.csv\n";

    return 0;
}