import copy

class GameHistory:
	
	def __init__(self, game, max_length):
		self.queue = [copy.deepcopy(game)] 	# stores Game objects
		self.max_length = max_length
		self.current_turn = 1
		self.selected_index = -1
	

	def enqueue_game(self, current_game):
		if len(self.queue) > 0:
			self.queue[-1].game_history = None
		self.queue.append(current_game)

		# dequeue game if history length exceeds max length
		if len(self.queue) > self.max_length:
			first_game = self.dequeue_game()
			del first_game

		self.current_turn+=1


	def dequeue_game(self):
		first_game = self.queue[0]
		if len(self.queue) > 1:
			self.queue = self.queue[1:]
		return first_game


	def add_to_selected_index(self, num):
		self.selected_index += num
		# selected index cannot be lower than the negative current turn
		if self.selected_index < self.current_turn*-1:
			self.selected_index = self.current_turn*-1
		# selected index must be larger than the negative max length of queue
		if self.selected_index < self.max_length*-1:
			self.selected_index = -self.max_length
		# selected index must be smaller than -1
		if self.selected_index > -1:
			self.selected_index = -1
		return self.selected_index


	def get_selected_turn(self):
		#returns the absolute turn number of the currently selected game (selected from gui)
		return self.current_turn + 1 + self.selected_index


	def refresh_history(self, game):
		self.queue = [game] 	# stores Game objects
		self.current_turn = 0
		self.selected_index = 0
