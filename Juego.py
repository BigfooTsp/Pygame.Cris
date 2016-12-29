import pygame
from pygame.locals import * # prescindible??
import teclado, personaje, escenario, utils
'''
Tareas:
	[.] Poner música.
  -	[x] Actualizar en display solo el cuadrado cambiante.
  -	[X] adaptar pantalla al tamaño del mapa.


	[X] Interacción con objetos.
	[.] incorporar juego mindmaster.
	[.] utilizar codificación y compresión
	[.] si el personaje está quieto se pone a bailar con música.

'''


class Game:

	screenW = 800
	screenH = 600
	screen_center = (screenW/2, screenH/2)


	def initialize(self):
		global screen, clock

		pygame.init()
		screen = pygame.display.set_mode((self.screenW, self.screenH))
		pygame.display.set_caption("Cris en El Collao")
		clock = pygame.time.Clock()


	def load_content(self):
		global Cris, pantalla

		# cargando pantalla:
		pantalla = escenario.Mapa('mapadesierto', screen)
		# cargando personajes.
		Cris = personaje.Personaje('Cris')


	def updates(self):

		utils.actualizar_camara(screen, Cris, pantalla)
		teclado.teclado(Cris, pantalla)


	def draw(self):

		# dibujar pantalla y personajes
		pantalla.dibujar_mapa(screen)
		Cris.dibujar_personaje(screen)

		# control, se dibujan los cuadros del personaje

		# actualizar pantalla
		pygame.display.update()


def main():
	game = Game()
	game.initialize()
	game.load_content()

	while True:
		time = clock.tick(80)
		game.updates()
		game.draw()

	return




if __name__ == '__main__':

	main()