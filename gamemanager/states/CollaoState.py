import pygame
from pygame.locals import *
from gamemanager.states import gamestate
from utilidades import utils
import escenario, personaje, mundo

class CollaoState(gamestate.GameState):

	def __init__(self, parent):
		print ('instanciando pantalla CollaoState...')
		
		self.parent = parent # parent es el gameManager
		self._mapa = escenario.Mapa('mapadesierto', parent.screen)

		# personajes:
	   		# instanciar personajes del state.

			# añadir principal y resto de personajes después.
		self._personajes = [self.parent.jugador] #, ..., ...]

		# envio a objeto 'mundo' el mapa y los personajes.
		self._mundo = mundo.Mundo(self._mapa, self._personajes)
		self._mundo.actualizar_posicion('S')

		# Sonidos
		fondo = pygame.mixer.music.load('utilidades/sonido/forest.ogg')
		pygame.mixer.music.play(loops=-1)


	def start(self):
		print('GameState CollaoState started')
		pass

	def cleanup(self):
		print("GameState CollaoState Cleaned")
		pass

	def pause(self):
		print("GameState CollaoState Paused")
		pass

	def resume(self):
		print("GameState CollaoState Resumed")

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

		# añadir otros eventos
		'''
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.parent.popstate(menustate.MenuState(self.parent))
		'''


	def update(self):
		self._mundo.update()
		'''
		# añadir cambio de pantalla.
		# parent.changeState(state)
		'''

	def draw(self):
		self.parent.screen.blit(self.parent.background, (0,0))
		self._mundo.dibujar(self.parent.screen)
