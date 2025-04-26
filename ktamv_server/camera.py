import cv2
import threading
import random

class Camera:
    def __init__(self):
        self.capture = None
        self.preview_thread = None
        self.running = False
        self.current_x = 42.32  # Startposition X
        self.current_y = -30.85  # Startposition Y

    def initialize(self):
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            print("Fehler: Kamera konnte nicht geöffnet werden.")

    def start_preview(self):
        if self.capture is None:
            self.initialize()
        if self.running:
            return

        self.running = True
        self.preview_thread = threading.Thread(target=self._preview_loop)
        self.preview_thread.start()

    def stop_preview(self):
        self.running = False
        if self.preview_thread is not None:
            self.preview_thread.join()

    def _preview_loop(self):
        while self.running:
            ret, frame = self.capture.read()
            if ret:
                cv2.imshow("Camera Preview", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        cv2.destroyAllWindows()

    def find_nozzle_center(self):
        self._simulate_position_change()
        return {"x_offset": 0.0, "y_offset": 0.0}

    def get_focus_score(self):
        if self.capture is None:
            self.initialize()
        ret, frame = self.capture.read()
        if not ret:
            return 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()

    def get_current_x(self):
        return self.current_x

    def get_current_y(self):
        return self.current_y

    def _simulate_position_change(self):
        """Simuliere minimale Bewegung bei jedem Nozzle-Find-Aufruf."""
        if self.current_x is None:
            self.current_x = 42.32
        if self.current_y is None:
            self.current_y = -30.85
        self.current_x += random.uniform(-0.05, 0.05)  # ±0.05 mm
        self.current_y += random.uniform(-0.05, 0.05)
