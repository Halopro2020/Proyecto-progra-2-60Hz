import customtkinter as ctk
from tkinter import ttk
from Clases.Guardar_Ingredientes import Guardar_ingrediente
from Clases.Ingredientes import Ingrediente
import re
from CTkMessagebox import CTkMessagebox
from VENTANAS.Ventana_ingredientes import crear_panel_ingredientes
from VENTANAS.Ventana_pedido import crear_panel_pedido
from VENTANAS.Ventana_pedido2 import *

class AplicacionConPestanas(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Gestion de ingredientes y pedidos por 60Hz")
        self.geometry("1200x700")

        # Inicializar la Biblioteca
        self.guardar_ingrediente = Guardar_ingrediente()

        # Crear pestañas
        self.tabview = ctk.CTkTabview(self, width=600, height=500)
        self.tabview.pack(padx=20, pady=20)

        self.crear_pestanas()

    def crear_pestanas(self):
        # Crear y configurar las pestañas
        self.tab1 = self.tabview.add("Ingreso de ingredientes")
        self.tab2 = self.tabview.add("Pedido")

        # Configurar el contenido de la pestaña 1
        self.configurar_pestana1()
        self.configurar_pestana2()
        
    def configurar_pestana1(self):
        self.entry_nombre, self.entry_cantidad, self.tree = crear_panel_ingredientes(
            self.tab1, self.ingresar_ingrediente, self.eliminar_ingrediente
        )
    def configurar_pestana2(self):
        crear_panel_pedido(
            self.tab2, self.ingresar_ingrediente, self.eliminar_ingrediente
        )
    def validar_nombre(self, nombre):
        if re.match(r"^[a-zA-Z\s]+$", nombre):
            return True
        else:
            CTkMessagebox(title="Error de Validación", message="El nombre debe contener solo letras y espacios.", icon="warning")
            return False

    def validar_cantidad(self, cantidad):
        try:
            valor = int(cantidad)
            if valor >= 0:
                return True
            else:
                CTkMessagebox(title="Error de Validación", message="Ingrese una cantidad valida, debe ser un número entero no negativo.", icon="warning")
                return False
        except ValueError:
            CTkMessagebox(title="Error de Validación", message="Ingrese una cantidad valida, debe ser un número entero.", icon="warning")

    def ingresar_ingrediente(self):
        nombre = self.entry_nombre.get()
        cantidad = self.entry_cantidad.get()

        # Validar entradas
        if not self.validar_nombre(nombre):
            return
        elif not self.validar_cantidad(cantidad):
            return

        # Crear una instancia de Libro
        ingrediente = Ingrediente(nombre, int(cantidad))

        # Agregar el libro a la biblioteca
        if self.guardar_ingrediente.agregar_ingrediente(ingrediente):
            self.actualizar_treeview()
        else:
            CTkMessagebox(title="Error", message="El ingrediente ya existe en la biblioteca.", icon="warning")

    def eliminar_ingrediente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor selecciona un ingrediente para eliminar.", icon="warning")
            return

        item = self.tree.item(seleccion)
        nombre = item['values'][0]
        cantidad = int(item['values'][1])

        # Eliminar el libro de la biblioteca
        if self.guardar_ingrediente.eliminar_ingrediente(nombre, cantidad):
            self.actualizar_treeview()
        else:
            CTkMessagebox(title="Error", message="El ingrediente no se pudo eliminar.", icon="warning")

    def actualizar_treeview(self):
        # Limpiar el Treeview actual
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agregar todos los libros de la biblioteca al Treeview
        for ingrediente in self.guardar_ingrediente.obtener_ingredientes():
            self.tree.insert("", "end", values=(ingrediente.nombre, ingrediente.cantidad))

