package(default_visibility = ["//visibility:public"])

filegroup(
   name="xodr_data",
   srcs=glob(["data/**"]),
   visibility = ["//visibility:public"],
)

py_library(
  name = "bark_viewer",
  srcs = ["bark_viewer.py"],
  data = ["@bark_project//bark:generate_core"],
  deps = []
)

py_binary(
  name = "bark_runtime_handler",
  srcs = ["bark_runtime_handler.py"],
  data = ["@bark_project//bark/python_wrapper:core.so"],
  deps = ["//server:bark_viewer"]
)

py_binary(
  name = "bark_ml_runtime_handler",
  srcs = ["bark_ml_runtime_handler.py"],
  data = ["@bark_project//bark/python_wrapper:core.so",
          "@bark_ml_project//bark_ml/python_wrapper:core.so"],
  imports = ["../bark_ml_project/bark_ml/python_wrapper/",
             "../bark_project/bark_ml/python_wrapper/",
             "../bark_ml_project/bark_ml/"],
  deps = [
    "//server:bark_viewer",
    "@bark_ml_project//bark_ml/environments:gym",
  ]
)

py_binary(
  name = "bark_ml_runner_handler",
  srcs = ["bark_ml_runner_handler.py"],
  data = ["@bark_project//bark/python_wrapper:core.so",
          "@bark_ml_project//bark_ml/python_wrapper:core.so"],
  imports = ["../bark_ml_project/bark_ml/python_wrapper/",
             "../bark_project/bark_ml/python_wrapper/",
             "../bark_ml_project/bark_ml/"],
  deps = [
    "//server:bark_viewer",
    "@bark_ml_project//bark_ml/environments:gym"
  ]
)
