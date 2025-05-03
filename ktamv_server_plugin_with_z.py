
import logging
import asyncio

from .ktamv_server.camera import Camera

class KTAMV:
    def __init__(self, mgr):
        self.camera = Camera()
        self.camera.initialize()
        self._logger = logging.getLogger("ktamv")
        self._printer = mgr.printer

        # Statusvariablen für Objektmodell
        self._origin_x = None
        self._origin_y = None
        self._preview_running = False
        self._last_nozzle_center = {"x_offset": None, "y_offset": None}
        self._focus_score = None
        self._z_offset = None

        # Kommandos registrieren
        mgr.register_command("ktamv.start_preview", self.cmd_start_preview)
        mgr.register_command("ktamv.stop_preview", self.cmd_stop_preview)
        mgr.register_command("ktamv.find_nozzle_center", self.cmd_find_nozzle_center)
        mgr.register_command("ktamv.set_origin", self.cmd_set_origin)
        mgr.register_command("ktamv.get_offset", self.cmd_get_offset)
        mgr.register_command("ktamv.get_focus_score", self.cmd_get_focus_score)

        mgr.register_command("ktamv.set_z_offset_from_focus", self.cmd_set_z_offset_from_focus)

        # Objektmodell registrieren
        mgr.register_object("ktamv", self)

    def get_status(self, session):
        return {
            "preview_running": self._preview_running,
            "origin_x": self._origin_x,
            "origin_y": self._origin_y,
            "x_offset": self._last_nozzle_center["x_offset"],
            "y_offset": self._last_nozzle_center["y_offset"],
            "focus_score": self._focus_score,
            "z_offset": self._z_offset
        }

    async def cmd_start_preview(self, params):
        self.camera.start_preview()
        self._preview_running = True
        self._logger.info("Preview gestartet.")

    async def cmd_stop_preview(self, params):
        self.camera.stop_preview()
        self._preview_running = False
        self._logger.info("Preview gestoppt.")

    async def cmd_find_nozzle_center(self, params):
        offset = self.camera.find_nozzle_center()
        self._last_nozzle_center = offset
        self._logger.info(f"Nozzle Center gefunden: {offset}")

    async def cmd_set_origin(self, params):
        self._origin_x = self.camera.get_current_x()
        self._origin_y = self.camera.get_current_y()
        self._logger.info(f"Origin gesetzt: X={self._origin_x} Y={self._origin_y}")

    async def cmd_get_offset(self, params):
        if self._origin_x is None or self._origin_y is None:
            raise Exception("Origin wurde noch nicht gesetzt.")
        offset_x = self.camera.get_current_x() - self._origin_x
        offset_y = self.camera.get_current_y() - self._origin_y
        self._last_nozzle_center = {"x_offset": offset_x, "y_offset": offset_y}
        self._logger.info(f"Offset: X={offset_x}, Y={offset_y}")

    async def cmd_get_focus_score(self, params):
        score = self.camera.get_focus_score()
        self._focus_score = score
        self._logger.info(f"Fokus Score: {score}")


    async def cmd_set_z_offset_from_focus(self, params):
        # Hier definierst du, wie aus dem Fokus-Score der Z-Offset berechnet wird
        score = self.camera.get_focus_score()
        # Beispiel: einfacher Zusammenhang (du kannst hier deine Logik einsetzen)
        self._z_offset = 5.0 - (score * 0.1)
        self._logger.info(f"Z-Offset aus Fokus berechnet: {self._z_offset}")


def load_component(config):
    return KTAMV(config)
