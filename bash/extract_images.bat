@echo off
mkdir images
ffmpeg -i %1 images/image%%03d.png