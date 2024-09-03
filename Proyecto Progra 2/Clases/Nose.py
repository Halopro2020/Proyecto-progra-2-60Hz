from Clases import Seno

class Biblioteca:
    def __init__(self):
        self.lista_libros = []

    def agregar_ingrediente(self, libro):
        # Buscar si el libro ya existe en la lista
        for lib in self.lista_libros:
            if lib.nombre == libro.nombre:
                # Si el libro ya existe, actualizar la cantidad
                lib.cantidad += libro.cantidad
                return True  # Cantidad actualizada
        
        # Si el libro no existe, agregarlo a la lista
        self.lista_libros.append(libro)
        return True  # Libro agregado como nuevo

    def eliminar_ingrediente(self, Nombre,  Cantidad):
        for lib in self.lista_libros:
            if lib.nombre == Nombre:
                if lib.cantidad > int(Cantidad):
                    # Reducir la cantidad en lugar de eliminar el libro
                    lib.cantidad -= int(Cantidad)
                else:
                    # Si la cantidad es menor o igual, eliminar el libro
                    self.lista_libros.remove(lib)
                return True
        return False

    def obtener_ingredientes(self):
        return [libro for libro in self.lista_libros]
