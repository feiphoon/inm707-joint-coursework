"""
Version of the Maze for Q-Learning.
(Keeping the basic Maze clean for now).
Based on Lab 3 code, but hoping to make some changes later.
"""
import numpy as np
from typing import Tuple

from maze import Maze, Action


class QMaze(Maze):
    def __init__(self, *args) -> None:
        super().__init__(*args)

        index_states = np.arange(0, self.size * self.size)
        np.random.shuffle(index_states)
        self.coord_to_index_state = index_states.reshape(self.size, self.size)

        # TODO: Adjust this later, be more creative with stochasticity
        # Set slipperiness of this QMaze
        # Select whether you move again, or stay in your current position
        self.prob_of_slipping = [0.1, 0.1, 0.1, 0.1, 0.6]

    def _get_agent_state(self) -> int:
        """
        Calculate the state once.
        """
        return self.coord_to_index_state[self.position_agent]

    def step(self, action: Action) -> Tuple[tuple, int, bool]:
        """
        We don't need the observations (a default requirement of basic RL) anymore,
        now we return a state, reward and done instead.
        """
        _, reward, done = super().step(action)
        state = self._get_agent_state()

        if done:
            return state, reward, done

        else:
            # np.random.multinomial "Draw samples from a multinomial distribution"
            # This is the random action that this policy will use to create a probability:
            # 1 draw, 1 given list of probabilities (adding to 1), 1 (size) run.
            # This "picks" one item out from the prob_of_action list: e.g. [0, 0, 1, 0]
            # Then argmax returns the index of the biggest item, so e.g. 2
            action_index = np.argmax(np.random.multinomial(1, self.prob_of_slipping))

            # Check for the action of "Don't move" other than the usual
            if action_index == (len(self.prob_of_slipping) - 1):
                # Do nothing
                # print("Oops, I slipped")
                return state, reward, done

            # Else it moves to another cell
            else:
                # This points to the index property/fetches the index of the action.
                # Yeah I refuse to make a dictionary just for this,
                # so this is what it's come to. We want this to return Action.DIRECTION
                for _ in list(Action):
                    if _.value.index == action_index:
                        action_to_take = _

                # E.g. action_to_take --> step(Action.DIRECTION)
                _, _additional_reward, done = super().step(action_to_take)

                # TODO: not sure if I needed to repeat this here, probably not.
                state = self._get_agent_state()

                # Don't penalize for second step, and don't increment timesteps.
                # The following offsets the usual action of reward -=1 for timestep taken.
                # Because we will commandeer step() to calculate the next step information.
                _additional_reward += 1
                self.turns_elapsed -= 1

                return state, reward + _additional_reward, done

    def reset(self) -> int:
        super().reset()
        # Return a goodness to be in a certain state instead
        # of original returned observation from Maze class.
        return self._get_agent_state()


# qm = QMaze(5)
# print(qm.reset())
# qm.display(debug=True)
