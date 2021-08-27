import matplotlib.pyplot as plt
import numpy as np
from numpy import mean
import torch

class Plotter():
	def __init__(self, moving_avg_period):
		self.moving_avg_period = moving_avg_period
		self.xs = [0]
		self.ys = [0]
		self.max_y = 0
		self.moving_avgs = [0]
		self.figure = plt.figure(1)
		plt.title('Training...')
		plt.xlabel('Episode')
		plt.ylabel('Duration')
		self.turns_graph, = plt.plot(self.xs, self.ys)
		self.ma_graph, = plt.plot(self.xs, self.moving_avgs)
		plt.pause(0.00001)

	def add_data(self, x, y):
		self.xs.append(x)
		self.ys.append(y)

		self.turns_graph.set_xdata(self.xs)
		self.turns_graph.set_ydata(self.ys)

		self.get_moving_average()
		self.ma_graph.set_xdata(self.xs)
		self.ma_graph.set_ydata(self.moving_avgs)

		# rescale the axes
		plt.xlim(0, x)
		if self.max_y < y:
			self.max_y = y
			plt.ylim(0, self.max_y)

		plt.draw()
		plt.pause(0.000001)

	def get_moving_average(self):
		if len(self.ys) >= self.moving_avg_period:
			self.moving_avgs.append(mean(self.ys[-self.moving_avg_period:]))
		else:
			self.moving_avgs.append(0)

	def show_plot(self):
		plt.title('Result')
		plt.show()