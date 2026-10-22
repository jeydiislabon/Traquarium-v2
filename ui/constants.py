"""UI constants -- Aquarium palette (DMC palette from reference image)"""

from PyQt6.QtGui import QFont

# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------
MAIN_FONT     = QFont("Segoe UI", 11)
TITLE_FONT    = QFont("Segoe UI", 22, QFont.Weight.Bold)
SUBTITLE_FONT = QFont("Segoe UI", 13)

# ---------------------------------------------------------------------------
# Aquarium Color Palette
# ---------------------------------------------------------------------------
#  DMC 336  -- Navy Blue          deep background / sidebar base
NAVY          = "#1A2472"
#  DMC 797  -- Royal Blue         panel fills / cards
ROYAL         = "#2255A4"
#  DMC 3837 -- Ultra Dark Lavender  accent / border / selected
LAVENDER      = "#673888"
#  DMC 3607 -- Light Plum         hover / secondary accent
PLUM          = "#C06090"
#  DMC 600  -- Very Dark Cranberry primary button / badge / danger
CRANBERRY     = "#B01040"
#  DMC 150  -- Ultra Very Dark Dusty Rose  deep accent / pressed
DUSTY_ROSE    = "#8B1A3A"

# Surface tones derived from palette
BG_DEEP       = "#0D1545"   # deepest background (darker navy)
BG_PANEL      = "#1A2472"   # main page background
BG_CARD       = "#1E2D6B"   # card surfaces
BG_ELEVATED   = "#243280"   # elevated card / hover state
BORDER_COLOR  = "#3A4A9A"   # card/input borders
BORDER_ACCENT = "#673888"   # focused / selected borders

# Text
TEXT_PRIMARY   = "#FFFFFF"
TEXT_SECONDARY = "#B8C4E8"
TEXT_MUTED     = "#6B7BB0"

# Semantic
SUCCESS_COLOR  = "#22C55E"   # safe NH3
WARNING_COLOR  = "#F59E0B"   # caution
DANGER_COLOR   = "#EF4444"   # critical toxic
INFO_COLOR     = "#A78BFA"   # informational (soft lavender)

# Legacy aliases (keep so older imports don't break)
PRIMARY_COLOR      = ROYAL
ACCENT_COLOR       = LAVENDER
ACCENT_HOVER       = PLUM
LIGHT_COLOR        = TEXT_PRIMARY
BG_GRADIENT_TOP    = BG_PANEL
BG_GRADIENT_BOTTOM = BG_DEEP
CYAN_ACCENT        = INFO_COLOR
