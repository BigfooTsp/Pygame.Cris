import pygame
from pygame.locals import *
import escenario, personaje


class Mundo:
    ''' Clase para controlar todo lo que ocurre durante el juego:
        Colisiones, Dibujar personajes, control del jugador, etc ...
        se instancia desde el state.
        Este módulo debería ser genérico, está adaptado a collaoState,
        cuando desarrolle otra state con más personajes y elementos ya veré
        como hacerlo.
    '''

    # [.] Modificar selfs por las variables globales correspondientes en el __init__

    def __init__(self, surface, mapa, personajes):
        print ("Instanciando Mundo...")

        # Cargando mapa y personajes.
        self._mapa = mapa
        self.personajes = personajes # array con los personajes
        '''               [0][0]                 [0][1]                    [0][2]
        personajes = [[personajePrincipal, personaje_posabs=(x, y), personaje_rectabs=Rect]
                      [personaje2,         personaje_posabs=(x, y), personaje_rectabs=Rect]
                      [...]]'''

        # lista con cuadros de personajes con los que se puede colisionar.
        self.personajesnpisables = []
            # a estas listas les reduzco dos pixeles para que me detecte colisiones
            # antes de que no me deje avanzar por no ser pisable.
        self.personajesnpisables0 = []
        self.objetosnpisables0 = []

        #Sonidos
        self.channel1 = pygame.mixer.Channel(1)
        self.channel1.set_volume(1)
            # Paso
        self.paso = pygame.mixer.Sound('utilidades/sonido/step.ogg')

        # lista con los mensajes para el modo test:
        self.test = ['']


    def mover_jugador(self, orientacion):
        ''' movimiento del jugador si es posible.'''

        jugador = self.personajes[0][0]
        jugadorposAbs = self.personajes[0][1]

        avance = jugador.orientacion[orientacion]
        direccion = (jugadorposAbs[0] + jugador.orientacion[orientacion][0], 
                     jugadorposAbs[1] + jugador.orientacion[orientacion][1])

        # Actualizando posición del personaje.
        if self.espisable(self.personajes[0], direccion):
            #actualizando posabs.
            self.personajes[0][1] = direccion
            # actualiza rect_abs
            self.personajes[0][2] = pygame.Rect(direccion[0], direccion[1], 
                self.personajes[0][0].rect.w, self.personajes[0][0].rect.h )

        # actualiza sprite del jugador con sonido.
        if self.channel1.get_busy() == False:
            self.channel1.play(self.paso)
        jugador.actualizar_sprite('camina_%s'%(orientacion))

        return


    def mover_personajes(self):
        ''' Mueve los personajes secundarios '''
        None



    def espisable(self, personaje, direccion):
        ''' devuelve True si el terreno es pisable '''

        ''' Nota: Si no reduzco el tamaño de los rectángulos de objetos
             y personajes para comrobar si es pisabel, no me dejará luego
             tener contanto con ellos. '''

        # [.] Habrá que adaptarlo para comprobar los personajes entre ellos.


        # mueve tantas posiciones como se indica en 'direccion'.
        pos = pygame.Rect(direccion[0], direccion[1] , 
            personaje[0].rect.w, personaje[0].rect.h )

        # Comprueba si el avance es pisable.
            # otros personajes
        idp = pos.collidelist(self.personajesnpisables0)
            # límites de escenario
        idx = pos.collidelist(self._mapa._nopisable)
            # objetos
        ido = pos.collidelist(self.objetosnpisables0)

        if idx == -1 and idp == -1 and ido == -1:
            self.test[0]=str(' - Es pisable, avanzando')
            return True
        else:
            self.test[0]=str(' ! no pisable')
            return False


    def _hay_colision(self):
        ''' según la posición de los elementos del escenario comprueba colisiones
        y sus resultados en la escena, devolverá tipo de colisión que se 
        gestionará en el update del state '''

        colj = []       # Colisiones de jugador con personajes.
        coljo = []      # Colisiones de jugador con objetos.
        colp = []       # Colisiones de personajes con personajes. 
        colpo = []      # Colisiones de personajes con objetos

        # Colisión entre personajes [.] Hay que mejorarla
        if len(self.personajesnpisables) > 1:
            p=0
            for personaje in self.personajesnpisables:
                otrospersonajes = self.personajesnpisables
                otrospersonajes.pop(p)
                colp = self.personajes[p][2].collidelistall(otrospersonajes)
                p += 1
        # Colisión de personajes con objetos
        if len(self.personajesnpisables) > 0:
            if len(self._mapa._objetos_escenario) > 0:
                colpo.append(self.personajes[0][2].collidedict(self._mapa._objetos_escenario))
        # Colisión entre el jugador y otros personajes.
        if len(self.personajesnpisables) > 0:
            colj = self.personajes[0][2].collidelistall(self.personajesnpisables)
    	# colisiones de jugador con objetos de escenario
        if len(self._mapa._objetos_escenario) > 0:
            coljo.append(self.personajes[0][2].collidedict(self._mapa._objetos_escenario))

        colisiones = {'colj':colj, 'coljo':coljo, 'colp':colp, 'colpo':colpo}

        if len(colj) == 0 and len(coljo) == 0 and len(colp) == 0 and len(colpo) == 0:
            return False

        else:
            return colisiones


    def actualizar_posicion(self):
        ''' Mueve personajes secundarios y elementos en relación al personaje principal (scroll)'''
        # La posición del personaje en el mapa y en cámara la indica el módulo 'scrolling'

        # actualiza rectángulo de posición de los secundarios.
        for n in range(1, len(self.personajes)):
            destino = pygame.Rect(self.personajes[n][1][0], self.personajes[n][1][1], 
                self.personajes[n][0].rect.w, self.personajes[n][0].rect.h)

        # actualiza cuadrados no pisables de objetos y personajes.
        p=1
        for personaje in range(1, len(self.personajes)):
            self.personajesnpisables.append(self.personajes[p][2])
            self.personajesnpisables0.append(self.personajes[p][2].inflate(-2,-2))
            p += 1

        for objeto in self._mapa._objetos_escenario:
            self.objetosnpisables0.append(objeto.value().inflate(-2,-2))


    def update(self, personajes):
        ''' mueve y actualiza las posiciones de los personajes '''

        # recibe modificación de los personajes en el state.
        self.personajes = personajes
        self.actualizar_posicion()          # Mueve personajes secundarios y objetos.
        self.mover_personajes()             # Mueve a los personajes.

        return self.personajes
