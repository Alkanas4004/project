# =========================
# Application Settings
# =========================
APP_NAME = "SuperMarket POS System"

APP_VERSION = "2.0 Pro"

COMPANY_NAME = "SuperMarket"
COMPANY_PHONE = "+20XXXXXXXXXX"
COMPANY_ADDRESS = "Egypt"

# =========================
# Window Settings
# =========================
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

INFO_COLOR = "#0EA5E9"

TEXT_COLOR = "#F8FAFC"
TEXT_SECONDARY = "#CBD5E1"

BORDER_COLOR = "#334155"

# =========================
# Fonts
# =========================
FONT_FAMILY = "Segoe UI"

TITLE_FONT = (
    FONT_FAMILY,
    32,
    "bold"
)

SUBTITLE_FONT = (
    FONT_FAMILY,
    22,
    "bold"
)

TEXT_FONT = (
    FONT_FAMILY,
    16
)

BUTTON_FONT = (
    FONT_FAMILY,
    15,
    "bold"
)

SMALL_FONT = (
    FONT_FAMILY,
    13
)

TABLE_FONT = (
    "Consolas",
    14
)

# =========================
# UI Settings
# =========================
BUTTON_RADIUS = 12
FRAME_RADIUS = 18

BUTTON_HEIGHT = 45
ENTRY_HEIGHT = 45

SIDEBAR_WIDTH = 260

TABLE_ROW_HEIGHT = 35

# =========================
# Database
# =========================
DATABASE_FOLDER = "database"
DATABASE_PATH = "database/supermarket.db"

BACKUP_FOLDER = "database/backups"

# =========================
# Default Admin
# =========================
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"

# =========================
# User Roles
# =========================
ROLE_ADMIN = "admin"
ROLE_MANAGER = "manager"
ROLE_CASHIER = "cashier"

# =========================
# Inventory Settings
# =========================
LOW_STOCK_LIMIT = 5

DEFAULT_PRODUCT_CATEGORY = "General"

# =========================
# Sales Settings
# =========================
DEFAULT_PAYMENT_METHOD = "Cash"

TAX_PERCENTAGE = 14
DEFAULT_DISCOUNT = 0

LOYALTY_POINTS_RATE = 1

# =========================
# Invoice Settings
# =========================
INVOICE_FOLDER = "invoices"

INVOICE_PREFIX = "INV"

RECEIPT_WIDTH = 80

# =========================
# Reports Settings
# =========================
REPORTS_FOLDER = "reports"

EXPORT_PDF = True
EXPORT_EXCEL = True

# =========================
# Security Settings
# =========================
PASSWORD_HASH_ROUNDS = 12

SESSION_TIMEOUT = 30  # minutes

# =========================
# Barcode Settings
# =========================
BARCODE_LENGTH = 12

# =========================
# Suppliers
# =========================
DEFAULT_SUPPLIER = "Unknown Supplier"

# =========================
# Customers
# =========================
DEFAULT_CUSTOMER = "Walk-in Customer"

# =========================
# Backup Settings
# =========================
AUTO_BACKUP = True
BACKUP_INTERVAL_DAYS = 7

# =========================
# Logs
# =========================
ENABLE_ACTIVITY_LOGS = True

# =========================
# Supported Payment Methods
# =========================
PAYMENT_METHODS = [
    "Cash",
    "Visa",
    "MasterCard",
    "Wallet"
]

# =========================
# Dashboard Charts
# =========================
ENABLE_ANALYTICS = True

# =========================
# Language
# =========================
DEFAULT_LANGUAGE = "en"
