import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from Clases.Ingredientes import Ingrediente  # Asegúrate de que esta clase está definida
from Clases.Guardar_Ingredientes import Guardar_ingrediente

# Crear una instancia de Guardar_ingrediente
gestor_ingredientes = Guardar_ingrediente()

def actualizar_ingredientes(entry_nombre, entry_cantidad):
    nombre = entry_nombre.get().strip().lower()
    cantidad = int(entry_cantidad.get().strip())
    
    # Crear una instancia de Ingrediente y añadirla al gestor
    nuevo_ingrediente = Ingrediente(nombre, cantidad)
    gestor_ingredientes.agregar_ingrediente(nuevo_ingrediente)
    
    # Depuración
    print("Ingredientes actuales:", gestor_ingredientes.obtener_ingredientes())


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

def generar_menu():
    recetas = {
        'papas fritas': {'papas': 2},  
        'hamburguesas': {'hamburguesa': 1, 'churrasco': 2, 'lamina queso': 1},
        'completos': {'vienesa': 1, 'pan completo': 1, 'tomate': 1, 'palta': 1},
        'pepsi': {'bebida': 1}
    }

    menus_generados, faltantes = [], []

    # Obtener ingredientes disponibles
    ingredientes_disponibles = {ing.nombre: ing.cantidad for ing in gestor_ingredientes.obtener_ingredientes()}
    
    # Depuración: verificar si los ingredientes están bien almacenados
    print("Stock actual:", ingredientes_disponibles)

    for receta, ingredientes in recetas.items():
        suficientes = True
        faltantes_en_receta = []  # Para hacer seguimiento de los ingredientes faltantes en cada receta

        for ing, cant_necesaria in ingredientes.items():
            disponible = ingredientes_disponibles.get(ing, 0)
            if disponible < cant_necesaria:
                suficientes = False
                faltantes_en_receta.append(f"{ing} - Necesario: {cant_necesaria}, Disponible: {disponible}")

        if suficientes:
            menus_generados.append(receta)
        else:
            faltantes.append(f"{receta} (Faltantes: {', '.join(faltantes_en_receta)})")

    if menus_generados:
        CTkMessagebox(title="Menús generados", message=", ".join(menus_generados), icon="check")
    if faltantes:
        CTkMessagebox(title="Faltan ingredientes", message=", ".join(faltantes), icon="warning")
