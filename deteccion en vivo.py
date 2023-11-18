import cv2
import numpy as np
from keras.models import load_model
#from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow
from keras.applications.mobilenet_v2 import preprocess_input
import os

# Cargar el modelo y pesos previamente entrenados
modelo = os.path.join(os.path.dirname(__file__), "cnn.h5")
pesos = os.path.join(os.path.dirname(__file__), "cnn_pesos.h5")

cnn = load_model(modelo)
cnn.load_weights(pesos)

# Crear un objeto de captura de video desde la cámara (0 representa la cámara predeterminada)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()  # Capturar un cuadro de video
    if not ret:
        break

    # Preprocesar el cuadro de video (ajustar tamaño, normalizar, etc.)
    frame = cv2.resize(frame, (50, 50))  # Ajustar al tamaño de entrada de tu modelo
    #frame = tensorflow.keras.utils.img_to_array(frame)
    frame = np.expand_dims(frame, axis=0)
    frame = preprocess_input(frame)

    # Realizar la predicción utilizando el modelo
    prediction = cnn.predict(frame)

    # Determinar la clase predicha
    arg_max = np.argmax(prediction[0])
    if arg_max == 0:
        label = "Buena"
    elif arg_max == 1:
        label = "Mala"
    elif arg_max == 2:
        label = "Regular"
    else: 
        label = "Desconocida"

    # Mostrar el resultado en el cuadro de video
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('DetecciOn en Vivo', frame)

    # Romper el bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura de video y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
