from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from functools import partial ##import partial, wich allows to apply arguments to bind functions

class GUI(App):
	def __init__(self, game, **kwargs):
		super(GUI, self).__init__(**kwargs)
		self.game = game
		self.rooms_list = []
		self.selected_agent = None
		self.blank_image = 'images/blank.png'

	def build(self):
		#returns a window object with all it's widgets
		self.window = BoxLayout(orientation='vertical')
		self.window.cols = 1
		self.window.size_hint = (0.95, 0.95)
		self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

		# button for proceeding
		button_proceed = Button(
					text= "Next",
					size_hint= (1,0.5),
					bold= True,
					# pos = (self.window.width, 1),
					background_color ='#FF6600',
					#remove darker overlay of background colour
					background_normal = ""
					)
		self.window.add_widget(button_proceed)
		button_proceed.bind(on_press=self.proceed)

		# memory display
		self.memory_panel = BoxLayout(orientation='vertical')
		
		self.selected_agent_display = Image(source=self.blank_image)
		self.memory_panel.add_widget(self.selected_agent_display)

		self.memory_display = Label(
						text= "Memory",
						font_size= 18,
						color= '#00FFCE'
						)
		self.memory_panel.add_widget(self.memory_display)

		self.window.add_widget(self.memory_panel)


		### create a space to represent rooms and its occupants
		self.rooms_list_state = GridLayout(cols=2)
		self.window.add_widget(self.rooms_list_state)

		# button widget
		self.room_grid = GridLayout(cols=1)
		for i in range(self.game.num_rooms+1):
			button = Button(
							text= "ROOM" + str(i),
							size_hint= (0.2,0.5),
							bold= True,
							pos = (self.window.width/2, 100 - i*self.window.height/self.game.num_rooms),
							background_color ='#00FFCE',
							#remove darker overlay of background colour
							# background_normal = ""
							)
			# TODO: player mode needs to have a callback function for clicking on room buttons
			self.rooms_list.append(button)
			self.room_grid.add_widget(button)
		
		self.rooms_list_state.add_widget(self.room_grid)

		# self.agents_grid = GridLayout(cols=self.game.num_agents)
		self.agent_buttons_grid_list = []
		self.agents_grid = GridLayout(cols=self.game.num_agents)
		self.update_data_on_ui(self.game)

		self.rooms_list_state.add_widget(self.agents_grid)

		return self.window


	def proceed(self, instance):
		print("proceeding................")
		self.game.proceed_turn()
		#TODO: update memory panel
		self.update_data_on_ui(self.game.get_rooms_data())

	
	def update_data_on_ui(self, game):
		self.agents_grid.clear_widgets()
		self.agent_buttons_grid_list = []
		for i in range(self.game.num_rooms+1):
			agent_buttons_grid_list_row = []
			for j in range(self.game.num_agents):
				try:
					agent = self.game.rooms[i].occupants[j]
					agent_button = Button(
							background_normal=agent.image,
							size=(100,100)
							)
					agent_button_callback = partial(self.on_click_display_memory, agent)  #allows passing argument into on_click_display_memory func
					# agent_button_callback = lambda agent:print(agent)
					agent_button.bind(on_press=agent_button_callback)
					agent_buttons_grid_list_row.append(agent_button)

				except:
					blank_agent = Image(source=self.blank_image)
					agent_buttons_grid_list_row.append(blank_agent)

			self.agent_buttons_grid_list.append(agent_buttons_grid_list_row)

		for row in self.agent_buttons_grid_list:
			for item in row:
				self.agents_grid.add_widget(item)

		self.update_memory_panel(self.selected_agent)


	def on_click_display_memory(self, selected_agent, instance):
		self.selected_agent = selected_agent
		self.game.refresh_selected_agent(selected_agent)
		self.update_memory_panel(selected_agent)
		self.update_agent_buttons()


	def update_memory_panel(self, selected_agent):
		# update memory panel
		self.memory_panel.clear_widgets()
		if self.selected_agent == None:
			image = self.blank_image
		else:
			image = selected_agent.image
		self.selected_agent_display = Image(source=image)
		self.memory_panel.add_widget(self.selected_agent_display)

		if self.selected_agent == None:
			txt = "Memory"
		else:
			txt = str(selected_agent.message_memory_decoded)

		self.memory_display = Label(
						text= txt,
						font_size= 18,
						color= '#00FFCE'
						)
		self.memory_panel.add_widget(self.memory_display)


	def update_agent_buttons(self):
		# TODO:refresh buttons
		i_selected = None
		j_selected = None
		for i in range(len(self.game.rooms)):
			for j in range(len(self.game.rooms[i].occupants)):
				if self.game.rooms[i].occupants[j].on_gui_selected == True:
					i_selected = i
					j_selected = j
					self.agent_buttons_grid_list[i_selected][j_selected].background_color == '#7e300f'

