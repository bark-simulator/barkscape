package(default_visibility = ["//visibility:public"])
load("@npm//http-server:index.bzl", "http_server")
load("@npm//webpack-cli:index.bzl", webpack = "webpack_cli")

webpack(
    name = "bundle",
    outs = ["app.bundle.js"],
    args = [
        "web_interface/src/app.js",
        "--config",
        "web_interface/webpack.config.js",
        "-o",
        "$@",
    ],
    data = [
        "index.html",
        "src/app.js",
        "src/constants.js",
        "src/log-from-live.js",
        "src/log-from-file.js",
        "src/log-from-stream.js",
        "webpack.config.js",
        "@npm//:node_modules",
    ],
)

# Note, on Windows you need `--enable_runfiles`
http_server(
    name = "server",
    data = [
        "app.bundle.js",
        "index.html",
        "assets/bark_logo_head.png",
    ],
    templated_args = ["./web_interface"],
)