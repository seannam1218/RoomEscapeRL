import random


class Agent:
	
	def __init__(self, number, name, location, message_len, code_len, num_agents):
		self.number = number
		self.name = name
		self.location = location
		self.message = [0] * message_len
		self.room_code = [0] * code_len
		self.message_memory = []
		for i in range(num_agents): 
			self.message_memory.append([0] * message_len)
		self.message_memory_decoded = []
		self.decode_memory()
		self.image = "images/" + str(self.number) + ".png"
		self.on_gui_selected = False

		

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
		action.update({"choose_room" : random.randint(0, num_rooms)})
		action.update({"escape" : False})
		return action


	def apply_action(self, action):
		if action["send_message"] is True:
			self.message = action["message"]
			return
		self.location = action["choose_room"]


	def receive_message(self, sender, received_message):
		self.message_memory[sender.number] = received_message
		self.decode_memory()


	def compose_nn_input(self):
		return