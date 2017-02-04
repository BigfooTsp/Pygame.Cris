import pygame, os
from pygame.locals import *
from gamemanager.states import gamestate
from utilidades import utils
import escenario, elementos

class PausaState(gamestate.GameState):
	''' Pantalla para pausas en el juego.'''

	def __init__(self, parent):
		print ('....instanciando pantalla Pausa...')
		
		self.parent = parent # parent es el gameManager
		self.screen_rect = parent.screen.get_rect()
		self.test = [[]]

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


	def sonido_start(self, sonido=True, canal=1, volumen = 1):
		canal = pygame.mixer.Channel(canal) 
		canal.set_volume(volumen)
	        
		menu_click = pygame.mixer.Sound('utilidades/sonido/menu-click.ogg')
		canal.play(menu_click)


	def cleanup(self):
		self.sonido_start()

		# Reactivando modo test
		if self.testwhait == True:
			self.parent.test_mode = True

	def start(self):
		print('........PAUSA')

		# Descativando modo test temporalmente.
		if self.parent.test_mode  == True:
			self.parent.test_mode = False
			self.testwhait 	= True
		else:
			self.testwhait 	= False

		# Sonidos
		self.sonido_start()



	def handleEvents(self, event, teclado):
		''' gestión de eventos de teclado '''

		# añadir otros eventos
		if event.type == pygame.KEYDOWN:
			if event.key:
				self.parent.popState()

		return


	def update(self):
		None

	def draw(self):
		self.parent.screen.blit(self.parent.background, (0,0))
		self.parent.screen.blit(self.texto1[0], (self.texto1[1].topleft))
		self.parent.screen.blit(self.texto2[0], (self.texto2[1].topleft))

