import pygame
import sys
import personaje
import Juego


# [.] cambiar cris por self de objeto.
# [.] incorporar movimiento diagonal
def teclado(Cris):
	#event = pygame.event.wait()

	teclado = pygame.key.get_pressed()

	# Cerrar la ventana
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()


	if teclado[pygame.K_UP]:
		Cris.columna -= 1
		Cris.update(nuevaaccion='camina_N')
	if teclado[pygame.K_DOWN]:
	    Cris.columna += 1
	    Cris.update(nuevaaccion='camina_S')
	if teclado[pygame.K_RIGHT]:
		Cris.fila += 1
		Cris.update(nuevaaccion='camina_E')
	if teclado[pygame.K_LEFT]:
		Cris.fila -= 1
		Cris.update(nuevaaccion='camina_O')

	return