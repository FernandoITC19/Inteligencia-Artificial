package diagnostico;
//-	Rivas Uriarte Fernando Noé – 23170303 – IA – 18:00-19:00 - 

public class Main {

    public static void main(String[] args) {

        Arbol arbol = new Arbol();

        System.out.println("Esta vacio? " + arbol.vacio());

        arbol.insertar("Maria");
        arbol.insertar("Juan");
        arbol.insertar("Pedro");
        arbol.insertar("Ana");
        arbol.insertar("Luis");

        System.out.println("Esta vacio? " + arbol.vacio());

        Nodo encontrado = arbol.buscarNodo("Luis");
        if (encontrado != null) {
            System.out.println("Encontre a: " + encontrado.nombre);
        } else {
            System.out.println("No se encontro");
        }

        Nodo otro = arbol.buscarNodo("Carlos");
        if (otro != null) {
            System.out.println("Encontre a: " + otro.nombre);
        } else {
            System.out.println("Carlos no esta en el arbol");
        }
    }
}