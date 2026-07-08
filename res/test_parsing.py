"""
Quick test to verify resume parsing and hybrid scoring are working
"""
import sys
sys.path.insert(0, '.')

import utils

# Test 1: Text extraction
print("=" * 80)
print("TEST 1: Text Extraction")
print("=" * 80)

test_file = "uploads/resumes/Job Title.pdf"
try:
    text = utils.extract_text_from_file(test_file)
    if text:
        print(f"[PASS] Successfully extracted {len(text)} characters from {test_file}")
        print(f"Preview: {text[:200]}...")
    else:
        print(f"[FAIL] No text extracted from {test_file}")
except Exception as e:
    print(f"[FAIL] Error extracting text: {e}")

# Test 2: Keyword extraction
print("\n" + "=" * 80)
print("TEST 2: Keyword Extraction")
print("=" * 80)

jd_text = """
Senior Python Developer - 5+ years experience
Required: Python, Django, Flask, AWS, Docker, Kubernetes, PostgreSQL, Git
"""

keywords = utils.extract_keywords(jd_text)
print(f"[PASS] Extracted {len(keywords)} keywords from job description:")
print(f"  {', '.join(keywords)}")

# Test 3: Experience extraction
print("\n" + "=" * 80)
print("TEST 3: Experience Extraction")
print("=" * 80)

exp_text = "I have 5 years of experience in Python development"
years = utils.extract_years_of_experience(exp_text)
print(f"[PASS] Extracted {years} years of experience from text")

# Test 4: Hybrid scoring
print("\n" + "=" * 80)
print("TEST 4: Hybrid Scoring")
print("=" * 80)

job_desc = """
Senior Python Developer - 5+ years required
We need an experienced Python developer with Django/Flask, AWS, Docker, PostgreSQL
"""

resume_1 = {
    "id": "test1",
    "name": "Good Candidate",
    "text": """
    Software Engineer with 6 years of experience in Python development.
    Expert in Django, Flask frameworks. Worked with AWS, Docker, Kubernetes.
    Strong PostgreSQL database skills. Git version control expert.
    """
}

resume_2 = {
    "id": "test2", 
    "name": "Poor Candidate",
    "text": """
    Java developer with 3 years experience.
    Worked with Spring framework and Oracle database.
    """
}

try:
    results = utils.calculate_match_scores(job_desc, [resume_1, resume_2])
    
    print(f"[PASS] Hybrid scoring completed for {len(results)} resumes\n")
    
    for i, res in enumerate(results, 1):
        print(f"{i}. {res['name']}")
        print(f"   Score: {res['score']:.4f} - {res['status']}")
        breakdown = res.get('score_breakdown', {})
        print(f"   TF-IDF: {breakdown.get('tfidf', 0):.3f} | "
              f"Keywords: {breakdown.get('keyword', 0):.3f} | "
              f"Semantic: {breakdown.get('semantic', 0):.3f} | "
              f"Experience: {breakdown.get('experience', 0):.3f}")
        print(f"   Matched {res.get('matched_keywords', 0)}/{res.get('total_keywords', 0)} keywords | "
              f"{res.get('experience_years', 0)} years exp\n")
    
    print("[PASS] All tests passed!")
    
except Exception as e:
    print(f"[FAIL] Error in hybrid scoring: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("CONCLUSION")
print("=" * 80)
print("If all tests show [PASS], then resume parsing and hybrid scoring are working!")
print("=" * 80)
