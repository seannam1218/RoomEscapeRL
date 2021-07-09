from game import Game

game = Game(num_agents=3, num_rooms=3, 
			room_code_len=3, message_len=8)  #room number needs to be odd number

game.print_game_initialization()
print("\n===proceeding....")
game.proceed_turn()
print("\n===proceeding....")
game.proceed_turn()


