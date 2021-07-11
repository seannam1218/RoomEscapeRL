from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class GUI(App):
	def __init__(self, game, **kwargs):
		super(GUI, self).__init__(**kwargs)
		self.game = game
		self.rooms = []
		self.agents = []


	def build(self):
		#returns a window object with all it's widgets
		self.window = BoxLayout(orientation='vertical')
		self.window.cols = 1
		self.window.size_hint = (0.95, 0.95)
		self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

		# button for proceed
		button_proceed = Button(
					text= "Proceed",
					size_hint= (1,0.5),
					bold= True,
					# pos = (self.window.width, 1),
					background_color ='#FF6600',
					#remove darker overlay of background colour
					background_normal = ""
					)
		self.window.add_widget(button_proceed)
		button_proceed.bind(on_press=self.proceed)
		

		# label widget
		self.greeting = Label(
						text= "Memory",
						font_size= 18,
						color= '#00FFCE'
						)
		self.window.add_widget(self.greeting)


		### create a space to represent rooms and its occupants
		self.rooms_state = GridLayout(cols=2)
		self.window.add_widget(self.rooms_state)

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
			self.rooms.append(button)
			self.room_grid.add_widget(button)
		
		self.rooms_state.add_widget(self.room_grid)

		# self.agents_grid = GridLayout(cols=self.game.num_agents)
		self.agents_grid_list = []
		self.agents_grid = GridLayout(cols=self.game.num_agents)
		self.update_data_on_ui(self.game)

		self.rooms_state.add_widget(self.agents_grid)

		return self.window


	def proceed(self, instance):
		print("proceeding................")
		self.game.proceed_turn()
		self.update_data_on_ui(self.game.get_rooms_data())

	
	def update_data_on_ui(self, game):
		# self.agents_grid.remove_widget(self.agents_grid)
		# self.agents_grid = GridLayout(cols=self.game.num_agents)
		self.agents_grid.clear_widgets()
		self.agents_grid_list = []
		for i in range(self.game.num_rooms+1):
			for j in range(self.game.num_agents):
				try:
					self.agents_grid_list.append(
						Image(source=self.game.rooms[i].occupants[j].image)
						)
				except:
					blank_agent = Image(source='images/blank.png')
					self.agents_grid_list.append(blank_agent)
		
		for agent in self.agents_grid_list:
			self.agents_grid.add_widget(agent)
		
