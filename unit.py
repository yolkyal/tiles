import pygame


DEFAULT_UNIT_TEXT_DISPLAY_COL = (50, 50, 50)


class Unit:
	def __init__(self, *, health=1, attack=1, defense=1, display_char='X'):
		self.health = health
		self.attack = attack
		self.defense = defense
		self.display_char = display_char


class UnitController:
	def get_attack_resultant(self, source, target):
		target_health = max(target.health - (source.attack - target.defense), 0)
		return Unit(health=target_health, attack=target.attack, defense=target.defense, display_char=target.display_char)


class UnitDrawer:
	def __init__(self, unit_display_char_font):
		self.unit_display_char_font = unit_display_char_font

	def draw(self, d_surf, unit, pos):
		display_char = unit.display_char if unit.health > 0 else '-'
		rendered_text = self.unit_display_char_font.render(display_char, False, DEFAULT_UNIT_TEXT_DISPLAY_COL)
		d_surf.blit(rendered_text, (pos[0] - rendered_text.get_width() // 2, pos[1] - rendered_text.get_height() // 2))
