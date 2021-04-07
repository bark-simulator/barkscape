# Copyright (c) 2021 fortiss GmbH
#
# Authors: Julian Bernhard, Klemens Esterle, Patrick Hart and
# Tobias Kessler
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.
import sys, os, logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from bark.runtime.viewer.buffered_viewer import BufferedViewer
from experiments.experiment_runner import ExperimentRunner
from bark_ml.library_wrappers.lib_tf_agents.runners import SACRunner

# BARKSCAPE
from barkscape.server.base_server import BaseServer
from barkscape.server.base_handler import BaseHandler
from barkscape.server.runners.bark_ml_runner_runner import BARKMLRunnerRunner


def load_exp_runner(file_name):
  return ExperimentRunner(
    json_file=file_name,
    mode=None,
    random_seed=0)


if __name__ == "__main__":
  # load experiment
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
  bark_server = BaseServer(
    runner=BARKMLRunnerRunner, runnable_object=runner, logger=logger)
  bark_server.Start()
