import unittest
from unittest import mock

from unit import Unit, UnitDrawer
from world import World, WorldDrawer

class StaticGraphicsIntegrationTest(unittest.TestCase):
	def setUp(self):
		self.mock_d_surf = mock.Mock()
		self.mock_unit_display_char_font = mock.Mock()
		self.mock_display_char_dsurf = mock.Mock()
		self.mock_display_char_dsurf.get_width.return_value = 10
		self.mock_display_char_dsurf.get_height.return_value = 10
		self.mock_unit_display_char_font.render.return_value = self.mock_display_char_dsurf
		self.unit_drawer = UnitDrawer(self.mock_unit_display_char_font)
		self.world_drawer = WorldDrawer(self.unit_drawer)

	@mock.patch('pygame.draw.rect')
	def testDrawWorld(self, mock_draw_rect):
		self.unit = Unit(health=3, display_char='R')
		self.world = World(dims=(2, 2), tile_size=40, pad=10, contents={(0, 0): self.unit})

		self.world_drawer.draw(self.mock_d_surf, self.world)

		for pos_dims in [(10, 10, 40, 40), (50, 10, 40, 40), (10, 50, 40, 40), (50, 50, 40, 40)]:
			self.assertIn(mock.call(self.mock_d_surf, (200, 200, 200), pos_dims), mock_draw_rect.call_args_list)
			self.assertIn(mock.call(self.mock_d_surf, (50, 50, 50), pos_dims, 1), mock_draw_rect.call_args_list)
