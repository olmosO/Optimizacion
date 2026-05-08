import java.util.*;
import java.io.FileWriter;
import java.io.IOException;

public class ExactCover {

    // ==============================
    // BACKTRACKING BASE (Sin copias en memoria)
    // ==============================

    public static boolean exactCover(int n, List<List<Integer>> S, List<List<Integer>> subsetsWithElement,
                                         boolean[] covered, int coveredCount, List<Integer> solutionIndices) {
        if (coveredCount == n) return true;

        // Buscar el primer elemento no cubierto
        int x = 1;
        while (x <= n && covered[x]) x++;
        if (x > n) return false;

        // Probar solo subconjuntos que contienen 'x'
        for (int subsetIdx : subsetsWithElement.get(x)) {
            List<Integer> subset = S.get(subsetIdx);

            // Verificar si es válido (ningún elemento está ya cubierto)
            boolean valid = true;
            for (int elem : subset) {
                if (covered[elem]) {
                    valid = false;
                    break;
                }
            }

            if (valid) {
                // AVANZAR (Marcar)
                for (int elem : subset) covered[elem] = true;
                solutionIndices.add(subsetIdx);

                if (exactCover(n, S, subsetsWithElement, covered, coveredCount + subset.size(), solutionIndices))
                    return true;

                // RETROCEDER / BACKTRACKING (Desmarcar)
                solutionIndices.remove(solutionIndices.size() - 1);
                for (int elem : subset) covered[elem] = false;
            }
        }
        return false;
    }

    // ==============================
    // HEURÍSTICA (Sin copias y con poda fuerte)
    // ==============================

    public static boolean exactCoverHeur(int n, List<List<Integer>> S, List<List<Integer>> subsetsWithElement,
                                             boolean[] covered, int coveredCount, List<Integer> solutionIndices) {
        if (coveredCount == n) return true;

        int bestX = -1;
        int minCount = Integer.MAX_VALUE;

        // Buscar elemento no cubierto con menor cantidad de subconjuntos válidos
        for (int i = 1; i <= n; i++) {
            if (!covered[i]) {
                int count = 0;
                for (int subsetIdx : subsetsWithElement.get(i)) {
                    boolean valid = true;
                    for (int elem : S.get(subsetIdx)) {
                        if (covered[elem]) {
                            valid = false;
                            break;
                        }
                    }
                    if (valid) count++;
                }

                if (count < minCount) {
                    minCount = count;
                    bestX = i;
                }

                // PODA: Si un elemento no tiene subconjuntos válidos, esta rama es un callejón sin salida
                if (minCount == 0) return false;
            }
        }

        if (bestX == -1) return false;

        for (int subsetIdx : subsetsWithElement.get(bestX)) {
            List<Integer> subset = S.get(subsetIdx);

            boolean valid = true;
            for (int elem : subset) {
                if (covered[elem]) {
                    valid = false;
                    break;
                }
            }

            if (valid) {
                // AVANZAR
                for (int elem : subset) covered[elem] = true;
                solutionIndices.add(subsetIdx);

                if (exactCoverHeur(n, S, subsetsWithElement, covered, coveredCount + subset.size(), solutionIndices))
                    return true;

                // BACKTRACKING
                solutionIndices.remove(solutionIndices.size() - 1);
                for (int elem : subset) covered[elem] = false;
            }
        }
        return false;
    }

    // ==============================
    // WRAPPERS PARA PREPARAR DATOS
    // ==============================

    public static boolean solveBase(int n, List<List<Integer>> S, List<Integer> solutionIndices) {
        List<List<Integer>> subsetsWithElement = buildAdjacencyList(n, S);
        boolean[] covered = new boolean[n + 1];
        return exactCover(n, S, subsetsWithElement, covered, 0, solutionIndices);
    }

    public static boolean solveHeuristic(int n, List<List<Integer>> S, List<Integer> solutionIndices) {
        List<List<Integer>> subsetsWithElement = buildAdjacencyList(n, S);
        boolean[] covered = new boolean[n + 1];
        return exactCoverHeur(n, S, subsetsWithElement, covered, 0, solutionIndices);
    }

    private static List<List<Integer>> buildAdjacencyList(int n, List<List<Integer>> S) {
        List<List<Integer>> adj = new ArrayList<>(n + 1);
        for (int i = 0; i <= n; i++) adj.add(new ArrayList<>());
        for (int i = 0; i < S.size(); i++) {
            for (int elem : S.get(i)) {
                adj.get(elem).add(i);
            }
        }
        return adj;
    }

    // ==============================
    // IMPRIMIR SOLUCIÓN
    // ==============================

    public static void printSolution(List<List<Integer>> S, List<Integer> solutionIndices) {
        if (solutionIndices.isEmpty()) {
            System.out.println("No existe solución");
            return;
        }
        System.out.print("{ ");
        for (int idx : solutionIndices) {
            System.out.print("{");
            List<Integer> sub = S.get(idx);
            for (int i = 0; i < sub.size(); i++) {
                System.out.print(sub.get(i));
                if (i < sub.size() - 1) System.out.print(",");
            }
            System.out.print("} ");
        }
        System.out.println("}");
    }

    // ==============================
    // GENERADOR ALEATORIO
    // ==============================

    static class Instance {
        int n;
        List<List<Integer>> S;
        Instance(int n, List<List<Integer>> S) { this.n = n; this.S = S; }
    }

    public static Instance generateInstance(int n, int numSubsets) {
        List<List<Integer>> S = new ArrayList<>();
        Random rand = new Random();

        for (int i = 0; i < numSubsets; i++) {
            int size = 2 + rand.nextInt(2);
            Set<Integer> subset = new HashSet<>();
            while (subset.size() < size) {
                subset.add(rand.nextInt(n) + 1);
            }
            S.add(new ArrayList<>(subset)); // Convertimos a List para acceso rápido
        }
        return new Instance(n, S);
    }

    // ==============================
    // MAIN
    // ==============================

    public static void main(String[] args) {
        // CASOS DETERMINÍSTICOS
        System.out.println("===== CASOS DETERMINÍSTICOS =====");
        int n1 = 4;
        List<List<Integer>> S1 = Arrays.asList(
            Arrays.asList(1, 2), Arrays.asList(2, 3), Arrays.asList(3, 4), Arrays.asList(1, 4)
        );
        List<Integer> sol1 = new ArrayList<>();
        solveBase(n1, S1, sol1);
        System.out.print("Caso 1 (Base): "); printSolution(S1, sol1);
        
        sol1.clear();
        solveHeuristic(n1, S1, sol1);
        System.out.print("Caso 1 (Heur): "); printSolution(S1, sol1);
        System.out.println();

        // EXPERIMENTOS
        int[] sizes = {6, 8, 10, 12, 14, 16, 18, 20, 40};
        int repetitions = 5;

        try (FileWriter writer = new FileWriter("results_java.csv")) {
            writer.write("n,base,heur\n");
            System.out.println("===== EXPERIMENTOS =====");

            for (int n : sizes) {
                double baseTotal = 0;
                double heurTotal = 0;

                for (int i = 0; i < repetitions; i++) {
                    Instance instance = generateInstance(n, n * 2);

                    List<Integer> solBase = new ArrayList<>();
                    long startBase = System.nanoTime();
                    solveBase(instance.n, instance.S, solBase);
                    baseTotal += (System.nanoTime() - startBase) / 1e9;

                    List<Integer> solHeur = new ArrayList<>();
                    long startHeur = System.nanoTime();
                    solveHeuristic(instance.n, instance.S, solHeur);
                    heurTotal += (System.nanoTime() - startHeur) / 1e9;
                }

                double avgBase = baseTotal / repetitions;
                double avgHeur = heurTotal / repetitions;

                System.out.printf("n=%d | Base=%.6f | Heur=%.6f\n", n, avgBase, avgHeur);
                writer.write(n + "," + avgBase + "," + avgHeur + "\n");
            }
            System.out.println("\nResultados guardados en results_java.csv");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
