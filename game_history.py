class GameHistory:
	
	def __init__(self, max_length):
		self.queue = [] 	# stores Game objects
		self.max_length = max_length
		self.current_turn = 0
		self.selected_index = 0
	
	def enqueue_game(self, current_game):
		# games in the queue need to have 0 length game_history to avoid memory overflow
		if len(self.queue) > 0:
			self.queue[-1].game_history = None

		self.queue.append(current_game)

		# dequeue game if history length exceeds max length
		if len(self.queue) > self.max_length:
			first_game = self.dequeue_game()
			del first_game

		self.current_turn+=1
		print(str(self.queue))

	def dequeue_game(self):
		first_game = self.queue[0]
		if len(self.queue) > 1:
			self.queue = self.queue[1:]
		return first_game
	
	def add_to_selected_index(self, num):
		self.selected_index += num

	def get_selected_turn(self):
		return self.current_turn + 1 + self.selected_index