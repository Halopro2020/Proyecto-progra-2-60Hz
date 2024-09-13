import customtkinter as ctk
from tkinter import ttk, Canvas
from Clases.Pedido import Pedido
from PIL import Image, ImageTk
from CTkMessagebox import CTkMessagebox
import re

# crear el panel del pedido con canvas(imagenes) y treeview
def crear_panel_pedido(tab, ingresar_pedido_callback, eliminar_pedido_callback):
    # Crear canvas parte de arriba
    canvas_superior = Canvas(tab, bg="white", height=300) 
    canvas_superior.pack(side="top", fill="x", expand=False)
    
    imagen = Image.open("./IMG/icono_papas_fritas_64x64.png")
    imagen2 = Image.open("./IMG/icono_cola_64x64.png")
    imagen3 = Image.open("./IMG/icono_hotdog_sin_texto_64x64.png")
    imagen4 = Image.open("./IMG/icono_hamburguesa_negra_64x64.png")
    imagen_tk = ImageTk.PhotoImage(imagen)
    
    # Crear los objetos PhotoImage para cada imagen
    imagen_tk = ImageTk.PhotoImage(imagen)
    imagen_tk2 = ImageTk.PhotoImage(imagen2)
    imagen_tk3 = ImageTk.PhotoImage(imagen3)
    imagen_tk4 = ImageTk.PhotoImage(imagen4)

    # guardar las referencias a las imágenes en el canvas
    canvas_superior.imagen_tk = imagen_tk
    canvas_superior.imagen_tk2 = imagen_tk2
    canvas_superior.imagen_tk3 = imagen_tk3
    canvas_superior.imagen_tk4 = imagen_tk4

    # Crear un Canvas y mostrar las imágenes
    canvas_superior.create_image(10, 10, anchor="nw", image=imagen_tk)
    canvas_superior.create_image(90, 10, anchor="nw", image=imagen_tk2)
    canvas_superior.create_image(10, 120, anchor="nw", image=imagen_tk3)
    canvas_superior.create_image(90, 120, anchor="nw", image=imagen_tk4)

    #De aca en adelante son los frames, trevieew 
    frame_inferior = ctk.CTkFrame(tab)
    frame_inferior.pack(side="bottom", expand=False, anchor="center")

    boton_generar_menu = ctk.CTkButton(frame_inferior, text="Generar Boleta", command=ingresar_pedido_callback)
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

    # Retornar el frame de tarjetas y el treeview
    return  tree

# Método de ayuda para crear tarjetas con menús solicitados dentro del canvas
def crear_tarjeta(canvas, self, menu):
    # Obtener el número de columnas y filas actuales
    num_tarjetas = len(self.menus_creados)
    fila = num_tarjetas // 2
    columna = num_tarjetas % 2

    # Crear la tarjeta con un tamaño fijo
    tarjeta = ctk.CTkFrame(canvas, corner_radius=10, border_width=1, border_color="#4CAF50", width=64, height=140, fg_color="transparent")
    tarjeta.pack(side="left", padx=15, pady=5)

    # Hacer que la tarjeta sea completamente clickeable 
    tarjeta.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))

    # Cambiar el color del borde cuando el mouse pasa sobre la tarjeta
    tarjeta.bind("<Enter>", lambda event: tarjeta.configure(border_color="#FF0000"))  # Cambia a rojo al pasar el mouse
    tarjeta.bind("<Leave>", lambda event: tarjeta.configure(border_color="#4CAF50"))  # Vuelve al verde al salir

    # Verifica si hay una imagen asociada con el menú
    if menu.icono_menu:
        # Crear y empaquetar el CTkLabel con la imagen, sin texto y con fondo transparente
        imagen_label = ctk.CTkLabel(tarjeta, image=menu.icono_menu, width=64, height=64, text="", bg_color="transparent")
        imagen_label.pack(anchor="center", pady=5, padx=10)
        imagen_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))  # Asegura que el clic en la imagen funcione

        # Agregar un Label debajo de la imagen para mostrar el nombre del menú
        texto_label = ctk.CTkLabel(tarjeta, text=f"{menu.nombre}", text_color="black", font=("Helvetica", 12, "bold"), bg_color="transparent")
        texto_label.pack(anchor="center", pady=1)
        texto_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))  # Asegura que el clic en el texto funcione

    else:
        print(f"No se pudo cargar la imagen para el menú '{menu.nombre}'")

# Código de ayuda para desarrollar el evento que se debe gatillar cuando se presiona cada tarjeta (Menú)
def tarjeta_click(self, event, menu):
    # Verificar si hay suficientes ingredientes en el stock para preparar el menú
    suficiente_stock = True
    if not self.stock.lista_ingredientes:  # Revisar si hay ingredientes en el stock
        suficiente_stock = False

    for ingrediente_necesario in menu.ingredientes:
        for ingrediente_stock in self.stock.lista_ingredientes:
            if ingrediente_necesario.nombre == ingrediente_stock.nombre:
                if int(ingrediente_stock.cantidad) < int(ingrediente_necesario.cantidad):
                    suficiente_stock = False
                    break
        if not suficiente_stock:
            break

    if suficiente_stock:
        # Descontar los ingredientes del stock
        for ingrediente_necesario in menu.ingredientes:
            for ingrediente_stock in self.stock.lista_ingredientes:
                if ingrediente_necesario.nombre == ingrediente_stock.nombre:
                    ingrediente_stock.cantidad = str(int(ingrediente_stock.cantidad) - int(ingrediente_necesario.cantidad))

        # Agregar el menú al pedido
        self.pedido.agregar_menu(menu)

        # Actualizar el Treeview
        self.actualizar_treeview_pedido()

        # Actualizar el total del pedido
        total = self.pedido.obtener_total()  # Usar obtener_total() en lugar de calcular_total()
        self.label_total.configure(text=f"Total: ${total:.2f}")
    else:
        # Mostrar un mensaje indicando que no hay suficientes ingredientes usando CTkMessagebox
        CTkMessagebox(title="Stock Insuficiente", message=f"No hay suficientes ingredientes para preparar el menú '{menu.nombre}'.", icon="warning")
