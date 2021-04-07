# Copyright (c) 2021 fortiss GmbH
#
# Authors: Julian Bernhard, Klemens Esterle, Patrick Hart and
# Tobias Kessler
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.
import sys, os, logging
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
from barkscape.handlers.base_server import BaseServer
from barkscape.handlers.bark_runtime_handler import BARKRunner

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
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    logging.getLogger("xviz-server").addHandler(handler)

    # parameters
    param_server = ParameterServer()
    param_server["BehaviorIDMClassic"]["BrakeForLaneEnd"] = True
    param_server["BehaviorIDMClassic"]["BrakeForLaneEndEnabledDistance"] = 60.0
    param_server["BehaviorIDMClassic"]["BrakeForLaneEndDistanceOffset"] = 30.0
    param_server["BehaviorLaneChangeRuleBased"]["MinRemainingLaneCorridorDistance"] = 80.
    param_server["BehaviorLaneChangeRuleBased"]["MinVehicleRearDistance"] = 0.
    param_server["BehaviorLaneChangeRuleBased"]["MinVehicleFrontDistance"] = 0.
    param_server["BehaviorLaneChangeRuleBased"]["TimeKeepingGap"] = 0.
    param_server["BehaviorMobilRuleBased"]["Politeness"] = 0.0
    param_server["BehaviorIDMClassic"]["DesiredVelocity"] = 10.
    param_server["World"]["FracLateralOffset"] = 0.8

    # configure both lanes of the highway. the right lane has one controlled agent
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
                    map_file_name="barkscape/handlers/data/DR_DEU_Merging_MT_v01_shifted.xodr",
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
      runner=BARKRunner, runnable_object=env, logger=logger)
    bark_server.Start()
