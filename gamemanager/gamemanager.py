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
		self.screen = pygame.display.set_mode (size, 0, 32)
		pygame.display.set_caption('Cris en El Collao')
		# pygame.display.setimage
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((209, 151, 191))
		
		# instancia de personaje principal
		self.jugador = personaje.Personaje('Cris') # El personaje se copia en el State. Habría que actualizarlo al cambiar esta.
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
		mousepos 	= ('Mouse(pos):      '+str(self.mouse_pos))
		x=635
		y=30
		textomouse = utils.texto(mousepos, x, y, 17, color=(242,12,146), fuente = None) # obtiene (objeto texto, rect.)
		self.screen.blit(textomouse[0], (x, y))

		v_mouseposabs = (self.mouse_pos[0]+self.states[-1].scroll[0], self.mouse_pos[1]+self.states[-1].scroll[1])
		mouseposabs = ('Mouse(posabs):'+str(v_mouseposabs))

		x2= 635
		y2= 45
		textomouse2 = utils.texto(mouseposabs, x2, y2, 17, color=(242,12,146), fuente = None) # obtiene (objeto texto, rect.)
		self.screen.blit(textomouse2[0], (x2, y2))

		# Posición del scroll:
		scroll = (self.states[-1].scroll[0], self.states[-1].scroll[1])
		scrolltext = ('Scroll: x %i, Y %i'%(scroll[0], scroll[1]))
		x=635
		y=60
		textoscroll = utils.texto(scrolltext, x, y, 17, color=(242,12,146), fuente = None) # obtiene (objeto texto, rect.)
		self.screen.blit(textoscroll[0], (x, y))

		# Posición del personaje:
		pos = ('Personaje en: x %i, Y %i'%(self.states[-1]._personajes['Cris'].posabs))
		x=635
		y=75
		textopos = utils.texto(pos, x, y, 17, color=(242,12,146), fuente = None) # obtiene (objeto texto, rect.)
		self.screen.blit(textopos[0], (x, y))

		# Cuadros de colisiones en escenario:
		screen_surface 	= pygame.display.get_surface()
		screen_rect 	= screen_surface.get_rect(topleft = scroll)
		for rect in self.states[-1]._mapa._nopisable:
			if screen_rect.colliderect(rect):
				rectscroll = rect.move(rect.left-(rect.left+scroll[0]), rect.top-(rect.top+scroll[1]))
				pygame.draw.rect(self.screen, (255,0,0), rectscroll, 1)

		# Cuadros de colisión de personajes y objetos
		for k,v in self.states[-1]._mundo.rectcols:
			rect = self.states[-1]._mundo.rectcols[k]
			if screen_rect.colliderect(rect):
				print ('############rect', k, rect)
				rectscroll = rect.move(rect.left-(rect.left+scroll[0]), rect.top-(rect.top+scroll[1]))
				pygame.draw.rect(self.screen, (100,13,255), rectscroll, 1)

		# desde los diferentes módulos:
		test = []
		test.extend(self.states[-1]._mundo.test)
		for criatura in self.states[-1]._personajes.values():
			test.extend(criatura.personaje.test)
		test.extend(self.states[-1].test[0]) # colisiones)
		
		y = 580
		x = 600
		for element in test:
			texto = utils.texto(element, x, y, 17, color=(242,12,146), fuente = None) # obtiene (objeto texto, rect.)
			y -= 20 # distancia hacia la linea siguiente (la superior)
			self.screen.blit(texto[0], (x, y))
