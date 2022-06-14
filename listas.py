from sre_constants import JUMP
from time import sleep
from hashlib import md5
from getpass import getpass
import datetime as dt
import fun_archivos as archivos

list_carreras=None
list_estudiantes=None
list_cursos=None
list_administradores=None
def cargar_archivos():
    global list_administradores
    global list_carreras
    global list_cursos
    global list_estudiantes
    list_carreras=archivos.cargar_archivo_carreras()
    list_estudiantes=archivos.cargar_archivo_estudiantes()
    list_administradores=archivos.cargar_archivo_admin()
    list_cursos=archivos.cargar_archivo_cursos()

def guardar_todo():
    archivos.guardar_admin(list_administradores)
    archivos.guardar_carrera(list_carreras)
    archivos.guardar_cursos(list_cursos)
    archivos.guardar_estudiante(list_estudiantes)
def limpiar_terminal():
    print (chr(27) + "[2J")
def cifrar (entrada):                               # funcion para convertir la contraseña en una cifrada
    entrada_binaria=entrada.encode('ascii')
    resultado = md5(entrada_binaria)
    return (resultado.hexdigest())
def obtener_clave(mensaje):          #funcion que privatiza la contraseña al escribirla
    pswd = getpass(mensaje+": ")
    return (pswd)

def listar_punteros_cursos_matri(l):
    respuesta=[]
    if l!=None and l!=[]:
            respuesta.append(l.nombre)
            respuesta.append(l.estado)
            respuesta+=listar_punteros_cursos_matri(l.sig)
    return (respuesta)

def listar_punteros_actividades(l):
    respuesta=[]
    if l!=None and l!=[]:
            respuesta.append(l.nombre)
            respuesta.append(l.curso)
            respuesta.append(l.inicia)
            respuesta.append(l.finaliza)
            respuesta.append(l.dia_clases)
            respuesta.append(l.estado)
            respuesta.append(l.emocion_inicial)
            respuesta.append(l.emocion_final)
            respuesta.append(l.predominante_general)
            respuesta+=listar_punteros_actividades(l.sig)
    return (respuesta)

 




def listar_punteros(l):
        respuesta=[]
        if l!=None and l!=[]:
            respuesta.append(l.nombre)
            respuesta+=listar_punteros(l.sig)
        return (respuesta)
def obtener_x_nombre_est(l,nombre):
        puntero=l
        try:
            while puntero.nombre!=nombre:
                puntero=puntero.sig
            return (puntero)
        except:
            return None



usu_actual=None
puntero_actividades=None


class estudiante:
    nombre:None
    carrera:None
    usuario:None
    contrasena:None
    cursos_matriculados:None 
    actividades:None
    sig=None

    def __init__(self,nom,carr,usu,contra,cursos_matriculados,actividades) -> None:
        
        self.nombre=nom
        self.carrera=carr
        self.usuario=usu
        self.contrasena=contra
        self.cursos_matriculados=cursos_matriculados
        self.actividades=actividades
        self.sig=None
   
    def insertar_est (self,p):
        actual=self
        if actual.sig==None:
            actual.sig=p
        else:
            actual.insertar_est(actual.sig,p)

  
    def obtener_x_nombre_est(l,nombre):
        puntero=l
        try:
            while puntero.nombre!=nombre:
                puntero=puntero.sig
            return (puntero)
        except:
            return False
    

    def registrar_estudiante_o():
        global list_estudiantes
        limpiar_terminal()
        nombre=input("Nombre: ")
        carrera=input("Carrera: ")
        print("Autenticacion")
        usuario = input("\tNombre de usuario: ")
        contraseña = cifrar(obtener_clave("Digite su contraseña: "))
        cursos_mat=None
        actividades=None
        nv=estudiante(nombre,carrera,usuario,contraseña,cursos_mat,actividades)
        if list_estudiantes==None:
            list_estudiantes=nv
        else:
            list_estudiantes.insertar_est(nv)
        archivos.guardar_estudiante(list_estudiantes)
        
    def validar_est(u,c):
        global puntero_actividades
        global usu_actual
        global list_estudiantes
        actual=list_estudiantes
        resp=False
        c=cifrar(c)
        try:
            while actual.usuario!=u and actual.contrasena!=c:
                actual=actual.sig
            resp=True
            usu_actual=actual
            puntero_actividades=usu_actual.actividades
        except Exception as error:
            print(error)
            print("Usted ha digitado el usuario o contraseña incorrecta")
            #showwarning(title="alerta", message="Usted ha digitado el usuario o contraseña incorrecta")
        
        return(resp)

    def cambiar_carrera_o():
        global usu_actual
        global list_estudiantes
        print("Carreras disponibles:")
        print(list_carreras.nombre)
        carreranueva= input("nueva carrera:" )
        usu_actual.carrera=carreranueva
        usu_actual.cursos_matriculados=[]
        archivos.guardar_estudiante(list_estudiantes)

    def matricular_cursos_o():
        global list_estudiantes
        global usu_actual
        limpiar_terminal()
        print("Cursos disponibles")
        cursos_listados=listar_punteros(list_cursos)
        print (cursos_listados)
        a_matricular = input("Escriba el nombre del curso que desea matricular:")
        try:
            curso_deseado=obtener_x_nombre_est(list_cursos,a_matricular)
            if usu_actual.carrera==curso_deseado.carrera:
                if usu_actual.cursos_matriculados!=None:
                    if not obtener_x_nombre_est(usu_actual.cursos_matriculados,a_matricular):
                        while usu_actual.cursos_matriculados.sig!=None:
                            usu_actual.cursos_matriculados=usu_actual.cursos_matriculados.sig

                        usu_actual.cursos_matriculados.sig= curso_matri(curso_deseado.nombre,'')
                        archivos.guardar_estudiante(list_estudiantes)
                    else:
                        print("Curso ya matriculado")
                else:
                    usu_actual.cursos_matriculados=curso_matri(curso_deseado.nombre,'')
                    archivos.guardar_estudiante(list_estudiantes)
            else:
                print("El curso a matricular, no pertenece a su carrera")
        except Exception as er:
            print(er)
        
            print("Curso no disponible")


    def aprobar_reprobar():
        global list_estudiantes
        global usu_actual
        lista_cursos=listar_punteros(usu_actual.cursos_matriculados)
        print(lista_cursos)
        curso_modificar = input("Cual curso desea modificar el estado:")
        actual=usu_actual.cursos_matriculados
        while actual.sig!=None:
            if actual.nombre==curso_modificar:
                actual.estado=input("Curso aprobado o reprobado:")
                archivos.guardar_estudiante(list_estudiantes)
                break
            else:
                actual=actual.sig

    def menu_registro_de_actividades_O():     #menu para que el estudiante registre las actividades que quiera
        limpiar_terminal()   
        global list_estudiantes
        global usu_actual
        
         
        estado=''
        nombre=input('Cual es el nombre de la actividad:')
        curso=input('si pertenece a algun curso escribalo,si no dejelo en blanco:')
        dia=input('Que dia es la actividad:')
        hora_inicio=(input("Hora de inicio: "))
        h_inicial=dt.time(int(hora_inicio),0)
        hora_final=(input("Hora de finalizacion: "))
        h_final=dt.time(int(hora_final),0)
        estado=''
        emo_init=''
        emo_fin=''
        predo_gen=''
        nueva_actividad=actividades(nombre,curso,h_inicial,h_final,dia,estado,emo_init,emo_fin,predo_gen)

        cursos_matr=usu_actual.cursos_matriculados


        if curso=='':
            insertar_actividad(nueva_actividad)
            
        else:
            try:
                while cursos_matr.nombre!=curso:
                    cursos_matr=cursos_matr.sig
                if cursos_matr.estado=='':
                    insertar_actividad(nueva_actividad)
                    
                else:
                    print("error: curso ya aprobado o reprobado")
            except Exception as error:
                print(error)
                print("error: actividad no relacionada a ningun curso matriculado")

    
def choque_horario (fi1,ff1,fi2,ff2):       #revisa 2 fechas de inicio y 2 finales para retornar su existe un choque
    return ((fi2>=fi1 and fi2<=ff1)or(ff2>=fi1 and ff2<=ff1))        


def insertar_actividad (nueva_actividad): #comprueba si una actividad a registrar no choca con alguna ya registrada
    global usu_actual
    choque=False
    if usu_actual.actividades!=None:
        while usu_actual.actividades.estado!='':
            usu_actual.actividades= usu_actual.actividades.sig
        if usu_actual.actividades.dia_clases==nueva_actividad.dia_clases:
            if choque_horario(fi1=usu_actual.actividades.inicia,ff1=usu_actual.actividades.finaliza,fi2=nueva_actividad.inicia,ff2=nueva_actividad.finaliza):
                choque=True
            
        if not choque: 
            insertar_actividad_o(usu_actual.actividades,nueva_actividad)
            archivos.guardar_estudiante(list_estudiantes)
            print ("se agrego la actividad")
        else:
            print ("No se agrega por choque de horarios")
    else:
        if not choque: 
            usu_actual.actividades=actividades(nueva_actividad.nombre,nueva_actividad.curso,nueva_actividad.inicia,nueva_actividad.finaliza,nueva_actividad.dia_clases,nueva_actividad.estado,nueva_actividad.emocion_inicial,nueva_actividad.emocion_final,nueva_actividad.predominante_general)
            print ("se agrego la actividad")
            archivos.guardar_estudiante(list_estudiantes)
        return (choque)





class administrador:
    nombre:None
    telefono:None
    usuario:None
    contrasena:None
    sig=None

    def __init__(self,n,t,u,c) -> None:
        self.nombre=n
        self.telefono=t
        self.usuario=u
        self.contrasena=c
        self.sig=None

    def insertar_admin (self,l,p):
            if l.sig==None:
                l.sig=p
            else:
                self.insertar_admin(l.sig,p)


    def registrar_administrador_o():
        global list_administradores
        limpiar_terminal()
        nombre=input("Nombre: ")
        telefono=input("Telefono: ")
        print("Autenticacion")
        usuario = input("\tNombre de usuario: ")
        contraseña = cifrar(obtener_clave("Digite su contraseña: "))
        nuevo_admin=administrador(nombre,telefono,usuario,contraseña)
        if list_administradores==None:
            list_administradores=nuevo_admin
        else:
            list_administradores.insertar_admin(list_administradores,nuevo_admin)
        archivos.guardar_admin(list_administradores)


    def validar_admin(u,c):
        global list_administradores
        actual=list_administradores
        resp=False
        c=cifrar(c)
        try:
            while actual.usuario!=u and actual.contrasena!=c:
                actual=actual.sig
            resp=True
        except:
            print("Usted ha digitado el usuario o contraseña incorrecta")
            #showwarning(title="alerta", message="Usted ha digitado el usuario o contraseña incorrecta")
        finally: 
            return(resp)





class carrera:
    nombre:None
    
    sig=None
    
    def __init__(self,n,) -> None:
        self.nombre=n
        
        self.sig=None

    def insertar_carrera (self,l,p):
            if l.sig==None:
                l.sig=p
            else:
                self.insertar_carrera(l.sig,p)

    def registrar_carreras_o():
        global list_carreras
        limpiar_terminal()
        print("Carreras existentes:") 
        try:
            while list_carreras.sig!=None:
                print(list_carreras.nombre)
                list_carreras=list_carreras.sig
            print(list_carreras.nombre)
        except Exception as error:
            print(error)
            print("Actualemente no hay ninguna carrera")
        nombre=(input("Nombre de la carrera: "))
        nuevo=carrera(nombre)
        if list_carreras==None:
            list_carreras=nuevo
        else: 
            list_carreras.insertar_carrera(list_carreras,nuevo)

        archivos.guardar_carrera(list_carreras)
    
class cursos:
    nombre:None
    creditos:None
    dedicacion:None
    horas_lectivas:None
    inicia:None
    finaliza:None
    dia_clases:None
    carrera:None
    sig:None

    def __init__(self,n,c,d,h,i,f,dia,carr) -> None:
        self.nombre=n
        self.creditos=c
        self.dedicacion=d
        self.horas_lectivas=h
        self.inicia=i
        self.finaliza=f
        self.dia_clases=dia
        self.carrera=carr
        self.sig=None


    def insertar_curso (self,l,p):
        if l.sig==None:
            l.sig=p
        else:
                self.insertar_curso(l.sig,p)


    def registrar_curso_o():
        global list_cursos
        nombre=input("Nombre del curso: ")
        creditos=(input("creditos: "))
        dedicacion=input("horas totales de dedicacion: ")
        horas_lectivas=(input("horas lectivas: "))
        h_ini=(input("Hora de inicio : "))
        inicia=dt.time(int(h_ini),0,0)
        h_fin=(input("Hora de finalizacion : "))
        finaliza=dt.time(int(h_fin),0,0)
        dia_clases=input("dia del curso: ")
        carrera=input("carreras que pertenece el curso: ")
        curso_nuevo=cursos(nombre,creditos,dedicacion,horas_lectivas,inicia,finaliza,dia_clases,carrera)
        if list_cursos==None:
            list_cursos=curso_nuevo
        else: 
            list_cursos.insertar_curso(list_cursos,curso_nuevo)
        archivos.guardar_cursos(list_cursos)


class curso_matri:
    nombre:None
    estado:None
    sig:None

    def __init__(self,n,e) -> None:
        self.nombre=n
        self.estado=e
        self.sig=None

    def insertar_curso_matri(l,p):
        actual=l
        if actual.sig==None:
            actual.sig=p
        else:
            actual.insertar_est(actual.sig,p)

        
class actividades:
    nombre:None
    curso:None
    inicia:None
    finaliza:None
    dia_clases:None
    estado=None
    emocion_inicial:None
    emocion_final:None
    predominante_general=None
    sig:None
    
    def __init__(self,n,c,i,f,d,estado,emo_init,emo_fin,predo_gen) -> None:
        self.nombre=n
        self.curso=c
        self.inicia=i
        self.finaliza=f
        self.dia_clases=d
        self.estado=estado
        self.sig=None
        self.emocion_inicial=emo_init
        self.emocion_final=emo_fin
        self.predominante_general=predo_gen
def insertar_actividad_o (l,p):
        if l.sig==None:
            l.sig=p
        else:
                insertar_actividad_o(l.sig,p)



def calendario_o():
    global usu_actual
    global list_cursos
    lunes=[]
    martes=[]
    miercoles=[]
    jueves=[]
    viernes=[]
    sabado=[]
    domingo=[]

    curso_pendiente=usu_actual.cursos_matriculados
    while curso_pendiente.sig!=None:
        if curso_pendiente.estado=='':
            curso_original=obtener_x_nombre_est(list_cursos,curso_pendiente.nombre)
            dia=curso_original.dia_clases
            if dia=='lunes':
                lunes.append(curso_original.nombre)
                lunes.append(curso_original.inicia)
                lunes.append(curso_original.finaliza)
                curso_pendiente=curso_pendiente.sig
                break
            elif dia=='martes':
                martes.append(curso_original.nombre)
                martes.append(curso_original.inicia)    
                martes.append(curso_original.finaliza)
                curso_pendiente=curso_pendiente.sig
                break
            elif dia=='miercoles':
                miercoles.append(curso_original.nombre)
                miercoles.append(curso_original.inicia)
                miercoles.append(curso_original.finaliza)
                curso_pendiente=curso_pendiente.sig
                break       
            elif dia=='jueves':
                jueves.append(curso_original.nombre)
                jueves.append(curso_original.inicia)
                jueves.append(curso_original.finaliza)
                curso_pendiente=curso_pendiente.sig
                break
            elif dia=='viernes':
                viernes.append(curso_original.nombre)
                viernes.append(curso_original.inicia)
                viernes.append(curso_original.finaliza)
                curso_pendiente=curso_pendiente.sig
                break
            elif dia=='sabado':
                sabado.append(curso_original.nombre)
                sabado.append(curso_original.inicia)
                sabado.append(curso_original.finaliza)
                curso_pendiente=curso_pendiente.sig
                break
            elif dia=='domingo':
                domingo.append(curso_original.nombre)
                domingo.append(curso_original.inicia)
                domingo.append(curso_original.finaliza)
                curso_pendiente=curso_pendiente.sig
                break            
        else:
             curso_pendiente=curso_pendiente.sig      
    if curso_pendiente.estado=='':
            curso_original=obtener_x_nombre_est(list_cursos,curso_pendiente.nombre)
            dia=curso_original.dia_clases
            if dia=='lunes':
                lunes.append(curso_original.nombre)
                lunes.append(curso_original.inicia)
                lunes.append(curso_original.finaliza)
                
            elif dia=='martes':
                martes.append(curso_original.nombre)
                martes.append(curso_original.inicia)    
                martes.append(curso_original.finaliza)
                
            elif dia=='miercoles':
                miercoles.append(curso_original.nombre)
                miercoles.append(curso_original.inicia)
                miercoles.append(curso_original.finaliza)
                       
            elif dia=='jueves':
                jueves.append(curso_original.nombre)
                jueves.append(curso_original.inicia)
                jueves.append(curso_original.finaliza)
                
            elif dia=='viernes':
                viernes.append(curso_original.nombre)
                viernes.append(curso_original.inicia)
                viernes.append(curso_original.finaliza)
                
            elif dia=='sabado':
                sabado.append(curso_original.nombre)
                sabado.append(curso_original.inicia)
                sabado.append(curso_original.finaliza)
                
            elif dia=='domingo':
                domingo.append(curso_original.nombre)
                domingo.append(curso_original.inicia)
                domingo.append(curso_original.finaliza)
    
    actividad_pen=usu_actual.actividades
    while actividad_pen.sig!=None:
        if actividad_pen.estado=='':
            dia=actividad_pen.dia_clases
            if dia=='lunes':
                lunes.append(actividad_pen.nombre)
                lunes.append(actividad_pen.inicia)
                lunes.append(actividad_pen.finaliza)
                lunes.append(actividad_pen.curso)
                actividad_pen=actividad_pen.sig
                break
            elif dia=='martes':
                martes.append(actividad_pen.nombre)
                martes.append(actividad_pen.inicia)    
                martes.append(actividad_pen.finaliza)
                martes.append(actividad_pen.curso)
                actividad_pen=actividad_pen.sig
                break
            elif dia=='miercoles':
                miercoles.append(actividad_pen.nombre)
                miercoles.append(actividad_pen.inicia)
                miercoles.append(actividad_pen.finaliza)
                miercoles.append(actividad_pen.curso)
                actividad_pen=actividad_pen.sig
                break       
            elif dia=='jueves':
                jueves.append(actividad_pen.nombre)
                jueves.append(actividad_pen.inicia)
                jueves.append(actividad_pen.finaliza)
                jueves.append(actividad_pen.curso)
                actividad_pen=actividad_pen.sig
                break
            elif dia=='viernes':
                viernes.append(actividad_pen.nombre)
                viernes.append(actividad_pen.inicia)
                viernes.append(actividad_pen.finaliza)
                viernes.append(actividad_pen.curso)
                actividad_pen=actividad_pen.sig
                break
            elif dia=='sabado':
                sabado.append(actividad_pen.nombre)
                sabado.append(actividad_pen.inicia)
                sabado.append(actividad_pen.finaliza)
                sabado.append(actividad_pen.curso)
                actividad_pen=actividad_pen.sig
                break
            elif dia=='domingo':
                domingo.append(actividad_pen.nombre)
                domingo.append(actividad_pen.inicia)
                domingo.append(actividad_pen.finaliza)
                domingo.append(actividad_pen.curso)
                actividad_pen=actividad_pen.sig
                break
        else:
            actividad_pen=actividad_pen.sig      
    if actividad_pen.estado=='':
        dia=actividad_pen.dia_clases
        if dia=='lunes':
            lunes.append(actividad_pen.nombre)
            lunes.append(actividad_pen.inicia)
            lunes.append(actividad_pen.finaliza)
            lunes.append(actividad_pen.curso)
             
        elif dia=='martes':
            martes.append(actividad_pen.nombre)
            martes.append(actividad_pen.inicia)    
            martes.append(actividad_pen.finaliza)
            martes.append(actividad_pen.curso)
              
        elif dia=='miercoles':
            miercoles.append(actividad_pen.nombre)
            miercoles.append(actividad_pen.inicia)
            miercoles.append(actividad_pen.finaliza)
            miercoles.append(actividad_pen.curso)
                      
        elif dia=='jueves':
            jueves.append(actividad_pen.nombre)
            jueves.append(actividad_pen.inicia)
            jueves.append(actividad_pen.finaliza)
            jueves.append(actividad_pen.curso)
                
        elif dia=='viernes':
            viernes.append(actividad_pen.nombre)
            viernes.append(actividad_pen.inicia)
            viernes.append(actividad_pen.finaliza)
            viernes.append(actividad_pen.curso)
              
        elif dia=='sabado':
            sabado.append(actividad_pen.nombre)
            sabado.append(actividad_pen.inicia)
            sabado.append(actividad_pen.finaliza)
            sabado.append(actividad_pen.curso)
             
        elif dia=='domingo':
            domingo.append(actividad_pen.nombre)
            domingo.append(actividad_pen.inicia)
            domingo.append(actividad_pen.finaliza)
            domingo.append(actividad_pen.curso)  
    limpiar_terminal()
    print("Lunes:")
    for e in lunes:
        print(e)
    print("Martes:")
    for e in martes:
        print(e)
    print("Miercoles:")
    for e in miercoles:
        print(e)
    print("Jueves:")
    for e in jueves:
        print(e)
    print("Viernes:")
    for e in viernes:
        print(e)
    print("Sabado:")
    for e in sabado:
        print(e)
    print("Domingo:")
    for e in domingo:
        print(e)
    opptt=input("Envie 1 tecla para regresar al menu:")        
    if opptt==1:
        JUMP        



## Listas###

# list_carreras=(carrera('computacion'))
# list_cursos=cursos('taller de programacion',3, 9,3,dt.time(8,00,),dt.time(11,00,),'martes','computacion')
# list_estudiantes= estudiante('jeison','computacion','jeisonb1','jei123')
# list_administradores=administrador('jeison',83782547,'admin','21232f297a57a5a743894a0e4a801fc3')


