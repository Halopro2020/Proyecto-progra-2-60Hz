# Pedido.py
from Clases.Menu import Menu  # Asegúrate de que esta ruta sea correcta según la estructura de tu proyecto

class Pedido:
    def __init__(self):
        self.menus = []
        self.total = 0

    def agregar_menu(self, menu):
        # Asegúrate de que 'menu' sea un objeto que tenga un atributo 'precio'
        if isinstance(menu, Menu):
            self.menus.append(menu)
            self.total += menu.precio
        else:
            print("Error: El menú no es una instancia de la clase Menu.")

    def eliminar_menu(self, menu):
        if menu in self.menus:
            self.menus.remove(menu)
            self.total -= menu.precio
