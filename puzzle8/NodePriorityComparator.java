package puzzle8;
//-	Rivas Uriarte Fernando Noé – 23170303 – IA – 18:00-19:00 - 

import java.util.Comparator;

public class NodePriorityComparator implements Comparator<Node> {

    @Override
    public int compare(Node a, Node b) {
        return a.getCost() - b.getCost();
    }
}
