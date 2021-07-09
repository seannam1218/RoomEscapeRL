from game import Game

game = Game(num_agents=3, num_rooms=3, 
			room_code_len=3, message_len=8)  #room number needs to be odd number

game.print_game_initialization()
print("\n===proceeding....")
game.proceed_turn()
print("\n===proceeding....")
game.proceed_turn()
### initialize agent states, messages, locations, and room codes (all binary numbers)
# states: [escaped, present]
# messages: [0,0,0,0]
# locations: [lobby, A, B, C] - one value of one and everything else 0
# room code: [1,1,0,0] - the code of the current room


