from game import Game
from GUI import GUI
from game_history import GameHistory


game = Game(total_num_agents=6, num_agents_per_game=2, num_rooms=2, password_len=4, message_len=8,
			batch_size=256, gamma=0.999, eps_start=1, eps_end=0.01, eps_decay=0.001, target_update=10, memory_size=100000, lr=0.001, num_eps=1000)
game.start_game()

game_history = GameHistory(game=game, max_length=10)

gui = GUI(game=game, game_history=game_history)

gui.run()

# episode_durations = []
# for episode in range(100):
# 	for a in game.game_agents:
# 		# get initial state: message_memory, room_hint, input_password, room_unlocked, 
		

# 		for step in count():






