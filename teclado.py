import pygame
import sys
import personaje
import Juego
import escenario


# [.] cambiar cris por self de objeto.
# [.] incorporar movimiento diagonal
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
		if pantalla.espisable(personaje, (0, -1)) == True:
			personaje.posY -= 1
		personaje.mover('camina_N')
	if teclado[pygame.K_DOWN]:
	    if pantalla.espisable(personaje, (0, 1)) == True:
	    	personaje.posY += 1
	    personaje.mover('camina_S')
	if teclado[pygame.K_RIGHT]:
		if pantalla.espisable(personaje, (1, 0)) == True:
			personaje.posX += 1
		personaje.mover('camina_E')
	if teclado[pygame.K_LEFT]:
		if pantalla.espisable(personaje, (-1, 0)) == True:
			personaje.posX -= 1
		personaje.mover('camina_O')

	# pixeles del mouse

	return