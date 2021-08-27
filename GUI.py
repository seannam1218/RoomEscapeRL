from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle
from Plotter import Plotter
from functools import partial ##import partial, wich allows to apply arguments to bind functions
import copy

NEW_GAME_BTN_COLOR = '#007fff'
TRAINING_BTN_COLOR = '#30f722'
OTHER_BTN_COLOR = '#FF6600'
LOCKED_COLOR = '#52349E'
UNLOCKED_COLOR = '#00FA9E'
SPEECH_COLOR = '#ff9966'
INACTIVITY_COLOR = '#E4DCD2'


class GUI(App):
	def __init__(self, game, game_history, max_turns, moving_avg_period, **kwargs):
		super(GUI, self).__init__(**kwargs)
		self.game = game
		self.game_history = game_history
		self.selected_agent_num = None
		self.blank_image = 'images/blank.png'
		self.max_turns = max_turns
		self.plotter = Plotter(moving_avg_period)


	def build(self):
		self.window = GridLayout(cols=2)
		# Window.clearcolor = (1,1,1,1)

		self.create_left_window()
		self.window.add_widget(self.left_window)

		self.right_window = BoxLayout(orientation='vertical')
		self.update_right_window()
		self.window.add_widget(self.right_window)

		self.update_ui()
		return self.window


	def create_left_window(self):
		# left window has buttons to control the game and visuals about rooms and occupants
		self.left_window = BoxLayout(orientation='vertical')
		self.left_window.cols = 1
		self.left_window.size_hint = (0.95, 0.95)
		self.left_window.pos_hint = {"center_x": 0.5, "center_y":0.5}

		# create button space
		self.create_button_space()
		self.left_window.add_widget(self.button_space)

		# memory display
		self.debug_panel = BoxLayout(orientation='vertical')
		self.left_window.add_widget(self.debug_panel)

		### create a space to represent rooms and its occupants
		self.create_game_window()
		self.left_window.add_widget(self.game_window)

		# add agents to the rooms
		selected_game = self.game_history.queue[self.game_history.selected_index]
		self.agents_grid = GridLayout(rows=selected_game.num_rooms+1)
		self.game_window.add_widget(self.agents_grid)


	def create_button_space(self):
		self.button_space = GridLayout(cols=4, size_hint_y=0.2)

		# new game button
		self.button_new_game = Button(
					text= "New Game",
					bold= True,
					background_color = NEW_GAME_BTN_COLOR,
					background_normal = ""
					)
		self.button_space.add_widget(self.button_new_game)
		self.button_new_game.bind(on_press=self.new_game)

		# training button
		self.button_train = Button(
					text= "Start Training",
					bold= True,
					background_color = TRAINING_BTN_COLOR,
					background_normal = ""
					)
		self.button_space.add_widget(self.button_train)
		self.button_train.bind(on_press=self.train)

		# previous button
		self.button_previous = Button(
					text= "Previous",
					bold= True,
					background_color = OTHER_BTN_COLOR,
					background_normal = ""
					)
		self.button_space.add_widget(self.button_previous)
		self.button_previous.bind(on_press=self.previous_turn)

		# button for proceeding
		self.button_next = Button(
					text= "Next",
					bold= True,
					background_color = OTHER_BTN_COLOR,
					background_normal = ""
					)
		self.button_space.add_widget(self.button_next)
		self.button_next.bind(on_press=self.next_turn)


	def new_game(self, instance):
		print("new game!")
		self.game.start_game()
		self.game_history.refresh_history(self.game)
		self.selected_agent_num = None
		self.update_ui()


	def train(self, instance):
		print("training")
		
		for episode in range(10):
			self.new_game(None)
			n = 0
			# loop through each turn
			selected_game = self.game_history.queue[self.game_history.selected_index]
			for turn in range(self.max_turns):
				if selected_game.is_over == 1:
					reward = 50			# TODO: calculate reward
					for a in self.game.game_agents:
						a.train_agent(reward)
					break
					# self.plotter.plot(n)
				else:
					for a in self.game.game_agents:
						self.next_turn(None)
						reward = 0 		# TODO: calculate reward
						a.train_agent(reward)
				n += 1
				
	
	def previous_turn(self, instance):
		print("previous turn...")
		self.game_history.add_to_selected_index(-1)
		self.update_ui()


	def next_turn(self, instance):
		selected_game = self.game_history.queue[self.game_history.selected_index]
		if selected_game.is_over == 1:
			print("game is over. start a new game!")
			return
		print("proceeding................")
		if self.game_history.selected_index == -1:
			self.game.proceed_turn()
			self.check_room_unlocks()
			self.update_game_history()
		else:
			self.game_history.add_to_selected_index(1)
		self.update_ui()


	def check_room_unlocks(self):
		# iterate through rooms and see if the occupants matched the password. 
		# Update agents on unlocked status of the rooms
		# Game is over if all rooms are unlocked
		total = 0
		for r in self.game.rooms:
			total += r.unlock(r.check_password_match())
			r.occupants[0].set_room_unlocked = r.check_password_match()
		if total == self.game.num_rooms:
			self.game_over()
			print("game over!")


	def game_over(self):
		self.game.is_over = 1
		for a in self.game.game_agents:
			a.done = 1


	def create_game_window(self):
		# create a space to represent rooms and its occupants
		self.game_window = GridLayout(cols=2)
		self.room_grid = GridLayout(cols=1)
		self.update_room_grid()
		self.game_window.add_widget(self.room_grid)
	

	def update_game_history(self):
		self.game_history.enqueue_game(copy.deepcopy(self.game))


	def update_ui(self):
		self.update_agents_grid()
		self.update_room_grid()
		self.update_debug_panel()
		self.update_right_window()


	def update_agents_grid(self):
		self.agents_grid.clear_widgets()
		selected_game = self.game_history.queue[self.game_history.selected_index]
		for i in range(len(selected_game.game_agents)):
			agent = selected_game.game_agents[i]
			stack = StackLayout()

			image = Image(source=agent.image, size_hint_x = 0.2)
			stack.add_widget(image)

			if agent.is_speaking:
				text = "says:\n" + str(agent.message)
				color = SPEECH_COLOR
			else:
				text = "inputs password:\n" + str(agent.input_password)
				color = UNLOCKED_COLOR
			label = Label(
					text= text,
					color= color,
					size_hint_x = 0.7
					)
			stack.add_widget(label)

			self.agents_grid.add_widget(stack)


	def on_click_display_memory(self, num, instance):
		self.selected_agent_num = num
		self.update_debug_panel()
		self.update_right_window()


	def update_room_grid(self):
		# create a space to represent rooms and its occupants
		self.room_grid.clear_widgets()
		selected_game = self.game_history.queue[self.game_history.selected_index]
		for i in range(selected_game.num_rooms):
			if selected_game.rooms[i].unlocked == True:
				button_color = UNLOCKED_COLOR
			else:
				button_color = LOCKED_COLOR
			button = Button(
						text= "ROOM " + str(i) + "\npassword: " + str(selected_game.rooms[i].get_decoded_password()) + "\nhint: " + str(selected_game.rooms[i].get_decoded_hint()),
						bold= True,
						background_color = button_color,
						)
			self.room_grid.add_widget(button)


	def update_debug_panel(self):
		# update debug panel
		self.debug_panel.clear_widgets()
		selected_game = self.game_history.queue[self.game_history.selected_index]
		txt = "current turn = " + str(self.game_history.current_turn) + "\nselected turn = " + str(self.game_history.get_selected_turn()) + "\ngameover = " + str(selected_game.is_over)
		self.debug_display = Label(
						text= txt,
						font_size= 18,
						color= '#00FFCE'
						)
		self.debug_panel.add_widget(self.debug_display)


	def update_right_window(self):
		# right window contains each agent's conversation history
		self.right_window.clear_widgets()
		selected_game = self.game_history.queue[self.game_history.selected_index]

		for j in range(len(selected_game.game_agents)):
			a = selected_game.game_agents[j]
			stack = StackLayout()

			# use an image to highlight the agent selection.
			if self.selected_agent_num == j:
				selection = Image(source='images/selection.png', size_hint_x=0.04)
				stack.add_widget(selection)

			for i in range(len(a.agents_order_in_memory)):
				# resize image - increase size if the image is of the agent itself.
				if i == 0: 
					s_x = 0.15
				else:
					s_x = 0.07
				order = a.agents_order_in_memory[i]
				image = Image(source=selected_game.game_agents[order].image, size_hint_x = s_x)

				# highlight speech color depending on whether agent is speaking or not
				if selected_game.game_agents[order].is_speaking:
					color = SPEECH_COLOR
				else:
					color = INACTIVITY_COLOR
				message = Label(text=str(a.message_memory_decoded[i]),
							font_size= 18,
							color= color,
							size_hint_x = 0.07
							)
				stack.add_widget(image)
				stack.add_widget(message)
			self.right_window.add_widget(stack)