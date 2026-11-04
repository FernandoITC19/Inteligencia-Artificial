package puzzle8;
//-	Rivas Uriarte Fernando Noé – 23170303 – IA – 18:00-19:00 - 
public class Node {

    private String state;
    private Node parent;
    private int depth;
    private int cost;

    public Node(String state, Node parent) {
        this.state = state;
        this.parent = parent;
        if (parent == null) {
            depth = 0;
        } else {
            depth = parent.getDepth() + 1;
        }
        cost = 0;
    }

    public String getState() {
        return state;
    }

    public Node getParent() {
        return parent;
    }

    public int getDepth() {
        return depth;
    }

    public int getCost() {
        return cost;
    }

    public void setCost(int cost) {
        this.cost = cost;
    }
}
