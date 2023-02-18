import cv2
import numpy as np

while True:

    # Inicializa la cámara
    cap = cv2.VideoCapture(0)

    # Lee un frame de la cámara
    ret, frame = cap.read()

    # Muestra el frame en una ventana
    cv2.imshow("Camera", frame)

    # Espera a que el usuario presione una tecla para tomar la foto
    key = cv2.waitKey(0) & 0xFF

    # Si el usuario presionó la tecla 's', guarda la foto
    if key == ord("s"):
        # Guarda la foto en formato JPEG
        cv2.imwrite("imagen.jpg", frame)
        break

cv2.destroyAllWindows()