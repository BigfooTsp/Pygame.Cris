'''
http://aventurapygame.blogspot.com.es/2011/10/el-personaje.html
'''

# -*- coding: utf-8 -*-

from pygame.locals import * # [.] ????
import pygame
from utils import tiles
import Juego


class Personaje(pygame.sprite.Sprite):

    #############################################################
    ########## Analisis del charsheet del personaje #############
    # [.] Crear un generador de personajes con estas info.

    actionlist = ['mov1_N', 'mov1_O', 'mov1_S', 'mov1_E', 
                'mov2_N', 'mov2_O', 'mov2_S', 'mov2_E',
                'camina_N', 'camina_O', 'camina_S', 'camina_E', 
                'mov3_N', 'mov3_O', 'mov3_S', 'mov3_E',
                'mov4_N', 'mov4_O', 'mov4_S', 'mov4_E',
                'muere']
    # sprites con imagen en la fila del tilesheet.
    nsprites = [7,7,7,7,8,8,8,8,9,9,9,9,6,6,6,6,13,13, 13, 13, 6]

    TILE_ALTO = 64
    TILE_ANCHO = 64

    path = 'imagenes\CrisSheet.png'

    ############################################################

    # referencias de self.direcciones
    NORTE = 0
    SUR = 1
    ESTE = 2
    OESTE = 3


    def __init__(self, path=path, TILE_ALTO=TILE_ALTO, TILE_ANCHO=TILE_ANCHO):

        # Tileset con la animación del personaje.
        self.tileset = tiles.cortar_tileset(path, TILE_ALTO, TILE_ANCHO)

        # diccionario con {acción:(sprites)}
        self.sprites_accion={}
        for n in range(0, len(self.tileset)):
            charsheet = []
            for l in range(0, (self.nsprites[n])): 
                charsheet.append(self.tileset[n][l])        
            self.sprites_accion[self.actionlist[n]] = charsheet


        # Para cuadrar el personaje en el bloque.
        self.offset = (0,0)
        
        # Posición actual del personaje en el mapa.
        self.fila = 0
        self.columna = 0 

        # contador de posición de sprite.
        self.cont = 0

        # charsheet a representar
        self.action = 'camina_S' # acción actual
        self.orientation = Personaje.SUR # orientación actual
        self.sprite = self.sprites_accion['camina_S'][self.cont] # sprite actual
        #self.rect = self.sprite.get_rect()

        
    def update(self, nuevaaccion):

        self.actualizar_posicion(nuevaaccion)


    def actualizar_posicion(self, nuevaaccion):
        # poniendo máximo contador cantidad de sprites validos.
        if self.cont > (len(self.sprites_accion[nuevaaccion])-1):
            self.cont = 0
        # resetear contador de sprite si acción es diferente.
        if nuevaaccion[:4] != self.action[:4]:
            self.cont = 0
        self.action = nuevaaccion
        # actualiza sprite del personaje.
        print ('Control: ',self.cont)
        print (self.action)
        self.sprite = self.sprites_accion[nuevaaccion][self.cont]
        self.cont += 1


    def dibujar(self, destino):

        # Dibujamos el tile correspondiente de Cris.
        destino.blit(self.sprite, (self.fila - self.offset[0], self.columna - self.offset[1]))


