import customtkinter as ctk
from tkinter import Canvas, ttk
from PIL import Image, ImageTk
from Clases.Menu import Menu
from Clases.Ingredientes import Ingrediente
from CTkMessagebox import CTkMessagebox
from Clases.Guardar_Ingredientes import Guardar_ingrediente
# Instanciar el gestor de ingredientes
gestor_ingredientes = Guardar_ingrediente()

# Crear menú gestionando el stock y los pedidos
menu = Menu(gestor_ingredientes.obtener_ingredientes(), [])

def verificar_stock(nombre_ingrediente):
    ingredientes = gestor_ingredientes.obtener_ingredientes()
    for ingrediente in ingredientes:
        if ingrediente.nombre == nombre_ingrediente:
            if ingrediente.cantidad > 0:
                gestor_ingredientes.eliminar_ingrediente(nombre_ingrediente, 1)  # Descontar el stock
                return True
            else:
                return False
    return False

def crear_panel_pedido(tab, ingresar_pedido_callback, eliminar_pedido_callback):
    # Crear canvas parte de arriba
    canvas_superior = Canvas(tab, bg="white", height=300)
    canvas_superior.pack(side="top", fill="x", expand=False)

    # Cargar imágenes de los menús
    imagen_papas = ImageTk.PhotoImage(Image.open("./IMG/icono_papas_fritas_64x64.png"))
    imagen_cola = ImageTk.PhotoImage(Image.open("./IMG/icono_cola_64x64.png"))
    imagen_hotdog = ImageTk.PhotoImage(Image.open("./IMG/icono_hotdog_sin_texto_64x64.png"))
    imagen_hamburguesa = ImageTk.PhotoImage(Image.open("./IMG/icono_hamburguesa_negra_64x64.png"))

    # Guardar las referencias para que no se eliminen las imágenes
    canvas_superior.imagenes = [imagen_papas, imagen_cola, imagen_hotdog, imagen_hamburguesa]

    # Lista de menús (puedes adaptarlo a tus datos)
    # Lista de menús (corrigiendo las imágenes)
    menus = [
        {"nombre": "Papas Fritas", "imagen": imagen_papas, "stock": "Papas Fritas"},
        {"nombre": "Cola", "imagen": imagen_cola, "stock": "Cola"},
        {"nombre": "Hotdog", "imagen": imagen_hotdog, "stock": "Hotdog"},  # Corregido
        {"nombre": "Hamburguesa", "imagen": imagen_hamburguesa, "stock": "Hamburguesa"}  # Corregido
    ]   


    def agregar_a_pedido(menu_nombre, stock_item, tree):
        if verificar_stock(stock_item):
            # Si hay suficiente stock, agregar el menú al pedido y actualizar el Treeview
            menu.pedido.append(menu_nombre)  # Añadir el menú al pedido en la clase Menu
        
            # Definir los precios de los menús (puedes ajustar estos valores)
            precios = {
                'Papas Fritas': 1500,
                'Cola': 1000,
                'Hotdog': 2000,
                'Hamburguesa': 2500
            }
        
            # Insertar en el Treeview (nombre del menú, cantidad=1, precio unitario)
            tree.insert("", "end", values=(menu_nombre, 1, precios[menu_nombre]))
        
            # Ejecutar la callback adicional al ingresar el pedido
            ingresar_pedido_callback()
        else:
            # Si no hay suficiente stock, mostrar mensaje de advertencia
            CTkMessagebox(title="Stock insuficiente", message=f"No hay suficiente stock para preparar {menu_nombre}.", icon="warning")

    def cambiar_color_verde(event):
        # Cambiar borde a verde al pasar el mouse
        canvas_superior.itemconfig(event.widget.find_closest(event.x, event.y), outline="green")

    def volver_color_rojo(event):
        # Volver el borde a rojo al salir del área
        canvas_superior.itemconfig(event.widget.find_closest(event.x, event.y), outline="red")

    # Crear función para dibujar rectángulos con esquinas redondeadas
    def crear_rectangulo_redondeado(x1, y1, x2, y2, radio=15, **kwargs):
        points = [
            x1 + radio, y1,
            x2 - radio, y1,
            x2, y1, 
            x2, y1 + radio,
            x2, y2 - radio,
            x2, y2, 
            x2 - radio, y2,
            x1 + radio, y2,
            x1, y2, 
            x1, y2 - radio,
            x1, y1 + radio,
            x1, y1
        ]
        return canvas_superior.create_polygon(points, smooth=True, **kwargs)

    # Crear tarjetas de menús dentro del canvas
    for i, menu in enumerate(menus):
        x1, y1 = (i % 2) * 100 + 10, (i // 2) * 100 + 10
        x2, y2 = x1 + 90, y1 + 90

        # Crear borde rojo redondeado
        rect = crear_rectangulo_redondeado(x1, y1, x2, y2, outline="red", width=5, fill="white")

        # Añadir imagen dentro del rectángulo
        canvas_superior.create_image(x1 + 10, y1 + 10, anchor="nw", image=menu["imagen"])

        # Crear frame transparente para el nombre del menú
        tarjeta_frame = ctk.CTkFrame(canvas_superior, corner_radius=10, fg_color="transparent")
        canvas_superior.create_window(x1, y2 - 10, window=tarjeta_frame, width=50, height=20, anchor="nw")

        # Mostrar nombre del menú en la tarjeta
        nombre_label = ctk.CTkLabel(tarjeta_frame, text=menu["nombre"], font=("Arial", 10))
        nombre_label.pack(side="top", padx=5, pady=5)

        # Asociar el clic en la tarjeta con la función de agregar al pedido
        # Asociar el clic en la tarjeta con la función de agregar al pedido
        # Asociar el clic en la tarjeta con la función de agregar al pedido
        tarjeta_frame.bind("<Button-1>", lambda e, m=menu["nombre"], s=menu["stock"]: agregar_a_pedido(m, s, tree))



        # Asociar eventos de entrada y salida del mouse para cambiar color del borde
        canvas_superior.tag_bind(rect, "<Enter>", cambiar_color_verde)
        canvas_superior.tag_bind(rect, "<Leave>", volver_color_rojo)

    # Frame inferior para botones adicionales
    frame_inferior = ctk.CTkFrame(tab)
    frame_inferior.pack(side="bottom", expand=False, anchor="center")

    boton_generar_menu = ctk.CTkButton(frame_inferior, text="Generar Boleta", command=ingresar_pedido_callback)
    boton_generar_menu.pack(side="bottom", fill="x", expand=False)

    frame_treeview2 = ctk.CTkFrame(tab)
    frame_treeview2.pack(side="top", fill="both", expand=True)

    # Botón para eliminar menú arriba del Treeview
    boton_eliminar = ctk.CTkButton(frame_treeview2, text="Eliminar Menu", fg_color="black", text_color="white", command=eliminar_pedido_callback)
    boton_eliminar.pack(pady=10)

    # Treeview en el segundo frame
    tree = ttk.Treeview(frame_treeview2, columns=("Nombre del menu", "Cantidad", "Precio Unitario"), show="headings")
    tree.heading("Nombre del menu", text="Nombre del menu")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Precio Unitario", text="Precio Unitario")
    tree.pack(expand=False, fill="both")

    return tree
