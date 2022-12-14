import pygame

from const import *

class Arrastrador:

    def __init__(self):
        self.pieza = None
        self.arrastrando = False
        #Eje X del mouse
        self.mouseX = 0
        #Eje Y del mouse
        self.mouseY = 0
        self.fila_inicial = 0
        self.col_inicial = 0
    
    #Método blit
    
    #Método para hacer a la pieza un poco más grande si se está seleccionando
    def act_blit(self, surface):
        #textura
        self.pieza.poner_textura(size=100)
        textura = self.pieza.textura
        #imagen
        img = pygame.image.load(textura)
        #rect
        img_center = (self.mouseX, self.mouseY)
        #Centrar la imágen en el cursor
        self.pieza.textura_rect = img.get_rect(center=img_center)
        #blit
        surface.blit(img, self.pieza.textura_rect)

    #Otros métodos


    def act_mouse(self, pos):

        #Coordinada x y coordinada Y
        self.mouseX, self.mouseY = pos
    
    def guardar_inicial(self, pos):
        self.fila_inicial = pos[1] // TCUAD
        self.col_inicial = pos[0] // TCUAD

    def arrastrar_pieza(self, pieza):
        self.pieza = pieza
        self.arrastrando = True
    
    def soltar_pieza(self):
        self.pieza = None
        self.arrastrando = False
        



