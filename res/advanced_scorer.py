"""
Advanced Resume Scoring Algorithm
Implements domain classification, multi-factor scoring, and intelligent filtering
"""

import re
import os
import numpy as np
import joblib
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
import logging

logger = logging.getLogger(__name__)

import config

class AdvancedResumeScorer:
    """
    Advanced scoring system with domain classification and multi-factor analysis
    """
    
    def __init__(self):
        self.domains = config.DOMAINS
        self.weights = config.SCORING_WEIGHTS
        self.thresholds = config.THRESHOLDS
        
        # Load ML Models
        _script_dir = os.path.dirname(os.path.abspath(__file__))
        classifier_path = os.path.join(_script_dir, "models", "domain_classifier_pipeline.joblib")
        w2v_path = os.path.join(_script_dir, "models", "resume_word2vec.model")
        
        try:
            if os.path.exists(classifier_path):
                self.classifier = joblib.load(classifier_path)
                logger.info("Loaded ML Domain Classifier model successfully.")
            else:
                self.classifier = None
                logger.warning(f"Domain classifier model not found at {classifier_path}. Using fallback.")
        except Exception as e:
            self.classifier = None
            logger.error(f"Error loading domain classifier model: {e}")
            
        try:
            if os.path.exists(w2v_path):
                self.w2v_model = Word2Vec.load(w2v_path)
                logger.info("Loaded Word2Vec embedding model successfully.")
            else:
                self.w2v_model = None
                logger.warning(f"Word2Vec model not found at {w2v_path}. Using fallback.")
        except Exception as e:
            self.w2v_model = None
            logger.error(f"Error loading Word2Vec model: {e}")
        
    def detect_domain(self, text):
        """
        Detect the most relevant domain(s) for a job description or resume using the trained ML model.
        Returns: List of (domain_key, score) tuples sorted by relevance
        """
        if not self.classifier:
            return self._detect_domain_fallback(text)
            
        try:
            # Predict probability distribution across 24 categories
            probs = self.classifier.predict_proba([text])[0]
            classes = self.classifier.classes_
            
            # Map pre-trained category labels to app domain keys
            category_to_domain = {
                'INFORMATION-TECHNOLOGY': 'SOFTWARE_ENGINEERING',
                'ENGINEERING': 'SOFTWARE_ENGINEERING',
                'DESIGNER': 'UI_UX_DESIGN',
                'HR': 'GENERAL_IT',
                'BUSINESS-DEVELOPMENT': 'PRODUCT_MANAGEMENT',
                'FINANCE': 'GENERAL_IT',
                'ACCOUNTANT': 'GENERAL_IT'
            }
            
            domain_scores = {k: 0.0 for k in self.domains.keys()}
            
            for cls, prob in zip(classes, probs):
                domain_key = category_to_domain.get(cls, 'GENERAL_IT')
                # If category directly maps to a domain (after converting format)
                clean_cls = cls.replace('-', '_').upper()
                if clean_cls in self.domains:
                    domain_scores[clean_cls] = max(domain_scores[clean_cls], float(prob))
                else:
                    domain_scores[domain_key] = max(domain_scores[domain_key], float(prob))
            
            # Sort by score descending
            sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
            return sorted_domains
            
        except Exception as e:
            logger.error(f"ML Domain detection failed: {e}. Using fallback.")
            return self._detect_domain_fallback(text)
            
    def _detect_domain_fallback(self, text):
        """Rule-based fallback for domain detection"""
        text_lower = text.lower()
        domain_scores = {}
        
        for domain_key, domain_info in self.domains.items():
            keywords = domain_info['keywords']
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            score = matches / len(keywords) if keywords else 0
            domain_scores[domain_key] = score
        
        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_domains
    
    def extract_domain_keywords(self, text, domain_key):
        """
        Extract keywords specific to a domain from text
        """
        if domain_key not in self.domains:
            return []
        
        text_lower = text.lower()
        domain_keywords = self.domains[domain_key]['keywords']
        
        found_keywords = [kw for kw in domain_keywords if kw in text_lower]
        return found_keywords
    
    def calculate_domain_score(self, jd_text, resume_text, primary_domain):
        """
        Calculate domain-specific matching score using ML predicted category profile similarity
        """
        if not self.classifier:
            return self._calculate_domain_score_fallback(jd_text, resume_text, primary_domain)
            
        try:
            # Vector of probabilities across 24 fields
            jd_probs = self.classifier.predict_proba([jd_text])[0]
            resume_probs = self.classifier.predict_proba([resume_text])[0]
            
            # Vector similarity (cosine) represents domain profile match
            dot_product = np.dot(jd_probs, resume_probs)
            norm_jd = np.linalg.norm(jd_probs)
            norm_resume = np.linalg.norm(resume_probs)
            
            if norm_jd * norm_resume > 0:
                sim = dot_product / (norm_jd * norm_resume)
            else:
                sim = 0.0
                
            return float(sim)
        except Exception as e:
            logger.error(f"ML Domain score similarity failed: {e}. Using fallback.")
            return self._calculate_domain_score_fallback(jd_text, resume_text, primary_domain)
            
    def _calculate_domain_score_fallback(self, jd_text, resume_text, primary_domain):
        """Rule-based fallback for domain score"""
        if primary_domain not in self.domains:
            return 0.5
        
        domain_info = self.domains[primary_domain]
        jd_keywords = set(self.extract_domain_keywords(jd_text, primary_domain))
        resume_keywords = set(self.extract_domain_keywords(resume_text, primary_domain))
        
        if not jd_keywords:
            return 0.5
        
        matched = len(jd_keywords.intersection(resume_keywords))
        total = len(jd_keywords)
        match_score = matched / total
        
        required_skills = domain_info.get('required_skills', [])
        resume_lower = resume_text.lower()
        required_matches = sum(1 for skill in required_skills if skill in resume_lower)
        required_score = required_matches / len(required_skills) if required_skills else 1.0
        
        domain_score = (match_score * 0.7) + (required_score * 0.3)
        return domain_score
    
    def extract_education_level(self, text):
        """
        Extract highest education level from resume text
        """
        text_lower = text.lower()
        
        for level, keywords in config.EDUCATION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return level
        
        return "none"
    
    def calculate_education_score(self, jd_text, resume_text):
        """
        Calculate education matching score
        """
        jd_education = self.extract_education_level(jd_text)
        resume_education = self.extract_education_level(resume_text)
        
        jd_score = config.EDUCATION_SCORES.get(jd_education, 0.2)
        resume_score = config.EDUCATION_SCORES.get(resume_education, 0.2)
        
        # If resume education >= JD education, full score
        # Otherwise, proportional score
        if resume_score >= jd_score:
            return 1.0
        else:
            return resume_score / jd_score if jd_score > 0 else 0.5
    
    def calculate_keyword_diversity(self, keywords):
        """
        Calculate diversity score based on variety of keywords
        """
        if not keywords:
            return 0.0
        
        # Count unique keywords
        unique_count = len(set(keywords))
        total_count = len(keywords)
        
        # Diversity is ratio of unique to total
        diversity = unique_count / total_count if total_count > 0 else 0
        
        return diversity
    
    def extract_years_of_experience(self, text):
        """
        Extract years of experience using multiple patterns
        """
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)',
            r'(?:experience|exp)(?:\s+of)?\s+(\d+)\+?\s*(?:years?|yrs?)',
            r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:in|with|of)',
            r'(\d+)\s*-\s*(\d+)\s*(?:years?|yrs?)',
        ]
        
        years = []
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                try:
                    if isinstance(match, tuple):
                        # Range pattern (e.g., "5-7 years")
                        years.append(max(int(m) for m in match if m))
                    else:
                        years.append(int(match))
                except:
                    pass
        
        return max(years) if years else 0
    
    def calculate_experience_score(self, jd_years, resume_years):
        """
        Calculate experience matching score with more nuanced scoring
        """
        if jd_years == 0:
            return 0.5  # Neutral if no requirement
        
        if resume_years == 0:
            return 0.2  # Low score if no experience mentioned
        
        difference = abs(jd_years - resume_years)
        
        # Perfect match
        if difference == 0:
            return 1.0
        # Within 1 year
        elif difference <= 1:
            return 0.95
        # Within 2 years
        elif difference <= 2:
            return 0.85
        # Within 3 years
        elif difference <= 3:
            return 0.70
        # Within 5 years
        elif difference <= 5:
            return 0.55
        # More experience is better than less
        elif resume_years > jd_years:
            return 0.60  # Overqualified but acceptable
        else:
            return 0.30  # Underqualified
    
    def calculate_tfidf_score(self, jd_text, resume_texts):
        """
        Calculate TF-IDF cosine similarity scores
        """
        try:
            corpus = [jd_text] + resume_texts
            vectorizer = TfidfVectorizer(
                ngram_range=(1, 3),  # Unigrams, bigrams, trigrams
                max_features=10000,
                min_df=1,
                max_df=0.95,
                sublinear_tf=True  # Use log scaling
            )
            
            tfidf_matrix = vectorizer.fit_transform(corpus)
            jd_vector = tfidf_matrix[0]
            
            similarities = cosine_similarity(jd_vector, tfidf_matrix[1:]).flatten()
            return similarities.tolist()
        except Exception as e:
            logger.error(f"TF-IDF calculation failed: {e}")
            return [0.0] * len(resume_texts)
    
    def calculate_keyword_score(self, jd_keywords, resume_keywords, resume_text=""):
        """
        Enhanced keyword matching with weighted scoring and Word2Vec synonym matching.
        """
        if not jd_keywords:
            return 0.0
        
        jd_set = set(jd_keywords)
        resume_set = set(resume_keywords)
        
        # Exact matches
        exact_matches = jd_set.intersection(resume_set)
        matched_count = len(exact_matches)
        
        # Check synonyms for unmatched JD keywords
        unmatched_jd = jd_set - resume_set
        synonym_matches = 0.0
        
        # Pre-tokenize the resume text to search for synonyms
        resume_words = set(re.findall(r'\w+', resume_text.lower())) if resume_text else set()
        
        if self.w2v_model and unmatched_jd and resume_words:
            for kw in unmatched_jd:
                try:
                    if kw in self.w2v_model.wv:
                        syns = self.w2v_model.wv.most_similar(kw, topn=5)
                        for syn_word, similarity in syns:
                            # If a high-similarity synonym (> 0.65) exists in the resume
                            if similarity >= 0.65 and syn_word in resume_words:
                                synonym_matches += similarity
                                break
                except:
                    pass
                    
        total_matched = matched_count + synonym_matches
        total_count = len(jd_set)
        
        # Coverage score (including synonym matches)
        coverage = min(total_matched / total_count, 1.0) if total_count > 0 else 0
        
        # Precision score (what % of resume keywords are relevant)
        precision = matched_count / len(resume_set) if len(resume_set) > 0 else 0
        
        # F1-like score combining coverage and precision
        if coverage + precision > 0:
            f1_score = 2 * (coverage * precision) / (coverage + precision)
        else:
            f1_score = 0
        
        # Weighted combination favoring coverage
        keyword_score = (coverage * 0.7) + (f1_score * 0.3)
        return float(keyword_score)
    
    def calculate_semantic_similarity(self, jd_text, resume_text, nlp=None):
        """
        Calculate semantic similarity using spaCy or fallback
        """
        if not nlp or not jd_text or not resume_text:
            return 0.0
        
        try:
            jd_doc = nlp(jd_text[:100000])
            resume_doc = nlp(resume_text[:100000])
            
            if jd_doc.has_vector and resume_doc.has_vector:
                return float(jd_doc.similarity(resume_doc))
            else:
                # Token overlap fallback
                jd_tokens = set([token.lemma_.lower() for token in jd_doc 
                               if token.is_alpha and not token.is_stop])
                resume_tokens = set([token.lemma_.lower() for token in resume_doc 
                                   if token.is_alpha and not token.is_stop])
                
                if not jd_tokens or not resume_tokens:
                    return 0.0
                
                intersection = len(jd_tokens.intersection(resume_tokens))
                union = len(jd_tokens.union(resume_tokens))
                
                return intersection / union if union > 0 else 0.0
        except Exception as e:
            logger.warning(f"Semantic similarity failed: {e}")
            return 0.0
    def calculate_role_match(self, job_title, resume_text):
        """
        Calculate how well the resume matches the job title.
        Stricter logic: Prioritizes exact matches in the header (first 1000 chars).
        """
        if not job_title or not resume_text:
            return 0.0
        
        job_title = job_title.lower().strip()
        # Only look in the top 1000 characters (Header/Summary) for the primary role
        resume_header = resume_text.lower()[:1000] 
        
        # 1. Exact Match in Header (Strongest)
        if job_title in resume_header:
            return 1.0
        
        # 2. Exact Match in Body (Good)
        if job_title in resume_text.lower()[:5000]:
            return 0.8
        
        # 3. Partial Match logic (Stricter)
        title_words = [w for w in job_title.split() if len(w) > 3] # Ignore "Sr", "Jr", "The"
        if not title_words:
            return 0.0
            
        # Count matches in header
        header_matches = sum(1 for word in title_words if word in resume_header)
        
        if header_matches == len(title_words):
            return 0.9 # All words found in header (even if not as phrase)
        elif header_matches >= len(title_words) / 2:
            return 0.5 # Half words found
            
        return 0.0 # Strict: If not even half words in header, it's 0.
    
    def calculate_final_score(self, component_scores):
        """
        Calculate weighted final score from all components and convert to percentage (0-100)
        """
        raw_score = (
            component_scores.get('tfidf', 0) * self.weights.get('tfidf', 0) +
            component_scores.get('keyword', 0) * self.weights.get('keyword', 0) +
            component_scores.get('semantic', 0) * self.weights.get('semantic', 0) +
            component_scores.get('experience', 0) * self.weights.get('experience', 0) +
            component_scores.get('domain', 0) * self.weights.get('domain', 0) +
            component_scores.get('education', 0) * self.weights.get('education', 0) +
            component_scores.get('role_match', 0) * self.weights.get('role_match', 0)
        )
        
        # Apply bonuses
        if component_scores.get('diversity_bonus', 0) > 0.7:
            raw_score += config.DIVERSITY_BONUS
        
        if component_scores.get('exact_matches', 0) > 0.8:
            raw_score *= config.EXACT_SKILL_BOOST
            
        # Scaling to Percentage (0-100)
        # Raw scores are typically 0.15-0.60.
        # Multiplier of 140 ensures 0.70+ is 98%+, but 0.3 is ~42%.
        
        final_percent = raw_score * 140 
        
        return min(final_percent, 100.0)
    
    def classify_candidate(self, score, keyword_match_percent):
        """
        Classify candidate based on score and other factors
        """
        # Check minimum thresholds
        if config.AUTO_REJECT_BELOW_THRESHOLD and score < self.thresholds['reject']:
            return "Auto Reject", "reject"
        
        if keyword_match_percent < config.MIN_KEYWORD_MATCH_PERCENT:
            return "Insufficient Skills", "reject"
        
        # Classify by score
        if score >= self.thresholds['excellent']:
            return "Excellent Fit - Highly Recommended", "excellent"
        elif score >= self.thresholds['good']:
            return "Good Fit - Recommended", "good"
        elif score >= self.thresholds['potential']:
            return "Potential Fit - Consider", "potential"
        elif score >= self.thresholds['marginal']:
            return "Marginal Fit - Review Carefully", "marginal"
        else:
            return "Not Fit - Reject", "reject"
    
    def should_interview(self, score, keyword_match_percent):
        """
        Determine if candidate should be interviewed
        """
        return (score >= config.MIN_INTERVIEW_SCORE and 
                keyword_match_percent >= config.MIN_KEYWORD_MATCH_PERCENT)
