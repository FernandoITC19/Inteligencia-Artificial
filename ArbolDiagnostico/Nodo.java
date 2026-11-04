package diagnostico;
//-	Rivas Uriarte Fernando Noé – 23170303 – IA – 18:00-19:00 - 

public class Nodo {

    String nombre;
    Nodo izquierdo;
    Nodo derecho;

    public Nodo(String nombre) {
        this.nombre = nombre;
        izquierdo = null;
        derecho = null;
    }
}
