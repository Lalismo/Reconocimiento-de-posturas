# Esta es mi primera red neuronal convolucional

# Importar los métodos necesarios
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
import numpy as np
from keras.utils import load_img, img_to_array
from keras.models import load_model
import tensorflow as tf
import os
import time
import scipy


train_path = os.path.join(os.path.dirname(__file__), 'app\static\DataGray\Training')
val_path = os.path.join(os.path.dirname(__file__), 'app\static\DataGray\Validation')

def entrenamiento():
    current_time = time.time()

    # Rutas para las imágenes de entrenamiento y prueba
    train = os.path.join(os.path.dirname(__file__), 'app\static\DataGray\Training')
    val = os.path.join(os.path.dirname(__file__), 'app\static\DataGray\Validation')

    # Definir los hiperparámetros
    epocas = 50
    altura, anchura = 50, 50
    batch_size = 2
    pasos = 100
    # Son hiperparámetros para la convolución
    # Primera convolución
    kernels_capa1 = 32
    size_kernels1 = (3, 3)
    # Primera Convolución:
    kernels_capa2 = 64
    size_kernels2 = (3, 3)
    pooling_size = (2, 2)
    # Clases
    clases = 3
    learning_rate = 0.001

    # Definir los datos sintéticos y la lectura de las imágenes
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'cnnGray.h5')) and not os.path.exists(
            os.path.join(os.path.dirname(__file__), 'cnn_pesosGray.h5')):

        entrenar = ImageDataGenerator(rescale=1 / 250, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        validar = ImageDataGenerator(rescale=1 / 250)

        datos_entrenamiento = entrenar.flow_from_directory(train, target_size=(altura, anchura),
                                                           batch_size=batch_size, class_mode="categorical",
                                                           classes=['Good_Posture', 'Bad_Posture', 'Regular_Posture'])
        datos_validacion = validar.flow_from_directory(val, target_size=(altura, anchura), batch_size=batch_size,
                                                       class_mode="categorical",
                                                       classes=['Good_Posture', 'Bad_Posture', 'Regular_Posture'])

        # Construir la arquitectura de la red neuronal convolucional
        cnn = Sequential()

        # Definir la primera capa convolucional
        cnn.add(Convolution2D(kernels_capa1, size_kernels1, padding="same", input_shape=(altura, anchura, 3),
                              activation="relu"))

        # Pooling
        cnn.add(MaxPooling2D(pool_size=pooling_size))

        # Definir la 2 capa convolucional
        cnn.add(Convolution2D(kernels_capa2, size_kernels2, padding="same", activation="relu"))

        # Pooling
        cnn.add(MaxPooling2D(pool_size=pooling_size))

        # Aplanado de las matrices o tensores 2D
        cnn.add(tf.keras.layers.Flatten())

        # Conectar los datos con una MLP o perceptrón multicapa
        # 256 se refiere a las neuronas
        cnn.add(tf.keras.layers.Dense(256, activation="relu"))
        cnn.add(tf.keras.layers.Dense(256, activation="relu"))

        # Sirve para el sobreentrenamiento
        cnn.add(tf.keras.layers.Dropout(0.5))  # Porcentaje para apagar las neuronas sobre la capa oculta

        # Clases = 4
        cnn.add(tf.keras.layers.Dense(clases, activation="softmax"))

        # Definir los parámetros del entrenamiento
        cnn.compile(loss='categorical_crossentropy', optimizer="adam", metrics=["acc", "mse"])

        # Entrenar red neuronal convolucional
        cnn.fit(datos_entrenamiento, validation_data=datos_validacion, epochs=epocas, validation_steps=pasos, verbose=1)

        # Guardar el modelo y los pesos de entrenamiento
        cnn.save(os.path.join(os.path.dirname(__file__), "cnnGray.h5"))
        cnn.save_weights(os.path.join(os.path.dirname(__file__), "cnn_pesosGray.h5"))

        # Elegir la imagen a clasificar
        imagen = os.path.join(val, 'Good_Posture', 'good_1.jpg')

        altura, anchura = 50, 50
        modelo = os.path.join(os.path.dirname(__file__), "cnnGray.h5")
        pesos = os.path.join(os.path.dirname(__file__), "cnn_pesosGray.h5")

        # Cargar el modelo y pesos
        cnn = load_model(modelo)
        cnn.load_weights(pesos)

        # Preparar imagen a clasificar
        img_clasificar = load_img(imagen, target_size=(altura, anchura))
        img_clasificar = img_to_array(img_clasificar)
        img_clasificar = np.expand_dims(img_clasificar, axis=0)

        # Clasificamos la imagen
        clase = cnn.predict(img_clasificar)

        print(clase)

        arg_max = np.argmax(clase[0])

        if arg_max == 0:
            print("Good posture")
        elif arg_max == 1:
            print("Bad posture")
        elif arg_max == 2:
            print("Regular posture")
        else:
            print("Empty")

        return time.time() - current_time

    else:

        # Elegir la imagen a clasificar
        imagen = os.path.join(val, 'Regular_Posture', 'regular_1.jpg')

        altura, anchura = 50, 50
        modelo = os.path.join(os.path.dirname(__file__), "cnnGray.h5")
        pesos = os.path.join(os.path.dirname(__file__), "cnn_pesosGray.h5")

        # Cargar el modelo y pesos
        cnn = load_model(modelo)
        cnn.load_weights(pesos)

        # Preparar imagen a clasificar
        img_clasificar = load_img(imagen, target_size=(altura, anchura))
        img_clasificar = img_to_array(img_clasificar)
        img_clasificar = np.expand_dims(img_clasificar, axis=0)

        # Clasificamos la imagen
        clase = cnn.predict(img_clasificar)

        print(clase)

        arg_max = np.argmax(clase[0])

        if arg_max == 0:
            print("Good posture")
        elif arg_max == 1:
            print("Regular posture")
        elif arg_max == 2:
            print("Bad posture")
        else:
            print("NADA")

        return time.time() - current_time

entrenamiento()
