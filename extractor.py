import re
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Structured Database based on the provided timetable image
TIMETABLE = [
    # 17/03/2026 (Tuesday)
    {"date": "17/03/2026", "day": "tuesday", "shift": "I", "time": "9:30 AM to 10:30 AM", "semester": "4", "course": "Microcontrollers and Embedded Systems"},
    {"date": "17/03/2026", "day": "tuesday", "shift": "I", "time": "9:30 AM to 10:30 AM", "semester": "6", "course": "Introduction to Android Programming"},
    {"date": "17/03/2026", "day": "tuesday", "shift": "II", "time": "11:30 AM to 12:30 PM", "semester": "2", "course": "Aptitude and Reasoning- II"},
    {"date": "17/03/2026", "day": "tuesday", "shift": "III", "time": "1:30 PM to 2:30 PM", "semester": "4", "course": "Flexi-Credit Course (Java)"},
    {"date": "17/03/2026", "day": "tuesday", "shift": "III", "time": "1:30 PM to 2:30 PM", "semester": "6", "course": "Elective - I (HCI/IMLDS/CCTT/OSTCSF)"},
    {"date": "17/03/2026", "day": "tuesday", "shift": "IV", "time": "3:30 PM to 4:30 PM", "semester": "2", "course": "Statistics and Probability"},

    # 18/03/2026 (Wednesday)
    {"date": "18/03/2026", "day": "wednesday", "shift": "I", "time": "9:30 AM to 10:30 AM", "semester": "4", "course": "Database Management Systems"},
    {"date": "18/03/2026", "day": "wednesday", "shift": "I", "time": "9:30 AM to 10:30 AM", "semester": "6", "course": "Elective- II (BDDC/NNDS/MWS)"},
    {"date": "18/03/2026", "day": "wednesday", "shift": "II", "time": "11:30 AM to 12:30 PM", "semester": "2", "course": "Digital Electronics and Logic Design"},
    {"date": "18/03/2026", "day": "wednesday", "shift": "III", "time": "1:30 PM to 2:30 PM", "semester": "4", "course": "Operating Systems"},
    {"date": "18/03/2026", "day": "wednesday", "shift": "III", "time": "1:30 PM to 2:30 PM", "semester": "6", "course": "Elective- III (DIP/AIoT/MA/NCDWS)"},
    {"date": "18/03/2026", "day": "wednesday", "shift": "IV", "time": "3:30 PM to 4:30 PM", "semester": "2", "course": "Data Structures"},

    # 20/03/2026 (Friday)
    {"date": "20/03/2026", "day": "friday", "shift": "I", "time": "9:30 AM to 10:30 AM", "semester": "4", "course": "Theory of Computation"},
    {"date": "20/03/2026", "day": "friday", "shift": "I", "time": "9:30 AM to 10:30 AM", "semester": "6", "course": "Specialisation-AIML-Pattern Recognition / DS-Data Analysis and Visualization"},
    {"date": "20/03/2026", "day": "friday", "shift": "I", "time": "9:30 AM to 10:30 AM", "semester": "8", "course": "Internship-Seminar"},
    {"date": "20/03/2026", "day": "friday", "shift": "II", "time": "11:30 AM to 12:30 PM", "semester": "2", "course": "Nanotechnology"},
    {"date": "20/03/2026", "day": "friday", "shift": "II", "time": "11:30 AM to 12:30 PM", "semester": "2", "course": "Physics for Quantum Computing"},
    {"date": "20/03/2026", "day": "friday", "shift": "III", "time": "1:30 PM to 2:30 PM", "semester": "4", "course": "Specialisation- Neural Networks/ Data Warehouse"},
    {"date": "20/03/2026", "day": "friday", "shift": "III", "time": "1:30 PM to 2:30 PM", "semester": "6", "course": "Flexi-Credit Course (Service Now)"},
    {"date": "20/03/2026", "day": "friday", "shift": "IV", "time": "3:30 PM to 4:30 PM", "semester": "2", "course": "Programming and Problem Solving"},
]

# Aliases to match natural language course names to official names
COURSE_ALIASES = {
    'microcontrollers': 'Microcontrollers and Embedded Systems',
    'embedded systems': 'Microcontrollers and Embedded Systems',
    'android': 'Introduction to Android Programming',
    'aptitude': 'Aptitude and Reasoning- II',
    'reasoning': 'Aptitude and Reasoning- II',
    'statistics': 'Statistics and Probability',
    'probability': 'Statistics and Probability',
    'database': 'Database Management Systems',
    'dbms': 'Database Management Systems',
    'digital electronics': 'Digital Electronics and Logic Design',
    'logic design': 'Digital Electronics and Logic Design',
    'operating systems': 'Operating Systems',
    'os': 'Operating Systems',
    'data structures': 'Data Structures',
    'dsa': 'Data Structures',
    'theory of computation': 'Theory of Computation',
    'toc': 'Theory of Computation',
    'machine learning': 'Specialisation-AIML-Pattern Recognition / DS-Data Analysis and Visualization',
    'aiml': 'Specialisation-AIML-Pattern Recognition / DS-Data Analysis and Visualization',
    'pattern recognition': 'Specialisation-AIML-Pattern Recognition / DS-Data Analysis and Visualization',
    'data science': 'Specialisation-AIML-Pattern Recognition / DS-Data Analysis and Visualization',
    'data analysis': 'Specialisation-AIML-Pattern Recognition / DS-Data Analysis and Visualization',
    'internship': 'Internship-Seminar',
    'seminar': 'Internship-Seminar',
    'nanotechnology': 'Nanotechnology',
    'physics': 'Physics for Quantum Computing',
    'quantum computing': 'Physics for Quantum Computing',
    'neural networks': 'Specialisation- Neural Networks/ Data Warehouse',
    'data warehouse': 'Specialisation- Neural Networks/ Data Warehouse',
    'service now': 'Flexi-Credit Course (Service Now)',
    'programming and problem solving': 'Programming and Problem Solving',
    'java': 'Flexi-Credit Course (Java)',
    'elective 1': 'Elective - I (HCI/IMLDS/CCTT/OSTCSF)',
    'elective i': 'Elective - I (HCI/IMLDS/CCTT/OSTCSF)',
    'elective 2': 'Elective- II (BDDC/NNDS/MWS)',
    'elective ii': 'Elective- II (BDDC/NNDS/MWS)',
    'elective 3': 'Elective- III (DIP/AIoT/MA/NCDWS)',
    'elective iii': 'Elective- III (DIP/AIoT/MA/NCDWS)',
}

def extract_entities(text):
    text_lower = text.lower()
    entities = {
        'semester': None,
        'course': None,
        'date': None
    }
    
    # 1. Extract Semester (e.g., SEM 5, Semester 3, Sem 1)
    # Also considering Roman numerals (e.g., Semester-II)
    sem_match = re.search(r'(?i)\bsem(?:ester)?\s*[-_]?\s*([ivx]+|\d+)\b', text)
    if sem_match:
        val = sem_match.group(1).upper()
        # Convert roman to digit if needed
        roman_to_digit = {'I': '1', 'II': '2', 'III': '3', 'IV': '4', 'V': '5', 'VI': '6', 'VII': '7', 'VIII': '8'}
        entities['semester'] = roman_to_digit.get(val, val)
        
    # 2. Extract Course using Aliases
    for alias, official in COURSE_ALIASES.items():
        if re.search(r'\b' + re.escape(alias) + r'\b', text_lower):
            entities['course'] = official
            break
            
    if not entities['course']:
        # Try finding exact matches directly
        for tt in TIMETABLE:
            if tt['course'].lower() in text_lower:
                entities['course'] = tt['course']
                break

    # 3. Extract Date or Day
    date_match = re.search(r'\b(\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?)\b', text)
    if date_match:
        # Standardize assumption that missing year refers to 2026 as per timetable
        d = date_match.group(1)
        if len(d.split('/')) == 2 or len(d.split('-')) == 2:
            d = d.replace('-', '/') + "/2026"
        entities['date'] = d
    else:
        # Check for days of the week explicitly mapped
        for day in ['tuesday', 'wednesday', 'friday', '17th', '18th', '20th']:
            if day in text_lower:
                if '17' in day or 'tuesday' in day:
                    entities['date'] = '17/03/2026'
                elif '18' in day or 'wednesday' in day:
                    entities['date'] = '18/03/2026'
                elif '20' in day or 'friday' in day:
                    entities['date'] = '20/03/2026'
                break
                
    return entities

def generate_response(question):
    entities = extract_entities(question)
    
    # Query database
    results = []
    for entry in TIMETABLE:
        match = True
        
        # If the user specified a semester, verify it matches
        if entities['semester'] and entry['semester'] != entities['semester']:
            match = False
            
        # If the user specified a course, verify it matches
        if entities['course'] and entry['course'] != entities['course']:
            match = False
            
        # If the user specified a date, verify it matches
        if entities['date'] and entry['date'] != entities['date']:
            match = False
            
        if match:
             results.append(entry)
             
    # If no entities were found in the text, ask to specify
    if not entities['semester'] and not entities['course'] and not entities['date']:
         return "Could you specify a semester number, a course name, or a date (e.g., Tuesday) to check the real schedule?"

    if not results:
         # To be helpful, mention what we looked up
         looked_up = [f"Semester {entities['semester']}" if entities['semester'] else "",
                      entities['course'] if entities['course'] else "",
                      f"on {entities['date']}" if entities['date'] else ""]
         lookup_str = " ".join([x for x in looked_up if x])
         return f"I couldn't find any exams matching <b>{lookup_str}</b> in the timetable."
         
    response_lines = ["<strong>Here are the exam details matching your query:</strong><br><br><ul style='list-style-type: none; padding-left: 0;'>"]
    for res in results:
         response_lines.append(
             f"<li style='margin-bottom: 15px; background: #fff; padding: 15px; border-radius: 8px; border-left: 5px solid #2ecc71; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>"
             f"<strong>Semester {res['semester']}</strong> — {res['course']} <br>"
             f"📅 <strong>Date:</strong> {res['date']} ({res['day'].capitalize()}) <br>"
             f"⏰ <strong>Time:</strong> {res['time']} (Shift {res['shift']})"
             f"</li>"
         )
    response_lines.append("</ul>")
    
    return "".join(response_lines)


@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    question = None
    entities = None
    
    if request.method == "POST":
        question = request.form.get("question")
        if question:
            response = generate_response(question)
            entities = extract_entities(question)
            
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>University Exam Scheduler</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 800px; margin: 0 auto; padding: 40px 20px; background-color: #f7f9fc; color: #333; }
            .card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; margin-top: 0; }
            input[type="text"] { width: 100%; padding: 12px; margin: 15px 0; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; font-size: 16px; }
            button { background-color: #3498db; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; transition: background 0.3s; }
            button:hover { background-color: #2980b9; }
            .result { margin-top: 30px; padding: 20px; background: #ecf0f1; border-radius: 8px; border-left: 5px solid #3498db; }
            .entities { margin-top: 15px; font-size: 0.9em; font-family: monospace; background: #e0e6ed; padding: 10px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>📄 Real Timetable Q/A Window
            </h1>
            <p>Ask a question based on <strong>Semester II, IV, VI, VIII Timetable</strong> details.</p>
            <form method="POST">
                <input type="text" name="question" placeholder="e.g. When is the DBMS exam?" required value="{{ question or '' }}">
                <button type="submit">Ask Chatbot</button>
            </form>
            
            {% if response %}
                <div class="result">
                    <strong>🤖 Bot Response:</strong>
                    <div style="font-size: 1.05em; color: #2c3e50; margin: 10px 0;">{{ response | safe }}</div>
                    
                    <div class="entities">
                        <strong>Debug Info - Extracted Entities:</strong><br>
                        Semester: <span style="color: #c0392b;">{{ entities.semester or 'None' }}</span><br>
                        Course: <span style="color: #2980b9;">{{ entities.course or 'None' }}</span><br>
                        Date Match: <span style="color: #27ae60;">{{ entities.date or 'None' }}</span>
                    </div>
                </div>
            {% endif %}
            
            <div style="margin-top: 30px; font-size: 0.9em; color: #7f8c8d;">
                <strong>Sample Queries:</strong>
                <ul>
                    <li>What exams are on Tuesday?</li>
                    <li>When is Operating Systems?</li>
                    <li>What exams does semester 2 have on 20th?</li>
                    <li>Is there an Android exam?</li>
                    <li>Timetable for TOC?</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, response=response, question=question, entities=entities)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
