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
