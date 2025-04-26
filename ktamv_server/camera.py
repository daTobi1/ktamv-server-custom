# camera.py
import cv2
import numpy as np
from ktamv_server.focus_detection import calculate_focus

class Camera:
    def __init__(self):
        self.cap = None

    def initialize(self):
        self.cap = cv2.VideoCapture(0)

    def start_preview(self):
        if not self.cap.isOpened():
            self.initialize()
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            cv2.imshow('Preview', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.stop_preview()

    def stop_preview(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

    def find_nozzle_center(self):
        # Beispiel (Dummy) Offset
        return {'x_offset': 0.0, 'y_offset': 0.0}

    def get_focus_score(self):
        ret, frame = self.cap.read()
        if not ret:
            return -1
        return calculate_focus(frame)

# Dummy-Position für Tests
import random

class Camera:
    def __init__(self):
        self.preview_running = False
        self.current_x = 42.32
        self.current_y = -30.85

    def initialize(self):
        pass

    def start_preview(self):
        self.preview_running = True

    def stop_preview(self):
        self.preview_running = False

    def find_nozzle_center(self):
        # Hier würdest du echtes Bildverarbeitungs-Offset berechnen
        return {"x_offset": 0.0, "y_offset": 0.0}

    def get_focus_score(self):
        # Einfacher Dummy-Fokuswert
        return random.uniform(0, 100)

    def get_current_x(self):
        # Gib aktuelle Dummy-X-Position zurück
        return self.current_x

    def get_current_y(self):
        # Gib aktuelle Dummy-Y-Position zurück
        return self.current_y
