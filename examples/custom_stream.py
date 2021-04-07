# Copyright (c) 2021 fortiss GmbH
#
# Authors: Julian Bernhard, Klemens Esterle, Patrick Hart and
# Tobias Kessler
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.
import sys, os, logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import xviz_avs
import xviz_avs.builder as xbuilder

# BARK
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
from barkscape.server.bark_xviz_stream import BarkXvizStream
from barkscape.server.runners.bark_runner import BARKRunner

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

# custom stream
class CustomStream(BarkXvizStream):
  def __init__(self, live=True, logger=None):
    super(CustomStream, self).__init__(
      live=live, logger=logger)

  def get_metadata(self):
    if not self._metadata:
      builder = xviz_avs.XVIZMetadataBuilder()
      builder.stream("/vehicle_pose").category(
        xviz_avs.CATEGORY.POSE)
      builder.stream("/ego_vehicle/velocity").category(
        xviz_avs.CATEGORY.TIME_SERIES).type(xviz_avs.SCALAR_TYPE.FLOAT)
      builder.stream("/ego_vehicle/acceleration").category(
        xviz_avs.CATEGORY.TIME_SERIES).type(xviz_avs.SCALAR_TYPE.FLOAT)          
      builder.stream("/map")\
        .coordinate(xviz_avs.COORDINATE_TYPES.IDENTITY)\
        .category(xviz_avs.CATEGORY.PRIMITIVE)\
        .type(xviz_avs.PRIMITIVE_TYPES.POLYLINE)
      builder.stream("/other/lines")\
        .coordinate(xviz_avs.COORDINATE_TYPES.IDENTITY)\
        .category(xviz_avs.CATEGORY.PRIMITIVE)\
        .type(xviz_avs.PRIMITIVE_TYPES.POLYLINE)
      # NOTE: CUSTOM TYPE ADDED HERE!
      builder.stream("/CUSTOM_LINE")\
        .coordinate(xviz_avs.COORDINATE_TYPES.IDENTITY)\
        .category(xviz_avs.CATEGORY.PRIMITIVE)\
        .type(xviz_avs.PRIMITIVE_TYPES.POLYLINE)
      builder.stream("/other/points")\
        .coordinate(xviz_avs.COORDINATE_TYPES.IDENTITY)\
        .category(xviz_avs.CATEGORY.PRIMITIVE)\
        .type(xviz_avs.PRIMITIVE_TYPES.CIRCLE)
      builder.stream("/other/polygons")\
        .coordinate(xviz_avs.COORDINATE_TYPES.IDENTITY)\
        .stream_style({
            'extruded': True,
        })\
        .category(xviz_avs.CATEGORY.PRIMITIVE)\
        .type(xviz_avs.PRIMITIVE_TYPES.POLYGON)
      builder.stream("/other_vehicles")\
        .coordinate(xviz_avs.COORDINATE_TYPES.IDENTITY)\
        .stream_style({
            'extruded': True,
        })\
        .category(xviz_avs.CATEGORY.PRIMITIVE)\
        .type(xviz_avs.PRIMITIVE_TYPES.POLYGON)
      builder.stream("/ego_vehicle/bounding_box")\
        .coordinate(xviz_avs.COORDINATE_TYPES.IDENTITY)\
        .stream_style({
            'extruded': True,
        })\
        .category(xviz_avs.CATEGORY.PRIMITIVE)\
        .type(xviz_avs.PRIMITIVE_TYPES.POLYGON)
      self._metadata = builder.get_message()
    return {
        'type': 'xviz/metadata',
        'data': self._metadata.to_object()
    }
  

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
  custom_stream = CustomStream(logger=logger)
  bark_server = BaseServer(
    runner=BARKRunner, runnable_object=env, logger=logger, stream=custom_stream)
  bark_server.Start()
