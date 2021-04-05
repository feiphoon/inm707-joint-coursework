"""
Adapted from here:
https://github.com/openai/baselines/blob/master/baselines/common/vec_env/vec_env.py
https://github.com/openai/baselines/blob/master/baselines/common/vec_env/subproc_vec_env.py

These are some useful abstractions to manage several async environments.
Could not just install baselines as a package because it required Mujoco
(we don't want the whole thing), so this is an adaptation/selective copy with credit.

We removed anything to do with viewing images, and there were some removals 
of values pertaining only to gym.openai envs.
"""
import numpy as np
from abc import ABC, abstractmethod
from multiprocessing import Process, Pipe


class VecEnv(ABC):
    """
    An abstract asynchronous, vectorized environment.
    Used to batch data from multiple copies of an environment, so that
    each observation becomes an batch of observations, and expected action is a batch of actions to
    be applied per-environment.
    """

    def __init__(self, num_envs, observation_space, action_space):
        self.num_envs = num_envs
        self.observation_space = observation_space
        self.action_space = action_space

    @abstractmethod
    def reset(self):
        """
        Reset all the environments and return an array of
        observations, or a dict of observation arrays.
        If step_async is still doing work, that work will
        be cancelled and step_wait() should not be called
        until step_async() is invoked again.
        """
        pass

    @abstractmethod
    def step_async(self, actions):
        """
        Tell all the environments to start taking a step
        with the given actions.
        Call step_wait() to get the results of the step.
        You should not call this if a step_async run is
        already pending.
        """
        pass

    @abstractmethod
    def step_wait(self):
        """
        Wait for the step taken with step_async().
        Returns (obs, rews, dones, infos):
         - obs: an array of observations, or a dict of
                arrays of observations.
         - rews: an array of rewards
         - dones: an array of "episode done" booleans
         - infos: a sequence of info objects
        """
        pass

    def close(self):
        """Modified! We don't actually need
        this unless we're using a gym.openai env.
        """
        pass

    def step(self, actions):
        """
        Step the environments synchronously.
        This is available for backwards compatibility.
        """
        self.step_async(actions)
        return self.step_wait()


class VecEnvWrapper(VecEnv):
    """
    An environment wrapper that applies to an entire batch
    of environments at once.
    """

    def __init__(self, venv, observation_space=None, action_space=None):
        self.venv = venv
        super().__init__(
            num_envs=venv.num_envs,
            observation_space=observation_space or venv.observation_space,
            action_space=action_space or venv.action_space,
        )

    def step_async(self, actions):
        self.venv.step_async(actions)

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def step_wait(self):
        pass

    def close(self):
        return self.venv.close()

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(
                "attempted to get missing private attribute '{}'".format(name)
            )
        return getattr(self.venv, name)


class VecEnvObservationWrapper(VecEnvWrapper):
    @abstractmethod
    def process(self, obs):
        pass

    def reset(self):
        obs = self.venv.reset()
        return self.process(obs)

    def step_wait(self):
        obs, rews, dones, infos = self.venv.step_wait()
        return self.process(obs), rews, dones, infos


class CloudpickleWrapper(object):
    """
    Uses cloudpickle to serialize contents (otherwise multiprocessing tries to use pickle)
    """

    def __init__(self, x):
        self.x = x

    def __getstate__(self):
        import cloudpickle

        return cloudpickle.dumps(self.x)

    def __setstate__(self, ob):
        import pickle

        self.x = pickle.loads(ob)


def worker(remote, parent_remote, env_fn_wrappers):
    def step_env(env, action):
        (
            ob,
            reward,
            done,
        ) = env.step(action)
        if done:
            ob = env.reset()
        return ob, reward, done

    parent_remote.close()
    envs = [env_fn_wrapper() for env_fn_wrapper in env_fn_wrappers.x]
    try:
        while True:
            cmd, data = remote.recv()
            if cmd == "step":
                remote.send([step_env(env, action) for env, action in zip(envs, data)])
            elif cmd == "reset":
                remote.send([env.reset() for env in envs])
            elif cmd == "render":
                remote.send([env.render(mode="rgb_array") for env in envs])
            elif cmd == "close":
                remote.close()
                break
            elif cmd == "get_spaces_spec":
                remote.send(
                    CloudpickleWrapper(
                        (envs[0].observation_space, envs[0].action_space, envs[0].spec)
                    )
                )
            else:
                raise NotImplementedError
    except KeyboardInterrupt:
        print("SubprocVecEnv worker: got KeyboardInterrupt")
    finally:
        for env in envs:
            env.close()


class SubprocVecEnv(VecEnv):
    """
    VecEnv that runs multiple environments in parallel in subproceses and communicates with them via pipes.
    Recommended to use when num_envs > 1 and step() can be a bottleneck.
    """

    def __init__(self, env_fns, spaces=None):
        """
        Arguments:
        env_fns: iterable of callables -  functions that create environments to run in subprocesses. Need to be cloud-pickleable
        """
        self.waiting = False
        self.closed = False
        self.nenvs = len(env_fns)

        self.remotes, self.work_remotes = zip(*[Pipe() for _ in range(self.nenvs)])
        self.ps = [
            Process(
                target=worker, args=(work_remote, remote, CloudpickleWrapper(env_fn))
            )
            for (work_remote, remote, env_fn) in zip(
                self.work_remotes, self.remotes, env_fns
            )
        ]
        for p in self.ps:
            # if the main process crashes, we should not cause things to hang
            p.daemon = True
            p.start()
        for remote in self.work_remotes:
            remote.close()

        self.remotes[0].send(("get_spaces", None))
        observation_space, action_space = self.remotes[0].recv()
        VecEnv.__init__(self, self.nenvs, observation_space, action_space)

    def step_async(self, actions):
        # actions = np.array_split(actions, self.nremotes)
        for remote, action in zip(self.remotes, actions):
            remote.send(("step", action))
        self.waiting = True

    def step_wait(self):
        results = [remote.recv() for remote in self.remotes]
        results = _flatten_list(results)
        self.waiting = False
        obs, rews, dones = zip(*results)
        return _flatten_obs(obs), np.stack(rews), np.stack(dones)

    def reset(self):
        for remote in self.remotes:
            remote.send(("reset", None))
        obs = [remote.recv() for remote in self.remotes]
        obs = _flatten_list(obs)
        return _flatten_obs(obs)

    def reset_task(self):
        for remote in self.remotes:
            remote.send(("reset_task", None))
        return np.stack([remote.recv() for remote in self.remotes])

    def close(self):
        if self.closed:
            return
        if self.waiting:
            for remote in self.remotes:
                remote.recv()
        for remote in self.remotes:
            remote.send(("close", None))
        for p in self.ps:
            p.join()
            self.closed = True

    def __len__(self):
        return self.nenvs

    # def close_extras(self):
    #     self.closed = True
    #     if self.waiting:
    #         for remote in self.remotes:
    #             remote.recv()
    #     for remote in self.remotes:
    #         remote.send(("close", None))
    #     for p in self.ps:
    #         p.join()

    # def get_images(self):
    #     self._assert_not_closed()
    #     for pipe in self.remotes:
    #         pipe.send(("render", None))
    #     imgs = [pipe.recv() for pipe in self.remotes]
    #     imgs = _flatten_list(imgs)
    #     return imgs

    # def _assert_not_closed(self):
    #     assert (
    #         not self.closed
    #     ), "Trying to operate on a SubprocVecEnv after calling close()"

    # def __del__(self):
    #     if not self.closed:
    #         self.close()


def _flatten_obs(obs):
    assert isinstance(obs, (list, tuple))
    assert len(obs) > 0

    if isinstance(obs[0], dict):
        keys = obs[0].keys()
        return {k: np.stack([o[k] for o in obs]) for k in keys}
    else:
        return np.stack(obs)


def _flatten_list(l):
    assert isinstance(l, (list, tuple))
    assert len(l) > 0
    assert all([len(l_) > 0 for l_ in l])

    return [l__ for l_ in l for l__ in l_]
