import cv2
import os
import math as m
import mediapipe as mp
import time


def findAngle(x1, y1, x2, y2):
    theta = m.acos((x2 - x1) / m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
    degree = m.degrees(theta)
    return degree
'''
accion 1.- Update
category 1.- Good 2.- Regular 3.- Bad
filename: filename path 
'''

def count_files_by_extension(dirname, extension):
    ''' Funcion para obtener el numero de archivos con la misma extension dentro de una carpeta 
    Arguments:
    dirname     -- Path
    extension   -- Extension
    '''
    
    # Obtener la lista de archivos en la carpeta
    files = os.listdir(dirname)

    # Filtrar archivos por la extensión deseada
    files_with_extension = [file for file in files if file.endswith(extension)]

    # Contar la cantidad de archivos con la extensión
    amount_files = len(files_with_extension)

    return amount_files

def count_exist_file(path, type):
    
    ''' Busca y encuentra el nombre del archivo que no existe dentro de la carpeta, retornando el nombre del archivo'''
    '''El rango final es el segundo numero en la funcion range()'''
    # Obtener la lista de archivos en la carpeta
    for number in range(1, 1501):
        if type == 0:
            if not os.path.exists(os.path.join(path,  f'good_{number}.jpg')):
                return f'good_{number}.jpg'
            else:
                return 3
            
        elif type == 2:
            if not os.path.exists(os.path.join(path, f'regular_{number}.jpg')):
                return f'regular_{number}.jpg'
            else:
                return 3
            
        elif type == 1:
            if not os.path.exists(os.path.join(path, f'bad_{number}.jpg')):
                return f'bad_{number}.jpg'
            else:
                return 3
    
def generacion_datagray():
    
    staticPath = os.path.join(os.path.dirname(__file__), 'app\static') #encuentra la ruta Data sin importar el sistema que se este usando al momento de la ejecucion
    dataGray = os.path.join(staticPath,'DataGray')
    data = os.path.join(staticPath,'Data')
    
    # Rutas de la carpeta del dataset RGB
    personpath = os.path.join(data, 'Training')
    valpath = os.path.join(data, 'Validation')
    goodposture = os.path.join(personpath, 'Good_Posture')
    val_good = os.path.join(valpath, 'Good_Posture')
    badposture = os.path.join(personpath, 'Bad_Posture')
    val_bad = os.path.join(valpath, 'Bad_Posture')
    regularposture = os.path.join(personpath, 'Regular_Posture')
    val_regular = os.path.join(valpath, 'Regular_Posture')    

    # Rutas de la carpeta del dataset GRAY
    train_gray = os.path.join(dataGray, 'Training')
    val_gray = os.path.join(dataGray, 'Validation')
    good_posture_gray = os.path.join(train_gray, 'Good_Posture')
    val_good_gray = os.path.join(val_gray, 'Good_Posture')
    bad_posture_gray = os.path.join(train_gray, 'Bad_Posture')
    val_bad_gray = os.path.join(val_gray, 'Bad_Posture')
    regular_posture_gray = os.path.join(train_gray, 'Regular_Posture')
    val_regular_gray = os.path.join(val_gray, 'Regular_Posture')

    if  os.path.exists(train_gray) and os.path.exists(val_gray):
        pass
    else:
        os.makedirs(train_gray)
        os.makedirs(val_gray)
        
        os.makedirs(good_posture_gray)
        os.makedirs(val_good_gray)
        
        os.makedirs(bad_posture_gray)
        os.makedirs(val_bad_gray)
        
        os.makedirs(regular_posture_gray)
        os.makedirs(val_regular_gray)

    rutas = [goodposture, val_good, badposture, val_bad, regularposture, val_regular]
    rutas_gray = [good_posture_gray, val_good_gray, bad_posture_gray, val_bad_gray, regular_posture_gray, val_regular_gray]
    
    for i in range(len(rutas)):

        directorio_rgb = rutas[i]
        directorio_gris = rutas_gray[i]

        # Lista de nombres de archivos en el directorio RGB
        nombres_archivos = os.listdir(directorio_rgb)

        # Iterar sobre cada archivo en el directorio RGB
        for nombre_archivo in nombres_archivos:
            # Construir la ruta completa para la imagen RGB
            ruta_rgb = os.path.join(directorio_rgb, nombre_archivo)

            # Leer la imagen RGB
            imagen_rgb = cv2.imread(ruta_rgb)

            # Convertir la imagen a escala de grises
            imagen_gris = cv2.cvtColor(imagen_rgb, cv2.COLOR_BGR2GRAY)

            # Construir la ruta completa para guardar la imagen en escala de grises
            ruta_gris = os.path.join(directorio_gris, nombre_archivo)

            # Guardar la imagen en escala de grises
            cv2.imwrite(ruta_gris, imagen_gris)



def CapturePosture(category:int, filename:list):

    # Font type.
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Colors.
    yellow = (0, 255, 255)
    
    # API para reconocimiento de pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # Colores.
    red = (50, 50, 255)
    green = (127, 255, 0)
    light_green = (127, 233, 100)
    yellow = (0, 255, 255)
    gray = (128, 128, 128)


    staticPath = os.path.join(os.path.dirname(__file__), 'app\static') #encuentra la ruta Data sin importar el sistema que se este usando al momento de la ejecucion
    data = os.path.join(staticPath,'Data')
    
    if not os.path.exists(data):
        os.makedirs(data)

    # Rutas de la carpeta del dataset RGB
    personpath = os.path.join(data, 'Training')
    valpath = os.path.join(data, 'Validation')
    goodposture = os.path.join(personpath, 'Good_Posture')
    val_good = os.path.join(valpath, 'Good_Posture')
    badposture = os.path.join(personpath, 'Bad_Posture')
    val_bad = os.path.join(valpath, 'Bad_Posture')
    regularposture = os.path.join(personpath, 'Regular_Posture')
    val_regular = os.path.join(valpath, 'Regular_Posture')    

    if  os.path.exists(personpath) and os.path.exists(valpath):
        #print(f"File successfully finding: {personpath} y {valpath}")
        pass
    else:
        os.makedirs(personpath)
        os.makedirs(valpath)
        
        os.makedirs(goodposture)
        os.makedirs(val_good)
        
        os.makedirs(badposture)
        os.makedirs(val_bad)
        
        os.makedirs(regularposture)
        os.makedirs(val_regular)
    '''///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'''
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    limite_inicial = 1
    limite_entrenamiento = 250
    imagenes_val = 38
    
    good_frames = limite_inicial
    bad_frames = limite_inicial
    regular_frames = limite_inicial
    total_good_postures = limite_inicial
    total_bad_postures = limite_inicial
    total_regular_posture = limite_inicial

    
    limite_final = limite_entrenamiento + imagenes_val        
    # limite
    
    
    while True:
        
        good_posture_files = count_files_by_extension(goodposture, 'jpg') + count_files_by_extension(val_good, 'jpg')
        regular_posture_files = count_files_by_extension(regularposture, 'jpg') + count_files_by_extension(val_regular, 'jpg')
        bad_posture_files = count_files_by_extension(badposture, 'jpg') + count_files_by_extension(val_bad, 'jpg')
        
        success, image = cap.read()
    
        if not success:
            break
        
        if (good_posture_files >= limite_final) and (regular_posture_files >= limite_final) and (bad_posture_files >= limite_final):
            break
        
        h, w, _ = image.shape
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        keypoints = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        lm = keypoints.pose_landmarks
        lmPose = mp_pose.PoseLandmark
        
        if lm:
            l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
            l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
            l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
            l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)
            l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
            l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)

            neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
            torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

            cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
            cv2.circle(image, (l_ear_x, l_ear_y), 7, yellow, -1)
            cv2.circle(image, (l_hip_x, l_hip_y), 7, yellow, -1)

            angle_text_string = 'Neck : ' + str(int(neck_inclination)) + '  Torso : ' + str(int(torso_inclination))

            if ((90 <= neck_inclination <= 110) or (80<= torso_inclination <=90)) and count_files_by_extension (goodposture, 'jpg') < limite_final:
                good_frames += 1

                """Generacion de textos en la imagen y generacion de puntos dentro de la imagen"""
                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, light_green, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, light_green, 2)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 4)

                """Generacion de rutas dependiendo de la accion con las imagenes"""
                if category == 1: # Actualizacion de imagen en good posture
                    img_filename = os.path.join(goodposture, filename)
                else: # Insercion de imagenes en good posture
                    img_filename = os.path.join(goodposture, 'good_{}.jpg'.format(total_good_postures))

                """Ciclos para actualizar o insertar"""
                if not os.path.exists(img_filename) and category == 1: # Update
                    cv2.imwrite(img_filename, image)
                    break
                elif not os.path.exists(img_filename) and count_files_by_extension(goodposture, 'jpg') <= limite_entrenamiento: # Insert
                    cv2.imwrite(img_filename, image)

                '''Datos de validacion'''
                if (limite_entrenamiento < good_frames <= limite_final):#se toman de las primeras 10 imagenes que se capturan de la camara
                    print(limite_entrenamiento < good_frames <= limite_final)
                    img_val_filename = os.path.join(val_good, 'good_{}.jpg'.format(total_good_postures))
                    cv2.imwrite(img_val_filename, image)
                    print(f"Por aqui paso {limite_entrenamiento < good_frames <= limite_final}")

                    # Cada vez que se detecta una buena postura, aumenta el contador de buenas posturas
                total_good_postures += 1

            elif ((69 <= neck_inclination <= 89) or (69 <= torso_inclination <=79 ))  and count_files_by_extension(regularposture, 'jpg') < limite_final:
            
                regular_frames += 1

                """Generacion de textos en la imagen y generacion de puntos dentro de la imagen"""
                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, yellow, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, yellow, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, yellow, 2)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), yellow, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), yellow, 4)

                """Generacion de rutas dependiendo de la accion con las imagenes"""
                if category == 2: # Regular
                    img_filename = os.path.join(regularposture, filename)
                else: # Insertar
                    img_filename = os.path.join(regularposture, 'regular_{}.jpg'.format(total_regular_posture))


                """Ciclos para actualizar o insertar"""
                if not os.path.exists(img_filename) and category == 2: # Actualizar
                    cv2.imwrite(img_filename, image)
                    break
                elif not os.path.exists(img_filename) and count_files_by_extension(regularposture, 'jpg') <= limite_entrenamiento: # Insert
                    cv2.imwrite(img_filename, image)

                
                '''Datos de validacion'''
                if (limite_entrenamiento < regular_frames <= limite_final):#si se toman de las primeras 10 imagenes que se capturan de la camara
                    img_val_filename = os.path.join(val_regular, 'regular_{}.jpg'.format(total_regular_posture))
                    cv2.imwrite(img_val_filename, image)

                total_regular_posture += 1

            elif ((111 <= neck_inclination <= 180) or (90<= torso_inclination <= 180)) and count_files_by_extension(badposture, 'jpg') < limite_final:

                bad_frames += 1

                """Generacion de textos en la imagen y generacion de puntos dentro de la imagen"""
                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, red, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 4)

                """Generacion de rutas dependiendo de la accion con las imagenes"""
                if category == 3: # Bad
                    img_filename = os.path.join(badposture, filename)
                else : # Insertar
                    img_filename = os.path.join(badposture, 'bad_{}.jpg'.format(total_bad_postures))

                """Ciclos para actualizar o insertar"""
                if not os.path.exists(img_filename) and category == 3: # Actualizar
                    cv2.imwrite(img_filename, image)
                    break
                elif not os.path.exists(img_filename) and count_files_by_extension(badposture, 'jpg') <= limite_entrenamiento: # Insertar
                    cv2.imwrite(img_filename, image)

                '''Datos de validacion'''
                if limite_entrenamiento < bad_frames <= limite_final:#si se toman de las primeras 10 imagenes que se capturan de la camara
                    img_val_filename = os.path.join(val_bad, 'bad_{}.jpg'.format(total_bad_postures))
                    cv2.imwrite(img_val_filename, image)

                # Cada vez que se detecta una mala postura, aumenta el contador de malas posturas
                total_bad_postures += 1
            else:
                
                """Generacion de textos en la imagen y generacion de puntos dentro de la imagen, cuando la imagen no se identifica"""
                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, gray, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, gray, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, gray, 2)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), gray, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), gray, 4)


            print(count_files_by_extension(goodposture, 'jpg'))
            print(count_files_by_extension(regularposture, 'jpg'))
            print(count_files_by_extension(badposture, 'jpg'))
            
        cv2.imshow('frame', image)
        
            
        if (good_posture_files >= limite_final) and (regular_posture_files >= limite_final) and (bad_posture_files >= limite_final) or cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
    
    if not os.path.exists(os.path.join(staticPath,'DataGray')):
        os.makedirs(os.path.join(staticPath,'DataGray'))
        generacion_datagray()
    else:
        generacion_datagray()
    
        

if __name__ == '__main__':
    category = 0
    filename = ''
    CapturePosture(category, filename)

