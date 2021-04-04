import gym
from typing import TypeVar
import random

Action = TypeVar("Action")


class RandomActionWrapper(gym.ActionWrapper):
    def __init__(self, env, epsilon=0.5) -> None:
        super(RandomActionWrapper, self).__init__(env)
        self.epsilon = epsilon

    def action(self, action: Action) -> Action:
        if random.random() > self.epsilon:
            print("random!")
            return self.env.action_space.sample()
        print("not random!")
        return action


if __name__ == "__main__":
    env = RandomActionWrapper(gym.make("CartPole-v1"))
    total_reward = 0.0
    total_steps = 0
    obs = env.reset()

    while True:
        action = env.action_space.sample()
        observation, reward, done, _ = env.step(action)
        total_reward += reward
        total_steps += 1
        if done:
            break

    print(f"Episode done in {total_steps}, total reward {total_reward}")

    env.close()
