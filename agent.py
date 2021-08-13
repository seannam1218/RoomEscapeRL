import random


class Agent:
	
	def __init__(self, number, name, location, message_len, password_len, num_agents):
		self.number = number
		self.order_in_game = None
		self.agents_order_in_memory = list(range(0, num_agents))
		self.name = name
		self.location = location
		self.prev_location = location
		self.message = [0] * message_len
		self.room_hint = [0] * password_len
		self.message_memory = []
		for i in range(num_agents): 
			self.message_memory.append([0] * message_len)
		self.message_memory_decoded = []
		self.decode_memory()
		self.is_speaking = False
		self.image = "images/" + str(self.number) + ".png"
		self.input_password = None


		self.msg_index = 0 # TODO: this variable is for debugging. remove when debugging is complete.

		
	def decode_memory(self):
		self.message_memory_decoded = []
		for m in self.message_memory:
			try:
				self.message_memory_decoded.append(m.index(1))
			except:
				self.message_memory_decoded.append(0)


	def identify(self):
		print(self.name, ": in room", self.location, ", message ", self.message)


	def set_room_hint(self, room_hint):
		self.room_hint = room_hint


	def get_action(self):
		# TODO: get actions from running the neural network
		action = {"send_message": None, "message": None, "input_password": None}
		action.update({"send_message" : random.choice([True, False])})
		if action['send_message'] is True:
			self.is_speaking = True
			self.msg_index += 1
			self.msg_index = self.msg_index % 8
			message = [0]*len(self.message)
			message[self.msg_index] = 1
			action.update({"message" : message})
		else:
			self.is_speaking = False
			input_password = [0]*4 # TODO: this is for debugging. Change the 4 to something else. Same with randint line below
			input_password[random.randint(0,3)] = 1
			action.update({"input_password" : input_password})
		return action


	def apply_action(self, action):
		if action["send_message"] is True:
			self.message = action["message"]
		else:
			self.input_password = action["input_password"]


	def receive_message(self, sender, received_message):
			self.message_memory[self.agents_order_in_memory[sender.order_in_game]] = received_message
			self.decode_memory()


	def set_order_in_game(self, order):
		self.order_in_game = order


	def reset_memory_order(self):
		# change memory order so that the agent of interest always appear in the front
		if self.order_in_game is not 0:
			self.agents_order_in_memory[0], self.agents_order_in_memory[self.order_in_game] = self.agents_order_in_memory[self.order_in_game], self.agents_order_in_memory[0]
