from typing import Tuple

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch import distributions


class ActorCritic(nn.Module):
    """
    A base Actor-Critic class
    """

    def __init__(
        self,
        num_inputs: int,
        num_outputs: int,
        hidden_layer_config: tuple = (10, 10),
        activation_func=F.relu,
    ) -> None:
        """
        Note:
        - num_inputs = size of the observation space
        - num_outputs = no. of possible actions
        - activation_func = activation function to use between layers. Using F.* format here.
        https://discuss.pytorch.org/t/whats-the-difference-between-nn-relu-vs-f-relu/27599
        """
        super(ActorCritic, self).__init__()

        self.num_inputs: int = num_inputs
        self.num_outputs: int = num_outputs
        # https://deepai.org/machine-learning-glossary-and-terms/hidden-layer-machine-learning
        self.hidden_layer_config: tuple = hidden_layer_config
        self.activation_func = activation_func

        # https://towardsdatascience.com/pytorch-layer-dimensions-what-sizes-should-they-be-and-why-4265a41e01fd
        # Format of nn:
        # https://pytorch.org/docs/stable/generated/torch.nn.Module.html

        self.hidden_layers = nn.ModuleList(
            [
                nn.Linear(hidden_layer_config[_], hidden_layer_config[_ + 1])
                for _ in range(len(hidden_layer_config) - 1)
            ]
        )

        # self.input_layer = nn.Linear(
        #     in_features=self.num_inputs,
        #     out_features=self.hidden_layers[0],
        #     bias=True
        # )

        # # Actor/probabilities
        # # LogSoftmax - pg126 Deep Reinforcement Learning in Action
        # self.policy_output_layer = nn.Sequential(
        #     nn.Linear(
        #         in_features=self.hidden_layers[-1],
        #         out_features=self.num_outputs,
        #         bias=True
        #     ),
        #     nn.LogSoftmax(dim=1)
        # )

        # Critic
        # The output is expected to be a single number because
        # it's an approximation of state value.
        # https://stackoverflow.com/questions/55405961/why-does-sigmoid-function-outperform-tanh-and-softmax-in-this-case
        # self.value_output_layer = nn.Linear(
        #     in_features=self.hidden_layers[-1],
        #     out_features=1,
        #     bias=True
        # )

        # Softmax output: Actor needs to return probabilities for each available action
        self.actor = nn.Sequential(
            nn.Linear(self.num_inputs, 10),
            nn.ReLU(),
            nn.Linear(10, self.num_outputs),
            nn.Softmax(dim=1),
        )

        self.critic = nn.Sequential(
            nn.Linear(self.num_inputs, 10), nn.ReLU(), nn.Linear(10, 1)
        )

    def forward(self, state: torch.FloatTensor) -> Tuple[torch.Tensor, torch.Tensor]:
        # Assert this state is a Tensor of floats, or else
        assert isinstance(state, torch.FloatTensor)

        # x = self.activation_func(self.input_layer(state))

        # for h in self.hidden_layers:
        #     state = self.activation_func(h(x))

        # actor = self.policy_output_layer(x)
        # critic = self.value_output_layer(x)

        # https://www.kite.com/python/docs/torch.distributions.Categorical
        # Categorical is to allow picking from a multinomial distribution
        # and allow .sample() to be used on the probability distribution.
        # Example
        # >>> m = Categorical(torch.tensor([ 0.01, 0.01, 0.97, 0.01 ]))
        # >>> m.sample()  # heavily in favour of tensor(2)
        action_probability_dist = distributions.Categorical(self.actor(state))
        state_values = self.critic(state)

        # print("actor(state)", self.actor(state))
        # print("action_probability_dist", action_probability_dist)
        # print(
        #     "action_probability_dist sampled", action_probability_dist.sample().item()
        # )
        # print("state_values", state_values)
        # state_values = critic
        return action_probability_dist, state_values
