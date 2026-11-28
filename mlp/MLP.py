# Practica - Perceptron multicapa (MLP) con MNIST
# Red densa que clasifica digitos escritos a mano (0 al 9).

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Flatten, Dense

# ------------------------------------------------------------
# 1. DATOS
# ------------------------------------------------------------
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Normalizamos los pixeles de 0-255 a 0-1
gray_scale = 255
x_train = x_train.astype('float32') / gray_scale
x_test = x_test.astype('float32') / gray_scale

print("Feature matrix (x_train):", x_train.shape)
print("Target matrix (y_train):", y_train.shape)
print("Feature matrix (x_test):", x_test.shape)
print("Target matrix (y_test):", y_test.shape)

# Mostramos las primeras 100 imagenes del conjunto de entrenamiento
fig, ax = plt.subplots(10, 10)
k = 0
for i in range(10):
    for j in range(10):
        ax[i][j].imshow(x_train[k].reshape(28, 28), aspect='auto')
        ax[i][j].axis('off')
        k += 1
plt.show()

# ------------------------------------------------------------
# 2. MODELO
# ------------------------------------------------------------
# Flatten: convierte la imagen 28x28 en un vector de 784 valores
# Dense(256) y Dense(128): capas ocultas con activacion sigmoide
# Dense(10): una salida por digito, con softmax (probabilidades)
model = Sequential([
    Input(shape=(28, 28)),
    Flatten(),
    Dense(256, activation='sigmoid'),
    Dense(128, activation='sigmoid'),
    Dense(10, activation='softmax'),
])

model.summary()

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# ------------------------------------------------------------
# 3. ENTRENAMIENTO
# ------------------------------------------------------------
mod = model.fit(x_train, y_train,
                epochs=10,
                batch_size=2000,
                validation_split=0.2)

# ------------------------------------------------------------
# 4. EVALUACION
# ------------------------------------------------------------
results = model.evaluate(x_test, y_test, verbose=0)
print('Test loss, Test accuracy:', results)

# ------------------------------------------------------------
# 5. GRAFICAS DE ENTRENAMIENTO
# ------------------------------------------------------------
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(mod.history['accuracy'], label='Training Accuracy', color='blue')
plt.plot(mod.history['val_accuracy'], label='Validation Accuracy', color='orange')
plt.title('Training and Validation Accuracy', fontsize=14)
plt.xlabel('Epochs', fontsize=12)
plt.ylabel('Accuracy', fontsize=12)
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(mod.history['loss'], label='Training Loss', color='blue')
plt.plot(mod.history['val_loss'], label='Validation Loss', color='orange')
plt.title('Training and Validation Loss', fontsize=14)
plt.xlabel('Epochs', fontsize=12)
plt.ylabel('Loss', fontsize=12)
plt.legend()
plt.grid(True)

plt.suptitle("Model Training Performance", fontsize=16)
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 6. PRUEBA CON ALGUNAS IMAGENES DEL TEST
# ------------------------------------------------------------
predicciones = model.predict(x_test[:10], verbose=0)
for i in range(10):
    print(f"Imagen {i}: real = {y_test[i]}, prediccion = {np.argmax(predicciones[i])}")