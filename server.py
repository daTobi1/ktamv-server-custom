from flask import Flask, request, jsonify, render_template
from ktamv_server.camera import Camera

app = Flask(__name__)
camera = Camera()

# ================== Klipper-API-Endpunkte ==================
@app.route('/machine/ktamv_server/start_preview', methods=['POST'])
def start_preview():
    camera.start_preview()
    return jsonify({'status': 'preview_started'})

@app.route('/machine/ktamv_server/stop_preview', methods=['POST'])
def stop_preview():
    camera.stop_preview()
    return jsonify({'status': 'preview_stopped'})

@app.route('/machine/ktamv_server/calibrate_camera', methods=['POST'])
def calibrate_camera():
    # Füge hier Kalibrierungslogik ein
    return jsonify({'status': 'calibrated', 'score': 0.95})

@app.route('/machine/ktamv_server/set_origin', methods=['POST'])
def set_origin():
    # Ursprung setzen
    return jsonify({'status': 'origin_set'})

@app.route('/machine/ktamv_server/get_offset', methods=['GET'])
def get_offset():
    # Mock-Daten (durch echte Logik ersetzen)
    return jsonify({'x': 0.0, 'y': 0.0, 'z': 0.0})

# ================== Web-UI ==================
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
