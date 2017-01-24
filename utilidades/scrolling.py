'''
Gestión del scroll de pantalla y cámara.

Indica la porción del mapa que se presenta en pantalla y las posiciones relativas
al personaje principal de los elementos de esta.

También funciones que muestren la posición equivalente entre absoluta y relativa. 
posición relativa: La mostrada en la cámara (scroll)
posición absoluta: La posición en el mapa, usada en colisiones.

modificar:
[.] escenario
[.] mundo

'''
import pygame
from utilidades import utils
import escenario, personaje



class Camara:
    ''' crea un objeto 'camara' que se enviará al mapa indicándole que rango
    de tiles debe de dibujar según la posición del personaje y el tamaño
    de la pantalla. También dibuja los objetos y personajes.'''

    #[.] Añadir variables mapa, personajes y screen como globales

    def __init__(self, screen, mapa, personajes):
        global screen_w, screen_h, mapa_sizex, mapa_sizey
        print ('....Creando objeto camara para scroll.')
        self.personajes = personajes

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

    def actualizar_scroll(self, personajes):
        ''' Define el rango de tiles de mapa a imprimir y 
            la posición del personaje'''

        self.personajes = personajes
        posabs = self.personajes['Cris'].posabs # [.] cambiar para afectar a personaje.focus

        #########################################################
        # - Definiendo scroll                                   #
        #   (posición sup. izq. de cámara relativa al personaje)#
        # - Creando posición relativa a cámara del personaje    #
        #########################################################

        self.scrollx = int(posabs[0] - screen_w/2)
        self.scrolly = int(posabs[1] - screen_h/2)

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
            self.scrollpos[0] = posabs[0]
            # a la derecha
        if self.scrollx > mapa_sizex - screen_w:
            self.scrollx = mapa_sizex - screen_w
            self.scrollpos[0] = posabs[0] - self.scrollx
            # arriba
        if self.scrolly < 0:
            self.scrolly = 0
            self.scrollpos[1] = posabs[1] 
            # abajo
        if self.scrolly > mapa_sizey - screen_h:
            self.scrolly = mapa_sizey - screen_h
            self.scrollpos[1] = posabs[1] - self.scrolly

        #########################################################
        # - Configurando rango de tiles del mapa a imprimir.    #
        #########################################################

        # coordenadas de cámara en el mapa.
        self.inicial = self.mouse_map(0, 0)
        self.lim_right = self.mouse_map(screen_w, 0)
        self.lim_bottom = self.mouse_map(0, screen_h)

        # Corrección de límites para que no dibuje los inexistentes.
        if self.lim_right[1] >= mapa_sizex:
        	self.lim_right[1] -= 1
        if self.lim_bottom[0] >= mapa_sizey:
        	self.lim_bottom[0] -= 1

        self.scroll = [self.scrollx, self.scrolly]


        return self.scroll, self.scrollpos


    def plot(self, f, c):
        ''' devuelve las coordenadas de un tile referente a cámara'''
        x = int(self.mapa._tileW * c - self.scrollx)
        y = int(self.mapa._tileH * f - self.scrolly)
        return (x, y)


    def mouse_map(self, x, y):
        ''' Devuelve el tile correspondiente a una coordenada referente a camara'''
        f = int((y + self.scrolly) / self.mapa._tileH)
        c = int((x + self.scrollx) / self.mapa._tileW)
        return (f, c)


    def dibujar_scroll(self, surface, personajes):
        ''' Versión que dibuja en la pantalla la porción del mapa correspondiente '''
        # dibujando layers principales:
        self.personajes = personajes

        l=0
        for layer in self.mapa._mapatiles:
            for f in range(self.inicial[0], self.lim_bottom[0]+1):			# tiles x
                for c in range(self.inicial[1], self.lim_right[1]+1):
                            surface.blit(self.mapa._mapatiles[l][f][c], self.plot(f, c))
            l += 1

        self.dibujar_personajes(surface)


    def dibujar_personajes(self, surface):

        # Dibujando a personajes secundarios:
        for criatura in self.personajes.values():
            criatura.personaje.dibujar_personaje(surface)

        # [.] Añadir junto a las layerts teniuendo en cuenta su altura


