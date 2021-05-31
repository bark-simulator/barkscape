load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository", "new_git_repository")
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def _maybe(repo_rule, name, **kwargs):
  if name not in native.existing_rules():
    repo_rule(name = name, **kwargs)

def dependencies():
  _maybe(
    git_repository,
    name = "bark_project",
    branch = "master",
    remote = "https://github.com/bark-simulator/bark",
  )

  # _maybe(
  #   native.local_repository,
  #   name = "bark_project",
  #   path = "/Users/hart/Development/bark"
  # )

  _maybe(
    git_repository,
    name = "bark_ml_project",
    branch = "master",
    remote = "https://github.com/bark-simulator/bark-ml",
  )
  # _maybe(
  #   native.local_repository,
  #   name = "bark_ml_project",
  #   path = "/Users/hart/Development/bark-ml",
  # )

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

  _maybe(
  git_repository,
  name = "com_github_glog_glog",
  commit = "c5dcae830670bfaea9573fa7b700e862833d14ff",
  remote = "https://github.com/google/glog.git"
  )

  _maybe(
    http_archive,
    name = "build_bazel_rules_nodejs",
    sha256 = "dd7ea7efda7655c218ca707f55c3e1b9c68055a70c31a98f264b3445bc8f4cb1",
    urls = ["https://github.com/bazelbuild/rules_nodejs/releases/download/3.2.3/rules_nodejs-3.2.3.tar.gz"],
  )
