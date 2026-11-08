def translate_to_language(text, target_lang):
    """
    A simple dictionary-based translator for our specific agricultural terms.
    (In a full production app, this would connect to Google Translate API or IndicTrans2).
    """
    if target_lang == "English" or not target_lang:
        return text

    # Dictionary mapping English phrases to Telugu and Hindi
    translations = {
        "Telugu": {
            "Nitrogen deficiency or waterlogging": "నత్రజని లోపం లేదా నీరు నిలిచిపోవడం",
            "Sucking pests (like whitefly)": "పీల్చే పురుగులు (తెల్ల బంగాళాదుంప లాంటివి)",
            "Fungal infection (Leaf spot disease)": "శిలీంధ్ర సంక్రమణ (ఆకు మచ్చల వ్యాధి)",
            "Nutrient deficiency (Zinc or Nitrogen)": "పోషకాల లోపం (జింక్ లేదా నత్రజని)",
            "Check soil moisture. If dry, irrigate lightly.": "నేల తేమను తనిఖీ చేయండి. పొడిగా ఉంటే, తేలికగా నీరు పెట్టండి.",
            "Inspect the underside of leaves for tiny insects.": "ఆకుల కింద చిన్న పురుగుల కోసం తనిఖీ చేయండి.",
            "Remove severely affected leaves.": "తీవ్రంగా ప్రభావితమైన ఆకులను తీసివేయండి.",
            "Do not apply heavy nitrogen fertilizer without soil testing.": "నేల పరీక్ష లేకుండా ఎక్కువ నత్రజని ఎరువులు వేయవద్దు.",
            "Are the older leaves or younger leaves turning yellow?": "పాత ఆకులు లేదా కొత్త ఆకులు పసుపు రంగులోకి మారుతున్నాయా?",
            "Is the soil wet or dry?": "నేల తడిగా ఉందా లేదా పొడిగా ఉందా?"
        },
        "Hindi": {
            "Nitrogen deficiency or waterlogging": "नाइट्रोजन की कमी या जलभराव",
            "Sucking pests (like whitefly)": "रस चूसने वाले कीट (सफेद मक्खी)",
            "Fungal infection (Leaf spot disease)": "फंगल संक्रमण (पत्ती धब्बा रोग)",
            "Nutrient deficiency (Zinc or Nitrogen)": "पोषक तत्वों की कमी (जिंक या नाइट्रोजन)",
            "Check soil moisture. If dry, irrigate lightly.": "मिट्टी की नमी की जाँच करें। अगर सूखा है, तो हल्की सिंचाई करें।",
            "Inspect the underside of leaves for tiny insects.": "पत्तियों के नीचे छोटे कीड़ों की जाँच करें।",
            "Remove severely affected leaves.": "गंभीर रूप से प्रभावित पत्तियों को हटा दें।",
            "Do not apply heavy nitrogen fertilizer without soil testing.": "मिट्टी परीक्षण के बिना भारी नाइट्रोजन उर्वरक न डालें।",
            "Are the older leaves or younger leaves turning yellow?": "क्या पुरानी पत्तियाँ या नई पत्तियाँ पीली पड़ रही हैं?",
            "Is the soil wet or dry?": "क्या मिट्टी गीली है या सूखी?"
        }
    }

    # Try to translate, otherwise return original English
    lang_dict = translations.get(target_lang, {})
    return lang_dict.get(text, text)