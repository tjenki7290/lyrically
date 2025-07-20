#!/bin/bash

# Install FFmpeg (required for yt-dlp audio processing)
apt-get update
apt-get install -y ffmpeg

# Install Python dependencies
pip install -r requirements.txt 