import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import ctypes               # Para Windows
import subprocess           # Para Unix/Linux
from sys import platform    # Identificar el sistema operativo
import os
import glob
from datetime import datetime

from fpdf import FPDF
from PIL import Image
from PyPDF2 import PdfFileMerger


# Función "Almc" - Será mostrada un ventana emergente en la cual deberá indicar la ruta en la cual deberá ser almacenado el archivo PDF
def Almc():
    Ruta.set(filedialog.askdirectory())

# Función "AlmacenarPDF" - Será mostrada un ventana emergente en la cual deberá proporcionar el nombre y la ruta en la cual debera ser almacenado el archivo PDF
def AlmacenarPDF():
    if Archs[0] != 0:
        global SubVent, Nomb, Ruta

        SubVent2 = tk.Toplevel(SubVent)
        SubVent2.grab_set()
        SubVent2.resizable(False, False)
        SubVent2.title(' - Almacenamiento de archivo PDF - ')
        SubVent2.geometry(str(Vent[2])+'x'+str(Vent[3])+'+'+str(Vent[4])+'+'+str(Vent[5]))
        SubVent2.config(bg = '#cdf2ff', bd = 8, relief = 'groove')
        SubVent2.grid_columnconfigure(0, weight = 2, uniform = 'fig')
        
        Nomb = tk.StringVar(SubVent2)
        Ruta = tk.StringVar(SubVent2)
        Ruta.set(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))

        color_fondo = '#cdf2ff'
        color_text = 'black'

        Secc = tk.LabelFrame(SubVent2, bd = 3, text = ' Almacenamiento del archivo PDF ', bg = color_fondo, fg = color_text, font = ('Microsoft YaHei UI',Vent[6],'bold'))
        Secc.grid_columnconfigure(0, weight = 1, uniform = 'fig')

        Etiq = tk.Label(Secc, text = ' > Nombre del archivo: ', bg = color_fondo, fg = color_text, font = ('Microsoft YaHei UI',Vent[6]+1,'bold'))
        Opc1 = tk.Entry(Secc, textvariable = Nomb, relief = tk.RIDGE, borderwidth = 2, cursor = 'xterm', bg = 'white', fg = 'black', font = ('Arial',Vent[6],' italic '))
        
        Etiq2 = tk.Label(Secc, text = ' > Ubicación donde será almacenado: ', bg = color_fondo, fg = color_text, font = ('Microsoft YaHei UI',Vent[6]+1,'bold'))
        Opc2 = tk.Entry(Secc, textvariable = Ruta, state="readonly", relief = tk.RIDGE, borderwidth = 2, cursor = 'arrow', bg = color_fondo, fg = 'black', font = ('Arial',Vent[6],' italic '))
        
        Buscar = tk.Button(Secc, text = ' Seleccionar Ubicación ', command = Almc, relief = tk.RIDGE, activebackground = 'white', borderwidth = 3, cursor = 'hand2', bg = '#f9f9a1', fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'))
        Acept = tk.Button(Secc, text = ' Aceptar ', command = ConvertPDF, relief = tk.RIDGE, activebackground = 'white', borderwidth = 3, cursor = 'hand2', bg = '#c3ffce', fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'))

        Secc.grid(column = 0, row = 0, padx = (5,5), pady = (15, 15), sticky = 'nsew', columnspan = 2)
        
        Etiq.grid(column = 0, row = 0, padx = (5,5), pady = (5, 1), sticky = 'w', columnspan = 2)
        Opc1.grid(column = 0, row = 1, padx = (5,5), pady = (1, 5), sticky = 'nsew', columnspan = 2)
        Etiq2.grid(column = 0, row = 2, padx = (5,5), pady = (5,1), sticky = 'w', columnspan = 2)
        Opc2.grid(column = 0, row = 3, padx = (5,5), pady = (1,5), sticky = 'nsew', columnspan = 2)
        Buscar.grid(column = 0, row = 4, padx = (5,5), pady = (1,5), sticky = 'nsew')
        Acept.grid(column = 1, row = 4, padx = (5,5), pady = (3,5), sticky = 'nsew')

# Función "CovertPDF" - Realizará la conversión de las Imágenes proporcionadas a un archivo PDF ó la fusión de otros archivos PDF
def ConvertPDF():
    if Archs[0] != 0:
        NombArch = Nomb.get()
        RutaDestino = Ruta.get()

        if not NombArch:
            F = datetime.now()
            NombArch = 'Resultado_'+str(F.hour)+'_'+str(F.minute)+'_'+str(F.second)

        if Vent[13] == 1:
            # --- Imgs a PDF

            # ___ Lista que almacenará las imagenes extraídas
            Imgs = []

            # Extración de las imagenes de la rutas previamente obtenidas
            for i in range(Archs[0]):
                Imgs.append(Image.open(Archs[i+1]))

                '''
                # Conversión de imágenes PNG a JPG
                path, nomb = os.path.split(Archs[i+1])
                TipoImg = nomb[nomb.find('.'):len(nomb)]

                if TipoImg == '.jpg':
                    # Extración de las imagenes
                    print(' -- Extrayendo imagen de: '+Archs[i+1])
                    Imgs.append(Image.open(Archs[i+1]))
                else:
                    # Extración de las imagenes
                    print(' -- Extrayendo imagen de: '+Archs[i+1])
                    img = Image.open(Archs[i+1])
                    print(' -- Conviertiendo a JPG')
                    img.convert('RGB')
                    Imgs.append(img)
                '''
            # _________________________ Creación del archivo PDF
            pdf = FPDF('P','mm','A4')

            for i in range(Archs[0]):
                # Extracción de ancho y largo de la Imagen "i"
                w, h = Imgs[i].size
                
                if w < h:
                    #Vertical
                    pdf.add_page('P')
                    pdf.image(Archs[i+1],0,0,210,297)
                else:
                    #Horizontal
                    pdf.add_page('L')
                    pdf.image(Archs[i+1],0,0,297,210)

                Info.configure(text = ' Hoja '+str(i)+' de '+str(Archs[0]))

            pdf.output(RutaDestino+'/'+NombArch+".pdf", "F")
        else:
            # --- PDFs a PDF

            NombArchSalida = RutaDestino+'/'+NombArch+'.pdf'
            fusionador = PdfFileMerger()

            for i in range(Archs[0]):
                fusionador.append(open(Archs[i+1], 'rb'))
            
            fusionador.write(open(NombArchSalida, 'wb'))
                        
        Info.configure(text = ' ¡Listo! Su archivo PDF: '+NombArch+' se encuentra en '+RutaDestino)

# ____________________________________________________________________________ Acciones en la tabla
# Función "VaciarTabl" - Elimina todos los items de la tabla...
def VaciarTabl():
    Archs.clear()
    Archs.append(0)
    
    Tabla.delete(*Tabla.get_children())

    if Vent[13] == 1:
        NumImgs.configure(text = ' Puedes ingresar un máximo de 50 imágenes...')
        ElimImg.configure(state=tk.DISABLED, cursor = 'arrow')
        SubirImgs.configure(state=tk.NORMAL, cursor = 'hand2')
    else:
        NumArchs.configure(text = ' Puedes ingresar un máximo de 50 archivos...')
        ElimArch.configure(state=tk.DISABLED, cursor = 'arrow')
        SubirArchs.configure(state=tk.NORMAL, cursor = 'hand2')

    VaciarTbl.configure(state=tk.DISABLED, cursor = 'arrow')
    MovArriba.configure(state=tk.DISABLED, cursor = 'arrow')
    MovAbajo.configure(state=tk.DISABLED, cursor = 'arrow')
    Convert.configure(state=tk.DISABLED, cursor = 'arrow')

# Función "MovArr" - Mueve al item seleccionado una posición arriba
def MovArr():
    global Tabla
    # Obteniendo ID del elemnto de la tabla seleccionado
    Elemt = Tabla.focus()

    if Elemt:
        Elemt = int(Elemt)
        if Elemt != 1:
            aux = Archs[Elemt]
            Archs[Elemt] = Archs[Elemt-1]
            Archs[Elemt-1] = aux

            Tabla.delete(*Tabla.get_children())

            for i in range(Archs[0]):
                path, nomb = os.path.split(Archs[i+1])
                Tabla.insert(parent = '', index=(i+1), iid=(i+1), values=((i+1),nomb,path))
            Tabla.selection_set(str(Elemt-1))
            Tabla.focus(str(Elemt-1))

# Función "MovAbj" - Mueve al item seleccionado una posición abajo
def MovAbj():
    # Obteniendo ID del elemnto de la tabla seleccionado
    Elemt = Tabla.focus()

    if Elemt:
        Elemt = int(Elemt)
        if Elemt != Archs[0]:
            aux = Archs[Elemt]
            Archs[Elemt] = Archs[Elemt+1]
            Archs[Elemt+1] = aux

            Tabla.delete(*Tabla.get_children())

            for i in range(Archs[0]):
                path, nomb = os.path.split(Archs[i+1])
                Tabla.insert(parent = '', index=(i+1), iid=(i+1), values=((i+1),nomb,path))
            
            Tabla.selection_set(str(Elemt+1))
            Tabla.focus(str(Elemt+1))

# Función "ElimElmt" - Elimina el item seleccionado de la tabla y posteriormente actualiza la información de la tabla...
def ElimElmt():
    # Obteniendo ID del elemnto de la tabla seleccionado
    Elemt = Tabla.focus()

    if Elemt:
        Archs[0] -= 1
        Archs.pop(int(Elemt))
        Tabla.delete(*Tabla.get_children())

        for i in range(Archs[0]):
            path, nomb = os.path.split(Archs[i+1])
            Tabla.insert(parent = '', index=(i+1), iid=(i+1), values=((i+1),nomb,path))
                
        if Archs[0] == 0:
            if Vent[13] == 1:
                NumArchs.configure(text = ' Puedes ingresar un máximo de '+str(50 - Archs[0])+' archivos...')
                SubirImgs.configure(state=tk.NORMAL, cursor = 'hand2')
                ElimImg.configure(state=tk.DISABLED, cursor = 'arrow')
            else:
                NumArchs.configure(text = ' Puedes ingresar un máximo de '+str(50 - Archs[0])+' archivos...')
                SubirArchs.configure(state=tk.NORMAL, cursor = 'hand2')
                ElimArch.configure(state=tk.DISABLED, cursor = 'arrow')

            MovArriba.configure(state=tk.DISABLED, cursor = 'arrow')
            MovAbajo.configure(state=tk.DISABLED, cursor = 'arrow')
            Convert.configure(state=tk.DISABLED, cursor = 'arrow')

# ____________________________________________________________________________ Conversión de Imgs a PDF
# Función "Imgs_PDF" - Dezpliega en la pantalla la ventana encargada del control de las imagenes a convertir
def Imgs_PDF():
    # Conversión de imgs a pdf
    Vent[13] = 1

    # Vaciando lista de archivos...
    Archs.clear()
    Archs.append(0)

    global SubVent, NumImgs, Info, Tabla, VaciarTbl, ElimImg, MovArriba, MovAbajo, Convert, SubirImgs
    
    color_fondo = '#ffdfb5'
    color_text = 'white'

    SubVent = tk.Toplevel(raiz)
    SubVent.grab_set()
    SubVent.title(' Conversor de PDFs - Opción: Imgs a PDF ')
    SubVent.resizable(False, False)
    SubVent.config(bg = color_fondo, bd = 8, relief = 'groove')
    SubVent.geometry(str(Vent[7])+'x'+str(Vent[8])+'+'+str(Vent[9])+'+'+str(Vent[10]))
    SubVent.grid_columnconfigure(0, weight = 1, uniform = 'fig')
    SubVent.grid_columnconfigure(1, weight = 1, uniform = 'fig')
    SubVent.grid_columnconfigure(2, weight = 1, uniform = 'fig')

    SubMenu = tk.LabelFrame(SubVent, relief = 'groove', bd = 7, text = ' - Conversión de imágenes a un archivo PDF - ', bg = color_fondo, fg = '#902626', font = ('Microsoft YaHei UI',Vent[6],'bold'))
    SubMenu.grid_columnconfigure(0, weight = 1, uniform = 'fig')
    SubMenu.grid_columnconfigure(1, weight = 1, uniform = 'fig')
    SubMenu.grid_columnconfigure(2, weight = 1, uniform = 'fig')
    SubMenu.grid_columnconfigure(3, weight = 1, uniform = 'fig')

    SubMenu.grid(column = 0, row = 0, padx = (10,10), pady = (5,5), columnspan = 3, sticky = 'new')

    Etiqueta2 = tk.Label(SubMenu, justify='left', text = ' Seleccione las imágenes que desea convertir a PDF. Posteriormente en la\n siguiente tabla será mostrada la información de cada imagen.', bg = color_fondo, fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'))
    SubirImgs = tk.Button(SubMenu, text = ' Seleccionar imagen(es) ', cursor = 'hand2', bg = '#fcf5d0', fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'), command=SeleccImgs)
    Tabla = ttk.Treeview(SubMenu, columns = (1,2,3), show = 'headings', height = 6)
    
    Tabla.column('#0', stretch = False)
    Tabla.column(1, width = Vent[12], minwidth = Vent[12], stretch = False)
    Tabla.column(2, width = (Vent[12]*10), minwidth = (Vent[12]*10), stretch = False)
    Tabla.column(3, width = (Vent[12]*10+5), minwidth = (Vent[12]*10+5), stretch = False)

    Barra = tk.Scrollbar(SubMenu, orient = tk.VERTICAL)
    Tabla.config(yscrollcommand = Barra.set)
    Barra.config(command = Tabla.yview)

    Tabla.heading(1, text = 'No.')
    Tabla.heading(2, text = 'Nombre de la imagen (.formato)')
    Tabla.heading(3, text = 'Ubicación del archivo')
    
    NumImgs = tk.Label(SubMenu, justify = 'left', text = ' Puede ingresar un máximo de 50 imágenes... ', bg = color_fondo, fg = '#902626', font = ('Arial',Vent[6],'bold italic'))
    
    CtrlInfoTbl = tk.LabelFrame(SubVent, relief = 'groove', bd = 7, text = ' - Movimientos a la información en la tabla - ', bg = color_fondo, fg = '#902626', font = ('Microsoft YaHei UI',Vent[6],'bold'))
    CtrlInfoTbl.grid_columnconfigure(0, weight = 1, uniform = 'fig')
    CtrlInfoTbl.grid_columnconfigure(1, weight = 1, uniform = 'fig')
    
    VaciarTbl = tk.Button(CtrlInfoTbl, state=tk.DISABLED, text = ' Vaciar Tabla ', bg = '#febf97', fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'), command = VaciarTabl)
    ElimImg = tk.Button(CtrlInfoTbl, state=tk.DISABLED, text = ' Quitar elemento de la Tabla ', bg = '#ffb0b0', fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'), command = ElimElmt)
    Etiqueta4 = tk.Label(CtrlInfoTbl, text = ' Si desea cambiar la posición (No.) de una imagen. Seleccionala\n en la tabla y usa los siguientes botones para cambiar su posición:', justify = 'left', bg = color_fondo, fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'))
    MovArriba = tk.Button(CtrlInfoTbl,state=tk.DISABLED, text = ' ▲ ', bg = '#d2d2fe', fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'), command = MovArr)
    MovAbajo = tk.Button(CtrlInfoTbl,state=tk.DISABLED, text = ' ▼ ', bg = '#d2d2fe', fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'), command = MovAbj)

    Convert = tk.Button(SubVent, state=tk.DISABLED, text = ' Convertir imagen(es) a\n un archivo PDF ', bg = '#c3ffce', fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'), command = AlmacenarPDF)
    Info = tk.Label(SubVent, justify = 'left', bg = 'black', fg = 'white', font = ('Arial',Vent[6],'bold italic'))
    
    Etiqueta2.grid(column = 0, row = 0, padx = (10,10), pady = (7,1), columnspan = 3, sticky = 'nsew')
    SubirImgs.place(x = Vent[11], y = 10)

    Tabla.grid(column = 0, row = 1, padx = (10,10), pady = (10,2), columnspan = 4, sticky = 'nsew')
    Barra.grid(column = 4, row = 1, padx = (10,10), pady = (10,2), sticky = 'nsew')
   
    NumImgs.grid(column = 0, row = 2, padx = (10,10), pady = (1,5), columnspan = 4, sticky = 'nsew')
    
    CtrlInfoTbl.grid(column = 0, row = 1, padx = (10,10), pady = (2,5), columnspan = 2, sticky = 'nsew')
    VaciarTbl.grid(column = 0, row = 0, padx = (10,10), pady = (5,5), sticky = 'nsew')
    ElimImg.grid(column = 1, row = 0, padx = (10,10), pady = (5,5), sticky = 'nsew')
    Etiqueta4.grid(column = 0, row = 1, padx = (10,10), pady = (5,5), columnspan = 2, sticky = 'nsew')
    MovArriba.grid(column = 0, row = 2, padx = (10,10), pady = (5,13), sticky = 'nsew')
    MovAbajo.grid(column = 1, row = 2, padx = (10,10), pady = (5,13), sticky = 'nsew')

    Convert.grid(column = 2, row = 1, padx = (10,10), pady = (5,5), sticky = 'nsew')
    Info.grid(column = 0, row = 2, padx = (10,10), pady = (1,5), columnspan = 3, sticky = 'nsew')

# Función "SeleccImgs" - Selección de la imágenes a convertir
def SeleccImgs():
    if Archs[0] < 50:
        Imgs = filedialog.askopenfilenames(title = "Elige tu(s) archivo(s): ", filetypes = (('Imágenes JNG', '*.jpg'),('Imágenes PNG', '*.png')))
        if Imgs:
            i = Archs[0]
            if i != 50:
                for Img in Imgs:
                    Archs.append(Img)
                    i += 1
                    path,nomb = os.path.split(Img)
                    Tabla.insert(parent = '', index=i, iid=i, values=(i,nomb,path))
                    
                    if i == 50:
                        break

                Archs[0] = i;

                if i != 50:
                    NumImgs.configure(text = ' Puedes ingresar un máximo de '+str(50 - Archs[0])+' imágenes...')
                else:
                    SubirImgs.configure(state=tk.DISABLED, cursor = 'arrow')
                    NumImgs.configure(text = ' Ya no es posible ingresar más imágenes...')

                VaciarTbl.configure(state=tk.NORMAL, cursor = 'hand2')
                ElimImg.configure(state=tk.NORMAL, cursor = 'hand2')
                MovArriba.configure(state=tk.NORMAL, cursor = 'hand2')
                MovAbajo.configure(state=tk.NORMAL, cursor = 'hand2')
                Convert.configure(state=tk.NORMAL, cursor = 'hand2')
            else:
                SubirImgs.configure(state=tk.DISABLED, cursor = 'arrow')
                NumImgs.configure(text = ' Ya no es posible ingresar más imágenes...')

# ____________________________________________________________________________ Conversión de PDFs a PDF
# Función "PDFs_PDF" - Dezpliega en la pantalla la ventana encargada del control de los archivos PDF a convertir
def PDFs_PDF():
    # Conversión de PDFs a uno solo
    Vent[13] = 2 

    # Vaciando lista de archivos...
    Archs.clear()
    Archs.append(0)

    global SubVent, NumArchs, Info, Tabla, VaciarTbl, ElimArch, MovArriba, MovAbajo, Convert, SubirArchs
    
    color_fondo = '#ffffd2'
    color_text = 'white'

    SubVent = tk.Toplevel(raiz)
    SubVent.grab_set()
    SubVent.title(' Conversor de PDFs - Opción: PDFs a PDF ')
    SubVent.resizable(False, False)
    SubVent.config(bg = color_fondo, bd = 8, relief = 'groove')
    SubVent.geometry(str(Vent[7])+'x'+str(Vent[8])+'+'+str(Vent[9])+'+'+str(Vent[10]))
    SubVent.grid_columnconfigure(0, weight = 1, uniform = 'fig')
    SubVent.grid_columnconfigure(1, weight = 1, uniform = 'fig')
    SubVent.grid_columnconfigure(2, weight = 1, uniform = 'fig')

    SubMenu = tk.LabelFrame(SubVent, relief = 'groove', bd = 7, text = ' - Conversión de archivos PDF a un solo archivo - ', bg = color_fondo, fg = '#00104d', font = ('Microsoft YaHei UI',Vent[6],'bold'))
    SubMenu.grid_columnconfigure(0, weight = 1, uniform = 'fig')
    SubMenu.grid_columnconfigure(1, weight = 1, uniform = 'fig')
    SubMenu.grid_columnconfigure(2, weight = 1, uniform = 'fig')
    SubMenu.grid_columnconfigure(3, weight = 1, uniform = 'fig')

    SubMenu.grid(column = 0, row = 0, padx = (10,10), pady = (5,5), columnspan = 3, sticky = 'new')

    Etiqueta2 = tk.Label(SubMenu, justify='left', text = ' Seleccione los archivos PDF que desea convertir a uno solo. Posteriormente \n en la siguiente tabla será mostrada la información de cada archivo.', bg = color_fondo, fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'))
    SubirArchs = tk.Button(SubMenu, text = ' Seleccionar archivos ', cursor = 'hand2', bg = '#ceefff', fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'), command = SeleccArch)
    Tabla = ttk.Treeview(SubMenu, columns = (1,2,3), show = 'headings', height = 6)
    
    Tabla.column('#0', stretch = False)
    Tabla.column(1, width = Vent[12], minwidth = Vent[12], stretch = False)
    Tabla.column(2, width = (Vent[12]*10), minwidth = (Vent[12]*10), stretch = False)
    Tabla.column(3, width = (Vent[12]*10+5), minwidth = (Vent[12]*10+5), stretch = False)

    Barra = tk.Scrollbar(SubMenu, orient = tk.VERTICAL)
    Tabla.config(yscrollcommand = Barra.set)
    Barra.config(command = Tabla.yview)

    Tabla.heading(1, text = 'No.')
    Tabla.heading(2, text = 'Nombre del archivo (.pdf)')
    Tabla.heading(3, text = 'Ubicación del archivo')
    
    NumArchs = tk.Label(SubMenu, justify = 'left', text = ' Puede ingresar un máximo de 50 archivos... ', bg = color_fondo, fg = '#00104d', font = ('Arial',Vent[6],'bold italic'))
    
    CtrlInfoTbl = tk.LabelFrame(SubVent, relief = 'groove', bd = 7, text = ' - Movimientos a la información en la tabla - ', bg = color_fondo, fg = '#00104d', font = ('Microsoft YaHei UI',Vent[6],'bold'))
    CtrlInfoTbl.grid_columnconfigure(0, weight = 1, uniform = 'fig')
    CtrlInfoTbl.grid_columnconfigure(1, weight = 1, uniform = 'fig')
    
    VaciarTbl = tk.Button(CtrlInfoTbl, state=tk.DISABLED, text = ' Vaciar Tabla ', bg = '#febf97', fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'), command = VaciarTabl)
    ElimArch = tk.Button(CtrlInfoTbl, state=tk.DISABLED, text = ' Quitar elemento de la Tabla ', bg = '#ffb0b0', fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'), command = ElimElmt)
    Etiqueta4 = tk.Label(CtrlInfoTbl, text = ' Si desea cambiar la posición (No.) de un archivo. Seleccionalo en\n la tabla y usa los siguientes botones para cambiar su posición:', justify = 'left', bg = color_fondo, fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'))
    MovArriba = tk.Button(CtrlInfoTbl,state=tk.DISABLED, text = ' ▲ ', bg = '#d2d2fe', fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'), command = MovArr)
    MovAbajo = tk.Button(CtrlInfoTbl,state=tk.DISABLED, text = ' ▼ ', bg = '#d2d2fe', fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'), command = MovAbj)

    Convert = tk.Button(SubVent, state=tk.DISABLED, text = ' Convertir archivos \n a un solo \n archivo PDF ', bg = '#c3ffce', fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'), command = AlmacenarPDF)
    Info = tk.Label(SubVent, justify = 'left', bg = 'black', fg = 'white', font = ('Arial',Vent[6],'bold italic'))
    
    Etiqueta2.grid(column = 0, row = 0, padx = (10,10), pady = (7,1), columnspan = 3, sticky = 'nsew')
    SubirArchs.place(x = Vent[11], y = 10)

    Tabla.grid(column = 0, row = 1, padx = (10,10), pady = (10,2), columnspan = 4, sticky = 'nsew')
    Barra.grid(column = 4, row = 1, padx = (10,10), pady = (10,2), sticky = 'nsew')
   
    NumArchs.grid(column = 0, row = 2, padx = (10,10), pady = (1,5), columnspan = 4, sticky = 'nsew')
    
    CtrlInfoTbl.grid(column = 0, row = 1, padx = (10,10), pady = (2,5), columnspan = 2, sticky = 'nsew')
    VaciarTbl.grid(column = 0, row = 0, padx = (10,10), pady = (5,5), sticky = 'nsew')
    ElimArch.grid(column = 1, row = 0, padx = (10,10), pady = (5,5), sticky = 'nsew')
    Etiqueta4.grid(column = 0, row = 1, padx = (10,10), pady = (5,5), columnspan = 2, sticky = 'nsew')
    MovArriba.grid(column = 0, row = 2, padx = (10,10), pady = (5,13), sticky = 'nsew')
    MovAbajo.grid(column = 1, row = 2, padx = (10,10), pady = (5,13), sticky = 'nsew')

    Convert.grid(column = 2, row = 1, padx = (10,10), pady = (5,5), sticky = 'nsew')
    Info.grid(column = 0, row = 2, padx = (10,10), pady = (1,5), columnspan = 3, sticky = 'nsew')

# Función "SeleccArch" - Selección de los archivos PDF a convertir
def SeleccArch():
    if Archs[0] < 50:
        Archvs = filedialog.askopenfilenames(title = "Elige tu(s) archivo(s): ", filetypes = (('Archivos PDF', '*.pdf'),))
        if Archvs:
            i = Archs[0]
            if i != 50:
                for A in Archvs:
                    Archs.append(A)
                    i += 1
                    path,nomb = os.path.split(A)
                    Tabla.insert(parent = '', index=i, iid=i, values=(i,nomb,path))
                    
                    if i == 50:
                        break

                Archs[0] = i;

                if i != 50:
                    NumArchs.configure(text = ' Puedes ingresar un máximo de '+str(50 - Archs[0])+' archivos...')
                else:
                    SubirArchs.configure(state=tk.DISABLED, cursor = 'arrow')
                    NumArchs.configure(text = ' Ya no es posible ingresar más archivos...')

                VaciarTbl.configure(state=tk.NORMAL, cursor = 'hand2')
                ElimArch.configure(state=tk.NORMAL, cursor = 'hand2')
                MovArriba.configure(state=tk.NORMAL, cursor = 'hand2')
                MovAbajo.configure(state=tk.NORMAL, cursor = 'hand2')
                Convert.configure(state=tk.NORMAL, cursor = 'hand2')
            else:
                SubirArchs.configure(state=tk.DISABLED, cursor = 'arrow')
                NumArchs.configure(text = ' Ya no es posible ingresar más archivos...')

# ____ Almacenará las caracteristicas que deberá tener la vantana y subventanas
Vent = []

# ____ Almacenará las rutas de los archivos a procesar (imagenes o pdfs)
Archs = []

# ____________________ DETERMINANDO ESTETICA DE VENTANA PRINCIPAL _____________________
# Identificando sistema operativo...
if platform == "linux" or platform == "linux2":
    # Sistema: Linux...
    # Dimensión de la pantalla
    args = ["xrandr", "-q", "-d", ":0"]
    proc = subprocess.Popen(args,stdout=subprocess.PIPE)
    for line in proc.stdout:
        if isinstance(line, bytes):
            line = line.decode("utf-8")
            # Dimensión de la pantalla
            if "Screen" in line:
                Vent.append(int(line.split()[7]))
                Vent.append(int(line.split()[9][:-1]))

    #print(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'))
elif platform == "darwin":
    # Sistema: OS X...
    pass
elif platform == "win32":
    # Sistema: Windows...
    # Dimensión de la pantalla
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    Vent.append(user32.GetSystemMetrics(0)) #Ancho
    Vent.append(user32.GetSystemMetrics(1)) #Alto
    
    #print(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))

# Dimensiones que deberá tener la ventana
if(Vent[0] >= 1920 and Vent[1] >= 1080):
    # --- 1920*1080
    Vent[0] = 1920
    Vent[1] = 1080

    # ____ Medidas de la Ventana principal
    Vent.append(int(Vent[0]/4))   # - 2 - w
    Vent.append(int(Vent[1]/4))   # - 3 - h
    
    # Posición en X, Y 
    Vent.append(int((Vent[0]/2) - (Vent[2]/2)))   # X - 4
    Vent.append(int((Vent[1]/2) - (Vent[3]/2)))   # Y - 5

    # Tamaño de Fuente
    Vent.append(12)   # - 6
    
    # ____ Medidas de la Subventana
    Vent.append(int(Vent[0]/2))   # - 7 - w
    Vent.append(int(Vent[1]/2))   # - 8 - h
    
    # Posición en X, Y 
    Vent.append(int((Vent[0]/2) - (Vent[7]/2)))   # X - 9
    Vent.append(int((Vent[1]/2) - (Vent[8]/2)))   # Y - 10

    # Posición en X, Y -- Botón SeleccImgs
    Vent.append(670) # X - 11

    # Ancho de la tabla de cada columna
    Vent.append(40) # w - 12

    #elif(DatosVentana[0] >= 1280 and DatosVentana[1] >= 720):
else:
    # --- 1280*720
    Vent[0] = 1280
    Vent[1] = 720

    # ____ Medidas de la Ventana principal
    Vent.append(Vent[0] - 850)   # - 2 - w
    Vent.append(Vent[1] - 490)   # - 3 - h
    
    # Posición en X, Y 
    Vent.append(int((Vent[0]/2) - (Vent[2]/2)))   # X - 4
    Vent.append(int((Vent[1]/2) - (Vent[3]/2)))   # Y - 5

    # Tamaño de Fuente
    Vent.append(9)   # - 6
    
    # ____ Medidas de la Subventana
    Vent.append(int(Vent[0] - 550))   # - 7 - w
    Vent.append(int(Vent[1] - 235))   # - 8 - h
    
    # Posición en X, Y 
    Vent.append(int((Vent[0]/2) - (Vent[7]/2)))   # X - 9
    Vent.append(int((Vent[1]/2) - (Vent[8]/2))-10)   # Y - 10

    # Posición en X, Y -- Botón SeleccImgs
    Vent.append(500) # X - 11

    # Ancho de la tabla de cada columna
    Vent.append(30) # w - 12

# Bandera de acción a realizar
Vent.append(0) # 13 - bandera -- 1 Conversión de imgs a pdf / 2 Conversión de PDFs a uno solo

# ______________________________ CREACIÓN DE VENTANA ______________________________
raiz = tk.Tk()
raiz.resizable(False, False)
raiz.title(' - Conversor de PDFs - ')
raiz.geometry(str(Vent[2])+'x'+str(Vent[3])+'+'+str(Vent[4])+'+'+str(Vent[5]))
raiz.config(bg = '#902626', bd = 8, relief = 'groove')
raiz.grid_columnconfigure(0, weight = 2, uniform = 'fig')

color_fondo = '#902626'
color_text = 'white'

MiniMenu1 = tk.LabelFrame(raiz, bd = 3, text = ' Convertir imágenes a un PDF ', bg = color_fondo, fg = color_text, font = ('Microsoft YaHei UI',Vent[6],'bold'))
MiniMenu1.grid_columnconfigure(0, weight = 1, uniform = 'fig')

Info1 = tk.Label(MiniMenu1, text = ' Convertir imágenes (.jpg y/o .png) a un archivo PDF ', bg = color_fondo, fg = color_text, font = ('Microsoft YaHei UI',Vent[6]+1))
Opc1 = tk.Button(MiniMenu1, text = ' Convertir: Imgs a PDF ', command = Imgs_PDF, relief = tk.RIDGE, activebackground = '#f6fdd5', borderwidth = 3, cursor = 'hand2', bg = '#f9d2a1', fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'))

MiniMenu1.grid(column = 0, row = 0, padx = (5,5), pady = (5, 5), sticky = 'nsew', columnspan = 2)
Info1.grid(column = 0, row = 0, padx = (5,5), pady = (5, 2), sticky = 'nsew', columnspan = 2)
Opc1.grid(column = 0, row = 1, padx = (5,5), pady = (3, 5), sticky = 'nsew', columnspan = 2)

MiniMenu2 = tk.LabelFrame(raiz, bd = 3, text = ' Convertir PDFs a uno solo ', bg = color_fondo, fg = color_text, font = ('Microsoft YaHei UI',Vent[6],'bold'))
MiniMenu2.grid_columnconfigure(0, weight = 1, uniform = 'fig')

Info2 = tk.Label(MiniMenu2, text = ' Convertir diferentes archivos (.pdf) a un solo ', bg = color_fondo, fg = color_text, font = ('Microsoft YaHei UI',Vent[6]+1))
Opc2 = tk.Button(MiniMenu2, text = ' Convertir: PDFs a un PDF ', command = PDFs_PDF, relief = tk.RIDGE, activebackground = '#f6fdd5', borderwidth = 3, cursor = 'hand2', bg = '#f9f9a1', fg = 'black', font = ('Microsoft YaHei UI',Vent[6],'bold'))

MiniMenu2.grid(column = 0, row = 1, padx = (5,5), pady = (5,5), sticky = 'nsew', columnspan = 2)
Info2.grid(column = 0, row = 0, padx = (5,5), pady = (5,2), sticky = 'nsew', columnspan = 2)
Opc2.grid(column = 0, row = 1, padx = (5,5), pady = (3,5), sticky = 'nsew', columnspan = 2)

raiz.mainloop() # Visualizando ventana