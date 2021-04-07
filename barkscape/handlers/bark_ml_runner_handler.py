# Copyright (c) 2021 fortiss GmbH
#
# Authors: Julian Bernhard, Klemens Esterle, Patrick Hart and
# Tobias Kessler
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import sys, os, logging
import asyncio, json, time
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# BARKSCAPE
from barkscape.handlers.base_runner import BaseRunner
from tf_agents.trajectories import time_step as ts


class BARKMLRunnerRunner(BaseRunner):
  def __init__(
    self, socket, request, runnable_object=None,
    dt=0.2, logger=None, stream=None):
    super().__init__(
      socket, request, runnable_object=runnable_object,
      dt=dt, logger=logger, stream=stream)
  
  async def RunEpisode(self, render=True, trace_colliding_ids=None, **kwargs):
    state = self._runnable_object._environment.reset()
    is_terminal = False
    t = 0.
    while not is_terminal:
      start_time = time.time()
      action_step = self._runnable_object._agent._eval_policy.action(
        ts.transition(state, reward=0.0, discount=1.0))
      action = self._runnable_object.ReshapeActionIfRequired(action_step)
      env_data = self._runnable_object._environment.step(action)
      state, reward, is_terminal, info = env_data
      
      if render:
        self._runnable_object._environment.render()
      message = await self._bark_xviz_stream.get_message(
        t, self._runnable_object._environment)
      await self._socket.send(json.dumps(message))
      end_time = time.time()
      self._runnable_object._environment._world.renderer.Clear()
      pause_dt = min(self._dt - end_time - start_time, 0.01)
      t += self._dt
      await asyncio.sleep(pause_dt)

  async def main(self):
    metadata = self._bark_xviz_stream.get_metadata()
    await self._socket.send(json.dumps(metadata))
    for i in range(0, 20):
      await self.RunEpisode()
