package puzzle8;

//-	Rivas Uriarte Fernando Noé – 23170303 – IA – 18:00-19:00 - 

import java.util.List;

public class App {

    // en true para ver los tableros paso a paso
    static boolean MOSTRAR_CAMINOS = true;

    public static void main(String[] args) {

        String initialState = "7621 8435";
        String goalState = "12345678 ";

        System.out.println("Estado inicial:");
        System.out.println(NodeUtils.formatState(initialState));
        System.out.println("Estado meta:");
        System.out.println(NodeUtils.formatState(goalState));

        PuzzleTree tree = new PuzzleTree(initialState, goalState);

        correr(tree, "Anchura (BFS)", 1);
        correr(tree, "Profundidad (DFS)", 2);
        correr(tree, "Costo uniforme (UCS)", 3);
        correr(tree, "Profundidad iterativa (IDDFS)", 4);
    }

    // tipo: 1 anchura, 2 profundidad, 3 costo uniforme, 4 iterativa
    static void correr(PuzzleTree tree, String nombre, int tipo) {
        Runtime runtime = Runtime.getRuntime();
        runtime.gc();
        long memoriaAntes = runtime.totalMemory() - runtime.freeMemory();
        long inicio = System.nanoTime();

        boolean encontrado;
        if (tipo == 1) {
            encontrado = tree.breadthFirstSearch();
        } else if (tipo == 2) {
            encontrado = tree.depthFirstSearch();
        } else if (tipo == 3) {
            encontrado = tree.uniformCostSearch();
        } else {
            encontrado = tree.iterativeDeepeningSearch(31);
        }

        long fin = System.nanoTime();
        long memoriaDespues = runtime.totalMemory() - runtime.freeMemory();

        double tiempo = (fin - inicio) / 1000000.0;
        long memoria = memoriaDespues - memoriaAntes;
        if (memoria < 0) {
            memoria = 0;
        }

        System.out.println("=========================================");
        System.out.println(nombre);
        System.out.println("=========================================");

        if (!encontrado) {
            System.out.println("No se encontro la meta");
            return;
        }

        List<String> path = tree.getPath();
        int movimientos = path.size() - 1;

        // la profundidad tiene miles de pasos, no se imprime
        if (MOSTRAR_CAMINOS && movimientos <= 50) {
            for (int i = 0; i < path.size(); i++) {
                System.out.println("Paso " + i + ":");
                System.out.println(NodeUtils.formatState(path.get(i)));
            }
        }

        System.out.println("Movimientos: " + movimientos);
        System.out.println("Costo total: " + NodeUtils.pathCost(path));
        System.out.println("Nodos expandidos: " + tree.getExpanded());
        System.out.println("Nodos generados: " + tree.getGenerated());
        System.out.println("Tiempo de ejecucion: " + tiempo + " ms");
        System.out.printf("Memoria consumida: %.2f MB (%d bytes)%n", memoria / (1024.0 * 1024.0), memoria);
        System.out.println();
    }
}