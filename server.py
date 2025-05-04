from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
import time

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)

# Server Status Variablen
class ServerState:
    def __init__(self):
        self.preview_active = False
        self.offsets = {
            'tools': {},
            'origin': {'x': 0, 'y': 0},
            'z_offsets': {}
        }
        self.last_response = 200

state = ServerState()

# API-Endpunkte
@app.route('/machine/ktamv_server/start_preview', methods=['POST'])
def start_preview():
    try:
        state.preview_active = True
        state.last_response = 200
        app.logger.info("Kameravorschau gestartet")
        return jsonify({'status': 'preview_started'}), 200
    except Exception as e:
        state.last_response = 500
        return jsonify({'error': str(e)}), 500

@app.route('/machine/ktamv_server/stop_preview', methods=['POST'])
def stop_preview():
    state.preview_active = False
    state.last_response = 200
    app.logger.info("Kameravorschau gestoppt")
    return jsonify({'status': 'preview_stopped'}), 200

@app.route('/machine/ktamv_server/calibrate_camera', methods=['POST'])
def calibrate_camera():
    try:
        # Mock-Kalibrierungslogik
        time.sleep(2)
        state.last_response = 200
        return jsonify({
            'status': 'calibrated',
            'score': 0.95,
            'matrix': [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
        }), 200
    except Exception as e:
        state.last_response = 500
        return jsonify({'error': str(e)}), 500

@app.route('/machine/ktamv_server/set_origin', methods=['POST'])
def set_origin():
    data = request.get_json()
    state.offsets['origin']['x'] = data.get('x', 0)
    state.offsets['origin']['y'] = data.get('y', 0)
    state.last_response = 200
    return jsonify(state.offsets['origin']), 200

@app.route('/machine/ktamv_server/get_offset', methods=['GET'])
def get_offset():
    tool_id = request.args.get('tool', default=0, type=int)
    state.last_response = 200
    return jsonify({
        'tool': tool_id,
        'x': state.offsets['tools'].get(tool_id, 0.0),
        'y': state.offsets['tools'].get(tool_id, 0.0),
        'z': state.offsets['z_offsets'].get(tool_id, 0.0)
    }), 200

@app.route('/machine/ktamv_server/find_nozzle_center', methods=['POST'])
def find_nozzle_center():
    try:
        tool_id = request.json.get('tool', 0)
        # Mock-Erkennungslogik
        state.offsets['tools'][tool_id] = {
            'x': 0.5 + tool_id*0.1,
            'y': -0.3 + tool_id*0.05
        }
        state.last_response = 200
        return jsonify(state.offsets['tools'][tool_id]), 200
    except Exception as e:
        state.last_response = 500
        return jsonify({'error': str(e)}), 500

@app.route('/machine/ktamv_server/zscan_start', methods=['POST'])
def zscan_start():
    try:
        tool_id = request.json.get('tool', 0)
        # Mock-Z-Scan
        state.offsets['z_offsets'][tool_id] = 0.75
        state.last_response = 200
        return jsonify({'z_offset': 0.75}), 200
    except Exception as e:
        state.last_response = 500
        return jsonify({'error': str(e)}), 500

# Status Endpunkt für Klipper
@app.route('/machine/ktamv_server/status', methods=['GET'])
def status():
    return jsonify({
        'preview_active': state.preview_active,
        'last_response': state.last_response,
        'offsets': state.offsets
    }), 200

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        threaded=True,
        debug=True,
        use_reloader=False
    )
