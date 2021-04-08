# BARKSCAPE

![Ubtuntu-CI Build](https://github.com/bark-simulator/barkscape/workflows/CI/badge.svg)

Interactive, web-based, 3D-GUI/visualization for [BARK](https://github.com/bark-simulator/bark) built using [streetscape](https://github.com/uber/streetscape.gl) and [xviz](https://github.com/uber/xviz).
BARKSCAPE provides web-client and server utilities for BARK.


<p align="center">
<img src="utils/barkscape.png" alt="BARKSCAPE" />
</p>


## Getting Started with the Web Interface

First, set up and build the web interface by running the command `bazel run //barkscape/web:run`.
After the JS-bundle has been built, the website should now be accessible at http://127.0.0.1:8080.



## Example Usage of BARK

First install the virtual environment run using `bash utils/install.sh` and enter it using `source utils/dev_into.sh`.

Start the web-interface via `bazel run //barkscape/web:run`

Run a simulation in BARK, e.g. `bazel run //bark/examples:barkscape_example` or test one of the examples in the barkscape repository, e.g. `bazel run //examples:bark_ml_example`. If you only experience a blank screen in the web interface, reload it via Ctrl+R or F5.
