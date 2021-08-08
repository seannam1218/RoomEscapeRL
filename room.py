class Room:
	
	def __init__(self, number, binary, code):
		self.number = number
		self.binary = binary
		self.code = code
		self.occupants = []
	

	def set_code(self, code):
		self.code = code

	
	def get_decoded_code(self):
		room = self.code[0].index(1)
		button = self.code[1].index(1)
		return (room, button)


	def identify(self):
		decoded_code = self.get_decoded_code()
		print("room", self.number, ";", self.binary, ";", "room " + str(decoded_code[0]) + " has " + str(decoded_code[1]))