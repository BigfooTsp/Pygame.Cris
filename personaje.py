# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame
from utilidades import utils


# listado de personajes:
_spritesinfo = {
    'Cris':{'actionlist':['mov1_N', 'mov1_O', 'mov1_S', 'mov1_E', 
                'mov2_N', 'mov2_O', 'mov2_S', 'mov2_E',
                'camina_N', 'camina_O', 'camina_S', 'camina_E', 
                'mov3_N', 'mov3_O', 'mov3_S', 'mov3_E',
                'mov4_N', 'mov4_O', 'mov4_S', 'mov4_E',
                'muere'],
            'nsprites':[7,7,7,7,8,8,8,8,9,9,9,9,6,6,6,6,13,13, 13, 13, 6], # sprites por linea del tileset.
            'rectval':[+22, +20, -42, -23], # cuadrado de sprite válido para colisiones
            'tileH':64, 
            'tileW':64, 
            'path':'utilidades\imagenes\CrisSheet.png'},
    'Otro':{},
    'Otro2':{}
    }


class Personaje(pygame.sprite.Sprite):

    orientacion = {'N':(0, -2), 'S':(0, 2), 'E':(2, 0), 'O':(-2, 0)}
  

    def __init__(self, personaje):
        print ("Creando personaje " + personaje + '...')
        global spriteinfo
        spriteinfo = _spritesinfo[personaje]

        # Tileset con la animación del personaje.
        self.tileW = spriteinfo['tileW']
        self.tileH = spriteinfo['tileH']
        self.tileset = utils.cortar_charset(spriteinfo['path'], self.tileW, self.tileH)
        self.pos = [0, 0]
        self.offset = (spriteinfo['rectval'][0], spriteinfo['rectval'][1])
        self.sprites_accion={} # diccionario con {acción:[sprites]}
        for n in range(0, len(self.tileset)):
            charsheet = []
            for l in range(0, (spriteinfo['nsprites'][n])): 
                charsheet.append(self.tileset[n][l])        
            self.sprites_accion[spriteinfo['actionlist'][n]] = charsheet
        
        self.cont = 0 # contador de posición de sprite.
        self.action = 'camina_S' # acción actual
        self.image = self.sprites_accion['camina_S'][self.cont] # sprite actual

        # rectángulo del personaje  (posición relativa, cámara).
        self.rect = pygame.Rect(
            self.pos[0]+spriteinfo['rectval'][0], self.pos[1]+spriteinfo['rectval'][1], 
            self.tileW+spriteinfo['rectval'][2], self.tileH+spriteinfo['rectval'][3])
     
   
    def mover(self, nuevaaccion):
        # Actualiza el sprite adecuado según la orientación.
        if self.cont > (len(self.sprites_accion[nuevaaccion])-1):
            self.cont = 0

        if nuevaaccion[:4] != self.action[:4]:
            self.cont = 0
        self.action = nuevaaccion

        self.image = self.sprites_accion[nuevaaccion][self.cont]
        self.cont += 1
        
        # actualizar rectángulo del personaje
        self.rect.topleft = (self.pos[0], self.pos[1])
        
        # control
        print ('\nsprite image: ',self.cont)
        print (self.action)
        print ('Pos: x %i y %i' %(self.pos[0], self.pos[1]))


    def dibujar(self, destino):
        # Dibujamos el tile correspondiente de Cris.
        destino.blit(self.image, (self.pos[0]-self.offset[0], self.pos[1]-self.offset[1]))
