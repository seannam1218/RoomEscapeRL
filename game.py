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


	def start_game(self, num_agents_per_game):
		# this function must be called from main.py because the resulting Game object must be passed as an argument for the GameHistory class.
		self.num_agents_per_game = num_agents_per_game
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


	def initialize_agents(self):
		# define agents
		agents = []
		for i in range(self.total_num_agents):
			agent = Agent(number=i, name="robot", message_len=self.message_len, 
						location=0, code_len=self.room_code_len, num_agents=self.num_agents_per_game)
			agents.append(agent)
		return agents


	def initialize_rooms(self):
		# create lobby
		lobby_location = [0] * (self.num_rooms + 1)
		lobby_code = [0] * self.room_code_len
		lobby = Room(0, lobby_location, lobby_code)
		rooms = [lobby]
		
		# create rooms
		code_list, escape_code = self.initialize_code_list()
		for i in range(1, self.num_rooms+1):
			room_number = i
			room_binary = [0]*(1+self.num_rooms)
			room_binary[i] += 1
			code = code_list[i-1]
			room = Room(room_number, room_binary, code)
			if room.code == escape_code:
				room.set_escape_room(True)
			rooms.append(room)
		
		return rooms


	def initialize_code_list(self):
		# create code list
		code_list = []
		exclude_list = [[0]*self.room_code_len]
		for c in range(int((self.num_rooms+1)/2)):
			rand_code = self.get_rand_code(exclude_list)
			code_list.append(rand_code)
			code_list.append(rand_code)
			exclude_list.append(rand_code)
		code_list = code_list[0:-1]
		escape_code = code_list[-1]
		random.shuffle(code_list)
		return code_list, escape_code


	def get_rand_code(self, exclude_list):
		rand_code = []
		for d in range(self.room_code_len):
			rand_code.append(random.randint(0, 1))
		if rand_code in exclude_list:
			return self.get_rand_code(exclude_list)
		return rand_code


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
		
		self.agents_send_messages()
		self.agents_observe_room_codes()
		self.rooms_update_occupants()


	def agents_send_messages(self):
		#identify occupants and send messages to them
		for a in self.game_agents:
			action = a.get_action(self.num_rooms)
			if action["send_message"] is True:
				for o in self.rooms[a.location].occupants:
					# TODO: as agent is leaving the room, it hears what other agent in the same room says. 
					# This should be fixed so that agent can only hear if it stays in the room.
					o.receive_message(a, a.message)


	def get_agent_actions(self):
		for a in self.game_agents:
			a.get_action


	def refresh_selected_agent(self, selected_agent):
		for a in self.game_agents:
			a.on_gui_selected = False
		selected_agent.on_gui_selected = True


	def print_game_initialization(self):
		print("========Game is starting with following variables:========")
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
