package puzzle8;
//-	Rivas Uriarte Fernando Noé – 23170303 – IA – 18:00-19:00 - 

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class NodeUtils {

    private static String swapPositions(String state, int pos1, int pos2) {
        char[] arr = state.toCharArray();
        char temp = arr[pos1];
        arr[pos1] = arr[pos2];
        arr[pos2] = temp;
        return new String(arr);
    }

    // Genera los hijos moviendo el hueco. El costo de cada movimiento
    // es el numero de la ficha que se mueve.
    public static List<Node> generateChildren(Node parentNode) {
        List<Node> successors = new ArrayList<>();
        String state = parentNode.getState();
        int zeroPos = state.indexOf(" ");

        int[][] adjacentPositions = {
            {1, 3},           // pos 0
            {0, 2, 4},        // pos 1
            {1, 5},           // pos 2
            {0, 4, 6},        // pos 3
            {1, 3, 5, 7},     // pos 4
            {2, 4, 8},        // pos 5
            {3, 7},           // pos 6
            {4, 6, 8},        // pos 7
            {5, 7}            // pos 8
        };

        for (int adjPos : adjacentPositions[zeroPos]) {
            String newState = swapPositions(state, zeroPos, adjPos);
            Node child = new Node(newState, parentNode);
            int ficha = state.charAt(adjPos) - '0';
            child.setCost(parentNode.getCost() + ficha);
            successors.add(child);
        }
        return successors;
    }

    // Estados desde la raiz hasta el nodo
    public static List<String> pathTo(Node node) {
        List<String> path = new ArrayList<>();
        while (node != null) {
            path.add(node.getState());
            node = node.getParent();
        }
        Collections.reverse(path);
        return path;
    }

    // Suma de las fichas que se movieron en todo el camino
    public static int pathCost(List<String> path) {
        int total = 0;
        for (int i = 1; i < path.size(); i++) {
            String antes = path.get(i - 1);
            String despues = path.get(i);
            int posFicha = despues.indexOf(" ");
            total += antes.charAt(posFicha) - '0';
        }
        return total;
    }

    public static String formatState(String state) {
        String formattedState = "";
        for (int i = 0; i < state.length(); i++) {
            formattedState += state.charAt(i) + " ";
            if ((i + 1) % 3 == 0) {
                formattedState += "\n";
            }
        }
        return formattedState;
    }
}
