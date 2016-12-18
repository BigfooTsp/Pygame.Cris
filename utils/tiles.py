import pygame
import os

def cargar_imagen(path, transparent=True, pixel = (0,0)):

	image = pygame.image.load(os.path.join(path))
	# imagen = pygame.image.load(os.path.join('imagenes', 'logo_pygame.gif'))
	# image = pygame.image.load(filename)

	image = image.convert_alpha()

	if transparent:
		color = image.get_at(pixel)
		image.set_colorkey(color, pygame.locals.RLEACCEL)

	return image

def cortar_tileset(path, TILE_ANCHO, TILE_ALTO):

	image = cargar_imagen(path)
	rect = image.get_rect()
	col = int(rect.w / TILE_ANCHO)
	fil = int(rect.h / TILE_ALTO)

	# Creo array bidimensional con los tiles.
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