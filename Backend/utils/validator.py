"""
Input validation utilities
"""

from typing import Optional, Dict, Any


class Validator:
    """Class for validating API inputs"""
    
    @staticmethod
    def validate_methodology_input(data: Dict[str, Any]) -> Optional[str]:
        """
        Validate input for methodology endpoint
        
        Args:
            data: Input data dictionary
        
        Returns:
            Error message if validation fails, None otherwise
        """
        if not isinstance(data, dict):
            return "Input must be a JSON object"
        
        # Check required fields
        if 'research_gap' not in data:
            return "Missing required field: research_gap"
        
        if 'research_questions' not in data:
            return "Missing required field: research_questions"
        
        # Validate research_gap
        research_gap = data.get('research_gap')
        if not isinstance(research_gap, str):
            return "research_gap must be a string"
        
        if not research_gap.strip():
            return "research_gap cannot be empty"
        
        # Validate research_questions
        research_questions = data.get('research_questions')
        if not isinstance(research_questions, list):
            return "research_questions must be an array"
        
        if len(research_questions) == 0:
            return "research_questions cannot be empty"
        
        # Validate each question is a string
        for i, question in enumerate(research_questions):
            if not isinstance(question, str):
                return f"research_questions[{i}] must be a string"
            if not question.strip():
                return f"research_questions[{i}] cannot be empty"
        
        return None
    
    @staticmethod
    def validate_compliance_input(data: Dict[str, Any]) -> Optional[str]:
        """
        Validate input for compliance endpoint
        
        Args:
            data: Input data dictionary
        
        Returns:
            Error message if validation fails, None otherwise
        """
        if not isinstance(data, dict):
            return "Input must be a JSON object"
        
        # Check required fields
        required_fields = ['project_title', 'data_sources', 'methods']
        for field in required_fields:
            if field not in data:
                return f"Missing required field: {field}"
        
        # Validate each field is a string
        for field in required_fields:
            value = data.get(field)
            if not isinstance(value, str):
                return f"{field} must be a string"
            if not value.strip():
                return f"{field} cannot be empty"
        
        return None
    
    @staticmethod
    def validate_ask_input(data: Dict[str, Any]) -> Optional[str]:
        """
        Validate input for ask endpoint
        
        Args:
            data: Input data dictionary
        
        Returns:
            Error message if validation fails, None otherwise
        """
        if not isinstance(data, dict):
            return "Input must be a JSON object"
        
        # Check required field
        if 'question' not in data:
            return "Missing required field: question"
        
        # Validate question
        question = data.get('question')
        if not isinstance(question, str):
            return "question must be a string"
        
        if not question.strip():
            return "question cannot be empty"
        
        # Check minimum length
        if len(question.strip()) < 3:
            return "question must be at least 3 characters long"
        
        return None


    @staticmethod
    def validate_questions_input(data: Dict[str, Any]) -> Optional[str]:
        """
        Validate input for questions-based methodology endpoint
        
        Args:
            data: Input data dictionary
        
        Returns:
            Error message if validation fails, None otherwise
        """
        if not isinstance(data, dict):
            return "Input must be a JSON object"
        
        # Check required fields
        if 'main_question' not in data:
            return "Missing required field: main_question"
        
        if 'sub_questions' not in data:
            return "Missing required field: sub_questions"
        
        # Validate main_question
        main_question = data.get('main_question')
        if not isinstance(main_question, str):
            return "main_question must be a string"
        
        if not main_question.strip():
            return "main_question cannot be empty"
        
        # Validate sub_questions
        sub_questions = data.get('sub_questions')
        if not isinstance(sub_questions, list):
            return "sub_questions must be an array"
        
        if len(sub_questions) == 0:
            return "sub_questions cannot be empty"
        
        # Validate each sub-question is a string
        for i, question in enumerate(sub_questions):
            if not isinstance(question, str):
                return f"sub_questions[{i}] must be a string"
            if not question.strip():
                return f"sub_questions[{i}] cannot be empty"
        
        return None
