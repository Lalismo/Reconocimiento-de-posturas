import cv2
import time
import numpy as np
from keras.models import load_model


# Cargar el modelo entrenado

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


# Función para realizar la detección de posturas en un frame de la cámara
def detect_posture():
# Inicializar variables de tiempo para cada postura
    buena = 0
    mala = 0
    regular = 0


    model = load_model('cnn.h5')
    model.load_weights('cnn_pesos.h5')

    

    # Iniciar la captura de video desde la cámara
    cap = cv2.VideoCapture(0)


    while True:

        inicio_frame = time.time()  # Tiempo de inicio del frame
        

        # Leer un frame de la cámara
        ret, frame = cap.read()

        
        # Redimensionar el frame para que coincida con el tamaño de entrada del modelo
        image = cv2.resize(frame, (50, 50))
        # Agregar una dimensión adicional para representar el lote de imágenes
        image = np.expand_dims(image, axis=0)
        # Normalizar los valores de píxeles
        image = image / 255.0
    
        if not ret:
            break
        
        # Realizar la detección de posturas en el frame actual
      
        
        # Realizar la predicción utilizando el modelo cargado
        predictions = model.predict(image)
        # Obtener la clase con la probabilidad más alta
        predicted_class = np.argmax(predictions)
        # Mapear el índice de clase predicho a la etiqueta de clase correspondiente
        if predicted_class == 0:
            posture = "Good Posture"
            buena += time.time() - inicio_frame

        elif predicted_class == 1:
            posture = "Regular Posture"
            regular += time.time() - inicio_frame

        else:
            posture = "Bad Posture"
            mala += time.time() - inicio_frame

        # Mostrar la postura predicha en el frame
        if posture=="Good Posture":
            cv2.putText(frame, f'{posture} - tiempo {buena:.2f}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif posture=="Bad Posture":
            cv2.putText(frame, f'{posture} - tiempo {mala:.2f}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif posture=="Regular Posture":
            cv2.putText(frame, f'{posture}  tiempo {regular:.2f}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

  
        tiempo.cambiar_tiempos(buena, regular, mala)
        
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Liberar la captura de video y cerrar todas las ventanas
    cap.release()
    cv2.destroyAllWindows()

        # Devolver la postura predicha
    return buena,mala,regular

