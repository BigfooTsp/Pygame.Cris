import pygame
import teclado
import personaje
import escenario
from utils import tiles
'''
Tareas:
	[.] Poner música.
	[.] Actualizar en display solo el cuadrado cambiante.
	[.] Interacción con objetos.
	[.] incorporar juego mindmaster.
'''


class Game:

	screen = 0
	clock = 0
	personajes = []


	def initialize(self):
		pygame.init()
		Game.screen = pygame.display.set_mode((800, 600))
		Game.clock = pygame.time.Clock()


	def load_content(self):
		global Cris, pantalla
		pantalla = escenario.Mapa()
		pantalla.CargarMapa('mapa1')
		#[.] adaptar pantalla al tamaño del mapa.
		#Game.screen = pygame.display.set_mode((pantalla._MapaW, pantalla._MapaH))

		Cris = personaje.Personaje('Cris')
		Game.personajes.append(Cris)


	def updates(self):
		teclado.teclado(Cris, pantalla)


	def draw(self):
		pantalla.dibujar_mapa(Game.screen, coordenadas=[0,0])
		Cris.dibujar(Game.screen)
		pygame.display.update()



def main():
	game = Game()
	game.initialize()
	game.load_content()

	while True:
		time = game.clock.tick(80)
		game.updates()
		game.draw()

	return




if __name__ == '__main__':

	main()