import pygame
import teclado
import personaje
from utils import tiles


class Game:

	screen = 0
	clock = 0
	personajes = []


	def initialize(self):
		pygame.init()
		Game.screen = pygame.display.set_mode((300, 400))

		Game.clock = pygame.time.Clock()


	def load_content(self):
		global Cris
		Game.fondo = tiles.cargar_imagen('imagenes/pruebafondo.png', transparent=False)

		Cris = personaje.Personaje()
		Game.personajes.append(Cris)


	def updates(self):
		teclado.teclado(Cris)


	def draw(self):
		Game.screen.blit(Game.fondo, [0,0])
		Cris.dibujar(Game.screen)
		pygame.display.update()



def main():
	game = Game()

	game.initialize()
	game.load_content()

	while True:
		time = game.clock.tick(40)
		game.updates()
		game.draw()

	return




if __name__ == '__main__':

	main()