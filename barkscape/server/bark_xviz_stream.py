# Copyright (c) 2021 fortiss GmbH
#
# Authors: Julian Bernhard, Klemens Esterle, Patrick Hart and
# Tobias Kessler
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import math
import json
import numpy as np
import xviz_avs
import xviz_avs.builder as xbuilder

# BARK
from bark.core.world.opendrive import *


class BarkXvizStream:
  def __init__(self, live=True, logger=None):
    self._metadata = None

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

  # TODO: add 3d lines
  async def get_message(self, t, runtime):
    world = runtime._world
    timestamp = world.time
    builder = xviz_avs.XVIZBuilder(metadata=self._metadata)
    for type_name, primitives in world.renderer.primitives.items():
      if type_name == "EGO_AGENT_STATE":
        await self.ProcessEgoState(builder, primitives, timestamp)
      elif type_name == "MAP_LINE":
        await self.DrawLines(
          builder, primitives, timestamp, channel="/map")
      elif type_name == "EGO_AGENT":
        await self.DrawPolygons(
          builder, primitives, timestamp, channel="/ego_vehicle/bounding_box")
      elif type_name == "OTHER_AGENT":
        await self.DrawPolygons(
          builder, primitives, timestamp, channel="/other_vehicles")
      elif type_name == "LINES":
        await self.DrawLines(
          builder, primitives, timestamp, channel="/other/lines")
      elif type_name == "POINTS":
        await self.DrawPoints(
          builder, primitives, timestamp, channel="/other/points")
      elif type_name == "POLYGONS":
        await self.DrawPolygons(
          builder, primitives, timestamp, channel="/other/polygons")
    data = builder.get_message()
    return {
        'type': 'xviz/state_update',
        'data': data.to_object()
    }
        
  async def ProcessEgoState(self, builder, primitives, timestamp):
    ego_state = primitives[-1].object
    builder.pose()\
      .timestamp(timestamp)\
      .orientation(0, 0, 0)\
      .map_origin(11.58, 48.13, 0.)\
      .position(ego_state[1], ego_state[2], 0)
    builder.time_series('/ego_vehicle/velocity')\
      .timestamp(timestamp)\
      .value(ego_state[4])

  async def DrawLines(self, builder, primitives, timestamp, channel):
    for primitive in primitives:
      np_pts = primitive.object.ToArray()
      zeros = np.zeros((np_pts.shape[0], 1))
      np_pts = np.hstack((np_pts, zeros))
      np_re_pts = list(np_pts.reshape(-1))
      builder.primitive(channel)\
        .polyline(np_re_pts)\
        .style(dict(primitive.conf))
  
  async def DrawPolygons(self, builder, primitives, timestamp, channel):
    for primitive in primitives:
      np_poly = primitive.object.ToArray()
      z_cord = np.zeros((np_poly.shape[0], 1))
      np_poly = np.hstack((np_poly, z_cord))
      np_poly_pts_list = list(np_poly.reshape(-1))
      builder.primitive(channel).polygon(
          np_poly_pts_list
      ).classes(['Unknown'])\
        .style({
          "height": primitive.conf["height"],
          "stroke_color": primitive.conf["stroke_color"],
          "fill_color": primitive.conf["fill_color"]})

  async def DrawPoints(self, builder, primitives, timestamp, channel):
    for primitive in primitives:
      builder.primitive('/other/points')\
        .circle([primitive.object.x(), primitive.object.y(), 0.],
                 primitive.conf["radius_pixels"])\
        .style({"fill_color": primitive.conf["fill_color"],
                "stroke_color": primitive.conf["stroke_color"]})