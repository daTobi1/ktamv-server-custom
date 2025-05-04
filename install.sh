#!/bin/bash

cd ktamv_server

echo "Installing dependencies..."
pip install flask opencv-python numpy

echo "Starting server..."
python3 server.py
