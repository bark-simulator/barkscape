# Copyright (c) 2021 fortiss GmbH
#
# Authors: Julian Bernhard, Klemens Esterle, Patrick Hart and
# Tobias Kessler
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import sys, os, logging
import asyncio, json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# BARKSCAPE
from barkscape.server.base_runner import BaseRunner


class BARKRunner(BaseRunner):
  def __init__(
    self, socket, request, runnable_object=None,
    dt=0.2, logger=None, stream=None):
    super().__init__(
      socket, request, runnable_object=runnable_object,
      dt=dt, logger=logger, stream=stream)
  
  async def main(self):
    metadata = self._bark_xviz_stream.get_metadata()
    await self._socket.send(json.dumps(metadata))
    # TODO: this needs to be a self-contained run-time
    for eps in range(0, 20):
      t = 0
      self._runnable_object.reset()
      for i in range(0, 35):
        self._runnable_object.step()
        message = await self._bark_xviz_stream.get_message(t, self._runnable_object)
        await self._socket.send(json.dumps(message))
        self._runnable_object._world.renderer.Clear()
        t += self._dt
        await asyncio.sleep(self._dt)

