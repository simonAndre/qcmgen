#!/usr/bin/env -S uv run --script --refresh
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "qcmgen>=0.1.0",
#     "jinja2",
# ]
# [[tool.uv.index]]
# name = "local_pypi"
# url = "/home/san/code/local_pypi"
# format = "flat"
# ///

from qcmgen import main 
main.main()


