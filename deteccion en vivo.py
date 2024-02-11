import cv2
from keras.preprocessing import image
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np

# Cargar el modelo y pesos previamente entrenados
modelo = load_model("cnn.h5")
pesos = "cnn_pesos.h5"
modelo.load_weights(pesos)

# Iniciar la captura de video desde la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Ajustar el tamaño de la imagen según los requisitos del modelo
    img = cv2.resize(frame, (50, 50))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalizar la imagen

    # Realizar la predicción
    predictions = modelo.predict(img_array)
    pred = np.argmax(predictions)
    print(pred)    
    if pred == 0:
        label = "Buena"
    elif pred == 1:
        label = "Mala"
    elif pred == 2:
        label = "Regular"
    else:
        label = "Desconocida"

    # Mostrar el resultado en la ventana de la cámara
    if (label == "Buena"):
        cv2.putText(frame, f'Posture: {label}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    elif (label == "Mala"):
        cv2.putText(frame, f'Posture: {label}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    elif (label == "Regular"):
        cv2.putText(frame, f'Posture: {label}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    else:
        cv2.putText(frame, f'Posture: {label}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (128, 128, 128), 2)
        
    cv2.imshow('Posture Detection', frame)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura de video y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
