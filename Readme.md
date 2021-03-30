# BARKSCAPE

A web-visualization for BARK built using [streetscape](https://github.com/uber/streetscape.gl) and [xviz](https://github.com/uber/xviz).

<p align="center">
<img src="utils/barkscape.png" alt="BARKSCAPE" />
</p>


## Install, Build and Run Web-Interface

`cd web_interface`

`yarn`

`yarn start-live-local`

## Install Python Environment

`bash utils/install.sh`

`source utils/dev_into.sh`

## Run BARK

`bazel run //tests:bark_runtime_tests`


## Run BARK-ML

`bazel run //tests:bark_ml_runner_tests`