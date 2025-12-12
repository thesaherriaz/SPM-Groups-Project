# Blog Format Changes

## Overview
Updated the blog generation system to produce:
1. **Gaps & Methodology**: Saved as separate JSON files
2. **Questions & Main Blog**: Generated in narrative paragraph format (no bullet points)

## Changes Made

### 1. Enhanced Gemini Prompt
- Added explicit instructions to format content as flowing paragraphs
- Instructed to avoid bullet points, numbered lists, and list markers
- Emphasized narrative integration of research questions

### 2. Updated Fallback Blog Generator
The `generate_basic_blog()` function now creates narrative paragraphs:

#### Research Gaps Section
- Converts individual gaps into flowing sentences
- Links gaps together with transitional phrases
- Example: "The current research landscape in {topic} reveals several critical gaps..."

#### Research Questions Section
- Integrates main question and sub-questions into narrative text
- Uses natural language connectors: "Specifically, we seek to understand..."
- Weaves questions smoothly: "question 1, question 2, and question 3"

#### Methodology Section
- Extracts methodology details from JSON
- Presents them as cohesive paragraphs
- Includes justification and study design in narrative form

### 3. JSON File Output
Added automatic file generation after blog creation:

**Location**: `output/` directory (auto-created)

**Files Generated**:
- `{topic}_gaps.json` - Contains all research gaps data
- `{topic}_methodology.json` - Contains methodology recommendations

**Filename Format**:
- Sanitized topic name (alphanumeric, spaces replaced with underscores)
- UTF-8 encoding with pretty printing (indent=2)

## Example Output Structure

### Blog Content (Narrative Format)
```markdown
# Research Blog: Data Engineering in Healthcare

## Introduction
This blog explores the current state of research in data engineering in healthcare...

## Research Questions
To address these research gaps, our investigation centers on the following inquiry: 
How can data engineering improve healthcare outcomes? This overarching question 
encompasses several important dimensions. Specifically, we seek to understand 
what data integration challenges exist, how real-time processing impacts patient care, 
and what security measures are most effective...
```

### JSON Files

**data_engineering_in_healthcare_gaps.json**
```json
{
  "gaps": [
    {
      "statement": "Limited research on real-time data processing",
      "reasoning": "Most studies focus on batch processing"
    }
  ]
}
```

**data_engineering_in_healthcare_methodology.json**
```json
{
  "data": {
    "methodology": {
      "recommended_methodology": "Mixed-methods approach",
      "justification": "Combines quantitative and qualitative data...",
      "study_design": "Sequential explanatory design..."
    }
  }
}
```

## Usage

1. **Run the Flask app**: `python app.py`
2. **Generate a blog**: POST to `/api/generate-blog` with topic
3. **Output**:
   - Blog content returned in API response (narrative paragraphs)
   - JSON files saved in `output/` directory
   - All data also stored in SQLite database

## Benefits

✅ **Better Readability**: Narrative format is more engaging and professional
✅ **Structured Data**: JSON files enable easy programmatic access to gaps/methodology
✅ **Dual Format**: Maintains both human-readable blog and machine-readable JSON
✅ **No Bullet Points**: Clean, flowing prose throughout the blog
✅ **Database Backup**: All data still saved to SQLite for retrieval

## Files Modified
- `app.py` (lines 106-212, 207-280)
