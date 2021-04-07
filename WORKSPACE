workspace(
    name = "bark_streetscape",
    managed_directories = {"@npm": ["web_interface/node_modules"]}
)


load("//utils:dependencies.bzl", "dependencies")
dependencies()

load("@bark_project//tools:deps.bzl", "bark_dependencies")
bark_dependencies()

load("@com_github_nelhage_rules_boost//:boost/boost.bzl", "boost_deps")
boost_deps()


load("@build_bazel_rules_nodejs//:index.bzl", "yarn_install")
yarn_install(
    # Name this npm so that Bazel Label references look like @npm//package
    name = "npm",
    package_json = "//barkscape/web:package.json",
    yarn_lock = "//barkscape/web:yarn.lock",
)