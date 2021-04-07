# Copyright (c) 2021 fortiss GmbH
#
# Authors: Julian Bernhard, Klemens Esterle, Patrick Hart and
# Tobias Kessler
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.
import gym
import sys, os, logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from bark.runtime.viewer.buffered_viewer import BufferedViewer
import bark_ml.environments.gym

# BARKSCAPE
from barkscape.handlers.base_server import BaseServer
from barkscape.handlers.base_handler import BaseHandler
from barkscape.handlers.bark_ml_runtime_handler import BARKMLRuntimeRunner

if __name__ == "__main__":
  env = gym.make("merging-medium-v0")
  # set buffered viewer
  viewer = BufferedViewer()
  env._viewer = viewer

  # run-stuff
  logger = logging.getLogger()
  bark_server = BaseServer(
    runner=BARKMLRuntimeRunner, runnable_object=env, logger=logger)
  bark_server.Start()

