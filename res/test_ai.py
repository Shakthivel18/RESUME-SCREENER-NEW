
import ai_interviewer
import os

print("Testing AI Interviewer...")

# Mock data
resume_text = """
Experienced Python Developer with 5 years of experience.
Skills: Python, Django, Flask, AWS, Docker, Kubernetes.
Experience:
- Senior Developer at Tech Co: Built microservices using FastAPI.
- Developer at Startup Inc: Developed REST APIs using Flask.
"""

job_description = """
We are looking for a Senior Python Developer with experience in AWS and Microservices.
Key skills: Python, AWS, Docker, FastAPI.
"""

domain = "SOFTWARE_ENGINEERING"

print("\n--- Testing Question Generation ---")
try:
    questions = ai_interviewer.generate_interview_questions(resume_text, job_description, domain)
    print(f"Generated {len(questions)} questions.")
    if len(questions) > 0:
        print("First question:", questions[0]['question'])
        print("Category:", questions[0]['category'])
    else:
        print("No questions generated.")
except Exception as e:
    print(f"Test failed: {e}")

print("\n--- Testing Answer Evaluation ---")
try:
    question = "Explain your experience with Microservices."
    answer = "I built several microservices at Tech Co using FastAPI. We used Docker for containerization and deployed on AWS ECS."
    
    evaluation = ai_interviewer.evaluate_answer(question, answer, resume_text)
    print("Score:", evaluation.get('score'))
    print("Feedback:", evaluation.get('feedback'))
except Exception as e:
    print(f"Test failed: {e}")
