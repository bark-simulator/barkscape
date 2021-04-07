import sys, os, logging
import asyncio, json
from xviz_avs.server import XVIZServer

# BARKSCAPE
from barkscape.handlers.base_handler import BaseHandler

"""BaseServer
   handler: XVIZ handler
   runner: runs the runnable_object, e.g., steps the runtime
   runnable_object: can, e.g., be the BARK runtime or a
                    BARK-ML runner
   logger: for log outputs
   stream: streams XVIZ of BARK
"""
class BaseServer:
  def __init__(self,
    handler=None,
    runner=None,
    runnable_object=None,
    logger=None,
    port=8081,
    stream=None):
    self._handler = handler or BaseHandler(
      runnable_object, logger, runner, stream)
    self._port = port
    
  def Start(self):
    server = XVIZServer(self._handler, port=self._port)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.serve())
    loop.run_forever()
