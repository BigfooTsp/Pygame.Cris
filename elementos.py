# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame
from utilidades import utils, chars_info
 

class Elemento():
    ''' Clase padre de personajes y objetos '''

    # Esta clase crea un elemento del mapa (personajes y objetos)
    # contiene los atributos y métodos necesarios para dibujarlo y 
    # moverlo.

    # Variables que indican la dirección del avance y su velocidad.
    velocidad = 6
    orientacion = {'N':(0, -1), 'NE':(-1, 1), 'E':(1, 0), 'SE':(1, 1), 'S':(0, 1), 'SO':(1, -1), 'O':(-1, 0), 'NO':(-1, -1)}
  
    '''
    [.] IMPLEMENTACIÓN DE CONDUCTA:
        El personaje debería responder a comandos como camina_N. Estos, en caso de seguir una ruta o un movimiento de varios
        frames, se acumularán en una lista, de las cuales el primero es la siguiente acción a cumplir.
        Habrá algunos casos en los que se terminará la serie de movimientos eliminándolos todos o selectivamente.
    '''



    def __init__(self, nombre, tipo, map_pos, focus=False, rect=None):
        print ("....Creando elemento " + nombre + '...')

        self.map_pos        = map_pos       # Posición en el mapa
        self.scroll_pos     = [0, 0]        # posición del personaje en la pantalla.
        self.nombre         = nombre        # Nombre del elemento, se utilizará para genera_srpite()
        self.tipo           = tipo          # Para agrupar los diferentes tipos de elementos
        self.altura         = 0             # Altura en el mapa
        self.focus          = focus         # Variable que indica si es el foco en scroll
        self.visible        = True          # Indica si se encuentra dentro de la cámara [.] modificar
        self.action         = 'camina_S'    # acción actual
        self.nextaction     = False         # Indica la siguiente posición.
        self.nextpos        = self.map_pos
        self.conducta       = Conducta()

        # Expresiones:
        self.expresion      = False         # Indica si hay una expresión (bocadillo) sobre el elemento.
        self.exp_exclamacion = pygame.image.load('utilidades/imagenes/exclamacion.png')
        self.exp_exclamacion.convert_alpha()

        self.test           = ['']          # lista con los mensajes para el modo test:
        self.genera_sprite(nombre, rect)          # A partir de su tileset y spriteinfo.


    #########################################################
    ########### - Configuración del elemento.  ##############
    #########################################################

    def genera_sprite(self, nombre, rect=None):
        '''genera el sprite del personaje con el tileset y diccionario de características 
        coorespondiente a su nombre'''
        global spriteinfo

        if rect:	# Si viene con rect desde mapa, es un objeto de mapa, sin sprite.
        	self.rectcol = rect

        else:
            spriteinfo          = chars_info._spritesinfo[nombre]
            self.tileW          = spriteinfo['tileW']
            self.tileH          = spriteinfo['tileH']
            self.tileset        = utils.cortar_charset(spriteinfo['path'], self.tileW, self.tileH)
            self.offset         = (spriteinfo['rectval'][0], spriteinfo['rectval'][1])
            self.sprites_accion = {}        # diccionario con {acción:[sprites]}
            self.contsprite     = 0         # Contador de sprite
            for n in range(0, len(self.tileset)):
                charsheet = []
                for l in range(0, (spriteinfo['nsprites'][n])): 
                    charsheet.append(self.tileset[n][l])        
                self.sprites_accion[spriteinfo['actionlist'][n]] = charsheet
            self.image          = self.sprites_accion['camina_S'][self.contsprite] # sprite actual
            self.rectcol        = pygame.Rect(self.map_pos[0], self.map_pos[1], 
                                                self.tileW+spriteinfo['rectval'][2], 
                                                self.tileH+spriteinfo['rectval'][3])
            self.rect           = pygame.Rect(self.map_pos[0]-spriteinfo['rectval'][0], 
                                                self.map_pos[1]-spriteinfo['rectval'][1],
                                                self.tileW, self.tileH)


    #########################################################
    ############# - Acciones del elemento#.  ################
    #########################################################

    def expresa(self, icono=False, stop=False):
        ''' Bocadillo sobre el sprite que dice algo o muestra un icono, estado, etc... 
        Podría estar acompañado de un sonido.'''
        if stop:
            self.expresion == False
            return
        elif self.expresion == False:
            self.expresion = True
        if icono == 'exclamacion':
            self.expresion_image = self.exp_exclamacion
        else:
            print ('... Expresión de elemento %s no encontrada'%(self.nombre))


    #########################################################
    ############ - Actualización del elemento.  #############
    #########################################################

    def calc_nextaction(self, nextaction):
        ''' Configura variables nextaction y nextpos desde acción nueva '''

        # Este método se invoca desde otro módulo por algún evento. Se actualizará la
        # posición con el update tras comprobar que la nueva posicíón es pisable.

        if nextaction == 0:
            self.nextaction =False
            self.nextpos    =self.map_pos

        elif nextaction.startswith('camina'):
            orientacion = (self.orientacion[nextaction[-1]]) ####### Adaptar al cambio a 8 direcciones.
            avance=self.orientacion[nextaction[-1]]
            self.nextpos = (self.map_pos[0] + avance[0], self.map_pos[1] + avance[1])
            self.nextaction = nextaction


    def avance(self):
        ''' devuelve cuanto avanza el personaje en el siguiente paso programado'''
        return (self.nextpos[0]-self.map_pos[0], self.nextpos[1]-self.map_pos[1])


    def update(self):
        ''' Actualiza a la siguiente posición programada siempre que el objeto no esté bloqueado
        por algo que le impida avanzar'''

        # Nota: Debería de desbloquearse si se indica una nueva conducta
        self.conducta.update()
        # preparar siguientes acciones.
        if self.conducta.activa:
            self.calc_nextaction(self.conducta.nextorden)
        else:
            self.calc_nextaction(0)     # reset si no hay conducta programada


    def actualizar_sprite(self):
        ''' actualiza self.action con self.nextaction y mueve el sprite. '''

        if self.contsprite > (len(self.sprites_accion[self.nextaction])-1) or (
                                        self.nextaction[:4] != self.action[:4]):            
            self.contsprite = 0

        self.action = self.nextaction
        self.image = self.sprites_accion[self.action][self.contsprite]
        self.contsprite += 1
        
        # control
        self.test[0]=str(' - Acción: ' + self.action)


    def mover_elemento(self, pisable=False):
        ''' Actualiza posiciones y rectángulos desde nextpos. '''
        self.rectcol.move_ip(self.avance())
        self.rect.move_ip(self.avance())
        self.map_pos = self.nextpos


    def dibujar(self, surface):
        # Dibujamos el tile correspondiente de Cris.
        posicion = (self.scroll_pos[0]-self.offset[0], self.scroll_pos[1]-self.offset[1])
        surface.blit(self.image, posicion)

        # Dibujamos si el elemento está expresando algo.
        if self.expresion:
            exp_rect = self.expresion_image.get_rect()
            exp_rect.midbottom = (posicion[0] + (self.rect.w // 2) , posicion[1] + 7 )
            surface.blit(self.expresion_image, exp_rect.topleft)



class Conducta():
    ''' clase que contiene las ordenes que se irán cumpliendo a cada paso 
        en los elementos con conducta programada'''
    ordenes        = []          # Listado de ordenes
    nextorden      = False       # Siguiente orden
    activa         = False       # Indica si hay ordenes pendientes.
    activa_cont    = 0
    bloqueado      = False


    def add(self, orden, conducta_programada=False, lista=False, reset=False):
        ''' añade una nueva orden al listado general o un listado de ellas '''
        self.bloqueado = False      # Si el elemento está bloqueado, lo desbloquea si inicia un nuevo comportamiento.
        self.activa = True

        if reset:
            self.ordenes = []
        if listado:
            self.ordenes.extend(self.lista)
        elif conducta_programada:
            self.ordenes.extend(self.conducta_programada(conducta_programada))
        elif orden:
            self.ordenes.append(orden)

        self.activa_cont = len(self.ordenes)


    def delete(self, pos=False, todas=False):
        ''' borra una orden o todas'''
        if pos:
            self.ordenes.pop(pos)
        elif todas:
            self.ordenes = []


    def update (self):
        ''' Actualiza la clase tras cumplir la última orden. '''

        if self.bloqueado:
            None
        else:
            if self.activa:
                self.ordenes.pop(0)
                if len(self.ordenes) > 0:
                    self.nextorden   = self.ordenes[0]
                    self.activa_cont = len(self.ordenes)
                else:
                    self.activa      = False
            else:
                return 'sin conducta planificada'


    def conducta_programada (self, conducta_programada):
        ''' actualizará self.ordenes con un listado de acciones que representa
            una acción programada. '''
        conductas_dict = {}     # {conducta_programada:listadoacciones, ...}
        return conductas_dict[conducta_programada]


