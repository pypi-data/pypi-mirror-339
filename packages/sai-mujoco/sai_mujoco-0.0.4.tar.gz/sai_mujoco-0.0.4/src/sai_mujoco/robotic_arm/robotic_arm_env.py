import os

import gymnasium as gym
import numpy as np
import mujoco

from gymnasium import utils
from gymnasium.envs.mujoco.mujoco_env import MujocoEnv

from ..utils.overlay import toggle_overlay

class RoboticArmEnv(MujocoEnv, utils.EzPickle):
    # Robot: https://www.ufactory.cc/product-page/ufactory-xarm-7/
    metadata = {
        "render_modes": [
            "human",
            "rgb_array",
            "depth_array",
        ],
        "render_fps": 167,
    }
    def __init__(self, show_overlay: bool = False, **kwargs):

        utils.EzPickle.__init__(self, **kwargs)
        # Gym Spaces
        observation_space = gym.spaces.Box(-np.inf, np.inf, shape=(413,), dtype=np.float64)
        self.action_space = gym.spaces.Box(0, 1, shape=(8,), dtype=np.float64)

        MujocoEnv.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__), "assets", "scene.xml"
            ),
            3,
            observation_space=observation_space,
            default_camera_config={
                "trackbodyid": 0,
                "distance": 3,
            },
            **kwargs,
        )

        toggle_overlay(self.mujoco_renderer, show_overlay, kwargs["render_mode"])
        self.total_steps = 1000

    def _get_obs(self):
        obs = np.concatenate(
            [
                self.data.qpos.flat, # position of each joint
                self.data.qvel.flat, # velocity of each joint
                self.data.cinert.flat, # center of mass - based body inertia and mass
                self.data.cvel.flat, # center of mass  -based velocity
                self.data.qfrc_actuator.flat, # net unconstrained force
                self.data.cfrc_ext.flat, # external force on body
            ]
        )
        return obs

    def _get_info(self):
        info = {
            "pos": self.data.xpos[1],
            "rot": self.data.xquat[1]
        }
        return info

    def reset(self, seed=None, options=None):
        # give the random reset a try after..
        super().reset(seed=None)
        mujoco.mj_resetData(self.model, self.data)
        self.step_count = 0
        self.done = False
        return self._get_obs(), self._get_info()

    def reset_model(self):
        pass

    def step(self, action):
        #initialize action
        action[0:2] = (action[0:2] * 100) - 50
        action[2:5] = (action[2:5] * 60) - 30
        action[5:7] = (action[5:7]* 40) - 20
        action[7] =  (action[7] * 100) - 50

        # map to -1 to 1
        self.data.ctrl = action

        for i in range(3):
            mujoco.mj_step(self.model, self.data)

        observation = self._get_obs()
        info = self._get_info()

        # Reward function
        reward = 1
        self.step_count += 1
        # self.reward_sum += reward

        # Episode ending
        if (self.step_count == self.total_steps):
            self.done = True

        return observation, reward, self.done, False, info
