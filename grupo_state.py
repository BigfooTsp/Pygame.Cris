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
					# [.] Si  no fuera pisable, o tropezara con algo, buscaría una ruta alternativa 2 o tres veces.
					element.mover_elemento()
					
			element.update() 					# prepara el siguiente ciclo.


	def es_pisable(self,element):
		''' Comprueba que las nextpos de los elementos son pisables antes de avanzar.
    	las anula si no es así.'''

    	# [.] Necesario con movimiento por click??

		pos = element.rectcol.inflate(-2,-2)
		pos.move_ip(element.nextpos[0]-element.map_pos[0], element.nextpos[1]-element.map_pos[1])

		# Comprobando colisión con mapa:
		#idm = pos.collidelist(self.mapanopisable)


		# Comprobando colisión con elementos:
		for elotro in self.elements.values():
			if elotro.nombre != element.nombre:
			    ide = pos.colliderect(elotro.rectcol)
		# Resultado:
		#if idm != -1 or ide:
		if ide:
			self.test[0]=str('! (%s) No pisable'%element.nombre)
			return False
		else:
			self.test[0]=str(' - Es pisable, %s avanzando'%element.nombre)
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




#### POSIBLES MÉTODOS A IMPLEMENTAR:

	def buscar(self, nombre):
		''' Busca un elemento en el grupo y retorna su posicion en mapa si está, None si no está'''
		None


	def informe(self, tipo=None):
		''' Imprime un informe con todos los elementos y sus caracterísiticas '''

		None
	def grupotipo(self, tipo):
		''' Crea diccionario de listas agrupando los elementos según su tipo '''
		# Los tipos puedes ser: pers_principal, objeto, pers_secundarios, criaturas...

		# return dict

	def distancia (self, elementA, elementB):
		''' Devuelve la distancia en pixeles entre dos elementos '''



