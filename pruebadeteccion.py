import cv2
from keras.preprocessing import image
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np
import time
import matplotlib.pyplot as plt
import os

def deteccion_en_vivo():
    # Cargar el modelo y pesos previamente entrenados
    modelo = load_model("cnn.h5")
    pesos = "cnn_pesos.h5"
    modelo.load_weights(pesos)

    # Iniciar la captura de video desde la cámara
    cap = cv2.VideoCapture(0)

    # Inicializar variables de tiempo para cada postura
    tiempo_buena = 0
    tiempo_mala = 0
    tiempo_regular = 0

    while True:
        inicio_frame = time.time()  # Tiempo de inicio del frame

        ret, frame = cap.read()

        # Ajustar el tamaño de la imagen según los requisitos del modelo
        img = cv2.resize(frame, (50, 50))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalizar la imagen

        # Realizar la predicción
        predictions = modelo.predict(img_array)
        pred = np.argmax(predictions)

        if pred == 0:
            label = "Buena"
            tiempo_buena += time.time() - inicio_frame
        elif pred == 1:
            label = "Mala"
            tiempo_mala += time.time() - inicio_frame
        elif pred == 2:
            label = "Regular"
            tiempo_regular += time.time() - inicio_frame
        # else:
        #     label = "Desconocida"

        # Mostrar el resultado en la ventana de la cámara
        if label == "Buena":
            cv2.putText(frame, f'Posture: {label} - Tiempo: {tiempo_buena:.2f}s', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif label == "Mala":
            cv2.putText(frame, f'Posture: {label} - Tiempo: {tiempo_mala:.2f}s', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif label == "Regular":
            cv2.putText(frame, f'Posture: {label} - Tiempo: {tiempo_regular:.2f}s', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        # else:
        #     cv2.putText(frame, f'Posture: {label}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (128, 128, 128), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
       

    # Mostrar el tiempo total de cada postura al final
    print(f'Tiempo total Buena: {tiempo_buena:.2f}s')
    print(f'Tiempo total Mala: {tiempo_mala:.2f}s')
    print(f'Tiempo total Regular: {tiempo_regular:.2f}s')

    # Liberar la captura de video y cerrar la ventana
    cap.release()
    cv2.destroyAllWindows()

    return tiempo_buena, tiempo_regular, tiempo_mala

if __name__ == '__main__':
    # Ejecutar la función
    deteccion_en_vivo()
