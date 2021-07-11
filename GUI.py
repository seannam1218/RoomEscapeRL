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

		# # text input widget
		# self.user = TextInput(
		# 			multiline= False,
		# 			padding_y= (20,20),
		# 			size_hint= (1, 0.5)
		# 			)

		# self.window.add_widget(self.user)
		self.rooms_state = GridLayout(cols=2)
		self.window.add_widget(self.rooms_state)




		# button widget
		self.button_grid = GridLayout(cols=1)
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
			# self.button.bind(on_press=self.callback)
			self.rooms.append(button)
			self.button_grid.add_widget(button)
		
		self.rooms_state.add_widget(self.button_grid)

		# label widget
		self.greeting2 = Label(
						text= "wow",
						font_size= 18,
						color= '#00FFCE'
						)
		self.rooms_state.add_widget(self.greeting2)


		return self.window


	def proceed(self, instance):
		print("proceeding................")
		self.game.proceed_turn()
		self.update_data(self.game.get_rooms_data())

	
	def update_data(self, data):
		self.data = data
		for i in range(len(self.data)):
			room = self.data[i]
			print(room.number)
			agents = room.occupants
			for j in range(len(agents)):
				print(agents[j].name)
				self.window.add_widget(Image(source=agents[j].image))



