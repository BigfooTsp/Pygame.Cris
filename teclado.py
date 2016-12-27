import pygame
import sys
import personaje, escenario, Juego, utils


def teclado(personaje, pantalla):
	#event = pygame.event.wait()

	teclado = pygame.key.get_pressed()

	# Cerrar la ventana
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
	            # obtiene la posición del mouse
	            x, y = pygame.mouse.get_pos()
	            print ('mouse x-%i y-%i' %(x, y))


	if teclado[pygame.K_UP]:
		if utils.espisable(personaje=personaje, avance=(0, -1), mapa=pantalla) == True:
			personaje.posY -= 1
			pantalla._char_posabs[1] -= 1
		personaje.mover('camina_N')
	if teclado[pygame.K_DOWN]:
	    if utils.espisable(personaje=personaje, avance=(0, 1), mapa=pantalla) == True:
	    	personaje.posY += 1
	    	pantalla._char_posabs[1] += 1
	    personaje.mover('camina_S')
	if teclado[pygame.K_RIGHT]:
		if utils.espisable(personaje=personaje, avance=(1, 0), mapa=pantalla) == True:
			personaje.posX += 1
			pantalla._char_posabs[0] += 1
		personaje.mover('camina_E')
	if teclado[pygame.K_LEFT]:
		if utils.espisable(personaje=personaje, avance=(-1, 0), mapa=pantalla) == True:
			personaje.posX -= 1
			pantalla._char_posabs[0] -= 1
		personaje.mover('camina_O')

	return