#!/bin/bash
virtualenv -p python3.7 ./utils/venv
source ./utils/venv/bin/activate && pip install --no-cache-dir --upgrade --trusted-host pypi.org -r ./utils/requirements.txt 