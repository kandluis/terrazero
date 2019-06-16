#!/usr/bin/env bash
BASEDIR=$(dirname "$0")

# Set the python path to contain our directory as a module.
export PYTHONPATH="${PYTHONPATH}:${BASEDIR}"

# Check type annotations.
mypy --strict -p simulation

# Run all tests.
python -m unittest discover --pattern="*_test.py"