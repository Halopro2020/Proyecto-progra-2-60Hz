import customtkinter as ctk
from tkinter import Canvas, ttk
from PIL import Image, ImageTk
from CTkMessagebox import CTkMessagebox

class App:
    def __init__(self, stock, pedido):
        self.stock = stock
        self.pedido = pedido
        self.menus_creados = []
    
    # Simulación de stock de ingredientes
    stock_ingredientes = {
        "papas_fritas": 10,
        "cola": 5,
        "hotdog": 7,
        "hamburguesa": 4
    }

    # Verificar si hay stock suficiente
    def verificar_stock(self, menu):
        if self.stock_ingredientes[menu] > 0:
            self.stock_ingredientes[menu] -= 1  # Descontar el stock
            return True
        else:
            return False

    # Crear tarjeta de menú
    def crear_tarjeta(self, tarjetas_frame, menu):
        num_tarjetas = len(self.menus_creados)
        fila = num_tarjetas // 2
        columna = num_tarjetas % 2

        # Crear la tarjeta
        tarjeta = ctk.CTkFrame(tarjetas_frame, corner_radius=10, border_width=1, border_color="#4CAF50", width=64, height=140, fg_color="transparent")
        tarjeta.grid(row=fila, column=columna, padx=15, pady=15)
        tarjeta.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))
        tarjeta.bind("<Enter>", lambda event: tarjeta.configure(border_color="#FF0000"))
        tarjeta.bind("<Leave>", lambda event: tarjeta.configure(border_color="#4CAF50"))

        # Cargar imagen del menú
        if menu.icono_menu:
            imagen_label = ctk.CTkLabel(tarjeta, image=menu.icono_menu, width=64, height=64, text="", bg_color="transparent")
            imagen_label.pack(anchor="center", pady=5, padx=10)
            imagen_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))

            # Nombre del menú
            texto_label = ctk.CTkLabel(tarjeta, text=f"{menu.nombre}", text_color="black", font=("Helvetica", 12, "bold"), bg_color="transparent")
            texto_label.pack(anchor="center", pady=1)
            texto_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))
        else:
            print(f"No se pudo cargar la imagen para el menú '{menu.nombre}'")

    # Evento cuando se clickea en una tarjeta
    def tarjeta_click(self, event, menu):
        suficiente_stock = self.verificar_stock(menu.stock_key)
        if suficiente_stock:
            # Agregar menú al pedido
            self.pedido.agregar_menu(menu)
            self.actualizar_treeview_pedido()
            total = self.pedido.obtener_total()
            self.label_total.configure(text=f"Total: ${total:.2f}")
        else:
            CTkMessagebox(title="Stock insuficiente", message=f"No hay suficiente stock para preparar {menu.nombre}.", icon="warning")

    # Actualizar Treeview con el pedido
    def actualizar_treeview_pedido(self):
        # Actualizar el treeview con los menús agregados
        pass

    # Crear panel de pedido con la interfaz gráfica
    def crear_panel_pedido(self, tab, ingresar_pedido_callback, eliminar_pedido_callback):
        canvas_superior = Canvas(tab, bg="white", height=300)
        canvas_superior.pack(side="top", fill="x", expand=False)

        # Cargar imágenes
        imagen_papas = ImageTk.PhotoImage(Image.open("./IMG/icono_papas_fritas_64x64.png"))
        imagen_cola = ImageTk.PhotoImage(Image.open("./IMG/icono_cola_64x64.png"))
        imagen_hotdog = ImageTk.PhotoImage(Image.open("./IMG/icono_hotdog_sin_texto_64x64.png"))
        imagen_hamburguesa = ImageTk.PhotoImage(Image.open("./IMG/icono_hamburguesa_negra_64x64.png"))

        menus = [
            {"nombre": "Papas Fritas", "imagen": imagen_papas, "stock_key": "papas_fritas"},
            {"nombre": "Cola", "imagen": imagen_cola, "stock_key": "cola"},
            {"nombre": "Hotdog", "imagen": imagen_hotdog, "stock_key": "hotdog"},
            {"nombre": "Hamburguesa", "imagen": imagen_hamburguesa, "stock_key": "hamburguesa"}
        ]

        for menu in menus:
            self.crear_tarjeta(canvas_superior, menu)

        frame_inferior = ctk.CTkFrame(tab)
        frame_inferior.pack(side="bottom", expand=False, anchor="center")

        boton_generar_menu = ctk.CTkButton(frame_inferior, text="Generar Boleta", command=ingresar_pedido_callback)
        boton_generar_menu.pack(side="bottom", fill="x", expand=False)

        frame_treeview2 = ctk.CTkFrame(tab)
        frame_treeview2.pack(side="top", fill="both", expand=True)

        boton_eliminar = ctk.CTkButton(frame_treeview2, text="Eliminar Menu", fg_color="black", text_color="white", command=eliminar_pedido_callback)
        boton_eliminar.pack(pady=10)

        tree = ttk.Treeview(frame_treeview2, columns=("Nombre del menu", "Cantidad", "Precio Unitario"), show="headings")
        tree.heading("Nombre del menu", text="Nombre del menu")
        tree.heading("Cantidad", text="Cantidad")
        tree.heading("Precio Unitario", text="Precio Unitario")
        tree.pack(expand=False, fill="both")

        return tree
