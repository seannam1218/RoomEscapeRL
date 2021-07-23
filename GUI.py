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

class GUI(App):
	def __init__(self, game, **kwargs):
		super(GUI, self).__init__(**kwargs)
		self.game = game
		self.selected_agent = None
		self.blank_image = 'images/blank.png'


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

		# button for proceeding
		self.button_proceed = Button(
					text= "Next",
					size_hint= (1,0.2),
					bold= True,
					background_color ='#FF6600',
					background_normal = ""
					)
		self.left_window.add_widget(self.button_proceed)
		self.button_proceed.bind(on_press=self.proceed)

		# memory display
		self.create_debug_display()
		self.left_window.add_widget(self.debug_panel)

		### create a space to represent rooms and its occupants
		self.create_game_window()
		self.left_window.add_widget(self.game_window)

		# add agents to the rooms
		self.agents_grid = GridLayout(rows=self.game.num_rooms+1)
		self.game_window.add_widget(self.agents_grid)


	def proceed(self, instance):
		print("proceeding................")
		self.game.proceed_turn()
		self.update_data_on_ui()


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
		for i in range(self.game.num_rooms+1):
			button = Button(
							text= "ROOM" + str(i),
							size_hint= (0.2,0.5),
							bold= True,
							pos = (self.left_window.width/2, 100 - i*self.left_window.height/self.game.num_rooms),
							background_color ='#00FFCE',
							)
			# TODO: player mode needs to have a callback function for clicking on room buttons
			self.room_grid.add_widget(button)
		self.game_window.add_widget(self.room_grid)
	

	def update_data_on_ui(self):
		self.agents_grid.clear_widgets()
		for r in self.game.rooms:
			stack = StackLayout()
			for o in r.occupants:
				print(o)
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
		for i in range(len(self.game.rooms)):
			for j in range(len(self.game.rooms[i].occupants)):
				if self.game.rooms[i].occupants[j].on_gui_selected == True:
					i_selected = i
					j_selected = j


	def update_right_window(self):
		# right window contains each agent's conversation history
		self.right_window.clear_widgets()
		for a in self.game.game_agents:
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
				image = Image(source=self.game.game_agents[order].image, size_hint_x = s_x)
				if self.game.game_agents[order].is_speaking and self.game.game_agents[order].location == a.location: #	and self.game.game_agents[order].is_moving == False and a.is_moving == False:
					color = '#e32636'
				else:
					color = '#E4DCD2'
				message = Label(text=str(a.message_memory_decoded[i]),
							font_size= 18,
							color= color,
							size_hint_x = 0.07
							)
				stack.add_widget(image)
				stack.add_widget(message)
			self.right_window.add_widget(stack)