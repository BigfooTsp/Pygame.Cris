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
ToDo:
[-] Acabar state_base de la que heredarán el resto de states.
[.] Cambiar el tratamiento de los layers del mapa:
	[.] Convertir los tiles en objetos con prioridades y alturas
	[.] En el dibujado, incorporar los personajes según su altura 

[.] Comprobar los imports inutiles.
[.] Incorporar desplazamiento del personaje con clic del ratón o dirección. (pathfinder)
[.] acabar pantalla inicial
[.] Hacer pantalla de pausa (puede ser un push-state)
[.] Ideas de eventos en Collao State
	[.] evento u2
	[.] internado con Mastermind y Marta.
	[.] rebaño en el collao
	[.] tumba con susto
	[.] disparar corazones.
'''
