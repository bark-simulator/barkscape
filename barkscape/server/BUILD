package(default_visibility = ["//visibility:public"])

py_library(
  name = "base_server",
  srcs = ["base_server.py"],
  data = [],
  deps = ["//barkscape/server:base_handler"]
)

py_library(
  name = "base_runner",
  srcs = ["base_runner.py"],
  data = [],
  deps = ["//barkscape/server:bark_xviz_stream"]
)

py_library(
  name = "base_handler",
  srcs = ["base_handler.py"],
  data = [],
  deps = []
)

py_library(
  name = "bark_xviz_stream",
  srcs = ["bark_xviz_stream.py"],
  data = ["@bark_project//bark:generate_core"],
  deps = []
)