#!/bin/bash
MY_PATH="`dirname \"$0\"`"

python3 $MY_PATH/../python/image_tools/scale_pics.py "$@"
