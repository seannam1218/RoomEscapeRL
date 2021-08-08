from game import Game
from GUI import GUI
from game_history import GameHistory


game = Game(total_num_agents=6, num_agents_per_game=3, num_rooms=3, 
			room_code_len=5, message_len=8)
game.start_game()

game_history = GameHistory(game=game, max_length=5)

gui = GUI(game=game, game_history=game_history)

gui.run()




