import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from modules.semantic_parser import extract_agricultural_entities
from modules.recommendation_engine import get_recommendation, get_follow_up_questions

st.set_page_config(page_title="AgriVoice AI", page_icon="🌾")

st.title("🌾 AgriVoice AI")
st.subheader("Problem Analysis & Solution Recommendation")

farmer_input = st.text_area(
    "Describe your crop problem (Try English or Telugu):", 
    "My cotton crop leaves are turning yellow."
)

if st.button("Analyze & Recommend"):
    if farmer_input:
        # Step 1: Extract Crop and Symptom
        result = extract_agricultural_entities(farmer_input)
        crop = result['Crop']
        symptom = result['Symptom']
        
        st.info(f"🔍 **Detected:** Crop = {crop} | Problem = {symptom}")
        
        if crop == "Unknown" or symptom == "Unknown":
            st.warning("⚠️ The AI could not clearly identify the crop or problem. Please try rephrasing.")
        else:
            # Step 2: Get Follow-up Questions
            questions = get_follow_up_questions(crop, symptom)
            if questions:
                st.markdown("### 🩺 Follow-Up Questions (Like a Doctor)")
                st.write("Please answer these to help the AI narrow down the cause:")
                st.write(f"1. {questions[0]}")
                st.write(f"2. {questions[1]}")
            
            st.markdown("---")
            
            # Step 3: Get Recommendation
            recommendation = get_recommendation(crop, symptom)
            if recommendation:
                st.markdown("### 🎯 Verified Recommendation")
                st.success(f"**Possible Cause:** {recommendation['cause']}")
                st.write(f"**Recommended Action:** {recommendation['action']}")
                st.error(f"**⚠️ Important Precaution:** {recommendation['precaution']}")
            else:
                st.error("No exact verified solution found in the database for this combination.")
    else:
        st.warning("Please enter a problem.")