filegroup(
   name="xodr_data",
   srcs=glob(["data/**"]),
   visibility = ["//visibility:public"],
)

py_test(
  name = "bark_example",
  srcs = ["bark_example.py"],
  data = ['@bark_project//bark:generate_core',
          '@bark_project//bark/runtime/tests:xodr_data',
          "//examples:xodr_data"],
  deps = ["@bark_project//bark/runtime/commons:parameters",
          "@bark_project//bark/runtime/commons:xodr_parser",
          "@bark_project//bark/runtime/viewer:pygame_viewer",
          "@bark_project//bark/runtime/viewer:matplotlib_viewer",
          "@bark_project//bark/runtime/viewer:buffered_viewer",
          "@bark_project//bark/runtime/scenario/scenario_generation:scenario_generation",
          "@bark_project//bark/runtime:runtime",
          "//barkscape/server/runners:bark_runner",
          "//barkscape/server:bark_xviz_stream",
          "//barkscape/server:base_server",
          "//barkscape/server:base_handler"],
)

py_test(
  name = "bark_ml_example",
  srcs = ["bark_ml_example.py"],
  data = ['@bark_project//bark:generate_core',
          "@bark_ml_project//bark_ml/python_wrapper:core.so"],
  deps = ["//barkscape/server/runners:bark_ml_runtime_runner",
          "//barkscape/server:bark_xviz_stream",
          "@bark_project//bark/runtime/viewer:buffered_viewer",
          "@bark_ml_project//bark_ml/environments:gym",
          "//barkscape/server:base_server",
          "//barkscape/server:base_handler"],
  imports = ["../bark_ml_project/bark_ml/python_wrapper/",
             "../bark_project/bark_ml/python_wrapper/",
             "../bark_ml_project/bark_ml/"],
)

py_test(
  name = "bark_ml_runner_example",
  srcs = ["bark_ml_runner_example.py"],
  data = ["@bark_project//bark/python_wrapper:core.so",
          "@bark_ml_project//bark_ml/python_wrapper:core.so"],
  imports = ["../bark_ml_project/bark_ml/python_wrapper/",
             "../bark_project/bark_ml/python_wrapper/",
             "../bark_ml_project/bark_ml/"],
  deps = [
    "@bark_ml_project//bark_ml/environments:gym",
    "@bark_ml_project//experiments:experiment_runner",
    "@bark_project//bark/runtime/viewer:buffered_viewer",
    "//barkscape/server/runners:bark_ml_runner_runner",
    "//barkscape/server:bark_xviz_stream",
    "//barkscape/server:base_server",
    "//barkscape/server:base_handler"
  ]
)