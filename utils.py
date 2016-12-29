import pygame
import os
import escenario, Juego, personaje

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


def actualizar_camara(screen, personaje, mapa):
	''' Cámara y desplazamiento del mapa con el personaje principal '''


	coordenadas = [0,0]
	posabsX = mapa._char_posabs[0]
	posabsY = mapa._char_posabs[1]
	posrelX = personaje.posX
	posrelY = personaje.posY
	mapasizeX = mapa._mapa_size[0]
	mapasizeY = mapa._mapa_size[1]
	camarasizeX = screen.get_width()
	camarasizeY = screen.get_height()

	# colocar posición inicial de personaje y coordenadas.
	if (posabsX > camarasizeX/2) or (posabsX < mapasizeX-camarasizeX/2) :
		posrelX = camarasizeX/2
		coordenadas[0] = (posabsX - camarasizeX/2)
	if (posabsY > camarasizeY/2) or (posabsY < mapasizeY-camarasizeY/2) :
		posrelY = camarasizeY/2
		coordenadas[1] = (posabsY - camarasizeY/2)

	if posabsX < camarasizeX/2:
		posrelX = posabsX
		coordenadas[0] = 0
	if posabsX > mapasizeX-camarasizeX/2:
		posrelX = camarasizeX - (mapasizeX - posabsX)
		coordenadas[0] = mapasizeX - camarasizeX
	if posabsY < camarasizeY/2:
		posrelY = posabsY
		coordenadas[1] = 0
	if posabsY > mapasizeY-camarasizeY/2:
		posrelY = camarasizeY - (mapasizeY - posabsY)
		coordenadas[1] = mapasizeY - camarasizeY

	mapa._coordenadas = (coordenadas[0], coordenadas[1], camarasizeX, camarasizeY )
	personaje.posX, personaje.posY = (posrelX, posrelY)

	mapa._charrect = pygame.Rect(
		mapa._char_posabs[0], mapa._char_posabs[1], personaje.rect.w, personaje.rect.h) 

def espisable(personaje, avance, mapa):
	''' devuelve True si el terreno es pisable '''
	#[.] poner limites del mapa o rectángulo de límite.
			
	pos = mapa._charrect.move(avance)
	print ('avance pos', pos) # control


	# si hay colisión
	idx = pos.collidelist(mapa._nopisable)

	if idx == -1:
		print ('avanzando')
		return True

	else: # Si hay colisión no se mueve
		print ('! colisión escenario', idx, mapa._nopisable[idx])
		return False
