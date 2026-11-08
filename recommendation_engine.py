import csv
import os

def get_recommendation(crop, symptom):
    if crop == "Unknown" or symptom == "Unknown": return None
    path = os.path.join("dataset", "crop_problems.csv")
    if not os.path.exists(path): return None
    with open(path, mode='r', encoding='utf-8') as file:
        for row in csv.DictReader(file):
            if row['crop'].lower() == crop.lower() and row['symptom'].lower() == symptom.lower():
                return {"cause": row['possible_cause'], "action": row['recommended_action'], "precaution": row['precaution']}
    return None

def get_follow_up_questions(crop, symptom):
    path = os.path.join("dataset", "follow_up_questions.csv")
    if not os.path.exists(path): return None
    with open(path, mode='r', encoding='utf-8') as file:
        for row in csv.DictReader(file):
            if row['crop'].lower() == crop.lower() and row['symptom'].lower() == symptom.lower():
                return [row['question_1'], row['question_2']]
    return None