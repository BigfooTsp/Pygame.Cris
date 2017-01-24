import pygame
from pygame.locals import *
from gamemanager.states import gamestate
from utilidades import utils, scrolling
import escenario, personaje, mundo

class CollaoState(gamestate.GameState):
	'''
	Añadiendo personajes a la pantalla.
	Debo de modificar la lista de personajes para que incluya su posición absoluta del mapa
	después modificaré 'mundo' para que los ubique bien en el mundo.
	[.] prescindir de la posicion inicial de JSON
	[.] eliminando mundo
	[.] Añadir spriteinfo como archivo separado enviado a instancia de personaje
	[.] Uniendo personajeState y personaje
	'''

	def __init__(self, parent):
		print ('....instanciando pantalla CollaoState...')
		
		self.parent = parent # parent es el gameManager
		# Creando mapa.
		self._mapa = escenario.Mapa('mapadesierto')
		# Creando personajes.         obj:        nombre   posabs      personaje(si ya existe)
		self._personajes = {'Cris':PersonajeState('Cris', (5,750), principal=True, actor=self.parent.jugador, focus = True),
							'Piti':PersonajeState('Piti', [16*32, 21*32])
							}

		# Creo objeto 'mundo' y envío el mapa y los personajes.
		self._mundo = mundo.Mundo(self.parent.screen, self._mapa, self._personajes)
        # configurando cámara
		self.scrolling = scrolling.Camara(self.parent.screen, self._mapa, self._personajes)
		self.scrollpos = self.scrolling.scrollpos
		# Sonidos
		fondo = pygame.mixer.music.load('utilidades/sonido/forest.ogg')
		pygame.mixer.music.play(loops=-1)
		# listado de mensajes para modo test.
		self.test = [[]]


	########################################################
	########## GESTIÓN DE ESTADO DE LA PANTALLA ############
	########################################################

	def start(self):
		print('........GameState CollaoState started')
		pass

	def cleanup(self):
		print("GameState CollaoState Cleaned")
		pass

	def pause(self):
		print("GameState CollaoState Paused")
		pass

	def resume(self):
		print("GameState CollaoState Resumed")


	########################################################
	################ BUCLE DE LA  PANTALLA #################
	########################################################

	def handleEvents(self, event, teclado):
		''' gestión de eventos de teclado '''

		# [.] Hay que optimizar el control del personaje.

		# movimiento
		if teclado[pygame.K_UP]:
			self._mundo.mover_jugador('N')
		if teclado[pygame.K_DOWN]:
			self._mundo.mover_jugador('S')
		if teclado[pygame.K_RIGHT]:
			self._mundo.mover_jugador('E')
		if teclado[pygame.K_LEFT]:
			self._mundo.mover_jugador('O')

		# añadir pausa
		'''
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.P_ESCAPE:
				self.parent.popstate(menustate.MenuState(self.parent))
		'''

	def espisable():
		''' Comprueba si es pisable '''


	def hay_colision():
		''' Comprueba si hay colisión '''


	def colisiones(self, colisiones):
		''' Gestiona las colsiones que tienen evento. '''

		#colisiones = {pers:[(k,v), (k,v)], ...}

		# para modo test
		col = []
		for k,v in colisiones.items():
			if len(v) > 0:
				for element in v:
					contacto = '%s, %s'%(k,str(v))
					col.append(contacto)
		col.append('Colsiones:')
		self.test[0] = col


	def update(self):
		''' Actualiza el juego en función de los eventos.'''


		# Actualiza mundo y personajes.
		''' Se envía personajes a mundo para que gestione sus movimientos y detecte
			colisiones. Al recuperarlos se procesarán en el state.'''
		self._personajes, colisiones = self._mundo.update(self._personajes)

		# Gestiona colisiones.
		if colisiones:
			self.colisiones(colisiones)
		else:
			self.test[0]=[]

		# Actualiza scroll y posición de personajes.
		self.scroll, self.scrollpos = self.scrolling.actualizar_scroll(self._personajes)  

		for k,v in self._personajes.items(): 
			self._personajes[k].update_pos(self.scroll, self.scrollpos)

	def draw(self):
		''' Dibuja el juego '''

		self.parent.screen.blit(self.parent.background, (0,0))
		self.scrolling.dibujar_scroll(self.parent.screen, self._personajes)


	########################################################
	#### GESTIÓN DE COLISIONES Y EVENTOS DE LA PANTALLA ####
	########################################################
	def MisionesState (self):
		''' Gestiona las misiones activas y el estado de la pantalla en general '''
		None

	def Mision1 (self):
		''' Misión 1 de la pantalla.'''
		None

	# Definir las actuaciones de personajes. es posible que desde update y con un reloj











	########################################################
	####       Clase personaje ampliada para State      ####
	########################################################


class PersonajeState(personaje.Personaje):
	''' Instancia especial de personaje para el State, 
	añade rectángulos de colisión y coordenadas de pantalla '''

	def __init__(self, nombre, posabs=[0,0], principal=False, actor=False, focus=False):
		if actor:
			self.personaje 	= actor
		else:
			self.personaje 	= personaje.Personaje(nombre)
		self.nombre 		= nombre
		self.tipo			= personaje 	# Para agrupar los diferentes tipos de elementos
		self.posabs			= posabs		# Posición en el mapa
		self.pos 			= self.personaje.pos
		self.altura 		= 0				# Altura en el mapa
		# [.] cambiar principar por tipo: personaje principal (o objeto o personaje o animal)
		self.principal 		= principal 	# Variable que indica si el es personaje principal.
		self.focusscroll 	= focus			# Variable que indica si es el foco en scroll
		self.visible 		= True			# Indica si se encuentra dentro de la cámara [.] modificar
		# Control de ordenes. blocked activa un contador para controlar una insturcción dada.
		self.blocked 		= False			# Si el personaje > 0 no puede nueva orden.
		self.nextpos	 	= False			# Siguiente posición a moverse
		self.rectcol 		= pygame.Rect(self.posabs[0], self.posabs[1], self.personaje.rect.w, self.personaje.rect.h)

		self.update_pos()


	def borrar_sprite():
		''' Borra sprite con el fondo del mapa '''
		visible = None

	def update_pos(self, scroll=[0,0], scrollpos=[0,0]):
		''' Actualiza posición en scroll y -1 a contador de acciones del personaje'''

		# cuadrado para detectar colisiones en el mapa
		self.rectcol = pygame.Rect(self.posabs[0], self.posabs[1], self.personaje.rect.w, self.personaje.rect.h)

		# Posición del personaje en cámara.
		if self.principal:
			self.personaje.pos = scrollpos
		else:
			self.personaje.pos = [self.posabs[0] - scroll[0], self.posabs[1] - scroll[1]]
		# Contador de bloqueado.
			if self.blocked > 0: # Contador marcha atrás de acciones.
				self.blocked -= 1

		if self.visible == None:
			None
			borrar_sprite()

	def dibujar():
		''' dibuja el personaje '''




 ##### CLASES PARA INCORPORAR PRÓXIMAMENTE #####

class Grupo():
	''' Clase que contiene grupos de personajes o objetos'''

	def __init__():
		self.rectcols = 0 	# Conjunto de rectángulos de colisiones

	def add():
		''' añade personajes al grupo '''
		None

	def delete():
		''' borra personajes al grupo '''
		None

	def update():
		''' actualiza parámetrps de los personajes '''

	def intercolision():
		''' detecta colisiones entre los miembros del grupo '''

	def colisionancon():
		''' detecta colisiones entre otros elementos o grupos'''

	def dibujar():
		''' dibuja el grupo de personajes '''


class Objeto(pygame.sprite.Sprite):
	''' Clase para objetos'''

	def __init__():
		self.nombre 		= nombre
		self.posabs			= posabs		# Posición en el mapa
		self.pos 			= self.personaje.pos
		self.altura 		= 0				# Altura en el mapa
		self.visible 		= True			# Indica si se encuentra dentro de la cámara [.] modificar
		self.tipo			= objeto
		self.cont 			= 0

	def borrar():
		''' Borra sprite con el fondo del mapa '''
		visible = None

	def update():
		''' Actualiza posición en scroll '''

		# Contador de bloqueado.
		if self.cont > 0: # Contador marcha atrás de acciones.
			self.cont -= 1

		if visible == None:
			borrar_sprite()

	def dibujar():
		''' dibuja el objeto '''


class Tile():
	''' clase que contiene las características de los tiles de los layers '''
	None
