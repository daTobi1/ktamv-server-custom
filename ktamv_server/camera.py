# ktamv_server/camera.py

import random
import time

class Camera:
    def __init__(self):
        self.preview_running = False
        self.current_x = 42.32
        self.current_y = -30.85
        self.origin_x = None
        self.origin_y = None

    def initialize(self):
        print("[kTAMV] Kamera-Server initialisiert.")

    def start_preview(self):
        if not self.preview_running:
            self.preview_running = True
            print("[kTAMV] Kamera-Vorschau gestartet.")

    def stop_preview(self):
        if self.preview_running:
            self.preview_running = False
            print("[kTAMV] Kamera-Vorschau gestoppt.")

    def find_nozzle_center(self):
        self._simulate_position_change()
        print(f"[kTAMV] Aktuelle simulierte Position: X={self.current_x:.3f} Y={self.current_y:.3f}")
        return {"x_offset": 0.0, "y_offset": 0.0}

    def get_focus_score(self):
        focus_score = random.uniform(0.8, 1.0)
        print(f"[kTAMV] Aktueller Focus-Score: {focus_score:.3f}")
        return focus_score

    def set_origin(self):
        self.origin_x = self.current_x
        self.origin_y = self.current_y
        print(f"[kTAMV] Ursprung gesetzt auf X={self.origin_x:.3f} Y={self.origin_y:.3f}")

    def get_offset(self):
        if self.origin_x is None or self.origin_y is None:
            raise ValueError("[kTAMV] Ursprung nicht gesetzt.")
        offset_x = self.current_x - self.origin_x
        offset_y = self.current_y - self.origin_y
        print(f"[kTAMV] Offset berechnet: X={offset_x:.3f} Y={offset_y:.3f}")
        return {"x_offset": offset_x, "y_offset": offset_y}

    def get_current_x(self):
        return self.current_x

    def get_current_y(self):
        return self.current_y

    def _simulate_position_change(self):
        # Simuliert eine minimale Veränderung der aktuellen Position (0.001 bis 0.01mm)
        delta_x = random.uniform(-0.01, 0.01)
        delta_y = random.uniform(-0.01, 0.01)
        self.current_x += delta_x
        self.current_y += delta_y
