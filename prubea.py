from tkinter.messagebox import showerror, showinfo, askokcancel
import os, io
import cv2 as cv
from google.cloud import vision
from pygame import mixer
resp=False
while resp!=True:
                            mixer.init()
                            mixer.music.load("sonido.mp3")
                            mixer.music.play(30)
                            resp=askokcancel(message="¿Desea continuar?", title="Alerta")

def capturar_imagen():
        
        camara = cv.VideoCapture(0)
        leido, imagen = camara.read()
        camara.release()

        if leido == True:
            cv.imwrite("foto.png", imagen)


os.environ['GOOGLE_APPLICATION_CREDENTIALS']= r'key.json'
client=vision.ImageAnnotatorClient()

with io.open('foto.png','rb') as image_file:
    content = image_file.read()

imagen = vision.Image(content=content)

response = client.face_detection(image=imagen)

faces = response.face_annotations

likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')

faces_list=[]
if len(faces)==1:
    for face in faces:
        #dicccionario con los angulos asociados a la detección de la cara
       face_angles=dict(roll_angle=face.roll_angle,pan_angle=face.pan_angle,tilt_angle=face.tilt_angle)


