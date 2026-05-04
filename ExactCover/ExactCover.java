import java.util.*;
import java.io.FileWriter;
import java.io.IOException;

public class ExactCover {

    // ==============================
    // BACKTRACKING BASE
    // ==============================

    public static boolean exactCover(Set<Integer> X, List<Set<Integer>> S, List<Set<Integer>> solution) {
        if (X.isEmpty()) return true;

        int x = X.iterator().next();

        for (Set<Integer> subset : S) {
            if (subset.contains(x)) {

                Set<Integer> newX = new HashSet<>(X);
                List<Set<Integer>> newS = new ArrayList<>();

                for (int elem : subset) {
                    newX.remove(elem);
                }

                for (Set<Integer> s : S) {
                    boolean disjoint = true;
                    for (int e : s) {
                        if (subset.contains(e)) {
                            disjoint = false;
                            break;
                        }
                    }
                    if (disjoint) newS.add(s);
                }

                solution.add(subset);

                if (exactCover(newX, newS, solution))
                    return true;

                solution.remove(solution.size() - 1);
            }
        }

        return false;
    }

    // ==============================
    // HEURÍSTICA
    // ==============================

    public static int chooseBestElement(Set<Integer> X, List<Set<Integer>> S) {
        int best = -1;
        int minCount = Integer.MAX_VALUE;

        for (int x : X) {
            int count = 0;
            for (Set<Integer> s : S) {
                if (s.contains(x)) count++;
            }

            if (count < minCount) {
                minCount = count;
                best = x;
            }
        }

        return best;
    }

    public static boolean exactCoverHeuristic(Set<Integer> X, List<Set<Integer>> S, List<Set<Integer>> solution) {
        if (X.isEmpty()) return true;

        int x = chooseBestElement(X, S);

        for (Set<Integer> subset : S) {
            if (subset.contains(x)) {

                Set<Integer> newX = new HashSet<>(X);
                List<Set<Integer>> newS = new ArrayList<>();

                for (int elem : subset) {
                    newX.remove(elem);
                }

                for (Set<Integer> s : S) {
                    boolean disjoint = true;
                    for (int e : s) {
                        if (subset.contains(e)) {
                            disjoint = false;
                            break;
                        }
                    }
                    if (disjoint) newS.add(s);
                }

                solution.add(subset);

                if (exactCoverHeuristic(newX, newS, solution))
                    return true;

                solution.remove(solution.size() - 1);
            }
        }

        return false;
    }

    // ==============================
    // IMPRIMIR SOLUCIÓN
    // ==============================

    public static void printSolution(List<Set<Integer>> solution) {
        if (solution.isEmpty()) {
            System.out.println("No existe solución");
            return;
        }

        System.out.print("{ ");
        for (Set<Integer> s : solution) {
            System.out.print("{");
            Iterator<Integer> it = s.iterator();
            while (it.hasNext()) {
                System.out.print(it.next());
                if (it.hasNext()) System.out.print(",");
            }
            System.out.print("} ");
        }
        System.out.println("}");
    }

    // ==============================
    // CASOS DETERMINÍSTICOS
    // ==============================

    public static void testCases() {
        System.out.println("===== CASOS DETERMINÍSTICOS =====");

        // Caso 1
        Set<Integer> X1 = new HashSet<>(Arrays.asList(1,2,3,4));
        List<Set<Integer>> S1 = Arrays.asList(
            new HashSet<>(Arrays.asList(1,2)),
            new HashSet<>(Arrays.asList(2,3)),
            new HashSet<>(Arrays.asList(3,4)),
            new HashSet<>(Arrays.asList(1,4))
        );

        List<Set<Integer>> sol = new ArrayList<>();
        exactCover(X1, S1, sol);
        System.out.print("Caso 1 (Base): ");
        printSolution(sol);

        sol.clear();
        exactCoverHeuristic(X1, S1, sol);
        System.out.print("Caso 1 (Heur): ");
        printSolution(sol);


        // Caso 2 (sin solución)
        Set<Integer> X2 = new HashSet<>(Arrays.asList(1,2,3));
        List<Set<Integer>> S2 = Arrays.asList(
            new HashSet<>(Arrays.asList(1,2)),
            new HashSet<>(Arrays.asList(2,3))
        );

        sol.clear();
        exactCover(X2, S2, sol);
        System.out.print("Caso 2 (Base): ");
        printSolution(sol);

        sol.clear();
        exactCoverHeuristic(X2, S2, sol);
        System.out.print("Caso 2 (Heur): ");
        printSolution(sol);


        // Caso 3 (múltiples soluciones)
        Set<Integer> X3 = new HashSet<>(Arrays.asList(1,2,3,4));
        List<Set<Integer>> S3 = Arrays.asList(
            new HashSet<>(Arrays.asList(1,2)),
            new HashSet<>(Arrays.asList(3,4)),
            new HashSet<>(Arrays.asList(1,3)),
            new HashSet<>(Arrays.asList(2,4))
        );

        sol.clear();
        exactCover(X3, S3, sol);
        System.out.print("Caso 3 (Base): ");
        printSolution(sol);

        sol.clear();
        exactCoverHeuristic(X3, S3, sol);
        System.out.print("Caso 3 (Heur): ");
        printSolution(sol);

        System.out.println();
    }

    // ==============================
    // GENERADOR ALEATORIO
    // ==============================

    public static Pair generateInstance(int n, int numSubsets) {
        Set<Integer> X = new HashSet<>();
        for (int i = 1; i <= n; i++) X.add(i);

        List<Set<Integer>> S = new ArrayList<>();
        Random rand = new Random();

        for (int i = 0; i < numSubsets; i++) {
            int size = 2 + rand.nextInt(2);
            Set<Integer> subset = new HashSet<>();

            while (subset.size() < size) {
                subset.add(rand.nextInt(n) + 1);
            }

            S.add(subset);
        }

        return new Pair(X, S);
    }

    // ==============================
    // TIEMPOS
    // ==============================

    public static double runBase(Set<Integer> X, List<Set<Integer>> S) {
        List<Set<Integer>> solution = new ArrayList<>();

        long start = System.nanoTime();
        exactCover(X, S, solution);
        long end = System.nanoTime();

        return (end - start) / 1e9;
    }

    public static double runHeuristic(Set<Integer> X, List<Set<Integer>> S) {
        List<Set<Integer>> solution = new ArrayList<>();

        long start = System.nanoTime();
        exactCoverHeuristic(X, S, solution);
        long end = System.nanoTime();

        return (end - start) / 1e9;
    }

    // ==============================
    // CLASE AUXILIAR
    // ==============================

    static class Pair {
        Set<Integer> X;
        List<Set<Integer>> S;

        Pair(Set<Integer> X, List<Set<Integer>> S) {
            this.X = X;
            this.S = S;
        }
    }

    // ==============================
    // MAIN
    // ==============================

    public static void main(String[] args) {

        // 🔹 1. Correctitud
        testCases();

        // 🔹 2. Experimentos
        int[] sizes = {6, 8, 10, 12, 14, 16, 18, 20, 40};
        int repetitions = 5;

        try {
            FileWriter writer = new FileWriter("results_java.csv");
            writer.write("n,base,heur\n");

            System.out.println("===== EXPERIMENTOS =====");

            for (int n : sizes) {
                double baseTotal = 0;
                double heurTotal = 0;

                for (int i = 0; i < repetitions; i++) {
                    Pair instance = generateInstance(n, n * 2);

                    baseTotal += runBase(instance.X, instance.S);
                    heurTotal += runHeuristic(instance.X, instance.S);
                }

                double avgBase = baseTotal / repetitions;
                double avgHeur = heurTotal / repetitions;

                System.out.println("n=" + n +
                        " | Base=" + avgBase +
                        " | Heur=" + avgHeur);

                writer.write(n + "," + avgBase + "," + avgHeur + "\n");
            }

            writer.close();
            System.out.println("\nResultados guardados en results_java.csv");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}