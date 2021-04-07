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
from bark.runtime.commons.parameters import ParameterServer
from bark.runtime.viewer.buffered_viewer import BufferedViewer
from bark.runtime.scenario.scenario_generation.config_with_ease import \
  LaneCorridorConfig, ConfigWithEase
from bark.runtime.runtime import Runtime

from bark.core.world.opendrive import *
from bark.core.world.goal_definition import *
from bark.core.models.behavior import *
from bark.core.commons import SetVerboseLevel

# BARKSCAPE
from barkscape.server.base_server import BaseServer
from barkscape.server.base_runner import BaseRunner

class CustomBARKRunner(BaseRunner):
  def __init__(
    self, socket, request, runnable_object=None,
    dt=0.2, logger=None, stream=None):
    super().__init__(
      socket, request, runnable_object=runnable_object,
      dt=dt, logger=logger, stream=stream)
  
  async def main(self):
    metadata = self._bark_xviz_stream.get_metadata()
    await self._socket.send(json.dumps(metadata))
    for eps in range(0, 30):
      t = 0
      self._runnable_object.reset()
      for i in range(0, 35):
        self._runnable_object.step()
        message = await self._bark_xviz_stream.get_message(t, self._runnable_object)
        await self._socket.send(json.dumps(message))
        self._runnable_object._world.renderer.Clear()
        t += self._dt
        await asyncio.sleep(self._dt)


# scenario
class CustomLaneCorridorConfig(LaneCorridorConfig):
  def __init__(self,
               params=None,
               **kwargs):
    super(CustomLaneCorridorConfig, self).__init__(params, **kwargs)
  
  def goal(self, world):
    road_corr = world.map.GetRoadCorridor(
      self._road_ids, XodrDrivingDirection.forward)
    lane_corr = self._road_corridor.lane_corridors[0]
    return GoalDefinitionPolygon(lane_corr.polygon)


if __name__ == "__main__":
  # configure lanes
  param_server = ParameterServer()
  left_lane = CustomLaneCorridorConfig(params=param_server,
                                      lane_corridor_id=0,
                                      road_ids=[0, 1],
                                      behavior_model=BehaviorMobilRuleBased(param_server),
                                      s_min=5.,
                                      s_max=50.)
  right_lane = CustomLaneCorridorConfig(params=param_server,
                                        lane_corridor_id=1,
                                        road_ids=[0, 1],
                                        controlled_ids=True,
                                        behavior_model=BehaviorMobilRuleBased(param_server),
                                        s_min=5.,
                                        s_max=20.)
  scenarios = \
    ConfigWithEase(num_scenarios=3,
                  map_file_name="examples/data/DR_DEU_Merging_MT_v01_shifted.xodr",
                  random_seed=0,
                  params=param_server,
                  lane_corridor_configs=[left_lane, right_lane])

  viewer = BufferedViewer()
  env = Runtime(step_time=0.2,
                viewer=viewer,
                scenario_generator=scenarios,
                render=True,
                maintain_world_history=True)

  # run BARKSCAPE
  logger = logging.getLogger()
  bark_server = BaseServer(
    runner=CustomBARKRunner, runnable_object=env, logger=logger)
  bark_server.Start()
