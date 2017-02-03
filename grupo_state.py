import pygame
from pygame.locals import *
import elementos
 

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
		for element in self.elements.values():
			if element.nextaction:
				element.actualizar_sprite()		
				if self.es_pisable(element):
					element.mover_elemento()
					
			element.update() 					# prepara el siguiente ciclo.


	def es_pisable(self,element):
		''' Comprueba que las nextpos de los elementos son pisables antes de avanzar.
    	las anula si no es así.'''

		pos = element.rectcol.inflate(-2,-2)
		pos.move_ip(element.avance())

		# Comprobando colisión con mapa:
		idm = pos.collidelist(self.mapanopisable)
		# Comprobando colisión con elementos:
		for elotro in self.elements.values():
			if elotro.nombre != element.nombre:
			    ide = pos.colliderect(elotro.rectcol)
		# Resultado:
		if idm != -1 or ide:
			self.test[0]=str('! (%s) No pisable'%element.nombre)
			element.conducta.bloqueado = True
			return False
		else:
			self.test[0]=str(' - Es pisable, %s avanzando'%element.nombre)
			if element.conducta.bloqueado == True:
				element.conducta.bloqueado == False
			return True


	def update_scrollpos(self, scroll, scroll_pos):
		''' Actualiza posición (x.pos) en cámara del personaje'''
        # Posición del personaje en cámara.
		for element in self.elements.values():
		    if element.focus:
		        element.scroll_pos = scroll_pos
		    else:
		        element.scroll_pos = [element.map_pos[0] - scroll[0], element.map_pos[1] - scroll[1]]


	def intercolision(self):
		''' detecta colisiones entre todos los miembros del grupo, devuelve diccionario
		con las colisiones. {elemento1.nombre:[(elemento2.nombre, elemento2.tipo),(...)...]} '''
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



