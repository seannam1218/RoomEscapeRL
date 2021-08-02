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
SPEECH_COLOR = '#ff9966'
INACTIVITY_COLOR = '#E4DCD2'


class GUI(App):
	def __init__(self, game, game_history, **kwargs):
		super(GUI, self).__init__(**kwargs)
		self.game = game
		self.game_history = game_history
		self.selected_agent = None
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

		self.update_data_on_ui()
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
		self.button_next.bind(on_press=self.proceed)


	def new_game(self, instance):
		print("new game!")
		self.game.start_game()
		self.game_history.refresh_history(self.game)
		self.update_data_on_ui()

	
	def previous_turn(self, instance):
		print("previous turn...")
		self.game_history.add_to_selected_index(-1)
		self.update_data_on_ui()
		print(str(self.game_history.current_turn), str(self.game_history.selected_index))


	def proceed(self, instance):
		print("proceeding................")
		if self.game_history.selected_index == -1:
			self.game.proceed_turn()
			self.update_game_history()
		else:
			self.game_history.add_to_selected_index(1)
		self.update_data_on_ui()
		print(str(self.game_history.current_turn), str(self.game_history.selected_index))


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
		
		selected_game = self.game_history.queue[self.game_history.selected_index]
		for i in range(selected_game.num_rooms+1):
			button = Button(
							text= "ROOM" + str(i),
							size_hint= (0.2,0.5),
							bold= True,
							pos = (self.left_window.width/2, 100 - i*self.left_window.height/selected_game.num_rooms),
							background_color ='#00FFCE',
							)
			self.room_grid.add_widget(button)
		self.game_window.add_widget(self.room_grid)
	

	def update_game_history(self):
		self.game_history.enqueue_game(copy.deepcopy(self.game))


	def update_data_on_ui(self):
		self.agents_grid.clear_widgets()
		selected_game = self.game_history.queue[self.game_history.selected_index]
		for r in selected_game.rooms:
			stack = StackLayout()
			for o in r.occupants:
				agent_button = Button(
							background_normal=o.image,
							size_hint_x = 0.2	#TODO: needs to be square
							)
				agent_button_callback = partial(self.on_click_display_memory, o)  #allows passing argument into on_click_display_memory func
				agent_button.bind(on_press=agent_button_callback)
				stack.add_widget(agent_button)
			self.agents_grid.add_widget(stack)

		self.update_debug_panel(self.selected_agent)
		self.update_right_window()


	def on_click_display_memory(self, selected_agent, instance):
		self.selected_agent = selected_agent
		self.game.refresh_selected_agent(selected_agent)
		self.update_debug_panel(selected_agent)
		self.update_agent_buttons()
		self.update_right_window()


	def update_debug_panel(self, selected_agent):
		# update debug panel
		self.debug_panel.clear_widgets()
		if self.selected_agent == None:
			image = self.blank_image
		else:
			image = selected_agent.image
		self.selected_agent_display = Image(source=image)
		self.debug_panel.add_widget(self.selected_agent_display)

		if self.selected_agent == None:
			txt = ""
		else:
			txt = 'is_moving = ' + str(selected_agent.is_moving) + '\nprev = ' + str(selected_agent.prev_location) + '; now = ' + str(selected_agent.location) + '\nis_speaking = ' + str(selected_agent.is_speaking)

		self.debug_display = Label(
						text= txt,
						font_size= 18,
						color= '#00FFCE'
						)
		self.debug_panel.add_widget(self.debug_display)


	def update_agent_buttons(self):
		# TODO:refresh buttons
		i_selected = None
		j_selected = None
		selected_game = self.game_history.queue[self.game_history.selected_index]
		for i in range(len(selected_game.rooms)): 
			for j in range(len(selected_game.rooms[i].occupants)):
				if selected_game.rooms[i].occupants[j].on_gui_selected == True:
					i_selected = i
					j_selected = j


	def update_right_window(self):
		# right window contains each agent's conversation history
		self.right_window.clear_widgets()
		selected_game = self.game_history.queue[self.game_history.selected_index]
		for a in selected_game.game_agents:
			stack = StackLayout()
			if a.on_gui_selected:
				selection = Image(source='images/selection.png', size_hint_x=0.04)
				stack.add_widget(selection)
			for i in range(len(a.agents_order_in_memory)):
				if i == 0: 
					s_x = 0.15
				else:
					s_x = 0.07
				order = a.agents_order_in_memory[i]
				image = Image(source=selected_game.game_agents[order].image, size_hint_x = s_x)
				if selected_game.game_agents[order].is_speaking and selected_game.game_agents[order].location == a.location:
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