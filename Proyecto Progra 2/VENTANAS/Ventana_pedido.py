import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
import re

def crear_panel_pedido(tab, ingresar_pedido_callback, eliminar_pedido_callback):
    
    frame_inferior = ctk.CTkFrame(tab)
    frame_inferior.pack(side="bottom", expand=False, anchor="center")

    boton_generar_menu = ctk.CTkButton(frame_inferior, text="Generar Menu", command=ingresar_pedido_callback)
    boton_generar_menu.pack(side="bottom", fill="x", expand=False)

    frame_treeview2 = ctk.CTkFrame(tab)
    frame_treeview2.pack(side="top", fill="both", expand=True)

    # Botón para eliminar menu arriba del Treeview
    boton_eliminar = ctk.CTkButton(frame_treeview2, text="Eliminar Menu", fg_color="black", text_color="white", command=eliminar_pedido_callback)
    boton_eliminar.pack(pady=10)

    # Treeview en el segundo frame
    tree = ttk.Treeview(frame_treeview2, columns=("Nombre del menu", "Cantidad", "Precio Unitario"), show="headings")
    tree.heading("Nombre del menu", text="Nombre del menu")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Precio Unitario", text="Precio Unitario")
    tree.pack(expand=False, fill="both")
