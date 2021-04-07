# Copyright (c) 2021 fortiss GmbH
#
# Authors: Julian Bernhard, Klemens Esterle, Patrick Hart and
# Tobias Kessler
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import sys, os, logging
import asyncio, json
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# BARKSCAPE
from barkscape.handlers.base_runner import BaseRunner


class BARKMLRuntimeRunner(BaseRunner):
  def __init__(
    self, socket, request, runnable_object=None,
    dt=0.2, logger=None, stream=None):
    super().__init__(
      socket, request, runnable_object=runnable_object,
      dt=dt, logger=logger, stream=stream)

  async def main(self):
    metadata = self._bark_xviz_stream.get_metadata()
    await self._socket.send(json.dumps(metadata))
    for eps in range(0, 20):
      t = 0        
      self._runnable_object.reset()
      for i in range(0, 35):
        action = np.random.uniform(
          low=np.array([-0.5, -0.1]), high=np.array([0.5, 0.1]), size=(2, ))
        observed_next_state, reward, done, info = self._runnable_object.step(action)
        message = await self._bark_xviz_stream.get_message(t, self._runnable_object)
        await self._socket.send(json.dumps(message))
        self._runnable_object._world.renderer.Clear()
        t += self._dt
        await asyncio.sleep(self._dt)