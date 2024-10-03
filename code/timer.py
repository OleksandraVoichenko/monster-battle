from settings import *

class Timer:
	def __init__(self, duration, repeat = False, autostart = False, func = None):
		self.duration = duration
		self.start_time = 0
		self.active = False
		self.repeat = repeat
		self.func = func
		
		if autostart:
			self.activate()


	def __bool__(self):
		"""Returns boolean value of timer being active."""

		return self.active


	def activate(self):
		"""Activates timer and starts the count of ticks."""

		self.active = True
		self.start_time = pygame.time.get_ticks()


	def deactivate(self):
		"""Deactivates timer and restarts it from 0.
		If repeat is active, timer is reactivated."""

		self.active = False
		self.start_time = 0
		if self.repeat:
			self.activate()


	def update(self):
		"""Updates timer based on provided duration, and calls on custom function."""

		if self.active:
			if pygame.time.get_ticks() - self.start_time >= self.duration:
				if self.func and self.start_time != 0: self.func()
				self.deactivate()