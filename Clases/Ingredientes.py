class Ingrediente:
    def __init__(self, nombre, cantidad):
        self.nombre = nombre
        self.cantidad = cantidad

    def __repr__(self):
        return f"Ingrediente(nombre={self.nombre}, cantidad={self.cantidad})"
