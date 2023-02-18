import cv2
import numpy as np
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps

matriz = [
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2]
]

tamano = 60

def crearTablero(tablero, matriz):
    cuadros = {}
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                cuadros[str(i) + str(j)] = tablero.create_rectangle(j * tamano, i * tamano, (j + 1) * tamano,
                                                                    (i + 1) * tamano,
                                                                    fill="black")
            else:
                cuadros[str(i) + str(j)] = tablero.create_rectangle(j * tamano, i * tamano, (j + 1) * tamano,
                                                                    (i + 1) * tamano,
                                                                    fill="white")
    modificarFichas(tablero, matriz)


def modificarFichas(tablero, matriz):
    fila1 = [1, 3, 5, 7]
    fila2 = [2, 4, 6, 8]
    fila3 = fila1
    fila4 = fila2
    fila5 = fila1
    fila6 = fila2
    fila7 = fila1
    fila8 = fila2

    filas = [fila1, fila2, fila3, fila4, fila5, fila6, fila7, fila8]

    matrizReducida = reducirMatriz(tablero, matriz)

    fila = 0
    for f in matrizReducida:
        columna = 0
        for c in f:
            if c == 1:
                crearFichas(tablero, filas[fila][columna] - 1, fila, "red")
            elif c == 2:
                crearFichas(tablero, filas[fila][columna] - 1, fila, "blue")
            columna = columna + 1

        fila = fila + 1


def reducirMatriz(tablero, matriz):
    nuevaMatriz = []

    for i in range(8):
        nuevaMatriz.append([matriz[i][0] + matriz[i][1], matriz[i][2] + matriz[i][3], matriz[i][4] + matriz[i][5],
                            matriz[i][6] + matriz[i][7]])

    return nuevaMatriz


def crearFichas(tablero, coor1, coor2, color):
    tablero.create_oval(coor1 * tamano, coor2 * tamano, (coor1 + 1) * tamano, (coor2 + 1) * tamano, fill=color)


def nuevoTablero():
    global verde1, verde2, segundos, jugador, tablero, lblnota, matriz
    segundos = 0
    tablero.delete(verde1)
    tablero.delete(verde2)
    tablero.delete(amarillo)
    verde1 = None
    verde2 = None
    print("nuevo tablero")
    mensaje, jugador ,movimientoValido = validarMovimiento(pos1, pos2, jugador)
    print(mensaje)
    #Aqui es donde debes agregar el codigo recibes "pos1" y "pos2" que son tuplas (fila, columna)
    #de donde a donde quiere hacer el movimiento y "matriz" que es la matriz actual
    #lo unico que necesito es que retornes la matriz actualizada (o la misma) y un booleano si se  relizaron cambios o no
   
    matrizFalsa = [
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2]
    ]
    if movimientoValido:
        """ if jugador == 1:
            jugador = 2
        else:
            jugador = 1 """
        #matriz = matrizFalsa
        crearTablero(tablero, matriz)
        lblturno.config(text="Turno del jugador: " + str(jugador))
    else:
        lblnota.config(text="Movimiento invalido realice otra vez el turno")



def visualizar():
    global cap, pantalla, amarillo, fila, columna, segundos, verde2, verde1, pos1, pos2
    
    count_matriz = np.array(matriz)
    gana_jugador_1 = count_matriz == 2
    gana_jugador_2 = count_matriz == 1
    if np.count_nonzero(gana_jugador_1) == 0:
        messagebox.showinfo("Ganador!", "Gana el jugador 1")
        pantalla.destroy()
    elif np.count_nonzero(gana_jugador_2) == 0:
        messagebox.showerror("Ganador!", "Gana el jugador 2")
        pantalla.destroy()

    tablero.delete(amarillo)
    lblnota.config(text="Esperando movimiento...")

    ret, frame = cap.read()
    print(np.shape(frame))
    frame = cv2.flip(frame,1)
    
    lower1 = np.array([119, 29, 104], np.uint8)
    upper1 = np.array([161, 56, 172], np.uint8)

    lower2 = np.array([71, 71, 104], np.uint8)
    upper2 = np.array([84, 133, 192], np.uint8)

    if ret:
        color = None
        if jugador == 2:
            frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            color = cv2.inRange(frameHSV, lower1, upper1)
            color = color[0:480, 0:480]
        else:
            frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            color = cv2.inRange(frameHSV, lower2, upper2)
            color = color[0:480, 0:480]

        im = Image.fromarray(color)
        img = ImageTk.PhotoImage(image=im)
        lblVideo.configure(image=img)

        blue8 = cv2.resize(color, (8, 8), interpolation=cv2.INTER_AREA)
        posicionmax = np.where(blue8 == np.amax(blue8))
        i = posicionmax[0][0]
        j = posicionmax[1][0]

        if (fila == i) & (columna == j):
            segundos += 1
        else:
            segundos = 0

        fila = i
        columna = j

        if segundos < 60:
            if verde1 is None:
                amarillo = tablero.create_rectangle(j * tamano, i * tamano, (j + 1) * tamano, (i + 1) * tamano,
                                                    fill="yellow")
            else:
                amarillo = tablero.create_rectangle(j * tamano, i * tamano, (j + 1) * tamano, (i + 1) * tamano,
                                                    fill="orange")

        else:
            if verde1 is None:
                verde1 = tablero.create_rectangle(j * tamano, i * tamano, (j + 1) * tamano, (i + 1) * tamano,
                                                  fill="green")
                segundos = 0
                pos1 = (i, j)
            else:
                verde2 = tablero.create_rectangle(j * tamano, i * tamano, (j + 1) * tamano, (i + 1) * tamano,
                                                  fill="green")
                segundos = 0
                pos2 = (i, j)

                nuevoTablero()
                pass

        lblVideo.image = img
        lblVideo.after(10, visualizar)

    else:
        lblVideo.image = ""
        cap.release()

def swapTurn(turno):
        return 1 if turno == 2 else 2

def validarMovimiento(initialPosition, finalPosition, turno):
    global matriz
    if matriz[initialPosition[0]][initialPosition[1]] == 0:
        return "Movimiento inválido, la casilla inicial no contiene una ficha", turno, False
    if matriz[initialPosition[0]][initialPosition[1]] != turno:
        return "Movimiento no válido, la posicion inicial ({}, {}) tiene una ficha contraria".format(
            initialPosition[0], initialPosition[1]), turno, False
    diferencia_x = finalPosition[0] - initialPosition[0]
    diferencia_y = abs(finalPosition[1] - initialPosition[1])
    if (turno == 1 and diferencia_x < 0) or (turno == 2 and diferencia_x > 0):
        return "Las fichas solo se pueden mover hacia adelante", turno, False
    diferencia_x = abs(diferencia_x)
    if diferencia_x != diferencia_y:
        return "Movimiento inválido, las fichas solo se pueden mover en diagonal", turno, False
    if diferencia_x > 2 or diferencia_y > 2:
        return "Movimiento no válido", turno, False
    """ print("Moviendo la ficha desde {} hasta {}".format(
        initialPosition, finalPosition)) """
    if matriz[finalPosition[0]][finalPosition[1]] == turno:
        return "No puedes mover la ficha a una casilla ocupada por otra ficha tuya", turno, False
    else:

        if diferencia_x == 1:
            if matriz[finalPosition[0]][finalPosition[1]] == 0:

                matriz[initialPosition[0]
                                         ][initialPosition[1]] = 0
                matriz[finalPosition[0]
                                         ][finalPosition[1]] = turno
                return "Movimiento válido, actualizando tablero", swapTurn(turno), True
            else:
                return "Para comer una ficha debes apuntar a la siguiente casilla", turno, False
        else:
            if matriz[finalPosition[0]][finalPosition[1]] != 0:
                return "Para comer una ficha la casilla detrás debe estar vacía", turno, False
            else:
                casilla_intermedia = (
                    int((finalPosition[0]+initialPosition[0])/2), int((finalPosition[1]+initialPosition[1])/2))
                if matriz[casilla_intermedia[0]][casilla_intermedia[1]] == swapTurn(turno):
                    matriz[casilla_intermedia[0]
                                             ][casilla_intermedia[1]] = 0
                    matriz[finalPosition[0]
                                             ][finalPosition[1]] = turno
                    matriz[initialPosition[0]
                                             ][initialPosition[1]] = 0
                    return "Movimiento válido, ficha comida. Actualizando el tablero", swapTurn(turno), True
                elif matriz[casilla_intermedia[0]][casilla_intermedia[1]] == 0:
                    return "Movimiento inválido, no puedes mover más de una casilla a menos que comas una ficha enemiga", turno, False
                else:
                    return "Movimiento inválido, la ficha que intentas comer es de tu equipo", turno, False


def ir_al_juego():
    pantalla_juego.pack(fill='both',expand=1)
    pantalla_inicio.forget()
    visualizar()

pantalla = Tk()

pantalla.title("Juego de Damas")

pantalla_inicio = Frame(pantalla, bg="#507af8")

""" label_bg_image = Label(pantalla_inicio, image= bg_image)
label_bg_image.pack() """
pantalla_juego = Frame(pantalla,bg= '#507af8')

pantalla_inicio_titulo = Label(pantalla_inicio, text="Proyecto de procesamiento digital de imágenes",font= ('New Times Roman', 20),bg= '#507af8')
subtitulo_inicio = Label(pantalla_inicio, text="Juego de damas usando visión artificial",font= ('New Times Roman', 15),bg= '#507af8')
pantalla_juego_titulo = Label(pantalla_juego, text="Juego de damas")

pantalla_inicio_titulo.pack()
subtitulo_inicio.pack()
pantalla_juego_titulo.pack()

#image_tablero = Image.open("tablero_gui.PNG")
#image_tablero = image_tablero.resize((300,300), Image.ANTIALIAS)
#image_tablero = ImageTk.PhotoImage(image_tablero)
frameCnt = 5
frames = [PhotoImage(file='juego.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]
def update(ind):

    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label_imagen.configure(image=frame)
    pantalla_inicio.after(1000, update, ind)
label_imagen = Label(pantalla_inicio, width=300, height=300)
label_imagen.pack(side=LEFT)
pantalla_inicio.after(0, update, 0)
info_frame = Frame(pantalla_inicio ,bg= '#507af8', padx=50)

desarrolladores_titulo = Label(info_frame, text="Desarrolladores",font= ('New Times Roman', 15, 'bold'),bg= '#507af8')
desarrollador_1 = Label(info_frame, text="○ María Rivera",font= ('New Times Roman', 10),bg= '#507af8')
desarrollador_2 = Label(info_frame, text="○ Danny Montenegro",font= ('New Times Roman', 10),bg= '#507af8')
desarrolladores_titulo.pack(side=TOP)
desarrollador_1.pack()
desarrollador_2.pack()
btn_a_juego = Button(info_frame, text="Jugar",command=ir_al_juego, bg='#95e1e9', activebackground="#95e1e9", )
btn_salir = Button(info_frame, text="Salir", command=pantalla.destroy, bg='#95e1e9', activebackground="#95e1e9")
btn_a_juego.pack(side=LEFT)
btn_salir.pack(side=RIGHT)
info_frame.pack(side=LEFT)

pantalla_inicio.pack(fill='both', expand=1)

jugador = 1

lblturno = Label(pantalla_juego, text="Turno del jugador: "+ str(jugador), pady=30, font= ('New Times Roman', 30),bg= '#507af8')
lblturno.pack(side=TOP)

lblnota= Label(pantalla_juego, text="Esperando movimiento...", font= ('New Times Roman', 15),bg= '#507af8')
lblnota.pack(side=BOTTOM)

tablero = Canvas(pantalla_juego, width=480, height=480)
crearTablero(tablero, matriz)
tablero.pack(side = LEFT)

amarillo = None
fila = None
columna = None
segundos = 0
pos1 = None
pos2 = None
verde1 = None
verde2 = None

cap = cv2.VideoCapture(0)

lblVideo = Label(pantalla_juego, width=480, height=480)
lblVideo.pack(side = RIGHT)

def rendirse():
    global cap
    cap.release()
    respuesta = messagebox.askyesno("Question", "Jugador {},¿Seguro que quieres rendirte?".format(jugador))
    if respuesta:
        messagebox.showinfo("Ganador!", "Gana el jugador {}".format(swapTurn(jugador)))
        pantalla.destroy()
    cap = cv2.VideoCapture(0)
    visualizar()

btn_rendirse = Button(pantalla_juego, text="Rendirse", command=rendirse, bg='#95e1e9', activebackground="#95e1e9")
btn_rendirse.pack()

pantalla.mainloop()