import pygame, os
from pygame.locals import *
from gamemanager.states import gamestate
from utilidades import utils
import escenario, elementos

class PausaState(gamestate.GameState):

	def __init__(self, parent):
		print ('....instanciando pantalla Pausa...')
		
		self.parent = parent # parent es el gameManager
		self.screen_rect = parent.screen.get_rect()

		# Cargando texto
		self.texto1 = utils.texto(
				'PAUSA', 
				self.screen_rect.centerx, self.screen_rect.centery-30,
				65, 
				fuente = 0)
		self.texto2 = utils.texto(
				'presione una tecla para continuar', 
				self.screen_rect.centerx, self.screen_rect.centery+30,
				25, 
				fuente = 0)



	def start(self):
		print('........PAUSA')

		pygame.mixer.music.pause()

		pass


	def handleEvents(self, event, teclado):
		''' gestión de eventos de teclado '''

		# añadir otros eventos
		if event.type == pygame.KEYDOWN:
			if event.key:
				pygame.mixer.music.unpause()
				self.parent.popState()

		return


	def update(self):
		None

	def draw(self):
		self.parent.screen.blit(self.parent.background, (0,0))
		self.parent.screen.blit(self.texto1[0], (self.texto1[1].topleft))
		self.parent.screen.blit(self.texto2[0], (self.texto2[1].topleft))

