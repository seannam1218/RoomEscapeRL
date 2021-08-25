import matplotlib.pyplot as plt
import numpy as np
import torch

class Plotter():
	def __init__(self, moving_avg_period):
		self.moving_avg_period = moving_avg_period
		plt.figure(1)
		plt.title('Training...')
		plt.xlabel('Episode')
		plt.ylabel('Duration')
		

	def plot(self, values):
		plt.clf()
		plt.plot(values)
		plt.plot(self.get_moving_average(self.moving_avg_period, values))
		plt.pause(1)
		

	def get_moving_average(self, period, values):
		values = torch.tensor(values, dtype=torch.float)
		if len(values) >= period:
			moving_avg = values.unfold(dimension=0, size=period, step=1).mean(dim=1).flatten(start_dim=0)
			moving_avg = torch.cat((torch.zeros(period-1), moving_avg))
			return moving_avg.numpy()
		else:
			moving_avg = torch.zeros(len(values))
			return moving_avg.numpy()
