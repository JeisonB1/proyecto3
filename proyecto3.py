"""
pip3 install opencv-python
pip3 install google-api-python-client
pip3 install google-cloud
pip3 install google-cloud-vision
"""
import fun_archivos as archivos
from pygame import mixer
import listas
import time
import os, io
from time import sleep
from tkinter.messagebox import showerror, showinfo, askokcancel
import cv2 as cv
import threading
from google.cloud import vision


###snake_case

estado_concentracion=[False]
estado=[False]

class rostro ():              ### clase tipo rostro, para la utilizacion de la funcion de capturar la imagen
    
    def __init__(self) -> None:
        pass

    def capturar_imagen(self,):    # captura una imagen
        
        camara = cv.VideoCapture(0)
        leido, imagen = camara.read()
        camara.release()

        if leido == True:
            cv.imwrite("foto.png", imagen)
        else:
            showerror(
                title='Error en la toma de imagen', 
                message='No fue posible capturar la imagen con esta dispositivo!')
        return imagen


def tarea_paralela(estado):
    '''FUNCION: si esta entre la hora de la actividad, 
                hace llamado a los procesos de captura de imagen y reconocimiento de emociones
                
                
        ARGS: estado: parametro que decide si se realiza el ciclo de inicio a la comparacion,
                para luego seguir con los procesos'''
    mi_rostro=rostro()
    hora_actual2=time.strftime("%H:%M:%S")
    while estado[0]:
        if str(actividad_actual.finaliza) > hora_actual2:
            mi_rostro.capturar_imagen()
            reconocimiento()
            sleep(60)
        else:
            guardar_reportes()
            

def proceso_ninja():
    '''FUNCION: Compara las horas de las actividades con la actual y si coinciden hace a la funcion tarea_paralela,
                 un hilo paralelo  '''
    global hora_actual
    hora_actual=time.strftime("%H:%M:%S")
    global estado
    if str(actividad_actual.inicia) <= hora_actual and str(actividad_actual.finaliza) >= hora_actual:
        estado=[True]
        parametros=[estado]
        proceso=threading.Thread(target=tarea_paralela,args=parametros)       ### linea exacta del hilo paralelo
        print (f"Captura de emociones activado")
        proceso.start()
    else:
        showerror(title="Error",message=" La activacion de Tiempo de actividad esta fuera de alguna actividad registrada")


## menu que va en interfaz de segunda etapa para activar todo los procesos de etapa 3 apara registro de emociones###
def menu_actividades_paralelas():
    '''Funcion: menu de interfaz en la terminal para el uso de las diferentes funciones principales del proyecto'''
    listas.limpiar_terminal()
    global pun_actividades
    global actividad_actual
    pun_actividades=listas.puntero_actividades
    while True:
        listas.limpiar_terminal()
        print ("1) Activar\n2) Desactivar\n3) Revisar emociones\n4) Guardar emociones\n5) Salir ")
        resp=input ('Selección: ')
        if resp=="1":
            actividad=input("Cual es el nombre de la actividad a realizar: ")
           
            if 'actividad_actual' in globals():
                if actividad!=actividad_actual.nombre:
                    guardar_reportes()
            actividad_actual=listas.obtener_x_nombre_est(pun_actividades,actividad)
            if actividad_actual!=None:
                proceso_ninja()
                
            else:
                print("Actividad no registrada")
        elif resp== "2":
        
            try:
                estado[0]=False
            except:
                pass
        elif resp=="3":
            actividad=input("Cual es el nombre de la actividad revisar: ")
            actividad_revisar=listas.obtener_x_nombre_est(pun_actividades,actividad)
            if actividad_revisar!=None:
                listas.limpiar_terminal()
                print("Emociones durante la actividad")
                print("Primeros minutos: " + actividad_revisar.emocion_inicial )
                print("Ultimos minutos: " + actividad_revisar.emocion_final )
                print("Emocion Predominante: "+ actividad_revisar.predominante_general)
                sleep(10)
        elif resp=="4":
            guardar_reportes()
        else:
            break

## menu que va en interfaz de segunda etapa para activar todo los procesos de etapa 3 para la concentarcion ###
def proceso_concentracion():
    '''FUNCION:  hace a la funcion tarea_paralela_concentracion, un hilo paralelo  '''
    global estado_concentracion

    estado_concentracion=[True]
    parametros=[estado_concentracion]
    proceso=threading.Thread(target=tarea_paralela_concentracion,args=parametros)
    print (f"Captura de concentracion activado")
    proceso.start()


def tarea_paralela_concentracion(estado):
    '''funcion: da inicio segun el estado a los proceso para la mecanica de concetracion
    args: estado: interruptor que decide si se continua con los procesos o se cortan'''
    global alarma
    mi_rostro=rostro()
    
    while estado[0]:
        mi_rostro.capturar_imagen()
        reconocimiento_concentracion()
        if alarma:
            sleep(3)
        else:
            sleep(25)


def menu_concentracion_paralela():
    '''funcion: menu para la activacion de la mecanica de concentracion'''
    global estado_concentracion
    listas.limpiar_terminal()
    while True:
        print ("1) Activar\n2) Desactivar\n3) Salir ")
        resp=input ('Selección: ')
        if resp=="1":
            proceso_concentracion()
            
        elif resp== "2":
            estado_concentracion[0]=False
           
        else:
            
            break





emotional_list=[]
cont_alarma=6
def reconocimiento_concentracion():
    ''' funcion: conexion con el servicio de google vision, para asi hacer reconocimiento facil y sacar los angulos para detectar si hay desconcentracion'''
    global alarma
    global emotional_list
    global cont_alarma
    global estado
 
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']= r'key.json'
    client=vision.ImageAnnotatorClient()

    with io.open('foto.png','rb') as image_file:
        content = image_file.read()

    imagen = vision.Image(content=content)

    response = client.face_detection(image=imagen)

    faces = response.face_annotations


    #faces_list=[]
    if len(faces)==1:
        for face in faces:
        #dicccionario con los angulos asociados a la detección de la cara
        #pan: horizontal=decir no
        #tilt:vertical=decir si
        #roll: cabecear 
            
            global estado_concentracion
            if estado_concentracion[0]==True:
                face_angles=dict(roll_angle=face.roll_angle,pan_angle=face.pan_angle,tilt_angle=face.tilt_angle)
                alarma=False
                if face_angles["pan_angle"] < -30 or face_angles["pan_angle"] > 40 or face_angles["tilt_angle"]<-13 or face_angles["tilt_angle"] > 23:
                    alarma=True
                    cont_alarma-=1
                    if cont_alarma<=0:
                        resp=False
                        while resp!=True:
                            mixer.init()
                            mixer.music.load("sonido.mp3")                ### si llega a haber desconcentracion, se imite un sonido hasta ser aceptado
                            mixer.music.play(30)
                            resp=askokcancel(message="¿Desea continuar?", title="Alerta")
                            if resp:
                                mixer.music.stop()
                else:
                    cont_alarma=6  

def reconocimiento():
    ''' funcion: conexion con el servicio de google vision, para asi hacer reconocimiento facil y sacar las emociones detectadas'''
    global alarma
    global emotional_list
    global cont_alarma
    global estado
 
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']= r'key.json'
    client=vision.ImageAnnotatorClient()

    with io.open('foto.png','rb') as image_file:
        content = image_file.read()

    imagen = vision.Image(content=content)

    response = client.face_detection(image=imagen)

    faces = response.face_annotations

    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')

    #faces_list=[]
    if len(faces)==1:
        for face in faces:
            #Emociones: Alegría, pena, ira, sorpresa
            if estado[0]==True:
                face_expressions=dict(  
                    joy_likelihood=likelihood_name[face.joy_likelihood],
                    sorrow_likelihood=likelihood_name[face.sorrow_likelihood],
                    anger_likelihood=likelihood_name[face.anger_likelihood],
                    surprise_likelihood=likelihood_name[face.surprise_likelihood])
                ##modo de conteo de expresiones
                if face_expressions["joy_likelihood"]=="UNLIKELY" or face_expressions["joy_likelihood"]=="POSSIBLE" or face_expressions["joy_likelihood"]=='LIKELY' or face_expressions["joy_likelihood"]== 'VERY_LIKELY':
                    emotional_list.append(1)

                elif face_expressions["sorrow_likelihood"]=="UNLIKELY" or face_expressions["sorrow_likelihood"]=="POSSIBLE" or face_expressions["sorrow_likelihood"]=='LIKELY' or face_expressions["sorrow_likelihood"]== 'VERY_LIKELY':
                    emotional_list.append(2)
                elif face_expressions["anger_likelihood"]=="UNLIKELY" or face_expressions["anger_likelihood"]=="POSSIBLE" or face_expressions["anger_likelihood"]=='LIKELY'or face_expressions["anger_likelihood"]== 'VERY_LIKELY':
                    emotional_list.append(3)

                elif face_expressions["surprise_likelihood"]=="UNLIKELY" or face_expressions["surprise_likelihood"]=="POSSIBLE" or face_expressions["surprise_likelihood"]=='LIKELY' or face_expressions["surprise_likelihood"]== 'VERY_LIKELY':
                   emotional_list.append(4)
    else:
        showerror( title="ERROR", message= "Ninguno o varios rostros detectado")
    
def mayor(a,b):
    '''funcion: sacar el mayor entre 2 numeros
    args: 2 numeros'''
    mayor=b
    if a>b:
        mayor=a
    return mayor
def guardar_reportes():
    '''funcion: hace el conteo de las emociones, y segun lo solicitado se guarda en las actividades esos registros'''
    global actividad_actual
    global emotional_list
    if estado[0]==False:
    
        cont_joy=0
        cont_sorrow=0
        cont_anger=0
        cont_surprise=0
        emocion_mayor=None

        
        for emocion in emotional_list[:5]:    #Emocion predominante primero 5min
            if emocion== 1:
                cont_joy+=1
            elif emocion== 2:
                cont_sorrow+=1
            elif emocion== 3:
                cont_anger+=1
            elif emocion== 4:
                cont_surprise+=1
        if mayor(cont_joy,cont_sorrow)>mayor(cont_anger,cont_surprise):
            emocion_mayor=mayor(cont_joy,cont_sorrow)
        else:
            emocion_mayor=mayor(cont_anger,cont_surprise)

        if emocion_mayor==cont_joy:
            actividad_actual.emocion_inicial='Felicidad'
        elif emocion_mayor==cont_sorrow:
            actividad_actual.emocion_inicial='Trsiteza'
        elif emocion_mayor==cont_anger:
            actividad_actual.emocion_inicial='Enojo'
        elif emocion_mayor==cont_surprise:
            actividad_actual.emocion_inicial='Sorpesa'
        cont_joy=0
        cont_sorrow=0
        cont_anger=0
        cont_surprise=0
        for emocion in emotional_list[-4:]:  
              #Emocion predominante ultimos 5min
            if emocion== 1:
                cont_joy+=1
            elif emocion== 2:
                cont_sorrow+=1
            elif emocion== 3:
                cont_anger+=1
            elif emocion== 4:
                cont_surprise+=1
        if mayor(cont_joy,cont_sorrow)>mayor(cont_anger,cont_surprise):
            emocion_mayor=mayor(cont_joy,cont_sorrow)
        else:
            emocion_mayor=mayor(cont_anger,cont_surprise)

        if emocion_mayor==cont_joy:
            actividad_actual.emocion_final='Felicidad'
        elif emocion_mayor==cont_sorrow:
            actividad_actual.emocion_final='Trsiteza'
        elif emocion_mayor==cont_anger:
            actividad_actual.emocion_final='Enojo'
        elif emocion_mayor==cont_surprise:
            actividad_actual.emocion_final='Sorpesa'

        cont_joy=0
        cont_sorrow=0
        cont_anger=0
        cont_surprise=0
        for emocion in emotional_list:    #Emocion predominante general 5min
            if emocion== 1:
                cont_joy+=1
            elif emocion== 2:
                cont_sorrow+=1
            elif emocion== 3:
                cont_anger+=1
            elif emocion== 4:
                cont_surprise+=1
        if mayor(cont_joy,cont_sorrow)>mayor(cont_anger,cont_surprise):
            emocion_mayor=mayor(cont_joy,cont_sorrow)
        else:
            emocion_mayor=mayor(cont_anger,cont_surprise)

        if emocion_mayor==cont_joy:
            actividad_actual.predominante_general='Felicidad'
        elif emocion_mayor==cont_sorrow:
            actividad_actual.predominante_general='Trsiteza'
        elif emocion_mayor==cont_anger:
            actividad_actual.predominante_general='Enojo'
        elif emocion_mayor==cont_surprise:
            actividad_actual.predominante_general='Sorpesa'

        emotional_list=[]
        archivos.guardar_estudiante(listas.list_estudiantes)
    else:
        showinfo("ALERTA","Primero desactive la sesion de fotos")

