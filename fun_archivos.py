
import datetime
from tkinter.messagebox import showerror
import listas as listas


def guardar_todo():
    guardar_admin
    guardar_carrera
    guardar_cursos
    guardar_estudiante(list)
def cargar_actividades(lista):
    if lista!=[]:
            respuesta=listas.actividades(lista[0],lista[1],lista[2],lista[3],lista[4],lista[5],lista[6],lista[7],lista[8])
            del(lista[0:9])
            while lista!=[]:
                respuesta.insertar_actividad_o(listas.actividades(lista[0],lista[1],lista[2],lista[3],lista[4],lista[5],lista[6],lista[7],lista[8]))  
                del(lista[0:9])    
    else:           
        respuesta=None
    return(respuesta)
def cargar_cursos_matri(lista):
    if lista!=[]:
            respuesta=listas.curso_matri(lista[0],lista[1])
            del(lista[0:2])
            while lista!=[]:
                respuesta.insertar_curso_matri(listas.curso_matri(lista[0],lista[1]))  
                del(lista[0:2])    
    else:           
        respuesta=None
    return(respuesta)

### archivos estudiantes ##
def cargar_archivo_estudiantes():
    respuesta=None
    try:
        with open("estudiantes.dat","tr") as lector:
            lectura= eval(lector.readline()[:-1])
            if lectura!='':
                respuesta=listas.estudiante(lectura[0],lectura[1],lectura[2],lectura[3],cargar_cursos_matri(lectura[4]),cargar_actividades(lectura[5]))
            lectura= eval(lector.readline()[:-1])
            while (lectura!=''):
                respuesta.insertar_est(listas.estudiante(lectura[0],lectura[1],lectura[2],lectura[3],lectura[4],lectura[5]))
                lectura= eval(lector.readline()[:-1])
    except FileNotFoundError as error:
        respuesta=input("No encontramos el archivo de estudiantes, desea crear un nuevo archivo de registro(si/no):")
        #respuesta=askyesno(title="Error", message="No encontramos el archivo de datos desea crear un nuevo archivo de registro (s/n)")
        if respuesta=='si':
            open("estudiantes.dat","tw").close()
    except Exception as error:
        print(error)
    finally:
        return respuesta


def guardar_estudiante(puntero):
        try:
            with open("estudiantes.dat","tw") as archivo:
                cursos_matri=listas.listar_punteros_cursos_matri(puntero.cursos_matriculados)
                actividades_matri=listas.listar_punteros_actividades(puntero.actividades)
                archivo.writelines([puntero.nombre,puntero.carrera,puntero.usuario,puntero.contrasena,cursos_matri,actividades_matri].__str__()+"\n")
                while puntero.sig!=None:
                    puntero=puntero.sig
                    cursos_matri=listas.listar_punteros_cursos_matri(puntero.cursos_matriculados)
                    actividades_matri=listas.listar_punteros_actividades(puntero.actividades)
                    archivo.writelines([puntero.nombre,puntero.carrera,puntero.usuario,puntero.contrasena,cursos_matri,actividades_matri].__str__()+"\n")
        except FileNotFoundError as error:
            showerror(message='No se pudo guardar en el archivo de estudiantes')



'''archivos administrador'''
def cargar_archivo_admin():
    respuesta=None
    try:
        with open("administradores.dat","tr") as lector:
            lectura= eval(lector.readline()[:-1])
            if lectura!='':
                respuesta=listas.administrador(lectura[0],lectura[1],lectura[2],lectura[3])
            lectura= eval(lector.readline()[:-1])
            while (lectura!=''):
                respuesta.insertar_admin(respuesta,listas.administrador(lectura[0],lectura[1],lectura[2],lectura[3]))
                lectura= eval(lector.readline()[:-1])
    except FileNotFoundError as error:
        respuesta=input("No encontramos el archivo de administradores desea crear un nuevo archivo de registro(si/no):")
        #respuesta=askyesno(title="Error", message="No encontramos el archivo de datos desea crear un nuevo archivo de registro (s/n)")
        if respuesta=='si':
            open("administradores.dat","tw").close()
    except Exception as error:
        print(error)
        
    finally:
        return respuesta



def guardar_admin(puntero):
        try:
            with open("administradores.dat","w") as archivo:
                archivo.writelines([puntero.nombre,puntero.telefono,puntero.usuario,puntero.contrasena].__str__()+"\n")
                while puntero.sig!=None:
                    puntero=puntero.sig
                    archivo.writelines([puntero.nombre,puntero.telefono,puntero.usuario,puntero.contrasena].__str__()+"\n")
        except FileNotFoundError as error:
            showerror(message='No se pudo guardar en el archivo de administradores')



'''ARCHIVOS CARRERAS'''

def cargar_archivo_carreras():
    respuesta=None
    try:
        with open("carreras.dat","r") as lector:
            lectura= eval(lector.readline()[:-1])
            if lectura!='':
                respuesta=listas.carrera(lectura[0])
            lectura= eval(lector.readline()[:-1])
            while (lectura!=''):
                respuesta.insertar_carrera(respuesta,listas.carrera(lectura[0]))
                lectura= eval(lector.readline()[:-1])
    except FileNotFoundError as error:
        respuesta=input("No encontramos el archivo de carreras desea crear un nuevo archivo de registro(si/no):")
        #respuesta=askyesno(title="Error", message="No encontramos el archivo de datos desea crear un nuevo archivo de registro (s/n)")
        if respuesta=='si':
            open("carreras.dat","w").close()
    except Exception as error:
        print(error)
    finally:
        return respuesta

def guardar_carrera(puntero):
        try:
            with open("carreras.dat","tw") as archivo:
                archivo.writelines([puntero.nombre].__str__()+"\n")
                while puntero.sig!=None:
                    puntero=puntero.sig
                    archivo.writelines([puntero.nombre].__str__()+"\n")
        except FileNotFoundError as error:
            showerror(message='No se pudo guardar en el archivo de carreras')



'''ARCHIVOS CURSOS'''      

def cargar_archivo_cursos():
    respuesta=None
    try:
        with open("cursos.dat","tr") as lector:
            lectura= eval(lector.readline()[:-1])
            if lectura!='':
                respuesta=listas.cursos(lectura[0],lectura[1],lectura[2],lectura[3],lectura[4],lectura[5],lectura[6],lectura[7])
            lectura= eval(lector.readline()[:-1])
            while (lectura!=''):
                respuesta.insertar_curso(respuesta,listas.cursos(lectura[0],lectura[1],lectura[2],lectura[3],lectura[4],lectura[5],lectura[6],lectura[7]))
                lectura= eval(lector.readline()[:-1])
    except FileNotFoundError as error:
        respuesta=input("No encontramos el archivo de cursos desea crear un nuevo archivo de registro(si/no):")
        #respuesta=askyesno(title="Error", message="No encontramos el archivo de datos desea crear un nuevo archivo de registro (s/n)")
        if respuesta=='si':
            open("cursos.dat","tw").close()
    except Exception as error:
        print(error)
    finally:
        return respuesta

def guardar_cursos(puntero):
        try:
            with open("cursos.dat","w") as archivo:
                archivo.writelines([puntero.nombre,puntero.creditos,puntero.dedicacion,puntero.horas_lectivas,puntero.inicia,puntero.finaliza,puntero.dia_clases,puntero.carrera].__str__()+"\n")
                while puntero.sig!=None:
                    puntero=puntero.sig
                    archivo.writelines([puntero.nombre,puntero.creditos,puntero.dedicacion,puntero.horas_lectivas,puntero.inicia,puntero.finaliza,puntero.dia_clases,puntero.carrera].__str__()+"\n")
        except FileNotFoundError as error:
            showerror(message='No se pudo guardar en el archivo de carreras')