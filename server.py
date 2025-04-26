# server.py
from ktamv_server.camera import Camera
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)
camera = Camera()

@app.route('/start_preview', methods=['POST'])
def start_preview():
    camera.start_preview()
    return jsonify({'status': 'preview started'})

@app.route('/stop_preview', methods=['POST'])
def stop_preview():
    camera.stop_preview()
    return jsonify({'status': 'preview stopped'})

@app.route('/find_nozzle_center', methods=['POST'])
def find_nozzle_center():
    offset = camera.find_nozzle_center()
    return jsonify(offset)

@app.route('/get_focus_score', methods=['GET'])
def get_focus_score():
    focus_score = camera.get_focus_score()
    return jsonify({'focus_score': focus_score})

if __name__ == "__main__":
    camera.initialize()
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
