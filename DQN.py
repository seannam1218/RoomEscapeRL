import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
# import namedtuple

class DQN(nn.Module):
	def __init__(self, message_len, password_len, num_agents):
		super().__init__()

		#TODO: fix these dimensions # message_memory, room_hint, input_password, is_room_unlocked, is_hint_room_unlocked
		input_dimension = 17
		action_dimension = 3

		self.fc1 = nn.Linear(in_features=input_dimension, out_features=12)
		self.fc2 = nn.Linear(in_features=12, out_features=10)
		self.out = nn.Linear(in_features=10, out_features=action_dimension)

	def forward(self, t): 
		# where t is the tensor that is being passed through the NN
		# print("forward: ", t)
		t = t.flatten(start_dim=0).float()
		t = F.relu(self.fc1(t))
		t = F.relu(self.fc2(t))
		t = self.out(t)
		# print("out: ", t)
		return t


# example of how to run this nn
# d = DQN(1, 1, 1)
# print(d(torch.tensor([0.,0.5,0.,1.,0.])))  # runs one time forward following the protocol in forward function. returns tensor