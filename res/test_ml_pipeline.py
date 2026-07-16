import os
import shutil
import gzip
import json
import numpy as np
import utils
from advanced_scorer import AdvancedResumeScorer

def test_pipeline():
    print("==================================================")
    print("RUNNING AUTOMATED ML PIPELINE TESTS")
    print("==================================================")
    
    # 1. Verify Model Files Exist
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    classifier_path = os.path.join(_script_dir, "models", "domain_classifier_pipeline.joblib")
    w2v_path = os.path.join(_script_dir, "models", "resume_word2vec.model")
    
    print(f"Checking Classifier Model path: {classifier_path} ... ", end="")
    assert os.path.exists(classifier_path), "Classifier model not found!"
    print("EXISTS")
    
    print(f"Checking Word2Vec Model path: {w2v_path} ... ", end="")
    assert os.path.exists(w2v_path), "Word2Vec model not found!"
    print("EXISTS")
    
    # Initialize Scorer
    print("Initializing AdvancedResumeScorer with ML models... ", end="")
    scorer = AdvancedResumeScorer()
    assert scorer.classifier is not None, "Classifier failed to load!"
    assert scorer.w2v_model is not None, "Word2Vec failed to load!"
    print("LOADED SUCCESSFULLY")
    
    # 2. Test NLP Segmentation
    print("Testing NLP Resume Segmentation... ", end="")
    test_resume_text = """
John Doe
Software Engineer

TECHNICAL SKILLS:
Python, Django, Flask, Java, SQL

WORK EXPERIENCE:
Senior Software Developer at TechCorp (2020-Present)
- Developed REST APIs in Python and backend services using Flask.

EDUCATION:
Bachelor of Science in Computer Science, University of California (2016-2020)

CERTIFICATIONS:
AWS Certified Solutions Architect
"""
    sections = utils.segment_resume_sections(test_resume_text)
    
    assert "skills" in sections
    assert "experience" in sections
    assert "education" in sections
    assert "certifications" in sections
    assert "python" in sections["skills"].lower()
    assert "techcorp" in sections["experience"].lower()
    assert "bachelor" in sections["education"].lower()
    print("PASSED")
    
    # 3. Test Data Compression & Storage
    print("Testing JSON Gzip Compression & Storage... ", end="")
    test_candidate_id = "test_candidate_compress_123"
    test_data = {
        "raw_text": test_resume_text,
        "sections": sections,
        "keywords": ["python", "django", "flask", "java", "sql", "aws"],
        "highlights": ["python", "django", "flask"]
    }
    
    # Save compressed
    save_success = utils.save_compressed_candidate_data(test_candidate_id, test_data)
    assert save_success, "Failed to save compressed candidate data"
    
    # Check file exists and has .json.gz extension
    expected_file = os.path.join("uploads/processed_text", f"{test_candidate_id}.json.gz")
    assert os.path.exists(expected_file), f"Compressed file not found at {expected_file}"
    
    # Read back and compare
    read_data = utils.load_compressed_candidate_data(test_candidate_id)
    assert read_data is not None, "Decompress loader returned None"
    assert read_data["raw_text"] == test_resume_text, "Raw text mismatch after decompression"
    assert read_data["sections"]["skills"] == sections["skills"], "Sections mismatch after decompression"
    assert read_data["keywords"] == test_data["keywords"], "Keywords mismatch after decompression"
    
    # Clean up test file
    if os.path.exists(expected_file):
        os.remove(expected_file)
        
    print("PASSED")
    
    # 4. Test ML Domain Detection
    print("Testing ML Domain Classification... ")
    jd_tech = "We are looking for a Senior Software Engineer with python, react, and aws experience."
    jd_hr = "Looking for a Human Resources Specialist to handle recruitment, onboarding, and payroll benefits."
    
    domain_tech = scorer.detect_domain(jd_tech)
    domain_hr = scorer.detect_domain(jd_hr)
    
    print(f"  - Tech JD top prediction: {domain_tech[0][0]} (score: {domain_tech[0][1]:.4f})")
    print(f"  - HR JD top prediction: {domain_hr[0][0]} (score: {domain_hr[0][1]:.4f})")
    
    assert domain_tech[0][0] == "SOFTWARE_ENGINEERING" or "ENGINEERING" in domain_tech[0][0], "Tech JD classification mismatch"
    assert domain_hr[0][0] == "GENERAL_IT" or "HR" in domain_hr[0][0], "HR JD classification mismatch"
    print("  - Domain Detection: PASSED")
    
    # 5. Test ML Domain Similarity Score
    print("Testing ML Domain Cosine Score... ", end="")
    score_same = scorer.calculate_domain_score(jd_tech, test_resume_text, "SOFTWARE_ENGINEERING")
    score_diff = scorer.calculate_domain_score(jd_hr, test_resume_text, "SOFTWARE_ENGINEERING")
    
    print(f"(Same: {score_same:.4f}, Different: {score_diff:.4f}) ... ", end="")
    assert score_same > score_diff, "Domain similarity scoring logic error"
    print("PASSED")
    
    # 6. Test Word2Vec Synonym-Aware Matching
    print("Testing Word2Vec Synonym Matching... ", end="")
    
    # 'scripting' is unmatched in exact matching since the resume lists 'python' and 'django'
    # But from Word2Vec training, 'scripting' and 'python' are highly related.
    # Let's test matching JD keyword "scripting" against resume keywords that only contain "python"
    jd_keywords = ["scripting"]
    resume_keywords_no_scripting = ["python"]
    
    # Test scorer keyword matching with synonym resolver
    score_exact_mismatch_synonym_match = scorer.calculate_keyword_score(
        jd_keywords=jd_keywords,
        resume_keywords=resume_keywords_no_scripting,
        resume_text="we use python and django for backend services"
    )
    
    print(f"(Synonym Score: {score_exact_mismatch_synonym_match:.4f}) ... ", end="")
    assert score_exact_mismatch_synonym_match > 0.0, "Synonym matching failed to credit matching Word2Vec concepts"
    print("PASSED")
    
    print("\n==================================================")
    print("ALL AUTOMATED TESTS PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    test_pipeline()
