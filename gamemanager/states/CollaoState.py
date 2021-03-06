import pygame
from pygame.locals import *
from gamemanager.states import gamestate
from utilidades import utils
import escenario, elementos, grupo_state, scrolling
import pdb

class CollaoState(gamestate.GameState):
	''' Clase básica de State de la que heredarán el resto de pantallas
	y que dirige una fase del juego '''


	def __init__(self, parent):
		print ('....instanciando pantalla CollaoState...')
		
		self.parent 	= parent 							# parent es el gameManager
		self._mapa 		= escenario.Mapa('mapadesierto') 			# Creando mapa.
		self.camara 	= scrolling.Camara(self.parent.screen.get_size(), self._mapa)
		self.grupoelementos 	= grupo_state.GrupoState()			# grupo de objetos y personajes.
		self.crear_elementos()	# configura self.grupoelementos con personajes y objetos del mapa
		self.dialog_surface 	= False	# Indica si hay un diálogo en marcha.
		self._misionPiti 		= False # Variable de misión inicial
		self.test 		= [[]]	# listado de mensajes para modo test.
		self.mouse_map_pos 	= (0,0)
		self.mostrar_minimapa = False

	#Creación inicial del grupo de personajes y objetos
	def crear_elementos(self):
		# Personajes: nombre, tipo, map_pos=[0,0], focus=False
		self.grupoelementos.add(elementos.Elemento('Cris', 'personaje_principal', [16,771], focus=True))
		self.grupoelementos.add(elementos.Elemento('Piti', 'personaje_secundario',  [523, 683]))
		# Objetos: {nombre:rect, ...}
		for k,v in self._mapa._objetos_escenario.items(): 				
			map_pos = v.topleft
			self.grupoelementos.add('k', 'objeto_escenario', map_pos, rect=v) # objeto sin sprite.

		# Generarndo matrices del mapa para pathfinding y minimapa.
		self.grupoelementos.matrizar_mapa(self._mapa._nopisable, self._mapa._mapa_size) 	# enviando a 'elementos' rectángulos nopisables del mapa.

		# añadir rectángulos de colisión del mapa:
		self.grupoelementos.mapanopisable = self._mapa._nopisable


	def sonidos(self):
		# Sonido de fondo
		fondo = pygame.mixer.music.load('utilidades/sonido/forest.ogg') # música de fondo.
		pygame.mixer.music.play(loops=-1)

		# sonido de pasos
		self.s_paso = pygame.mixer.Sound('utilidades/sonido/step.ogg')    # Paso

	def sonido_start(self, sonido, canal=1, volumen = 1):
		canal = pygame.mixer.Channel(canal) 
		canal.set_volume(volumen)
	        
		if canal.get_busy() == False:
			if sonido == 'paso':
				canal.play(self.s_paso)


	########################################################
	########## GESTIÓN DE ESTADO DE LA PANTALLA ############
	########################################################

	def start(self):
		''' Se ejecuta al iniciar la pantalla'''
		print('........GameState CollaoState started')
		self.sonidos()

	def cleanup(self):
		''' Se ejecuta al cerrar la pantalla'''
		print("GameState CollaoState Cleaned")
		pass

	def pause(self):
		'''Se ejecuta al iniciar pausa'''
		print("GameState CollaoState Paused")
		pygame.mixer.music.pause()

	def resume(self):
		'''Se ejecuta al retomar pantalla'''
		print("GameState CollaoState Resumed")
		pygame.mixer.music.unpause()


	########################################################
	################ BUCLE DE LA  PANTALLA #################
	########################################################

	# Gestiona eventos del teclado y mouse:
	def handleEvents(self, event, teclado):
		personaje = self.grupoelementos.elements[self.grupoelementos.focus()]

		# movimiento (Modifica 'nextaction' del personaje principal.)
		if teclado[pygame.K_UP]:
			personaje.calc_nextaction('camina_N')
			self.sonido_start('paso')
		if teclado[pygame.K_DOWN]:
			personaje.calc_nextaction('camina_S')
			self.sonido_start('paso')
		if teclado[pygame.K_RIGHT]:
			personaje.calc_nextaction('camina_E')
			self.sonido_start('paso')
		if teclado[pygame.K_LEFT]:
			personaje.calc_nextaction('camina_O')
			self.sonido_start('paso')

		# Clik del ratón
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_click_left = pygame.mouse.get_pressed()[0]
			mouse_click_right = pygame.mouse.get_pressed()[2]
			self.mouse_scroll_pos = pygame.mouse.get_pos()
			self.mouse_map_pos = [self.mouse_scroll_pos[0]+self.scroll[0], self.mouse_scroll_pos[1]+self.scroll[1]]

			# test
			print ('  - Mouse click (map_pos)', self.mouse_map_pos, end = '; ')

			if mouse_click_left:
				print (' > botón izquierdo')
				if self.dialog_surface == False:
					if self.grupoelementos.accesible(self.mouse_map_pos):
						self.grupoelementos.pathfinding(personaje, dest=self.mouse_map_pos)
					else:
						print ('Destino no accesible')
			elif mouse_click_right:
				print (' 	> botón derecho')

		# Pausa
		if teclado[pygame.K_p]:
			self.parent.pushState(self.parent._pausa)

		# Minimapa
		if teclado[pygame.K_m]:
			if self.mostrar_minimapa:
				self.mostrar_minimapa = False
			else:
				self.mostrar_minimapa = True


	# Actualiza el juego en función de los eventos.
	def update(self):
		self.control_misiones()
		self.colisiones(self.grupoelementos.update())

		#[.] El scrollpos se está cambiando a movimiento con flechas, deja de ser relativo al personaje, en principio.
		focus = self.grupoelementos.focus()
		focus_map_pos = self.grupoelementos.elements[focus].map_pos
		self.scroll, self.scrollpos = self.camara.update_scroll(focus_map_pos)
		for element in self.grupoelementos.elements.values():
		    element.scroll = self.scroll

		# reinicializar variables.
		self.mouse_map_pos 	= (0,0)


	# Dibuja el juego.
	def draw(self):
		self.parent.screen.blit(self.parent.background, (0,0))

		# dibuja mapa
		l=0
		for layer in self._mapa._mapatiles:
		    for f in range(self.camara.inicial[0], self.camara.lim_bottom[0]+1):
		        for c in range(self.camara.inicial[1], self.camara.lim_right[1]+1):
		        	self.parent.screen.blit(self._mapa._mapatiles[l][f][c], self.camara.plot(f, c))
		    l += 1

		# dibuja elementos
		for element in self.grupoelementos.elements.values():
		    element.dibujar(self.parent.screen)

		# dibuja diálogos
		if self.dialog_surface:
			self.parent.screen.blit(self.dialog_surface, self.diagrect.topleft)

		# dibuja minimapa
		if self.mostrar_minimapa:
			minimapa_surface = self.grupoelementos.get_minimapa()
			minimap_size = minimapa_surface.get_size()
			screen_center = self.parent.screen.get_rect().center
			pos = (screen_center[0]-minimap_size[0]//2, screen_center[1]-minimap_size[1]//2)
			self.parent.screen.blit(minimapa_surface, pos)

	########################################################
	#### GESTIÓN DE COLISIONES Y EVENTOS DE LA PANTALLA ####
	########################################################


	def colisiones(self, colisiones):
		''' Gestiona las colsiones que tienen evento. '''

		# {elemento1.nombre:[(elemento2.nombre, elemento2.tipo), ...}
		if colisiones:
			# test:
			self.test[0] = []
			for k,v in colisiones.items():
				for col in v:
					self.test[0].append('%s con %s'%(k,col))
			self.test[0].append('!COLISIONES:')

			for element in colisiones.keys():
			# Colisiones con eventos. (Nta: Recordar indicar al elemento si frena o sigue ruta)
				# Colisiones de elemento 'Cris'
				if element == 'Cris':
					for element in colisiones['Cris']:
						if self._misionPiti == 'fase_1': 	# Colisión con Piti para misión 1:
							if 'Piti' in element:
								self.grupoelementos.elements['Cris'].detener()
								self.dialogs('quiere_hablar')


	def control_misiones (self):
		''' Gestiona las misiones activas y el estado de la pantalla en general '''
		if self._misionPiti == False:
			self._misionPiti = 'fase_1'

		if self._misionPiti:
			self.misionPiti()


	def misionPiti (self):
		''' Misión 1 de la pantalla.'''

		# El personaje Piti expresa una exclamación. (fase=1)
		# Cuando Cris colisiona con Piti, se inicia menú para conversar.
		# conversan y este le manda al internado. (fase=2)


		if self._misionPiti == 'fase_1': 
			# El personaje muestra una exclamación.
			# Espera a que el jugador seleccione sí a conversar cuando colisiona con Piti.
			self.grupoelementos.elements['Piti'].expresa(icono='exclamacion')

		elif self._misionPiti == 'fase_2': 
			# Si el ratón hace clik en sí, hablamos, si es que no, seguimos en fase 1.
			None

		elif  self._misionPiti == 'fase_3': 
			# Responde que no...
			None


	def dialogs(self, dialog):
		'''Menú que aparece en la pantalla preguntando o indicando algo'''

		# Diálogos:
		def dialog_Piti_quiere_hablar():
			# En el primer encuentro entre Cris y Piti, este quiere decirle algo.
			# Se pregunta si quiere hablar y como respuesta si o no.
			self.dialog_surface = pygame.image.load('utilidades/imagenes/dialogos/Piti1(300x120).png')
			self.diagrect = self.dialog_surface.get_rect()
			self.diagrect.midbottom = (self.parent.screen_rect.centerx, self.parent.screen_rect.bottom - 15)

			mask = pygame.image.load('utilidades/imagenes/dialogos/Piti1(300x120)mask.png')
			dialog_mask = pygame.mask.from_surface(mask)
			rect_si, rect_no = dialog_mask.get_bounding_rects()

			rect_si.left += self.diagrect.left
			rect_si.top  += self.diagrect.top
			rect_no.left += self.diagrect.left
			rect_no.top  += self.diagrect.top

			print ('\n ! Esperando respuesta a diálogo')
			print ('Sí en', rect_si)
			print ('No en', rect_no)

			if rect_si.collidepoint(self.mouse_scroll_pos):

				# si en 438,970 según self.pos ... necesita el self.pos0??

				print ('Dialog:  Si')
				print ('Iniciando fase 2 de mision Piti')
				self.dialog_surface = False
				self._misionPiti = 'fase_2'
				return
			elif rect_no.collidepoint(self.mouse_scroll_pos):

				# no [565, 969] 
				print ('Dialog:  No')
				print ('Iniciando fase 3 de mision Piti')
				self.dialog_surface = False
				self._misionPiti = 'fase_3'
				return
#______________________________________________________________________

		# Selección de diálogos.
		if dialog == 'quiere_hablar':
			dialog_Piti_quiere_hablar()













