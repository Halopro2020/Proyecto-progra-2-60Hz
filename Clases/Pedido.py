class Pedido:
    def __init__(self):
        self.menus = []  
        self.total = 0

    def agregar_menu(self, menu):
        self.menus.append(menu)
        self.total += menu.precio

    def eliminar_menu(self, menu):
        if menu in self.menus:
            self.menus.remove(menu)
            self.total -= menu.precio