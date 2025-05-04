from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/get_frame', methods=['POST'])
def get_frame():
    # Dummy frame-Rückgabe
    return jsonify({"frame": "dummy"})

@app.route('/detect_nozzle', methods=['POST'])
def detect_nozzle():
    return jsonify({"offset_x": 0.0, "offset_y": 0.0})

@app.route('/set_origin', methods=['POST'])
def set_origin():
    return jsonify({"status": "origin set"})

@app.route('/get_offset', methods=['POST'])
def get_offset():
    return jsonify({"offset_x": 0.0, "offset_y": 0.0})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085)
