import streamlit as st

st.title("🩸 Vascular Mapper")

text = st.text_input("Enter finding (e.g. left sfa proximal stenosis)")

def parse(text):
    text = text.lower()
    
    side = "Left" if "left" in text else "Right"
    
    vessel_map = {
        "sfa": "Superficial Femoral Artery",
        "femoral": "Superficial Femoral Artery",
        "popliteal": "Popliteal Artery",
        "ata": "Anterior Tibial Artery",
        "pta": "Posterior Tibial Artery",
        "peroneal": "Peroneal Artery"
    }
    
    vessel = None
    for key in vessel_map:
        if key in text:
            vessel = vessel_map[key]
    
    if vessel is None:
        vessel = "Unspecified Vessel"
    
    segment = "Proximal" if "proximal" in text else "Distal"
    
    pathology = "Stenosis" if "stenosis" in text else "Occlusion"
    
    return side, vessel, segment, pathology
