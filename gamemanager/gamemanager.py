import sys, os
import pygame
from pygame.locals import *
from gamemanager.singleton import *
import personaje


class GameManager():
	# aplicando patrón singleton como metaclase.
	__metaclass__ = Singleton

	def __init__(self, size=(800, 600)):
		print ("Instanciando GameManager...")

		self.states = [] # contenedor de states
		self.running = True # Activación de bucle de juego.

		# Load content:
		pygame.init()
		pygame.key.set_repeat(25, 25) # Activa repetición de teclas pulsadas.(delay, interval)
		self.screen = pygame.display.set_mode (size)
		pygame.display.set_caption('Cris en El Collao')
		# pygame.display.setimage
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((209, 151, 191))
		
		# instancia de personaje principal
		self.jugador = personaje.Personaje('Cris')


	def cleanUp (self):
		'''Cierre del juego'''
		print ('Cleanup del GameManager')

		while len(self.states) > 0:
			state = self.states.pop()
			state.cleanUp()

		sys.exit()


	def changeState(self, gameState):
		''' cambio de estado sin romper el bucle de juego'''
		print("Cambio de state")

		if len(self.states) > 0:
			state = self.states.pop()
			state.cleanUp()

		self.states.append(gameState)
		self.states[-1].start()

	def pushState(self, gameState):
		print("iniciar state")

		if len(self.states) > 0:
			state = self.states.pop()
			state.pause()

		self.states.append(gameState)
		self.states[-1].start()

	def popstate(self, gameState):
		print("retomando state")

		if len(self.states) > 0:
			state = self.states.pop()
			state.cleanUp()

		self.states.append(gameState)
		self.states[-1].resume()


	def handleEvents(self, events):
		''' gestión de eventos'''
		teclado  = pygame.key.get_pressed()

		for event in events:
			if event.type == pygame.QUIT:
				self.quit()

			if event.type == pygame.MOUSEMOTION:
		            # imprime la posición del mouse
		            x, y = pygame.mouse.get_pos()
		            print ('mouse x-%i y-%i' %(x, y))
			else:
				self.states[-1].handleEvents(event, teclado)


	def update(self):
		self.states[-1].update()

	def draw(self):
		self.states[-1].draw()
		pygame.display.flip()

	def quit(self):
		print ("Quit")
		self.running = False
		self.cleanUp()
