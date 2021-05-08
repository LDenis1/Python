#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from math import *

##############VENTANA$$$$$$$$$$$$$$$
ventana=Tk()
ventana.title("CALCULADORA")
ventana.geometry("750x450")
ventana.iconbitmap('icon.ico')
ventana.configure(background="white smoke")
ventana.resizable(0,0)
color_boton=("white smoke")


##################Bottones################
AC = PhotoImage(file='Buttons/AC.png')
DEL = PhotoImage(file='Buttons/DEL.png')
igual = PhotoImage(file='Buttons/igual.png')

simplep = PhotoImage(file='Buttons/simplep.png')
simpleq = PhotoImage(file='Buttons/simpleq.png')
simpler = PhotoImage(file='Buttons/simpler.png')
simples = PhotoImage(file='Buttons/simples.png')

negacion = PhotoImage(file='Buttons/negacion.png')
conjuncion = PhotoImage(file='Buttons/conjuncion.png')
disyuncion = PhotoImage(file='Buttons/disyuncion.png')
condicional = PhotoImage(file='Buttons/condicional.png')


bicondicional = PhotoImage(file='Buttons/bicondicional.png')
XOR = PhotoImage(file='Buttons/XOR.png')
par1 = PhotoImage(file='Buttons/par1.png')
par2 = PhotoImage(file='Buttons/par2.png')

entrada = PhotoImage(file='Buttons/entrada.png')







def btnClik(num):
    global operador
    operador=operador+str(num)
    input_text.set(operador) #VISUALIZAR LA OPERACION EN LA PANTALLA
    
def clear():
    global operador
    operador=("")
    input_text.set("0")

def operacion():
    global operador
    try:
        opera=str(eval(operador))#REALIZAR LA OPERACIÓN PREVIAMENTE VISUALIZADA EN PANTALLA
    except:
        clear()
        opera=("ERROR")
    input_text.set(opera)#MUESTRA EL RESULTADO


########OTROS###########
ancho_boton=7
alto_boton=2
input_text=StringVar()
operador=""
clear()





###Botones##
Button(ventana, image=AC,            border='0',  bg=color_boton,              command=clear).place(x=17,y=180)
Button(ventana, image=DEL,           border='0',  bg=color_boton,   command=lambda:btnClik(1)).place(x=107,y=180)
Button(ventana, image=simplep,       border='0',  bg=color_boton,   command=lambda:btnClik("p")).place(x=17,y=240)
Button(ventana, image=simpleq,       border='0',  bg=color_boton,   command=lambda:btnClik("q")).place(x=107,y=240)
Button(ventana, image=simpler,       border='0',  bg=color_boton,   command=lambda:btnClik("r")).place(x=197,y=240)
Button(ventana, image=simples,       border='0',  bg=color_boton,   command=lambda:btnClik("s")).place(x=267,y=240)
Button(ventana, image=negacion,      border='0',  bg=color_boton,   command=lambda:btnClik("~")).place(x=17,y=300)
Button(ventana, image=conjuncion,    border='0',  bg=color_boton,   command=lambda:btnClik("^")).place(x=107,y=300)
Button(ventana, image=disyuncion,    border='0',  bg=color_boton,   command=lambda:btnClik("v")).place(x=197,y=300)
Button(ventana, image=condicional,   border='0',  bg=color_boton,   command=lambda:btnClik("→")).place(x=267,y=300)
Button(ventana, image=bicondicional, border='0',  bg=color_boton,   command=lambda:btnClik("↔")).place(x=17,y=360)
Button(ventana, image=XOR,           border='0',  bg=color_boton,   command=lambda:btnClik("+")).place(x=107,y=360)
Button(ventana, image=par1,          border='0',  bg=color_boton,   command=lambda:btnClik("(")).place(x=197,y=360)
Button(ventana, image=par2,          border='0',  bg=color_boton,   command=lambda:btnClik(")")).place(x=267,y=360)



Button(ventana, image=igual,         border= '0', bg=color_boton,   command=operacion).place(x=197,y=180)

Salida=Entry(ventana,font=('arial',20,'bold'),width=18,textvariable=input_text,bd=7,insertwidth=4,bg="light gray",justify="right").place(x=30,y=70)



ventana.mainloop()
