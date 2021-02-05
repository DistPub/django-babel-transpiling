#!/usr/bin/env bash
python3 setup.py sdist bdist_wheel
rm -rf build
rm -rf django_babel_transpiling.egg-info