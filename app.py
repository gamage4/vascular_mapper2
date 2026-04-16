import streamlit as st
import re

st.title("🩸 Vascular Mapper")

text = st.text_input("Enter finding (e.g. left sfa proximal 70% stenosis)")

def parse(text):
    text = text.lower()
    
    # Side
    side = "Left" if "left" in text else "Right"
    
    # Vessel mapping
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
            break
    
    if vessel is None:
        return side, "⚠️ Specify vessel (e.g. SFA, popliteal)", "", "", ""
    
    # Segment
    segment = "Proximal" if "proximal" in text else "Distal"
    
    # Pathology
    pathology = "Stenosis" if "stenosis" in text else "Occlusion"
    
    # % stenosis detection
    percent_match = re.search(r"(\d+)%", text)
    percent = percent_match.group(1) if percent_match else None
    
    # Severity classification
    severity = ""
    if percent:
        p = int(percent)
        if p < 50:
            severity = "Mild"
        elif 50 <= p < 70:
            severity = "Moderate"
        else:
            severity = "Severe"
    
    return side, vessel, segment, pathology, percent, severity


if text:
    side, vessel, segment, pathology, percent, severity = parse(text)
    
    # Simple output
    if percent:
        st.success(f"{side} {vessel} ({segment}): {severity} {percent}% {pathology}")
    else:
        st.success(f"{side} {vessel} ({segment}): {pathology}")
    
    # Clinical report output
    if vessel and "⚠️" not in vessel:
        if percent:
            report = f"{severity} ({percent}%) {pathology.lower()} of the {segment.lower()} {side.lower()} {vessel.lower()}."
        else:
            report = f"{pathology} of the {segment.lower()} {side.lower()} {vessel.lower()}."
        
        st.markdown("### 📄 Report")
        st.write(report)
