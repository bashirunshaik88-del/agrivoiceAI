# 🌾 AgriVoice AI: Multilingual Farmer Problem Understanding System

## 📌 Abstract
AgriVoice AI is an NLP-based agricultural problem understanding and solution recommendation system. It allows farmers to describe their crop problems in English, Telugu, or Hindi and provides verified, context-aware agricultural suggestions. The system uses semantic parsing to extract the crop and symptom, asks follow-up questions, retrieves solutions from a verified knowledge base, and translates the final advice into the farmer's native language.

## 🎯 Objectives
1. Accept agricultural queries in English, Telugu, and Hindi.
2. Detect the input language automatically using Unicode regex.
3. Parse the sentence to extract the Crop and Symptom.
4. Provide follow-up questions based on the crop and symptom.
5. Retrieve verified solutions from a curated CSV database.
6. Save query history to a local SQLite database.
7. Provide a web interface with voice input capabilities.

## 🛠️ Technologies Used
- **Programming Language:** Python 3
- **NLP Concepts:** Semantic Parsing, Language Detection, Text Preprocessing.
- **Web Server:** Python `http.server` (Built-in)
- **Frontend:** HTML5, CSS3, JavaScript (Voice Recognition API)
- **Database:** SQLite3 (Built-in)
- **Data Handling:** Python `csv` module

## 📂 Project Structure
```text
agrivoiceAI/
│
├── app.py                     # (Legacy) Streamlit prototype
├── web_app.py                 # Main Web Server (Run this!)
├── run_local.py               # Terminal version of the app
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
│
├── modules/                   # The NLP Brain
│   ├── language_detection.py  # Detects Telugu, Hindi, or English
│   ├── text_preprocessing.py  # Cleans input text
│   ├── semantic_parser.py     # Extracts Crop and Symptom
│   ├── recommendation_engine.py # Fetches data from CSV
│   ├── translator.py          # Translates output to regional languages
│   └── database_manager.py    # Handles SQLite database operations
│
├── dataset/                   # Verified Agricultural Knowledge Base
│   ├── crop_problems.csv      # Contains causes and solutions
│   └── follow_up_questions.csv# Contains follow-up questions
│
└── database/                  # SQLite Database Folder
    └── agri_history.db        # Auto-generated query history