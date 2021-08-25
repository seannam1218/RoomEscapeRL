import random

class Room:
	
	def __init__(self, number, binary, password):
		self.number = number
		self.binary = binary
		self.password = password
		self.occupants = []
		self.unlocked = False
	

	def set_hint(self, hint):
		self.hint = hint


	def unlock(self, boolean):
		self.unlocked = boolean
		if boolean:
			return 1
		else: 
			return 0


	def get_decoded_password(self):
		decoded_password = self.password.index(1)
		return decoded_password

	
	def get_decoded_hint(self):
		room = self.hint[0].index(1)
		button = self.hint[1].index(1)
		return (room, button)


	def check_password_match(self):
		return self.occupants[0].input_password == self.password


	def identify(self):
		decoded_code = self.get_decoded_hint()
		print("room", self.number, ";", self.binary, ";", "room " + str(decoded_code[0]) + " has " + str(decoded_code[1]))