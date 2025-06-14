
SHELL:=/bin/bash
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))
PYTHON_BIN := uv run python
.ONESHELL:
.PHONY: build publish all owcache
PYTHON_RUN := $(PYTHON_BIN)
PYTHON_DEBUG := $(PYTHON_BIN) -m debugpy --listen 127.0.0.1:5678 --wait-for-client 

test:
	$(PYTHON_RUN) -m pytest ./tests

testd:
	$(PYTHON_DEBUG) -m pytest ./tests

build:
	uv build -o ~/code/local_pypi/ .

owcache: build
	rm -rf  /home/san/.cache/uv/environments-v2/*

all: build

