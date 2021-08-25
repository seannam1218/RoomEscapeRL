import torch

class QValues():
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

	@staticmethod
	def get_current(policy_net, states, actions):
		return policy_net(states).gather(dim=1, index=actions.unsqeeze(-1))
	
	@staticmethod
	def get_next(target_net, next_states):
		final_state_locations = next_states.flatten(start_dim=1).max(dim=1)[0].eq(0).type(torch.bool)
		print(str(final_state_locations))
		return

	