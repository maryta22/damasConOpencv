import cv2
import numpy as np

# Cargar la imagen
img = cv2.imread("imagen.jpg")

# Convertir a HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Definir el rango de color que se desea detectar en HSV
lower_color = np.array([0, 0, 0])
upper_color = np.array([180, 255, 255])

# Aplicar una máscara para detectar solo los píxeles dentro del rango de color
mask = cv2.inRange(hsv, lower_color, upper_color)

# Función para seleccionar la ROI

def select_roi(event, x, y, flags, param):
    global roi, roi_selected
    if event == cv2.EVENT_LBUTTONDOWN:
        roi = [x, y, x, y]
        roi_selected = False
    elif event == cv2.EVENT_LBUTTONUP:
        roi[2] = x
        roi[3] = y
        roi_selected = True


# Crear una ventana y asignar la función select_roi como el controlador de eventos del mouse
cv2.namedWindow("Imagen")
cv2.setMouseCallback("Imagen", select_roi)

# Variable global para indicar si se ha seleccionado la ROI
roi_selected = False

# Bucle hasta que se seleccione la ROI o se presione una tecla
while True:
    img_copy = img.copy()
    if not roi_selected:
        cv2.imshow("Imagen", img)
    else:
        # Obtener la ROI de la imagen
        x1 = roi[0]
        y1 = roi[1]
        x2 = roi[2]
        y2 = roi[3]

        print(x1,x2,y1,y2)

        roi = hsv[np.min((y1, y2)):np.max((y1, y2)),
                np.min((x1, x2)):np.max((x1, x2))]
        h, s, v = cv2.split(roi)

        lower_hue = np.min(h)
        upper_hue = np.max(h)
        lower_saturation = np.min(s)
        upper_saturation = np.max(s)
        lower_value = np.min(v)
        upper_value = np.max(v)

        lower_color = np.array(
            [lower_hue, lower_saturation, lower_value], dtype=np.uint8)
        upper_color = np.array(
            [upper_hue, upper_saturation, upper_value], dtype=np.uint8)

        print(lower_color, upper_color)

        break

    # Esperar a que se presione una tecla
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Cerrar la ventana y liberar recursos
cv2.destroyAllWindows()
