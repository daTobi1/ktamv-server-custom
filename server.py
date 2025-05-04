from flask import Flask, request, jsonify, render_template
from ktamv_server.camera import Camera

app = Flask(__name__)
camera = Camera()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_preview', methods=['POST'])
def start_preview():
    camera.start_preview()
    return jsonify({'status': 'preview started'})

@app.route('/stop_preview', methods=['POST'])
def stop_preview():
    camera.stop_preview()
    return jsonify({'status': 'preview stopped'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)