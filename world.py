import pygame

DEFAULT_TILE_OUTLINE_COL = (50, 50, 50)
DEFAULT_TILE_COL = (200, 200, 200)
DEFAULT_TILE_HIGHLIGHT_COL = (220, 220, 220)
DEFAULT_TILE_SUPER_HIGHLIGHT_COL = (240, 240, 240)


class World:
	def __init__(self, *, dims=(1, 1), pad=0, tile_size=1, contents={}):
		self.dims = dims
		self.pad = pad
		self.tile_size = tile_size
		self.contents = contents
		self.drag_source_tile_coords = None
		self.drag_target_tile_coords = None
		self.drag_mouse_pos = None


class WorldController:
	def __init__(self, unit_controller):
		self.unit_controller = unit_controller

	def set_drag_tile(self, world, mouse_pos):
		drag_tile_coords = self._get_mouse_pos_tile_coords(world, mouse_pos)
		world.drag_source_tile_coords = drag_tile_coords
		world.drag_target_tile_coords = drag_tile_coords
		world.drag_mouse_pos = mouse_pos
		return world

	def update_drag_tile(self, world, mouse_pos):
		drag_tile_coords = self._get_mouse_pos_tile_coords(world, mouse_pos)
		world.drag_target_tile_coords = drag_tile_coords
		world.drag_mouse_pos = mouse_pos
		return world

	def move_tile(self, world, mouse_pos):
		source_tile_index = world.drag_source_tile_coords
		source_unit = world.contents.get(source_tile_index)

		target_tile_index = world.drag_target_tile_coords
		target_unit = world.contents.get(target_tile_index)

		if source_unit:
			if target_unit:
				world.contents[target_tile_index] = self.unit_controller.get_attack_resultant(source_unit, target_unit)
			else:
				world.contents[target_tile_index] = world.contents.pop(source_tile_index)

		world.drag_source_tile_coords = None
		world.drag_target_tile_coords = None
		world.drag_mouse_pos = None

		return world

	def _get_mouse_pos_tile_coords(self, world, mouse_pos):
		tile_coords_x = (mouse_pos[0] - world.pad) // world.tile_size
		tile_coords_y = (mouse_pos[1] - world.pad) // world.tile_size
		return (tile_coords_x, tile_coords_y)


class WorldEventHandler:
	def __init__(self, world_controller):
		self.world_controller = world_controller

	def handle(self, world, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			world = self.world_controller.set_drag_tile(world, event.pos)
		elif event.type == pygame.MOUSEMOTION:
			if world.drag_mouse_pos:
				world = self.world_controller.update_drag_tile(world, event.pos)
		elif event.type == pygame.MOUSEBUTTONUP:
			if world.drag_mouse_pos:
				world = self.world_controller.move_tile(world, event.pos)

		return world


class WorldDrawer:
	def __init__(self, unit_drawer):
		self.unit_drawer = unit_drawer

	def draw(self, d_surf, world):
		for col in range(world.dims[0]):
			for row in range(world.dims[1]):
				x = world.pad + world.tile_size * col
				y = world.pad + world.tile_size * row
				pygame.draw.rect(d_surf, DEFAULT_TILE_COL, (x, y, world.tile_size, world.tile_size))
				pygame.draw.rect(d_surf, DEFAULT_TILE_OUTLINE_COL, (x, y, world.tile_size, world.tile_size), 1)

		if world.drag_mouse_pos:
			source_tile_screen_pos = self._get_tile_coords_screen_pos(world, world.drag_source_tile_coords)
			target_tile_screen_pos = self._get_tile_coords_screen_pos(world, world.drag_target_tile_coords)
			drag_tile_screen_pos = self._get_screen_pos_tile_with_centre_point(world, world.drag_mouse_pos)
			pygame.draw.rect(d_surf, DEFAULT_TILE_HIGHLIGHT_COL, (source_tile_screen_pos[0], source_tile_screen_pos[1], world.tile_size, world.tile_size))
			pygame.draw.rect(d_surf, DEFAULT_TILE_OUTLINE_COL, (source_tile_screen_pos[0], source_tile_screen_pos[1], world.tile_size, world.tile_size), 1)
			pygame.draw.rect(d_surf, DEFAULT_TILE_HIGHLIGHT_COL, (target_tile_screen_pos[0], target_tile_screen_pos[1], world.tile_size, world.tile_size))
			pygame.draw.rect(d_surf, DEFAULT_TILE_OUTLINE_COL, (target_tile_screen_pos[0], target_tile_screen_pos[1], world.tile_size, world.tile_size), 1)

			pygame.draw.rect(d_surf, DEFAULT_TILE_SUPER_HIGHLIGHT_COL, (drag_tile_screen_pos[0], drag_tile_screen_pos[1], world.tile_size, world.tile_size))
			pygame.draw.rect(d_surf, DEFAULT_TILE_OUTLINE_COL, (drag_tile_screen_pos[0], drag_tile_screen_pos[1], world.tile_size, world.tile_size), 1)
			if world.drag_source_tile_coords in world.contents:
				self.unit_drawer.draw(d_surf, world.contents[world.drag_source_tile_coords], self._corner_to_centre_screen_pos(world, drag_tile_screen_pos))

		for unit_key, unit in world.contents.items():
			if unit_key != world.drag_source_tile_coords:
				unit_screen_pos = self._get_tile_coords_screen_pos(world, unit_key)
				unit_screen_pos = self._corner_to_centre_screen_pos(world, unit_screen_pos)
				self.unit_drawer.draw(d_surf, unit, unit_screen_pos)

	def _get_tile_coords_screen_pos(self, world, tile_coords):
		screen_pos_x = world.pad + (tile_coords[0] * world.tile_size)
		screen_pos_y = world.pad + (tile_coords[1] * world.tile_size)
		return (screen_pos_x, screen_pos_y)

	def _get_screen_pos_tile_with_centre_point(self, world, pos):
		screen_pos_x = pos[0] - world.tile_size // 2
		screen_pos_y = pos[1] - world.tile_size // 2
		return (screen_pos_x, screen_pos_y)

	def _corner_to_centre_screen_pos(self, world, pos):
		return (pos[0] + world.tile_size // 2, pos[1] + world.tile_size // 2)
