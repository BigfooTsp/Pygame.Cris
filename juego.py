import pygame
from pygame.locals import *

from gamemanager.gamemanager import GameManager
from gamemanager.states import CollaoState, menustate

if __name__ == '__main__':

	game = GameManager()
	game.changeState(menustate.MenuState(game))
	clock = pygame.time.Clock()

	# Inicio de bucle de juego.
	while game.running:
		time = clock.tick(30)
		game.handleEvents(pygame.event.get())
		game.update()
		game.draw()

	game.cleanUp()


'''
ToDo:
[.] Incorporar música.
[.] Hacer pantalla inicial
[.] Hacer pantalla de pausa
[.] evento u2
[.] internado con Mastermind y Marta.
[.] rebaño en el collao
[.] tumba con susto
[.] disparar corazones.

'''