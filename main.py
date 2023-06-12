import pygame, sys


from unit import Unit, UnitController, UnitDrawer
from world import World, WorldController, WorldEventHandler, WorldDrawer


BG_COL = (47,79,79)


def main():
	pygame.init()
	size = width, height = 240, 240
	d_surf = pygame.display.set_mode(size)
	clock = pygame.time.Clock()

	unit_display_char_font = pygame.font.Font("text/Blockletter.otf", 24)
	unit_drawer = UnitDrawer(unit_display_char_font)
	unit_controller = UnitController()
	world_controller = WorldController(unit_controller)
	world_event_handler = WorldEventHandler(world_controller)
	world_drawer = WorldDrawer(unit_drawer)

	unit_1 = Unit(attack=2, defense=1, health=2, display_char='R')
	unit_2 = Unit(attack=1, defense=0, health=1, display_char = 'S')
	world = World(dims=(5, 5), pad=20, tile_size=40, contents={(2, 3): unit_1, (2, 1): unit_2})

	while True:
		delta_ms = clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			else:
				world = world_event_handler.handle(world, event)
		
		d_surf.fill(BG_COL)
		world_drawer.draw(d_surf, world)
		pygame.display.update()
	
if __name__ == '__main__':
	main()