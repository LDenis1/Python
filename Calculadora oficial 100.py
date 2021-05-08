
#Librerias
from tkinter import*
import ast
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from itertools import product
import re

#Ventana
ventana=Tk()
ventana.title("CALCULADORA LOGICA")
ventana.geometry("1000x450")
ventana.iconbitmap('icon.ico')
ventana.configure(background="white smoke")
color_boton=("white smoke")

#Ventana para mostrar las tablas
texto = Text(ventana)
texto.pack()
texto.place(x=370,y=75)
txt = scrolledtext.ScrolledText(texto,width=75,height=20)
txt.grid(column=0,row=0)


#reemplaza los datos que se vienen de los botones
def remplazar(expr):
    REPLACEMENTS = {
       '~': ' not ',
       'v': ' or ',
       '^': ' and ',

       '+': ' xor ',
       '->': ' nand ',
       '↔': ' is ',
       '[': '(',
       ']': ')',
       '{': '(',
       '}': ')',
    }
    return re.sub('|'.join(re.escape(sym) for sym in REPLACEMENTS.keys()),
                  lambda sym: REPLACEMENTS[sym.group(0)],
                  expr).strip()
#Estructura para poder guardar datos booleanos
class Nodo:
    __slots__ = 'etiqueta', 'hijos'

    def __init__(self, etiqueta, *hijos):
        self.etiqueta = etiqueta
        self.hijos = hijos


#Valida 0 y 1
def postorden(nodoraiz):
    pila, descubiertos = [nodoraiz], set()
    while pila:
        u = pila[-1]
        if u in descubiertos:
            yield u
            pila.pop()
        else:
            descubiertos.add(u)
            pila.extend(reversed(u.hijos)
                        )

#Valida si las operaciones cumplen 
def compilar(expresion):
    def nodificar(nodo):
        if isinstance(nodo, ast.BoolOp) and isinstance(nodo.op, ast.And):
            etiqueta = 'and'
            hijos = nodo.values
        elif isinstance(nodo, ast.BoolOp) and isinstance(nodo.op,ast.Or):
            etiqueta = 'or'
            hijos = nodo.values
        elif isinstance(nodo, ast.BoolOp) and isinstance(nodo.op,ast.Is):
            etiqueta = 'is'
            hijos = nodo.values
        elif isinstance(nodo, ast.UnaryOp) and isinstance(nodo.op, ast.Not):
            etiqueta = 'not'
            hijos = [nodo.operand]

        elif isinstance(nodo, ast.Name):
            etiqueta = nodo.id
            hijos = []
        else: raise RuntimeError(msj_error)
        return Nodo(etiqueta, *map(nodificar, hijos))
    msj_error = 'Expresión boolena no válida...'
    T = ast.parse(expresion, mode = 'eval')
    if not isinstance(T, ast.Expression): raise RuntimeError(msj_error)
    return nodificar(T.body)

## Evalua los  simbolos y los parentesis que tiene la expresion
def formula(nodo):
    if nodo.etiqueta == 'and':
        return '({})'.format(' ∧ '.join(map(formula, nodo.hijos)))
    elif nodo.etiqueta == 'or':
        return '({})'.format(' ∨ '.join(map(formula, nodo.hijos)))
    elif nodo.etiqueta == 'is':
        return '({})'.format('<->'.join(map(formula, nodo.hijos)))

    elif nodo.etiqueta == 'not':
        return '¬' + formula(nodo.hijos[0])

    else: return nodo.etiqueta


#Evalua el cirtuito para usarlos de manera que la maquina lo entienda 
def evaluar_circuito(nodoraiz, asignacion,):
    ev = dict()
    for nodo in postorden(nodoraiz):
        if nodo.etiqueta == 'and':
            s = 1
            for h in nodo.hijos:
                s = s and ev[h]
        elif nodo.etiqueta == 'or':
            s = 0
            for h in nodo.hijos:
                s = s or ev[h]
        elif nodo.etiqueta == 'is':
            s = 0
            for h in nodo.hijos:
                s = s is ev[h]
        elif nodo.etiqueta == 'not':
            s = not ev[nodo.hijos[0]]

        elif nodo.etiqueta in asignacion:
            s = asignacion[nodo.etiqueta]
        else: raise KeyError('No se pudo evaluar la compuerta {}'.format(nodo))
        ev[nodo] = int(s)
    return ev

#Cuenta los 0 y 1 que se usaran 
def contador_binario(n):
    d = [0]*n
    while True:
        yield tuple(d)
        j = n - 1
        while j >= 0:
            d[j] = 1 - d[j]
            if d[j] == 1: break
            j -= 1
        if j < 0: break

#Evalua las etiquetas usadas y los digitos que se usaran
def tabla_verdad(nodoraiz):
    variables, compuertas, formulas = set(), [], set()
    for u in postorden(nodoraiz):
        if u.etiqueta in ('and', 'or','xor','nand','is','not'):
            f = formula(u)
            if f not in formulas:
                formulas.add(f)
                compuertas.append(u)
        else: variables.add(u.etiqueta)
    variables = tuple(sorted(variables))
    yield variables + tuple(formula(u) for u in compuertas)
    for digitos in contador_binario(len(variables)):
        asignacion = dict(zip(variables, digitos))
        val = evaluar_circuito(nodoraiz, asignacion)
        yield digitos + tuple(val[c] for c in compuertas)


#Se encarga de imprimir las tablas con los datos que recibe de funciones atras
def imprimir_tabla(renglones):
    
    renglones = iter(renglones)
    encabezado = next(renglones)
    tam = tuple(map(len, encabezado))
    txt.insert(INSERT,('el resultado es:'+'\n'))
    txt.insert(INSERT,'    │ '.join(encabezado))
   
    for renglon in renglones:
        cadena = ""
        for i,valor in enumerate(renglon):
            if valor == 0:
                cadena += "F"
                
            else: 
                cadena += "V"
                
        txt.insert(INSERT,' \n'+'    │ '.join(str(cadena)))
    

#Condiciones
def main():
    if entrada1.get()=="p+q":
         abrirventana26()
    if entrada1.get()=="p+r":
         abrirventana27()
    if entrada1.get()=="p+s":
         abrirventana28()
    if entrada1.get()=="q+p":
         abrirventana29()
    if entrada1.get()=="q+r":
         abrirventana30()
    if entrada1.get()=="q+s":
         abrirventana31()
    if entrada1.get()=="r+q":
         abrirventana32()
    if entrada1.get()=="r+p":
         abrirventana33()
    if entrada1.get()=="r+s":
         abrirventana34()
    if entrada1.get()=="s+q":
         abrirventana35()
    if entrada1.get()=="s+p":
         abrirventana36()
    if entrada1.get()=="s+r":
         abrirventana37()
#-------- (->)
    if entrada1.get()=="p→q":
         abrirventana38()
    if entrada1.get()=="p→r":
         abrirventana39()
    if entrada1.get()=="p→s":
         abrirventana40()
    if entrada1.get()=="q→p":
         abrirventana41()
    if entrada1.get()=="q→r":
         abrirventana42()
    if entrada1.get()=="q→s":
         abrirventana43()
    if entrada1.get()=="r→q":
         abrirventana44()
    if entrada1.get()=="r→p":
         abrirventana45()
    if entrada1.get()=="r→s":
         abrirventana46()
    if entrada1.get()=="s→q":
         abrirventana47()
    if entrada1.get()=="s→p":
         abrirventana48()
    if entrada1.get()=="s→r":
         abrirventana49()
#---------  (<->)
    if entrada1.get()=="p↔q":
         abrirventana50()
    if entrada1.get()=="p↔r":
         abrirventana51()
    if entrada1.get()=="p↔s":
         abrirventana52()
    if entrada1.get()=="q↔p":
         abrirventana53()
    if entrada1.get()=="q↔r":
         abrirventana54()
    if entrada1.get()=="q↔s":
         abrirventana55()
    if entrada1.get()=="r↔q":
         abrirventana56()
    if entrada1.get()=="r↔p":
         abrirventana57()
    if entrada1.get()=="r↔s":
         abrirventana58()
    if entrada1.get()=="s↔q":
         abrirventana59()
    if entrada1.get()=="s↔p":
         abrirventana60()
    if entrada1.get()=="s↔r":
         abrirventana61()
    
    else:
        f = operador
        nodoraiz = compilar(remplazar(operador))
        imprimir_tabla(tabla_verdad(nodoraiz))
    

    

#Funcion para visualisar las letras en pantalla

def btnClik(letra):
    global operador
    input_text.set(input_text.get()+letra)
    operador=input_text.get()


def clear():
    global operador
    operador=("")
    input_text.set("")
    txt.delete('1.0', END)         #Se encarga de borrar los datos de la pantalla y la tablas
    
    
#Contiene los operadores
def operacion():
    global operador
    operador=input_text.get()
    main()
# Aqui cree las sentencias if donde llama a  una funcion y crea cada probabilidad que aparezca.
#Entonces una compleja no agarra, solamente sencillas. Se puden complejas pero igual abria que hacer todas las probabilidades.
#------- (+)



#Se muestran las funciones
def abrirventana26():

        txt.insert(INSERT,('                      Tabla\n'))
        txt.insert(INSERT,("P                      Q                       P+Q\n"))
        txt.insert(INSERT,("F                      F                       F\n"))
        txt.insert(INSERT,("F                      V                       V\n"))
        txt.insert(INSERT,("V                      F                       V\n"))
        txt.insert(INSERT,("V                      V                       V\n"))
        

def abrirventana27():      
        txt.insert(INSERT,"                     tabla\n")   
        txt.insert(INSERT,"P                      R                   P+R\n") 
        txt.insert(INSERT,"1                      1                     1\n")  
        txt.insert(INSERT,"1                      0                     0\n")   
        txt.insert(INSERT,"0                      1                     0\n")  
        txt.insert(INSERT,"0                      0                     1\n")
       

def abrirventana28():
        txt.insert(INSERT,"                     tabla\n")
        txt.insert(INSERT,"P                      S                   P+S\n")       
        txt.insert(INSERT,"1                      1                     1\n")
        txt.insert(INSERT,"1                      0                     0\n")       
        txt.insert(INSERT,"0                      1                     0\n")
        txt.insert(INSERT,"0                      0                     1\n")

def abrirventana29():
        txt.insert(INSERT,"                     Tabla\n")
        txt.insert(INSERT,"Q                      P                   Q+P\n")
        txt.insert(INSERT,"1                      1                     1\n")
        txt.insert(INSERT,"1                      0                     0\n")
        txt.insert(INSERT,"0                      1                     0\n")
        txt.insert(INSERT,"0                      0                     1\n")
      
def abrirventana30():
        txt.insert(INSERT,"                     Tabla\n")
        txt.insert(INSERT,"Q                      R                   Q+R\n")
        txt.insert(INSERT,"1                      1                     1\n")
        txt.insert(INSERT,"1                      0                     0\n")
        txt.insert(INSERT,"0                      1                     0\n")      
        txt.insert(INSERT,"0                      0                     1\n")
   
def abrirventana31():
        txt.insert(INSERT,"                      Tabla\n")
        txt.insert(INSERT,"Q                      S                   Q+S\n")
        txt.insert(INSERT,"1                      1                     1\n")
        txt.insert(INSERT,"1                      0                     0\n")
        txt.insert(INSERT,"0                      1                     0\n")
        txt.insert(INSERT,"0                      0                     1\n")
       
def abrirventana32():    
        txt.insert(INSERT,"                     Tabla\n")
        txt.insert(INSERT,"R                      Q                   R+Q\n")       
        txt.insert(INSERT,"1                      1                     1\n")
        txt.insert(INSERT,"1                      0                     0\n")
        txt.insert(INSERT,"0                      1                     0\n")
        txt.insert(INSERT,"0                      0                     1\n")
 
def abrirventana33():   
        txt.insert(INSERT,"                     Tabla\n")   
        txt.insert(INSERT,"R                      P                   R+P\n")
        txt.insert(INSERT,"1                      1                     1\n")     
        txt.insert(INSERT,"1                      0                     0\n")
        txt.insert(INSERT,"0                      1                     0\n")      
        txt.insert(INSERT,"0                      0                     1\n")
       
def abrirventana34():
        txt.insert(INSERT,"                     Tabla\n")  
        txt.insert(INSERT,"R                      S                   R+S\n")
        txt.insert(INSERT,"1                      1                     1\n")       
        txt.insert(INSERT,"1                      0                     0\n")
        txt.insert(INSERT,"0                      1                     0\n")       
        txt.insert(INSERT,"0                      0                     1\n")

def abrirventana35():
        txt.insert(INSERT,"                     Tabla\n")      
        txt.insert(INSERT,"S                      Q                   S+Q\n")
        txt.insert(INSERT,"1                      1                     1\n")
        txt.insert(INSERT,"1                      0                     0\n")
        txt.insert(INSERT,"0                      1                     0\n")     
        txt.insert(INSERT,"0                      0                     1\n")

def abrirventana36():
        txt.insert(INSERT,"                     Tabla\n")      
        txt.insert(INSERT,"S                      P                   S+P\n")
        txt.insert(INSERT,"1                      1                     1\n")   
        txt.insert(INSERT,"1                      0                     0\n")      
        txt.insert(INSERT,"0                      1                     0\n")
        txt.insert(INSERT,"0                      0                     1\n")
        

def abrirventana37():
       
         txt.insert(INSERT,"                   Tabla\n")
         txt.insert(INSERT,"S                      R                   S+R\n")    
         txt.insert(INSERT,"1                      1                     1\n")      
         txt.insert(INSERT,"1                      0                     0\n")       
         txt.insert(INSERT,"0                      1                     0\n")  
         txt.insert(INSERT,"0                      0                     1\n")
       
#-----------  (->)
def abrirventana38():
         txt.insert(INSERT,"                    Tabla\n")
         txt.insert(INSERT,"P                      Q                   P→Q\n")       
         txt.insert(INSERT,"1                      1                     0\n")
         txt.insert(INSERT,"1                      0                     0\n")       
         txt.insert(INSERT,"0                      1                     1\n")   
         txt.insert(INSERT,"0                      0                     0\n")
      
def abrirventana39():
        txt.insert(INSERT,"                      Tabla\n")    
        txt.insert(INSERT,"P                      R                   P→R\n")     
        txt.insert(INSERT,"1                      1                     0\n")
        txt.insert(INSERT,"1                      0                     0\n")
        txt.insert(INSERT,"0                      1                     1\n")   
        txt.insert(INSERT,"0                      0                     0\n")

def abrirventana40():
         txt.insert(INSERT,"                    Tabla\n")
         txt.insert(INSERT,"P                      S                   P→S\n")       
         txt.insert(INSERT,"1                      1                     0\n")
         txt.insert(INSERT,"1                      0                     0\n")       
         txt.insert(INSERT,"0                      1                     1\n")
         txt.insert(INSERT,"0                      0                     0\n")
      

def abrirventana41():

        txt.insert(INSERT,"                     Tabla\n")
        txt.insert(INSERT,"Q                      P                   Q→P\n")
        txt.insert(INSERT,"1                      1                     0\n")       
        txt.insert(INSERT,"1                      0                     0\n")
        txt.insert(INSERT,"0                      1                     1\n")   
        txt.insert(INSERT,"0                      0                     0\n")


def abrirventana42():

        txt.insert(INSERT,"                    Tabla\n")
        txt.insert(INSERT,"Q                      R                   Q→R\n")
        txt.insert(INSERT,"1                      1                     0\n")      
        txt.insert(INSERT,"1                      0                     0\n")
        txt.insert(INSERT,"0                      1                     1\n")        
        txt.insert(INSERT,"0                      0                     0\n")

def abrirventana43():

        txt.insert(INSERT,"                    Tabla\n")      
        txt.insert(INSERT,"Q                      S                   Q→S\n") 
        txt.insert(INSERT,"1                      1                     0\n")       
        txt.insert(INSERT,"1                      0                     0\n")
        txt.insert(INSERT,"0                      1                     1\n")       
        txt.insert(INSERT,"0                      0                     0\n")

def abrirventana44():

         txt.insert(INSERT,"                      Tabla\n")
         txt.insert(INSERT,"R                      Q                   R→Q\n")     
         txt.insert(INSERT,"1                      1                     0\n")
         txt.insert(INSERT,"1                      0                     0\n")      
         txt.insert(INSERT,"0                      1                     1\n")
         txt.insert(INSERT,"0                      0                     0\n")
       
def abrirventana45():

        txt.insert(INSERT,"                    Tabla\n")       
        txt.insert(INSERT,"R                      P                   R→P\n")
        txt.insert(INSERT,"1                      1                     0\n")      
        txt.insert(INSERT,"1                      0                     0\n")       
        txt.insert(INSERT,"0                      1                     1\n")   
        txt.insert(INSERT,"0                      0                     0\n")
       
def abrirventana46():
        txt.insert(INSERT,"                     Tabla\n")
        txt.insert(INSERT,"R                      S                   R→S\n")
        txt.insert(INSERT,"1                      1                     0\n")
        txt.insert(INSERT,"1                      0                     0\n")
        txt.insert(INSERT,"0                      1                     1\n")
        txt.insert(INSERT,"0                      0                     0\n")

def abrirventana47():
        txt.insert(INSERT,"                     Tabla\n")
        txt.insert(INSERT,"S                      Q                   S→Q\n")
        txt.insert(INSERT,"1                      1                     0\n")
        txt.insert(INSERT,"1                      0                     0\n")
        txt.insert(INSERT,"0                      1                     1\n")
        txt.insert(INSERT,"0                      0                     0\n")

def abrirventana48():
        txt.insert(INSERT,"                     Tabla\n")
        txt.insert(INSERT,"S                      P                   S→P\n")
        txt.insert(INSERT,"1                      1                     0\n")
        txt.insert(INSERT,"1                      0                     0\n")
        txt.insert(INSERT,"0                      1                     1\n")
        txt.insert(INSERT,"0                      0                     0\n")

def abrirventana49():
        txt.insert(INSERT,"                     Tabla\n")
        txt.insert(INSERT,"S                      R                   S→R\n")
        txt.insert(INSERT,"1                      1                     0\n")
        txt.insert(INSERT,"1                      0                     0\n")
        txt.insert(INSERT,"0                      1                     1\n")   
        txt.insert(INSERT,"0                      0                     0\n")

#----------  (<->)
def abrirventana50():   
        txt.insert(INSERT,"                    Tabla\n")
        txt.insert(INSERT,"P                      Q                   P↔Q\n")
        txt.insert(INSERT,"1                      1                     0\n")
        txt.insert(INSERT,"1                      0                     1v")
        txt.insert(INSERT,"0                      1                     1\n")
        txt.insert(INSERT,"0                      0                     0\n")

def abrirventana51():
        txt.insert(INSERT,"                     Tabla\n")
        txt.insert(INSERT,"P                      R                   P↔R\n")
        txt.insert(INSERT,"1                      1                     0\n")
        txt.insert(INSERT,"1                      0                     1\n")
        txt.insert(INSERT,"0                      1                     1\n")
        txt.insert(INSERT,"0                      0                     0\n")


def abrirventana52():
        txt.insert(INSERT,"                    Tabla\n")
        txt.insert(INSERT,"P                      S                   P↔S\n")
        txt.insert(INSERT,"1                      1                     0\n")   
        txt.insert(INSERT,"1                      0                     1\n")
        txt.insert(INSERT,"0                      1                     1\n")
        txt.insert(INSERT,"0                      0                     0\n")

def abrirventana53():
        txt.insert(INSERT,"                     Tabla\n")
        txt.insert(INSERT,"Q                      P                   Q↔P\n")
        txt.insert(INSERT,"1                      1                     0\n")
        txt.insert(INSERT,"1                      0                     1\n")
        txt.insert(INSERT,"0                      1                     1\n")
        txt.insert(INSERT,"0                      0                     0\n")


def abrirventana54():
        txt.insert(INSERT,"                     Tabla\n")
        txt.insert(INSERT,"Q                      R                   Q↔R\n")
        txt.insert(INSERT,"1                      1                     0\n")
        txt.insert(INSERT,"1                      0                     1\n")
        txt.insert(INSERT,"0                      1                     1\n")
        txt.insert(INSERT,"0                      0                     0\n")

def abrirventana55():
        txt.insert(INSERT,"                      Tabla\n")
        txt.insert(INSERT,"Q                      S                   Q↔S\n")
        txt.insert(INSERT,"1                      1                     0\n")
        txt.insert(INSERT,"1                      0                     1\n")
        txt.insert(INSERT,"0                      1                     1\n")
        txt.insert(INSERT,"0                      0                     0\n")

def abrirventana56():
        txt.insert(INSERT,"                     Tabla\n")
        txt.insert(INSERT,"R                      Q                   R↔Q\n")
        txt.insert(INSERT,"1                      1                     0\n")
        txt.insert(INSERT,"1                      0                     1\n")
        txt.insert(INSERT,"0                      1                     1\n")
        txt.insert(INSERT,"0                      0                     0\n")

def abrirventana57():
        txt.insert(INSERT,"                    Tabla\n")
        txt.insert(INSERT,"R                      P                   R↔P\n")
        txt.insert(INSERT,"1                      1                     0\n")
        txt.insert(INSERT,"1                      0                     1\n")
        txt.insert(INSERT,"0                      1                     1\n")
        txt.insert(INSERT,"0                      0                     0\n")

def abrirventana58():
        txt.insert(INSERT,"                     Tabla\n")
        txt.insert(INSERT,"R                      S                   R↔S\n")
        txt.insert(INSERT,"1                      1                     0\n")
        txt.insert(INSERT,"1                      0                     1\n")
        txt.insert(INSERT,"0                      1                     1\n")
        txt.insert(INSERT,"0                      0                     0\n")

def abrirventana59():
        txt.insert(INSERT,"                     Tabla\n")
        txt.insert(INSERT,"S                      Q                   S↔Q\n")
        txt.insert(INSERT,"1                      1                     0\n")
        txt.insert(INSERT,"1                      0                     1\n")
        txt.insert(INSERT,"0                      1                     1\n")
        txt.insert(INSERT,"0                      0                     0\n")

def abrirventana60():

        txt.insert(INSERT,"                     Tabla\n")
        txt.insert(INSERT,"S                      P                   S↔P\n")
        txt.insert(INSERT,"1                      1                     0\n")
        txt.insert(INSERT,"1                      0                     1\n")     
        txt.insert(INSERT,"0                      1                     1\n")
        txt.insert(INSERT,"0                      0                     0\n")

def abrirventana61():
        txt.insert(INSERT,"                     Tabla\n")
        txt.insert(INSERT,"S                      R                   S↔R")
        txt.insert(INSERT,"1                      1                     0") 
        txt.insert(INSERT,"1                      0                     1")  
        txt.insert(INSERT,"0                      1                     1")    
        txt.insert(INSERT,"0                      0                     0")

##################################OPERACIONES CORTAS



    
    
        


#Datos prestablecidos 
ancho_boton=11
alto_boton=3
input_text=StringVar()
operador=""

#Diseño de la interfaz
AC = PhotoImage(file='Buttons/AC.png')
DEL = PhotoImage(file='Buttons/DEL.png')
igual = PhotoImage(file='Buttons/igual.png')
igual2 = PhotoImage(file='Buttons/igual2.png')

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

#Interfaz de la calculadora
BotonP=Button(      ventana,          image=simplep,            border='0',             command=lambda:btnClik("p")).place(x=17,y=240)
BotonQ=Button(      ventana,          image=simpleq,            border='0',            bg=color_boton,command=lambda:btnClik("q")).place(x=107,y=240)
BotonR=Button(      ventana,          image=simpler,            border='0',            bg=color_boton,command=lambda:btnClik("r")).place(x=197,y=240)
BotonS=Button(      ventana,          image=simples,            border='0',            bg=color_boton,command=lambda:btnClik("s")).place(x=267,y=240)
BotonNot=Button(    ventana,          image=negacion,           border='0',            bg=color_boton,command=lambda:btnClik("~")).place(x=17,y=300)
BotonY=Button(      ventana,          image=conjuncion,         border='0',            bg=color_boton,command=lambda:btnClik("^")).place(x=107,y=300)
BotonV=Button(      ventana,          image=disyuncion,         border='0',            bg=color_boton,command=lambda:btnClik("v")).place(x=197,y=300)
BotonIf=Button(     ventana,          image=condicional,        border='0',            bg=color_boton,command=lambda:btnClik("→")).place(x=267,y=300)
BotonBi=Button(     ventana,          image=bicondicional,      border='0',            bg=color_boton,command=lambda:btnClik("↔")).place(x=17,y=360)
BotonMas=Button(    ventana,          image=XOR,                border='0',            bg=color_boton,command=lambda:btnClik("+")).place(x=107,y=360)
BotonParen1=Button( ventana,          image=par1,               border='0',            bg=color_boton,command=lambda:btnClik("(")).place(x=197,y=360)
BotonParen2=Button( ventana,          image=par2,               border='0',            bg=color_boton,command=lambda:btnClik(")")).place(x=267,y=360)
BotonC=Button(      ventana,          image=AC,                 border='0',            bg=color_boton,command=clear).place(x=17,y=180)
BotonC1=Button(     ventana,          image=DEL,                border='0',            bg=color_boton,command=clear).place(x=107,y=180)

#Operador 
BotonResul=Button(  ventana,            image=igual,              border='0', bg=color_boton,command=operacion).place(x=197,y=180)

#Botontablas=Button(  ventana,   text='Circuitos logicos', bg=color_boton,state= DISABLED,command=clear).place(x=675,y=49)
#Botontablas=Button(  ventana,   text='Tablas de verdad',border= "0", bg=color_boton, state= DISABLED,command=clear).place(x=550,y=49)

#Muestran los valores en pantalla
Salida=Entry(ventana,font=('arial',20,'bold'),width=18,textvariable=input_text,bd=7,insertwidth=8,bg="light gray",justify="right").place(x=35,y=75)
entrada1=Entry(ventana,textvariable=input_text,bg="white")
entrada1.pack(fill=tk.X,padx=10,pady=10,ipadx=10,ipady=10)




ventana.mainloop()
