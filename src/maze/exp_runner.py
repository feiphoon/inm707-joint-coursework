from maze import Maze


def run_single_exp(env, policy):
    obs = env.reset()
    _done = False

    total_reward = 0

    while not _done:
        action = policy(obs)
        obs, reward, _done = env.step(action)

        total_reward += reward

    print(env.turns_elapsed)
    return total_reward
