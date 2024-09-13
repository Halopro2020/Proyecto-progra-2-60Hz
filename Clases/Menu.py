class Menu:
    def __init__(self, stock, pedido):
        self.stock = stock
        self.pedido = pedido
        self.menus_creados = []

    def verificar_stock(self, nombre_menu):
        recetas = {
            'papas fritas': {'papas': 2},  
            'hamburguesas': {'hamburguesa': 1, 'churrasco': 2, 'lamina queso': 1},
            'completos': {'vienesa': 1, 'pan completo': 1, 'tomate': 1, 'palta': 1},
            'pepsi': {'bebida': 1}
        }

        ingredientes_necesarios = recetas.get(nombre_menu, {})
        ingredientes_actuales = {ing.nombre: ing.cantidad for ing in self.stock}
        
        for ingrediente, cantidad_necesaria in ingredientes_necesarios.items():
            if ingredientes_actuales.get(ingrediente, 0) < cantidad_necesaria:
                return False

        return True

    def agregar_menu(self, nombre_menu):
        if self.verificar_stock(nombre_menu):
            self.pedido.append(nombre_menu)
            self.menus_creados.append(nombre_menu)
            # Descontar el stock
            recetas = {
                'papas fritas': {'papas': 2},  
                'hamburguesas': {'hamburguesa': 1, 'churrasco': 2, 'lamina queso': 1},
                'completos': {'vienesa': 1, 'pan completo': 1, 'tomate': 1, 'palta': 1},
                'pepsi': {'bebida': 1}
            }
            ingredientes_necesarios = recetas.get(nombre_menu, {})
            for ingrediente, cantidad_necesaria in ingredientes_necesarios.items():
                self.stock = [Ingrediente(ing.nombre, ing.cantidad - cantidad_necesaria) if ing.nombre == ingrediente else ing for ing in self.stock]
            return True
        return False
