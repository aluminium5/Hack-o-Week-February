# Entity Extractor & Exam Schedule Chatbot

*Made for the month of February as a Hack-o-Week problem statement... Made by Ishika Dubey, Samruddhi, and Atharv Lulekar for hands-on project experience.*

This project is a Flask-based chatbot application designed to parse standard exam-related queries using natural language processing (specifically Entity Extraction) and match them against a structured university timetable database.

## Features

- **Entity Extraction:** Identifies entities such as "Semester", "Course Names", and "Dates/Days" from unstructured user questions using regular expressions and alias mapping.
- **Alias Mapping:** Understanding of various ways students refer to courses (e.g., "OS" = "Operating Systems", "DBMS" = "Database Management Systems").
- **Smart Response Generation:** Cross-references the extracted entities with a hardcoded timetable (based on Semesters II, IV, VI, VIII) to return accurately scheduled exam dates, times, and shifts.
- **Interactive UI:** Provides a simple, clean web interface to test queries locally.
- **Debug View:** Displays what the entity extractor identified (Semester, Course, Date) below the bot's response to help understand how the AI parses the query.

## Prerequisites

- Python 3.6 or higher
- Flask

## Installation & Setup

1. **Install Flask** if you haven't already:
   ```bash
   pip install flask
   ```

2. **Run the application:**
   ```bash
   python extractor.py
   ```

3. **Open the web application:**
   Open your browser and navigate to the local server link:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Sample Queries to Try

- "What exams are on Tuesday?"
- "When is Operating Systems?"
- "What exams does semester 2 have on 20th?"
- "Is there an Android exam?"
- "Timetable for TOC?"
- "When is the DBMS exam?"
- "Show me semester 4 exams on 18th March."

## How it works (Entity Extraction)

The `extract_entities(text)` function analyzes user text:
1. **Semester Matching:** Uses regex to look for "sem", "semester", followed by a digit or Roman numeral (e.g., "Sem 2", "Semester-IV").
2. **Course Matching:** Iterates through a dictionary of `COURSE_ALIASES` to map natural language input (like "machine learning") to official specific courses (like "Specialisation-AIML-Pattern Recognition").
3. **Date/Day Matching:** Extracts explicit dates (like "15/03/2026") or maps days of the week ("Tuesday") to standard dates referencing the actual timetable.
