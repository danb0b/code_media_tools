#!/bin/bash
MY_PATH="`dirname \"$0\"`"

python3 $MY_PATH/../python/media_tools/video_tools/shrink_videos.py "$@"
