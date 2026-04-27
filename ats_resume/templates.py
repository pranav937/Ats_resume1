from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

TEMPLATES = {
    # ---------------------------------------------------------
    # 1. Eclipse (Modern & Professional - Left Aligned)
    # ---------------------------------------------------------
    "Eclipse": {
        "primary_color": colors.HexColor("#2C3E50"),  # Dark Navy Blue
        "alignment": TA_LEFT,
        "header_bg": None
    },

    # ---------------------------------------------------------
    # 2. Astralis (Creative & Bold - Center Aligned)
    # ---------------------------------------------------------
    "Astralis": {
        "primary_color": colors.HexColor("#8E44AD"),  # Deep Purple
        "alignment": TA_CENTER,
        "header_bg": None
    },

    # ---------------------------------------------------------
    # 3. Orbit (Sleek & Technical - Left Aligned with Tint)
    # ---------------------------------------------------------
    "Orbit": {
        "primary_color": colors.HexColor("#2980B9"),  # Bright Blue
        "alignment": TA_LEFT,
        "header_bg": colors.HexColor("#ECF0F1")       # Light grey background for headers
    },

    # ---------------------------------------------------------
    # 4. Comet (Warm & Energetic - Left Aligned)
    # ---------------------------------------------------------
    "Comet": {
        "primary_color": colors.HexColor("#D35400"),  # Burnt Orange
        "alignment": TA_LEFT,
        "header_bg": None
    },

    # ---------------------------------------------------------
    # 5. Solstice (Nature & Balanced - Center Aligned)
    # ---------------------------------------------------------
    "Solstice": {
        "primary_color": colors.HexColor("#27AE60"),  # Emerald Green
        "alignment": TA_CENTER,
        "header_bg": None
    },

    # ---------------------------------------------------------
    # 6. Pulsar (High Impact & Striking - Center Aligned)
    # ---------------------------------------------------------
    "Pulsar": {
        "primary_color": colors.HexColor("#C0392B"),  # Strong Red
        "alignment": TA_CENTER,
        "header_bg": colors.HexColor("#F9EBEA")       # Light red background for headers
    },

    # ---------------------------------------------------------
    # 7. Quasar (Tech-Focused - Left Aligned)
    # ---------------------------------------------------------
    "Quasar": {
        "primary_color": colors.HexColor("#16A085"),  # Teal
        "alignment": TA_LEFT,
        "header_bg": None
    },

    # ---------------------------------------------------------
    # 8. Nebular (Dark & Elegant - Right Aligned)
    # ---------------------------------------------------------
    "Nebular": {
        "primary_color": colors.HexColor("#34495E"),  # Dark Blueish Grey
        "alignment": TA_RIGHT,
        "header_bg": None
    },

    # ---------------------------------------------------------
    # 9. Nova (Minimalist & Clean - Left Aligned)
    # ---------------------------------------------------------
    "Nova": {
        "primary_color": colors.HexColor("#7F8C8D"),  # Ashen Grey
        "alignment": TA_LEFT,
        "header_bg": None
    }
}
