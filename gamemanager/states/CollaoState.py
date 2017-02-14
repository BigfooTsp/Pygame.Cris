import pygame
from pygame.locals import *
from gamemanager.states import gamestate
from utilidades import utils, scrolling, a_star
import escenario, elementos, grupo_state

class CollaoState(gamestate.GameState):
	''' Clase básica de State de la que heredarán el resto de pantallas
	y que dirige una fase del juego '''


	def __init__(self, parent):
		print ('....instanciando pantalla CollaoState...')
		
		self.parent 	= parent 							# parent es el gameManager
		self._mapa 		= escenario.Mapa('mapadesierto') 			# Creando mapa.
		self.camara 	= scrolling.Camara(self.parent.screen, self._mapa)
		self.grupoelementos 	= grupo_state.GrupoState()			# grupo de objetos y personajes.
		self.crear_elementos()	# configura self.grupoelementos con personajes y objetos del mapa
		self.dialog_surface 	= False	# Indica si hay un diálogo en marcha.
		self._misionPiti 		= False # Variable de misión inicial
		self.test 		= [[]]	# listado de mensajes para modo test.
		self.mouse_map_pos 	= (0,0)

	def crear_elementos(self):
		''' Creación inicial del grupo de personajes y objetos '''

		# Mapa
		self.grupoelementos.mapanopisable = self._mapa._nopisable 	# enviando a 'elementos' rectángulos nopisables del mapa.
		# Personajes: nombre, tipo, map_pos=[0,0], focus=False
		self.grupoelementos.add(elementos.Elemento('Cris', 'personaje_principal', (16,761), matriz_astar=self._mapa.matriz_astar(22), focus=True))
		self.grupoelementos.add(elementos.Elemento('Piti', 'personaje_secundario',  (523, 683), matriz_astar=self._mapa.matriz_astar(22)))
		# Objetos: {nombre:rect, ...}
		for k,v in self._mapa._objetos_escenario.items(): 				
			map_pos = v.topleft
			self.grupoelementos.add('k', 'objeto_escenario', map_pos, rect=v) # objeto sin sprite.

			# Notas:
			# Configurar características individuales de objetos si se requiere.
			# Es posible que se puedan añadir atributos en tiledmaps
			# 		y procesarlos aquí luego automáticamente.
			# Para cambiar la velocidad cambiar su variable orientacion.
			# Para añadir una conducta, siempre utilizar el metodo add() de elementos.Conducta.
		
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


	def update(self):
		''' Actualiza el juego en función de los eventos.'''
        #------------------------------------------------
		# -0- Repasa estado de misiones.
		# -1- Detecta colisiones y las manda gestionar si las hay
		# 		- paralelo a handleEvents. (x.nextaction, x.nextpos)
		# 		- Gestiona nuevo evento por colisión, si se requiere, que deriva en 
		#			nueva acción (nexaction) o en una lista de acciones (conducta_programada)
		# -2- Actualizar elementos
		# 		+ Comprueba si las nuevas posiciones son pisables.
		# 		+ selecciona elementos con siguientes acciones.
		#			+ cambia el sprite.
		#			+  Emite sonidos de movimiento
		# 			+ borra nextpos si no es pisable.
		#		+ Actualiza las posiciones actuales por nextpos y nextaction
		# 		+ Actualiza sus rectángulos
		#		+ Actualiza siguientes acciones futuras si hay conducta programada. (element.update())
		# -3- Actualiza scroll (posiciones antes de dibujar)
		# 		+ obtiene scroll y scrollpos
		# 		+ Actualiza la variable 'scroll_pos' de los elementos (que indicará su pos en pantalla).
		# -5- Dibuja la pantalla
		#		+- Layers con sprites teniendo en cuenta alturas y preferencias.
		# -6- Reinicializar las variables que lo necesitan.
		#
		# -7- [.]?? Cuando finalice la pantalla se actualizará parent.player
        #------------------------------------------------

		self.control_misiones()
		self.colisiones(self.grupoelementos.intercolision())
		self.grupoelementos.update()	

		focus = self.grupoelementos.focus()
		focus_map_pos = self.grupoelementos.elements[focus].map_pos

		#[.] El scrollpos se está cambiando a movimiento con flechas, deja de ser relativo al personaje, en principio.
		
		self.scroll, self.scrollpos = self.camara.update_scroll(focus_map_pos)
		for element in self.grupoelementos.elements.values():
		    element.scroll = self.scroll

		# reinicializar variables.
		self.mouse_map_pos 	= (0,0)


	def handleEvents(self, event, teclado):
		''' gestión de eventos de teclado '''

		personaje = self.grupoelementos.elements[self.grupoelementos.focus()]

		# [.] Cambiar para incorporar movimiento mediante click de ratón.
		# [.] Las flechas moverán el scroll.
		# [.] El icono del mouse cambiará con la acción activable por click.

		# movimiento (Modifica 'nextaction' del personaje principal.)
			# [.] Hay que optimizar el control del personaje.
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
			print ('(scroll_pos)', self.mouse_scroll_pos)

			if mouse_click_left:
				print (' > botón izquierdo')
				if self.dialog_surface == False:
					if a_star.accesible(self.mouse_map_pos, personaje.matriz_astar, width=personaje.rectcol.w):
						personaje.pathfinding(pos=self.mouse_map_pos)
					else:
						print ('Destino no accesible')
			elif mouse_click_right:
				print (' 	> botón derecho')

		# Pausa
		if teclado[pygame.K_p]:
			self.parent.pushState(self.parent._pausa)

		# Selección de respuesta en diálogos.
		#if self.dialog_surface:


	# Dibuja el juego.
	def draw(self):
		self.parent.screen.blit(self.parent.background, (0,0))

		l=0
		for layer in self._mapa._mapatiles:
		    for f in range(self.camara.inicial[0], self.camara.lim_bottom[0]+1):
		        for c in range(self.camara.inicial[1], self.camara.lim_right[1]+1):
		        	self.parent.screen.blit(self._mapa._mapatiles[l][f][c], self.camara.plot(f, c))
		    l += 1

		for element in self.grupoelementos.elements.values():
		    element.dibujar(self.parent.screen)

		if self.dialog_surface:
			self.parent.screen.blit(self.dialog_surface, self.diagrect.topleft)



	########################################################
	#### GESTIÓN DE COLISIONES Y EVENTOS DE LA PANTALLA ####
	########################################################


	def colisiones(self, colisiones=False):
		''' Gestiona las colsiones que tienen evento. '''

		# {elemento1.nombre:[(elemento2.nombre, elemento2.tipo), ...}
		if colisiones:

			# test:
			self.test[0] = []
			for k,v in colisiones.items():
				for col in v:
					self.test[0].append('%s con %s'%(k,col))
			self.test[0].append('!COLISIONES:')

			# Colisiones de elemento 'Cris'
			if 'Cris' in colisiones.keys():
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




		# Selección de diálogos.
		if dialog == 'quiere_hablar':
			dialog_Piti_quiere_hablar()













