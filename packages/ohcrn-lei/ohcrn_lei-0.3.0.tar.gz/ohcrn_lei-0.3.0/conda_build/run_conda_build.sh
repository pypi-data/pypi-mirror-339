#!/usr/bin/env bash

mkdir -p recipe
python generate_meta.yaml.py ../pyproject.toml recipe/meta.yaml
cp ../LICENSE ../README.md recipe/
pixi run conda-build recipe
