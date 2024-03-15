import cv2
import math
import mediapipe as mp

def findAngle(x1, y1, x2, y2):
    theta = math.acos((x2 - x1) / math.sqrt((x2 - x1) * 2 + (y2 - y1) * 2))
    degree = math.degrees(theta)
    return degree

def CapturePosture():

    # Font type.
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Colors.
    yellow = (0, 255, 255)
    gray = (128, 128, 128)
    red = (50, 50, 255)
    green = (127, 255, 0)
    light_green = (127, 233, 100)
    yellow = (0, 255, 255)
    
    # API para reconocimiento de pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()



   
    '''///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'''
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    # limite
    while True:
        success, image = cap.read()
        if not success:
            break

        h, w, _ = image.shape
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        keypoints = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        lm = keypoints.pose_landmarks
        lmPose = mp_pose.PoseLandmark
        
        if lm:
            

            angle_text_string = 'Neck : ' + str(int(neck_inclination)) + '  Torso : ' + str(int(torso_inclination))

            if  (90 > neck_inclination < 110) and 110 >  torso_inclination < 90:

                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, light_green, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, light_green, 2)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 4)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 4)
                
            elif neck_inclination < 40 and neck_inclination > 20 and torso_inclination < 10 and torso_inclination > 5:

                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, yellow, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, yellow, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, yellow, 2)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), yellow, 4)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), yellow, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), yellow, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), yellow, 4)
                
                
            elif (neck_inclination > 40 and neck_inclination < 60) and (20 < torso_inclination > 10):
                  
                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, red, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 4)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 4)
                
            else:
                cv2.putText(image, angle_text_string, (10, 30), font, 0.9, gray, 2)
                cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, gray, 2)
                cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, gray, 2)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), gray, 4)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), gray, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), gray, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), gray, 4)
            
        # Display the image
        cv2.imshow('frame', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

CapturePosture()
        
# Liberar la captura de video y cerrar la ventana