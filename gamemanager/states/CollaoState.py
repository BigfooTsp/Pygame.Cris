import pygame
from pygame.locals import *
from gamemanager.states import gamestate
from utilidades import utils, scrolling
import escenario, elementos, grupo_state

class CollaoState(gamestate.GameState):
	''' Clase básica de State de la que heredarán el resto de pantallas
	y que dirige una fase del juego '''


	#----------------------------------------------------
	# Tareas:
		# [x] Añadir mapa y personajes.
		# [x] Configurando handle events para cambiar nextaction del personaje.
		# configurar colisiones.
		# configurar eventos.
	#----------------------------------------------------

	def __init__(self, parent):
		print ('....instanciando pantalla CollaoState...')
		
		self.parent 	= parent 							# parent es el gameManager
		self._mapa 		= escenario.Mapa('mapadesierto') 			# Creando mapa.
		self.camara 	= scrolling.Camara(self.parent.screen, self._mapa)
		self.grupoelementos 	= grupo_state.GrupoState()			# grupo de objetos y personajes.
		self.crear_elementos()	# configura self.grupoelementos con personajes y objetos del mapa
		self.test 		= [[]]	# listado de mensajes para modo test.


	def crear_elementos(self):
		''' Creación inicial del grupo de personajes y objetos '''

		# Mapa
		self.grupoelementos.mapanopisable = self._mapa._nopisable 	# enviando a 'elementos' rectángulos nopisables del mapa.
		# Personajes: nombre, tipo, map_pos=[0,0], focus=False
		self.grupoelementos.add(self.parent.player) 					# Cris, personaje principal
		self.grupoelementos.add(elementos.Elemento('Piti', 'personaje_secundario',  [16*32, 21*32],))
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
		# -0- Si no está en pausa:
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

		# -7- [.]?? Cuando finalice la pantalla se actualizará parent.player
        #------------------------------------------------

		self.colisiones(self.grupoelementos.intercolision())
		self.grupoelementos.update()	
		focus = self.grupoelementos.focus()
		focus_map_pos = self.grupoelementos.elements[focus].map_pos
		self.scroll, self.scrollpos = self.camara.update_scroll(focus_map_pos)
		self.grupoelementos.update_scrollpos(self.scroll, self.scrollpos)


	def handleEvents(self, event, teclado):
		''' gestión de eventos de teclado '''

		personaje = self.grupoelementos.focus()

		# movimiento (Modifica 'nextaction' del personaje principal.)
			# [.] Hay que optimizar el control del personaje.
		if teclado[pygame.K_UP]:
			self.grupoelementos.elements[personaje].calc_nextaction('camina_N')
			self.sonido_start('paso')
		if teclado[pygame.K_DOWN]:
			self.grupoelementos.elements[personaje].calc_nextaction('camina_S')
			self.sonido_start('paso')
		if teclado[pygame.K_RIGHT]:
			self.grupoelementos.elements[personaje].calc_nextaction('camina_E')
			self.sonido_start('paso')
		if teclado[pygame.K_LEFT]:
			self.grupoelementos.elements[personaje].calc_nextaction('camina_O')
			self.sonido_start('paso')

		# Pausa
		if teclado[pygame.K_p]:
			self.parent.pushState(self.parent._pausa)


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


	def draw(self):
		''' Dibuja el juego '''

		self.parent.screen.blit(self.parent.background, (0,0))

		l=0
		for layer in self._mapa._mapatiles:
		    for f in range(self.camara.inicial[0], self.camara.lim_bottom[0]+1):
		        for c in range(self.camara.inicial[1], self.camara.lim_right[1]+1):
		        	self.parent.screen.blit(self._mapa._mapatiles[l][f][c], self.camara.plot(f, c))
		    l += 1

		for element in self.grupoelementos.elements.values():
		    element.dibujar(self.parent.screen)


	########################################################
	#### GESTIÓN DE COLISIONES Y EVENTOS DE LA PANTALLA ####
	########################################################


	def MisionesState (self):
		''' Gestiona las misiones activas y el estado de la pantalla en general '''
		None

	def Mision1 (self):
		''' Misión 1 de la pantalla.'''
		None

	# Definir las actuaciones de personajes. es posible que desde update y con un reloj












