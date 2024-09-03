import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
import re

def crear_panel_pedido(tab, ingresar_pedido_callback, eliminar_pedido_callback):
    
    # Dividir la pestaña en dos frames
    frame_formulario2 = ctk.CTkFrame(tab)
    frame_formulario2.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    frame_treeview2 = ctk.CTkFrame(tab)
    frame_treeview2.pack(side="bottom", fill="x", expand=True, padx=10, pady=20)

    # Botón para eliminar menu arriba del Treeview
    boton_eliminar = ctk.CTkButton(frame_treeview2, text="Eliminar Menu", fg_color="black", text_color="white", command=eliminar_pedido_callback)
    boton_eliminar.pack(pady=10)

    # Treeview en el segundo frame
    tree = ttk.Treeview(frame_treeview2, columns=("Nombre del menu", "Cantidad", "Precio Unitario"), show="headings")
    tree.heading("Nombre del menu", text="Nombre del menu")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Precio Unitario", text="Precio Unitario")
    tree.pack(expand=True, fill="x", padx=10, pady=10)
   
    # Botón de ingreso deberia ir hasta abajo
    boton_ingresar = ctk.CTkButton(frame_formulario2, text="Generar Menu", command=ingresar_pedido_callback, )
    boton_ingresar.place(relx=0.5, rely=0.9, relwidth=0.9, relheight=0.05)
