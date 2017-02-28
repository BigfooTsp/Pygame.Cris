import pygame, os
from pygame.locals import *
from gamemanager.states import gamestate, CollaoState
from utilidades import utils
import escenario, elementos

class MenuState(gamestate.GameState):

	def __init__(self, parent):
		print ('....instanciando pantalla menustate...')
		
		self.parent = parent # parent es el gameManager
		self.screen_rect = parent.screen.get_rect()

		# Cargando texto
		self.texto1 = utils.texto(
				'Cris en El Collao', 
				self.screen_rect.centerx, self.screen_rect.centery-30,
				65, 
				fuente = 0)
		self.texto2 = utils.texto(
				'presione una tecla para empezar', 
				self.screen_rect.centerx, self.screen_rect.centery+30,
				25, 
				fuente = 0)

		# Cargando musica
		pathmusica = 'utilidades/sonido/intro.mp3'
		pygame.mixer.music.load(pathmusica)
		pygame.mixer.music.play(loops=-1)


	def cleanup(self):
		# Reactivando modo test
		if self.testwhait == True:
			self.parent.test_mode = True


	def start(self):
		print('........GameState menustate started')
		# Descativando modo test temporalmente.
		if self.parent.test_mode  == True:
			self.parent.test_mode = False
			self.testwhait 	= True
		else:
			self.testwhait 	= False


	def handleEvents(self, event, teclado):
		''' gestión de eventos de teclado '''

		if event.type == pygame.KEYDOWN:
			if event.key:
				pygame.mixer.music.stop()
				self.parent.changeState(CollaoState.CollaoState(self.parent))
		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.mixer.music.stop()
			self.parent.changeState(CollaoState.CollaoState(self.parent))

		return


	def update(self):
		None

	def draw(self):
		self.parent.screen.blit(self.parent.background, (0,0))
		self.parent.screen.blit(self.texto1[0], (self.texto1[1].topleft))
		self.parent.screen.blit(self.texto2[0], (self.texto2[1].topleft))

