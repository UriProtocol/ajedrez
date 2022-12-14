#Modulo os que utilizaremos para acceder a archivos en otra carpeta
import os
# Creando la clase pieza
class Pieza:
    #Propiedad init con los atributos de la pieza
    def __init__(self, nombre, color, valor, textura=None, textura_rect=None):
        self.nombre = nombre
        self.color = color
        #Signo del valor para la IA, el valor será positivo para las piezas blancas y negativo para las negras.
        value_sign = 1 if color == 'blanco' else -1
        self.valor = valor * value_sign
        #Movimientos válidos
        self.movs = []
        self.movido = False
        self.textura = textura
        self.poner_textura()
        self.textura_rect = textura_rect
        
    #Método para agregar la textura dependiendo del tipo de pieza
    def poner_textura(self, size=80):
        self.textura = os.path.join(
            f'recursos/imagenes/imgs-{size}px/{self.color}_{self.nombre}.png'
        )
    #Método para agregar movimientos de una pieza
    def agregar_mov(self, move):
        self.movs.append(move)
    
    def limpiar_movs(self):
        self.movs = []

#Creando la clase peón que hereda a la clase pieza
class Peon(Pieza):

    def __init__(self, color):
        #Operador ternario, si el color de la pieza es blanco, la dirección será -1 (en pygame significa hacia arriba), en caso de que sea negra, será 1
        self.dir = -1 if color == 'blanco' else 1
        #Extendiendo la funcionalidad de la propiedad init de la clase pieza, asignamos el nombre, el color y el valor 
        super().__init__('peon', color, 1.0)

#Creando la clase caballo que hereda a la clase pieza
class Caballo(Pieza):

    def __init__(self, color):
        super().__init__('caballo', color, 3.0)

#Creando la clase alfil que hereda a la clase pieza
class Alfil(Pieza):

    def __init__(self, color):
        super().__init__('alfil', color, 3.001)

#Creando la clase torre que hereda a la clase pieza
class Torre(Pieza):

    def __init__(self, color):
        super().__init__('torre', color, 5.0)

#Creando la clase Reina que hereda a la clase pieza
class Reina(Pieza):

    def __init__(self, color):
        super().__init__('reina', color, 9.0)

class Rey(Pieza):

    def __init__(self, color):
        super().__init__('rey', color, 10000.0)
