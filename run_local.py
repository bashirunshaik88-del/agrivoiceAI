import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.language_detection import detect_language
from modules.text_preprocessing import clean_text
from modules.semantic_parser import extract_agricultural_entities
from modules.recommendation_engine import get_recommendation, get_follow_up_questions

def main():
    print("="*55)
    print("🌾 WELCOME TO AGRIVOICE AI (Local Terminal Version)")
    print("="*55)
    print("Type 'exit' to quit.\n")

    while True:
        raw_input = input("👨‍🌾 Farmer: ")
        
        if raw_input.lower() == 'exit':
            print("Goodbye! Have a great harvest.")
            break
            
        if not raw_input.strip():
            continue

        lang = detect_language(raw_input)
        clean_input = clean_text(raw_input)
        
        print(f"\n[System]: Language Detected: {lang}")
        
        parsed_data = extract_agricultural_entities(clean_input)
        crop = parsed_data['Crop']
        symptom = parsed_data['Symptom']
        
        print(f"[System]: Crop Identified: {crop}")
        print(f"[System]: Problem Identified: {symptom}\n")
        
        if crop == "Unknown" or symptom == "Unknown":
            print("⚠️  AI: I could not understand the crop or the problem.")
            print("    Please try typing something like: 'My cotton leaves are turning yellow.'\n")
            print("-" * 55)
            continue

        questions = get_follow_up_questions(crop, symptom)
        if questions:
            print("🩺 AI: Before I give a solution, I need to ask:")
            print(f"    1. {questions[0]}")
            print(f"    2. {questions[1]}\n")
            
        recommendation = get_recommendation(crop, symptom)
        print("🎯 AI Recommendation:")
        if recommendation:
            print(f"    Cause: {recommendation['cause']}")
            print(f"    Action: {recommendation['action']}")
            print(f"    Precaution: {recommendation['precaution']}")
        else:
            print("    No exact verified solution found in our database.")
            
        print("\n" + "-" * 55 + "\n")

if __name__ == "__main__":
    main()