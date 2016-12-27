'''
http://aventurapygame.blogspot.com.es/2011/10/el-personaje.html
'''

# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame
import Juego, escenario, utils


# listado de personajes:
_spritesinfo = {
    'Cris':{'actionlist':['mov1_N', 'mov1_O', 'mov1_S', 'mov1_E', 
                'mov2_N', 'mov2_O', 'mov2_S', 'mov2_E',
                'camina_N', 'camina_O', 'camina_S', 'camina_E', 
                'mov3_N', 'mov3_O', 'mov3_S', 'mov3_E',
                'mov4_N', 'mov4_O', 'mov4_S', 'mov4_E',
                'muere'],
            'nsprites':[7,7,7,7,8,8,8,8,9,9,9,9,6,6,6,6,13,13, 13, 13, 6], # sprites por linea del tileset.
            'rectval':[+22, +20, -42, -23], # cuadrado de srpite válido para colisiones
            'tileH':64, 
            'tileW':64, 
            'path':'imagenes\CrisSheet.png'},
    'Otro':{},
    'Otro2':{}
    }


class Personaje(pygame.sprite.Sprite):
  

    def __init__(self, personaje):
        spriteinfo = _spritesinfo[personaje]

        # Tileset con la animación del personaje.
        self.path = spriteinfo['path']
        self.tileW = spriteinfo['tileW']
        self.tileH = spriteinfo['tileH']
        self.tileset = utils.cortar_charset(self.path, self.tileW, self.tileH)
        self.posX = 0
        self.posY = 0
        # diccionario con {acción:[sprites]}
        self.sprites_accion={}
        for n in range(0, len(self.tileset)):
            charsheet = []
            for l in range(0, (spriteinfo['nsprites'][n])): 
                charsheet.append(self.tileset[n][l])        
            self.sprites_accion[spriteinfo['actionlist'][n]] = charsheet


        # Para cuadrar el personaje en el bloque.
        self.offset = (0,0)
        
        # Posición inicial del personaje en el mapa.
        # desde archivo escenario.py

        # contador de posición de sprite.
        self.cont = 0

        # charsheet a representar
        self.action = 'camina_S' # acción actual
        self.image = self.sprites_accion['camina_S'][self.cont] # sprite actual

        # rectángulo del personaje.
        self.rectval = spriteinfo['rectval']
        self.rect = pygame.Rect(self.posX, self.posY, self.tileW, self.tileH)
        self.rectcolision= pygame.Rect(
            self.posX+self.rectval[0], self.posY+self.rectval[1], 
            self.tileW+self.rectval[2], self.tileH+self.rectval[3])

        
    def mover(self, nuevaaccion):

        # Actualiza sprite con la dirección adecuada
        if self.cont > (len(self.sprites_accion[nuevaaccion])-1):
            self.cont = 0

        if nuevaaccion[:4] != self.action[:4]:
            self.cont = 0
        self.action = nuevaaccion

        self.image = self.sprites_accion[nuevaaccion][self.cont]
        self.cont += 1
        # actualizar resctángulos del personaje
        self.rectcolision= pygame.Rect(
            self.posX+self.rectval[0], self.posY+self.rectval[1], 
            self.tileW+self.rectval[2], self.tileH+self.rectval[3])
        self.rect = pygame.Rect(self.posX, self.posY, self.tileW, self.tileH)


        # control
        print ('\nsprite image: ',self.cont)
        print ('sprite.rect', self.rect)
        print (self.action)
        print ('Pos: x %i y %i' %(self.posX, self.posY))

    def dibujar_personaje(self, destino):
        # Dibujamos el tile correspondiente de Cris.
        destino.blit(self.image, (self.posX - self.offset[0], self.posY - self.offset[1]))
        

