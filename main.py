from game import Game
from GUI import GUI

game = Game(num_agents=3, num_rooms=3, 
			room_code_len=3, message_len=8)  #room number needs to be odd number

gui = GUI(game=game)
gui.run()

game.print_game_initialization()
gui.update_data_on_ui(game.get_rooms_data())




