@echo off
mkdir images
ffmpeg -i %1 "images/%1-%%03d.png"