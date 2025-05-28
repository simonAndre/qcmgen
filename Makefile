
SHELL:=/bin/bash
.ONESHELL:
.PHONY: build publish all owcache

test:
	uv run pytest ./src/tests

build: test
	uv build -o ~/code/local_pypi/ .

owcache: build
	rm -rf  /home/san/.cache/uv/environments-v2/*

all: build

