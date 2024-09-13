import customtkinter as ctk
from tkinter import Canvas, ttk
from PIL import Image, ImageTk
from Clases.Menu import Menu
from Clases.Ingredientes import Ingrediente
from CTkMessagebox import CTkMessagebox
from Clases.Guardar_Ingredientes import Guardar_ingrediente
from fpdf import FPDF
from Clases.Pedido import Pedido


pedido = Pedido()
# Instanciar el gestor de ingredientes
gestor_ingredientes = Guardar_ingrediente()

# Crear menú gestionando el stock y los pedidos
menu = Menu(gestor_ingredientes.obtener_ingredientes(), [])
def verificar_stock(nombre_menu):
    recetas = {
        'Papas Fritas': {'papas': 2},
        'Hamburguesas': {'hamburguesa': 1, 'churrasco': 2, 'lamina queso': 1},
        'Completos': {'vienesa': 1, 'pan completo': 1, 'tomate': 1, 'palta': 1},
        'Pepsi': {'bebida': 1}
    }

    ingredientes_necesarios = recetas.get(nombre_menu, {})
    ingredientes_actuales = gestor_ingredientes.obtener_ingredientes()

    for ingrediente, cantidad_necesaria in ingredientes_necesarios.items():
        if ingrediente not in ingredientes_actuales or ingredientes_actuales[ingrediente] < cantidad_necesaria:
            print(f"No hay suficiente stock de {ingrediente} para {nombre_menu}.")
            return False

    for ingrediente, cantidad_necesaria in ingredientes_necesarios.items():
        gestor_ingredientes.eliminar_ingrediente(ingrediente, cantidad_necesaria)

    return True


# Función para actualizar el total del pedido
def actualizar_total(tree, label_total):
    total = 0
    for item in tree.get_children():
        total += int(tree.item(item, "values")[2])  # Sumar el precio unitario de cada ítem
    label_total.config(text=f"Total: {total} CLP")

# Función para crear el panel del pedido
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

    # Lista de menús (corrigiendo las imágenes)
    menus = [
        {"nombre": "Papas Fritas", "imagen": imagen_papas, "stock": "Papas Fritas"},
        {"nombre": "Cola", "imagen": imagen_cola, "stock": "Pepsi"},  # Este debe coincidir con el nombre en recetas
        {"nombre": "Hotdog", "imagen": imagen_hotdog, "stock": "Completos"},
        {"nombre": "Hamburguesa", "imagen": imagen_hamburguesa, "stock": "Hamburguesas"}
    ]


    def agregar_a_pedido(menu_nombre, stock_item, tree, label_total):
        print(f"Intentando agregar {menu_nombre} al pedido.")
        if verificar_stock(stock_item):  # Verificamos el stock correctamente con el stock_item
            print(f"Stock suficiente para {menu_nombre}.")
            # Si hay suficiente stock, agregar el menú al pedido y actualizar el Treeview
            menu.pedido.append(menu_nombre)

            # Definir los precios de los menús
            precios = {
                'Papas Fritas': 1500,
                'Cola': 1000,
                'Hotdog': 2000,
                'Hamburguesa': 2500
            }

            print(f"Precio de {menu_nombre}: {precios[menu_nombre]}")

            # Insertar en el Treeview
            tree.insert("", "end", values=(menu_nombre, 1, precios[menu_nombre]))

            # Actualizar el total
            actualizar_total(tree, label_total)

            # Ejecutar la callback adicional al ingresar el pedido
            ingresar_pedido_callback()
        else:
            print(f"No hay suficiente stock para {menu_nombre}.")
            CTkMessagebox(title="Stock insuficiente", message=f"No hay suficiente stock para preparar {menu_nombre}.", icon="warning")

    # Crear función para eliminar un menú del pedido
    def eliminar_menu(tree, label_total):
        selected_item = tree.selection()
        if selected_item:
            menu_nombre = tree.item(selected_item, "values")[0]

            # Reponer stock
            gestor_ingredientes.agregar_ingrediente(menu_nombre, 1)

            # Eliminar el ítem del Treeview
            tree.delete(selected_item)

            # Actualizar el total
            actualizar_total(tree, label_total)

            eliminar_pedido_callback()

    # Crear el botón para generar la boleta
    def generar_boleta(tree):
        if len(tree.get_children()) == 0:
            CTkMessagebox(title="Advertencia", message="No hay menús en el pedido.", icon="warning")
        else:
            # Generar el PDF de la boleta
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Boleta de Pedido", ln=True, align="C")
            pdf.ln(10)

            total = 0
            for item in tree.get_children():
                values = tree.item(item, "values")
                nombre = values[0]
                cantidad = values[1]
                precio = values[2]
                total += int(precio)
                pdf.cell(200, 10, txt=f"{nombre} - {cantidad} - {precio} CLP", ln=True, align="L")

            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Total: {total} CLP", ln=True, align="R")
            pdf.output("boleta_pedido.pdf")
            CTkMessagebox(title="Éxito", message="Boleta generada exitosamente.", icon="check")

    # Posicionar los menús en el canvas
    def mostrar_menus():
        for i, menu in enumerate(menus):
            x1, y1 = (i % 2) * 150 + 20, (i // 2) * 150 + 20
            x2, y2 = x1 + 100, y1 + 100

            # Crear un rectángulo con bordes redondeados
            rect = canvas_superior.create_rectangle(x1, y1, x2, y2, outline="black", width=2)

            # Colocar imagen
            img = canvas_superior.create_image((x1 + x2) // 2, y1 + 30, anchor="center", image=menu["imagen"])

            # Colocar nombre del menú
            canvas_superior.create_text((x1 + x2) // 2, y2 - 20, text=menu["nombre"], font=("Arial", 12))

            # Asociar la función de clic al rectángulo y a la imagen
            canvas_superior.tag_bind(rect, "<Button-1>", lambda event, m=menu["nombre"], s=menu["stock"]: agregar_a_pedido(m, s, tree, label_total))
            canvas_superior.tag_bind(img, "<Button-1>", lambda event, m=menu["nombre"], s=menu["stock"]: agregar_a_pedido(m, s, tree, label_total))

    mostrar_menus()
    # Frame para botones adicionales y Treeview
    frame_treeview2 = ctk.CTkFrame(tab)
    frame_treeview2.pack(side="top", fill="both", expand=True)

    # Botón para eliminar menú
    boton_eliminar = ctk.CTkButton(frame_treeview2, text="Eliminar Menú", fg_color="black", text_color="white", command=lambda: eliminar_menu(tree, label_total))
    boton_eliminar.pack(pady=10)

    # Treeview en el segundo frame
    tree = ttk.Treeview(frame_treeview2, columns=("Nombre del menu", "Cantidad", "Precio Unitario"), show="headings")
    tree.heading("Nombre del menu", text="Nombre del menu")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Precio Unitario", text="Precio Unitario")
    tree.pack(expand=False, fill="both")

    # Frame inferior para mostrar el total y generar boleta
    frame_inferior = ctk.CTkFrame(tab)
    frame_inferior.pack(side="bottom", expand=False, anchor="center")

    # Label para mostrar el total
    label_total = ctk.CTkLabel(frame_inferior, text="Total: 0 CLP", font=("Arial", 14))
    label_total.pack(side="left", padx=10)

    # Botón para generar boleta
    boton_generar_boleta = ctk.CTkButton(frame_inferior, text="Generar Boleta", command=lambda: generar_boleta(tree))
    boton_generar_boleta.pack(side="right", padx=10)

    return tree
