"""
Flask Backend for AI-powered Research Methodology & IP Compliance Assistant
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging

from services.gemini_service import GeminiService
from services.prompt_templates import PromptTemplates
from utils.validator import Validator

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend requests
CORS(app, origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
gemini_service = GeminiService()
prompt_templates = PromptTemplates()
validator = Validator()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Backend is running"
    }), 200


@app.route('/api/routes', methods=['GET'])
def list_routes():
    """List all available API routes for debugging"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "endpoint": rule.endpoint,
            "path": str(rule),
            "methods": list(rule.methods)
        })
    return jsonify({
        "available_routes": routes
    }), 200


@app.route('/api/get-methodology', methods=['POST'])
def get_methodology():
    """
    Endpoint to get recommended research methodology
    
    Expected input:
    {
        "research_gap": "text",
        "research_questions": ["q1", "q2"]
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No JSON data provided"
            }), 400
        
        # Validate input
        validation_error = validator.validate_methodology_input(data)
        if validation_error:
            return jsonify({
                "error": validation_error
            }), 400
        
        # Extract data
        research_gap = data.get('research_gap', '')
        research_questions = data.get('research_questions', [])
        
        # Build prompt
        prompt = prompt_templates.get_methodology_prompt(
            research_gap=research_gap,
            research_questions=research_questions
        )
        
        # Call Gemini API
        logger.info("Calling Gemini API for methodology recommendation")
        response = gemini_service.call_gemini(prompt)
        
        if not response:
            return jsonify({
                "error": "Failed to get response from AI service"
            }), 500
        
        # Parse and return response
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in get_methodology: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


@app.route('/api/get-compliance', methods=['POST'])
def get_compliance():
    """
    Endpoint to get legal, IP, and compliance guidance
    
    Expected input:
    {
        "project_title": "string",
        "data_sources": "string",
        "methods": "string"
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No JSON data provided"
            }), 400
        
        # Validate input
        validation_error = validator.validate_compliance_input(data)
        if validation_error:
            return jsonify({
                "error": validation_error
            }), 400
        
        # Extract data
        project_title = data.get('project_title', '')
        data_sources = data.get('data_sources', '')
        methods = data.get('methods', '')
        
        # Build prompt
        prompt = prompt_templates.get_compliance_prompt(
            project_title=project_title,
            data_sources=data_sources,
            methods=methods
        )
        
        # Call Gemini API
        logger.info("Calling Gemini API for compliance analysis")
        response = gemini_service.call_gemini(prompt)
        
        if not response:
            return jsonify({
                "error": "Failed to get response from AI service"
            }), 500
        
        # Parse and return response
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in get_compliance: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


@app.route('/api/ask', methods=['POST'])
def ask_question():
    """
    Endpoint for general research questions
    
    Expected input:
    {
        "question": "string"
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        # print(data)
        
        if not data:
            return jsonify({
                "error": "No JSON data provided"
            }), 400
        
        # Validate input
        validation_error = validator.validate_ask_input(data)
        if validation_error:
            return jsonify({
                "error": validation_error
            }), 400
        
        # Extract question
        question = data.get('question', '')
        
        # Build prompt
        prompt = prompt_templates.get_ask_prompt(user_question=question)
        
        # Call Gemini API
        logger.info("Calling Gemini API for general question")
        response = gemini_service.call_gemini(prompt, is_json=False)
        
        if not response:
            return jsonify({
                "error": "Failed to get response from AI service"
            }), 500
        
        # Return response
        return jsonify({
            "answer": response
        }), 200
        
    except Exception as e:
        logger.error(f"Error in ask_question: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


@app.route('/api/analyze-questions', methods=['POST'])
def analyze_questions():
    """
    Endpoint to analyze research questions and recommend methodology
    
    Expected input:
    {
        "main_question": "string",
        "sub_questions": ["q1", "q2", "q3"]
    }
    
    Response format:
    {
        "success": true,
        "message": "Methodology analysis completed",
        "data": {
            "questions": {
                "main_question": "string",
                "sub_questions": ["q1", "q2"],
                "rationale": "optional explanation"
            },
            "methodology": {
                "recommended_methodology": "string",
                "justification": "string",
                "study_design": "string",
                "data_collection_tools": "string"
            }
        }
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "No JSON data provided",
                "data": None
            }), 400
        
        # Validate input
        validation_error = validator.validate_questions_input(data)
        if validation_error:
            return jsonify({
                "success": False,
                "message": validation_error,
                "data": None
            }), 400
        
        # Extract data
        main_question = data.get('main_question', '')
        sub_questions = data.get('sub_questions', [])
        
        # Build prompt
        prompt = prompt_templates.get_questions_methodology_prompt(
            main_question=main_question,
            sub_questions=sub_questions
        )
        
        # Call Gemini API
        logger.info("Calling Gemini API for questions-based methodology analysis")
        methodology_response = gemini_service.call_gemini(prompt, is_json=True)
        
        if not methodology_response:
            return jsonify({
                "success": False,
                "message": "Failed to get response from AI service",
                "data": None
            }), 500
        
        # Build response in the specified format
        response_data = {
            "questions": {
                "main_question": main_question,
                "sub_questions": sub_questions
            },
            "methodology": methodology_response
        }
        
        return jsonify({
            "success": True,
            "message": "Methodology analysis completed successfully",
            "data": response_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error in analyze_questions: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Internal server error: {str(e)}",
            "data": None
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    # Check if API key is set
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        logger.warning("GEMINI_API_KEY not found in environment variables")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)

