package(default_visibility = ["//visibility:public"])
py_library(
  name = "bark_runner",
  srcs = ["bark_runner.py"],
  data = ["@bark_project//bark/python_wrapper:core.so"],
  deps = ["//barkscape/server:bark_xviz_stream",
          "//barkscape/server:base_runner"]
)

py_library(
  name = "bark_ml_runtime_runner",
  srcs = ["bark_ml_runtime_runner.py"],
  data = ["@bark_project//bark/python_wrapper:core.so",
          "@bark_ml_project//bark_ml/python_wrapper:core.so",
          "//barkscape/server:base_runner"],
  imports = ["../bark_ml_project/bark_ml/python_wrapper/",
             "../bark_project/bark_ml/python_wrapper/",
             "../bark_ml_project/bark_ml/"],
  deps = [
    "//barkscape/server:bark_xviz_stream",
    "@bark_ml_project//bark_ml/environments:gym",
  ]
)

py_library(
  name = "bark_ml_runner_runner",
  srcs = ["bark_ml_runner_runner.py"],
  data = ["@bark_project//bark/python_wrapper:core.so",
          "@bark_ml_project//bark_ml/python_wrapper:core.so"],
  imports = ["../bark_ml_project/bark_ml/python_wrapper/",
             "../bark_project/bark_ml/python_wrapper/",
             "../bark_ml_project/bark_ml/"],
  deps = [
    "//barkscape/server:bark_xviz_stream",
    "@bark_ml_project//bark_ml/environments:gym",
    "//barkscape/server:base_runner"
  ]
)
