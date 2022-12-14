import pygame
from tablero import Tablero
from const import *
from arrastrador import Arrastrador

class Juego:

    def __init__(self):
        self.sig_jugador = 'blanco'
        #Haciendo una referencia a board
        self.tablero = Tablero()
        #Haciendo una referencia a dragger
        self.arrastrador = Arrastrador()

    #Métodos para mostrar
    def mostrar_bg(self, superficie):
        for fila in range(FILAS):
            for col in range(COLS):
                if  (fila + col) % 2 == 0:
                    color = '#ebf0fe' #Blanco
                else:
                    color = '#b6cafb' #Negro


                #Creando el elemento de rectángulo, incluye las posiciones x, y, así como la altura y anchura  
                rect = (col * TCUAD, fila * TCUAD, TCUAD, TCUAD)

                #Dibujando el rectangulo, los parámetros necesarios son la superficie (en este caso la pantalla), que será definida en main.py
                #El color, que dependerá de la posición en el tablero y la posición y dimensiones que definimos anteriormente
                pygame.draw.rect(superficie, color, rect)


    def mostrar_piezas(self, superficie):
        for fila in range(FILAS):
            for col in range(COLS):

                #Checando si hay una pieza en el cuadrado
                if self.tablero.cuadros[fila][col].tiene_pieza():
                    #Guardando la pieza en una variable
                    pieza = self.tablero.cuadros[fila][col].pieza

                    #Todas las piezas excepto la que está siendo arrastrada
                    if pieza is not self.arrastrador.pieza:
                        pieza.poner_textura(size=80)
                        #Convirtiendo la textura en una imágen con pygame
                        img = pygame.image.load(pieza.textura)
                        #Creando una variable para centrar la imágen
                        img_center = col * TCUAD + TCUAD // 2, fila * TCUAD + TCUAD // 2
                        #definiendo pieza.textura_rect como la imágen centrada
                        pieza.textura_rect = img.get_rect(center = img_center)
                        #Dibujando la imagen creada dentro del textura_rect
                        superficie.blit(img, pieza.textura_rect)

    def mostrar_movs(self, superficie):
        if self.arrastrador.arrastrando:
            pieza = self.arrastrador.pieza

            #Iterar todos los valores válidos
            for mov in pieza.movs:
                #Color
                color = '#f98b8b' if (mov.final.fila + mov.final.col) % 2 == 0 else '#f65555'
                #Rect
                rect = (mov.final.col * TCUAD, mov.final.fila * TCUAD, TCUAD, TCUAD)
                #Blit
                pygame.draw.rect(superficie, color, rect)

    def mostrar_ultimo_mov(self, superficie):
        if self.tablero.ultimo_mov:
            inicial = self.tablero.ultimo_mov.inicial
            final = self.tablero.ultimo_mov.final

            for pos in [inicial, final]:
                #color
                color = '#fbf0bb' if (pos.fila + pos.col) % 2 == 0 else '#f9e685'
                #rect
                rect = (pos.col * TCUAD, pos.fila * TCUAD, TCUAD, TCUAD )
                #blit
                pygame.draw.rect(superficie, color, rect)
    #Otros métodos

    def sig_turno(self):
        self.sig_jugador = 'blanco' if self.sig_jugador == 'negro' else 'negro'

    def reset(self):
        self.__init__()