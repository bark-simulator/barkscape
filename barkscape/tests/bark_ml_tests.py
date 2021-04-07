# Copyright (c) 2021 fortiss GmbH
#
# Authors: Julian Bernhard, Klemens Esterle, Patrick Hart and
# Tobias Kessler
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import numpy as np
import time
import gym
import sys, os, logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import asyncio, json
from bark.runtime.viewer.buffered_viewer import BufferedViewer
import bark_ml.environments.gym

# visual
from barkscape.handlers.bark_ml_runtime_handler import BarkMLRuntimeHandler
import xviz_avs
from xviz_avs.builder import XVIZBuilder, XVIZMetadataBuilder
from xviz_avs.server import XVIZServer, XVIZBaseSession

if __name__ == "__main__":
  handler = logging.StreamHandler(sys.stdout)
  handler.setLevel(logging.DEBUG)
  logging.getLogger("xviz-server").addHandler(handler)


  env = gym.make("merging-medium-v0")
  # set buffered viewer
  viewer = BufferedViewer()
  env._viewer = viewer

  # run-stuff
  logger = logging.getLogger()
  scen_handler = BarkMLRuntimeHandler(runtime=env, logger=logger)
  server = XVIZServer(scen_handler, port=8081)
  loop = asyncio.get_event_loop()
  loop.run_until_complete(server.serve())
  loop.run_forever()