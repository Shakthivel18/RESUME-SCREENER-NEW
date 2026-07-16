"""
AI Interview System - Reliable Implementation
Generates personalized interview questions with robust fallback mechanisms
"""

import google.generativeai as genai
import os
import json
import time
from datetime import datetime
import traceback
from typing import Any, Dict, List, Optional, Union

# Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyBb4pn90oA-YfwG_vpr_kMVH22ulqhgMMg')
# List of models to try in order of preference
MODELS_TO_TRY = ['gemini-flash-latest', 'gemini-1.5-flash', 'gemini-pro']

MAX_RETRIES = 2
RETRY_DELAY = 1  # seconds

def get_model() -> Optional[bool]:
    """Attempt to configure and return a working Gemini model"""
    if not GEMINI_API_KEY:
        print("WARNING: AI Interviewer - No API Key found.")
        return None

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # We don't instantiate the model here anymore, we'll do it per request 
        # to allow falling back to different model names if one is 404/overloaded
        return True 
    except Exception as e:
        print(f"ERROR: AI Interviewer - Configuration failed: {e}")
        return None

def generate_with_retry(prompt: str, model_name: str = 'gemini-flash-latest') -> str:
    """Generate content with retry logic and model fallback"""
    
    # Try the requested model first, then others
    attempt_models = [model_name] + [m for m in MODELS_TO_TRY if m != model_name]
    
    for model_id in attempt_models:
        try:
            model = genai.GenerativeModel(model_id)
            print(f"INFO: AI Interviewer - Attempting generation with {model_id}")
            
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"WARNING: AI Interviewer - Model {model_id} failed: {str(e)}")
            continue
            
    raise Exception("All AI models failed")

def validate_json_structure(data: Any, default_structure: Any) -> Any:
    """
    Recursively ensure data matches default_structure keys/types.
    """
    if isinstance(default_structure, dict):
        if not isinstance(data, dict):
            return default_structure
        
        cleaned = {}
        for key, default_val in default_structure.items():
            if key in data:
                cleaned[key] = validate_json_structure(data[key], default_val)
            else:
                cleaned[key] = default_val
        return cleaned
    
    elif isinstance(default_structure, list):
        if not isinstance(data, list):
            return default_structure
        # For lists, we assume it's a list of items resembling the first item of default list
        # or just pass through if default list is empty
        if not default_structure:
            return data
            
        template = default_structure[0]
        cleaned_list = []
        for item in data:
            cleaned_list.append(validate_json_structure(item, template))
        return cleaned_list
        
    return data

def generate_interview_questions(resume_text, job_description, domain, num_questions=10):
    """
    Generate personalized interview questions with strict JSON validation and fallback
    """
    # 1. Prepare Prompt
    prompt = f"""You are an expert technical interviewer hiring for the '{domain}' domain. 
    Task: Generate {num_questions} completely unique, dynamic interview questions that heavily focus on the specifics of the '{domain}' domain, the candidate's experiences, and the job requirements.
    
    Job Description:
    {job_description[:2000]}
    
    Candidate Resume Summary:
    {resume_text[:2000]}
    
    Requirements:
    - VERY IMPORTANT: Questions MUST be highly tailored to the '{domain}' domain. Do not ask generic software engineering questions if the domain is Data Science, for example.
    - Ask a mix of highly specific Technical, scenario-based Behavioral, and Architecture/Problem-Solving questions.
    - Tailored to gaps, unique projects, or specific tools in the resume. Avoid standard boilerplate questions.
    
    OUTPUT FORMAT: Return ONLY a raw JSON array. Do not use markdown blocks.
    [
        {{
            "question": "Question text here",
            "category": "Technical",
            "difficulty": "Medium",
            "focus_area": "React Hooks"
        }}
    ]
    """

    # 2. Try AI Generation
    try:
        if get_model():
            json_str = generate_with_retry(prompt)
            
            # Clean response (remove markdown if present)
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0]
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0]
                
            questions = json.loads(json_str.strip())
            
            # Validation
            if isinstance(questions, list) and len(questions) > 0:
                # Validate structure of each question
                default_q = {
                    "question": "Default question",
                    "category": "General",
                    "difficulty": "Medium",
                    "focus_area": "General"
                }
                validated_questions = [validate_json_structure(q, default_q) for q in questions]
                
                print(f"INFO: AI Interviewer - Successfully generated {len(validated_questions)} dynamic {domain} questions.")
                return validated_questions[:num_questions]
                
    except Exception as e:
        print(f"ERROR: AI Interviewer - Generation failed. Using fallback. Error: {e}")
        with open('error_log.txt', 'a') as f:
            f.write(f"\\n{datetime.now()} - Gen Error: {e}\\n")

    # 3. Fallback Mechanism (Guaranteed Return)
    print("INFO: AI Interviewer - Returning fallback questions.")
    return get_fallback_questions(domain, num_questions)


def evaluate_answer(question, answer, resume_text):
    """
    Evaluate answer with AI, returning default score on failure
    """
    prompt = f"""You are a supportive, pragmatic Technical Hiring Manager. 
    Your Goal: Evaluate this candidate's answer for practical logical correctness, effort, and general understanding.
    
    CONTEXT:
    Question: {question}
    Candidate Answer: {answer}
    Candidate Resume Snippet: {resume_text[:800]}
    
    INSTRUCTIONS:
    1. BE LENIENT AND PRAGMATIC: Reward candidates for understanding the core concept, even if they miss small details.
    2. Partial credit is highly encouraged. If they are logically on the right track or mention practical real-world usage, score them well (7-9 range).
    3. Do NOT grade based on "Top 1%" perfection. A perfectly acceptable, average, working answer should get a solid score.
    4. Only give very low scores (<4) if the answer is completely blank, hallucinates wildly, or shows zero understanding.
    
    OUTPUT FORMAT (Return ONLY raw JSON):
    {{
        "metrics": {{
            "technical_accuracy": <number 1-10>,
            "communication_clarity": <number 1-10>,
            "problem_solving": <number 1-10>,
            "cultural_fit": <number 1-10>
        }},
        "score": <calculated average of metrics (1 decimal)>,
        "feedback": "Start with a strength. Then provide 1-2 sharp, actionable improvements. End with a quick encouraging remark.",
        "key_observations": ["specific technical terminology used/missed", "structured vs unstructured thinking"],
        "strengths": ["Strong point 1", "Strong point 2"],
        "improvements": ["Critical area to fix 1", "Critical area to fix 2"],
        "red_flags": ["Any major warning signs or 'None'"]
    }}
    """
    
    default_response = {
        "metrics": {"technical_accuracy": 0, "communication_clarity": 0, "problem_solving": 0, "cultural_fit": 0},
        "score": 0,
        "feedback": "Evaluation unavailable. Answer recorded for manual review.",
        "key_observations": [],
        "strengths": ["Response recorded"],
        "improvements": [],
        "red_flags": []
    }

    try:
        if get_model():
            json_str = generate_with_retry(prompt)
            
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0]
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0]
                
            data = json.loads(json_str.strip())
            
            # Validate structure
            validated_data = validate_json_structure(data, default_response)
            return validated_data
            
    except Exception as e:
        print(f"ERROR: AI Interviewer - Evaluation failed: {e}")
        
    # Fallback: Smart NLP Scoring (Semantic)
    try:
        import utils
        similarity = utils.calculate_answer_similarity(question, answer)
        
        # Scale 0.0-1.0 to 1-10
        # If similarity is > 0.7, it's very relevant (8-10)
        # If similarity is < 0.3, it's barely relevant (1-4)
        
        relevance_score = similarity * 10
        
        # Length Penalty (for very short answers that accidentally match keywords)
        words = len(answer.split())
        length_factor = min(1.0, words / 30) # 30 words required for full potential score
        
        final_score = relevance_score * length_factor
        final_score = max(1, min(10, final_score)) # Clamp 1-10
        
        # Boost a bit as strict keyword matching is harsh
        if final_score < 5 and words > 20: 
            final_score += 2
        
        final_score = round(final_score, 1)

        # Generate intelligent fallback feedback
        if final_score >= 8:
            heuristic_feedback = "Strong answer with high relevance to the question."
        elif final_score >= 5:
            heuristic_feedback = "Relevant answer, though could be more specific."
        else:
            heuristic_feedback = "Answer seems brief or off-topic based on key terms."

        default_response["score"] = final_score
        default_response["feedback"] = heuristic_feedback + " (Semantic Analysis)"
        
        default_response["metrics"] = {
            "technical_accuracy": min(10, final_score + 1), 
            "communication_clarity": min(10, final_score), 
            "problem_solving": min(10, final_score - 1 if final_score > 5 else final_score), 
            "cultural_fit": 5
        }
    except Exception as e:
        print(f"Fallback scoring error: {e}")
        # Absolute fallback
        default_response["score"] = 3
        default_response["feedback"] = "Answer recorded. Pending manual review."


    return default_response

def get_fallback_questions(domain, num_questions=10):
    """Reliable static questions for when AI fails"""
    # ... (Keep existing fallback questions logic or simplify)
    defaults = [
        {"question": "Tell me about a challenging project you worked on.", "category": "Behavioral", "difficulty": "Easy", "focus_area": "Experience"},
        {"question": "What are your strongest technical skills?", "category": "Technical", "difficulty": "Easy", "focus_area": "Self-Assessment"},
        {"question": "How do you handle tight deadlines?", "category": "Behavioral", "difficulty": "Medium", "focus_area": "Management"},
        {"question": "Describe a time you had to learn a new technology quickly.", "category": "Behavioral", "difficulty": "Medium", "focus_area": "Adaptability"},
        {"question": "How do you ensure code quality?", "category": "Technical", "difficulty": "Medium", "focus_area": "Best Practices"}
    ]
    
    # Simple mapping for key domains
    domain_questions = {
        "SOFTWARE_ENGINEERING": [
            {"question": "Explain the difference between a process and a thread.", "category": "Technical", "difficulty": "Medium", "focus_area": "OS Concepts"},
            {"question": "What is the CAP theorem?", "category": "Technical", "difficulty": "Hard", "focus_area": "System Design"},
        ],
        "DATA_SCIENCE": [
            {"question": "What is overfitting and how do you prevent it?", "category": "Technical", "difficulty": "Medium", "focus_area": "ML Theory"},
            {"question": "Explain the difference between L1 and L2 regularization.", "category": "Technical", "difficulty": "Hard", "focus_area": "Math"},
        ]
    }
    
    # Combine tailored + default to ensure we have enough
    selected = domain_questions.get(domain, []) + defaults
    
    # Ensure we fill up to num_questions
    while len(selected) < num_questions:
        selected.append(defaults[len(selected) % len(defaults)])
        
    return selected[:num_questions]

def save_interview_session(candidate_id, interview_data):
    """Robust save with error handling"""
    try:
        os.makedirs('interviews', exist_ok=True)
        filename = f"interviews/{candidate_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(interview_data, f, indent=2)
        return filename
    except Exception as e:
        print(f"ERROR: Failed to save interview: {e}")
        return None

def load_interview_session(candidate_id):
    """Robust load"""
    try:
        import glob
        pattern = f"interviews/{candidate_id}_*.json"
        files = glob.glob(pattern)
        if not files: return None
        latest_file = max(files, key=os.path.getctime)
        with open(latest_file, 'r') as f:
            return json.load(f)
    except Exception:
        return None
