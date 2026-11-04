package diagnostico;
//-	Rivas Uriarte Fernando Noé – 23170303 – IA – 18:00-19:00 - 

public class Arbol {

    Nodo raiz;

    public Arbol() {
        raiz = null;
    }

    public boolean vacio() {
        return raiz == null;
    }

    public void insertar(String nombre) {
        Nodo nuevo = new Nodo(nombre);

        if (vacio()) {
            raiz = nuevo;
            return;
        }

        Nodo actual = raiz;
        while (true) {
            if (nombre.compareTo(actual.nombre) < 0) {
                if (actual.izquierdo == null) {
                    actual.izquierdo = nuevo;
                    return;
                }
                actual = actual.izquierdo;
            } else {
                if (actual.derecho == null) {
                    actual.derecho = nuevo;
                    return;
                }
                actual = actual.derecho;
            }
        }
    }

    // Busca un nodo por su nombre. Si no lo encuentra regresa null
    public Nodo buscarNodo(String nombre) {
        Nodo actual = raiz;

        while (actual != null) {
            if (nombre.equals(actual.nombre)) {
                return actual;
            }
            if (nombre.compareTo(actual.nombre) < 0) {
                actual = actual.izquierdo;
            } else {
                actual = actual.derecho;
            }
        }
        return null;
    }
}