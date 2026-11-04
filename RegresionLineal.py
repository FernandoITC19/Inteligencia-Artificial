# Tarea 4 - Regresion lineal "from scratch" con California Housing
#
# Idea: queremos predecir el precio de una casa a partir del ingreso de su zona.
# Buscamos una recta   Y = w * X + b   que se ajuste lo mejor posible a los datos.
#   X = ingreso mediano de la zona (MedInc)
#   Y = precio mediano de las casas (MedHouseVal, en cientos de miles de dolares)
#   w = pendiente  (cuanto sube el precio por cada unidad de ingreso)
#   b = ordenada   (el precio cuando el ingreso es 0)
# w y b los va aprendiendo el modelo con descenso de gradiente.

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import fetch_california_housing

# ------------------------------------------------------------
# 1. DATOS
# ------------------------------------------------------------
datos = fetch_california_housing(as_frame=True)
tabla = datos.frame

print("Primeras filas:")
print(tabla.head())
print("Filas y columnas:", tabla.shape)
print()

X = tabla["MedInc"].values
Y = tabla["MedHouseVal"].values
n = len(X)

# ------------------------------------------------------------
# 2. PARAMETROS DEL MODELO
# ------------------------------------------------------------
w = 0.0                    # pendiente, empieza en 0
b = 0.0                    # ordenada, empieza en 0
tasa_aprendizaje = 0.01    # que tan grandes son los pasos que da el modelo al aprender
epochs = 3000              # cuantas veces repasa todos los datos
historial_costos = []      # aqui guardamos el error de cada epoca para graficarlo

# ------------------------------------------------------------
# 3. ENTRENAMIENTO (descenso de gradiente)
# En cada epoca:
#   a) predecimos con la recta actual:   Y_pred = w * X + b
#   b) medimos el error (MSE):           promedio de (Y_pred - Y) al cuadrado
#   c) calculamos hacia donde mover w y b para bajar el error (gradientes)
#   d) movemos w y b un pasito en esa direccion
# ------------------------------------------------------------
for epoca in range(epochs):
    Y_pred = w * X + b
    error = Y_pred - Y

    costo = np.mean(error ** 2)
    historial_costos.append(costo)

    gradiente_w = (2 / n) * np.sum(error * X)
    gradiente_b = (2 / n) * np.sum(error)

    w = w - tasa_aprendizaje * gradiente_w
    b = b - tasa_aprendizaje * gradiente_b

    if epoca % 500 == 0:
        print("Epoca", epoca, "- costo (MSE):", round(costo, 4))

print()
print("Resultado del modelo: Y =", round(w, 4), "* X +", round(b, 4))
print("Costo final (MSE):", round(historial_costos[-1], 4))
print("Por cada unidad que sube el ingreso, el precio sube", round(w, 3), "unidades")

# Comprobacion: np.polyfit calcula la recta exacta. Debe salir casi igual.
w_exacta, b_exacta = np.polyfit(X, Y, 1)
print("Recta exacta (polyfit): Y =", round(w_exacta, 4), "* X +", round(b_exacta, 4))

# Que tan bien explica el modelo los precios (R2)
Y_pred = w * X + b
r2 = 1 - np.sum((Y - Y_pred) ** 2) / np.sum((Y - np.mean(Y)) ** 2)
print("R2:", round(r2, 4), "-> explica el", round(r2 * 100, 1), "% de las variaciones del precio")

# Ejemplo de prediccion
ingreso_ejemplo = 5.0
print("Si el ingreso es", ingreso_ejemplo, "el precio predicho es", round(w * ingreso_ejemplo + b, 3),
      "(en cientos de miles de dolares)")

# ------------------------------------------------------------
# 4. VISUALIZACION DE RESULTADOS
# ------------------------------------------------------------
plt.figure(figsize=(10, 6))

# Puntos reales (para que no se vea muy saturado dibujamos solo 2000 casas)
muestra = np.random.default_rng(0).choice(n, size=2000, replace=False)
plt.scatter(X[muestra], Y[muestra], color='royalblue', s=15, alpha=0.5, label='Datos Reales (Casas)', zorder=5)

# Linea aprendida por el modelo
X_linea = np.linspace(min(X) - 1, max(X) + 1, 100)
Y_linea = w * X_linea + b
plt.plot(X_linea, Y_linea, color='crimson', linewidth=3, label=f'Modelo Lineal: Y = {w:.2f}X + {b:.2f}')

plt.title('Regresion Lineal From Scratch: Ingreso de la Zona vs Precio de la Casa', fontsize=12, fontweight='bold', pad=15)
plt.xlabel('Ingreso Mediano de la Zona (MedInc)', fontsize=11)
plt.ylabel('Precio Mediano de la Casa (MedHouseVal)', fontsize=11)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# Evolucion del error durante el entrenamiento
plt.figure(figsize=(8, 4))
plt.plot(range(epochs), historial_costos, color='darkorange', linewidth=2)
plt.title('Evolucion de la Funcion de Costo (Error Cuadratico Medio)', fontsize=11, fontweight='bold')
plt.xlabel('Epocas / Iteraciones', fontsize=10)
plt.ylabel('Costo (MSE)', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()