# Copyright (c) 2021 fortiss GmbH
#
# Authors: Julian Bernhard, Klemens Esterle, Patrick Hart and
# Tobias Kessler
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import time
import numpy as np
import sys, os, logging
import asyncio, json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import xviz_avs
from xviz_avs.builder import XVIZBuilder, XVIZMetadataBuilder
from xviz_avs.server import XVIZServer, XVIZBaseSession
from tf_agents.trajectories import time_step as ts

from server.bark_viewer import BarkViewer


class BarkMLRunnerSession(XVIZBaseSession):
  def __init__(self, socket, request, runner=None, dt=0.2, logger=None):
    super().__init__(socket, request)
    self._runner = runner
    self._bark_viewer = BarkViewer()
    self._socket = socket
    self._dt = dt
    self._logger = logger

  def on_connect(self):
    print("Connected!")

  def on_disconnect(self):
    print("Disconnect!")
  
  async def RunEpisode(self, render=True, trace_colliding_ids=None, **kwargs):
    state = self._runner._environment.reset()
    is_terminal = False
    t = 0.
    while not is_terminal:
      start_time = time.time()
      action_step = self._runner._agent._eval_policy.action(
        ts.transition(state, reward=0.0, discount=1.0))
      action = self._runner.ReshapeActionIfRequired(action_step)
      env_data = self._runner._environment.step(action)
      # self._runner._tracer.Trace(env_data, **kwargs)
      state, reward, is_terminal, info = env_data
      # visualize graph
      try:
        graph_tuples = self._runner._agent._agent._actor_network._latent_trace
        ego_id = self._runner._environment._scenario._eval_agent_ids[0]
        self._runner.ProcessGraphTuple(
          self._runner._environment,
          graph_tuples[-1],
          ego_id,
          render)
      except:
        pass
      if render:
        self._runner._environment.render()
      message = await self._bark_viewer.get_message(t, self._runner._environment)
      await self._socket.send(json.dumps(message))
      end_time = time.time()
      self._runner._environment._world.renderer.Clear()
      pause_dt = min(self._dt - end_time - start_time, 0.01)
      t += self._dt
      await asyncio.sleep(pause_dt)

        
  async def main(self):
    metadata = self._bark_viewer.get_metadata()
    await self._socket.send(json.dumps(metadata))
    for i in range(0, 20):
      await self.RunEpisode()

     
class BarkMLRunnerHandler:
  def __init__(self, runner=None, logger=None):
    self._runner = runner
    self._logger = logger

  def __call__(self, socket, request):
    return BarkMLRunnerSession(
      socket, request, runner=self._runner, logger=self._logger)
