import unittest
from unittest import mock
from world import World, WorldController, WorldEventHandler
from unit import Unit, UnitController


PYGAME_MOUSEMOTION = 1024
PYGAME_MOUSEBUTTONDOWN = 1025
PYGAME_MOUSEBUTTONUP = 1026


class TestMove(unittest.TestCase):
	def setUp(self):
		self.unit_controller = UnitController()
		self.world_controller = WorldController(self.unit_controller)
		self.world_event_handler = WorldEventHandler(self.world_controller)

	def testMoveUnit(self):
		unit = Unit()
		world = World(dims=(5, 5), pad=10, tile_size=20, contents={(0, 0): unit})

		world = self.world_event_handler.handle(world, mouse_down(20, 20))
		world = self.world_event_handler.handle(world, mouse_move(20, 40))
		world = self.world_event_handler.handle(world, mouse_up(20, 40))

		self.assertEqual([(0, 1)], list(world.contents.keys()))
	
	def testMoveUnitOffGrid(self):
		unit = Unit()

		world = World(dims=(5, 5), pad=10, tile_size=20, contents={(0, 0): unit})

		world = self.world_event_handler.handle(world, mouse_down(20, 20))
		world = self.world_event_handler.handle(world, mouse_move(20, -20))
		world = self.world_event_handler.handle(world, mouse_up(20, -20))

		self.assertEqual([(0, 0)], list(world.contents.keys()))

	def testMoveUnitOntoAnotherUnit(self):
		unit_1 = Unit(attack=2)
		unit_2 = Unit(defense=1, health=2)

		world = World(dims=(5, 5), pad=10, tile_size=20, contents={(0, 0): unit_1, (0, 1): unit_2})

		world = self.world_event_handler.handle(world, mouse_down(20, 20))
		world = self.world_event_handler.handle(world, mouse_move(20, 40))
		world = self.world_event_handler.handle(world, mouse_up(20, 40))

		self.assertEqual([(0, 0), (0, 1)], list(world.contents.keys()))
		self.assertEqual(1, world.contents.get((0, 1)).health)


def mouse_down(posx, posy):
	return mock.Mock(type=PYGAME_MOUSEBUTTONDOWN, button=1, pos=(posx, posy))


def mouse_move(posx, posy):
	return mock.Mock(type=PYGAME_MOUSEMOTION, button=1, pos=(posx, posy))


def mouse_up(posx, posy):
	return mock.Mock(type=PYGAME_MOUSEBUTTONUP, button=1, pos=(posx, posy))
