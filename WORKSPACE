workspace(name = "bark_streetscape")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

load("//utils:dependencies.bzl", "dependencies")
dependencies()

load("@bark_project//tools:deps.bzl", "bark_dependencies")
bark_dependencies()

load("@com_github_nelhage_rules_boost//:boost/boost.bzl", "boost_deps")
boost_deps()
