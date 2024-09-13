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

    def eliminar_ingrediente(self, nombre, cantidad):
        for ing in self.lista_ingredientes:
            if ing.nombre == nombre:
                if ing.cantidad > cantidad:
                    ing.cantidad -= cantidad
                else:
                    self.lista_ingredientes.remove(ing)  # Elimina el ingrediente si la cantidad es igual o menor
                return True
        return False


    # Este método ahora devuelve una lista de objetos Ingrediente
    def obtener_ingredientes(self):
        return self.lista_ingredientes
