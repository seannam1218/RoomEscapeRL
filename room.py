class Room:
	
	def __init__(self, number, binary, code):
		self.number = number
		self.binary = binary
		self.code = code
		self.occupants = []
	
	def identify(self):
		print("room", self.number, ";", self.binary, ";", self.code)