"""
Configuration and settings management for the Level Crossing Interface Test app.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any

# =========================
# APP METADATA
# =========================
APP_VERSION = "v1.3.0 (2026-02-11)"
APP_NAME = "Unipart Level Crossing Interface Test"

# =========================
# SIMULATION MODE
# =========================
SIMULATION_MODE = True  # Windows preview True, Raspberry Pi live False

# =========================
# HARDWARE SETTINGS
# =========================
SPLASH_SECONDS = 5
SCRIPT_DIR = Path(__file__).resolve().parent
LOGO_PATH = str(SCRIPT_DIR / "Unipart_RGB_Logo.png")

# GPIO (BCM)
PIN_RAISE = 17
PIN_LOWER = 27
PIN_START_BTN = 22
PIN_STOP_BTN = 23

# LEDs (BCM)
PIN_LED_RAISE = 5
PIN_LED_LOWER = 6

RELAY_ACTIVE_HIGH = True
LED_ACTIVE_HIGH = True

# =========================
# TEMPERATURE SENSORS
# =========================
TEMP_LOG_INTERVAL = 30  # fixed default (seconds)
SENSOR_FAULT_SECONDS = 120  # if ANY probe reads None continuously -> stop

# DS18B20 probe IDs (replace on Pi)
SENSOR_ID_LOC_TOP = "28-000000000000"
SENSOR_ID_LOC_BOTTOM = "28-000000000000"
SENSOR_ID_INV_1 = "28-000000000000"
SENSOR_ID_INV_2 = "28-000000000000"
SENSOR_ID_LOC_EXTERNAL = "28-000000000000"

SENSORS = [
    ("Loc Top Temp", SENSOR_ID_LOC_TOP),
    ("Loc Bottom Temp", SENSOR_ID_LOC_BOTTOM),
    ("Inverter 1 Temp", SENSOR_ID_INV_1),
    ("Inverter 2 Temp", SENSOR_ID_INV_2),
    ("Loc External Temp", SENSOR_ID_LOC_EXTERNAL),
]

DEFAULT_WD_LIMITS = {
    "Loc Top Temp": 60.0,
    "Loc Bottom Temp": 60.0,
    "Inverter 1 Temp": 60.0,
    "Inverter 2 Temp": 60.0,
    "Loc External Temp": 60.0,
}

# =========================
# TIMING OPTIONS
# =========================
STEP_OPTIONS = list(range(1, 181, 1))
DWELL_OPTIONS = [0] + list(range(1, 61, 1))

DEFAULT_RAISE_SECONDS = 1
DEFAULT_LOWER_SECONDS = 1
DEFAULT_DWELL_SECONDS = 0
DEFAULT_MAX_CYCLES = 0
DEFAULT_MAX_MINUTES = 0

# =========================
# SECURITY
# =========================
DEFAULT_SETTINGS_PIN = "1234"
SETTINGS_PIN_HASH = hashlib.sha256(DEFAULT_SETTINGS_PIN.encode("utf-8")).hexdigest()

# =========================
# FILE PATHS
# =========================
BASE_DIR = Path.home() / "level_crossing_test"
LOG_DIR = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "reports"

COUNTS_FILE = Path.home() / ".unipart_lc_interface_counts.json"
SETTINGS_FILE = Path.home() / ".unipart_lc_interface_settings.json"
EMAIL_CONFIG_FILE = Path.home() / ".unipart_lc_interface_email.json"
LOG_FILE = LOG_DIR / "test_log.csv"

# =========================
# UI SETTINGS
# =========================
KIOSK_FULLSCREEN_DEFAULT = False

# =========================
# EMAIL CONFIGURATION
# =========================
DEFAULT_EMAIL_CONFIG = {
    "enabled": False,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "",
    "sender_password": "",
    "recipient_emails": [],
}


def sha256(s: str) -> str:
    """Hash a string using SHA256."""
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


class SettingsManager:
    """Manages application settings persistence."""

    def __init__(self):
        self.watchdog_limits = DEFAULT_WD_LIMITS.copy()
        self.raise_seconds = DEFAULT_RAISE_SECONDS
        self.lower_seconds = DEFAULT_LOWER_SECONDS
        self.dwell_seconds = DEFAULT_DWELL_SECONDS
        self.max_cycles = DEFAULT_MAX_CYCLES
        self.max_minutes = DEFAULT_MAX_MINUTES
        self.operator_name = ""
        self.settings_pin_hash = SETTINGS_PIN_HASH

    def load(self):
        """Load settings from file."""
        self.watchdog_limits = DEFAULT_WD_LIMITS.copy()
        self.raise_seconds = DEFAULT_RAISE_SECONDS
        self.lower_seconds = DEFAULT_LOWER_SECONDS
        self.dwell_seconds = DEFAULT_DWELL_SECONDS
        self.max_cycles = DEFAULT_MAX_CYCLES
        self.max_minutes = DEFAULT_MAX_MINUTES
        self.operator_name = ""
        self.settings_pin_hash = SETTINGS_PIN_HASH

        try:
            if SETTINGS_FILE.exists():
                data = json.loads(SETTINGS_FILE.read_text())

                # Timings
                rs = int(data.get("raise_seconds", DEFAULT_RAISE_SECONDS))
                ls = int(data.get("lower_seconds", DEFAULT_LOWER_SECONDS))
                ds = int(data.get("dwell_seconds", DEFAULT_DWELL_SECONDS))
                self.raise_seconds = rs if rs in STEP_OPTIONS else DEFAULT_RAISE_SECONDS
                self.lower_seconds = ls if ls in STEP_OPTIONS else DEFAULT_LOWER_SECONDS
                self.dwell_seconds = ds if ds in DWELL_OPTIONS else DEFAULT_DWELL_SECONDS

                # Auto-stop
                mc = int(data.get("max_cycles", DEFAULT_MAX_CYCLES))
                mm = int(data.get("max_minutes", DEFAULT_MAX_MINUTES))
                self.max_cycles = mc if mc >= 0 else DEFAULT_MAX_CYCLES
                self.max_minutes = mm if mm >= 0 else DEFAULT_MAX_MINUTES

                # Watchdog limits
                wd = data.get("watchdog_limits", {})
                for k in DEFAULT_WD_LIMITS.keys():
                    if k in wd:
                        try:
                            self.watchdog_limits[k] = float(wd[k])
                        except Exception:
                            self.watchdog_limits[k] = DEFAULT_WD_LIMITS[k]

                # Operator name
                self.operator_name = data.get("operator_name", "").strip()

                # PIN hash
                pin_hash = data.get("settings_pin_hash")
                if pin_hash:
                    self.settings_pin_hash = pin_hash
        except Exception:
            pass

    def save(self):
        """Save settings to file."""
        tmp = SETTINGS_FILE.with_suffix(".tmp")
        tmp.write_text(
            json.dumps(
                {
                    "raise_seconds": self.raise_seconds,
                    "lower_seconds": self.lower_seconds,
                    "dwell_seconds": self.dwell_seconds,
                    "max_cycles": self.max_cycles,
                    "max_minutes": self.max_minutes,
                    "watchdog_limits": self.watchdog_limits,
                    "operator_name": self.operator_name,
                    "settings_pin_hash": self.settings_pin_hash,
                },
                indent=2,
            )
        )
        tmp.replace(SETTINGS_FILE)

    def verify_pin(self, pin: str) -> bool:
        """Verify a PIN against the stored hash."""
        return sha256(pin) == self.settings_pin_hash

    def set_pin(self, new_pin: str):
        """Set a new PIN."""
        self.settings_pin_hash = sha256(new_pin)
        self.save()


class EmailConfigManager:
    """Manages email configuration for alerts."""

    def __init__(self):
        self.config = DEFAULT_EMAIL_CONFIG.copy()

    def load(self):
        """Load email configuration from file."""
        self.config = DEFAULT_EMAIL_CONFIG.copy()
        try:
            if EMAIL_CONFIG_FILE.exists():
                data = json.loads(EMAIL_CONFIG_FILE.read_text())
                self.config.update(data)
        except Exception:
            pass

    def save(self):
        """Save email configuration to file."""
        tmp = EMAIL_CONFIG_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.config, indent=2))
        tmp.replace(EMAIL_CONFIG_FILE)

    def is_enabled(self) -> bool:
        """Check if email alerts are enabled."""
        return self.config.get("enabled", False)

    def get_config(self) -> Dict[str, Any]:
        """Get the full email configuration."""
        return self.config.copy()

    def set_config(self, config: Dict[str, Any]):
        """Set the email configuration."""
        self.config.update(config)
        self.save()

    def validate(self) -> tuple[bool, str]:
        """Validate email configuration."""
        if not self.config.get("enabled"):
            return True, "Email alerts disabled"

        if not self.config.get("smtp_server"):
            return False, "SMTP server not configured"
        if not self.config.get("smtp_port"):
            return False, "SMTP port not configured"
        if not self.config.get("sender_email"):
            return False, "Sender email not configured"
        if not self.config.get("sender_password"):
            return False, "Sender password not configured"
        if not self.config.get("recipient_emails"):
            return False, "No recipient emails configured"

        return True, "Email configuration valid"