from Room import Room
from Agent import Agent
import random
import copy

class Game():
	def __init__(self, total_num_agents, num_agents_per_game, num_rooms, password_len, message_len,
				batch_size, gamma, eps_start, eps_end, eps_decay, target_update, memory_size, lr, num_eps):
		self.total_num_agents = total_num_agents
		self.num_agents_per_game = num_agents_per_game
		self.num_rooms = num_rooms
		self.password_len = password_len
		self.message_len = message_len
		self.all_agents = self.initialize_agents(batch_size, gamma, eps_start, eps_end, eps_decay, target_update, memory_size, lr, num_eps)
		self.game_agents = self.all_agents[0:self.num_agents_per_game]
		self.rooms = self.initialize_rooms()
		self.rooms_update_occupants()
		self.is_over = 0



	def start_game(self):
		# this function must be called from main.py because the resulting Game object must be passed as an argument for the GameHistory class.
		self.is_over = 0
		random.shuffle(self.all_agents)
		self.game_agents = self.all_agents[0:self.num_agents_per_game]
		self.rooms = self.initialize_rooms()
		self.rooms_update_occupants()
		
		# reset order in game
		for a in self.all_agents:
			a.set_order_in_game(None)
		for i in range(len(self.game_agents)):
			a = self.game_agents[i]
			a.set_order_in_game(i)		# for each agent, reset order in memory and set current step to 0
			a.location = i				# lock up each agent in each room
			a.set_room_hint(self.rooms[a.location].hint)			
			a.reset_agent()

		self.initialize_game()
		self.print_game_initialization()


	def initialize_agents(self, batch_size, gamma, eps_start, eps_end, eps_decay, target_update, memory_size, lr, num_eps):
		# define agents
		agents = []
		for i in range(self.total_num_agents):
			agent = Agent(number=i, name="robot", message_len=self.message_len, location=0, 
						password_len=self.password_len, num_agents=self.num_agents_per_game,
						batch_size=batch_size, gamma=gamma, eps_start=eps_start, eps_end=eps_end, eps_decay=eps_decay, 
						target_update=target_update, memory_size=memory_size, lr=lr, num_eps=num_eps)
			agents.append(agent)
		random.shuffle(agents)
		return agents


	def initialize_rooms(self):
		rooms = []
		
		for i in range(0, self.num_rooms):
			# generate room number
			room_number = i
			room_binary = [0]*(self.num_rooms)
			room_binary[i] += 1
			
			# generate random password
			password = [0] * self.password_len
			password[random.randint(0, self.password_len-1)] = 1

			room = Room(room_number, room_binary, password)
			rooms.append(room)

		shuffled_room_list = list(range(0, self.num_rooms))
		random.shuffle(shuffled_room_list)

		for j in range(0, self.num_rooms):
			# generate room hint
			rand_room = [0] * self.num_rooms
			rand_room[shuffled_room_list[j]] = 1
			rand_room_index = rand_room.index(1)
			hint = [rand_room, rooms[rand_room_index].password]
			rooms[j].set_hint(hint)

		return rooms


	def initialize_game(self):
		self.agents_observe_room_hints()
		self.rooms_update_occupants()


	def agents_observe_room_hints(self):
		for a in self.game_agents:
			a.set_room_hint(self.rooms[a.location].hint)
			a.update_state()
			

	def rooms_update_occupants(self): #not optimal
		for r in self.rooms:
			occupants = []
			for a in self.game_agents:
				if a.location == r.number:
					occupants.append(a)
			r.occupants = occupants
			

	def proceed_turn(self):
		for a in self.game_agents:
			action = a.get_action_nn()
			a.take_action(action)

			# other agents receive message
			if a.action.tolist()[0] == 0: 	# speak
				for o in self.game_agents:
					o.receive_message(a, a.message)

		self.rooms_update_occupants()
		self.agents_observe_room_hints()


	def print_game_initialization(self):
		print("=" * 30)
		print("--PLAYERS:")
		for agent in self.game_agents:
			agent.identify()
		print("--ROOMS:")
		for room in self.rooms:
			room.identify()
		print("enjoy!")


	def print_rooms(self):
		for i in range(len(self.rooms)):
			print(str(i), ":", self.rooms[i].occupants)

	
	def print_agents(self):
		for a in self.game_agents:
			print(a.name, "in room", a.location, " with message", a.message)