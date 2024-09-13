import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
import re

# Diccionario global de ingredientes disponibles
ingredientes_disponibles = {
    'papas': 0,
    'hamburguesa': 0,
    'pan completo': 0,
    'churrasco' : 0,
    'lamina queso': 0,
    'vienesa': 0,
    'tomate': 0,
    'palta': 0,
    'bebida': 0
}

# Lista de ingredientes válidos
INGREDIENTES_VALIDOS = ['papas', 'bebida', 'hamburguesa', 'vienesa', 'pan completo', 'palta', 'tomate', 'lamina queso', 'churrasco']

def actualizar_ingredientes(entry_nombre, entry_cantidad):
    nombre = entry_nombre.get().strip().lower()  # Convertir a minúsculas para normalizar
    cantidad = entry_cantidad.get().strip()  # Obtener la cantidad como cadena
    
    # Validar que el nombre sea un ingrediente válido
    if nombre not in INGREDIENTES_VALIDOS:
        CTkMessagebox(title="Error", message="El ingrediente ingresado no es válido.", icon="warning")
        return  # Salir de la función para que no siga ejecutando

    try:
        cantidad = int(cantidad)  # Convertir la cantidad a entero
    except ValueError:
        CTkMessagebox(title="Error", message="La cantidad debe ser un número entero válido.", icon="warning")
        return  # Salir de la función si la cantidad no es válida

    # Actualizar el diccionario de ingredientes
    if nombre in ingredientes_disponibles:
        ingredientes_disponibles[nombre] += cantidad  # Sumar la cantidad si ya existe
    else:
        ingredientes_disponibles[nombre] = cantidad  # Agregar nuevo ingrediente
        
        

def crear_panel_ingredientes(tab, ingresar_libro_callback, eliminar_libro_callback):
    # Dividir la pestaña en tres frames
    frame_formulario = ctk.CTkFrame(tab)
    frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    frame_inferior = ctk.CTkFrame(tab)
    frame_inferior.pack(side="bottom", fill="y", expand=False)

    frame_treeview = ctk.CTkFrame(tab)
    frame_treeview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # Formulario en el primer frame
    label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre del Ingrediente")
    label_nombre.pack(pady=5)
    entry_nombre = ctk.CTkEntry(frame_formulario)
    entry_nombre.pack(pady=5)

    label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad: ")
    label_cantidad.pack(pady=5)
    entry_cantidad = ctk.CTkEntry(frame_formulario)
    entry_cantidad.pack(pady=5)
    
    # Botón de ingreso con actualización de ingredientes
    boton_ingresar = ctk.CTkButton(frame_formulario, text="Ingresar ingrediente", 
                                   command=lambda: [actualizar_ingredientes(entry_nombre, entry_cantidad), ingresar_libro_callback()])
    boton_ingresar.pack(pady=10)

    # Botón para eliminar ingrediente arriba del Treeview
    boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar Ingrediente", fg_color="black", text_color="white", command=eliminar_libro_callback)
    boton_eliminar.pack(pady=10)

    # Treeview en el segundo frame
    tree = ttk.Treeview(frame_treeview, columns=("Nombre", "Cantidad"), show="headings")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Cantidad", text="Cantidad")
    tree.pack(expand=False, fill="y", padx=10, pady=10)

    # Botón para generar menús en el frame inferior
    boton_generar_menu = ctk.CTkButton(frame_inferior, text="Generar Menu", command=generar_menu)
    boton_generar_menu.pack(side="bottom", fill="y", expand=False)
    
    return entry_nombre, entry_cantidad, tree

# Función para generar menús basado en los ingredientes del stock
def generar_menu():
    # Recetas con los ingredientes y cantidades necesarias
    recetas = {
        'Papas Fritas': {'papas': 2},
        'Hamburguesas': {'hamburguesa': 1, 'churrasco': 2, 'lamina queso': 1},
        'Completos': {'vienesa': 1, 'pan completo': 1, 'tomate': 1, 'palta': 1},
        'Pepsi': {'bebida': 1}
    }

    menus_generados, faltantes = [], []

    # Obtener ingredientes disponibles (adaptar a la lógica de tu aplicación)
    for receta, ingredientes in recetas.items():
        suficientes = True

        # Iterar sobre los ingredientes de la receta
        for ing, cant_necesaria in ingredientes.items():
            disponible = ingredientes_disponibles.get(ing, 0)
            if disponible < cant_necesaria:
                suficientes = False
                break

        if suficientes:
            menus_generados.append(receta)
        else:
            faltantes.append(receta)

    # Mostrar menús generados o faltantes
    if menus_generados:
        CTkMessagebox(title="Menús generados", message=", ".join(menus_generados), icon="check")
    if faltantes:
        CTkMessagebox(title="Faltan ingredientes", message=", ".join(faltantes), icon="warning")
