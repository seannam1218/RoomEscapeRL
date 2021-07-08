class Agent:
	
	def __init__(self, name, location, total_words, code_len):
		self.name = name
		self.location = location
		self.message = [0] * total_words
		self.room_code = [0] * code_len
	
	def observe_room_code(self, room_code):
		self.room_code = room_code

	def identify(self):
		print(self.name)