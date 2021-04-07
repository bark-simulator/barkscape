import sys, os, logging
from xviz_avs.server import XVIZServer


class BaseSever:
  def __init__(self,
    handler=None,
    runner=None,
    runtime=None,
    logger=None,
    port=8081,
    viewer=None):
  self._handler = handler or BaseHandler(
    runtime, logger, runner, viewer)
  self._port = port
  
  def Start(self):
    server = XVIZServer(self._handler, port=self._port)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.serve())
    loop.run_forever()
