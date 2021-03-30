py_test(
  name = "bark_xviz_tests",
  srcs = ["bark_xviz_tests.py"],
  data = ['@bark_project//bark:generate_core',
          '@bark_project//bark/runtime/tests:xodr_data',
          "//server:xodr_data"],
  deps = ["@bark_project//bark/runtime/commons:parameters",
          "@bark_project//bark/runtime/commons:xodr_parser",
          "@bark_project//bark/runtime/viewer:pygame_viewer",
          "@bark_project//bark/runtime/viewer:matplotlib_viewer",
          "@bark_project//bark/runtime/viewer:buffered_viewer",
          "@bark_project//bark/runtime/scenario/scenario_generation:scenario_generation",
          "@bark_project//bark/runtime:runtime",
          "//server:bark_runtime_handler",
          "//server:bark_viewer"],
)

py_test(
  name = "bark_ml_xviz_tests",
  srcs = ["bark_ml_xviz_tests.py"],
  data = ['@bark_project//bark:generate_core',
          "@bark_ml_project//bark_ml/python_wrapper:core.so"],
  deps = ["//server:bark_ml_runtime_handler",
          "//server:bark_viewer",
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
    "//server:bark_ml_runner_handler",
    "//server:bark_viewer"
  ]
)