import cv2
import os
import math as m
import mediapipe as mp

# Calculate angle.
def findAngle(x1, y1, x2, y2):
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
    degree = int(180 / m.pi) * theta
    return degree

'''
accion 1.- Update
category 1.- Good 2.- Regular 3.- Bad
filename: filename path 
'''

def count_files_by_extension(dirname, extension):
    # Obtener la lista de archivos en la carpeta
    files = os.listdir(dirname)

    # Filtrar archivos por la extensión deseada
    files_with_extension = [file for file in files if file.endswith(extension)]

    # Contar la cantidad de archivos con la extensión
    amount_files = len(files_with_extension)

    return amount_files


def CapturePosture(category:int, filename:list):

    # Font type.
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Colors.
    yellow = (0, 255, 255)
    pink = (255, 0, 255)

    # API para reconocimiento de pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # Colors.
    red = (50, 50, 255)
    green = (127, 255, 0)
    light_green = (127, 233, 100)
    yellow = (0, 255, 255)
    pink = (255, 0, 255)

    staticPath = os.path.join(os.path.dirname(__file__), 'app\static') #encuentra la ruta Data sin importar el sistema que se este usando al momento de la ejecucion
    data = os.path.join(staticPath,'DataGray')
    
    if not os.path.exists(data):
        os.makedirs(data)

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
    
    
    good_frames = 1
    bad_frames = 1
    regular_frames = 1
    total_good_postures = 1
    total_bad_postures = 1
    total_regular_posture = 1
    
    # limite
    while True:
        success, image = cap.read()
        if not success:
            break

        h, w, _ = image.shape
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        keypoints = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        lm = keypoints.pose_landmarks
        lmPose = mp_pose.PoseLandmark
        
        if lm:
            l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
            l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
            r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
            r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
            l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
            l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)
            l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
            l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)

            neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
            torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

            cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
            cv2.circle(image, (l_ear_x, l_ear_y), 7, yellow, -1)
            cv2.circle(image, (l_shldr_x, l_shldr_y - 100), 7, yellow, -1)
            cv2.circle(image, (r_shldr_x, r_shldr_y), 7, pink, -1)
            cv2.circle(image, (l_hip_x, l_hip_y), 7, yellow, -1)
            cv2.circle(image, (l_hip_x, l_hip_y - 100), 7, yellow, -1)

            angle_text_string = 'Neck : ' + str(int(neck_inclination)) + '  Torso : ' + str(int(torso_inclination))

            if  neck_inclination < 20 and neck_inclination > 0 and torso_inclination < 5 and torso_inclination > 0  and count_files_by_extension(goodposture, 'jpg') < 250:
                good_frames += 1

                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, light_green, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, light_green, 2)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 4)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 4)

                if category == 1: # Good update
                    img_filename = os.path.join(goodposture, filename)
                else: # Insert
                    img_filename = os.path.join(goodposture, 'good_{}.jpg'.format(total_good_postures))

                if not os.path.exists(img_filename) and category == 1: # Update
                    cv2.imwrite(img_filename, image)
                    break
                elif not os.path.exists(img_filename): # Insert
                    cv2.imwrite(img_filename, image)
                
                if good_frames<11:#se toman de las primeras 10 imagenes que se capturan de la camara
                    img_val_filename = os.path.join(val_good, 'good_{}.jpg'.format(total_good_postures))
                    if not os.path.exists(img_val_filename):
                        cv2.imwrite(img_val_filename, image)
                
                # Cada vez que se detecta una buena postura, aumenta el contador de buenas posturas
                total_good_postures += 1
                
            elif neck_inclination < 40 and neck_inclination > 20 and torso_inclination < 10 and torso_inclination > 5 and count_files_by_extension(regularposture, 'jpg') < 250:

                regular_frames += 1
                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, yellow, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, yellow, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, yellow, 2)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), yellow, 4)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), yellow, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), yellow, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), yellow, 4)
                
                if category == 2: # Regular
                    img_filename = os.path.join(regularposture, filename)
                else: # Insertar
                    img_filename = os.path.join(regularposture, 'regular_{}.jpg'.format(total_regular_posture))
                

                if not os.path.exists(img_filename) and category == 2: # Actualizar
                    cv2.imwrite(img_filename, image)
                    break
                elif not os.path.exists(img_filename): # Insert
                    cv2.imwrite(img_filename, image)

                    
                if regular_frames<11:#se toman de las primeras 10 imagenes que se capturan de la camara
                    img_val_filename = os.path.join(val_regular, 'regular_{}.jpg'.format(total_regular_posture))
                    if not os.path.exists(img_val_filename):
                        cv2.imwrite(img_val_filename, image)
                
                total_regular_posture += 1
                
            elif count_files_by_extension(badposture, 'jpg') < 250:
                  
                bad_frames += 1
                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, red, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 4)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 4)
                
                if category == 3: # Bad
                    img_filename = os.path.join(badposture, filename)
                else: # Insertar
                    img_filename = os.path.join(badposture, 'bad_{}.jpg'.format(total_bad_postures))


                if not os.path.exists(img_filename) and category == 3: # Actualizar
                    cv2.imwrite(img_filename, image)
                    break
                elif not os.path.exists(img_filename): # Insertar
                    cv2.imwrite(img_filename, image)
                
                
                if bad_frames<11:#se toman de las primeras 10 imagenes que se capturan de la camara
                    img_val_filename = os.path.join(val_bad, 'bad_{}.jpg'.format(total_bad_postures))
                    if not os.path.exists(img_val_filename):
                        cv2.imwrite(img_val_filename, image)
                # Cada vez que se detecta una mala postura, aumenta el contador de malas posturas
                total_bad_postures += 1
            print(count_files_by_extension(goodposture, 'jpg'))
            print(count_files_by_extension(regularposture, 'jpg'))
            print(count_files_by_extension(badposture, 'jpg'))
        # Display the image
        cv2.imshow('frame', image)
        print(count_files_by_extension(goodposture, 'jpg'))
        print(count_files_by_extension(regularposture, 'jpg'))
        print(count_files_by_extension(badposture, 'jpg'))
        #Paro generico para insercion de frames
        if count_files_by_extension(goodposture, 'jpg') == 250 and count_files_by_extension(regularposture, 'jpg') == 250 and count_files_by_extension(badposture, 'jpg') == 250 or cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

    

if __name__ == '__main__':
    category = 0
    filename = ''
    CapturePosture(category, filename)
