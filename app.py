import streamlit as st
import re
from PIL import Image, ImageDraw

st.title("🩸 Vascular Mapper")

text = st.text_input("Enter finding (e.g. left sfa proximal 70% stenosis)")

# -------------------------
# PARSE INPUT
# -------------------------
def parse(text):
    text = text.lower()
    
    side = "left" if "left" in text else "right"
    
    vessel_map = {
        "sfa": "sfa",
        "femoral": "sfa",
        "popliteal": "popliteal",
        "ata": "ata",
        "pta": "pta"
    }
    
    vessel = None
    for key in vessel_map:
        if key in text:
            vessel = vessel_map[key]
            break
    
    segment = "proximal" if "proximal" in text else "distal"
    
    percent_match = re.search(r"(\d+)%", text)
    percent = int(percent_match.group(1)) if percent_match else None
    
    return side, vessel, segment, percent


# -------------------------
# DRAW DIAGRAM
# -------------------------
def draw_map(side, vessel):
    img = Image.new("RGB", (400, 700), "white")
    draw = ImageDraw.Draw(img)
    
    # Draw legs
    draw.line((150, 50, 150, 650), fill="black", width=6)  # left leg
    draw.line((250, 50, 250, 650), fill="black", width=6)  # right leg
    
    # Choose side
    x = 150 if side == "left" else 250
    
    # Draw arteries (basic layout)
    if vessel == "sfa":
        draw.line((x, 120, x, 400), fill="red", width=10)
    elif vessel == "popliteal":
        draw.line((x, 400, x, 550), fill="red", width=10)
    elif vessel == "ata":
        draw.line((x, 550, x-20, 680), fill="red", width=8)
    elif vessel == "pta":
        draw.line((x, 550, x+20, 680), fill="red", width=8)
    
    return img


# -------------------------
# MAIN
# -------------------------
if text:
    side, vessel, segment, percent = parse(text)
    
    if vessel is None:
        st.warning("⚠️ Please specify vessel (e.g. SFA, popliteal)")
    else:
        img = draw_map(side, vessel)
        st.image(img, caption="Vascular Map")
        
        # Output text
        if percent:
            st.success(f"{side.capitalize()} {vessel.upper()} ({segment}): {percent}% stenosis")
        else:
            st.success(f"{side.capitalize()} {vessel.upper()} ({segment})")
        
        # Clinical report
        vessel_names = {
            "sfa": "superficial femoral artery",
            "popliteal": "popliteal artery",
            "ata": "anterior tibial artery",
            "pta": "posterior tibial artery"
        }
        
        vessel_full = vessel_names.get(vessel, vessel)
        
        if percent:
            report = f"{percent}% stenosis of the {segment} {side} {vessel_full}."
        else:
            report = f"Disease of the {segment} {side} {vessel_full}."
        
        st.markdown("### 📄 Report")
        st.write(report)
