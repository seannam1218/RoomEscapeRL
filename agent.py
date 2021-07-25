import random


class Agent:
	
	def __init__(self, number, name, location, message_len, code_len, num_agents):
		self.number = number
		self.order_in_game = None
		self.agents_order_in_memory = list(range(0, num_agents))
		self.name = name
		self.location = location
		self.prev_location = location
		self.message = [0] * message_len
		self.room_code = [0] * code_len
		self.message_memory = []
		for i in range(num_agents): 
			self.message_memory.append([0] * message_len)
		self.message_memory_decoded = []
		self.decode_memory()
		self.image = "images/" + str(self.number) + ".png"
		self.on_gui_selected = False
		self.is_speaking = False
		self.is_moving = False

		
	def decode_memory(self):
		self.message_memory_decoded = []
		for m in self.message_memory:
			try:
				self.message_memory_decoded.append(m.index(1))
			except:
				self.message_memory_decoded.append(0)


	def identify(self):
		print(self.name, ": in room", self.location, ", message ", self.message)


	def set_room_code(self, room_code):
		self.room_code = room_code


	def get_action(self, num_rooms):
		# TODO: get actions from running the neural network
		action = {}
		message = [0]*len(self.message)
		message[random.randint(0, len(self.message))-1] = 1
		action.update({"message" : message})
		action.update({"send_message" : random.choice([True, False])})
		if action['send_message'] is False:
			action.update({"choose_room" : random.randint(0, num_rooms)})
		else: 
			action.update({"choose_room" : self.location})
		action.update({"escape" : False})
		return action

	# TODO: probably better to break this function into two: one for updating state, one for applying action. GUI class is having trouble differentiating what gets updated when. 
	def update_states(self, action):
		return
		
	def apply_action(self, action):
		if action["send_message"] is True:
			self.is_speaking = True
			self.message = action["message"]
		else:
			self.is_speaking = False
		
		# update location and related states
		self.prev_location = self.location
		if self.prev_location != action["choose_room"]:
			self.is_moving = True
		else:
			self.is_moving = False

		self.location = action["choose_room"]


	def receive_message(self, sender, received_message):
		if self.is_moving == False:
			self.message_memory[self.agents_order_in_memory[sender.order_in_game]] = received_message
			self.decode_memory()


	def set_order_in_game(self, order):
		self.order_in_game = order


	def reset_memory_order(self):
		# change memory order so that the agent of interest always appear in the front
		if self.order_in_game is not 0:
			self.agents_order_in_memory[0], self.agents_order_in_memory[self.order_in_game] = self.agents_order_in_memory[self.order_in_game], self.agents_order_in_memory[0]


	def compose_nn_input(self):
		return