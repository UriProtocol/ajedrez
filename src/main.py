#Antes de iniciar el proyecto debemos de instalar el paquete pygame (pip install -U pygame --user en la terminal)
import pygame
#importando el módulo sys par poder salir del programa 
import sys
#Importando el archivo const.py
from const import *
#Importando la clase game de game.py
from juego import Juego
#Importando la clase cuadrado de cuadrado.py
from cuadrado import Cuadrado
#Importando la clase mov de movimiento.py
from movimiento import mov

class Main:
    def __init__(self):
        #Inicializando el modelo pygame
        pygame.init()
        #Creando la pantalla de pygame
        self.pantalla = pygame.display.set_mode((ANCHURA, ALTURA))
        pygame.display.set_caption('Ajedrez')
        #Referencia a la clase game
        self.juego = Juego()


    def mainloop(self):
            
        pantalla = self.pantalla
        
        #Guardando algunos atributos en variables
        juego = self.juego
        tablero = self.juego.tablero
        arrastrador = self.juego.arrastrador

        while True:
            #Llamando a la función de Game para dibujar el tablero
            juego.mostrar_bg(pantalla)
            #Mostrar el último mov
            juego.mostrar_ultimo_mov(pantalla)
            #Mostrando los movimientos
            juego.mostrar_movs(pantalla)
            #Mostrando las piezas en la pantalla
            juego.mostrar_piezas(pantalla)

            #Superponiendo la pieza arrastrada
            if arrastrador.arrastrando:
                arrastrador.act_blit(pantalla)
            #Función para salir de la aplicación
            for event in pygame.event.get():

                #Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    arrastrador.act_mouse(event.pos)

                    clicked_fila = arrastrador.mouseY // TCUAD
                    clicked_col = arrastrador.mouseX // TCUAD

                    #Si el cuadrado clickeado tiene una pieza
                    if tablero.cuadros[clicked_fila][clicked_col].tiene_pieza():
                        pieza = tablero.cuadros[clicked_fila][clicked_col].pieza
                        #Pieza valida (color)
                        if pieza.color == juego.sig_jugador:

                            tablero.calc_movs(pieza, clicked_fila, clicked_col)
                            arrastrador.guardar_inicial(event.pos)
                            arrastrador.arrastrar_pieza(pieza)
                            #mostrar métodos
                            juego.mostrar_bg(pantalla)
                            juego.mostrar_movs(pantalla)
                            juego.mostrar_piezas(pantalla)


                #Movimiento del mouse
                elif event.type == pygame.MOUSEMOTION:
                    if arrastrador.arrastrando:
                        arrastrador.act_mouse(event.pos)
                        juego.mostrar_bg(pantalla)
                        juego.mostrar_ultimo_mov(pantalla)
                        juego.mostrar_movs(pantalla)
                        juego.mostrar_piezas(pantalla)
                        arrastrador.act_blit(pantalla)

                #Levantamiento del mouse
                elif event.type == pygame.MOUSEBUTTONUP:

                    if arrastrador.arrastrando:
                        arrastrador.act_mouse(event.pos)

                        fila_soltada = arrastrador.mouseY // TCUAD
                        col_soltada = arrastrador.mouseX // TCUAD

                        #crear movimiento posible
                        inicial = Cuadrado(arrastrador.fila_inicial, arrastrador.col_inicial)
                        final = Cuadrado(fila_soltada, col_soltada)
                        movimiento = mov(inicial, final)

                        #Es movimiento válido?
                        if tablero.mov_valido(arrastrador.pieza, movimiento):
                            tablero.mover(arrastrador.pieza, movimiento)
                            #métodos de mostrar
                            juego.mostrar_bg(pantalla)
                            juego.mostrar_ultimo_mov(pantalla)
                            juego.mostrar_piezas(pantalla)

                            #Siguiente turno
                            juego.sig_turno()


                    arrastrador.soltar_pieza()
                #Salir de la aplicación
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            #Actualizar el display
            pygame.display.update()


main = Main()
main.mainloop()