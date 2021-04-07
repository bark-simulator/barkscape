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

To run and visualize BARK in the web-interface (started with `bazel run //barkscape/web:run`) run, e.g., `bazel run //examples:bark_example`. Note: Both commands need to be run at the same time.
