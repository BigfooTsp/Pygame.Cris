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

        self._mapa = mapa                           # Cargando mapa y personajes.
        self.personajes = personajes                 # {nombre:PersonajeState, ...}
        self.channel1 = pygame.mixer.Channel(1)     # Sonidos
        self.channel1.set_volume(1)
        self.paso = pygame.mixer.Sound('utilidades/sonido/step.ogg')    # Paso
        self.test = ['']                            # lista con los mensajes para el modo test:


    def mover_jugador(self, orientacion, actor='Cris'):
        ''' movimiento del jugador si es posible.'''

        #[.] En lugar de orientación debería de ser 'accion'
        # (desde handleevents o nextaction de personajeState) para determinar esta y gestionar
        # desde state ya que personaje solo cambia sprites

        jugador = self.personajes[actor].personaje
        posabs = self.personajes[actor].posabs
        avance = jugador.orientacion[orientacion]
        direccion = (posabs[0] + jugador.orientacion[orientacion][0], 
                     posabs[1] + jugador.orientacion[orientacion][1])

        # Actualizando posición y sprite del personaje.
        if self.espisable(self.personajes[actor], avance):
            self.personajes[actor].posabs = direccion           # actualizando posabs.
            #self.personajes[actor].rectcol.move_ip(avance)      # actualiza rectcol (eliminado, desde update de personajestate)
        jugador.actualizar_sprite('camina_%s'%(orientacion))
        # Sonido al caminar
        # [.] El sonido debería ir en personaje ??.
        if self.channel1.get_busy() == False:
            self.channel1.play(self.paso)


    def mover_personajes(self):
        ''' Mueve los personajes secundarios '''

        # Mover a personaje si es pisable.
        for k,v in self.personajes.items():
            if self.personajes[k].principal == False:
                if self.personajes[k].nextpos:
                    self.mover_jugador(self.personajes[k].nextaction, self.personajes[k].nombre)


    def espisable(self, jugador, avance):
        ''' devuelve True si el terreno es pisable '''

        # reducir cuadrado de personaje para que detecte colisión antes que avance pisable.

        pos = jugador.rectcol.move(avance)
        pos.inflate_ip(-2,-2)

        # Comprueba si el avance es pisable.
            # Colisión con otros personajes y objetos.
        print ('rectcols en pisable',self.rectcols)
        idp = pos.collidedictall(self.rectcols)
            # límites de escenario
        idx = pos.collidelist(self._mapa._nopisable)

        print ('idp', idp)
        print ('idx', idx)

        if idp == [] and idx == -1:
            self.test[0]=str(' - Es pisable, avanzando')
            return True
        else:
            self.test[0]=str(' ! no pisable')
            return False

    def _hay_colision(self):
        ''' según la posición de los elementos del escenario comprueba colisiones
        y devuelve el resultado para gestoinar en el state '''

        # Colisión de personajes con otros personajes y objetos {pers:[(k,v), (k,v)], ...}
        colisiones = {}
        for k,v in self.personajes.items():
            rect = v.rectcol
            cols = []
            pisables = self.rectcols
            pisables.pop(k)
            c = rect.collidedictall(pisables,1)
            if c:
                colisiones.update({k:c})
                print ('cols',colisiones)

        if len(colisiones) > 0:
            print ('colisinando con ', colisiones)
            return colisiones
        else:
            return False


    def actualizar_posicion(self):
        ''' Mueve personajes secundarios en el mapa'''
        # La posición del personaje principal en cámara la determina el módulo 'scrolling'
        # Actualiza rectángulos de colisión para eventos.
        self.rectcols = self._mapa._objetos_escenario
        for k,v in self.personajes.items():
            self.rectcols.update({k:v.rectcol})


    def update(self, personajes):
        ''' mueve y actualiza las posiciones de los personajes '''

        self.personajes = personajes


        self.actualizar_posicion()          # Actualiza la posición de secundarios y objetos.
        self.mover_personajes()             # Mueve a los personajes.

            
        print ('\n  ## rectcols',self.rectcols) ##############


        colisiones = self._hay_colision()

        return self.personajes, colisiones, 
