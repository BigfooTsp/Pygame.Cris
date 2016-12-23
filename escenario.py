import json
import pygame
from pygame.locals import *
from utils import tiles

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
'''
# [.] trabajar con numpy
# [.] utilizar codificación y compresión
# [.] iteración de layers desde la llamada a la función
# para la capa pisable solo necesito sacar las coordenadas, no las imagenes

class Mapa:
	''' Genera array con los datos de tiledmap.'''

	_tileH = 0
	_tileW = 0
	_MapaW = 0
	_MapaH = 0

	_transparentcolor = -1

	# array multidimensional, cada lista con las referencias 
	# numéricas al tileset de la layer correspondiente del mapa 
	_matrizMapa = []

	# array unidimensional con las imágenes (subsurface) del mapa.
	_mapaImagenes = []

	# array multidimensional con las imagenes (subsurfaces) incorporadas
	# y organizadas por layers y filas.
	_mapatiles = []

	# diccionario que guardará los objetos fijos del escenario.
	_objetos_escenario = {}

	# objetos no pisables
	_nopisable = []



	def CargarMapa(self, nivel):

		# carga archivo JSON con DATA sin comprimir ni codificar (en CSV)
		f = open("imagenes/"+nivel+".json", "r")
		data = json.load(f)
		f.close()

		# distingue entre capas tilelayer, de objetos, pisable y las procesa.
		for item in data["layers"]:
			if item['type'] == "tilelayer": # para mapas
				self._matrizMapa.append(self.layers(item))
			elif item['type'] == "objectgroup": 
				if item['name'] == 'nopisable': # para los rectángulos no pisables
					self.nopisable(item) 
				else: # para los objetos [.] se pueden meter en un diccionario
					self._objetos_escenario[item['name']] = objetoescena(item)
				#for element in item['objects']:

		# crear array _mapaImagenes con subsurfaces del tileset.
		for item in data["tilesets"]:
			self.tilesets(item)

		# crear array _mapatiles con las subsurfaces del mapa
		self.crear_mapa()

		return


	def layers(self, layer):

		self._MapaW = layer["width"]
		self._MapaH = layer["height"]
		mapa = layer['data']

		# resto 1 a cada referencia de data porque desde el JSON viene con
		# 1 de más y me dibuja el tile siguiente... (??)
		c = 0
		for element in mapa:
			mapa[c] = element-1
			c += 1

		# convertir vector en matriz
		layerTemp = []
		for i in range(0, len(mapa), self._MapaW):
			layerTemp.append(mapa[i:i + self._MapaW])

		return layerTemp


	def tilesets(self, tileset):

		self._tileW = tileset['tilewidth']
		self._tileH = tileset['tileheight']

		imgTemp = tileset['name']

		self._transparentcolor = tileset['transparentcolor']

		img = pygame.image.load('imagenes/' + imgTemp + '.png')
		img = img.convert()

		# convierte valor alpha (#ffffff) a decimal (255,255,255)
		if self._transparentcolor != 1:
			alpha = self._transparentcolor
			alpha = alpha.lstrip('#')
			lv = len(alpha)
			alpha = tuple(int(alpha[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

		# Cortar tileset (array unidimensional) usando función tiles.utils
		path = tileset['image']
		self._mapaImagenes = tiles.cortar_tileset(path, self._tileW, self._tileH)

		return


	def crear_mapa(self):
		'''	Hay que crear la cámara( parte visible del mapa)
		y dibujar la parte correspondiente. '''

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

		return


	def dibujar_mapa(self, destino, coordenadas=[0,0]):
		''' dibuja el mapa (se invoca el objeto tras instanciarlo desde aquí)'''
		#self.CargarMapa(nivel, destino, coordenadas)
		x=coordenadas[0]
		y=coordenadas[1]
		for layer in self._mapatiles:
			for fila in layer:
				for tile in fila:
					destino.blit(tile, (x,y))
					x += self._tileW
				y += self._tileH
				x = coordenadas[0]
			x = coordenadas[0]
			y = coordenadas[1]


	def nopisable(self, layer):
		''' configura listado de zonas no pisables '''
		for element in layer['objects']:
			x = element['x']
			y = element['y']
			width = element['width']
			height = element['height']
			self._nopisable.append(pygame.Rect(x, y, width, height))


	def espisable(self, personaje, avance):
		''' devuelve True si el terreno es pisable '''
		pos = personaje.rect.move(avance)
		print ('avance', pos) # control

		# comprobando colisiones:
		idx = pos.collidelist(self._nopisable)

		if  idx == -1: # si no las hay
			personaje.rect = pos
			return True
		else:
			print ('! colisión escenario', idx, self._nopisable[idx])
			#pos = personaje.rect
			return False


class objetoescena():
	''' Extrae los objetos de escena desde tiledmaps '''

	def __init__(self, obj):
		''' obj es un diccionario que aporta las siguientes
		características del objeto'''
		self._nombre = obj["name"]
		self._objectW = obj["width"]
		self._objectH = obj["height"]
		self._objecttype = obj["type"]
		self._visible = obj["visible"]
		self._objectpos = (obj["x"], obj["y"])
		#[] solucionar problema al sumar negativos
		self._objrect = pygame.Rect(
			self._objectpos[0], self._objectpos[1], (
				self._objectpos[0]+self._objectW), (self._objectpos[1]+self._objectH))


# pruebas:
if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((800, 600)) 
	mapa = Mapa()
	mapa.CargarMapa('mapa1')
	mapa.dibujar_mapa(screen)
	while True:
		pygame.display.update()

