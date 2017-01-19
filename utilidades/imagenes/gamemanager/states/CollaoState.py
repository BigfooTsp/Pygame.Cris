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
	'''

	def __init__(self, parent):
		print ('....instanciando pantalla CollaoState...')
		
		self.parent = parent # parent es el gameManager
		self._mapa = escenario.Mapa('mapadesierto')

		############### PERSONAJES ######################
		# Creando personajes.

		# Cris (Principal)
		Cris = self.parent.jugador 		# Posición de personaje relativa scroll
		Cris_posabs = (5,750)			# coordenadas para rectángulo en mapa.
		Cris_rectabs = pygame.Rect(Cris_posabs[0], Cris_posabs[1],
                        Cris.rect.w, Cris.rect.h)

		# Piti (personaje secundario)
		Piti = personaje.Personaje('Piti')
		Piti_posabs = [16*32, 21*32] 	# coordenadas de celda.
		Piti_rectabs = pygame.Rect(Piti_posabs[0], Piti_posabs[1],
                        Piti.rect.w, Piti.rect.h)

		# Agregando a listado de personajes (Primero el principal)
		self._personajes = [[Cris, Cris_posabs, Cris_rectabs],
							[Piti, Piti_posabs, Piti_rectabs]
							]

		##################################################

		# Creo objeto 'mundo' y envío el mapa y los personajes.
		self._mundo = mundo.Mundo(self.parent.screen, self._mapa, self._personajes)

        # configurando cámara
		self.scroll = scrolling.Camara(self.parent.screen, self._mapa, self._personajes)

		# Sonidos
		fondo = pygame.mixer.music.load('utilidades/sonido/forest.ogg')
		pygame.mixer.music.play(loops=-1)

		# mensajes para modo test.
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


	def update(self):
		''' Comportamiento de los elementos de pantalla.'''

		# - Pendiente mover un personaje secundario por aquí.

		# Gestiona colisiones.
		colisiones = self._mundo._hay_colision()
		if colisiones:
			self.colisiones(colisiones)
		else:
			self.test[0]=[]

		# Actualiza mundo y scroll
		self._personajes = self._mundo.update(self._personajes)
		self.scroll.actualizar_scroll(self._personajes)  


	def draw(self):
		''' Dibuja el juego '''

		self.parent.screen.blit(self.parent.background, (0,0))
		self.scroll.dibujar_scroll(self.parent.screen)

	########################################################
	#### GESTIÓN DE COLISIONES Y EVENTOS DE LA PANTALLA ####
	########################################################

	def colisiones(self, colisiones):
		''' Gestiona las colsiones que tienen evento. '''

		# {'colj':jug con pers, 'coljo':jug con objs, 
		#  'colp':pers con pers, 'colpo':pers con objs}

		# para modo test
		print (colisiones)
		col = []
		for c,v in colisiones.items():
			if len(v) > 0:
				contacto = '%s, %s'%(c,str(v))
				col.append(contacto)
		col.append('Colsiones:')
		self.test[0] = col

		return

	# Definir las actuaciones de personajes. es posible que desde update y con un reloj
