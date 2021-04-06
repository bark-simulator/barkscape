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
from bark.core.world.renderer import *
from bark.core.geometry import *
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

def dist_reward(goal_center_line, x, y, d_max=5, exp=0.4):
  return 1. - (Distance(goal_center_line, Point2d(x, y))/d_max)**exp

def dist_other(world, ego_id, x, y, d_max=20, exp=0.2):
  d = 0.
  for id, agent in world.agents.items():
    state = agent.history[-1][0]
    dist = Distance(Point2d(state[1], state[2]), Point2d(x, y))
    if ego_id != id and dist < d_max:
      d += (dist/d_max)**exp - 1.
  return d

def DrawPhiDistDist(env, a=0.4):
  bark_world = env._world
  bb = bark_world.bounding_box
  ego_id = env._scenario._eval_agent_ids[0]
  ego_agent = env._world.agents[ego_id]
  goal_center_line = ego_agent.goal_definition.center_line
  x_range = np.arange(bb[0].x(), bb[1].x(), 1.5)
  y_range = np.arange(bb[0].y(), bb[1].y(), 1.5)
  X, Y = np.meshgrid(x_range, y_range)
  zs = np.array([dist_reward(goal_center_line, x, y, exp=a) + dist_other(bark_world, ego_id, x, y) for x,y in zip(np.ravel(X), np.ravel(Y))])
  total_reward = zs.reshape(X.shape)
  # cmap = LinearSegmentedColormap.from_list('mycmap', [(12/255, 44/255, 132/255, 1), (199/255, 233/255, 180/255, 1)])
  
  for xx, yy, zz in zip(X, Y, total_reward):
    for x, y, z in zip(xx, yy, zz):
      poly = Polygon2d([0, 0, 0], [
        Point2d(-0.5, -0.5),
        Point2d(-0.5, 0.5),
        Point2d(0.5, 0.5),
        Point2d(0.5, -0.5)])
      poly = poly.Translate(Point2d(x, y))
      norm = plt.Normalize(-1, 1)
      color = [int(255*x) for x in plt.cm.jet(norm(z))]
      # set alpha
      color[-1] = 64
      color = tuple(color)
      poly_primitive = RenderPrimitive(poly)
      poly_primitive.Add("height", 2.5*z)
      poly_primitive.Add("stroke_color", (128, 128, 128, 128))
      poly_primitive.Add("fill_color", color)
      bark_world.renderer.Add("POLYGONS", poly_primitive)

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
      
      # TODO: visualize rewards
      DrawPhiDistDist(self._runner._environment)
      
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
