import random


class Agent:
	
	def __init__(self, name, location, message_len, code_len):
		self.name = name
		self.location = location
		self.message = [0] * message_len
		self.room_code = [0] * code_len
	
	def identify(self):
		print(self.name, ": in room", self.location, ", message ", self.message)

	def set_room_code(self, room_code):
		self.room_code = room_code

	def get_action(self, num_rooms):
		action = {}
		action.update({"message" : random.randint(0, len(self.message))})
		action.update({"send_message" : False})
		action.update({"choose_room" : random.randint(0, num_rooms)})
		action.update({"escape" : False})
		return action


	def apply_action(self, action):
		if action["send_message"] is True:
			self.message = action["message"]
		self.location = action["choose_room"]


	def compose_nn_input(self):
		return