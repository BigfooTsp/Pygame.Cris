import pygame
import os

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


def cortar_tileset(path, TILE_ANCHO, TILE_ALTO):
	''' crea array unidimensional con tileset del mapa'''

	image = cargar_imagen(path, TILE_ANCHO, TILE_ALTO)

	sprite = []
	for f in range(fil):
		for c in range(col):
			sprite.append(image.subsurface((rect.left, rect.top, TILE_ANCHO, TILE_ALTO)))
			rect.left += TILE_ANCHO
		rect.top += TILE_ALTO
		rect.left = 0

	return sprite


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


