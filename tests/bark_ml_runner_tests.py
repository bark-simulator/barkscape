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
from experiments.experiment_runner import ExperimentRunner
from bark_ml.library_wrappers.lib_tf_agents.runners import SACRunner
import bark_ml.environments.gym

# visual
from server.bark_ml_runner_handler import BarkMLRunnerHandler
import xviz_avs
from xviz_avs.builder import XVIZBuilder, XVIZMetadataBuilder
from xviz_avs.server import XVIZServer, XVIZBaseSession


def load_exp_runner(file_name):
  return ExperimentRunner(
    json_file=file_name,
    mode=None,
    random_seed=0)

if __name__ == "__main__":
  handler = logging.StreamHandler(sys.stdout)
  handler.setLevel(logging.DEBUG)
  logging.getLogger("xviz-server").addHandler(handler)


  exp_runner_gnn = load_exp_runner(
    "/Users/hart/Development/bark-ml/experiments/configs/phd/01_hyperparams/gnns/merging_large_embedding.json")
  runtime = exp_runner_gnn._experiment._runtime
  
  # set buffered viewer
  viewer = BufferedViewer()
  runtime._viewer = viewer
  
  runner = SACRunner(params=exp_runner_gnn._params,
                     environment=runtime,
                     agent=exp_runner_gnn._experiment._agent)

      
  # run-stuff
  logger = logging.getLogger()
  scen_handler = BarkMLRunnerHandler(runner=runner, logger=logger)
  server = XVIZServer(scen_handler, port=8081)
  loop = asyncio.get_event_loop()
  loop.run_until_complete(server.serve())
  loop.run_forever()