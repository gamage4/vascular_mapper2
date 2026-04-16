import streamlit as st
import re
from PIL import Image, ImageDraw
import random

st.title("🩸 Venous Mapper")

text = st.text_input("Enter finding (e.g. left gsv reflux, varicose veins)")

# -------------------------
# PARSE INPUT
# -------------------------
def parse(text):
    text = text.lower()
    
    side = "left" if "left" in text else "right"
    
    reflux = "reflux" in text or "varicose" in text
    
    vessel = "gsv" if "gsv" in text else "ssv" if "ssv" in text else None
    
    return side, vessel, reflux


# -------------------------
# DRAW SQUIGGLY VEIN
# -------------------------
def draw_squiggly(draw, x, y_start, y_end):
    y = y_start
    points = []
    
    while y < y_end:
        offset = random.randint(-15, 15)
        points.append((x + offset, y))
        y += 20
    
    draw.line(points, fill="blue", width=4)


# -------------------------
# DRAW MAP
# -------------------------
def draw_map(side, vessel, reflux):
    img = Image.new("RGB", (500, 800), "white")
    draw = ImageDraw.Draw(img)
    
    # Draw body outline (simple)
    draw.line((200, 100, 200, 700), fill="black", width=5)  # left leg
    draw.line((300, 100, 300, 700), fill="black", width=5)  # right leg
    
    x = 200 if side == "left" else 300
    
    # Draw vein
    if vessel == "gsv":
        if reflux:
            draw_squiggly(draw, x, 150, 650)
        else:
            draw.line((x, 150, x, 650), fill="blue", width=5)
    
    elif vessel == "ssv":
        if reflux:
            draw_squiggly(draw, x, 350, 700)
        else:
            draw.line((x, 350, x, 700), fill="blue", width=5)
    
    return img


# -------------------------
# MAIN
# -------------------------
if text:
    side, vessel, reflux = parse(text)
    
    if vessel is None:
        st.warning("⚠️ Specify vein (GSV or SSV)")
    else:
        img = draw_map(side, vessel, reflux)
        st.image(img, caption="Venous Map")
        
        if reflux:
            st.success(f"{side.capitalize()} {vessel.upper()} reflux / varicosities")
        else:
            st.success(f"{side.capitalize()} {vessel.upper()} normal")
