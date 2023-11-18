import cv2
import time
import math as m
import mediapipe as mp

# face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

# Calculo de distancia
def findDistance(x1, y1, x2, y2):
    dist = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

# Calculo de angulos
def findAngle(x1, y1, x2, y2):
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
    degree = int(180 / m.pi) * theta
    return degree

# Envia advertencias al usuario
def sendWarning(x):
    pass

# =============================CONSTANTS and INITIALIZATIONS=====================================#
# Modif

frame_count = 0

class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.good_frames = 0
        self.bad_frames = 0
        self.regular_frames = 0
        self.total_good_postures = 0
        self.total_bad_postures = 0
        self.total_regular_posture = 0
    
    def __del__(self):
        self.cap.release()

    def get_frame(self):
        # Default settings of the color and configuration
        # Inicializacion deconteo para los frames.
        self.good_frames = 0
        self.bad_frames = 0
        self.regular_frames = 0

        # Font type.
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Colors.
        blue = (255, 127, 0)
        red = (50, 50, 255)
        green = (127, 255, 0)
        dark_blue = (127, 20, 0)
        light_green = (127, 233, 100)
        yellow = (0, 255, 255)
        pink = (255, 0, 255)

        # Initialize mediapipe pose class.
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()
        # Frame count 
        global frame_count
        
        # Get the time when initialize the code
        start_time = time.time()

        # Instance of the propertie cap read that read the frames
        success, image = self.cap.read()
        
        # Creation of frame characteristics
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_size = (width, height)
        image = cv2.resize(image, frame_size, interpolation=cv2.INTER_LINEAR)
        
        # frame_count += 0
        
        # Transform the image shape
        h, w = image.shape[:2]
        
        # Image filter color and proccesing 
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        keypoints = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        

        lm = keypoints.pose_landmarks
        lmPose = mp_pose.PoseLandmark
        
        l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
        l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
        r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
        r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
        l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
        l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)
        l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
        l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)

        offset = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)

        if offset < 100:
            cv2.putText(image, str(int(offset)) + ' Alineado', (w - 150, 30), font, 0.9, green, 2)
        else:
            cv2.putText(image, str(int(offset)) + ' No alineado', (w - 150, 30), font, 0.9, red, 2)

        neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
        torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

        cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
        cv2.circle(image, (l_ear_x, l_ear_y), 7, yellow, -1)
        cv2.circle(image, (l_shldr_x, l_shldr_y - 100), 7, yellow, -1)
        cv2.circle(image, (r_shldr_x, r_shldr_y), 7, pink, -1)
        cv2.circle(image, (l_hip_x, l_hip_y), 7, yellow, -1)
        cv2.circle(image, (l_hip_x, l_hip_y - 100), 7, yellow, -1)

        angle_text_string = 'Neck : ' + str(int(neck_inclination)) + '  Torso : ' + str(int(torso_inclination))

        if  neck_inclination < 20 and neck_inclination > 0 and torso_inclination < 5 and torso_inclination > 0 :
            self.good_frames += 1
            cv2.putText(image, angle_text_string, (10, 30), font, 0.9, light_green, 2)
            cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, light_green, 2)
            cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, light_green, 2)
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 4)
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 4)
            cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 4)
            cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 4)
            
            # Cada vez que se detecta una buena postura, aumenta el contador de buenas posturas
            self.total_good_postures += 1
        elif neck_inclination < 40 and neck_inclination > 20 and torso_inclination < 10 and torso_inclination > 5:
            self.regular_frames += 1
            cv2.putText(image, angle_text_string, (10, 30), font, 0.9, yellow, 2)
            cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, yellow, 2)
            cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, yellow, 2)
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), yellow, 4)
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), yellow, 4)
            cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), yellow, 4)
            cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), yellow, 4)
            self.total_regular_posture += 1
            
        else:
            
            self.bad_frames += 1
            cv2.putText(image, angle_text_string, (10, 30), font, 0.9, red, 2)
            cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.9, red, 2)
            cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.9, red, 2)
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 4)
            cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 4)
            cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 4)
            cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 4)
            
            # Cada vez que se detecta una mala postura, aumenta el contador de malas posturas
            self.total_bad_postures += 1
        
        time_string_good = 'Buenas posturas : ' + str(round(self.good_time, 1)) + 's'
        cv2.putText(image, time_string_good, (10, h - 100), font, 0.9, green, 2)
        time_string_regular = 'Regular posturas : ' + str(round(self.regular_time, 1)) + 's'
        cv2.putText(image, time_string_regular, (10, h - 80), font, 0.9, yellow, 2)
        time_string_bad = 'Malas posturas : ' + str(round(self.bad_time, 1)) + 's'
        cv2.putText(image, time_string_bad, (10, h - 60), font, 0.9, red, 2)
        time_string_total = 'Total de posturas : ' + str(round(self.total_time, 1)) + 's'
        cv2.putText(image, time_string_total, (10, h - 15), font, 0.9, blue, 2)
        percent_string = str(round(self.correct_percent, 2)) + ' %'
        cv2.putText(image, percent_string, (w - 160, h - 75), font, 0.9, green, 2)
        
        if self.bad_time > 1000000000000000000:
            sendWarning()
        ret, jpeg = cv2.imencode('.jpg', image)

        return [jpeg.tobytes()]