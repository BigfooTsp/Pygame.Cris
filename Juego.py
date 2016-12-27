import pygame
from pygame.locals import * # prescindible??
import teclado, personaje, escenario, utils
'''
Tareas:
	[.] Poner música.
  -	[x] Actualizar en display solo el cuadrado cambiante.
  -	[.] adaptar pantalla al tamaño del mapa.


	[.] Interacción con objetos.
	[.] incorporar juego mindmaster.
	[.] utilizar codificación y compresión
	[.] si el personaje está quieto se pone a bailar con música.

'''


class Game:

	rect_update=[] # Zonas de la pantalla a actualizar
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
		#pantalla._screenrect = pygame.Rect(pantalla)

		# cargando personajes.
		Cris = personaje.Personaje('Cris')
			# Su posición inicial.


	def updates(self):

		# Movimiento y colisiones de escenario.
		utils.actualizar_camara(screen, Cris, pantalla)
		teclado.teclado(Cris, pantalla)
		# desplazamiento del mapa


	def draw(self):
		# posiciones iniciales para pantalla y personajes.

		# dibujar pantalla y personajes
		pantalla.dibujar_mapa(screen)
		Cris.dibujar_personaje(screen)

		pygame.draw.rect(screen, (0,0,0), Cris.rect, 1)
		pygame.draw.rect(screen, (0,0,0) ,Cris.rectcolision, 1)

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