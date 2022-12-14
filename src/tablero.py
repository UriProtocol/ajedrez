from const import *
from cuadrado import Cuadrado
from pieza import *
from movimiento import mov

class Tablero:

    def __init__(self):
        #Creando un arreglo bidimensional que representa cada cuadrado del tablero de ajedrez, contiene 8 arreglos que representan cada fila y 8 elementos dentro de cada arreglo que representan cada 
        self.cuadros = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self._create()
        self.ultimo_mov = None
        self._agregar_piezas('blanco')
        self._agregar_piezas('negro')

    def mover(self, pieza, mov):
        inicial = mov.inicial
        final = mov.final

        #
        self.cuadros[inicial.fila][inicial.col].pieza = None
        self.cuadros[final.fila][final.col].pieza = pieza

        #Coronación del peón
        if isinstance(pieza, Peon):
            self.checar_coronacion(pieza, final)

        #movimiento
        pieza.movido = True

        #limpiar movimientos válidos
        pieza.limpiar_movs()

        #Definir último movimiento
        self.ultimo_mov = mov

    def mov_valido(self, pieza, mov):
        return mov in pieza.movs

    def checar_coronacion(self, pieza, final):
        if final.fila == 0 or final.fila == 7:
            self.cuadros[final.fila][final.col].pieza = Reina(pieza.color)

    #Calcular todos los movimientos validos de una pieza en específico en una posición en específico
    def calc_movs(self, pieza, fila, col):

        #Falta el movimiento "en passant" por ahora
        def mov_peon():
            #Ver cuantos pasos puede dar el peon, si no se ha movido de la posición inicial puede dar 2
            pasos = 1 if pieza.movido else 2
            #mov verticales
            inicio = fila + pieza.dir
            fin = fila + (pieza.dir * (1 + pasos))
            for mov_fila in range(inicio, fin, pieza.dir):
                if Cuadrado.en_rango(mov_fila):
                    if self.cuadros[mov_fila][col].vacio():
                        #Crear cuadrados de movimiento inicial y final
                        inicial = Cuadrado(fila, col)
                        final = Cuadrado(mov_fila, col)
                        #Crear un nuevo movimiento
                        movimiento = mov(inicial, final)
                        pieza.agregar_mov(movimiento)
                    #bloqueado
                    else: break
                #fuera de rango
                else: break

            #Movimientos diagonales
            #Solo se puede mover un espacio diagonalmente, así que no necesitamos agregar la variable de pasos
            mov_posible_fila = fila + pieza.dir
            #Las colimnas posibles a las que nos podemos mover son: la columna inmediatamente a la derecha o inmediatamente a la izquierda (col+1, col-1)
            mov_posible_cols = [col-1, col+1]
            #Iterando sobre las dos columnas laterales posibles para ver cual de los dos movimientos es posible
            for mov_posible_col in mov_posible_cols:
                if Cuadrado.en_rango(mov_posible_fila, mov_posible_col):
                    if self.cuadros[mov_posible_fila][mov_posible_col].tiene_pieza_enemiga(pieza.color):
                        #Crear cuadrados de movimiento inicial y final
                        inicial = Cuadrado(fila, col)
                        final = Cuadrado(mov_posible_fila, mov_posible_col)
                        #Crear un nuevo movimiento
                        movimiento = mov(inicial, final)
                        #Añadiendo el movimiento
                        pieza.agregar_mov(movimiento) 

        #Método que contiene los movimientos de un caballo
        def mov_caballo():
            #8 movimientos posibles
            mov_posibles = [
                (fila-2, col+1),
                (fila-1, col+2),
                (fila+1, col+2),
                (fila+2, col+1),
                (fila+2, col-1),
                (fila+1, col-2),
                (fila-1, col-2),
                (fila-2, col-1),
            ]

            for mov_posible in mov_posibles:
                mov_posibles_fila, mov_posibles_col = mov_posible

                if Cuadrado.en_rango(mov_posibles_fila, mov_posibles_col):
                    if self.cuadros[mov_posibles_fila][mov_posibles_col].vacio_o_enemiga(pieza.color):
                        # Creando cuadrados del nuevo movimiento
                        inicial = Cuadrado(fila, col)
                        final = Cuadrado(mov_posibles_fila, mov_posibles_col) # pieza=pieza
                        # Creando el movimiento
                        movimiento = mov(inicial, final)
                        #Agregando un nuevo movimiento válido
                        pieza.agregar_mov(movimiento)

                        
        def mov_linea_recta(incrs):
            for incr in incrs:
                fila_incr, col_incr = incr
                mov_posible_fila = fila + fila_incr
                mov_posible_col = col + col_incr

                while True:
                    if Cuadrado.en_rango(mov_posible_fila, mov_posible_col):
                        #Crear cuadrados de el posible nuevo movimiento
                        inicial = Cuadrado(fila, col)
                        final = Cuadrado(mov_posible_fila, mov_posible_col)
                        #Crer nuevo movimiento posible
                        movimiento = mov(inicial, final)
                        #Cuadrado vacío, sigue avanzando
                        if self.cuadros[mov_posible_fila][mov_posible_col].vacio():
                            #Agregar nuevo movimiento
                            pieza.agregar_mov(movimiento)
                        #Cuadrado con pieza enemiga, agrega movimiento y después se detiene
                        if self.cuadros[mov_posible_fila][mov_posible_col].tiene_pieza_enemiga(pieza.color):
                            #Agregar nuevo movimiento
                            pieza.agregar_mov(movimiento)
                            break
                        #Cuadrado tiene pieza amiga, se detiene
                        if self.cuadros[mov_posible_fila][mov_posible_col].tiene_pieza_amiga(pieza.color):
                            break

                    #Fuera del rango
                    else: break
                    #Incrementos
                    mov_posible_fila = mov_posible_fila + fila_incr
                    mov_posible_col = mov_posible_col + col_incr    

        #Falta enroque por ahora
        def mov_rey():
            #Todos los cuadrados adyacentes
            adys = [
                (fila - 1, col + 1), #arriba-derecha
                (fila - 1, col - 1), #arriba-izquierda
                (fila + 1, col - 1), #abajo-izquierda
                (fila + 1, col + 1), #abajo-derecha
                (fila - 1, col + 0), #arriba
                (fila + 0, col + 1), #derecha
                (fila + 1, col + 0), #abajo
                (fila + 0, col - 1) #izquierda
            ]

            for mov_posible in adys:
                mov_posible_fila, mov_posible_col = mov_posible

                if Cuadrado.en_rango(mov_posible_fila, mov_posible_col):
                    if self.cuadros[mov_posible_fila][mov_posible_col].vacio_o_enemiga(pieza.color):

                        inicial = Cuadrado(fila, col)
                        final = Cuadrado(mov_posible_fila, mov_posible_col)
                        movimiento = mov(inicial, final)
                        pieza.agregar_mov(movimiento)


        #Calcular los todos los movimientos de un peon
        if isinstance(pieza, Peon):
            mov_peon() 
        #Calcular los todos los movimientos de un caballo
        elif isinstance(pieza, Caballo):
            mov_caballo()
        #Calcular los todos los movimientos de un alfil
        elif isinstance(pieza, Alfil):
            mov_linea_recta([
                (-1, 1), #arriba-derecha
                (-1, -1), #arriba-izquierda
                (1, -1), #abajo-izquierda
                (1, 1) #abajo-derecha
            ])
        #Calcular los todos los movimientos de una torre
        elif isinstance(pieza, Torre):
            mov_linea_recta([
                (-1, 0), #arriba
                (0, 1), #derecha
                (1, 0), #abajo
                (0, -1) #izquierda
            ])
        #Calcular los todos los movimientos de una Reina
        elif isinstance(pieza, Reina):
            mov_linea_recta([
                (-1, 1), #arriba-derecha
                (-1, -1), #arriba-izquierda
                (1, -1), #abajo-izquierda
                (1, 1), #abajo-derecha
                (-1, 0), #arriba
                (0, 1), #derecha
                (1, 0), #abajo
                (0, -1) #izquierda
            ])
        #Calcular los todos los movimientos de un Rey
        elif isinstance(pieza, Rey):
            mov_rey()

        
    def _create(self):
        print(self.cuadros)

        #Asignando unn objeto Cuadrado a cada elemento del arreglo cuadros
        for fila in range(FILAS):
            for col in range(COLS):
                self.cuadros[fila][col] = Cuadrado(fila, col)

    def _agregar_piezas(self, color):
        #Si el color de las piezas es blanco, la fila de los peones será la 6 y la de las otras piezas será la 7 (penúltima y última)
        #Si el color de las piezas es negro, la fila de los peones será la 1 y la de las otras piezas será la 0 (segunda y primera)
        fila_peon, fila_otro = (6, 7) if color == 'blanco' else (1, 0)

        # Peones
        for col in range(COLS):
            self.cuadros[fila_peon][col] = Cuadrado(fila_peon, col, Peon(color))
            


        # Torres
        self.cuadros[fila_otro][0] = Cuadrado(fila_otro, 0, Torre(color))
        self.cuadros[fila_otro][7] = Cuadrado(fila_otro, 7, Torre(color))

        # Caballos
        self.cuadros[fila_otro][1] = Cuadrado(fila_otro, 1, Caballo(color))
        self.cuadros[fila_otro][6] = Cuadrado(fila_otro, 6, Caballo(color))

        # Alfiles
        self.cuadros[fila_otro][2] = Cuadrado(fila_otro, 2, Alfil(color))
        self.cuadros[fila_otro][5] = Cuadrado(fila_otro, 5, Alfil(color))

        # Reina
        self.cuadros[fila_otro][3] = Cuadrado(fila_otro, 3, Reina(color))

        # Rey
        self.cuadros[fila_otro][4] = Cuadrado(fila_otro, 4, Rey(color))


        

Tablero()._create()