import cv2
import os

def flip_images():

    train_path = os.path.join(os.path.dirname(__file__), 'app\static\Data\Training')
    good = os.path.join(train_path, 'Good_Posture')
    regular = os.path.join(train_path, 'Regular_Posture')
    bad = os.path.join(train_path, 'Bad_Posture')
    
    for i in range(251, 501):
        img_filename = os.path.join(regular, 'regular_{}.jpg'.format(i))
        # Leer la imagen
        imagen = cv2.imread(img_filename)
        # Invertir horizontalmente la imagen
        imagen_invertida = cv2.flip(imagen, 1)
        
        os.remove(img_filename)
        cv2.imwrite(img_filename, imagen_invertida)
        print(f"La imagen numero {i} ha sido cambiada")

flip_images()