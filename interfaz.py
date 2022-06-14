
from sre_constants import JUMP
from time import sleep
from listas import carrera, cursos, limpiar_terminal
from listas import administrador
from listas import estudiante 
#import fun_archivos as archivos
import listas
from proyecto3 import menu_actividades_paralelas, menu_concentracion_paralela
'''                             MENU DEL PROYECTO                                                                              '''
#                               INTERFAZ GRAFICA

listas.cargar_archivos()



def menu_interfaz():  #Este es el menu principal de la interfaz funciona para la division de usuarios y de funciones
    listas.limpiar_terminal()
    while True:
        listas.limpiar_terminal()
        print ("Bienvenido a tu calendario")


        print("¿Usuario estudiante o administrativo?")
        
        print ("1) Estudiante")
        print ("2) Administrador")
        print ("3) Salir")
        opcion= int(input("Digite el numero de opcion que desea:"))
        listas.limpiar_terminal()

        match opcion:
            case 1:
                while True:
                    listas.limpiar_terminal()
                # interfaz que si quiere registrarse, inicar sesion, o salir como estudiante
                    print("Usuario Estudiante")
                    print("1) Iniciar sesion")
                    print("2) Registrarse")

                    print("3) Salir")
                    opt= int(input(" Su opcion es: "))
                    match opt:
                        case 1: 
                        
                            #iniciar sesion estudiante*****
                            usuario= input("Usuario: ")
                            contra= listas.obtener_clave("Contraseña: ")
                            
                            if estudiante.validar_est(usuario,contra):    #mediante la funcion validar_estudiante, se logra compararlos datos almacenados en una listan de diccionarios con los datos puestos en tiempo real
                                listas.limpiar_terminal()
                                menu_prin_estudiante()  #menu principal para estudiantes
                            else:
                                
                                sleep(2)


                        case 2:
                            estudiante.registrar_estudiante_o()  #funcion que registra el nuevo estudiante

                        case 3:
                            break
                        case _:
                            print("Opcion invalida")
            case 2:
                print("Usuario Administrativo") #menu de registro o inicio de sesion para administradores
                print("1) Iniciar sesion")
                print("2) Registrarse")
                print("3) Salir")
                optt= int(input(" Su opcion es: "))
                match optt:
                    case 1: #iniciar sesion acomo administrador
                        usuario= input("Usuario: ")
                        contraseña = listas.obtener_clave("Contraseña: ")
                        if administrador.validar_admin(u=usuario,c=contraseña): #en esta funcion se valida el administrador
                            
                            menu_prin_administrativo()  #menu principal del administrador
                                
                        else:
                            
                            sleep(2)
                    case 2:
                        administrador.registrar_administrador_o()   #funcion para registrar nuevos datos de un usuario administrador
                        
                    case 3:
                        break
                    case _:
                        print("Opcion invalida")
            
                
            case 3:
                print("\n\t¡Muchas garcias por utilizar nuestro sistema!")
                listas.sleep(3)
                listas.limpiar_terminal()
                break



def menu_prin_estudiante():  #menu principal del estudiante
    while True: 
        JUMP
        listas.limpiar_terminal()
        print("1) Cambio de carrera")
        print("2) Matricular cursos")
        print("3) Agregar actividades")
        print("4) Mostar calendario")
        print("5) Tiempo de actividad")
        print("6) Control de concentracion")
        print("7) Salir")
        opt= int(input(" Su opcion es: "))

        match opt: 
            case 1:
                # Cambio de Carrera:
                estudiante.cambiar_carrera_o()    # hace que la carrera previamente guardada se cambie por una nueva
            
            
            

            case 2:
                while True:
                    listas.limpiar_terminal()        #menu para cursos
                # Matricular cursos:
                    print("1) Matricular cursos")
                    print("2) Modificar estado de cursos")
                    print("3) Salir")
                    opttt= int(input(" Su opcion es: "))
                    match opttt:
                        case 1:
                            estudiante.matricular_cursos_o()       # esta funcion matricula los cursos que escojan y que sean de carrera
                        case 2: 
                           estudiante.aprobar_reprobar()  # funcion para poder cambiar el estado del curso
                        case 3: 
                            break
                        case _:
                            print("Opcion invalida")

            case 3:
                # Agregar actividades
                    estudiante.menu_registro_de_actividades_O()
            case 4:
                listas.calendario_o()     #funcion que imprime un horario con varios datos de los cursos y actividades del estudiante
            case 5:  
                limpiar_terminal()
                menu_actividades_paralelas()  
            case 6:
                limpiar_terminal()
                menu_concentracion_paralela()
            case 7:
                break
            case _:
                print("Opcion invalida")

def menu_prin_administrativo(): #menu del administrador
    while True: 
        listas.limpiar_terminal()
        print("Bienvenido administrador")  
        print("1) Agregar cursos")
        print("2) Agregar carreras")
        print("3) Salir")
        opt= int(input(" Su opcion es: "))
        match opt:
            case 1:
                cursos.registrar_curso_o() # esta funcion agrega cursos para matricularlos despues
                
            case 2:
                carrera.registrar_carreras_o() #agrega carreras
            case 3:
                break
            case _:
                print("Opcion invalida")

menu_interfaz()
