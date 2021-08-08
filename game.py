from room import Room
from agent import Agent
import random
import copy

class Game():
	def __init__(self, total_num_agents, num_agents_per_game, num_rooms, room_code_len, message_len):
		self.total_num_agents = total_num_agents
		self.num_agents_per_game = num_agents_per_game
		self.num_rooms = num_rooms
		self.room_code_len = room_code_len
		self.message_len = message_len
		self.all_agents = self.initialize_agents()
		shuffled = copy.deepcopy(self.all_agents)
		random.shuffle(shuffled)
		self.game_agents = shuffled[0:self.num_agents_per_game]
		self.rooms = self.initialize_rooms()
		self.rooms_update_occupants()


	def start_game(self):
		# this function must be called from main.py because the resulting Game object must be passed as an argument for the GameHistory class.
		shuffled = copy.deepcopy(self.all_agents)
		random.shuffle(shuffled)
		self.game_agents = shuffled[0:self.num_agents_per_game]
		self.rooms = self.initialize_rooms()
		self.rooms_update_occupants()
		
		# reset order in game
		for a in self.all_agents:
			a.set_order_in_game(None)
		for i in range(len(self.game_agents)):
			self.game_agents[i].set_order_in_game(i)

		# for each agent, reset order in memory
		for a in self.game_agents:
			a.reset_memory_order()

		# lock up each agent in each room
		for i in range(len(self.game_agents)):
			self.game_agents[i].location = i
		self.initialize_game()

		self.print_game_initialization()


	def initialize_agents(self):
		# define agents
		agents = []
		for i in range(self.total_num_agents):
			agent = Agent(number=i, name="robot", message_len=self.message_len, 
						location=0, code_len=self.room_code_len, num_agents=self.num_agents_per_game)
			agents.append(agent)
		return agents


	def initialize_rooms(self):
		rooms = []
		shuffled_room_list = list(range(0, self.num_rooms))
		random.shuffle(shuffled_room_list)

		for i in range(0, self.num_rooms):
			# generate room number
			room_number = i
			room_binary = [0]*(self.num_rooms)
			room_binary[i] += 1
			
			# generate room code
			rand_room = [0] * self.num_rooms
			rand_room[shuffled_room_list[i]] = 1
			rand_num = [0] * self.room_code_len
			rand_num[random.randint(0, self.room_code_len-1)] = 1
			code = (rand_room, rand_num)

			room = Room(room_number, room_binary, code)
			rooms.append(room)

		return rooms


	def initialize_game(self):
		self.agents_observe_room_codes()
		self.rooms_update_occupants()


	def agents_observe_room_codes(self):
		for agent in self.game_agents:
			agent.set_room_code(self.rooms[agent.location].code)


	def rooms_update_occupants(self): #not optimal
		for r in self.rooms:
			occupants = []
			for a in self.game_agents:
				if a.location == r.number:
					occupants.append(a)
			r.occupants = occupants
			

	def proceed_turn(self):
		for a in self.game_agents:
			action = a.get_action(self.num_rooms)
			a.apply_action(action)
		
		self.agents_send_messages(action)
		self.agents_observe_room_codes()
		self.rooms_update_occupants()


	def agents_send_messages(self, action):
		#identify occupants and send messages to them
		for a in self.game_agents:
			action = a.get_action(self.num_rooms)
			if action["send_message"] is True:
				for o in self.game_agents:
					o.receive_message(a, a.message)


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
