from maze import Maze


def run_single_exp(envir, policy):
    obs = envir.reset()
    _done = False

    total_reward = 0

    while not _done:
        action = policy(obs)
        obs, reward, _done = envir.step(action)

        total_reward += reward

    print(envir.turns_elapsed)
    return total_reward
