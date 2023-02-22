import openpyxl
import os.path
import re
import datetime

# Esta función toma como entrada una cadena de texto y la guarda en un archivo Excel
def guardar_en_excel(texto, numero):


    # definir el trimestre 
    trimestre_actual = define_trimestre(datetime.datetime.now())
    # crea el nombre del archivo con el numero de la persona
    name=numero+'_'+trimestre_actual+".xlsx"
    #crea la ruta del archivo
    ruta_archivo = os.path.join( 'src', 'files', name)

    # Carga el archivo Excel existente o crea uno nuevo si no existe
 
    if os.path.isfile(ruta_archivo):
        # Si el archivo existe, carga el libro Excel
        libro_excel = openpyxl.load_workbook(ruta_archivo)
        # Usa la hoja activa del libro Excel
        hoja = libro_excel.active
    
    else:
        # Si el archivo no existe, crea uno nuevo
        libro_excel = openpyxl.Workbook()
        hoja = libro_excel.active

    texto, valor = separar_texto_y_numeros(texto)
    # Escribe el texto en la siguiente fila vacía en la columna A
    fila_vacia = hoja.max_row + 1
    
    hoja.cell(row=fila_vacia, column=1, value=texto)
    
    
    hoja.cell(row=fila_vacia, column=2, value=valor)

    # Guarda el archivo Excel en el disco
    libro_excel.save(ruta_archivo)



# Esta función toma como entrada una cadena de texto y devuelve dos listas, una con las letras y otra con los números
def separar_texto_y_numeros(cadena):
    # Reemplazar todos los caracteres que no son letras ni números por espacios
    cadena = re.sub(r'[^\w\s\.]', ' ', cadena)
    
    # Dividir la cadena en palabras
    palabras = cadena.split()
    
    # Inicializar listas para texto y números
    texto = []
    numeros = []
    
    for palabra in palabras:
        # Intentar convertir la palabra a un número
        try:
            numero = float(palabra)
            numeros.append(numero)
        except ValueError:
            # Si la palabra no es un número, agregarla a la lista de texto
            texto.append(palabra)
    
    # Unir la lista de texto en una sola cadena con espacios entre cada palabra
    texto = ' '.join(texto)
    
    return texto, numeros[0]



def define_trimestre(fecha):
    # Obtener el trimestre actual
    trimestre = (fecha.month - 1) // 3 + 1

    # Asignar el nombre del archivo según el trimestre actual
    if trimestre == 1:
        trimestreactual= 'ene-mar'
    elif trimestre == 2:
        trimestreactual = 'abr-jun'
    elif trimestre == 3:
       trimestreactual = 'jul-sep'
    elif trimestre == 4:
       trimestreactual = 'oct-dic'

    return trimestreactual