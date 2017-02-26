import pygame
from pygame.locals import *
import elementos, a_star
from utilidades import utils
import pdb
# [.] Tras pathfinding, eliminar comprobacion método para no pisables de escenario (mantener liksta
# 		para generar matriz de mapa) pero eliminar comprobación a cada paso del personaje. YA que se
# 		cokprueba con la creación de la ruta.




	########################################################
	################# OBJETO GRUPO_STATE ###################
	########################################################


class GrupoState():
	''' Clase que contiene grupos de personajes o objetos. 
	Comprueba colisiones y ordena dibujarlos'''

	elements 		= {}	
	test 			= ['']								# listado de mensajes para modo test.

	########################################################
	################ GESTIÓN DE ELEMENTOS ##################
	########################################################

	def add(self, elemento):
		''' añade personajes al grupo '''
		self.elements.update({elemento.nombre:elemento})


	def delete(self, nombre):
		''' borra personajes al grupo '''
		try:
			self.elements.pop(nombre)
		except:
			print ('Error: No se encuentra el elemento a borrar.')


	def focus(self):
		''' devuelve el nombre del elemento que está como foco '''
		for element in self.elements.values():
			if element.focus:
				return element.nombre


	# Busca elementos con cambios y actualiza sus posiciones
	def update(self):
		for element in self.elements.values():
			if element.nextaction:
				element.actualizar_sprite()
			element.mover_elemento()
			element.update()

		colisiones = self.intercolision()

		return colisiones


	########################################################
	############ GESTIÓN DE MAPA Y PATHFINDING #############
	########################################################

	# Devuelve la posición de la celda desde una coordenada.
	def buscarPos(self, pos):
		width = 22
		mapa = self.matriz_mapa
		for f in range(0, len(mapa)):
			for c in range(0, len(mapa[0])):
				cel = pygame.Rect(c*width, f*width, width, width)
				if cel.collidepoint(pos):
					return [f, c]


	# Comprueba en la matriz del mapa si una posición (pixel) es pisable
	def accesible(self, pos):
		f,c = self.buscarPos(pos)
		if self.matriz_mapa[f][c] == 0:
			return True
		else:
			return False


	# Crea lista para caminar hacia un punto concreto del mapa.
	def pathfinding(self, element, orig=False, dest=False):
		# Se crean dos variables mapa y destino por si, en caso de colisión, necesita recalcularse la ruta.
		if not orig: 
		    orig = element.map_pos
		if not dest: 
		    dest = element.destino

		element.destino = dest
		mapa = self.matriz_mapa

		astar = a_star.Pathfinding(orig, dest, mapa, element.rectcol.w)
		if astar.camino != -1:
		    element.ruta = astar.waypoints_pixel
		    return True
		else:
		    return False

	# Crea una matriz con el mapa donde 0 es pisable y 1 no.
	def matrizar_mapa(self, mapa_nopisable, mapasize):
		matrizm = []
		width = 22
		
		fil = 0
		for y in range(0, mapasize[0], width):
			matrizm.append([])
			for x in range (0, mapasize[1], width):
				cel = pygame.Rect(x, y, width, width)
				if cel.collidelist(mapa_nopisable) == -1:
					matrizm[fil].append(0)
				else:
					matrizm[fil].append(1)
			fil += 1

		self.matriz_mapa = matrizm


	# Crea una matriz con el mapa.
	def matrizar_minimapa(self):
		matriz = [l[:] for l in self.matriz_mapa]
		
		for element in self.elements.values():
			f,c = self.buscarPos(element.map_pos)
			matriz[f][c] = 2

		return matriz


	# crea una superficie minimapa donde se representa el mapa y elementos
	def get_minimapa(self):
		celwidth = 3
		minimap_w = len(self.matriz_mapa)*celwidth
		minimap_h = len(self.matriz_mapa[0])*celwidth
		matriz = self.matrizar_minimapa()

		pisable 	= pygame.image.load('utilidades/imagenes/minimapa/pisable.png')
		nopisable 	= pygame.image.load('utilidades/imagenes/minimapa/nopisable.png')
		elemento 	= pygame.image.load('utilidades/imagenes/minimapa/elemento.png')
		foco 		= pygame.image.load('utilidades/imagenes/minimapa/foco.png')

		minimap_surface = pygame.Surface((minimap_w, minimap_h))
		x = 0
		y = 0
		for f in matriz:
			for c in f:
				if c == 0:
					minimap_surface.blit(pisable, (x,y))
				elif c == 1:
					minimap_surface.blit(nopisable, (x,y))
				elif c == 2:
					minimap_surface.blit(elemento, (x,y))
				x += celwidth
			y += celwidth
			x = 0

		minimap_surface.convert_alpha()
		return minimap_surface


	########################################################
	################ GESTIÓN DE EVENTOS ####################
	########################################################

	# Detecta colisiones y reajusta la posición de los elementos para que no se atraviesen.
	# Devuelve lista con las colisiones detectadas.
	def intercolision(self):
		# calculará las distancias necesarias para rectificar la posición del elemento si se traspasan.

		# Ajustando las posiciones hasta tener la distancia correcta.
		def reajustar_pos(element, elotro):
			# distancia mínima que debería de haber entre los elementos.
			dist = (element.rectcol.w//2 + elotro.rectcol.w//2, element.rectcol.h//2 + elotro.rectcol.h//2)
			# distancia real.
			distcol = (abs(element.nextpos[0] - elotro.map_pos[0]), abs(element.nextpos[1] - elotro.map_pos[1]))

			retroceso = [0,0]
			for n in 0,1:
				if element.nextpos[n] > elotro.map_pos[n]:
					retroceso[n] = +1
				elif element.nextpos[n] < elotro.map_pos[n]:
					retroceso[n] = -1
				elif element.nextpos[n] == elotro.map_pos[n]:
					retroceso[n] = 0

			distancia = [0,0]
			for n in 0,1: distancia[n] = (distcol[n]-dist[n])
			if abs(distancia[0]) > abs(distancia[1]):
				distancia = abs(distancia[0])
			else:
				distancia = abs(distancia[1])

			nextpos = [0,0]
			for n in 0,1: nextpos[n] = element.nextpos[n]+distancia*retroceso[n]
			element.nextpos = nextpos
			element.mover_elemento()
		#______________________________________________________________________
		colisiones = {}
		for element in self.elements.values():
			coltemp = {element.nombre:[]}
			cols = False
			for elotro in self.elements.values():
				if elotro.nombre != element.nombre:
					# Detecta si hay colisión.
				    if element.rectcol.colliderect(elotro.rectcol):
				    	cols = True
				    	coltemp[element.nombre].append((elotro.nombre,elotro.tipo))
				    	reajustar_pos(element,elotro)
			# Si el elemento ha tenido alguna colisión:
			if cols: 
				colisiones.update(coltemp)
		# Si ha habido colisiones, devuelve diccionario: {elemento1.nombre:[(elemento2.nombre, elemento2.tipo), ...}
		if len(colisiones) > 0:
			return colisiones
		else:
			return False
