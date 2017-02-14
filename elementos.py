# -*- coding: utf-8 -*-

from pygame.locals import *
import pygame
from utilidades import utils, chars_info, a_star
 

class Elemento():
    ''' Clase padre de personajes y objetos '''

    # Esta clase crea un elemento del mapa (personajes y objetos)
    # contiene los atributos y métodos necesarios para dibujarlo y 
    # moverlo.

  
    '''
    [.] IMPLEMENTACIÓN DE CONDUCTA:

        La 'conducta' sería una lista de órdenes que influyen en al menos dos atributos del personaje:
            Su imagen:
                Determinada por self.image
            Su posíción:
                Determinada por self.map_pos

        self.action sería el primer elemento de la lista self.nextaction, si esta fuera camina_

        Si el personaje debiera de moverse, se genera una lista con los puntos hacia los que se dirige (módulo A-Star). 
            Luego, una lista con los siguientes movimientos desde el último waypoint...

        A cada ciclo,se examina si el personaje está moviéndose y si además desarolla otra acción.
            Si no hay acción, self.image por defecto es moverse.
            ... si la hay, se cambia la imagen mientras este se mueve (o se borra la ruta si debiera de estarse quieto.)

        [.] Cambio objeto Conducta por métodos aplicables a las listas de conducta y posición.
        [.] Nextpos es una posición sin comprobar.. al incluir pathfinding se eliminan las comprobaciones
            de escenario pero se mantienen las de los personajes.


    '''

    # Variables que indican la dirección del avance y su velocidad.
    velocidad = 5
    # La clave del siguiente diccionario determina la imagen del sprite. La de SO y O son el mismo, por eso coincide la letra.
    orientacion = {(0, -1):'N', (-1, 1):'O', (1, 0):'E', (1, 1):'E', (0, 1):'S', (1, -1):'E', (-1, 0):'O', (-1, -1):'O'}

    def __init__(self, nombre, tipo, map_pos, matriz_astar, focus=False, rect=None):
        print ("....Creando elemento " + nombre + '...')

        self.map_pos        = map_pos       # Posición en el mapa (centro del elemento)
        self.matriz_astar   = matriz_astar
        self.scroll_pos     = [0, 0]        # posición del elemento en la pantalla.
        self.nombre         = nombre        # Nombre del elemento, se utilizará para genera_srpite()
        self.tipo           = tipo          # Para agrupar los diferentes tipos de elementos
        self.altura         = 0             # Altura en el mapa
        self.focus          = focus         # Variable que indica si es el foco en scroll
        self.visible        = True          # Indica si se encuentra dentro de la cámara [.] modificar
        self.nextaction     = False         # Lista que indica la siguiente acción.
        self.action         = 'camina_S'    # acción actual (posición 0 de nextaction)
        self.ruta           = []
        self.destino        = self.map_pos  # Indica el destino final hacia el cual se mueve el elemento.
        self.nextpos        = self.map_pos  # Indica la posición a la que se moverá el elemento en el ciclo actual.
        self.scroll         = (0,0)         # Pixel superior izquierda de la cámara en el mapa.

        # Expresiones:
        self.expresion      = False         # Indica si hay una expresión (bocadillo) sobre el elemento.
        self.exp_exclamacion = pygame.image.load('utilidades/imagenes/exclamacion.png')
        self.exp_exclamacion.convert_alpha()

        self.test           = ['']          # lista con los mensajes para el modo test:
        self.genera_sprite(nombre, rect)    # A partir de su tileset y spriteinfo.


    # genera el sprite del personaje con el tileset y diccionario 'chars_info._spritesinfo'
    def genera_sprite(self, nombre, rect=None):
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
            self.rectcol        = pygame.Rect(0, 0, self.tileW+spriteinfo['rectval'][2], self.tileH+spriteinfo['rectval'][3])
            self.rect           = pygame.Rect(0,0, self.tileW, self.tileH)
            self.rectcol.center = self.map_pos
            self.rect.center    = self.map_pos


    #########################################################
    ############# - Acciones del elemento#.  ################
    #########################################################

    # Bocadillo sobre el sprite que dice algo o muestra un icono, estado, etc...
    def expresa(self, icono=False, stop=False):
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

    # Crea lista para caminar hacia un punto concreto del mapa.
    def pathfinding(self, pos=False):
        # Se crean dos variables mapa y destino por si, en caso de colisión, necesita recalcularse la ruta.
        if pos:
            self.destino = pos 
        else:
            pos = self.destino

        mapa = self.matriz_astar
            
        self.ruta = a_star.Pathfinding(self.map_pos, pos, mapa, width=self.rectcol.w).waypoints_pixel
        # test:
        print ('Nueva ruta para %s: '%self.nombre, end='')
        print (self.ruta)


    # Detiene el movimiento del elemento.
    def detener(self):
        self.ruta = []


    # actualiza self.action con self.nextaction y mueve el sprite.
    def actualizar_sprite(self):
        if self.contsprite > (len(self.sprites_accion[self.nextaction])-1) or (
                                        self.nextaction[:4] != self.action[:4]):            
            self.contsprite = 0

        self.action = self.nextaction
        self.image = self.sprites_accion[self.action][self.contsprite]
        self.contsprite += 1
        
        # control
        self.test[0]=str(' - Acción: ' + self.action)


    # Calcula la siguiente posición desde una ruta
    def calc_nextpos(self):
        if len(self.ruta)>0:
            waypoint = self.ruta[0]         # siguiente waypoint
            pos = self.map_pos
            #distancia = abs((pos[1] - waypoint[1]) + (pos[0] - waypoint[0]))
            distancia = abs(waypoint[0] - self.map_pos[0]) + abs(waypoint[1] - self.map_pos[1])

            print ('\nmap_pos  ', self.map_pos)
            print ('waypoint', waypoint)
            print ('distancia', distancia) ###########

            # Obtengo la orientación del movimiento:
            direcc = []
            for p in [0,1]:
                if waypoint[p] > pos[p]:
                    direcc.append(1)
                elif waypoint[p] == pos[p]:
                    direcc.append(0)
                elif waypoint[p] < pos[p]:
                    direcc.append(-1)
            self.direccion  = direcc
            print ('dirección',direcc) ##########

            # Determina la acción que le corresponde dibujar.
            for k,v in self.orientacion.items():
                if direcc == list(k):
                    orient = v
                    self.nextaction = 'camina_'+orient
                    print ('nextaction- ',self.nextaction)

            # Determina la nueva posición del elemento 
            #(Si  dist<vel sin +1, entraría en bucle con else).
            if distancia < self.velocidad+1:
                self.nextpos = list(waypoint)
                del self.ruta[0]
            else:
                self.nextpos = [pos[0]+(direcc[0]*self.velocidad), pos[1]+(direcc[1]*self.velocidad)]
            

        elif self.ruta == []:
            self.nextaction = False
            self.nextpos    = self.map_pos
            self.direccion  = (0,0)
            

    # Actualiza posiciones y rectángulos desde nextpos.
    def mover_elemento(self):
        print (' ! nextpos, map_pos',self.nextpos, self.map_pos)
        print (' ! rectcol', self.rectcol)
        #avance = (self.nextpos[0]-self.map_pos[0], self.nextpos[1]-self.map_pos[1])

        self.rectcol.center = self.nextpos
        self.rect.center    = self.nextpos
        self.map_pos        = self.nextpos


    def update(self):
        # Actualizando scroll_pos
        self.scroll_pos = ((self.map_pos[0]-self.rectcol.w//2) - self.scroll[0], (self.map_pos[1]-self.rectcol.h//2) - self.scroll[1])

        # genera nextaction desde self.ruta.
        self.calc_nextpos()

        # Calculta action (sprite)
            # Hay acciones que podrían interrumpir el movimiento o modificar la imagen...
            # Estos distintos comportamientos se definirían aquí.


    def dibujar(self, surface):
        # Dibujamos el elemento.
        screen_rect = surface.get_rect()
        screen_rect.topleft = screen_rect.left+self.scroll[0], screen_rect.top+self.scroll[1]

        #if screen_rect.contains(self.rect):
        posicion = (self.scroll_pos[0]-self.offset[0], self.scroll_pos[1]-self.offset[1])
        surface.blit(self.image, posicion)

        # Dibujamos si el elemento está expresando algo.
        if self.expresion:
            exp_rect = self.expresion_image.get_rect()
            exp_rect.midbottom = (posicion[0] + (self.rect.w // 2) , posicion[1] + 7 )
            surface.blit(self.expresion_image, exp_rect.topleft)

        # Dibuja la ruta en caso de camino definido:
        if self.ruta:
            color = (133,148,153)
            closed = False
            pointlist = [self.rect.center]
            pointlist.extend(self.ruta)

            for n in range(len(pointlist)):
                pointlist[n] = (pointlist[n][0]-self.scroll[0], pointlist[n][1]-self.scroll[1])

            if len(pointlist) == 1:
                pygame.draw.line(surface, color, self.scroll_pos, pointlist[0], 1)
            elif len(pointlist) > 1:
                pygame.draw.lines(surface, color, False, pointlist, 1)
            pygame.draw.circle(surface, color, pointlist[-1], self.rectcol.h//2, 1)









