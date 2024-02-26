import unittest
from unittest import mock

from unit import Unit, UnitController, UnitDrawer
from world import World, WorldController, WorldEventHandler, WorldDrawer


PYGAME_MOUSEMOTION = 1024
PYGAME_MOUSEBUTTONDOWN = 1025
PYGAME_MOUSEBUTTONUP = 1026


class DynamicGraphicsIntegrationTest(unittest.TestCase):
	def setUp(self):
		self.mock_d_surf = mock.Mock()
		self.unit_controller = UnitController()
		self.world_controller = WorldController(self.unit_controller)
		self.world_event_handler = WorldEventHandler(self.world_controller)
		self.mock_unit_display_char_font = mock.Mock()
		self.mock_display_char_dsurf = mock.Mock()
		self.mock_display_char_dsurf.get_width.return_value = 10
		self.mock_display_char_dsurf.get_height.return_value = 10
		self.mock_unit_display_char_font.render.return_value = self.mock_display_char_dsurf
		self.unit_drawer = UnitDrawer(self.mock_unit_display_char_font)
		self.world_drawer = WorldDrawer(self.unit_drawer)

	@mock.patch('pygame.draw.rect')
	def testDragUnitSameSquare(self, mock_draw_rect):
		self.mock_draw_rect = mock_draw_rect
		self.unit = Unit(display_char='R')
		self.world = World(dims=(2, 2), tile_size=40, pad=10, contents={(0, 0): self.unit})

		self.world = self.world_event_handler.handle(self.world, mouse_down(30, 30))
		self.world = self.world_event_handler.handle(self.world, mouse_move(35, 35))

		self.world_drawer.draw(self.mock_d_surf, self.world)
		self.assertDrewRect(dims=(40, 40), pos=(10, 10), col=(220, 220, 220)) # Highlight origin/destination square
		self.assertDrewRect(dims=(40, 40), pos=(15, 15), col=(240, 240, 240)) # Highlight dragged square more

		for pos in [(10, 10), (50, 10), (10, 50), (50, 50)]:
			self.assertDrewRect(pos=pos, dims=(40, 40), col=(200, 200, 200))

		self.assertDrewChar(pos=(30, 30), dims=(10, 10))
		self.assertDrewChar(pos=(35, 35), dims=(10, 10))

	@mock.patch('pygame.draw.rect')
	def testDragUnitDifferentSquare(self, mock_draw_rect):
		self.mock_draw_rect = mock_draw_rect
		self.unit = Unit(display_char='R')
		self.world = World(dims=(2, 2), tile_size=40, pad=10, contents={(0, 0): self.unit})

		self.world = self.world_event_handler.handle(self.world, mouse_down(30, 30))
		self.world = self.world_event_handler.handle(self.world, mouse_move(40, 60))

		self.world_drawer.draw(self.mock_d_surf, self.world)
		self.assertDrewRect(pos=(10, 10), dims=(40, 40), col=(220, 220, 220)) # Highlight origin square
		self.assertDrewRect(pos=(20, 40), dims=(40, 40), col=(240, 240, 240)) # Highlight dragged square more
		self.assertDrewRect(pos=(10, 50), dims=(40, 40), col=(220, 220, 220)) # Highlight destination square
		
		for pos in [(10, 10), (50, 10), (10, 50), (50, 50)]:
			self.assertDrewRect(pos=pos, dims=(40, 40), col=(200, 200, 200))

		self.assertDrewChar(pos=(30, 30), dims=(10, 10))
		self.assertDrewChar(pos=(40, 60), dims=(10, 10))

	def assertDrewRect(self, *, pos, dims, col):
		self.assertIn(mock.call(self.mock_d_surf, col, (pos[0], pos[1], dims[0], dims[1])), self.mock_draw_rect.call_args_list)
		self.assertIn(mock.call(self.mock_d_surf, (50, 50, 50), (pos[0], pos[1], dims[0], dims[1]), 1), self.mock_draw_rect.call_args_list)

	def assertDrewChar(self, *, pos, dims):
		self.assertIn(mock.call(self.mock_display_char_dsurf, (pos[0] - dims[0] // 2, pos[1] - dims[1] // 2)), self.mock_d_surf.blit.call_args_list)


def mouse_down(posx, posy):
	return mock.Mock(type=PYGAME_MOUSEBUTTONDOWN, button=1, pos=(posx, posy))


def mouse_move(posx, posy):
	return mock.Mock(type=PYGAME_MOUSEMOTION, button=1, pos=(posx, posy))


def mouse_up(posx, posy):
	return mock.Mock(type=PYGAME_MOUSEBUTTONUP, button=1, pos=(posx, posy))
