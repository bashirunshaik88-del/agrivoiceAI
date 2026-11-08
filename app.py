import streamlit as st
import pandas as pd
import csv
import os

st.set_page_config(page_title="AgriVoice AI", page_icon="🌾")

# --- 1. NLP FUNCTIONS (Moved here to fix the import error) ---
def extract_agricultural_entities(text: str):
    text_lower = text.lower()
    crop_keywords = {
        "Cotton": ["cotton", "పత్తి", "कपास"],
        "Paddy": ["paddy", "rice", "వరి", "ధాన్యం", "धान", "चावल"],
        "Tomato": ["tomato", "టమాట", "टमाटर"],
        "Chilli": ["chilli", "chili", "మిరప", "मिर्च"],
        "Maize": ["maize", "corn", "మొక్కజొన్న", "मक्का"],
        "Groundnut": ["groundnut", "peanut", "వేరుశనగ", "मूंगफली"]
    }
    symptom_keywords = {
        "Yellow Leaves": ["yellow", "yellowing", "పసుపు", "पीली", "पीला"],
        "Red Leaves": ["red", "reddish", "ఎరుపు", "लाल"],
        "Leaf Spots": ["spot", "spots", "మచ్చలు", "धब्बे"],
        "Poor Growth": ["poor growth", "not growing", "stunted", "పెరగడం లేదు", "बढ़ नहीं"],
        "Pest": ["insect", "pest", "bug", "worm", "పురుగు", "कीट", "कीड़े"],
        "Water Shortage": ["dry", "water", "drought", "ఎండు", "నీరు", "सूखा", "पानी"]
    }
    detected_crop = "Unknown"
    for crop, keywords in crop_keywords.items():
        if any(word in text_lower for word in keywords):
            detected_crop = crop
            break
    detected_symptom = "Unknown"
    for symptom, keywords in symptom_keywords.items():
        if any(word in text_lower for word in keywords):
            detected_symptom = symptom
            break
    return {"Crop": detected_crop, "Symptom": detected_symptom, "Original_Text": text}

def get_recommendation(crop, symptom):
    if crop == "Unknown" or symptom == "Unknown": return None
    path = "dataset/crop_problems.csv" # Adjusted path for cloud
    if not os.path.exists(path): return None
    with open(path, mode='r', encoding='utf-8') as file:
        for row in csv.DictReader(file):
            if row['crop'].lower() == crop.lower() and row['symptom'].lower() == symptom.lower():
                return {"cause": row['possible_cause'], "action": row['recommended_action'], "precaution": row['precaution']}
    return None

def get_follow_up_questions(crop, symptom):
    path = "dataset/follow_up_questions.csv"
    if not os.path.exists(path): return None
    with open(path, mode='r', encoding='utf-8') as file:
        for row in csv.DictReader(file):
            if row['crop'].lower() == crop.lower() and row['symptom'].lower() == symptom.lower():
                return [row['question_1'], row['question_2']]
    return None

# --- 2. STREAMLIT UI ---
st.title("🌾 AgriVoice AI")
st.subheader("Problem Analysis & Solution Recommendation")

farmer_input = st.text_area(
    "Describe your crop problem (Try English or Telugu):", 
    "My cotton crop leaves are turning yellow."
)

if st.button("Analyze & Recommend"):
    if farmer_input:
        result = extract_agricultural_entities(farmer_input)
        crop = result['Crop']
        symptom = result['Symptom']
        
        st.info(f"🔍 **Detected:** Crop = {crop} | Problem = {symptom}")
        
        if crop == "Unknown" or symptom == "Unknown":
            st.warning("⚠️ The AI could not clearly identify the crop or problem. Please try rephrasing.")
        else:
            questions = get_follow_up_questions(crop, symptom)
            if questions:
                st.markdown("### 🩺 Follow-Up Questions")
                st.write(f"1. {questions[0]}")
                st.write(f"2. {questions[1]}")
            
            st.markdown("---")
            
            recommendation = get_recommendation(crop, symptom)
            if recommendation:
                st.markdown("### 🎯 Verified Recommendation")
                st.success(f"**Possible Cause:** {recommendation['cause']}")
                st.write(f"**Recommended Action:** {recommendation['action']}")
                st.error(f"**⚠️ Important Precaution:** {recommendation['precaution']}")
            else:
                st.error("No exact verified solution found in the database.")
    else:
        st.warning("Please enter a problem.")
