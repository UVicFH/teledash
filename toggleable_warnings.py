import time

next_id = 0
def new_id():
	global next_id
	val = next_id
	next_id = next_id + 1
	return val

class Toggleable_warning(object):
	def __init__(self, text, code = None, initial_state = False):
		self.on = initial_state
		self.text = text # Full text of warning
		self.id_num = new_id()
		if code is None:
			self.code = "%03d" % self.id_num
		else:
			self.code = code # Brief code to display in gui. Should be <= 5 characters

		self.last_focused = time.time() # last time warning was switched to
		self.last_seen = 0 # last time warning was on screen

	def __bool__(self):
		return self.on
	__nonzero__ = __bool__

	def toggle(self):
		self.on = not self.on # flip self.on truth value

	def switch_on(self):
		self.on = True
	def switch_off(self):
		self.on = False

	def mark_seen(self):
		"""Mark this moment as the last time this warning was on screen."""
		self.last_seen = time.time()

	def mark_focused(self):
		"""Mark this moment as the last time this warning was switched to."""
		self.last_focused = time.time()
		self.mark_seen()
	

	def __str__(self):

		if self.on:
			initial = "Warning:"
		else:
			initial = "Inactive warning:"

		if self.code != self.text:
			extra = " (%s)" % self.text
		else:
			extra = ""

		return "%s %s%s." % (initial, self.code, extra)
	
	def __repr__(self):
		if self.on:
			initial = "W!:"
		else:
			initial = "iw:"
		return "%s%s" % (initial, self.code)
			
