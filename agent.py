import random
from EpsilonGreedyStrategy import EpsilonGreedyStrategy
from ReplayMemory import ReplayMemory
from DQN import DQN
import torch.optim as optim
import torch


class Agent:
	
	def __init__(self, number, name, location, message_len, password_len, num_agents, batch_size, gamma, eps_start, eps_end, eps_decay, target_update, memory_size, lr, num_eps):
		
		# RL variables
		self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
		self.done = 0
		self.policy_net = DQN(message_len, password_len, num_agents).to(self.device)
		self.target_net = DQN(message_len, password_len, num_agents).to(self.device)
		self.target_net.load_state_dict(self.policy_net.state_dict())	# sets target net's weights and biases equal to policy net
		self.target_net.eval()	# target net not for training; only used for inference
		self.optimizer = optim.Adam(params = self.policy_net.parameters(), lr=lr)
		self.strategy = EpsilonGreedyStrategy(eps_start, eps_end, eps_decay)
		self.memory = ReplayMemory(memory_size)

		# game variables
		self.number = number
		self.order_in_game = None
		self.agents_order_in_memory = list(range(0, num_agents))
		self.name = name
		self.location = location
		self.current_step = 0
		self.num_actions = 0  	#TODO: automatically calculate num actions based on message len and password len
		self.message = [0] * message_len
		self.room_hint = None
		self.message_memory = []
		for i in range(num_agents): 
			self.message_memory.append([0] * message_len)
		self.message_memory_decoded = []
		self.decode_memory()
		self.is_speaking = False
		self.image = "images/" + str(self.number) + ".png"
		self.input_password = [0] * password_len
		self.room_unlocked = 0

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


	def set_room_unlocked(self, room_unlocked):
		self.room_unlocked = room_unlocked


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


	def compose_state_dict(self):
		# message_memory, room_hint, input_password, room_unlocked, 
		state = {"message_memory": self.message_memory, "room_hint": self.room_hint, "input_password": self.input_password, "room_unlocked": self.room_unlocked}
		return state

	
	def compose_state_list(self):
		state = self.message_memory + self.room_hint + self.input_password + self.room_unlocked
		return state


	def get_action_nn(self, state):
		rate = self.strategy.get_exploration_rate(self.current_step)
		self.current_step += 1

		if rate > random.random():
			action = random.randrange(self.num_actions) # explore
			return torch.tensor([action], device=self.device)  # supposed to be torch.tensor, but torch.as_tensor might work
		else:
			with torch.no_grad():
				return self.policy_net(state).argmax(dim=1).to(self.device) # exploit


	def take_action(self, action):
		#obs, reward, self.done, info
		reward = 0
		return torch.tensor([reward], device=self.device)  # supposed to be torch.tensor, but torch.as_tensor might work


	def receive_message(self, sender, received_message):
		self.message_memory[self.agents_order_in_memory[sender.order_in_game]] = received_message
		self.decode_memory()


	def set_order_in_game(self, order):
		self.order_in_game = order


	def reset_agent(self):
		# change memory order so that the agent of interest always appear in the front
		if self.order_in_game is not 0:
			self.agents_order_in_memory[0], self.agents_order_in_memory[self.order_in_game] = self.agents_order_in_memory[self.order_in_game], self.agents_order_in_memory[0]

		self.current_step = 0
