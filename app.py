import streamlit as st
import re
from PIL import Image, ImageDraw
import math

st.title("🩸 Venous Mapper")

text = st.text_input("Enter findings (e.g. left gsv reflux 3s 5mm, perforator calf, right ssv normal)")

# -------------------------
# PARSE INPUT
# -------------------------
def parse_multiple(text):
    findings = []
    
    parts = re.split(r",|\+", text.lower())
    
    for part in parts:
        side = "left" if "left" in part else "right"
        
        vessel = None
        if "gsv" in part:
            vessel = "gsv"
        elif "ssv" in part:
            vessel = "ssv"
        
        reflux = "reflux" in part or "varicose" in part
        
        duration_match = re.search(r"(\d+)\s*s", part)
        duration = duration_match.group(1) if duration_match else None
        
        diameter_match = re.search(r"(\d+)\s*mm", part)
        diameter = diameter_match.group(1) if diameter_match else None
        
        perforator = "perforator" in part
        
        findings.append({
            "side": side,
            "vessel": vessel,
            "reflux": reflux,
            "duration": duration,
            "diameter": diameter,
            "perforator": perforator
        })
    
    return findings


# -------------------------
# SMOOTH SQUIGGLE
# -------------------------
def draw_squiggle(draw, x, y1, y2):
    points = []
    for y in range(y1, y2, 5):
        offset = int(10 * math.sin(y / 30))
        points.append((x + offset, y))
    draw.line(points, fill="blue", width=4)


# -------------------------
# DRAW ARROWS
# -------------------------
def draw_arrow(draw, x, y):
    draw.polygon([(x, y), (x - 5, y - 10), (x + 5, y - 10)], fill="blue")


# -------------------------
# DRAW PERFORATOR
# -------------------------
def draw_perforator(draw, x, y):
    draw.line((x - 20, y, x + 20, y), fill="blue", width=3)
    draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill="blue")


# -------------------------
# DRAW MAP
# -------------------------
def draw_map(findings):
    img = Image.new("RGB", (500, 800), "white")
    draw = ImageDraw.Draw(img)
    
    # Legs
    draw.line((200, 100, 200, 700), fill="black", width=5)
    draw.line((300, 100, 300, 700), fill="black", width=5)
    
    # Junction labels
    draw.text((160, 100), "SFJ", fill="black")
    draw.text((260, 100), "SFJ", fill="black")
    draw.text((160, 350), "SPJ", fill="black")
    draw.text((260, 350), "SPJ", fill="black")
    
    for f in findings:
        side = f["side"]
        vessel = f["vessel"]
        reflux = f["reflux"]
        diameter = f["diameter"]
        perforator = f["perforator"]
        
        x = 200 if side == "left" else 300
        
        # ---------------- GSV ----------------
        if vessel == "gsv":
            if reflux:
                draw_squiggle(draw, x, 120, 650)
                for y in range(200, 650, 120):
                    draw_arrow(draw, x, y)
            else:
                draw.line((x, 120, x, 650), fill="blue", width=5)
        
        # ---------------- SSV ----------------
        elif vessel == "ssv":
            if reflux:
                draw_squiggle(draw, x, 350, 700)
                for y in range(400, 700, 120):
                    draw_arrow(draw, x, y)
            else:
                draw.line((x, 350, x, 700), fill="blue", width=5)
        
        # ---------------- PERFORATOR ----------------
        if perforator:
            draw_perforator(draw, x, 500)
        
        # ---------------- DIAMETER ----------------
        if diameter:
            draw.text((x + 20, 200), f"{diameter} mm", fill="black")
    
    return img


# -------------------------
# REPORT
# -------------------------
def generate_report(findings):
    lines = []
    
    for f in findings:
        side = f["side"]
        vessel = f["vessel"]
        
        if vessel:
            line = f"{side.capitalize()} {vessel.upper()}"
            
            if f["diameter"]:
                line += f" ({f['diameter']} mm)"
            
            if f["reflux"]:
                if f["duration"]:
                    line += f": Reflux ({f['duration']}s)"
                else:
                    line += ": Reflux"
            else:
                line += ": Competent"
            
            lines.append(line)
        
        if f["perforator"]:
            lines.append(f"{side.capitalize()} perforator incompetence")
    
    return lines


# -------------------------
# MAIN
# -------------------------
if text:
    findings = parse_multiple(text)
    
    img = draw_map(findings)
    st.image(img, caption="Venous Map")
    
    st.markdown("### 📄 Report")
    report = generate_report(findings)
    
    for line in report:
        st.write("- " + line)
