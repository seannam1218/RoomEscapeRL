class Room:
	
	def __init__(self, number, binary, code):
		self.number = number
		self.binary = binary
		self.code = code
		self.occupants = []
		self.escape_room = False
	

	def set_escape_room(self, boolean):
		self.escape_room = boolean


	def identify(self):
		print("room", self.number, ";", self.binary, ";", self.code, "; escape room?", self.escape_room)