load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository", "new_git_repository")
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def _maybe(repo_rule, name, **kwargs):
  if name not in native.existing_rules():
    repo_rule(name = name, **kwargs)

def dependencies():
  # _maybe(
  #   git_repository,
  #   name = "bark_project",
  #   branch = "master",
  #   remote = "https://github.com/bark-simulator/bark",
  # )
  _maybe(
    native.local_repository,
    name = "bark_project",
    path = "/Users/hart/Development/bark"
  )

  # _maybe(
  #   git_repository,
  #   name = "bark_ml_project",
  #   branch = "master",
  #   remote = "https://github.com/bark-simulator/bark-ml",
  # )
  _maybe(
    native.local_repository,
    name = "bark_ml_project",
    path = "/Users/hart/Development/bark-ml",
  )

  _maybe(
    native.new_local_repository,
    name = "python_linux",
    path = "./utils/venv/",
    build_file_content = """
cc_library(
    name = "python-lib",
    srcs = glob(["lib/libpython3.*", "libs/python3.lib", "libs/python36.lib"]),
    hdrs = glob(["include/**/*.h", "include/*.h"]),
    includes = ["include/python3.6m", "include", "include/python3.7m", "include/python3.5m"], 
    visibility = ["//visibility:public"],
)
    """)

  # if we include glog twice, gflags are defined mult. times
  _maybe(
    new_git_repository,
    name = "com_github_google_glog",
    commit = "195d416e3b1c8dc06980439f6acd3ebd40b6b820",
    remote = "https://github.com/google/glog",
    build_file="//:utils/glog.BUILD"
  )
