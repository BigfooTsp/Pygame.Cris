import sys, os
import pygame
from pygame.locals import *
from gamemanager.singleton import *
from utilidades import utils
import elementos


class GameManager():
	# aplicando patrón singleton como metaclase.
	__metaclass__ = Singleton

	def __init__(self, test_mode, size=(800, 600)):
		print ("> Instanciando GameManager...")

		# Load content:
		self.states 	= [] 					# contenedor de states
		self.running 	= True 					# Activación de bucle de juego.
		pygame.init()
		self.clock 		= pygame.time.Clock() 	# Creación de objeto reloj.
		pygame.key.set_repeat(25, 25) 			# Activa repetición de teclas pulsadas.(delay, interval)
		self.screen 	= pygame.display.set_mode (size, 0, 32)
		pygame.display.set_caption('Cris en El Collao')
		self.test_mode 	= test_mode 			# Estableciendo variable para modo test.
		self.mouse_pos 	= (0,0)

		# pygame.display.setimage
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((209, 151, 191))
		self._pausa = 0 # Se completa con un objeto pauseState instanciado en 'juego.py'
		# instancia de personaje principal
		self.player 	= elementos.Elemento('Cris', 'personaje_principal', (5,750), focus=True)
		
		
    #########################################################
    ############ - CONTROL DEL ESTADO DEL JUEGO.  ###########
    #########################################################

	def cleanUp (self):
		'''Cierre del juego'''
		print ('Cleanup del GameManager')

		while len(self.states) > 0:
			self.states[-1].cleanup()
			self.states.pop()

	def changeState(self, gameState):
		''' cambio de estado sin romper el bucle de juego'''
		print("..Cambio de state")

		if len(self.states) > 0:
			self.states[-1].cleanup()
			self.states.pop()

		self.states.append(gameState)
		self.states[-1].start()

	def pushState(self, gameState):
		''' Pausa del juego'''
		# El gameState debería de ser la pantalla de pausa.

		if len(self.states) > 0:
			self.states[-1].pause()

		self.states.append(gameState)
		self.states[-1].start()

	def popState(self):
		'''Retoma un state pausado anteriormente'''
		print("retomando state")

		if len(self.states) > 0:
			self.states[-1].cleanup()
			self.states.pop()
		self.states[-1].resume()

	def quit(self):
		'''Cierra el juego'''
		print ("Quit")
		self.running = False
		self.cleanUp()
		sys.exit()

    #########################################################
    ################## - BUCLE DEL JUEGO.  ##################
    #########################################################

	def handleEvents(self, events):
		''' Gestión de eventos manuales'''
		teclado  = pygame.key.get_pressed()
		
		for event in events: 									# Control del personaje
			if event.type == pygame.QUIT:
				self.quit()
			if event.type == pygame.MOUSEMOTION:				# imprime la posición del mouse
		            self.mouse_pos = (pygame.mouse.get_pos())
			else:
				self.states[-1].handleEvents(event, teclado) 	# Control desde el State.


	def update(self):
		'''Update del juego'''

		# Gestiona reloj
		time = self.clock.tick(50) 		# 40,s = 25 fps
		self.fps = self.clock.get_fps()

		# Update de pantalla
		self.states[-1].update()


	def draw(self):
		'''Manda dibujar la pantalla.'''
		self.states[-1].draw()

		# Dibuja información en modo test
		if self.test_mode:
			self.test()

		pygame.display.flip()


    #########################################################
    ########### - Configuración de modo test.  ##############
    #########################################################

	def test(self):
		''' Dibuja información en modo test:'''

		# Configuración de la información a mostrar.
		_fps 			= True
		_mousepos 		= True
		_scrollpos 		= True
		_playerpos	 	= True
		_rectangulos 	= True
		_colisiones 	= True
		_modulos		= True

		# fps
		if _fps:
			fps = ('FPS: %.2f'%(self.fps))
			x=696
			y=20
			textofps = utils.texto(fps, x, y, 30, color=(242,12,146), fuente = None) # obtiene (objeto texto, rect.)
			self.screen.blit(textofps[0], (textofps[1].topleft))

		# posición del mouse:
		if _mousepos:
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
		if _scrollpos:
			scroll = (self.states[-1].scroll[0], self.states[-1].scroll[1])
			scrolltext = ('Scroll: x %i, Y %i'%(scroll[0], scroll[1]))
			x=635
			y=60
			textoscroll = utils.texto(scrolltext, x, y, 17, color=(242,12,146), fuente = None) # obtiene (objeto texto, rect.)
			self.screen.blit(textoscroll[0], (x, y))

			# Posición del personaje:
			pos = ('Personaje en: x %i, Y %i'%(self.states[-1].grupoelementos.elements['Cris'].map_pos))
			x=635
			y=75
			textopos = utils.texto(pos, x, y, 17, color=(242,12,146), fuente = None) # obtiene (objeto texto, rect.)
			self.screen.blit(textopos[0], (x, y))

		# Cuadros de colisiones en escenario:
		if _playerpos:
			screen_surface 	= pygame.display.get_surface()
			screen_rect 	= screen_surface.get_rect(topleft = scroll)
			for rect in self.states[-1].grupoelementos.mapanopisable:
				if screen_rect.colliderect(rect):
					rectscroll = rect.move(rect.left-(rect.left+scroll[0]), rect.top-(rect.top+scroll[1]))
					pygame.draw.rect(self.screen, (255,0,0), rectscroll, 1)

		# Cuadros de colisión de personajes y objetos
		if _rectangulos:
			for element in self.states[-1].grupoelementos.elements.values():
				rectcol = element.rectcol
				if screen_rect.colliderect(rectcol):
					rectscroll2 = pygame.Rect(rectcol.left-scroll[0], rectcol.top-scroll[1], rectcol.w, rectcol.h)
					pygame.draw.rect(self.screen, (100,13,255), rectscroll2, 1)

		# desde los diferentes módulos:
		test = []

		if _modulos:
			test.extend(self.states[-1].grupoelementos.test) 					# grupo_elementos					
			for criatura in self.states[-1].grupoelementos.elements.values(): 	# Elementos
				test.extend(criatura.test)

		if _colisiones:
			for col in self.states[-1].test[0]:									# colisiones
				test.append(col)
			self.states[-1].test[0] = []
		
		y = 550
		x = 600
		for mensaje in test:
			texto = utils.texto(mensaje, x, y, 17, color=(242,12,146), fuente = None) # obtiene (objeto texto, rect.)
			self.screen.blit(texto[0], (x, y))
			y -= 20 # distancia hacia la linea siguiente (la superior)
