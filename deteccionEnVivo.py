import cv2
from keras.preprocessing import image
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np
import time
import os
from capturaPosturas import findAngle
import mediapipe as mp


class Tiempos():
    def  __init__(self, bueno=0, regular=0, malo=0):
        self.bueno = bueno
        self.regular = regular
        self.malo = malo
    
    def get_times(self):
        return self.bueno, self.regular, self.malo
    
    def cambiar_tiempos(self, bueno, regular, malo):
        self.bueno = bueno
        self.regular = regular
        self.malo = malo

tiempo = Tiempos()

def deteccion_en_vivo() :
    
    # API para reconocimiento de pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # Colors.
    red = (50, 50, 255)
    green = (127, 255, 0)
    yellow = (0, 255, 255)
    gray = (130, 130, 130)
    
    # Cargar el modelo y pesos previamente entrenados
    modelo = load_model("cnnAND.h5")
    pesos = "cnn_pesosAND.h5"
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
        
        # Font type.
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalizar la imagen

        h, w, _ = frame.shape
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        keypoints = pose.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        lm = keypoints.pose_landmarks
        lmPose = mp_pose.PoseLandmark
        
        if lm:
            l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
            l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
            l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
            l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)
            l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
            l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)

            cv2.circle(frame, (l_shldr_x, l_shldr_y), 7, yellow, -1)
            cv2.circle(frame, (l_ear_x, l_ear_y), 7, yellow, -1)
            # cv2.circle(frame, (l_shldr_x, l_shldr_y - 100), 7, yellow, -1)
            cv2.circle(frame, (l_hip_x, l_hip_y), 7, yellow, -1)
            cv2.circle(frame, (l_hip_x, l_hip_y - 100), 7, yellow, -1)

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
            #else:
            #    label = "Desconocida"

            # Mostrar el resultado en la ventana de la cámara
            if label == "Buena":
                cv2.putText(frame, f'Posture: {label} - Tiempo: {tiempo_buena:.2f}s', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.line(frame, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 4)
                # cv2.line(frame, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 4)
                cv2.line(frame, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 4)
                cv2.line(frame, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 4)

            elif label == "Mala":
                cv2.putText(frame, f'Posture: {label} - Tiempo: {tiempo_mala:.2f}s', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.line(frame, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 4)
                # cv2.line(frame, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 4)
                cv2.line(frame, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 4)
                cv2.line(frame, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 4)

            elif label == "Regular":
                cv2.putText(frame, f'Posture: {label} - Tiempo: {tiempo_regular:.2f}s', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                cv2.line(frame, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), yellow, 4)
                # cv2.line(frame, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), yellow, 4)
                cv2.line(frame, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), yellow, 4)
                cv2.line(frame, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), yellow, 4)
            else:
                cv2.putText(frame, f'Posture: {label}', (10, 30), font, 1, gray, 2)
                cv2.line(frame, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), gray, 4)
                # cv2.line(frame, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), gray, 4)
                cv2.line(frame, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), gray, 4)
                cv2.line(frame, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), gray, 4)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            tiempo.cambiar_tiempos(tiempo_buena, tiempo_regular, tiempo_mala)
            
            #buena, regular, mala = tiempo.get_times()
        
            #print(buena, regular, mala)
            
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        # Salir del bucle si se presiona la tecla 'q'
        

    # Mostrar el tiempo total de cada postura al final
    print(f'Tiempo total Buena: {tiempo_buena:.2f}s')
    print(f'Tiempo total Mala: {tiempo_mala:.2f}s')
    print(f'Tiempo total Regular: {tiempo_regular:.2f}s')

    # Liberar la captura de video y cerrar la ventana
    cap.release()
    cv2.destroyAllWindows()

    return tiempo_buena, tiempo_regular, tiempo_mala



if __name__ == '__main__': 

    # Obtener generador para la detección en vivo de posturas
    resultados_generador = deteccion_en_vivo()

  