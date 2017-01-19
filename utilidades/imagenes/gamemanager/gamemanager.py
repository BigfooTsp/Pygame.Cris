import sys, os
import pygame
from pygame.locals import *
from gamemanager.singleton import *
from utilidades import utils
import personaje


class GameManager():
	# aplicando patrón singleton como metaclase.
	__metaclass__ = Singleton

	def __init__(self, test_mode, size=(800, 600)):
		print ("> Instanciando GameManager...")

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
		self.clock = pygame.time.Clock()

		# Estableciendo variable para modo test.
		self.test_mode = test_mode

		self.mouse_pos = (0,0)


	def cleanUp (self):
		'''Cierre del juego'''
		print ('Cleanup del GameManager')

		while len(self.states) > 0:
			state = self.states.pop()
			state.cleanUp()

		sys.exit()


	def changeState(self, gameState):
		''' cambio de estado sin romper el bucle de juego'''
		print("..Cambio de state")

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
		            self.mouse_pos = (pygame.mouse.get_pos())
			else:
				self.states[-1].handleEvents(event, teclado)

		# Hacer pausa
		#pygame.time.delay(milliseconds) -> int


	def update(self):

		# Gestiona reloj
		time = self.clock.tick(50) 		# 40,s = 25 fps
		self.fps = self.clock.get_fps()

		# Update de pantalla
		self.states[-1].update()

	def draw(self):
		# Dibuja pantalla.
		self.states[-1].draw()

		# Dibuja información en modo test
		if self.test_mode:
			self.test()

		pygame.display.flip()

	def quit(self):
		print ("Quit")
		self.running = False
		self.cleanUp()
	


	def test(self):
		''' Dibuja información en modo test:'''

		# fps
		fps = ('FPS: %.2f'%(self.fps))
		x=696
		y=20
		textofps = utils.texto(fps, x, y, 30, color=(242,12,146), fuente = None) # obtiene (objeto texto, rect.)
		self.screen.blit(textofps[0], (textofps[1].topleft))

		# posición del mouse:
		mouse = ('Mouse: '+str(self.mouse_pos))
		x=650
		y=30
		textomouse = utils.texto(mouse, x, y, 17, color=(242,12,146), fuente = None) # obtiene (objeto texto, rect.)
		self.screen.blit(textomouse[0], (x, y))

		# Posición del scroll:
		scroll = ('Scroll: x %i, Y %i'%(self.states[-1].scroll.scrollx, self.states[-1].scroll.scrolly ))
		x=650
		y=45
		textoscroll = utils.texto(scroll, x, y, 17, color=(242,12,146), fuente = None) # obtiene (objeto texto, rect.)
		self.screen.blit(textoscroll[0], (x, y))

		# Posición del personaje:
		pos = ('Personaje en: x %i, Y %i'%(self.states[-1]._personajes[0][1][0], self.states[-1]._personajes[0][1][1]))
		x=650
		y=60
		textopos = utils.texto(pos, x, y, 17, color=(242,12,146), fuente = None) # obtiene (objeto texto, rect.)
		self.screen.blit(textopos[0], (x, y))

		# desde los diferentes módulos:
		test = []
		test.extend(self.states[-1]._mundo.test)
		for personaje in self.states[-1]._personajes:
			test.extend(personaje[0].test)
		test.extend(self.states[-1].test[0]) # colisiones)
		test.extend(self.states[-1].scroll.test)

		
		y = 580
		x = 600
		for element in test:
			texto = utils.texto(element, x, y, 17, color=(242,12,146), fuente = None) # obtiene (objeto texto, rect.)
			y -= 20 # distancia hacia la linea siguiente (la superior)
			self.screen.blit(texto[0], (x, y))
