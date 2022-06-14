import tkinter as tk
import listas





ventana_principal = tk.Tk()
ventana_principal.title("Aplicación principal")
ventana_principal.minsize(800,600)

def cerrarVentana(v):
    v.destroy()
btn_salir = tk.Button(ventana_principal, text="Salir", command=lambda: cerrarVentana(ventana_principal))
btn_salir.place(x=720, y=550)
menubar = tk.Menu(ventana_principal)
ventana_principal.config(menu=menubar)
menu_archivo = tk.Menu(menubar, tearoff=1)
menu_archivo.add_command(label="Guardar",  command=listas.guardar_todo)
menu_archivo.add_checkbutton(label="Autoguardado", onvalue=1, offvalue=0)
menu_archivo.add_separator()
menu_archivo.add_command(label="Exit", command=ventana_principal.destroy)
menu_login = tk.Menu(menubar, tearoff=0)


# Adicionar al menu pirncipal los dos submenus
menubar.add_cascade(label="Archivo", menu=menu_archivo)


# Ciclo principal de la aplicación
ventana_principal.mainloop()