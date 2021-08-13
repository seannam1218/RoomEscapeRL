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
from functools import partial ##import partial, wich allows to apply arguments to bind functions
import copy

NEW_GAME_BTN_COLOR = '#007fff'
OTHER_BTN_COLOR = '#FF6600'
LOCKED_COLOR = '#52349E'
UNLOCKED_COLOR = '#00FA9E'
SPEECH_COLOR = '#ff9966'
INACTIVITY_COLOR = '#E4DCD2'


class GUI(App):
	def __init__(self, game, game_history, **kwargs):
		super(GUI, self).__init__(**kwargs)
		self.game = game
		self.game_history = game_history
		self.selected_agent_num = None
		self.blank_image = 'images/blank.png'
		print(str(self.game_history.queue))
		print(str(self.game_history.current_turn), str(self.game_history.selected_index))


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
		self.create_debug_display()
		self.left_window.add_widget(self.debug_panel)

		### create a space to represent rooms and its occupants
		self.create_game_window()
		self.left_window.add_widget(self.game_window)

		# add agents to the rooms
		selected_game = self.game_history.queue[self.game_history.selected_index]
		self.agents_grid = GridLayout(rows=selected_game.num_rooms+1)
		self.game_window.add_widget(self.agents_grid)


	def create_button_space(self):
		self.button_space = GridLayout(cols=3, size_hint_y=0.2)

		# new game button
		self.button_new_game = Button(
					text= "New Game",
					bold= True,
					background_color = NEW_GAME_BTN_COLOR,
					background_normal = ""
					)
		self.button_space.add_widget(self.button_new_game)
		self.button_new_game.bind(on_press=self.new_game)

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

	
	def previous_turn(self, instance):
		print("previous turn...")
		self.game_history.add_to_selected_index(-1)
		self.update_ui()
		print(str(self.game_history.current_turn), str(self.game_history.selected_index))


	def next_turn(self, instance):
		print("proceeding................")
		if self.game_history.selected_index == -1:
			self.game.proceed_turn()
			self.update_game_history()
		else:
			self.game_history.add_to_selected_index(1)
		self.update_ui()


	def create_debug_display(self):
		self.debug_panel = BoxLayout(orientation='vertical')
		self.selected_agent_display = Image(source=self.blank_image)
		self.debug_panel.add_widget(self.selected_agent_display)
		self.debug_display = Label(
						text= "Memory",
						font_size= 18,
						color= '#00FFCE'
						)
		self.debug_panel.add_widget(self.debug_display)


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
		for r in selected_game.rooms:
			stack = StackLayout()
			for o in r.occupants:
				agent_button = Button(
							background_normal=o.image,
							size_hint_x = 0.2	#TODO: needs to be square
							)
				agent_button_callback = partial(self.on_click_display_memory, o.order_in_game)  #allows passing argument into on_click_display_memory func
				agent_button.bind(on_press=agent_button_callback)
				stack.add_widget(agent_button)
			self.agents_grid.add_widget(stack)


	def on_click_display_memory(self, num, instance):
		self.selected_agent_num = num
		# self.game.refresh_selected_agent(selected_agent)
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
							size_hint= (0.2,0.5),
							bold= True,
							pos = (self.left_window.width/2, 100 - i*self.left_window.height/selected_game.num_rooms),
							background_color = button_color,
							)
			self.room_grid.add_widget(button)


	def update_debug_panel(self):
		# update debug panel
		self.debug_panel.clear_widgets()
		selected_game = self.game_history.queue[self.game_history.selected_index]

		if self.selected_agent_num == None:
			image = self.blank_image
			txt = ""
		else:
			selected_agent = selected_game.game_agents[self.selected_agent_num]
			image = selected_agent.image
			txt = 'location = ' + str(selected_agent.location) + '\nis_speaking = ' + str(selected_agent.is_speaking) + '\nmessage = ' + str(selected_agent.message) + '\ninput_password = ' + str(selected_agent.input_password)

		self.selected_agent_display = Image(source=image)
		self.debug_panel.add_widget(self.selected_agent_display)
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