package puzzle8;
//-	Rivas Uriarte Fernando Noé – 23170303 – IA – 18:00-19:00 - 

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Queue;
import java.util.Set;

public class PuzzleTree {

    private String goalState;
    private Node root;

    // Datos de la ultima busqueda
    private int expanded;
    private int generated;
    private List<String> path;

    public PuzzleTree(String initialState, String goalState) {
        this.goalState = goalState;
        this.root = new Node(initialState, null);
    }

    public int getExpanded() {
        return expanded;
    }

    public int getGenerated() {
        return generated;
    }

    public List<String> getPath() {
        return path;
    }

    private void reset() {
        expanded = 0;
        generated = 1;
        path = null;
    }

    // 1. Anchura (cola)
    public boolean breadthFirstSearch() {
        reset();
        Set<String> visited = new HashSet<>();
        Queue<Node> queue = new LinkedList<>();

        visited.add(root.getState());
        queue.add(root);

        while (!queue.isEmpty()) {
            Node currentNode = queue.poll();
            expanded++;

            if (currentNode.getState().equals(goalState)) {
                path = NodeUtils.pathTo(currentNode);
                return true;
            }

            for (Node child : NodeUtils.generateChildren(currentNode)) {
                if (!visited.contains(child.getState())) {
                    visited.add(child.getState());
                    generated++;
                    queue.add(child);
                }
            }
        }
        return false;
    }

    // 2. Profundidad (pila)
    public boolean depthFirstSearch() {
        reset();
        Set<String> visited = new HashSet<>();
        Deque<Node> stack = new ArrayDeque<>();

        visited.add(root.getState());
        stack.push(root);

        while (!stack.isEmpty()) {
            Node currentNode = stack.pop();
            expanded++;

            if (currentNode.getState().equals(goalState)) {
                path = NodeUtils.pathTo(currentNode);
                return true;
            }

            for (Node child : NodeUtils.generateChildren(currentNode)) {
                if (!visited.contains(child.getState())) {
                    visited.add(child.getState());
                    generated++;
                    stack.push(child);
                }
            }
        }
        return false;
    }

    // 3. Costo uniforme (cola de prioridad)
    public boolean uniformCostSearch() {
        reset();
        PriorityQueue<Node> queue = new PriorityQueue<>(new NodePriorityComparator());
        Map<String, Integer> bestCost = new HashMap<>();

        bestCost.put(root.getState(), 0);
        queue.add(root);

        while (!queue.isEmpty()) {
            Node currentNode = queue.poll();

            // si ya habia llegado a este estado con menos costo, se ignora
            if (currentNode.getCost() > bestCost.get(currentNode.getState())) {
                continue;
            }
            expanded++;

            if (currentNode.getState().equals(goalState)) {
                path = NodeUtils.pathTo(currentNode);
                return true;
            }

            for (Node child : NodeUtils.generateChildren(currentNode)) {
                Integer old = bestCost.get(child.getState());
                if (old == null || child.getCost() < old) {
                    bestCost.put(child.getState(), child.getCost());
                    generated++;
                    queue.add(child);
                }
            }
        }
        return false;
    }

    // 4. Profundidad iterativa (profundidad limitada con limite que va subiendo)
    public boolean iterativeDeepeningSearch(int maxDepth) {
        reset();
        for (int limit = 0; limit <= maxDepth; limit++) {
            Node goal = depthLimited(root, limit);
            if (goal != null) {
                path = NodeUtils.pathTo(goal);
                return true;
            }
        }
        return false;
    }

    // Profundidad limitada: no baja mas de "limit" niveles
    private Node depthLimited(Node node, int limit) {
        expanded++;
        if (node.getState().equals(goalState)) {
            return node;
        }
        if (limit == 0) {
            return null;
        }
        for (Node child : NodeUtils.generateChildren(node)) {
            generated++;
            if (!estaEnCamino(node, child.getState())) {
                Node found = depthLimited(child, limit - 1);
                if (found != null) {
                    return found;
                }
            }
        }
        return null;
    }

    // Revisa si el estado ya aparece entre los ancestros (para no dar vueltas en circulo)
    private boolean estaEnCamino(Node node, String state) {
        while (node != null) {
            if (node.getState().equals(state)) {
                return true;
            }
            node = node.getParent();
        }
        return false;
    }
}