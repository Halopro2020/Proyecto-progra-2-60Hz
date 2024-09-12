class Pedido:
    def __init__(self):
        self.menus = []
        self.total = 0

    def agregar_menu(self, menu, stock):
        # Verificar si hay suficiente stock de ingredientes para el menú
        for ingrediente, cantidad_necesaria in menu.ingredientes.items():
            if stock[ingrediente].cantidad < cantidad_necesaria:
                raise ValueError(f"No hay suficiente stock para {ingrediente}")
        
        # Descontar los ingredientes del stock
        for ingrediente, cantidad_necesaria in menu.ingredientes.items():
            stock[ingrediente].cantidad -= cantidad_necesaria
        
        # Agregar el menú al pedido
        self.menus.append(menu)
        self.total += menu.precio

    def eliminar_menu(self, menu, stock):
        if menu in self.menus:
            # Reponer los ingredientes en el stock
            for ingrediente, cantidad_necesaria in menu.ingredientes.items():
                stock[ingrediente].cantidad += cantidad_necesaria
            
            # Eliminar el menú del pedido
            self.menus.remove(menu)
            self.total -= menu.precio
        else:
            raise ValueError("El menú no está en el pedido")

    def obtener_total(self):
        return self.total

    def obtener_detalle(self):
        return [(menu.nombre, menu.precio) for menu in self.menus]
