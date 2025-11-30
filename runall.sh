#!/bin/sh
if [[ ! -f ./data/hdf5/ES.h5 ]] ; then
    echo 'File "./data/hdf5/ES.h5" not found'
    exit
fi

uv run hdf5_convert.py
uv run barmake.py
uv run qa.py
