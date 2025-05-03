# ktamv_server/camera.py

import cv2
import numpy as np

class Camera:
    def __init__(self):
        self.capture = None
        self.preview_running = False
        self.origin_x = None
        self.origin_y = None
        self.current_x = 0.0
        self.current_y = 0.0

        # --- Kalibrierwert: mm pro Pixel ---
        self.mm_per_pixel = 0.05  # WICHTIG: Anpassen oder aus KTAMV_CALIB_CAMERA setzen

        # --- Debug ---
        self.debug_mode = True

    def initialize(self):
        # Verbindung zu deinem Crowsnest MJPG-Stream
        self.capture = cv2.VideoCapture("http://192.168.178.110/webcam/?action=stream")

    def start_preview(self):
        self.preview_running = True
        # Optional: könnte später mit Live-Anzeige ergänzt werden

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

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)

        # Kreis-Erkennung
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50,
                                   param1=50, param2=30, minRadius=5, maxRadius=50)

        frame_center_x = frame.shape[1] / 2
        frame_center_y = frame.shape[0] / 2

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            x, y, r = circles[0]  # Nimm den ersten gefundenen Kreis

            self.current_x = (x - frame_center_x) * self.mm_per_pixel
            self.current_y = (y - frame_center_y) * self.mm_per_pixel

            if self.debug_mode:
                # Debug-Ausgabe mit Kreiszeichnung
                debug_frame = frame.copy()
                cv2.circle(debug_frame, (x, y), r, (0, 255, 0), 2)
                cv2.circle(debug_frame, (x, y), 2, (0, 0, 255), 3)
                cv2.line(debug_frame, (int(frame_center_x) - 20, int(frame_center_y)),
                         (int(frame_center_x) + 20, int(frame_center_y)), (255, 0, 0), 2)
                cv2.line(debug_frame, (int(frame_center_x), int(frame_center_y) - 20),
                         (int(frame_center_x), int(frame_center_y) + 20), (255, 0, 0), 2)
                cv2.imshow("Nozzle Detection Debug", debug_frame)
                cv2.waitKey(500)  # 500ms anzeigen

            return {"x_offset": self.current_x - (self.origin_x or 0),
                    "y_offset": self.current_y - (self.origin_y or 0)}
        else:
            if self.debug_mode:
                print("Kein Kreis gefunden!")
            return {"x_offset": 0.0, "y_offset": 0.0}

    def get_focus_score(self):
        if not self.capture or not self.capture.isOpened():
            return 0.0

        ret, frame = self.capture.read()
        if not ret:
            return 0.0

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        focus_score = cv2.Laplacian(gray, cv2.CV_64F).var()
        return focus_score

    # --- Position & Origin ---
    def get_current_x(self):
        return self.current_x

    def get_current_y(self):
        return self.current_y

    def set_origin(self):
        self.origin_x = self.current_x
        self.origin_y = self.current_y
