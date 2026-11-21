import os
import tkinter as tk

import numpy as np
import tensorflow as tf
from PIL import Image, ImageDraw

ARCHIVO_MODELO = "modelo_digitos.keras"
TAM_LIENZO = 280
GROSOR_TRAZO = 18


def construir_modelo():
    modelo = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(28, 28, 1)),
        tf.keras.layers.Conv2D(16, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.25),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(10, activation="softmax"),
    ])
    modelo.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return modelo


def obtener_modelo():
    if os.path.exists(ARCHIVO_MODELO):
        return tf.keras.models.load_model(ARCHIVO_MODELO)

    (x_ent, y_ent), (x_prueba, y_prueba) = tf.keras.datasets.mnist.load_data()
    x_ent = x_ent.astype("float32")[..., np.newaxis] / 255.0
    x_prueba = x_prueba.astype("float32")[..., np.newaxis] / 255.0

    modelo = construir_modelo()
    modelo.fit(x_ent, y_ent, epochs=6, batch_size=64, validation_split=0.1)
    perdida, precision = modelo.evaluate(x_prueba, y_prueba, verbose=0)
    print(f"Precisión en datos de prueba: {precision:.4f}")
    modelo.save(ARCHIVO_MODELO)
    return modelo


def preparar_dibujo(imagen):
    datos = np.array(imagen)
    filas, columnas = np.where(datos > 30)
    if len(filas) == 0:
        return None
    recorte = datos[filas.min():filas.max() + 1, columnas.min():columnas.max() + 1]
    alto, ancho = recorte.shape
    factor = 20 / max(alto, ancho)
    nuevo_ancho = max(1, round(ancho * factor))
    nuevo_alto = max(1, round(alto * factor))
    digito = Image.fromarray(recorte).resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

    lienzo = Image.new("L", (28, 28), 0)
    x = (28 - nuevo_ancho) // 2
    y = (28 - nuevo_alto) // 2
    lienzo.paste(digito, (x, y))
    entrada = np.array(lienzo, dtype="float32") / 255.0
    return entrada.reshape(1, 28, 28, 1)


class AppDibujo:
    def __init__(self, ventana, modelo):
        self.modelo = modelo
        self.imagen = Image.new("L", (TAM_LIENZO, TAM_LIENZO), 0)
        self.pincel = ImageDraw.Draw(self.imagen)
        self.ultimo = None

        ventana.title("Clasificador de dígitos")
        self.lienzo = tk.Canvas(ventana, width=TAM_LIENZO, height=TAM_LIENZO,
                                bg="black", cursor="cross")
        self.lienzo.pack(padx=10, pady=10)
        self.lienzo.bind("<B1-Motion>", self.dibujar)
        self.lienzo.bind("<ButtonRelease-1>", self.soltar)

        botones = tk.Frame(ventana)
        botones.pack()
        tk.Button(botones, text="Predecir", command=self.predecir).pack(side="left", padx=5)
        tk.Button(botones, text="Borrar", command=self.borrar).pack(side="left", padx=5)

        self.resultado = tk.Label(ventana, text="Dibuja un número del 0 al 9",
                                  font=("Arial", 14))
        self.resultado.pack(pady=10)

    def dibujar(self, evento):
        if self.ultimo is not None:
            x0, y0 = self.ultimo
            self.lienzo.create_line(
                x0, y0, evento.x, evento.y,
                fill="white", width=GROSOR_TRAZO, capstyle="round",
            )
            self.pincel.line([x0, y0, evento.x, evento.y], fill=255, width=GROSOR_TRAZO)
        self.ultimo = (evento.x, evento.y)

    def soltar(self, evento):
        self.ultimo = None

    def predecir(self):
        entrada = preparar_dibujo(self.imagen)
        if entrada is None:
            self.resultado.config(text="El lienzo está vacío")
            return
        probabilidades = self.modelo.predict(entrada, verbose=0)[0]
        digito = int(np.argmax(probabilidades))
        confianza = probabilidades[digito] * 100
        self.resultado.config(text=f"Predicción: {digito}  ({confianza:.1f}%)")

    def borrar(self):
        self.lienzo.delete("all")
        self.pincel.rectangle([0, 0, TAM_LIENZO, TAM_LIENZO], fill=0)
        self.resultado.config(text="Dibuja un número del 0 al 9")


def main():
    modelo = obtener_modelo()
    ventana = tk.Tk()
    AppDibujo(ventana, modelo)
    ventana.mainloop()


if __name__ == "__main__":
    main()