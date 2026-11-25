from PIL import Image, ImageDraw, ImageFont
import sys

# Configuration
WIDTH, HEIGHT = 1024, 1024
BG_COLOR = "#ffffff"
TEXT_COLOR = "#1a1a1a"
TAG_COLOR = "#b30000"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
BOLD_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

STORIES = [
    ("MIDDLE EAST", "TANKERS HIT MINES IN STRAIT OF HORMUZ", "Iran's IRGC says three oil tankers hit naval mines and caught fire while under U.S. air escort; Iran orders the strait closed 'further day by day' until its seven conditions are met; Qatar's PM meets Rubio and Vance in Washington to revive peace talks."),
    ("RUSSIA-UKRAINE", "PUTIN: RETALIATION 'INEVITABLE'", "Putin says Ukraine keeps striking Russian oil refineries despite Trump's appeal; drone strikes cut Russian refining capacity 45% since late October; overnight attack on Zaporizhzhia kills 2, wounds 40."),
    ("US / BUSINESS", "NVIDIA REINSTATES JENSEN HUANG AS CEO", "Trump personally intervened with the board; NVDA stock soared over 30%; U.S. Commerce blacklists Singapore's Megaspeed over chip diversion."),
    ("EUROPE", "RUSSIA THREATENS 'OPEN WAR' WITH ESTONIA", "Kremlin rages as Estonia closes its land border with Russia; a Russian drone strayed into Polish airspace for 8 minutes; EU bans Russian seaborne LNG from 1 January."),
    ("AFRICA", "SUDAN: RSF DRONES HIT KHARTOUM", "Army intercepts drone attack on the capital; main airport and a UN facility struck; national power grid near collapse."),
    ("MIDDLE EAST / YEMEN", "HOUTHIS ADVANCE ON ADEN", "Rebels push 60 km toward Yemen's southern capital; government declares 'Aden is a red line'; Riyadh tower hit by 'terrorist attack', 11 injured."),
    ("ASIA", "CHINA-RUN AI CAMPAIGN TARGETS TAIWAN VOTE", "Research finds coordinated AI-powered influence operation ahead of Taiwan's election; Seoul offers up to $375,000 rewards to catch AI exam cheats."),
    ("AMERICAS", "MEXICO CAPTURES CARTEL BOSS 'EL CHAPO ISIDRO'", "Beltrán Leyva leader Meza Flores seized in Sinaloa; clashes set flaming roadblocks; extradition refused.")
]

def get_wrapped_lines(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        if draw.textlength(test_line, font=font) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def get_layout(draw, scale):
    fonts = {
        "masthead": ImageFont.truetype(BOLD_FONT_PATH, int(70 * scale)),
        "date": ImageFont.truetype(SANS_FONT_PATH, int(24 * scale)),
        "cat": ImageFont.truetype(SANS_FONT_PATH, int(18 * scale)),
        "headline": ImageFont.truetype(BOLD_FONT_PATH, int(26 * scale)),
        "detail": ImageFont.truetype(FONT_PATH, int(20 * scale)),
    }
    
    y = 50 * scale
    max_w = WIDTH - 100
    
    # Masthead
    y += 70 * scale
    y += 30 * scale
    y += 30 * scale
    y += 10 * scale # Rule
    
    elements = []
    
    for i, (category, headline, detail) in enumerate(STORIES):
        if i == 0:
            y += 24 * scale
        # Category
        elements.append(("text", category, fonts["cat"], (50, y), TAG_COLOR))
        y += 20 * scale * 1.2
        
        # Headline (max 2 lines)
        h_lines = get_wrapped_lines(headline, fonts["headline"], max_w, draw)[:2]
        for line in h_lines:
            elements.append(("text", line, fonts["headline"], (50, y), TEXT_COLOR))
            y += 28 * scale * 1.2
        
        # Detail (max 2 lines)
        d_lines = get_wrapped_lines(detail, fonts["detail"], max_w, draw)[:2]
        for line in d_lines:
            elements.append(("text", line, fonts["detail"], (50, y), TEXT_COLOR))
            y += 22 * scale * 1.2
            
        y += 15 * scale
    
    return elements, y

def create_image():
    image = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(image)
    
    scale = 1.0
    while scale > 0.5:
        elements, y_end = get_layout(draw, scale)
        if y_end < 978:
            break
        scale -= 0.05
    
    # Final Draw
    fonts = {
        "masthead": ImageFont.truetype(BOLD_FONT_PATH, int(70 * scale)),
        "date": ImageFont.truetype(SANS_FONT_PATH, int(24 * scale)),
        "cat": ImageFont.truetype(SANS_FONT_PATH, int(18 * scale)),
        "headline": ImageFont.truetype(BOLD_FONT_PATH, int(26 * scale)),
        "detail": ImageFont.truetype(FONT_PATH, int(20 * scale)),
    }
    
    # Masthead Draw
    draw.text((WIDTH//2, 80 * scale), "THE WORLD", fill=TEXT_COLOR, font=fonts["masthead"], anchor="mm")
    draw.text((WIDTH//2, 140 * scale), "Tuesday, 24 November 2026", fill=TEXT_COLOR, font=fonts["date"], anchor="mm")
    draw.text((WIDTH//2, 170 * scale), "A picture of the day's news", fill=TEXT_COLOR, font=fonts["date"], anchor="mm")
    draw.line((50, 200 * scale, 974, 200 * scale), fill=TEXT_COLOR, width=int(3 * scale))
    
    for kind, text, font, pos, color in elements:
        draw.text(pos, text, fill=color, font=font)
        
    image.save("entry.png", "PNG", optimize=True)
    print(f"Created entry.png with scale {scale:.2f}, height {y_end:.0f}")

if __name__ == "__main__":
    create_image()
