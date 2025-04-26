# ktamv_server/camera.py

import cv2

class Camera:
    def __init__(self):
        self.capture = None
        self.preview_running = False
        self.origin_x = None
        self.origin_y = None
        self.current_x = 42.32  # Simulierter Startwert
        self.current_y = -30.85  # Simulierter Startwert

    def initialize(self):
        # Verbindung zu deinem Crowsnest MJPG-Stream
        self.capture = cv2.VideoCapture("http://192.168.178.110/webcam/?action=stream")

    def start_preview(self):
        self.preview_running = True
        # Hier könnte man erweitern für eine Live-Anzeige

    def stop_preview(self):
        self.preview_running = False
        if self.capture:
            self.capture.release()

    def find_nozzle_center(self):
        if not self.capture or not self.capture.isOpened():
            return {"x_offset": 0.0, "y_offset": 0.0}

        ret, frame = self.capture.read()
        if not ret:
            return {"x_offset": 0.0, "y_offset": 0.0}

        # Simulation: Einfach kleine zufällige Versätze
        self.current_x += 0.05
        self.current_y += 0.03
        return {"x_offset": self.current_x - (self.origin_x or 0), "y_offset": self.current_y - (self.origin_y or 0)}

    def get_focus_score(self):
        if not self.capture or not self.capture.isOpened():
            return 0.0

        ret, frame = self.capture.read()
        if not ret:
            return 0.0

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        focus_score = cv2.Laplacian(gray, cv2.CV_64F).var()
        return focus_score

    # --- Position & Origin Simulation ---
    def get_current_x(self):
        return self.current_x

    def get_current_y(self):
        return self.current_y

    def set_origin(self):
        self.origin_x = self.current_x
        self.origin_y = self.current_y
