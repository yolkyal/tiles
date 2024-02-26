import pygame

DEFAULT_TILE_OUTLINE_COL = (50, 50, 50)
DEFAULT_TILE_COL = (200, 200, 200)
DEFAULT_TILE_HIGHLIGHT_COL = (220, 220, 220)
DEFAULT_TILE_SUPER_HIGHLIGHT_COL = (240, 240, 240)


class WorldDragEvent:
	def __init__(self, source_tile_coords, target_tile_coords, mouse_pos):
		self.source_tile_coords = source_tile_coords
		self.target_tile_coords = target_tile_coords
		self.mouse_pos = mouse_pos


class World:
	def __init__(self, *, dims=(1, 1), pad=0, tile_size=1, contents={}):
		self.dims = dims
		self.pad = pad
		self.tile_size = tile_size
		self.contents = contents
		self.drag_event = None


class WorldController:
	def __init__(self, unit_controller):
		self.unit_controller = unit_controller

	def start_drag(self, world, mouse_pos):
		drag_tile_coords = self._get_mouse_pos_tile_coords(world, mouse_pos)
		world.drag_event = WorldDragEvent(drag_tile_coords, drag_tile_coords, mouse_pos)
		return world

	def update_drag(self, world, mouse_pos):
		drag_tile_coords = self._get_mouse_pos_tile_coords(world, mouse_pos)
		world.drag_event.target_tile_coords = drag_tile_coords
		world.drag_event.mouse_pos = mouse_pos
		return world

	def move_tile(self, world, mouse_pos):
		source_tile_index = world.drag_event.source_tile_coords
		source_unit = world.contents.get(source_tile_index)

		target_tile_index = world.drag_event.target_tile_coords
		if source_unit and target_tile_index:
			target_unit = world.contents.get(target_tile_index)
			if target_unit:
				world.contents[target_tile_index] = self.unit_controller.get_attack_resultant(source_unit, target_unit)
			else:
				world.contents[target_tile_index] = world.contents.pop(source_tile_index)

		world.drag_event = None

		return world

	def _get_mouse_pos_tile_coords(self, world, mouse_pos):
		tile_coords_x = (mouse_pos[0] - world.pad) // world.tile_size
		tile_coords_y = (mouse_pos[1] - world.pad) // world.tile_size
		
		if min(tile_coords_x, tile_coords_y) < 0 or max(tile_coords_x, tile_coords_y) >= world.dims[0]:
			return None
		else:
			return (tile_coords_x, tile_coords_y)


class WorldEventHandler:
	def __init__(self, world_controller):
		self.world_controller = world_controller

	def handle(self, world, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			world = self.world_controller.start_drag(world, event.pos)
		elif event.type == pygame.MOUSEMOTION:
			if world.drag_event:
				world = self.world_controller.update_drag(world, event.pos)
		elif event.type == pygame.MOUSEBUTTONUP:
			if world.drag_event:
				world = self.world_controller.move_tile(world, event.pos)

		return world


class WorldDrawer:
	def __init__(self, unit_drawer):
		self.unit_drawer = unit_drawer

	def draw(self, d_surf, world):
		for col in range(world.dims[0]):
			for row in range(world.dims[1]):
				self._draw_tile(d_surf, world, (col, row), DEFAULT_TILE_COL, DEFAULT_TILE_OUTLINE_COL)

		if world.drag_event:
			self._draw_tile(d_surf, world, world.drag_event.source_tile_coords, DEFAULT_TILE_HIGHLIGHT_COL, DEFAULT_TILE_OUTLINE_COL)
			if world.drag_event.target_tile_coords:
				self._draw_tile(d_surf, world, world.drag_event.target_tile_coords, DEFAULT_TILE_HIGHLIGHT_COL, DEFAULT_TILE_OUTLINE_COL)

			drag_tile_screen_pos = self._get_screen_pos_tile_with_centre_point(world, world.drag_event.mouse_pos)
			self._draw_tile(d_surf, world, world.drag_event.source_tile_coords, DEFAULT_TILE_SUPER_HIGHLIGHT_COL, DEFAULT_TILE_OUTLINE_COL, drag_tile_screen_pos)

	def _draw_tile(self, d_surf, world, tile_coords, fill_col, outline_col, tile_screen_pos=None):
		if not tile_screen_pos:
			tile_screen_pos = self._get_tile_coords_screen_pos(world, tile_coords)

		pygame.draw.rect(d_surf, fill_col, (tile_screen_pos[0], tile_screen_pos[1], world.tile_size, world.tile_size))
		pygame.draw.rect(d_surf, outline_col, (tile_screen_pos[0], tile_screen_pos[1], world.tile_size, world.tile_size), 1)

		if tile_coords in world.contents:
			self.unit_drawer.draw(d_surf, world.contents[tile_coords], self._corner_to_centre_screen_pos(world, tile_screen_pos))

	def _get_tile_coords_screen_pos(self, world, tile_coords):
		return (world.pad + (tile_coords[0] * world.tile_size), world.pad + (tile_coords[1] * world.tile_size))

	def _get_screen_pos_tile_with_centre_point(self, world, pos):
		return (pos[0] - world.tile_size // 2, pos[1] - world.tile_size // 2)

	def _corner_to_centre_screen_pos(self, world, pos):
		return (pos[0] + world.tile_size // 2, pos[1] + world.tile_size // 2)
