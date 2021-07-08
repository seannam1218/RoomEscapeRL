from room import Room
from agent import Agent
import random

class Game():
	def __init__(self, num_agents, num_rooms, room_code_len, total_words):
		self.num_agents = num_agents
		self.num_rooms = num_rooms
		self.room_code_len = room_code_len
		self.total_words = total_words
		self.agents = self.initialize_agents()
		self.rooms = self.initialize_rooms()
		self.update_rooms_occupants()


	def initialize_agents(self):
		# define agents
		alice = Agent(name="alice", total_words=self.total_words, location=0, code_len=self.room_code_len)
		bob = Agent("bob", total_words=self.total_words, location=0, code_len=self.room_code_len)
		charlie = Agent("charlie", total_words=self.total_words, location=0, code_len=self.room_code_len)
		return [alice, bob, charlie]


	def initialize_rooms(self):
		# create lobby
		lobby_location = [0] * (self.num_rooms + 1)
		lobby_code = [0] * self.room_code_len
		lobby = Room(0, lobby_location, lobby_code)
		rooms = [lobby]
		
		# create rooms
		code_list = self.initialize_code_list()
		for i in range(1, self.num_rooms+1):
			room_number = str(i)
			room_binary = [0]*(1+self.num_rooms)
			room_binary[i] += 1
			code = code_list[i-1]
			room = Room(room_number, room_binary, code)
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
		random.shuffle(code_list)
		return code_list


	def get_rand_code(self, exclude_list):
		rand_code = []
		for d in range(self.room_code_len):
			rand_code.append(random.randint(0, 1))
		if rand_code in exclude_list:
			return self.get_rand_code(exclude_list)
		return rand_code


	def initialize_game(self):
		self.agents_observe_room_codes()
		self.update_rooms_occupants()


	def agents_observe_room_codes(self):
		for agent in self.agents:
			agent.observe_room_code(self.rooms[agent.location].code)


	def update_rooms_occupants(self):
		for r in self.rooms:
			occupants = []
			for a in self.agents:
				if a.location == r.number:
					occupants.append(a)
			r.occupants = occupants
			

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

game = Game(num_agents=3, num_rooms=3, room_code_len=3, total_words=8)  #room number needs to be odd number
game.print_game_initialization()
game.print_rooms()

### initialize agent states, messages, locations, and room codes (all binary numbers)
# states: [escaped, present]
# messages: [0,0,0,0]
# locations: [lobby, A, B, C] - one value of one and everything else 0
# room code: [1,1,0,0] - the code of the current room



