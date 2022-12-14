class Cuadrado:
    #Propiedad init con los atributos de posicion y el atributo pieza con un valor por defecto de None
    def __init__(self, fila, col, pieza=None):
        self.fila = fila
        self.col = col
        self.pieza = pieza
    
    def __eq__(self, other):
        return self.fila == other.fila and self.col == other.col
         
    def tiene_pieza(self):
        return self.pieza != None

    def vacio(self):
        return not self.tiene_pieza()

    def tiene_pieza_amiga(self, color):
        #Checando si tiene una pieza y si el color de la pieza es igual a nuestro color
        return self.tiene_pieza() and self.pieza.color == color

    def tiene_pieza_enemiga(self, color):
        #Checando si tiene una pieza y si el color de la pieza es diferente a nuestro color
        return self.tiene_pieza() and self.pieza.color != color

    def vacio_o_enemiga(self, color):
        return self.vacio() or self.tiene_pieza_enemiga(color)
    #Un método estático puede ser llamado directamente con el nombre de clase sin necesidad de instanciarlo
    @staticmethod
    #Método para verificar si un movimiento se encuentra dentro del rango del tablero, acepta cualquier número de argumentos
    def en_rango(*args):
        for arg in args:
            #0 y 7 son los límites del tablero
            if arg < 0 or arg > 7:
                return False
            
        return True