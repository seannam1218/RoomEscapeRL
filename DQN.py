import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
# import namedtuple

class DQN(nn.Module):
	def __init__(self, message_len, password_len, num_agents):
		super().__init__()

		input_dimension = 10 #TODO: fix these dimensions
		action_dimension = 10

		self.fc1 = nn.Linear(in_features=input_dimension, out_features=24)
		self.fc2 = nn.Linear(in_features=24, out_features=32)
		self.out = nn.Linear(in_features=32, out_features=action_dimension)

	def forward(self, t): 
		# where t is the tensor that is being passed through the NN
		t = t.flatten(start_dim=1)
		t = F.relu(self.fc1(t))
		t = F.relu(self.fc2(t))
		t = self.out(t)
		return t


# Experience = namedtuple(
# 	'Experience',
# 	('state', 'action', 'next_state', 'reward')
# )
