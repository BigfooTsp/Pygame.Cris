import pygame
from pygame.locals import *
import elementos
 
# [.] Tras pathfinding, eliminar comprobacion método para no pisables de escenario (mantener liksta
# 		para generar matriz de mapa) pero eliminar comprobación a cada paso del personaje. YA que se
# 		cokprueba con la creación de la ruta.

class GrupoState():
	''' Clase que contiene grupos de personajes o objetos. 
	Comprueba colisiones y ordena dibujarlos'''

	elements 		= {}	
	mapanopisable 	= False
	test 			= ['']								# listado de mensajes para modo test.

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


	def update(self):
		''' Busca elementos con cambios y actualiza sus posiciones
		y rectángulos tras comprobar que la nueva posición es pisable'''

		# [.] Modificar para movimiento por click de ratón

		for element in self.elements.values():
			if element.nextaction:
				element.actualizar_sprite()
			element.mover_elemento()
			element.update()
		colisiones = self.intercolision()

		return colisiones


	# Detecta colisiones y reajusta la posición de los elementos para que no se atraviesen.
	# Devuelve lista con las colisiones detectadas.
	def intercolision(self):
		# calculará las distancias necesarias para rectificar la posición del elemento si se traspasan.
		def calculadistancias(element):
			# distancia mínima que debería de haber entre los elementos.
			dist = (element.rectcol.w//2 + elotro.rectcol.w//2 +1 , element.rectcol.h//2 + elotro.rectcol.h//2 +1)
			# distancia real.
			distcol = (abs(element.nextpos[0] - elotro.map_pos[0]), abs(element.nextpos[1] - elotro.map_pos[1]))
			return dist, distcol

		colisiones = {}
		for element in self.elements.values():
			retroceso = (element.direccion[0] * -1, element.direccion[1] * -1)
			coltemp = {element.nombre:[]}
			cols = False
			for elotro in self.elements.values():
				if elotro.nombre != element.nombre:
					# Detecta si hay colisión.
				    if element.rectcol.colliderect(elotro.rectcol):
				    	cols = True
				    	coltemp[element.nombre].append((elotro.nombre,elotro.tipo))

				    	# Ajustando las posiciones hasta tener la distancia correcta.
				    	dist, distcol = calculadistancias(element)
				    	while distcol[0] < dist[0] and distcol[1] < dist[1]:
				    		for n in 0,1:
					    		element.nextpos[n] += retroceso[n]
					    	dist, distcol = calculadistancias(element)
					    	element.mover_elemento()
			# Si el elemento ha tenido alguna colisión:
			if cols: 
				colisiones.update(coltemp)
		# Si ha habido colisiones, devuelve diccionario: {elemento1.nombre:[(elemento2.nombre, elemento2.tipo), ...}
		if len(colisiones) > 0:
			return colisiones
		else:
			return False


