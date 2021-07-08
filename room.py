class Room:
	
	def __init__(self, number, binary, code):
		self.number = number
		self.binary = binary
		self.code = code
		self.occupants = []
	
	# def get_room_code(self):
	# 	return self.code


	def identify(self):
		print(self.number, self.binary, self.code)