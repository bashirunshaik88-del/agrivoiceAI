import http.server
import socketserver
import urllib.parse
import sys
import os
import uuid
import email
import email.policy
import http.cookies

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from modules.language_detection import detect_language
from modules.text_preprocessing import clean_text
from modules.semantic_parser import extract_agricultural_entities
from modules.recommendation_engine import get_recommendation, get_follow_up_questions
from modules.database_manager import initialize_database, save_query, get_all_history
from modules.translator import translate_to_language

os.makedirs("uploads", exist_ok=True)
PORT = int(os.environ.get("PORT", 8000))

# ---------------- HTML TEMPLATES ----------------

HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AgriVoice AI 🌾</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: url('https://images.unsplash.com/photo-1625246333195-78d9c38ad449?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80') no-repeat center center fixed; background-size: cover; margin: 0; padding: 0; }
        .overlay { background-color: rgba(0, 0, 0, 0.6); height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; color: white; text-align: center; }
        h1 { font-size: 4em; margin-bottom: 10px; text-shadow: 2px 2px 4px #000; }
        p { font-size: 1.5em; margin-bottom: 40px; text-shadow: 1px 1px 2px #000; }
        .btn { background-color: #2e7d32; color: white; padding: 15px 40px; text-decoration: none; font-size: 1.2em; border-radius: 5px; transition: 0.3s; }
        .btn:hover { background-color: #1b5e20; }
    </style>
</head>
<body>
    <div class="overlay">
        <h1>🌾 AgriVoice AI</h1>
        <p>Multilingual Farmer Problem Understanding System</p>
        <a href="/login" class="btn">Get Started 🚀</a>
    </div>
</body>
</html>
"""

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Login - AgriVoice AI</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f4f9f4; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-box { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; width: 300px; }
        h2 { color: #2e7d32; margin-bottom: 20px; }
        input[type="text"] { width: 90%; padding: 10px; margin-bottom: 20px; border: 1px solid #ccc; border-radius: 5px; }
        .btn { background-color: #2e7d32; color: white; padding: 10px 20px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; width: 100%; }
        .btn:hover { background-color: #1b5e20; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>👨‍🌾 Farmer Login</h2>
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Enter your name" required>
            <button type="submit" class="btn">Login</button>
        </form>
    </div>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AgriVoice AI Dashboard 🌾</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background-color: #f4f9f4; margin: 0; padding: 0; }}
        .header {{ background-color: #2e7d32; color: white; padding: 20px; text-align: center; position: relative; }}
        .logout-btn {{ position: absolute; top: 20px; right: 20px; background-color: #d32f2f; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; font-size: 14px; }}
        .container {{ width: 80%; margin: 30px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        textarea {{ width: 100%; height: 100px; padding: 10px; border: 2px solid #2e7d32; border-radius: 5px; font-size: 16px; box-sizing: border-box; }}
        .btn {{ background-color: #2e7d32; color: white; padding: 12px 24px; border: none; border-radius: 5px; font-size: 18px; cursor: pointer; margin-top: 10px; }}
        .btn:hover {{ background-color: #1b5e20; }}
        .mic-btn {{ background-color: #d32f2f; color: white; padding: 10px; border: none; border-radius: 50%; cursor: pointer; margin-bottom: 10px; font-size: 20px; }}
        .result-box {{ margin-top: 20px; padding: 20px; background-color: #e8f5e9; border-left: 5px solid #2e7d32; border-radius: 5px; }}
        .error-box {{ margin-top: 20px; padding: 20px; background-color: #ffebee; border-left: 5px solid #c62828; border-radius: 5px; }}
        .question {{ color: #0277bd; font-weight: bold; }}
        .action {{ color: #2e7d32; font-weight: bold; }}
        .precaution {{ color: #c62828; font-weight: bold; }}
        .uploaded-img {{ max-width: 300px; height: auto; border-radius: 8px; margin-top: 10px; border: 2px solid #2e7d32; display: block; }}
        .history-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 14px; }}
        .history-table th, .history-table td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
        .history-table th {{ background-color: #2e7d32; color: white; }}
        .history-table tr:nth-child(even) {{ background-color: #f9f9f9; }}
    </style>
    <script>
        function startVoice() {{
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
                var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                recognition.lang = document.getElementById('lang_select').value === 'Telugu' ? 'te-IN' : 
                                   document.getElementById('lang_select').value === 'Hindi' ? 'hi-IN' : 'en-US';
                recognition.onresult = function(event) {{
                    document.getElementById('farmer_input').value = event.results[0][0].transcript;
                }};
                recognition.start();
            }} else {{
                alert("Your browser does not support voice recognition. Please use Google Chrome.");
            }}
        }}
    </script>
</head>
<body>
    <div class="header">
        <h1>🌾 AgriVoice AI Dashboard</h1>
        <p>Welcome, {username}!</p>
        <a href="/logout" class="logout-btn">Logout</a>
    </div>
    <div class="container">
        <h3>Describe your crop problem:</h3>
        <form method="POST" action="/dashboard" enctype="multipart/form-data">
            <label>Select Output Language: </label>
            <select name="target_lang" id="lang_select">
                <option value="English">English</option>
                <option value="Telugu">తెలుగు (Telugu)</option>
                <option value="Hindi">हिंदी (Hindi)</option>
            </select>
            <br><br>
            <button type="button" class="mic-btn" onclick="startVoice()" title="Speak">🎤</button>
            <span style="font-size: 14px; color: #666;">(Click mic to speak)</span>
            <br><br>
            <textarea name="farmer_input" id="farmer_input" placeholder="Example: My cotton crop leaves are turning yellow.">{previous_input}</textarea>
            <br><br>
            <label>📷 Upload a photo of the crop (Optional): </label>
            <input type="file" name="crop_image" accept="image/*">
            <br><br>
            <button type="submit" class="btn">Analyze Problem</button>
        </form>
        
        {result_html}
        
        <hr style="margin-top: 40px; border: 1px solid #ccc;">
        <h3>📚 Recent Query History (From SQLite Database)</h3>
        {history_html}
    </div>
</body>
</html>
"""

# ---------------- HELPER FUNCTIONS ----------------

def generate_history_html():
    history = get_all_history()
    if not history:
        return "<p>No queries found yet.</p>"
    html = '<table class="history-table"><tr><th>Date & Time</th><th>Language</th><th>Crop</th><th>Symptom</th><th>Original Query</th></tr>'
    for row in history:
        html += f'<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>'
    html += '</table>'
    return html

def get_user_from_cookie(handler):
    cookie_header = handler.headers.get('Cookie')
    if cookie_header:
        cookie = http.cookies.SimpleCookie(cookie_header)
        if 'username' in cookie:
            return cookie['username'].value
    return None

# ---------------- MAIN SERVER HANDLER ----------------

class AgriVoiceHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HOME_TEMPLATE.encode('utf-8'))
            
        elif self.path == '/login':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(LOGIN_TEMPLATE.encode('utf-8'))
            
        elif self.path == '/logout':
            self.send_response(302)
            self.send_header('Set-Cookie', 'username=; expires=Thu, 01 Jan 1970 00:00:00 GMT')
            self.send_header('Location', '/')
            self.end_headers()
            
        elif self.path == '/dashboard':
            username = get_user_from_cookie(self)
            if not username:
                self.send_response(302)
                self.send_header('Location', '/login')
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                html = DASHBOARD_TEMPLATE.format(
                    username=username, 
                    previous_input="", 
                    result_html="", 
                    history_html=generate_history_html()
                )
                self.wfile.write(html.encode('utf-8'))
                
        elif self.path.startswith('/uploads/'):
            filename = self.path.split('/')[-1]
            filepath = os.path.join("uploads", filename)
            if os.path.exists(filepath):
                self.send_response(200)
                self.send_header("Content-type", "image/jpeg")
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404)
                
        else:
            self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        content_type = self.headers['Content-Type']
        raw_data = self.rfile.read(content_length)
        
        if self.path == '/login':
            params = urllib.parse.parse_qs(raw_data.decode('utf-8'))
            username = params.get('username', ['Farmer'])[0]
            self.send_response(302)
            self.send_header('Set-Cookie', f'username={username}')
            self.send_header('Location', '/dashboard')
            self.end_headers()
            return

        if self.path == '/dashboard':
            username = get_user_from_cookie(self)
            if not username:
                self.send_response(302)
                self.send_header('Location', '/login')
                self.end_headers()
                return

            msg = email.message_from_bytes(f"Content-Type: {content_type}\r\n\r\n".encode('utf-8') + raw_data, policy=email.policy.default)
            
            farmer_input = ""
            target_lang = "English"
            image_html = ""

            for part in msg.iter_parts():
                name = part.get_param('name', header='content-disposition')
                if not name: continue
                    
                if name == 'farmer_input':
                    farmer_input = part.get_payload(decode=True).decode('utf-8')
                elif name == 'target_lang':
                    target_lang = part.get_payload(decode=True).decode('utf-8')
                elif name == 'crop_image':
                    file_data = part.get_payload(decode=True)
                    filename = part.get_filename()
                    if file_data and filename:
                        unique_filename = f"img_{uuid.uuid4().hex[:8]}.jpg"
                        filepath = os.path.join("uploads", unique_filename)
                        with open(filepath, 'wb') as f:
                            f.write(file_data)
                        image_html = f'<br><img src="/uploads/{unique_filename}" class="uploaded-img" alt="Uploaded Crop Image">'

            result_html = ""
            if farmer_input.strip():
                lang = detect_language(farmer_input)
                clean_input = clean_text(farmer_input)
                parsed = extract_agricultural_entities(clean_input)
                crop = parsed['Crop']
                symptom = parsed['Symptom']
                
                save_query(lang, crop, symptom, farmer_input)

                if crop != "Unknown" and symptom == "Unknown":
                    result_html = f"""
                    <div class="result-box" style="border-left: 5px solid #f57c00; background-color: #fff3e0;">
                        <h3>🤔 Clarification Needed</h3>
                        <p>Language Detected: <b>{lang}</b></p>
                        <p>Crop Identified: <b>{crop}</b></p>
                        <p>I see you have a <b>{crop}</b> crop, but I didn't catch the specific problem.</p>
                        <p>Could you please specify the symptom? (e.g., "yellow leaves", "spots", "poor growth").</p>
                        {image_html}
                    </div>
                    """
                elif crop == "Unknown" or symptom == "Unknown":
                    result_html = f"""
                    <div class="error-box">
                        <h3>⚠️ Analysis Result</h3>
                        <p>Language Detected: <b>{lang}</b></p>
                        <p>Sorry, I could not understand the crop or the problem. Please try rephrasing your sentence.</p>
                        {image_html}
                    </div>
                    """
                else:
                    questions = get_follow_up_questions(crop, symptom)
                    rec = get_recommendation(crop, symptom)
                    
                    q_html = ""
                    if questions:
                        q1 = translate_to_language(questions[0], target_lang)
                        q2 = translate_to_language(questions[1], target_lang)
                        q_html = f"<p class='question'>🩺 Q1: {q1}</p><p class='question'>🩺 Q2: {q2}</p>"
                    
                    rec_html = ""
                    if rec:
                        cause = translate_to_language(rec['cause'], target_lang)
                        action = translate_to_language(rec['action'], target_lang)
                        precaution = translate_to_language(rec['precaution'], target_lang)
                        rec_html = f"<p><b>Possible Cause:</b> {cause}</p><p class='action'>✅ Recommended Action: {action}</p><p class='precaution'>⚠️ Precaution: {precaution}</p>"
                    else:
                        rec_html = "<p>No exact verified solution found. Please consult an expert.</p>"

                    result_html = f"""
                    <div class="result-box">
                        <h3>🎯 Analysis Result</h3>
                        <p>Language Detected: <b>{lang}</b></p>
                        <p>Crop Identified: <b>{crop}</b></p>
                        <p>Problem Identified: <b>{symptom}</b></p>
                        {image_html}
                        <hr>{q_html}<hr>
                        <h4>Verified Recommendation:</h4>{rec_html}
                    </div>
                    """

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html = DASHBOARD_TEMPLATE.format(
                username=username, 
                previous_input=farmer_input, 
                result_html=result_html, 
                history_html=generate_history_html()
            )
            self.wfile.write(html.encode('utf-8'))

if __name__ == "__main__":
    initialize_database()
    print("="*50)
    print("🌾 AgriVoice AI Web Server with Login is Running!")
    print("👉 Open your browser and go to: http://localhost:8000")
    print("="*50)
    with socketserver.TCPServer(("", PORT), AgriVoiceHandler) as httpd:
        httpd.serve_forever()