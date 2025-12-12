# Research Blog Generator

An interactive web application that transforms research data into compelling blog posts using AI. The system integrates multiple APIs to gather research gaps, generate questions, determine methodology, and uses Google's Gemini API to create well-structured blogs.

## Features

- 🔍 **Multi-API Integration**: Calls research gaps API, questions generation API, and methodology API sequentially
- 🤖 **AI-Powered Blog Generation**: Uses Google Gemini to transform research data into engaging blog posts
- 📝 **Narrative Blog Format**: Generates blogs with flowing paragraphs (no bullet points or lists)
- 📊 **Progress Tracking**: Visual progress indicators showing each API processing stage
- 💾 **Dual Storage Format**: 
  - SQLite Database: Stores all generated blogs with full research data
  - JSON Files: Automatically saves gaps and methodology as separate JSON files
- 📥 **Download Blogs**: Export blogs as Markdown files
- 🎨 **Modern UI**: Dark theme with smooth animations and responsive design
- 📱 **Fully Responsive**: Works on desktop, tablet, and mobile devices

## Architecture

1. **Research Gaps API** (Local - Port 8000): Analyzes research landscape and identifies gaps
2. **Questions Generation API** (External): Generates research questions from gaps
3. **Methodology API** (Local - Port 5000): Determines research methodology
4. **Gemini API**: Transforms all data into blog format

## Installation

### Prerequisites

- Python 3.8+
- Node.js (for some dependencies)
- Google Gemini API key

### Setup Steps

1. **Clone/Navigate to the project directory**
```bash
cd "C:\Users\USER\OneDrive\University\3rd year\5th\SPM\spm"
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
# Copy the example env file
copy .env.example .env

# Edit .env and add your Gemini API key
# Get your key from: https://makersuite.google.com/app/apikey
```

4. **Ensure all required APIs are running**
- Research Gaps API: `http://127.0.0.1:8000`
- Methodology API: `http://127.0.0.1:5000`
- Questions API: External (already configured)

## Usage

1. **Start the application**
```bash
python app.py
```

2. **Open your browser**
Navigate to: `http://localhost:3000`

3. **Generate a blog**
- Enter a research topic (e.g., "data engineering in healthcare")
- Click "Generate Blog"
- Watch the progress indicators as each API is called
- View the generated blog (in narrative paragraph format)
- Check the `output/` directory for JSON files:
  - `{topic}_gaps.json` - Research gaps data
  - `{topic}_methodology.json` - Methodology recommendations
- Download as Markdown or view detailed research data

## API Endpoints

### Frontend Routes
- `GET /` - Landing page

### Backend API Routes
- `POST /api/generate-blog` - Generate new blog from topic
- `GET /api/blogs` - Get all saved blogs
- `GET /api/blogs/<id>` - Get specific blog
- `GET /api/blogs/<id>/download` - Download blog as Markdown

## Output Format

### Blog Content
Blogs are generated in **narrative paragraph format**:
- All content flows as cohesive paragraphs
- Research questions are integrated naturally into the text
- No bullet points, numbered lists, or list markers
- Professional and engaging writing style

### JSON Files (Auto-generated)
For each blog, two JSON files are automatically created in the `output/` directory:

**`{topic}_gaps.json`**
```json
{
  "gaps": [
    {
      "statement": "Gap description",
      "reasoning": "Why this gap exists"
    }
  ]
}
```

**`{topic}_methodology.json`**
```json
{
  "data": {
    "methodology": {
      "recommended_methodology": "Mixed-methods approach",
      "justification": "Detailed reasoning...",
      "study_design": "Design details..."
    }
  }
}
```

## Database Schema

**blogs** table:
- `id`: INTEGER PRIMARY KEY
- `topic`: TEXT (research topic)
- `content`: TEXT (generated blog content in narrative format)
- `research_gaps`: TEXT (JSON of gaps data)
- `research_questions`: TEXT (JSON of questions data)
- `methodology`: TEXT (JSON of methodology data)
- `created_at`: TIMESTAMP

## File Structure

```
spm/
├── app.py                          # Flask backend server
├── api.py                          # Original API integration script
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (create from .env.example)
├── .env.example                   # Environment template
├── blogs.db                        # SQLite database (auto-created)
├── output/                         # Auto-created directory for JSON files
│   ├── {topic}_gaps.json          # Research gaps data
│   └── {topic}_methodology.json   # Methodology data
├── templates/
│   └── index.html                 # Main landing page
├── static/
│   ├── style.css                  # Styling and animations
│   └── script.js                  # Frontend logic and API calls
└── BLOG_FORMAT_CHANGES.md         # Documentation of format changes
```

## Technologies Used

### Backend
- **Flask**: Python web framework
- **SQLite**: Lightweight database
- **Google Generative AI**: Gemini API for blog generation
- **Requests**: HTTP library for API calls

### Frontend
- **HTML5**: Structure
- **CSS3**: Modern styling with CSS Grid/Flexbox
- **JavaScript (ES6+)**: Interactive functionality
- **Fetch API**: Async API communication

## Customization

### Modify Blog Structure
Edit the prompt in `app.py` in the `generate_blog_with_gemini()` function:

```python
prompt = f"""
You are an expert technical writer...
# Customize the structure and tone here
# Note: The system generates narrative paragraphs by default
# Avoid bullet points and numbered lists in instructions
"""
```

### Change Output Directory
By default, JSON files are saved to `output/`. To change this:

```python
# In app.py, line ~265
output_dir = 'output'  # Change to your preferred directory
```

### Change UI Theme
Edit CSS variables in `static/style.css`:

```css
:root {
    --primary-color: #6366f1;
    --bg-color: #0f172a;
    /* Customize colors */
}
```

### Add More APIs
Add new API functions in `app.py` following the pattern:

```python
def call_new_api(data):
    url = "http://your-api-url"
    response = requests.post(url, json=data)
    return response.json()
```

## Troubleshooting

### APIs Not Responding
- Ensure all required APIs are running on their respective ports
- Check firewall settings
- Verify API URLs in `app.py`

### Gemini API Errors
- Check your API key in `.env`
- Verify API quota/limits
- Check internet connection

### Database Issues
- Delete `blogs.db` to reset database
- Check file permissions

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, port=3001)  # Use different port
```

## Recent Updates

### v2.0 - Blog Format Enhancement
- ✅ Narrative paragraph format for all blog content
- ✅ Automatic JSON file generation for gaps and methodology
- ✅ Improved readability with flowing prose
- ✅ Dual storage: Database + JSON files
- ✅ Enhanced Gemini AI prompts for better content

For detailed information, see `BLOG_FORMAT_CHANGES.md`

## Future Enhancements

- [ ] Real-time WebSocket progress updates
- [ ] User authentication and blog ownership
- [ ] Blog editing capabilities
- [ ] Export to PDF with embedded JSON data
- [ ] Sharing functionality
- [ ] Search and filter saved blogs
- [ ] API key management UI
- [ ] Multiple blog templates
- [ ] Batch blog generation from multiple topics
- [ ] Custom JSON export formats

## License

MIT License - Feel free to use and modify

## Support

For issues or questions, please check the API documentation or contact the development team.
