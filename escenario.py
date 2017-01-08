import json
import pygame
from pygame.locals import *
from utilidades import utils
# [.] Actualizar json con datos correctos.
'''
Configuración de tiledmap:
	-sin compresión ni codificación
	-ordenadas desde derecha/abajo
	-capa 'suelo'
	-capa 'objetos'
	-capa 'objetos_superpuestos'
	-capa de objetos 'nopisable'
	-añadir propiedades al mapa para ubicación inical del personaje.
		-inicial_posX
		-inicial_posY
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

class Mapa:
	
	def __init__(self, nivel, screen):
		print ("Creando Escenario " + nivel + '...')
		self._tileH = 0 # tamaño de los tiles en pixeles
		self._tileW = 0
		#self._mapaW = 0 # tamaño del mapa en tiles
		#self._mapaH = 0
		self._mapa_size = 0 # tamaño del mapa en pixeles.
		self._camara_size = (screen.get_size())
		self._transparentcolor = -1
		self._matrizMapa = [] # array multidimensional con referencias numéricas del tileset
		self._mapaImagenes = [] # array unidimensional con las imágenes (subsurface) del mapa.
		self._mapatiles = [] # array multidimensional con las imagenes (subsurfaces)
		self._mapasurface = 0 # surface del mapa completo dibujado
		self._objetos_escenario = {} # diccionario con objetos fijos del escenario.
		self._nopisable = [] # lista de rectángulos de objetos no pisables.
		self._char_posabs = [0,0] # posición inicial del personaje en el mapa.
		self._char_posrel = (0,0) # posición del personaje relativa a la cámara.
		self._coordenadas = (0, 0, 0, 0) # coordenadas del mapa que se imprimiran en pantalla.
		# rectángulo de colisión del personaje

		# Cargando archivo json
		f = open("utilidades/imagenes/"+nivel+".json", "r")
		data = json.load(f)
		f.close()

		# Configuración del mapa.
		for item in data["layers"]:
			if item['type'] == "tilelayer": # para capas del mapa
				self._matrizMapa.append(self.layers(item))
			elif item['type'] == "objectgroup": 
				if item['name'] == 'nopisable': # para los rectángulos no pisables
					for element in item['objects']:
						self._nopisable.append(self.func_nopisable(element))
				else: # crea un objeto para cada objeto de escena
					for element in item['objects']:
						self._objetos_escenario[element['name']] = objetoescena(element)

		# crear array _mapaImagenes con subsurfaces del tileset.
		for item in data["tilesets"]:
			self._mapaImagenes = self.tilesets(item)

		# crear array _mapatiles con las subsurfaces del mapa
		self.crear_mapa()

		return


	def layers(self, layer):

		self._mapaW = layer["width"]
		self._mapaH = layer["height"]

		mapa = layer['data']

		# configurando posición inicial del personaje.
		if layer['name'] == 'suelo':
			#personaje
			self._char_posabs = [
				layer['properties']["inicial_posX"], layer['properties']["inicial_posY"]]

		# resto 1 a cada referencia de data porque desde el JSON viene con
		# 1 de más y me dibuja el tile siguiente... (??)
		c = 0
		for element in mapa:
			mapa[c] = element-1
			c += 1

		# convertir vector en matriz
		layerTemp = []
		for i in range(0, len(mapa), self._mapaW):
			layerTemp.append(mapa[i:i + self._mapaW])

		return layerTemp


	def tilesets(self, tileset):

		self._tileW = tileset['tilewidth']
		self._tileH = tileset['tileheight']
		self._mapa_size = (self._tileW*self._mapaW, self._tileH*self._mapaH)


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

		# Cortar tileset (array unidimensional) usando función tiles.utils
		path = tileset['image']
		return utils.cortar_tileset(path, self._tileW, self._tileH)


	def crear_mapa(self):

		# creando maptiles
		l = 0
		f = 0
		for layer in self._matrizMapa:
			self._mapatiles.append([])
			for fila in layer:
				self._mapatiles[l].append([])
				for tile in fila:
					self._mapatiles[l][f].append(self._mapaImagenes[tile])
				f += 1
			l += 1
			f = 0

		# creando surface del mapa
		self._mapasurface = pygame.Surface((self._mapa_size[0], self._mapa_size[1]))
		x=0
		y=0
		for layer in self._mapatiles:
			for fila in layer:
				for tile in fila:
					self._mapasurface.blit(tile, (x,y))
					x += self._tileW
				y += self._tileH
				x = self._coordenadas[0]
			x = 0
			y = 0


		return


	def dibujar(self, destino):
		''' dibuja el mapa (se invoca el objeto tras instanciarlo desde aquí)'''

		for element in self._nopisable:
			pygame.draw.rect(self._mapasurface, (255,0,0), element, 1)

		camara = self._mapasurface.subsurface(self._coordenadas)
		destino.blit(camara, (0,0))	

		return	


	def func_nopisable(self, element):
		''' configura elemento para listado de zonas no pisables '''
		x = element['x']
		y = element['y']
		width = element['width']
		height = element['height']
		return pygame.Rect(x, y, width, height)


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

# Pruebas:
if __name__ == '__main__':
	pygame.init()
	display = pygame.display.set_mode((800, 600))
	pantalla = Mapa('mapadesierto', display)
	pantalla._coordenadas = (0,0,800,600)
	pantalla.dibujar(display)

	while True:
		pygame.display.update()

