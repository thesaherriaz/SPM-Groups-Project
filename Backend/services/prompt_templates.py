"""
Prompt templates for different AI interactions
"""


class PromptTemplates:
    """Class containing prompt templates for Gemini API"""
    
    @staticmethod
    def get_methodology_prompt(research_gap: str, research_questions: list) -> str:
        """
        Generate prompt for methodology recommendation
        
        Args:
            research_gap: Description of the research gap
            research_questions: List of research questions
        
        Returns:
            Formatted prompt string
        """
        questions_text = "\n".join([f"- {q}" for q in research_questions])
        
        prompt = f"""You are an expert academic research supervisor. 

Based on the research gap and research questions provided, recommend the most suitable research methodology.

Return the answer strictly in JSON with the keys:
- recommended_methodology
- justification
- study_design
- data_collection_tools

GAP: {research_gap}

QUESTIONS:
{questions_text}

Provide a comprehensive recommendation that considers:
- Whether quantitative, qualitative, or mixed-methods is most appropriate
- Specific study design (survey, experiment, case study, simulation, etc.)
- Justification for your selection
- Recommended data collection tools and methods"""
        
        return prompt
    
    @staticmethod
    def get_questions_methodology_prompt(main_question: str, sub_questions: list) -> str:
        """
        Generate prompt for methodology recommendation based on research questions only
        
        Args:
            main_question: The main research question
            sub_questions: List of sub-questions
        
        Returns:
            Formatted prompt string
        """
        sub_questions_text = "\n".join([f"  - {q}" for q in sub_questions])
        
        prompt = f"""You are an expert academic research supervisor specializing in research methodology.

Based on the research questions provided, recommend the most suitable research methodology.

Return the answer strictly in JSON with this EXACT structure:
{{
  "recommended_methodology": "string",
  "justification": "string",
  "study_design": "string",
  "data_collection_tools": {{
    "qualitative_tools": ["tool1 with description", "tool2 with description"],
    "quantitative_tools": ["tool1 with description", "tool2 with description"]
  }}
}}

MAIN RESEARCH QUESTION:
{main_question}

SUB-QUESTIONS:
{sub_questions_text}

Analyze the questions and provide a comprehensive methodology recommendation:
- recommended_methodology: Type of methodology (e.g., "Mixed-Methods Approach", "Qualitative", "Quantitative")
- justification: Detailed explanation of why this methodology is appropriate for these questions
- study_design: Specific design approach (e.g., "Convergent Parallel Mixed Methods Design", "Sequential Explanatory Design")
- data_collection_tools: Object with two arrays:
  - qualitative_tools: Array of qualitative tools with detailed descriptions
  - quantitative_tools: Array of quantitative tools with detailed descriptions

Each tool should include the tool name followed by a colon and detailed description of how it will be used."""
        
        return prompt
    
    @staticmethod
    def get_compliance_prompt(project_title: str, data_sources: str, methods: str) -> str:
        """
        Generate prompt for legal/IP/compliance analysis
        
        Args:
            project_title: Title of the research project
            data_sources: Description of data sources
            methods: Description of research methods
        
        Returns:
            Formatted prompt string
        """
        input_json = f"""
Project Title: {project_title}
Data Sources: {data_sources}
Research Methods: {methods}
"""
        
        prompt = f"""You are an expert in research ethics, Pakistani HEC guidelines, copyright laws, and patent regulations.

Analyze the research details and provide compliance and legal/IP guidance.

Return strictly in JSON with:
- ip_risks
- copyright_concerns
- patentability
- ethical_considerations
- data_privacy_requirements
- compliance_recommendations

RESEARCH DETAILS:
{input_json}

Provide comprehensive analysis covering:
- Intellectual property risks and concerns
- Copyright issues and protections needed
- Patentability assessment
- Ethical considerations and risks
- HEC ethics compliance requirements
- Local and international research standards
- Data privacy requirements (GDPR, local laws)
- Specific compliance recommendations"""
        
        return prompt
    
    @staticmethod
    def get_ask_prompt(user_question: str) -> str:
        """
        Generate prompt for general research questions
        
        Args:
            user_question: The user's question
        
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are a helpful AI research assistant specializing in research methodology, IP law, and compliance.

Provide a CONCISE, clear answer to the following question. Keep your response brief and to the point (2-4 paragraphs maximum).

QUESTION: {user_question}

Your answer should be:
- Brief and concise (2-4 paragraphs max)
- Clear and well-structured
- Based on academic best practices
- Relevant to research methodology, IP law, or compliance
- Helpful and actionable
- Avoid lengthy explanations or excessive detail
- Use simple language, not overly academic"""
        
        return prompt

