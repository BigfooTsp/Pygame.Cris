import pygame
from pygame.locals import *

from gamemanager.gamemanager import GameManager
from gamemanager.states import CollaoState, menustate, pausastate

# Activar o descativar modo test.
test_mode = True

if __name__ == '__main__':

	#[-] añadir modotest como parámetro pero seguir gestionándolo desde allí.
	game = GameManager(test_mode) #modo test como parámetro

	# Pantallas iniciales:
	game._pausa = pausastate.PausaState(game)
	game._intro = menustate.MenuState(game)
	# CollaoState = CollaoState.CollaoState(game)

	# Envía pantalla al gamemanager
	game.changeState(game._intro)

	# Inicio de bucle de juego.
	while game.running:
		game.handleEvents(pygame.event.get())
		game.update()
		game.draw()

	game.cleanUp()

