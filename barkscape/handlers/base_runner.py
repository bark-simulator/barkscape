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

# BARKSCAPE
from barkscape.handlers.bark_xviz_stream import BarkXvizStream


"""BaseRunner
   Steps the runnable_object and the XVIZstream.
"""
class BaseRunner(XVIZBaseSession):
  def __init__(
    self, socket, request, runnable_object=None,
    dt=0.2, logger=None, stream=None):
    super().__init__(socket, request)
    self._runnable_object = runnable_object
    self._bark_xviz_stream = stream or BarkXvizStream()
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
    metadata = self._bark_xviz_stream.get_metadata()
    await self._socket.send(json.dumps(metadata))
    message = await self._bark_xviz_stream.get_message(t, self._runnable_object)
    await self._socket.send(json.dumps(message))
    await asyncio.sleep(self._dt)