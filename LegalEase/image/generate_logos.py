"""
LegalEase Logo Generator
Generates high-resolution branded logo images for dark mode (web UI) and light mode (Word/PDF export).
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = BASE_DIR / "image"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

LOGO_LIGHT = IMAGE_DIR / "Logo.png"
LOGO_DARK = IMAGE_DIR / "inverseLogo.png"


def create_logo(dark_mode=False, output_path=None):
    width, height = 700, 220
    # Background
    if dark_mode:
        bg_color = (15, 23, 42, 255)  # Slate dark #0F172A
        fg_color = (255, 255, 255, 255)  # White
        accent_color = (56, 189, 248, 255)  # Sky blue #38BDF8
        sub_color = (148, 163, 184, 255)  # Slate light #94A3B8
    else:
        bg_color = (255, 255, 255, 255)  # Pure White #FFFFFF
        fg_color = (26, 32, 44, 255)  # Charcoal #1A202C
        accent_color = (37, 99, 235, 255)  # Blue #2563EB
        sub_color = (100, 116, 139, 255)  # Slate grey #64748B

    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Draw Scales of Justice Icon on the left
    # Scale center: (100, 110)
    cx, cy = 110, 110

    # Base
    draw.line([(cx - 45, cy + 65), (cx + 45, cy + 65)], fill=fg_color, width=6)
    draw.line([(cx - 30, cy + 60), (cx + 30, cy + 60)], fill=fg_color, width=5)

    # Central Pillar
    draw.line([(cx, cy - 65), (cx, cy + 60)], fill=fg_color, width=6)
    # Finial / Top circle
    draw.ellipse([(cx - 9, cy - 74), (cx + 9, cy - 56)], fill=accent_color)

    # Main Balance Beam
    draw.line([(cx - 70, cy - 40), (cx + 70, cy - 40)], fill=fg_color, width=6)
    # Fulcrum triangle/pivot
    draw.polygon([(cx, cy - 40), (cx - 10, cy - 25), (cx + 10, cy - 25)], fill=fg_color)

    # Left Pan Strings & Pan
    left_x = cx - 65
    left_beam_y = cy - 40
    pan_y = cy + 15
    draw.line([(left_x, left_beam_y), (left_x - 22, pan_y)], fill=sub_color, width=3)
    draw.line([(left_x, left_beam_y), (left_x + 22, pan_y)], fill=sub_color, width=3)
    # Left Pan Arc
    draw.arc([(left_x - 28, pan_y - 10), (left_x + 28, pan_y + 18)], start=0, end=180, fill=fg_color, width=5)
    draw.line([(left_x - 28, pan_y + 4), (left_x + 28, pan_y + 4)], fill=fg_color, width=4)

    # Right Pan Strings & Pan
    right_x = cx + 65
    right_beam_y = cy - 40
    draw.line([(right_x, right_beam_y), (right_x - 22, pan_y)], fill=sub_color, width=3)
    draw.line([(right_x, right_beam_y), (right_x + 22, pan_y)], fill=sub_color, width=3)
    # Right Pan Arc
    draw.arc([(right_x - 28, pan_y - 10), (right_x + 28, pan_y + 18)], start=0, end=180, fill=fg_color, width=5)
    draw.line([(right_x - 28, pan_y + 4), (right_x + 28, pan_y + 4)], fill=fg_color, width=4)

    # Try to load a nice font, fallback to default
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 64)
        font_sub = ImageFont.truetype("arial.ttf", 22)
    except IOError:
        try:
            font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
            font_sub = ImageFont.truetype("DejaVuSans.ttf", 22)
        except IOError:
            font_title = ImageFont.load_default()
            font_sub = ImageFont.load_default()

    # Draw Text
    text_x = 220
    draw.text((text_x, 50), "LegalEase", fill=fg_color, font=font_title)
    draw.text((text_x + 2, 130), "AI LEGAL DOCUMENT GENERATOR", fill=sub_color, font=font_sub)

    # Decorative accent bar
    draw.line([(text_x, 122), (text_x + 180, 122)], fill=accent_color, width=4)

    if output_path:
        img.save(output_path, "PNG")
    return img


def generate_all_logos():
    brain_dir = Path(r"C:\Users\acer\.gemini\antigravity-ide\brain\6be1a216-7cf9-452e-8ef7-e565c05d7fd0")
    source_white = brain_dir / "legalease_white_bg_1790435106281.jpg"
    source_inverse = brain_dir / "legalease_inverse_1790435085253.jpg"

    # If high quality AI renders exist, convert/save them
    if source_white.exists():
        try:
            img = Image.open(source_white)
            img.save(LOGO_LIGHT, "PNG")
        except Exception:
            create_logo(dark_mode=False, output_path=LOGO_LIGHT)
    else:
        create_logo(dark_mode=False, output_path=LOGO_LIGHT)

    if source_inverse.exists():
        try:
            img = Image.open(source_inverse)
            img.save(LOGO_DARK, "PNG")
        except Exception:
            create_logo(dark_mode=True, output_path=LOGO_DARK)
    else:
        create_logo(dark_mode=True, output_path=LOGO_DARK)


if __name__ == "__main__":
    generate_all_logos()
    print("Logos successfully created in image/ directory.")
