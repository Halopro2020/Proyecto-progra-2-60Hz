import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
import re

def crear_panel_ingredientes(tab, ingresar_libro_callback, eliminar_libro_callback):
    # Dividir la pestaña en dos frames
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

    # Formulario en el segundo frame
    label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad: ")
    label_cantidad.pack(pady=5)
    entry_cantidad = ctk.CTkEntry(frame_formulario)
    entry_cantidad.pack(pady=5)
    
    # Botón de ingreso
    boton_ingresar = ctk.CTkButton(frame_formulario, text="Ingresar ingrediente", command=ingresar_libro_callback)
    boton_ingresar.pack(pady=10)

    # Botón para eliminar ingrediente arriba del Treeview
    boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar Ingrediente", fg_color="black", text_color="white", command=eliminar_libro_callback)
    boton_eliminar.pack(pady=10)

    # Treeview en el segundo frame
    tree = ttk.Treeview(frame_treeview, columns=("Nombre", "Cantidad"), show="headings")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Cantidad", text="Cantidad")
    tree.pack(expand=False, fill="y", padx=10, pady=10)

    # Botón de menu
    boton_generar_menu = ctk.CTkButton(frame_inferior, text="Generar Menu", command=ingresar_libro_callback)
    boton_generar_menu.pack(side="bottom", fill="y",expand=False)
    
    return entry_nombre, entry_cantidad, tree
