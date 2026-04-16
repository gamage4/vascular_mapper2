import streamlit as st

st.title("🩸 Vascular Mapper")

text = st.text_input("Enter finding (e.g. left sfa proximal stenosis)")

def parse(text):
    text = text.lower()
    
    side = "Left" if "left" in text else "Right"
    
    vessel = None
    if "sfa" in text:
        vessel = "Superficial Femoral Artery"
    elif "popliteal" in text:
        vessel = "Popliteal Artery"
    
    segment = "Proximal" if "proximal" in text else "Distal"
    
    pathology = "Stenosis" if "stenosis" in text else "Occlusion"
    
    return side, vessel, segment, pathology

if text:
    side, vessel, segment, pathology = parse(text)
    
    st.success(f"{side} {vessel} ({segment}): {pathology}")
