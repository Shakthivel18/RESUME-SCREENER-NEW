import os
import re
from collections import Counter
import fitz  # PyMuPDF
import docx
from PIL import Image
import pytesseract
import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 1. Text Extraction ---

def extract_text_from_file(file_path):
    """
    Extracts text from a given file based on its extension.
    Supports PDF, DOCX, and common image formats.
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return ""
    
    file_extension = os.path.splitext(file_path)[1].lower()
    text = ""
    
    try:
        if file_extension == ".pdf":
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()
        elif file_extension == ".docx":
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        elif file_extension in [".png", ".jpg", ".jpeg", ".tiff"]:
            try:
                text = pytesseract.image_to_string(Image.open(file_path))
            except Exception as e:
                logger.warning(f"Tesseract OCR failed (is it installed?): {e}")
                return "" # Return empty if OCR fails
        elif file_extension == ".txt":
             with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        else:
            logger.warning(f"Unsupported file format: {file_extension}")
            return ""
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {e}")
        return ""
    
    return text

# --- 2. Text Preprocessing ---

# Load Spacy model once
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.warning("Spacy model 'en_core_web_sm' not found. Using simple fallback preprocessing.")
    nlp = None

def preprocess_text(text):
    """
    Cleans and tokenizes text. Uses Spacy if available, otherwise simple lowercase/split.
    """
    if not text:
        return ""
        
    text = str(text).strip()
    
    if nlp:
        doc = nlp(text)
        # Lemmatize and remove stop words/punctuation
        tokens = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop]
        return " ".join(tokens)
    else:
        # Fallback: simple lowercase and removal of non-alphanumeric (basic)
        import re
        text = text.lower()
        # Keep only letters and spaces
        text = re.sub(r'[^a-z\s]', '', text)
        return text

# --- 3. Advanced Matching Logic with Domain Classification ---

# Import advanced scorer
try:
    from advanced_scorer import AdvancedResumeScorer
    import config
    USE_ADVANCED_SCORER = True
    logger.info("Advanced scoring system loaded successfully")
except ImportError as e:
    logger.warning(f"Advanced scorer not available, using basic hybrid model: {e}")
    USE_ADVANCED_SCORER = False

def extract_keywords(text):
    """
    Extract important keywords like technologies, skills, and certifications.
    Now uses domain-aware keyword extraction if available.
    """
    # Common tech skills, programming languages, frameworks, tools
    tech_keywords = [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust', 'php',
        'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring', 'laravel',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'ci/cd', 'devops',
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'nosql',
        'machine learning', 'deep learning', 'ai', 'nlp', 'computer vision', 'tensorflow', 'pytorch',
        'data science', 'data analysis', 'pandas', 'numpy', 'scikit-learn', 'tableau', 'power bi',
        'agile', 'scrum', 'jira', 'rest api', 'graphql', 'microservices', 'cloud', 'linux',
        'html', 'css', 'sass', 'webpack', 'babel', 'testing', 'jest', 'pytest', 'selenium',
        'security', 'encryption', 'oauth', 'jwt', 'blockchain', 'ethereum', 'solidity'
    ]
    
    text_lower = text.lower()
    found_keywords = []
    
    for keyword in tech_keywords:
        if keyword in text_lower:
            found_keywords.append(keyword)
    
    return found_keywords

def extract_years_of_experience(text):
    """
    Extract years of experience from text using regex patterns.
    Returns the maximum years found, or 0 if none found.
    """
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)',
        r'(?:experience|exp)(?:\s+of)?\s+(\d+)\+?\s*(?:years?|yrs?)',
        r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:in|with|of)',
    ]
    
    years = []
    text_lower = text.lower()
    
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            try:
                years.append(int(match))
            except:
                pass
    
    return max(years) if years else 0

def calculate_keyword_score(jd_keywords, resume_keywords):
    """
    Calculate keyword matching score based on overlap.
    """
    if not jd_keywords:
        return 0.0
    
    jd_set = set(jd_keywords)
    resume_set = set(resume_keywords)
    
    # Calculate Jaccard similarity
    intersection = len(jd_set.intersection(resume_set))
    union = len(jd_set.union(resume_set))
    
    if union == 0:
        return 0.0
    
    jaccard_score = intersection / union
    
    # Also calculate percentage of JD keywords found in resume
    coverage_score = intersection / len(jd_set) if len(jd_set) > 0 else 0.0
    
    # Weighted combination
    return (jaccard_score * 0.4) + (coverage_score * 0.6)

def calculate_semantic_similarity(jd_text, resume_text):
    """
    Calculate semantic similarity using spaCy word embeddings.
    Falls back to token overlap if word vectors are not available.
    """
    if not nlp or not jd_text or not resume_text:
        return 0.0
    
    try:
        # Use spaCy's similarity (requires word vectors)
        jd_doc = nlp(jd_text[:100000])  # Limit to 100k chars for performance
        resume_doc = nlp(resume_text[:100000])
        
        # Check if the model has word vectors
        if jd_doc.has_vector and resume_doc.has_vector:
            # spaCy's built-in similarity uses word vectors
            similarity = jd_doc.similarity(resume_doc)
            return float(similarity)
        else:
            # Fallback: Use token overlap similarity
            logger.debug("Word vectors not available, using token overlap similarity")
            jd_tokens = set([token.lemma_.lower() for token in jd_doc if token.is_alpha and not token.is_stop])
            resume_tokens = set([token.lemma_.lower() for token in resume_doc if token.is_alpha and not token.is_stop])
            
            if not jd_tokens or not resume_tokens:
                return 0.0
            
            # Jaccard similarity of lemmatized tokens
            intersection = len(jd_tokens.intersection(resume_tokens))
            union = len(jd_tokens.union(resume_tokens))
            
            return intersection / union if union > 0 else 0.0
            
    except Exception as e:
        logger.warning(f"Semantic similarity calculation failed: {e}")
        return 0.0

def calculate_experience_score(jd_years, resume_years):
    """
    Calculate experience matching score.
    """
    if jd_years == 0:
        return 0.5  # Neutral score if no experience requirement specified
    
    if resume_years == 0:
        return 0.0  # Low score if resume doesn't mention experience
    
    # Perfect match gets 1.0, decreasing score for mismatch
    difference = abs(jd_years - resume_years)
    
    if difference == 0:
        return 1.0
    elif difference <= 2:
        return 0.8
    elif difference <= 5:
        return 0.5
    else:
        return 0.2

def calculate_match_scores(job_description, resume_data_list, job_title=None):
    """
    Advanced scoring system with domain classification and multi-factor analysis.
    
    Uses the AdvancedResumeScorer if available, otherwise falls back to basic hybrid model.
    
    Args:
        job_description (str): The recruiter's job description.
        resume_data_list (list): List of dicts, e.g., [{'id': '...', 'name': '...', 'text': '...'}]
        job_title (str): Optional job title for specific role matching.
        
    Returns:
        list: The input list with added 'score', 'status', score breakdown, and domain info.
    """
    if not job_description or not resume_data_list:
        return []

    logger.info(f"Starting advanced scoring for {len(resume_data_list)} resumes...")
    
    # Use advanced scorer if available
    if USE_ADVANCED_SCORER:
        return _calculate_advanced_scores(job_description, resume_data_list, job_title)
    else:
        return _calculate_basic_hybrid_scores(job_description, resume_data_list, job_title)

def _calculate_advanced_scores(job_description, resume_data_list, job_title=None):
    """
    Advanced scoring with domain classification
    """
    scorer = AdvancedResumeScorer()
    
    # Detect primary domain from job description
    domain_scores = scorer.detect_domain(job_description)
    primary_domain = domain_scores[0][0] if domain_scores else "GENERAL_IT"
    primary_domain_score = domain_scores[0][1] if domain_scores else 0.0
    
    domain_name = config.DOMAINS[primary_domain]['name']
    logger.info(f"Detected primary domain: {domain_name} (confidence: {primary_domain_score:.2f})")
    
    # Preprocess texts
    jd_clean = preprocess_text(job_description)
    resume_texts_clean = [preprocess_text(item.get('text', '')) for item in resume_data_list]
    
    # Extract JD features
    jd_keywords = scorer.extract_domain_keywords(job_description, primary_domain)
    jd_years = scorer.extract_years_of_experience(job_description)
    
    logger.info(f"JD Analysis - Domain: {domain_name}, Keywords: {len(jd_keywords)}, Required Experience: {jd_years} years")
    
    # Calculate TF-IDF scores for all resumes at once
    tfidf_scores = scorer.calculate_tfidf_score(jd_clean, resume_texts_clean)
    
    results = []
    
    for i, resume_item in enumerate(resume_data_list):
        resume_text = resume_item.get('text', '')
        
        # Extract resume features
        resume_keywords = scorer.extract_domain_keywords(resume_text, primary_domain)
        resume_years = scorer.extract_years_of_experience(resume_text)
        
        # Calculate component scores
        component_scores = {
            'tfidf': tfidf_scores[i],
            'keyword': scorer.calculate_keyword_score(jd_keywords, resume_keywords),
            'semantic': scorer.calculate_semantic_similarity(job_description, resume_text, nlp),
            'experience': scorer.calculate_experience_score(jd_years, resume_years),
            'domain': scorer.calculate_domain_score(job_description, resume_text, primary_domain),
            'education': scorer.calculate_education_score(job_description, resume_text),
            'diversity_bonus': scorer.calculate_keyword_diversity(resume_keywords),
            'exact_matches': len(set(jd_keywords).intersection(set(resume_keywords))) / len(jd_keywords) if jd_keywords else 0,
            'role_match': scorer.calculate_role_match(job_title, resume_text)
        }
        
        # Calculate final score
        final_score = scorer.calculate_final_score(component_scores)
        
        # Calculate keyword match percentage
        keyword_match_percent = len(set(jd_keywords).intersection(set(resume_keywords))) / len(jd_keywords) if jd_keywords else 0
        
        # Classify candidate
        status, category = scorer.classify_candidate(final_score, keyword_match_percent)
        should_interview = scorer.should_interview(final_score, keyword_match_percent)
        
        # Detect resume domain
        resume_domains = scorer.detect_domain(resume_text)
        resume_primary_domain = resume_domains[0][0] if resume_domains else "GENERAL_IT"
        
        # Build result
        result = resume_item.copy()
        result['score'] = float(final_score)
        result['status'] = status
        result['category'] = category
        result['should_interview'] = should_interview
        result['score_breakdown'] = {
            'tfidf': float(component_scores['tfidf']),
            'keyword': float(component_scores['keyword']),
            'semantic': float(component_scores['semantic']),
            'experience': float(component_scores['experience']),
            'domain': float(component_scores['domain']),
            'education': float(component_scores['education'])
        }
        result['matched_keywords'] = len(set(jd_keywords).intersection(set(resume_keywords)))
        result['total_keywords'] = len(jd_keywords)
        result['keyword_match_percent'] = float(keyword_match_percent)
        result['experience_years'] = resume_years
        result['required_experience'] = jd_years
        result['jd_domain'] = domain_name
        result['resume_domain'] = config.DOMAINS[resume_primary_domain]['name']
        result['domain_match'] = resume_primary_domain == primary_domain
        
        results.append(result)
    
    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # Log summary
    top_score = results[0]['score'] if results else 0
    interview_count = sum(1 for r in results if r['should_interview'])
    
    logger.info(f"Advanced scoring complete. Top score: {top_score:.4f}, Interview candidates: {interview_count}/{len(results)}")
    
    return results

def _calculate_basic_hybrid_scores(job_description, resume_data_list, job_title=None):
    """
    Fallback to basic hybrid scoring if advanced scorer not available
    """
    logger.info("Using basic hybrid scoring (advanced scorer not available)")
    
    # Preprocess JD
    jd_clean = preprocess_text(job_description)
    jd_keywords = extract_keywords(job_description)
    jd_years = extract_years_of_experience(job_description)
    
    logger.info(f"JD Analysis - Keywords: {len(jd_keywords)}, Required Experience: {jd_years} years")
    
    # Preprocess Resumes
    resume_texts = [preprocess_text(item.get('text', '')) for item in resume_data_list]
    
    # === 1. TF-IDF + Cosine Similarity ===
    corpus = [jd_clean] + resume_texts
    tfidf_scores = []
    
    try:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
        tfidf_matrix = vectorizer.fit_transform(corpus)
        jd_vector = tfidf_matrix[0]
        cosine_similarities = cosine_similarity(jd_vector, tfidf_matrix[1:]).flatten()
        tfidf_scores = cosine_similarities.tolist()
    except Exception as e:
        logger.error(f"TF-IDF calculation failed: {e}")
        tfidf_scores = [0.0] * len(resume_data_list)
    
    # === 2. Calculate all scores ===
    results = []
    
    for i, resume_item in enumerate(resume_data_list):
        resume_text = resume_item.get('text', '')
        
        # TF-IDF Score (40% weight)
        tfidf_score = tfidf_scores[i]
        
        # Keyword Matching Score (30% weight)
        resume_keywords = extract_keywords(resume_text)
        keyword_score = calculate_keyword_score(jd_keywords, resume_keywords)
        
        # Semantic Similarity Score (20% weight)
        semantic_score = calculate_semantic_similarity(job_description, resume_text)
        
        # Experience Matching Score (10% weight)
        resume_years = extract_years_of_experience(resume_text)
        experience_score = calculate_experience_score(jd_years, resume_years)
        
        # === Hybrid Score Calculation ===
        hybrid_score = (
            tfidf_score * 0.40 +
            keyword_score * 0.30 +
            semantic_score * 0.20 +
            experience_score * 0.10
        )
        
        # Create result with detailed breakdown
        result = resume_item.copy()
        result['score'] = float(hybrid_score)
        result['score_breakdown'] = {
            'tfidf': float(tfidf_score),
            'keyword': float(keyword_score),
            'semantic': float(semantic_score),
            'experience': float(experience_score)
        }
        result['matched_keywords'] = len(set(jd_keywords).intersection(set(resume_keywords)))
        result['total_keywords'] = len(jd_keywords)
        result['experience_years'] = resume_years
        
        # Dynamic threshold based on hybrid score
        # Dynamic threshold based on hybrid score (Scaled to 0-100)
        final_percent = hybrid_score * 140 # Consistency with advanced scorer
        final_percent = min(final_percent, 100.0)

        result['score'] = float(final_percent)
        
        if final_percent >= config.THRESHOLDS["excellent"]:
            result['status'] = "Excellent Fit"
        elif final_percent >= config.THRESHOLDS["good"]:
            result['status'] = "Good Fit"
        elif final_percent >= config.THRESHOLDS["potential"]:
            result['status'] = "Potential Fit"
        else:
            result['status'] = "Not Fit"
        
        results.append(result)
    
    # Sort by hybrid score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    
    top_score = results[0]['score'] if results else 0
    logger.info(f"Hybrid scoring complete. Top score: {top_score:.4f}")
    
    
    return results


# --- 4. LLM Summarization (Optional) ---
# NOTE: This is currently for Summarization, NOT format parsing.

def calculate_answer_similarity(question, answer):
    """
    Calculates semantic similarity between question and answer to score relevance.
    Used for AI Interviewer fallback scoring.
    """
    import re
    if not question or not answer:
        return 0.0
    
    # 1. Spacy Semantic Similarity (if available)
    if nlp:
        try:
            q_doc = nlp(question)
            a_doc = nlp(answer)
            if q_doc.has_vector and a_doc.has_vector:
                return float(q_doc.similarity(a_doc))
        except:
            pass
            
    # 2. Key Term Overlap (Fallback)
    q_words = set(re.findall(r'\w+', question.lower()))
    a_words = set(re.findall(r'\w+', answer.lower()))
    
    # Remove common stop words (manual list as fallback)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'what', 'how', 'why', 'tell', 'me', 'about', 'describe', 'explain'}
    
    q_keywords = q_words - stop_words
    a_keywords = a_words - stop_words
    
    if not q_keywords:
        return 0.5 # Neutral if question is only stop words
    
    # Check overlap
    overlap = len(q_keywords.intersection(a_keywords))
    
    # Score calculation:
    # 1. Coverage: What % of question keywords are addressed?
    coverage = overlap / len(q_keywords)
    
    return min(coverage * 1.5, 1.0) # Boost score slightly as answers often paraphrase



