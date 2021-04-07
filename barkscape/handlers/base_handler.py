# Copyright (c) 2021 fortiss GmbH
#
# Authors: Julian Bernhard, Klemens Esterle, Patrick Hart and
# Tobias Kessler
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.


"""BaseHandler for handling XVIZStreams

   Can be viewed as "instructions for what the server
   should do".
"""
class BaseHandler:
  def __init__(self, runnable_object=None, logger=None, runner=None, viewer=None):
    self._runnable_object = runnable_object
    self._logger = logger
    self._runner = runner
    self._viewer = viewer

  def __call__(self, socket, request):
    # TODO: need to infuse socket and request here
    # TODO: might need to use eval
    return self._runner(
      socket, request, runnable_object=self._runnable_object, logger=self._logger, viewer=None)