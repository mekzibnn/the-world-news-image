from PIL import Image, ImageDraw, ImageFont

# Configuration
WIDTH, HEIGHT = 1024, 1024
BG_COLOR = "#ffffff"
TEXT_COLOR = "#1a1a1a"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
BOLD_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

STORIES = [
    ("MIDDLE EAST", "TANKERS HIT MINES IN STRAIT OF HORMUZ", "Iran's IRGC says three oil tankers hit naval mines; Iran orders the strait closed until its seven conditions are met."),
    ("RUSSIA-UKRAINE", "PUTIN: RETALIATION 'INEVITABLE'", "Putin says Ukraine keeps striking Russian oil refineries despite Trump's appeal; drone strikes cut Russian refining capacity 45% since late October; overnight attack on Zaporizhzhia kills 2, wounds 40."),
    ("US / BUSINESS", "NVIDIA REINSTATES JENSEN HUANG AS CEO", "Trump personally intervened with the board; NVDA stock soared over 30%; U.S. Commerce blacklists Singapore's Megaspeed over chip diversion."),
    ("EUROPE", "RUSSIA THREATENS 'OPEN WAR' WITH ESTONIA", "Kremlin rages as Estonia closes its land border with Russia; a Russian drone strayed into Polish airspace for 8 minutes; EU bans Russian seaborne LNG from 1 January."),
    ("AFRICA", "SUDAN: RSF DRONES HIT KHARTOUM", "Army intercepts drone attack on the capital; main airport and a UN facility struck; national power grid near collapse."),
    ("MIDDLE EAST / YEMEN", "HOUTHIS ADVANCE ON ADEN", "Rebels push 60 km toward Yemen's southern capital; government declares 'Aden is a red line'; Riyadh tower hit by 'terrorist attack', 11 injured."),
    ("ASIA", "CHINA-RUN AI CAMPAIGN TARGETS TAIWAN VOTE", "Research finds coordinated AI-powered influence operation ahead of Taiwan's election; Seoul offers up to $375,000 rewards to catch AI exam cheats."),
    ("AMERICAS", "MEXICO CAPTURES CARTEL BOSS 'EL CHAPO ISIDRO'", "Beltrán Leyva leader Meza Flores seized in Sinaloa; clashes set flaming roadblocks; extradition refused.")
]

def draw_chip(draw, x, y, text, color, font):
    w = draw.textlength(text, font=font)
    padding = 6
    h = 18
    draw.rounded_rectangle([x, y, x + w + 2*padding, y + h + 2], radius=3, fill=color)
    draw.text((x + padding, y + 1), text, fill="white", font=font)
    return x + w + 2*padding + 8 # return new x

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

def create_image():
    image = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(image)
    
    scale = 0.81 # Adjusted to fit 8 stories
    
    # Fonts
    fonts = {
        "masthead": ImageFont.truetype(BOLD_FONT_PATH, int(60 * scale)),
        "date": ImageFont.truetype(SANS_FONT_PATH, int(20 * scale)),
        "headline": ImageFont.truetype(BOLD_FONT_PATH, int(22 * scale)),
        "lead_headline": ImageFont.truetype(BOLD_FONT_PATH, int(26 * scale)),
        "detail": ImageFont.truetype(FONT_PATH, int(17 * scale)),
        "chip": ImageFont.truetype(BOLD_FONT_PATH, int(12 * scale)),
    }
    
    # Masthead Draw
    draw.text((WIDTH//2, 60 * scale), "THE WORLD", fill=TEXT_COLOR, font=fonts["masthead"], anchor="mm")
    date_str = "Tuesday · 24 November 2026"
    draw.text((WIDTH//2, 100 * scale), date_str, fill=TEXT_COLOR, font=fonts["date"], anchor="mm")
    draw.line((50, 130 * scale, 974, 130 * scale), fill="#dc143c", width=int(6 * scale))
    
    y = 160 * scale
    
    for i, (cat, head, det) in enumerate(STORIES):
        accent_color = {"MIDDLE EAST": "#dc143c", "RUSSIA-UKRAINE": "#4682b4", "US / BUSINESS": "#ffbf00", "EUROPE": "#008080", "AFRICA": "#ffa500", "MIDDLE EAST / YEMEN": "#8b0000", "ASIA": "#800080", "AMERICAS": "#008000"}.get(cat, "#000000")
        
        # Block height based on position
        is_lead = (i == 0)
        h_font = fonts["lead_headline"] if is_lead else fonts["headline"]
        h_lines = get_wrapped_lines(head, h_font, 800 * scale, draw)[:2]
        d_lines = get_wrapped_lines(det, fonts["detail"], 800 * scale, draw)[:3]
        
        block_h = (len(h_lines) * (36 if is_lead else 30) + len(d_lines) * 22 + 40) * scale
        
        # Draw background and accent
        bg_color = "#e0e0e0" if is_lead else "#f5f5f5"
        draw.rectangle([50, y, 974, y + block_h], fill=bg_color)
        draw.rectangle([50, y, 60, y + block_h], fill=accent_color)
        
        # Draw Chip
        draw_chip(draw, 75 * scale, y + 12 * scale, cat, accent_color, fonts["chip"])
        
        # Draw Text
        text_y = y + 40 * scale # lower text to make room for chip
        for line in h_lines:
            draw.text((140 * scale, text_y), line, fill=TEXT_COLOR, font=h_font)
            text_y += (36 if is_lead else 30) * scale
        for line in d_lines:
            draw.text((140 * scale, text_y), line, fill=TEXT_COLOR, font=fonts["detail"])
            text_y += 22 * scale
            
        y += block_h + 15 * scale
    
    # Assert layout
    if y > (1024 - 30):
        raise Exception(f"Layout exceeds page limit: y={y}")
        
    image.save("entry.png", "PNG", optimize=True)
    print("Created entry.png")

if __name__ == "__main__":
    create_image()
