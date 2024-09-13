class Guardar_ingrediente:
    def __init__(self):
        self.lista_ingredientes = []

    def agregar_ingrediente(self, ingrediente):
        for ing in self.lista_ingredientes:
            if ing.nombre == ingrediente.nombre:
                ing.cantidad += ingrediente.cantidad
                return True
        self.lista_ingredientes.append(ingrediente)
        return True

    def eliminar_ingrediente(self, Nombre, Cantidad):
        for lib in self.lista_ingredientes:
            if lib.nombre == Nombre:
                if lib.cantidad > int(Cantidad):
                    lib.cantidad -= int(Cantidad)
                else:
                    self.lista_ingredientes.remove(lib)
                return True
        return False

    # Este método ahora devuelve una lista de objetos Ingrediente
    def obtener_ingredientes(self):
        return self.lista_ingredientes
