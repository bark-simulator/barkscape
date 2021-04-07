py_test(
  name = "bark_tests",
  srcs = ["bark_tests.py"],
  data = ['@bark_project//bark:generate_core',
          '@bark_project//bark/runtime/tests:xodr_data',
          "//barkscape/handlers:xodr_data"],
  deps = ["@bark_project//bark/runtime/commons:parameters",
          "@bark_project//bark/runtime/commons:xodr_parser",
          "@bark_project//bark/runtime/viewer:pygame_viewer",
          "@bark_project//bark/runtime/viewer:matplotlib_viewer",
          "@bark_project//bark/runtime/viewer:buffered_viewer",
          "@bark_project//bark/runtime/scenario/scenario_generation:scenario_generation",
          "@bark_project//bark/runtime:runtime",
          "//barkscape/handlers:bark_runtime_handler",
          "//barkscape/handlers:bark_xviz_stream",
          "//barkscape/handlers:base_server",
          "//barkscape/handlers:base_handler"],
)

py_test(
  name = "bark_ml_tests",
  srcs = ["bark_ml_tests.py"],
  data = ['@bark_project//bark:generate_core',
          "@bark_ml_project//bark_ml/python_wrapper:core.so"],
  deps = ["//barkscape/handlers:bark_ml_runtime_handler",
          "//barkscape/handlers:bark_xviz_stream",
          "@bark_project//bark/runtime/viewer:buffered_viewer",
          "@bark_ml_project//bark_ml/environments:gym"],
  imports = ["../bark_ml_project/bark_ml/python_wrapper/",
             "../bark_project/bark_ml/python_wrapper/",
             "../bark_ml_project/bark_ml/"],
)

py_binary(
  name = "bark_ml_runner_tests",
  srcs = ["bark_ml_runner_tests.py"],
  data = ["@bark_project//bark/python_wrapper:core.so",
          "@bark_ml_project//bark_ml/python_wrapper:core.so"],
  imports = ["../bark_ml_project/bark_ml/python_wrapper/",
             "../bark_project/bark_ml/python_wrapper/",
             "../bark_ml_project/bark_ml/"],
  deps = [
    "@bark_ml_project//bark_ml/environments:gym",
    "@bark_ml_project//experiments:experiment_runner",
    "@bark_project//bark/runtime/viewer:buffered_viewer",
    "//barkscape/handlers:bark_ml_runner_handler",
    "//barkscape/handlers:bark_xviz_stream"
  ]
)