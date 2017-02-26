import pygame
import os


	########################################################
	################# GESTIÓN DE IMÁGENES ##################
	########################################################

def cargar_imagen(path, TILE_ANCHO, TILE_ALTO, transparent=True, pixel = (0,0)):
	global rect, col, fil, image

	image = pygame.image.load(os.path.join(path))

	image = image.convert_alpha()

	if transparent:
		color = (image.get_at(pixel))
		image.set_colorkey(color, pygame.locals.RLEACCEL)

	rect = image.get_rect()
	col = int(rect.w / TILE_ANCHO)
	fil = int(rect.h / TILE_ALTO)


	return image


def cortar_charset(path, TILE_ANCHO, TILE_ALTO):
	''' crea array bidimensional con tileset del personaje'''

	image = cargar_imagen(path, TILE_ANCHO, TILE_ALTO)

	sprite = []
	for i in range(fil):
		sprite.append([])
	for f in range(fil):
		for c in range(col):
			sprite[f].append(image.subsurface((rect.left, rect.top, TILE_ANCHO, TILE_ALTO)))
			rect.left += TILE_ANCHO
		rect.top += TILE_ALTO
		rect.left = 0

	return sprite

	########################################################
	################# GESTIÓN DE TEXTO #####################
	########################################################

def texto(texto, posx, posy, tamaño, color=(255,255,255), fuente=0,):
	''' Control de impresión de texto, las fuentes en una lista
	http://razonartificial.com/2010/02/pygame-10-fuentes-tipograficas/'''
	if fuente:
		fuentes = ['Christmas.ttf']
		path = 'utilidades\imagenes\%s'%(fuentes[fuente])
		font = pygame.font.Font(path, tamaño)
	else:
		font = pygame.font.Font(None, tamaño)

	salida = pygame.font.Font.render(font, texto, 1, color) # 1 es antialias (True o False)
	salida_rect = salida.get_rect()
	salida_rect.centerx = posx
	salida_rect.centery = posy

	return salida, salida_rect

	########################################################
	################# GESTIÓN DE MATRICES ##################
	########################################################

# devuelve lista de tuplas con las posiciones de una matriz que tienen un valor dado
def buscar_en_matriz(matriz, valor):
	lista = []
	for f in range(len(matriz)):
		for c in range(len(matriz[0])):
			if self.matriz_elementos[f][c] == valor:
				lista.append (f,c)
	return lista

# cambia el valor de las posiciones de una matriz por uno dado.
def cambiar_valor_en_matriz(matriz, lista, valor):
	for tupla in lista:
		for f,c in tupla:
			matriz[f,c] = valor
	return matriz

