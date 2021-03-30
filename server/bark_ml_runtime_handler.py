# Copyright (c) 2021 fortiss GmbH
#
# Authors: Julian Bernhard, Klemens Esterle, Patrick Hart and
# Tobias Kessler
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import numpy as np
import sys, os, logging
import asyncio, json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import xviz_avs
from xviz_avs.builder import XVIZBuilder, XVIZMetadataBuilder
from xviz_avs.server import XVIZServer, XVIZBaseSession

from server.bark_viewer import BarkViewer


class BarkMLSession(XVIZBaseSession):
  def __init__(self, socket, request, runtime=None, dt=0.2, logger=None):
    super().__init__(socket, request)
    self._runtime = runtime
    self._bark_viewer = BarkViewer()
    self._socket = socket
    self._dt = dt
    self._logger = logger

  def on_connect(self):
    print("Connected!")

  def on_disconnect(self):
    print("Disconnect!")
  
  async def main(self):
    metadata = self._bark_viewer.get_metadata()
    await self._socket.send(json.dumps(metadata))
    # TODO: can we call the runner here
    for eps in range(0, 20):
      t = 0        
      self._runtime.reset()
      for i in range(0, 35):
        action = np.random.uniform(
          low=np.array([-0.5, -0.1]), high=np.array([0.5, 0.1]), size=(2, ))
        observed_next_state, reward, done, info = self._runtime.step(action)
        message = await self._bark_viewer.get_message(t, self._runtime)
        await self._socket.send(json.dumps(message))
        self._runtime._world.renderer.Clear()
        t += self._dt
        await asyncio.sleep(self._dt)

     
class BarkMLRuntimeHandler:
  def __init__(self, runtime=None, logger=None):
    self._runtime = runtime
    self._logger = logger

  def __call__(self, socket, request):
    return BarkMLSession(
      socket, request, runtime=self._runtime, logger=self._logger)
