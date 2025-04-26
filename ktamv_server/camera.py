# camera.py
import cv2

class Camera:
    def __init__(self):
        self.capture = None
        self.preview_running = False
        self.simulated_x = 42.32
        self.simulated_y = -30.85

    def initialize(self):
        self.capture = cv2.VideoCapture(0)

    def start_preview(self):
        if not self.preview_running:
            self.preview_running = True
            threading.Thread(target=self._preview_loop, daemon=True).start()

    def stop_preview(self):
        self.preview_running = False

    def _preview_loop(self):
        while self.preview_running:
            ret, frame = self.capture.read()
            if ret:
                cv2.imshow('Preview', frame)
                if cv2.waitKey(1) == 27:
                    break
        cv2.destroyAllWindows()

    def find_nozzle_center(self):
        # Simulation der Düse in der Mitte
        return {"x_offset": 0.0, "y_offset": 0.0}

    def get_focus_score(self):
        ret, frame = self.capture.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            fm = cv2.Laplacian(gray, cv2.CV_64F).var()
            return fm
        return 0.0

    def get_current_x(self):
        return self.simulated_x

    def get_current_y(self):
        return self.simulated_y

    def move_relative(self, dx, dy):
        self.simulated_x += dx
        self.simulated_y += dy
