import json
import pygame
from pygame.locals import *
from utilidades import utils

'''
Notas:
	- Sobre la creación de la matriz para pathfinder: 
		El cuadro por defecto es de 22x22vp r el cual debe de caber el elemento en movimiento, si este fuera más grande, habría
		que modificar el cuadro o asegurarse de que no hay espacios demasiado pequeños para este.
'''


class Mapa:
	''' crea un listado con los tilesets del escenario, se dibuja mediante el módulo scroll. '''
	
	def __init__(self, nivel):
		print ("....Creando Escenario " + nivel + '...')
		#self._tileH = 0 					# tamaño de los tiles en pixeles
		#self._tileW = 0
		#self._mapaW = 0 					# tamaño del mapa en tiles
		#self._mapaH = 0
		#self._mapa_size = 0 				# tamaño del mapa en pixeles.
		self._transparentcolor = -1
		self._list_tiles = []				# lista con las imágenes de los tilesets.
		self._mapatiles = [] 				# array con las imagenes (subsurfaces).
		self._objetos_escenario = {}		# diccionario con objetos del escenario.
		self._nopisable = [] 				# lista de rectángulos de objetos no pisables.
		
		self.load_map(nivel) 	# cargar y configurar mapa
		
		for tileset in data["tilesets"]: # crear lista _list_tiles con surfaces del tileset.
			self.tilesets(tileset)

		self.layers() 			# Configuración de layers. (suelo, no pisable, objetos)
		self.mapear_completo()	# obtiene self._mapasurface con objeto surface del mapa completo.
		self.map_info()			# Mostrar información del mapa creado


	def load_map(self, nivel):
		''' Cargar y configurar mapa'''
		global data

		# Cargando archivo json
		f = open("utilidades/imagenes/"+nivel+".json", "r")
		data = json.load(f)
		f.close()

		# Configurando variables del mapa.
		self._mapaW = data["width"] 		# Anchura en tiles		
		self._mapaH = data["height"]		# Altura en tiles
		self._tileW = data['tilewidth'] 	# Anchura del tile
		self._tileH = data['tileheight']	# Altura del tile	
		self._mapa_size = (self._tileW*self._mapaW, self._tileH*self._mapaH)


	def layers(self):
		''' genera array con los tiles del mapa '''

		############ NOTA. Borrar si correcto porque he borrado variable mapa por layer['data']
		# resto 1 a cada referencia de layer['data'] porque desde el JSON viene con +1.

		l = 0 # Contador de layers.
		for layer in data["layers"]: 						
			if layer['type'] == "tilelayer":
				self._mapatiles.append([])

				# convertir lista numérica en matriz con los maptiles:
				matrizmapa = []
				for i in range(0, len(layer['data']), self._mapaW):
					matrizmapa.append(layer['data'][i:i + self._mapaW])
					self._mapatiles[l].append([])
				f = 0
				for fila in matrizmapa:
					for tile in fila:
						self._mapatiles[l][f].append(self._list_tiles[tile-1]) # tile-1???
					f +=1 
				l += 1

			# Procesando objetos.
			if layer['type'] == "objectgroup": 
				if layer['name'] == 'nopisable': 			# para los rectángulos no pisables
					for element in layer['objects']:
						self._nopisable.append(pygame.Rect(element['x'], element['y'], 
												element['width'], element['height']))
				else: 										
					for element in layer['objects']: 		# para los objetos de escenario
						self._objetos_escenario[element['name']] = pygame.Rect(element['x'], element['y'], 
																	element['width'], element['height'])


	def tilesets(self, tileset):
		''' configura self._list_tiles. '''

		imgTemp = tileset['name']
		self._transparentcolor = tileset['transparentcolor']
		img = pygame.image.load('utilidades/imagenes/' + imgTemp + '.png')
		img = img.convert()

		# convierte valor alpha (#ffffff) a decimal (255,255,255)
		if self._transparentcolor != 1:
			alpha = self._transparentcolor
			alpha = alpha.lstrip('#')
			lv = len(alpha)
			alpha = tuple(int(alpha[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

		# Crea lista _list_tiles con los elementos de los tilesets del mapa.
		path = tileset['image']
		image = utils.cargar_imagen(path, self._tileW, self._tileH)
		rectSp = image.get_rect()

		for f in range(self._mapaH):
			for c in range(self._mapaW):
				self._list_tiles.append(image.subsurface((rectSp.left, rectSp.top, self._tileW, self._tileH)))
				rectSp.left += self._tileW
			rectSp.top += self._tileH
			rectSp.left = 0


	def mapear_completo(self):
		''' Método para otros usos. Devuelve superficie con el mapa completo '''

		# creando surface del mapa
		mapasurface = pygame.Surface((self._mapa_size[0], self._mapa_size[1]))
		x=0
		y=0

		for layer in self._mapatiles: # (50 x 50)
			for fila in layer:
				for tile in fila:
					mapasurface.blit(tile, (x,y))
					x += self._tileW
				y += self._tileH
				x = 0
			x=0
			y=0

		return	mapasurface

	# Devuelve una matriz donde 0 es pisable y 1 no.
	def matriz_astar(self, width):
		matriz = []
		fil = 0
		screen_rect = pygame.Rect(0, 0, self._mapa_size[0], self._mapa_size[0])

		for y in range(0, self._mapa_size[0], width):
			matriz.append([])
			for x in range (0, self._mapa_size[1], width):
				cel = pygame.Rect(x, y, width, width)
				#if screen_rect.contains(cel):
				if cel.collidelist(self._nopisable) == -1:
					matriz[fil].append(0)
				else:
					matriz[fil].append(1)
			fil += 1

		return matriz


	def map_info(self):
		''' Muestra en consola las características del mapa creado.'''
		print('      ______________________________________________________')
		print("      ### Características del mapa %s ###\n" %data["tilesets"][0]['name'])
		print("         Tamaño de los tiles %i x %i"%(data["tilewidth"], data["tileheight"]))
		print('         Tamaño del mapa en pixeles= %s x %s' %(data["tilesets"][0]["imagewidth"], data["tilesets"][0]['imageheight']))
		print('         Tamaño del mapa en tiles = filas(%i) columnas(%i)'%(data["width"], data["height"]))

		print('         capas:')
		for layer in data['layers']:
			print('             ', layer["name"])

		print('         objetos:')
		for key, value in self._objetos_escenario:
			print('              %s - %s'%(key, value))
		print('      ______________________________________________________')



class objetoescena():
	''' Extrae los objetos de escena desde tiledmaps '''

	def __init__(self, obj):
		''' atributos y características del objeto'''
		self._nombre = obj["name"]
		self._objectW = obj["width"]
		self._objectH = obj["height"]
		self._objecttype = obj["type"]
		self._visible = obj["visible"]
		self._objectpos = (obj["x"], obj["y"])
		#[.] solucionar problema al sumar negativos
		self._objrect = pygame.Rect(
			self._objectpos[0], self._objectpos[1], (
				self._objectpos[0]+self._objectW), (self._objectpos[1]+self._objectH))



class Tile():
	''' clase que contiene las características de los tiles de los layers '''
	None


'''
Configuración de tiledmap:
	-sin compresión ni codificación
	-ordenadas desde derecha/abajo
	-capa 'suelo'
	-capa 'objetos'
	-capa 'objetos_superpuestos'
	-capa de objetos 'nopisable'
	-exportado en JSON
	-Hacer una capa 'nopisable'

	[.] desplazamiento del mapa
		 En el json pongo una posición de inicio al personaje.
		 esta posición debe de estar centrada en la pantalla (800x600)
		 Los rectángulos de colisión y la pantalla deben de adaptarse a la posición
		 del personaje.

	[.] COnvertir la ruta de la imagen del json en relativo.
	[.] Optimizar los rectángulos del mapa de colisión.

'''
