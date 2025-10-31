class Producto:
    def __init__(self, codigo, nombre, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio

class Extintor(Producto):
    def __init__(self, codigo, nombre, precio, tipo, capacidad):
        super().__init__(codigo,nombre, precio)
        self.tipo = tipo
        self.capacidad = capacidad
