from game import Game
from GUI import GUI

game = Game(total_num_agents=6, num_agents_per_game=3, num_rooms=3, 
			room_code_len=3, message_len=8)  #room number needs to be odd number

gui = GUI(game=game)
game.print_game_initialization()
gui.run()

# gui.update_data_on_ui()




