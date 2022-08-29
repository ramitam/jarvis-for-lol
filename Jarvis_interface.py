# SOLO INTERFAZ GRÁFICA

from tkinter import *

from jarvis_for_lol import pedir_cosas

# iniciar tkinter
aplicacion = Tk()

#titulo
aplicacion.title('Jarvis for LoL')

#color de fondo
aplicacion.config(bg='gray10')

#panel superior
panel_superior = Frame(aplicacion, bd=1, relief=FLAT)
panel_superior.pack(side=TOP)

#etiqueta titulo
etiqueta_titulo = Label(panel_superior, text='JARVIS', fg='gray98',
                        font=('Dosis', 58), bg='gray10', width=27)
etiqueta_titulo.grid(row=0, column=0)

# panel iniciar


boton = Button(aplicacion, text="Iniciar", command=pedir_cosas)
boton.pack()
aplicacion.mainloop()
