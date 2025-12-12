from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import requests
import json
import sqlite3
import google.generativeai as genai
from datetime import datetime
import io
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

# Database setup
def init_db():
    conn = sqlite3.connect('blogs.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS blogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            content TEXT NOT NULL,
            research_gaps TEXT,
            research_questions TEXT,
            methodology TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# API Functions (from api.py)
def call_research_gaps_api(topic):
    """Step 1: Get research gaps from local API"""
    url = "http://127.0.0.1:8000/researchgap"
    params = {"query": topic}
    
    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Research Gaps API: {e}")
        return {}

def call_external_questions_api(topic, gaps):
    """Step 2: Generate research questions from gaps"""
    if not gaps or "gaps" not in gaps or len(gaps["gaps"]) == 0:
        return {}
    
    gaps_payload = [
        {
            "gap_id": f"gap_{i+1}",
            "description": gap["statement"],
            "category": "methodological_gap"
        }
        for i, gap in enumerate(gaps["gaps"])
    ]
    
    url = f"https://spm-production.up.railway.app/generateQuestions?topic={topic}"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(gaps_payload), timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Questions API: {e}")
        return {}

def call_methodology_api(question_data):
    """Step 3: Get research methodology"""
    if not question_data or "data" not in question_data:
        return {}
    
    main_question = question_data["data"]["main_question"]
    sub_questions = question_data["data"]["sub_questions"]
    
    url = "http://127.0.0.1:5000/api/analyze-questions"
    payload = {
        "main_question": main_question,
        "sub_questions": sub_questions
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Methodology API: {e}")
        return {}

def generate_blog_with_gemini(topic, gaps_data, questions_data, methodology_data):
    """Transform research data into blog format using Gemini"""
    
    # Prepare the prompt with all collected data
    prompt = f"""
You are an expert technical writer. Transform the following research data into a well-structured, engaging blog post.

Topic: {topic}

Research Gaps:
{json.dumps(gaps_data, indent=2)}

Research Questions:
{json.dumps(questions_data, indent=2)}

Research Methodology:
{json.dumps(methodology_data, indent=2)}

Create a comprehensive blog post with the following structure:
1. Title (catchy and relevant)
2. Introduction (engaging hook about the topic)
3. Current Research Landscape (discuss the gaps identified in flowing paragraph format)
4. Key Research Questions (write the main question and sub-questions as flowing narrative paragraphs, NOT as bullet points or lists. Weave them naturally into the text)
5. Proposed Methodology (explain the research approach in paragraph format)
6. Potential Impact (discuss implications and future directions)
7. Conclusion (summarize key takeaways)

IMPORTANT FORMATTING RULES:
- Use markdown formatting with proper headings (# ## ###)
- Write ALL content in flowing paragraphs, NOT bullet points or numbered lists
- When presenting research questions, integrate them smoothly into narrative paragraphs
- Make it professional yet accessible
- Include relevant insights and connections between the data points
- DO NOT use bullet points (•, -, *) or numbered lists (1., 2., 3.) anywhere in the blog
"""

    try:
        if not GEMINI_API_KEY:
            # Fallback: Generate basic blog without Gemini
            return generate_basic_blog(topic, gaps_data, questions_data, methodology_data)
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating blog with Gemini: {e}")
        return generate_basic_blog(topic, gaps_data, questions_data, methodology_data)

def generate_basic_blog(topic, gaps_data, questions_data, methodology_data):
    """Fallback blog generation without Gemini - using narrative paragraph format"""
    blog = f"# Research Blog: {topic.title()}\n\n"
    blog += f"*Generated on {datetime.now().strftime('%B %d, %Y')}*\n\n"
    
    blog += "## Introduction\n\n"
    blog += f"This blog explores the current state of research in {topic}, identifying key gaps and proposing research directions. "
    blog += f"Through a comprehensive analysis of the research landscape, we examine critical areas requiring further investigation "
    blog += f"and outline a methodological framework for advancing knowledge in this domain.\n\n"
    
    if gaps_data and "gaps" in gaps_data:
        blog += "## Research Gaps Identified\n\n"
        blog += f"The current research landscape in {topic} reveals several critical gaps that warrant attention. "
        for i, gap in enumerate(gaps_data["gaps"], 1):
            statement = gap.get('statement', 'N/A')
            reasoning = gap.get('reasoning', 'N/A')
            blog += f"Notably, {statement.lower() if i > 1 else statement} "
            blog += f"This gap is significant because {reasoning.lower() if reasoning.endswith('.') else reasoning}. "
        blog += "These identified gaps collectively point to the need for more comprehensive research approaches in this field.\n\n"
    
    if questions_data and "data" in questions_data:
        blog += "## Research Questions\n\n"
        main_q = questions_data['data'].get('main_question', 'N/A')
        sub_qs = questions_data['data'].get('sub_questions', [])
        
        blog += f"To address these research gaps, our investigation centers on the following inquiry: {main_q} "
        blog += f"This overarching question encompasses several important dimensions. "
        
        if sub_qs:
            blog += "Specifically, we seek to understand "
            for i, sq in enumerate(sub_qs):
                if i == 0:
                    blog += f"{sq.lower() if sq[0].isupper() else sq}"
                elif i == len(sub_qs) - 1:
                    blog += f", and {sq.lower() if sq[0].isupper() else sq}"
                else:
                    blog += f", {sq.lower() if sq[0].isupper() else sq}"
            blog += ". These interconnected questions form the foundation of our research framework and guide our methodological approach.\n\n"
    
    if methodology_data and "data" in methodology_data:
        blog += "## Research Methodology\n\n"
        method_info = methodology_data.get('data', {}).get('methodology', {})
        if method_info:
            rec_method = method_info.get('recommended_methodology', 'comprehensive research approach')
            justification = method_info.get('justification', '')
            study_design = method_info.get('study_design', '')
            
            blog += f"Our research employs a {rec_method} to address the identified questions and gaps. "
            if justification:
                blog += f"{justification} "
            if study_design:
                blog += f"{study_design} "
            blog += "This methodological framework ensures rigor and validity in our investigation.\n\n"
        else:
            blog += "A comprehensive research methodology will be employed to address the identified questions and gaps.\n\n"
    
    blog += "## Conclusion\n\n"
    blog += f"This research framework provides a comprehensive approach to advancing knowledge in {topic}. "
    blog += "By addressing the identified gaps through well-defined research questions and a robust methodology, "
    blog += "this work aims to contribute meaningfully to the field and open new avenues for future investigation.\n"
    
    return blog

@app.route('/')
def index():
    """Serve the landing page"""
    return render_template('index.html')

@app.route('/api/generate-blog', methods=['POST'])
def generate_blog():
    """Main endpoint to generate blog from topic"""
    data = request.json
    topic = data.get('topic', '')
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    try:
        # Step 1: Get research gaps
        gaps_data = call_research_gaps_api(topic)
        if not gaps_data:
            return jsonify({'error': 'Failed to fetch research gaps'}), 500
        
        # Step 2: Generate research questions
        questions_data = call_external_questions_api(topic, gaps_data)
        if not questions_data:
            return jsonify({'error': 'Failed to generate research questions'}), 500
        
        # Step 3: Get methodology
        methodology_data = call_methodology_api(questions_data)
        
        # Step 4: Generate blog with Gemini
        blog_content = generate_blog_with_gemini(topic, gaps_data, questions_data, methodology_data)
        
        # Save to database
        conn = sqlite3.connect('blogs.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO blogs (topic, content, research_gaps, research_questions, methodology)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            topic,
            blog_content,
            json.dumps(gaps_data),
            json.dumps(questions_data),
            json.dumps(methodology_data)
        ))
        blog_id = c.lastrowid
        conn.commit()
        conn.close()
        
        # Save gaps and methodology as separate JSON files
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        
        # Create safe filename from topic
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_topic = safe_topic.replace(' ', '_')
        
        # Save gaps as JSON
        gaps_filename = os.path.join(output_dir, f"{safe_topic}_gaps.json")
        with open(gaps_filename, 'w', encoding='utf-8') as f:
            json.dump(gaps_data, f, indent=2, ensure_ascii=False)
        
        # Save methodology as JSON
        methodology_filename = os.path.join(output_dir, f"{safe_topic}_methodology.json")
        with open(methodology_filename, 'w', encoding='utf-8') as f:
            json.dump(methodology_data, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'success': True,
            'blog_id': blog_id,
            'content': blog_content,
            'gaps': gaps_data,
            'questions': questions_data,
            'methodology': methodology_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blogs', methods=['GET'])
def get_blogs():
    """Get all saved blogs"""
    conn = sqlite3.connect('blogs.db')
    c = conn.cursor()
    c.execute('SELECT id, topic, created_at FROM blogs ORDER BY created_at DESC')
    blogs = [{'id': row[0], 'topic': row[1], 'created_at': row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify({'blogs': blogs})

@app.route('/api/blogs/<int:blog_id>', methods=['GET'])
def get_blog(blog_id):
    """Get a specific blog"""
    conn = sqlite3.connect('blogs.db')
    c = conn.cursor()
    c.execute('SELECT * FROM blogs WHERE id = ?', (blog_id,))
    row = c.fetchone()
    conn.close()
    
    if not row:
        return jsonify({'error': 'Blog not found'}), 404
    
    return jsonify({
        'id': row[0],
        'topic': row[1],
        'content': row[2],
        'research_gaps': json.loads(row[3]),
        'research_questions': json.loads(row[4]),
        'methodology': json.loads(row[5]) if row[5] else {},
        'created_at': row[6]
    })

@app.route('/api/blogs/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    """Update blog content"""
    data = request.json
    content = data.get('content', '')
    
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    
    conn = sqlite3.connect('blogs.db')
    c = conn.cursor()
    
    # Check if blog exists
    c.execute('SELECT id FROM blogs WHERE id = ?', (blog_id,))
    if not c.fetchone():
        conn.close()
        return jsonify({'error': 'Blog not found'}), 404
    
    # Update blog
    c.execute('UPDATE blogs SET content = ? WHERE id = ?', (content, blog_id))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Blog updated successfully'})

@app.route('/api/blogs/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    """Delete a blog"""
    conn = sqlite3.connect('blogs.db')
    c = conn.cursor()
    
    # Check if blog exists
    c.execute('SELECT id FROM blogs WHERE id = ?', (blog_id,))
    if not c.fetchone():
        conn.close()
        return jsonify({'error': 'Blog not found'}), 404
    
    # Delete blog
    c.execute('DELETE FROM blogs WHERE id = ?', (blog_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Blog deleted successfully'})

@app.route('/api/blogs/<int:blog_id>/download', methods=['GET'])
def download_blog(blog_id):
    """Download blog as markdown file"""
    conn = sqlite3.connect('blogs.db')
    c = conn.cursor()
    c.execute('SELECT topic, content FROM blogs WHERE id = ?', (blog_id,))
    row = c.fetchone()
    conn.close()
    
    if not row:
        return jsonify({'error': 'Blog not found'}), 404
    
    topic, content = row
    
    # Create markdown file
    filename = f"{topic.replace(' ', '_')}_blog.md"
    buffer = io.BytesIO()
    buffer.write(content.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='text/markdown'
    )

@app.route('/api/progress/<string:step>', methods=['POST'])
def update_progress(step):
    """Endpoint for progress updates (for future websocket implementation)"""
    return jsonify({'status': 'acknowledged', 'step': step})

if __name__ == '__main__':
    app.run(debug=True, port=3000)
