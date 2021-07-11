from room import Room
from agent import Agent
import random

class Game():
	def __init__(self, num_agents, num_rooms, room_code_len, message_len):
		self.num_agents = num_agents
		self.num_rooms = num_rooms
		self.room_code_len = room_code_len
		self.message_len = message_len
		self.agents = self.initialize_agents()
		self.rooms = self.initialize_rooms()
		self.rooms_update_occupants()


	def initialize_agents(self):
		# define agents
		alice = Agent(number=0, name="alice", message_len=self.message_len, location=0, code_len=self.room_code_len, num_agents=self.num_agents)
		bob = Agent(number=1, name="bob", message_len=self.message_len, location=0, code_len=self.room_code_len, num_agents=self.num_agents)
		charlie = Agent(number=2, name="charlie", message_len=self.message_len, location=0, code_len=self.room_code_len, num_agents=self.num_agents)
		return [alice, bob, charlie]


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
		exclude_list = [[0,0,0]]
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
		for agent in self.agents:
			agent.set_room_code(self.rooms[agent.location].code)


	def rooms_update_occupants(self): #not optimal
		for r in self.rooms:
			occupants = []
			for a in self.agents:
				if a.location == r.number:
					occupants.append(a)
			r.occupants = occupants
			
	
	def proceed_turn(self):
		for a in self.agents:
			action = a.get_action(self.num_rooms)
			a.apply_action(action)
			#identify occupants and send messages to them
			if action["send_message"] is True:
				for o in self.rooms[a.location].occupants:
					o.receive_message(a, a.message)
		self.agents_observe_room_codes()
		self.rooms_update_occupants()


	def get_agent_actions(self):
		for a in self.agents:
			a.get_action


	def get_rooms_data(self):
		return self.rooms


	def print_game_initialization(self):
		print("========Game is starting with following variables:========")
		print("--PLAYERS:")
		for agent in self.agents:
			agent.identify()
		print("--ROOMS:")
		for room in self.rooms:
			room.identify()
		print("enjoy!")


	def print_rooms(self):
		for i in range(len(self.rooms)):
			print(str(i), ":", self.rooms[i].occupants)

	
	def print_agents(self):
		for a in self.agents:
			print(a.name, "in room", a.location, " with message", a.message)
