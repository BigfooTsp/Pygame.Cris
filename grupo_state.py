import pygame
from pygame.locals import *
import elementos
 
# [.] Tras pathfindon, eliminar comprobacion método para no pisables de escenario (mantener liksta
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
				if self.es_pisable(element):
					print ('es pisable')
					element.mover_elemento()
				else:
					print ('! %s colisiona, detiene ruta...'%element.nombre)
					element.mover_elemento()
					element.detener()
			    	
			    	# [ ANULADO ]
			    	# Inicia una nueva búsqueda de camino para continuar, evadiendo a 'elotro'.
			    	# Nota (es posible que esto genere un bucle entre dos elementos...)
					#element.pathfinding()
			element.update() 					# prepara el siguiente ciclo.


	# Comprueba que las nextpos de los elementos son pisables antes de avanzar.
	def es_pisable(self,element):
		pos = element.rectcol.inflate(-(element.velocidad-1),-(element.velocidad-1))
		pos.move_ip(element.nextpos[0]-element.map_pos[0], element.nextpos[1]-element.map_pos[1])

		#pos = element.rectcol
		retroceso = (element.direccion[0] * -1, element.direccion[1] * -1)

		# calculará las distancias necesarias para rectificar la posición del elemento si se traspasan.
		def calculadistancias():
			# distancia mínima que debería de haber entre los elementos.
			dist = (element.rectcol.w//2 + elotro.rectcol.w//2 -1 , element.rectcol.h//2 + elotro.rectcol.h//2 -1)
			# distancia real.
			distcol = (abs(element.nextpos[0] - elotro.map_pos[0]), abs(element.nextpos[1] - elotro.map_pos[1]))
			return dist, distcol

		# Comprobando colisión con elementos:
		for elotro in self.elements.values():
			if elotro.nombre != element.nombre:
			    if pos.colliderect(elotro.rectcol):
			    	dist, distcol = calculadistancias()

			    	# Ajustando las posiciones hasta tener la distancia correcta.
			    	while distcol[0] < dist[0] and distcol[1] < dist[1]:
			    		for n in 0,1:
				    		element.nextpos[n] += retroceso[n]
				    	dist, distcol = calculadistancias()

			    	return False
			    else:
			    	return True


	def intercolision(self):
		''' detecta colisiones entre todos los miembros del grupo, devuelve diccionario
		con las colisiones. {elemento1.nombre:[(elemento2.nombre, elemento2.tipo),(...)...]} '''

    	# [.] Comprobar si funciona bien con el cambio de añadir velocidad a Elementos...??

		colisiones = {}
		for element in self.elements.values():
			coltemp = {element.nombre:[]}
			cols = False
			for elotro in self.elements.values():
				if elotro.nombre != element.nombre:
				    col = element.rectcol.colliderect(elotro.rectcol)
				    if col:
				    	cols = True
				    	coltemp[element.nombre].append((elotro.nombre,elotro.tipo))
			if cols: # Si el elemento ha tenido alguna colisión:
				colisiones.update(coltemp)

		if len(colisiones) > 0:
			return colisiones
		else:
			return False


