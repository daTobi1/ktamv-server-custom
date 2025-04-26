# kTAMV Server + Klipper Integration

Eine leistungsstarke, automatisierte Lösung zur Nozzle- und Tool-Offset-Kalibrierung für Toolchanger-Drucker 🛠️🔬

---

## 🔄 Voraussetzungen
- **kTAMV-Server** läuft separat auf einem Proxmox LXC oder anderem Server.
- **Moonraker** ist richtig konfiguriert, damit Klipper die kTAMV-API ansprechen kann.
- **Kamera** über CrowNest oder direkt am Klipper angebunden (MJPG Stream erreichbar).


---

## 🔍 Verzeichnisstruktur

```
macros/
 |- ktamv_config.cfg   # Nur Konfigurationsdaten
 |- ktamv_macros.cfg   # Alle Automatisierungs-Makros
```

In **printer.cfg** einbinden:
```ini
[include macros/ktamv_config.cfg]
[include macros/ktamv_macros.cfg]
```

---

## 🏢 Konfiguration (ktamv_config.cfg)

| Bereich            | Beschreibung                                  |
|--------------------|------------------------------------------------|
| _KTAMV_SERVER      | URL deines kTAMV-Servers                       |
| _KTAMV_TRAVEL      | Kamerafahrgeschwindigkeit (mm/min)             |
| _KTAMV_ORIGIN      | Kamera-Zentrumkoordinaten (X/Y)                |
| _KTAMV_TOOLS       | Liste der zu kalibrierenden Tools              |
| _KTAMV_TIMEOUT     | API-Timeout in Sekunden                       |
| _KTAMV_Z_SCAN_SETTINGS | Start, Ende, Schrittweite und Fokusgrenzwert |

---

## 🧰 Wichtige Makros (ktamv_macros.cfg)

| Makro                     | Beschreibung                           |
|----------------------------|----------------------------------------|
| KTAMV_START_PREVIEW        | Startet das Kamerabild (Vorschau)       |
| KTAMV_STOP_PREVIEW         | Stoppt die Kameravorschau              |
| KTAMV_CALIB_CAMERA         | Kalibriert Kamera (mm/px)              |
| KTAMV_SET_ORIGIN           | Setzt Düsenmittelpunkt als Kamera-Zentrum |
| KTAMV_ALIGN_TOOL TOOL=ID   | Kalibriert Offset eines einzelnen Tools |
| KTAMV_FULL_AUTOCALIBRATE_XY| Komplettkalibrierung (nur XY)          |
| KTAMV_FULL_AUTOCALIBRATE_XYZ| Komplettkalibrierung (XY + Z-Offset)    |

**Beispiel: Vollkalibrierung starten:**
```gcode
KTAMV_FULL_AUTOCALIBRATE_XYZ
```

---

## 🧙️‍♂️ Workflow für Vollautomatische Kalibrierung

1. Home Drucker (**G28**)
2. 📍 Starte Makro `KTAMV_FULL_AUTOCALIBRATE_XYZ`
3. 🔍 Kamera wird kalibriert (falls notwendig)
4. 🔖 Origin (Nullpunkt) wird gesetzt
5. 🔄 Alle Tools werden auf T0 kalibriert
6. 🔬 Z-Offset wird für jedes Tool automatisch ermittelt (falls gewünscht)
7. 🟢 Status-LED blinkt grün bei Erfolg!

---

## 📈 Erweiterte Funktionen (coming soon)
- Manuelle Justierung der Kamera 🎥 via Webinterface
- Z-Offset Optimierung mit Fokusgrenzwert
- Speichern der Ergebnisse in separater Datei


---

## 📊 Sonstiges
- T0 wird immer als **Referenz-Tool** genutzt.
- Alle anderen Tools werden relativ zu T0 eingemessen.
- Kameraauflösung optimieren für bessere Ergebnisse!

---

## 💪 Viel Spaß beim Kalibrieren und Happy Printing!

---

> Maintainer: **daTobi1** & ChatGPT

