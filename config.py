# config.py

# =========================
# Application Settings
# =========================

APP_NAME = "SuperMarket POS System"

# Window Settings
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900

MIN_WIDTH = 1200
MIN_HEIGHT = 700

# =========================
# Theme Settings
# =========================

APPEARANCE_MODE = "dark"
COLOR_THEME = "blue"

# =========================
# Professional Color Palette
# =========================

PRIMARY_COLOR = "#2563EB"
PRIMARY_HOVER = "#1D4ED8"
SECONDARY_COLOR = "#1E293B"

BACKGROUND_COLOR = "#0F172A"
SIDEBAR_COLOR = "#111827"
CARD_COLOR = "#1E293B"

SUCCESS_COLOR = "#22C55E"
DANGER_COLOR = "#EF4444"
WARNING_COLOR = "#F59E0B"

TEXT_COLOR = "#F8FAFC"
TEXT_SECONDARY = "#CBD5E1"

BORDER_COLOR = "#334155"

# =========================
# Fonts
# =========================

FONT_FAMILY = "Segoe UI"

TITLE_FONT = (FONT_FAMILY, 32, "bold")
SUBTITLE_FONT = (FONT_FAMILY, 22, "bold")

TEXT_FONT = (FONT_FAMILY, 16)
BUTTON_FONT = (FONT_FAMILY, 15, "bold")

SMALL_FONT = (FONT_FAMILY, 13)

# =========================
# UI Settings
# =========================

BUTTON_RADIUS = 12
FRAME_RADIUS = 18

BUTTON_HEIGHT = 45
ENTRY_HEIGHT = 45

SIDEBAR_WIDTH = 260

# =========================
# Database
# =========================

DATABASE_PATH = "database/supermarket.db"

# =========================
# Default Admin
# =========================

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"

# =========================
# Low Stock Alert
# =========================

LOW_STOCK_LIMIT = 5
