# Copyright (c) 2021 fortiss GmbH
#
# Authors: Julian Bernhard, Klemens Esterle, Patrick Hart and
# Tobias Kessler
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import sys, os, logging
import asyncio, json
import xviz_avs
from xviz_avs.server import XVIZBaseSession
from barkscape.handlers.bark_viewer import BarkViewer


"""BaseRunner
   Steps the runtime and the XVIZViewer.
"""
class BaseRunner(XVIZBaseSession):
  def __init__(
    self, socket, request, runtime=None, dt=0.2, logger=None, viewer=None):
    super().__init__(socket, request)
    self._runtime = runtime
    self._bark_viewer = viewer or BarkViewer()
    self._socket = socket
    self._dt = dt
    self._logger = logger

  def on_connect(self):
    print("Web-client connected.")

  def on_disconnect(self):
    print("Web-client disconnect.")
  
  """Main functionality for stepping and sending visualization messages
  """
  async def main(self):
    t = 0
    metadata = self._bark_viewer.get_metadata()
    await self._socket.send(json.dumps(metadata))
    message = await self._bark_viewer.get_message(t, self._runtime)
    await self._socket.send(json.dumps(message))
    await asyncio.sleep(self._dt)