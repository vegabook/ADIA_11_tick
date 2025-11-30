#!/bin/sh
uv run hdf5_convert.py
uv run barmake.py
uv run qa.py
