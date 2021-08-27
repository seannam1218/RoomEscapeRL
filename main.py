from Game import Game
from GUI import GUI
from GameHistory import GameHistory


game = Game(total_num_agents=6, num_agents_per_game=2, num_rooms=2, password_len=4, message_len=3,
			batch_size=16, gamma=0.999, eps_start=1, eps_end=0.01, eps_decay=0.001, target_update=10, memory_size=1000, lr=0.001, num_eps=1000)
game.start_game()

game_history = GameHistory(game=game, max_length=10)

gui = GUI(game=game, game_history=game_history, max_turns=500, moving_avg_period=5)

gui.run()







