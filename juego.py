import pygame
from pygame.locals import *

from gamemanager.gamemanager import GameManager
from gamemanager.states import CollaoState, menustate

# Activar o descativar modo test.
test_mode = True

if __name__ == '__main__':

	#[-] añadir modotest como parámetro pero seguir gestionándolo desde allí.
	game = GameManager(test_mode) #modo test como parámetro
	game.changeState(CollaoState.CollaoState(game))


	# Inicio de bucle de juego.
	while game.running:

		game.handleEvents(pygame.event.get())
		game.update()
		game.draw()

	game.cleanUp()


'''
Actual:
[-] Moviendo instancia de scroll a State


[.] Configuración del test. (en Juego)
	[-] Añadir rectángulos de colisión
	[-] añadir modo de configuracion dibujar scroll 1 o 2

[.] Cambiar listas de personajes por diccionarios.

ToDo:
[.] Añadir sistema de prioridades al mapa para representar suelo y alturas
[.] Añadir numpy para gestion de matrices
[.] Test con Pandaself._list_tiles[tile-1]
[.] Incorporar desplazamiento del personaje con clic del ratón o dirección.
[.] acabar pantalla inicial
[.] Hacer pantalla de pausa
[.] evento u2
[.] internado con Mastermind y Marta.
[.] rebaño en el collao
[.] tumba con susto
[.] disparar corazones.
'''