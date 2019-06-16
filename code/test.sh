#!/usr/bin/env bash
BASEDIR=$(dirname "$0")

export PYTHONPATH="${PYTHONPATH}:${BASEDIR}"
mypy --strict -p simulation