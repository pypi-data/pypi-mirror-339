"""
Create SpeedClick Pro icons if they don't already exist
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icons():
    """Create app icons if they don't exist already"""
    icons_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
    os.makedirs(icons_dir, exist_ok=True)
    
    icon_path = os.path.join(icons_dir, "icon.png")
    logo_path = os.path.join(icons_dir, "logo.png")
    
    # Skip if icons already exist
    if os.path.exists(icon_path) and os.path.exists(logo_path):
        return
    
    # Create icon (64x64)
    icon_size = (64, 64)
    icon_img = Image.new('RGBA', icon_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon_img)
    
    # Draw a circle with gradient
    for i in range(32, 0, -1):
        color_value = int(255 * (i / 32))
        draw.ellipse((32-i, 32-i, 32+i, 32+i), fill=(50, color_value, 255))
    
    # Draw click cursor
    cursor_points = [(25, 15), (35, 25), (30, 30), (45, 45)]
    draw.line(cursor_points, fill=(255, 255, 255), width=3)
    
    # Save icon
    icon_img.save(icon_path)
    
    # Create logo (200x60)
    logo_size = (200, 60)
    logo_img = Image.new('RGBA', logo_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(logo_img)
    
    # Draw app name with custom styling
    try:
        # Try to load a font, fall back to default
        font = ImageFont.truetype("arial.ttf", 28)
    except IOError:
        font = ImageFont.load_default()
    
    # Draw text shadow
    draw.text((52, 17), "SpeedClick Pro", fill=(20, 20, 20, 128), font=font)
    # Draw text
    draw.text((50, 15), "SpeedClick Pro", fill=(50, 100, 255), font=font)
    
    # Add the icon to the logo
    logo_img.paste(icon_img.resize((50, 50)), (0, 5), icon_img.resize((50, 50)))
    
    # Save logo
    logo_img.save(logo_path)

if __name__ == "__main__":
    create_icons()
