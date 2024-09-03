from Clases import Ingredientes

class Guardar_ingrediente:
    def __init__(self):
        self.lista_ingredientes = []

    def agregar_ingrediente(self, ingrediente):
        # Buscar si el ingrediente ya existe en la lista
        for lib in self.lista_ingredientes:
            if lib.nombre == ingrediente.nombre:
                # Si el ingrediente ya existe, actualizar la cantidad
                lib.cantidad += ingrediente.cantidad
                return True  # Cantidad actualizada
        
        # Si el ingrediente no existe, agregarlo a la lista
        self.lista_libros.append(ingrediente)
        return True  # ingrediente agregado como nuevo

    def eliminar_ingrediente(self, Nombre,  Cantidad):
        for lib in self.lista_ingredientes:
            if lib.nombre == Nombre:
                if lib.cantidad > int(Cantidad):
                    # Reducir la cantidad en lugar de eliminar el ingrediente
                    lib.cantidad -= int(Cantidad)
                else:
                    # Si la cantidad es menor o igual, eliminar el ingrediente
                    self.lista_ingredientes.remove(lib)
                return True
        return False

    def obtener_ingredientes(self):
        return [libro for libro in self.lista_ingredientes]
