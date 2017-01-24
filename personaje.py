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
    'Piti':{'actionlist':['mov1_N', 'mov1_O', 'mov1_S', 'mov1_E', 
                'mov2_N', 'mov2_O', 'mov2_S', 'mov2_E',
                'camina_N', 'camina_O', 'camina_S', 'camina_E', 
                'mov3_N', 'mov3_O', 'mov3_S', 'mov3_E',
                'mov4_N', 'mov4_O', 'mov4_S', 'mov4_E',
                'muere'],
            'nsprites':[7,7,7,7,8,8,8,8,9,9,9,9,6,6,6,6,13,13, 13, 13, 6], # sprites por linea del tileset.
            'rectval':[+22, +20, -42, -23], # cuadrado de sprite válido para colisiones
            'tileH':64, 
            'tileW':64, 
            'path':'utilidades\imagenes\PitiSheet.png'},
    'Otro2':{}
    }


class Personaje(pygame.sprite.Sprite):
    ''' Clase padre de personajes '''

    orientacion = {'N':(0, -2), 'S':(0, 2), 'E':(2, 0), 'O':(-2, 0)}
  

    def __init__(self, personaje):
        print ("....Creando personaje " + personaje + '...')
        global spriteinfo
        spriteinfo = _spritesinfo[personaje]

        # Tileset con la animación del personaje.
        self.tileW = spriteinfo['tileW']
        self.tileH = spriteinfo['tileH']
        self.tileset = utils.cortar_charset(spriteinfo['path'], self.tileW, self.tileH)
        self.pos = [0, 0] # posición del personaje en la pantalla.
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
      
        # lista con los mensajes para el modo test:
        self.test = ['']

        #########################################################
        ################ - Control del sprite - #################
        #########################################################

    def actualizar_sprite(self, nuevaaccion):
        ''' Actualiza el sprite adecuado según la acción. '''

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
        self.test[0]=str(' - Acción: ' + self.action)


    def dibujar_personaje(self, surface):
        # Dibujamos el tile correspondiente de Cris.
        print (self.pos) ###
        posicion = (self.pos[0]-self.offset[0], self.pos[1]-self.offset[1])
        surface.blit(self.image, posicion)

        # añadir expresión


        #########################################################
        ############# - Acciones del personaje.  ################
        #########################################################

    def expresa(self, texto, icono=False):
        ''' Bocadillo sobre el sprite que dice algo '''
        None



