# Esta es mi primera red neuronal convolucional

# Importar los métodos necesarios
from keras.metrics import CategoricalAccuracy
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
import numpy as np
from keras.utils import load_img, img_to_array
from keras.models import load_model, Model
import tensorflow as tf
import os
import time
import multiprocessing
import matplotlib
from matplotlib import pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Image, Table, TableStyle

train_path = os.path.join(os.path.dirname(__file__), 'app\static\DataGray\Training')
val_path = os.path.join(os.path.dirname(__file__), 'app\static\DataGray\Validation')

def exist_model():
    return (os.path.exists(os.path.join(os.path.dirname(__file__),'cnnGray_experimentacion.h5')) and os.path.exists(os.path.join(os.path.dirname(__file__), 'cnnGray_pesos_experimentacion.h5')))

def entrenamiento(epocas, pasos):
  
  inicio = time.time()
  
  # Rutas para las imágenes de entrenamiento y prueba   
  train = os.path.join(os.path.dirname(__file__), 'app\static\DataGray\Training')
  val = os.path.join(os.path.dirname(__file__), 'app\static\DataGray\Validation')

  # Definir los hiperparámetros
  altura, anchura = 50, 50    
  batch_size = 2    
  # Son hiperparámetros para la convolución   
  # Primera convolución   
  kernels_capa1 = 32    
  size_kernels1 = (3, 3)    
  # Segunda Convolución:    
  kernels_capa2 = 64    
  size_kernels2 = (3, 3)    
  pooling_size = (2, 2)   
  # Clases    
  clases = 3    
  learning_rate = 0.001   

  # Definir los datos sintéticos y la lectura de las imágenes
  if not exist_model(): 
    
    entrenar = ImageDataGenerator(rescale=1 / 250, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
    validar = ImageDataGenerator(rescale=1 / 250)
    
    datos_entrenamiento = entrenar.flow_from_directory(train, target_size=(altura,anchura),
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
    cnn.add(Convolution2D(kernels_capa2, size_kernels2, padding="same", activation="relu")    )

    # Pooling   
    cnn.add(MaxPooling2D(pool_size=pooling_size))   

    # Aplanado de las matrices o tensores 2D    
    cnn.add(tf.keras.layers.Flatten())    

    # Conectar los datos con una MLP o perceptrón multicapa   
    # 256 se refiere a las neuronas   
    cnn.add(tf.keras.layers.Dense(256, activation="relu"))    
    #cnn.add(tf.keras.layers.Dense(256, activation="relu"))    

    # Sirve para el sobreentrenamiento    
    cnn.add(tf.keras.layers.Dropout(0.5))  # Porcentaje para apagar las neuronas sobre la capa oculta   

    # Clases = 4    
    cnn.add(tf.keras.layers.Dense(clases, activation="softmax"))    

    # Definir los parámetros del entrenamiento    
    cnn.compile(loss='categorical_crossentropy', optimizer="adam", metrics=[CategoricalAccuracy()])   

    #Entrenar red neuronal convolulcional   
    history = cnn.fit(datos_entrenamiento,validation_data=datos_validacion, epochs=epocas, validation_steps=pasos,verbose=1)

    # Guardar datos de metrica en historial
    # Guarda el historial del entrenamiento
    accuracy = history.history['categorical_accuracy']
    loss = history.history['loss']


    #Guardar el modelo y los pesos de entrenamiento   

    cnn.save(os.path.join(os.path.dirname(__file__), "cnnGray_experimentacion.h5"))    
    cnn.save_weights(os.path.join(os.path.dirname(__file__), "cnnGray_pesos_experimentacion.h5"))
    
    '''////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'''
    #Elegir la imagen a clasificar    
    imagen= os.path.join(val, 'Regular_Posture', 'regular_250.jpg')
       

    altura,anchura=50,50    
    modelo= os.path.join(os.path.dirname(__file__), "cnnGray_experimentacion.h5")   
    pesos= os.path.join(os.path.dirname(__file__), "cnnGray_pesos_experimentacion.h5")


    #Cargar el modelo y pesos   
    cnn=load_model(modelo)    
    cnn.load_weights(pesos)

    #preparar imagen a clasificar
    img_clasificar=load_img(imagen,target_size=(altura,anchura))
    img_clasificar=img_to_array(img_clasificar)
    img_clasificar=np.expand_dims(img_clasificar,axis=0)

    #Clasificamos la imagen   
    clase=cnn.predict(img_clasificar)

    arg_max=np.argmax(clase[0])   

    if arg_max==0:
      print("Good posture")    
    elif arg_max==1:
      print("Regular posture") 
    elif arg_max==2:
      print("Bad posture")
    else:
      print("Empty")
      arg_max=3

    tiempo_final = time.time() - inicio

    print(f'current_time: {tiempo_final}')
    print(f"Accuracy: {accuracy[-1]}")
    print(f'Loss: {loss[-1]}')
    
    return tiempo_final, accuracy[-1], loss[-1], epocas, pasos

  else:

    modelo_experimentacion = os.path.join(os.path.dirname(__file__), 'cnnGray_experimentacion.h5')
    pesos_experimentacion = os.path.join(os.path.dirname(__file__), 'cnnGray_pesos_experimentacion.h5')
    pdf = os.path.join(os.path.dirname(__file__), 'MetricasExperimentacionGray.pdf')

    if (os.path.exists(pdf)):
      os.remove(pdf)
      
    os.remove(modelo_experimentacion)
    os.remove(pesos_experimentacion)
    
    return (entrenamiento(epocas, pasos))

def val_image(val_path):
  ''' Valida la existencia del archivo h5'''
  if (os.path.exists(os.path.join('cnnGray_experimentacion.h5')) and os.path.exists(os.path.join('cnnGray_pesos_experimentacion.h5'))):
    #Elegir la imagen a clasificar    
    imagen= os.path.join(val_path)
    

    altura,anchura=50,50    
    modelo= os.path.join(os.path.dirname(__file__), "cnnGray_experimentacion.h5")
    pesos= os.path.join(os.path.dirname(__file__), "cnnGray_pesos_experimentacion.h5")

    #Cargar el modelo y pesos   
    cnn=load_model(modelo)    
    cnn.load_weights(pesos)

    #preparar imagen a clasificar
    img_clasificar=load_img(imagen,target_size=(altura,anchura))
    img_clasificar=img_to_array(img_clasificar)
    img_clasificar=np.expand_dims(img_clasificar,axis=0)

    #Clasificamos la imagen   
    clase=cnn.predict(img_clasificar)   

    print(clase)    

    arg_max=np.argmax(clase[0])   

    if arg_max==0:
        print("Good posture")    
    elif arg_max==1:
        print("Bad posture") 
    elif arg_max==2:
        print("Regular posture")
    else:
        print("NADA")
        arg_max == 3
    return arg_max
  
def create_pdf (time, accuracy, loss, epochs, pasos):
    
    matplotlib.use('Agg')
    # Crear un objeto BytesIO para almacenar el contenido del PDF
    buffer = BytesIO()

    # Crear un documento PDF con reportlab
    doc = SimpleDocTemplate(buffer, pagesize=letter)
 

    elements= []

    # Generar tabla de tiempos
    data = [
        ["Metricas", "Valores de la experimentacion"],
        ["Pasos", f"{pasos}"],
        ["Epocas", f"{epochs}"],
        ["Time of training", f"{time:.2f}"],
        ["Accuraccy", f"{accuracy:.2f}"],
        ["Categorical Crossentropy", f"{loss:.2f}"]
    ]
    
    tabla = Table(data, colWidths=150, rowHeights=30)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    elements.append(tabla)

    # Generar gráfico
    plt.figure(figsize=(6, 4))
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    plt.plot(x, y)
    plt.title('Gráfico de ejemplo')
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')

    # Guardar el gráfico en un objeto BytesIO
    image_buffer = BytesIO()
    plt.savefig(image_buffer, format='png')
    plt.close()

    # Crear un objeto Image con el contenido del gráfico
    image = Image(image_buffer)
    elements.append(image)

    # Agregar los elementos al documento
    doc.build(elements)

    # Mover el cursor del objeto BytesIO al principio del archivo
    buffer.seek(0)


    # Guardar el contenido del PDF en un archivo
    with open('MetricasExperimentacionGray.pdf', 'wb') as f:
        f.write(buffer.read())


if __name__ == '__main__':
  train_time, val, loss, epochs, steps= entrenamiento(2,2)
  print(train_time, val, loss, epochs, steps)
  create_pdf(train_time, val, loss, epochs, steps)
