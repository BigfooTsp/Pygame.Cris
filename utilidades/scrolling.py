'''
Gestión del scroll de pantalla y cámara.

Indica la porción del mapa que se presenta en pantalla y las posiciones relativas
al personaje principal de los elementos de esta.

También funciones que muestren la posición equivalente entre absoluta y relativa. 
posición relativa: La mostrada en la cámara (scroll)
posición absoluta: La posición en el mapa, usada en colisiones.

'''
import pygame
from utilidades import utils
import escenario



class Camara:
    ''' crea un objeto 'camara' que se enviará al mapa indicándole que rango
    de tiles debe de dibujar según la posición del personaje y el tamaño
    de la pantalla. También dibuja los objetos y personajes.'''


    def __init__(self, screen, mapa):
        global screen_w, screen_h, mapa_sizex, mapa_sizey
        print ('....Creando objeto camara para scroll.')

        # Mapa
        self.mapa = mapa
        mapa_sizex = self.mapa._mapa_size[0]
        mapa_sizey = self.mapa._mapa_size[1]
        mapa_size = (mapa_sizex, mapa_sizey)
        
        # Pantalla
        self.screen = screen
        screen_size = self.screen.get_size()
        screen_w = screen_size[0]
        screen_h = screen_size[1]

        # lista con los mensajes para el modo test:
        self.test = []
        self.scrollx = 0
        self.scrolly = 0
        self.scrollpos = [0,0] # Posición en cámara para personaje principal


    def update_scroll(self, map_pos):
        ''' Define posición de scroll, el rango de tiles del mapa a imprimir y 
            la posición del personaje'''

        #########################################################
        # - Definiendo scroll                                   #
        #   (posición sup. izq. de cámara relativa al personaje)#
        # - Creando posición relativa a cámara del personaje    #
        #########################################################

        self.scrollx = int(map_pos[0] - screen_w/2)
        self.scrolly = int(map_pos[1] - screen_h/2)

        # si cámara está entre medias del mapa:
            # x
        if self.scrollx > 0 and self.scrollx < mapa_sizex-screen_w:
            self.scrollpos[0] = int(screen_w/2)
            # y
        if self.scrolly > 0 and self.scrolly < mapa_sizey-screen_h:
            self.scrollpos[1] = int(screen_h/2)

        # si cámara está en extremos del mapa:
            # a la izquierda
        if self.scrollx < 0:
            self.scrollx = 0
            self.scrollpos[0] = map_pos[0]
            # a la derecha
        if self.scrollx > mapa_sizex - screen_w:
            self.scrollx = mapa_sizex - screen_w
            self.scrollpos[0] = map_pos[0] - self.scrollx
            # arriba
        if self.scrolly < 0:
            self.scrolly = 0
            self.scrollpos[1] = map_pos[1] 
            # abajo
        if self.scrolly > mapa_sizey - screen_h:
            self.scrolly = mapa_sizey - screen_h
            self.scrollpos[1] = map_pos[1] - self.scrolly

        #########################################################
        # - Configurando rango de tiles del mapa a imprimir.    #
        #########################################################

        # Rango de tiles correspondientes a dibujar en c'amara.
        self.inicial = self.mouse_map(0, 0)             # primer tile del scroll
        self.lim_right = self.mouse_map(screen_w, 0)    # último tile x del scroll
        self.lim_bottom = self.mouse_map(0, screen_h)   # último tile y del scroll

        # Corrección de límites para que no dibuje los inexistentes.
        if self.lim_right[1] >= self.mapa._mapaW:
        	self.lim_right[1] -= 1
        if self.lim_bottom[0] >= self.mapa._mapaH:
        	self.lim_bottom[0] -= 1


        return [self.scrollx, self.scrolly], self.scrollpos


    def plot(self, f, c):
        ''' devuelve las coordenadas de un tile referente a cámara'''
        x = int(self.mapa._tileW * c - self.scrollx)
        y = int(self.mapa._tileH * f - self.scrolly)
        return [x, y]


    def mouse_map(self, x, y):
        ''' Devuelve el tile correspondiente a una coordenada referente a camara'''
        f = (y + self.scrolly) // self.mapa._tileH
        c = (x + self.scrollx) // self.mapa._tileW
        return [f, c]




