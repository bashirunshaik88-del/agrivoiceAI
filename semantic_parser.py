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