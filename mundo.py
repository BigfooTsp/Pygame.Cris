import pygame
from pygame.locals import *

import escenario
import personaje


class Mundo:
    ''' Clase para controlar todo lo que ocurre durante el juego:
        Colisiones, Dibujar personajes, control del jugador, etc ...
        se instancia desde el state.
        Este módulo debería ser genérico, está adaptado a collaoState,
        cuando desarrolle otra state con más personajes y elementos ya veré
        como hacerlo.
    '''

    def __init__(self, mapa, personajes):
        print ("Instanciando Mundo...")

        self._mapa = mapa
        self.personajes = personajes # array con los personajes
        self._jugador = personajes[0]
        self._jugadorPosAbs =  mapa._char_posabs
        self._jugadorRect = (self._jugadorPosAbs[0], self._jugadorPosAbs[1],
                            self._jugador.rect.w, self._jugador.rect.h)


    def mover_jugador(self, orientacion):
        ''' movimiento del jugador si es posible.'''

        avance = self._jugador.orientacion[orientacion]
        direccion = (self._jugadorPosAbs[0] + self._jugador.orientacion[orientacion][0], 
                     self._jugadorPosAbs[1] + self._jugador.orientacion[orientacion][1])

        print ('moviendo personaje hacia el %s a posición %s' %(orientacion, direccion))

        if self.espisable(avance):
            self._jugadorPosAbs = direccion
            self._jugador.pos = (self._jugador.pos[0] + self._jugador.orientacion[orientacion][0], 
                                 self._jugador.pos[1] + self._jugador.orientacion[orientacion][1])

        self.actualizar_posicion(orientacion)

        return


    def espisable(self, avance):
        ''' devuelve True si el terreno es pisable '''
        #[.] poner limites del mapa o rectángulo de límite.

        # mueve tantas posiciones como se indica en 'direccion'.
        pos = self._jugadorRect.move(avance)

        # si hay colisión
        idx = pos.collidelist(self._mapa._nopisable)
        if idx == -1:
            print ('avanzando')
            return True
        else: # Si hay colisión no se mueve
            print ('! colisión escenario', idx, self._mapa._nopisable[idx])
            return False


    def _hay_colisión(self):
        ''' gestion de colisión con elementos de escenario y otros personajes.'''

    	# colisiones escenario
    	# otros personajes
        ''' según la posición de los elementos del escenario comprueba colisiones
        y sus resultados en la escena '''

        return False


    def actualizar_camara(self):
        ''' Cámara y desplazamiento del mapa con el personaje principal.
            actualiza coordenadas absolutas y relativas.'''

        coordenadas = [0,0]
        posabsX = self._jugadorPosAbs[0]
        posabsY = self._jugadorPosAbs[1]
        posrelX = self._jugador.pos[0]
        posrelY = self._jugador.pos[1]
        mapasizeX = self._mapa._mapa_size[0]
        mapasizeY = self._mapa._mapa_size[1]
        camarasizeX = self._mapa._camara_size[0]
        camarasizeY = self._mapa._camara_size[1]

        # colocar posición inicial de personaje y coordenadas.
        if (posabsX > camarasizeX/2) or (posabsX < mapasizeX-camarasizeX/2) :
            posrelX = camarasizeX/2
            coordenadas[0] = (posabsX - camarasizeX/2)
        if (posabsY > camarasizeY/2) or (posabsY < mapasizeY-camarasizeY/2) :
            posrelY = camarasizeY/2
            coordenadas[1] = (posabsY - camarasizeY/2)

        if posabsX < camarasizeX/2:
            posrelX = posabsX
            coordenadas[0] = 0
        if posabsX > mapasizeX-camarasizeX/2:
            posrelX = camarasizeX - (mapasizeX - posabsX)
            coordenadas[0] = mapasizeX - camarasizeX
        if posabsY < camarasizeY/2:
            posrelY = posabsY
            coordenadas[1] = 0
        if posabsY > mapasizeY-camarasizeY/2:
            posrelY = camarasizeY - (mapasizeY - posabsY)
            coordenadas[1] = mapasizeY - camarasizeY

        self._mapa._coordenadas = (coordenadas[0], coordenadas[1], camarasizeX, camarasizeY )
        self._jugador.pos = (posrelX, posrelY)

        self._jugadorRect = pygame.Rect(
            self._jugadorPosAbs[0], self._jugadorPosAbs[1], 
            self._jugador.rect.w, self._jugador.rect.h) 

        return


    def actualizar_posicion(self, orientacion):
        ''' muve personajes y elementos'''
        ''' [.] Tal vez sea redundante con update().
        aunque en este momento solo utilizo al jugador, puede que
        esta función sea útil para controlar a todos los personajes...
        veremos conforme vaya desarrollando el juego.'''

        self._jugador.mover('camina_%s'%(orientacion))

        return


    def update(self):
        ''' mueve y actualiza las posiciones de los personajes '''

        # comprueba acciones
        # colisiones

        if self._hay_colisión():
            None
        self.actualizar_camara()

        return
    
    def dibujar(self, surface):
        self._mapa.dibujar(surface)
        
        for personaje in self.personajes:
            personaje.dibujar(surface)
        return

