import pygame
from pygame.locals import *

from gamemanager.gamemanager import GameManager
from gamemanager.states import CollaoState

if __name__ == '__main__':

	game = GameManager()
	game.changeState(CollaoState.CollaoState(game))
	clock = pygame.time.Clock()

	# Inicio de bucle de juego.
	while game.running:
		time = clock.tick(30)
		game.handleEvents(pygame.event.get())
		game.update()
		game.draw()

	game.cleanUp()