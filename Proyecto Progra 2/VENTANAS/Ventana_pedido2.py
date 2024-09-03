import customtkinter as ctk
import tkinter 



#metodo de ayuda para crear targetas con menus solicitados
def crear_tarjeta(self, menu):
    # Obtener el número de columnas y filas actuales
    num_tarjetas = len(self.menus_creados)
    fila = num_tarjetas // 2
    columna = num_tarjetas % 2

    # Crear la tarjeta con un tamaño fijo
    tarjeta = ctk.CTkFrame(tarjetas_frame, corner_radius=10, border_width=1, border_color="#4CAF50", width=64, height=140, fg_color="transparent")
    tarjeta.grid(row=fila, column=columna, padx=15, pady=15)

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

#codigo de ayuda para desarrollar el evento que se debe gatillar, cuando se presiona cada targeta(Menu)
def tarjeta_click(self, event, menu):
        # Verificar si hay suficientes ingredientes en el stock para preparar el menú
        suficiente_stock = True
        if self.stock.lista_ingredientes==[]:
            suficiente_stock=False
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
            total = self.pedido.calcular_total()
            self.label_total.configure(text=f"Total: ${total:.2f}")
        else:
            # Mostrar un mensaje indicando que no hay suficientes ingredientes usando CTkMessagebox
            CTkMessagebox(title="Stock Insuficiente", message=f"No hay suficientes ingredientes para preparar el menú '{menu.nombre}'.", icon="warning")