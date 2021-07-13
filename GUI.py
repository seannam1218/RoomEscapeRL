from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout

from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from functools import partial ##import partial, wich allows to apply arguments to bind functions

class GUI(App):
	def __init__(self, game, **kwargs):
		super(GUI, self).__init__(**kwargs)
		self.game = game
		self.selected_agent = None
		self.blank_image = 'images/blank.png'

	def build(self):
		#returns a window object with all it's widgets
		self.window = BoxLayout(orientation='vertical')
		self.window.cols = 1
		self.window.size_hint = (0.95, 0.95)
		self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

		# button for proceeding
		self.button_proceed = Button(
					text= "Next",
					size_hint= (1,0.5),
					bold= True,
					# pos = (self.window.width, 1),
					background_color ='#FF6600',
					#remove darker overlay of background colour
					background_normal = ""
					)
		self.window.add_widget(self.button_proceed)
		self.button_proceed.bind(on_press=self.proceed)

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
		self.game_window = GridLayout(cols=2)
		self.window.add_widget(self.game_window)

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
			self.room_grid.add_widget(button)
		
		self.game_window.add_widget(self.room_grid)

		# add agents to the rooms
		self.agents_grid = GridLayout(rows=self.game.num_rooms+1)
		self.update_data_on_ui(self.game)

		self.game_window.add_widget(self.agents_grid)

		return self.window


	def proceed(self, instance):
		print("proceeding................")
		self.game.proceed_turn()
		#TODO: update memory panel
		self.update_data_on_ui(self.game.get_rooms_data())

	
	def update_data_on_ui(self, game):
		self.agents_grid.clear_widgets()
		for r in self.game.rooms:
			stack = StackLayout()
			for o in r.occupants:
				print(o)
				agent_button = Button(
							background_normal=o.image,
							size_hint_x = 0.2	#TODO: needs to be square
							)
				# agent_button.size_hint_x = agent_button.size_hint_y
				agent_button_callback = partial(self.on_click_display_memory, o)  #allows passing argument into on_click_display_memory func
				agent_button.bind(on_press=agent_button_callback)
				stack.add_widget(agent_button)
			self.agents_grid.add_widget(stack)

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

