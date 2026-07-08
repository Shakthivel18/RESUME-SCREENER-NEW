# Hybrid Resume Scoring Model Documentation

## Overview

The resume screening application now uses a **sophisticated hybrid scoring algorithm** that combines multiple techniques to provide more accurate and nuanced candidate rankings. This replaces the previous single-method TF-IDF approach with a multi-faceted evaluation system.

## Scoring Components

The hybrid model evaluates resumes across **4 key dimensions**, each with its own weight in the final score:

### 1. TF-IDF + Cosine Similarity (40% weight)
- **What it does**: Measures overall text similarity between job description and resume
- **How it works**: Uses Term Frequency-Inverse Document Frequency vectorization with bigrams (1-2 word phrases)
- **Why it matters**: Captures general relevance and domain alignment
- **Technical details**: 
  - Uses scikit-learn's TfidfVectorizer with ngram_range=(1, 2)
  - Limited to 5000 features for performance
  - Calculates cosine similarity between JD and resume vectors

### 2. Keyword Matching (30% weight)
- **What it does**: Identifies exact matches of important technical skills and technologies
- **How it works**: Extracts keywords from a curated list of 70+ technologies, frameworks, and tools
- **Why it matters**: Ensures candidates have the specific skills required
- **Keyword categories**:
  - Programming languages (Python, Java, JavaScript, TypeScript, C++, etc.)
  - Frameworks (React, Angular, Django, Flask, Spring, etc.)
  - Cloud platforms (AWS, Azure, GCP)
  - DevOps tools (Docker, Kubernetes, Jenkins, Git, CI/CD)
  - Databases (SQL, MySQL, PostgreSQL, MongoDB, Redis, etc.)
  - Data Science/ML (TensorFlow, PyTorch, Pandas, NumPy, etc.)
  - Methodologies (Agile, Scrum, REST API, GraphQL, Microservices)
- **Scoring method**: Combines Jaccard similarity (40%) and coverage score (60%)

### 3. Semantic Similarity (20% weight)
- **What it does**: Understands meaning and context beyond exact word matches
- **How it works**: Uses spaCy's word embeddings to calculate semantic similarity
- **Why it matters**: Captures conceptual alignment even when different terminology is used
- **Technical details**: 
  - Leverages spaCy's en_core_web_sm model
  - Compares document-level embeddings
  - Gracefully degrades if spaCy model unavailable

### 4. Experience Level Matching (10% weight)
- **What it does**: Matches years of experience between JD requirements and candidate background
- **How it works**: Uses regex patterns to extract experience mentions
- **Why it matters**: Ensures candidates meet seniority requirements
- **Scoring logic**:
  - Perfect match (0 years difference): 1.0
  - Close match (1-2 years difference): 0.8
  - Moderate match (3-5 years difference): 0.5
  - Large difference (6+ years): 0.2
  - No requirement specified: 0.5 (neutral)

## Final Score Calculation

```
Hybrid Score = (TF-IDF × 0.40) + (Keywords × 0.30) + (Semantic × 0.20) + (Experience × 0.10)
```

## Status Classification

Based on the hybrid score, candidates are classified into four categories:

| Score Range | Status | Meaning |
|-------------|--------|---------|
| ≥ 0.15 | **Excellent Fit** | Strong match across multiple dimensions |
| 0.10 - 0.14 | **Good Fit** | Solid candidate worth interviewing |
| 0.05 - 0.09 | **Potential Fit** | May be suitable with some gaps |
| < 0.05 | **Not Fit** | Significant mismatch with requirements |

## API Response Format

The `/api/match-resumes` endpoint now returns enhanced information:

```json
{
  "message": "Matching process completed successfully!",
  "matched_resumes": [
    {
      "id": "candidate_resume.pdf",
      "name": "candidate_resume.pdf",
      "score": 0.2345,
      "status": "Excellent Fit",
      "source": "upload",
      "score_breakdown": {
        "tfidf": 0.3456,
        "keyword": 0.4567,
        "semantic": 0.1234,
        "experience": 0.8000
      },
      "matched_keywords": 12,
      "total_keywords": 15,
      "experience_years": 5
    }
  ]
}
```

## Console Output

When matching resumes, the top 10 candidates are displayed in the console with detailed breakdowns:

```
==================================================
TOP 10 MATCHES for Job Description
==================================================
1. [0.2345] john_doe_resume.pdf - Excellent Fit
    TF-IDF: 0.346 | Keywords: 0.457 | Semantic: 0.123 | Experience: 0.800
    Matched 12/15 keywords | 5 years experience
2. [0.1987] jane_smith_resume.pdf - Good Fit
    TF-IDF: 0.289 | Keywords: 0.378 | Semantic: 0.098 | Experience: 0.500
    Matched 9/15 keywords | 3 years experience
...
==================================================
```

## Advantages of Hybrid Approach

1. **More Accurate**: Combines multiple signals instead of relying on a single metric
2. **Transparent**: Score breakdown shows exactly why a candidate ranked high or low
3. **Balanced**: Weights prevent any single factor from dominating the score
4. **Flexible**: Easy to adjust weights based on specific hiring needs
5. **Robust**: Gracefully handles missing data or model failures
6. **Explainable**: Recruiters can see matched keywords and experience levels

## Customization

To adjust the scoring weights, modify the hybrid score calculation in `utils.py`:

```python
hybrid_score = (
    tfidf_score * 0.40 +      # Adjust these weights
    keyword_score * 0.30 +    # to match your priorities
    semantic_score * 0.20 +
    experience_score * 0.10
)
```

To add more keywords, update the `tech_keywords` list in the `extract_keywords()` function.

## Performance Considerations

- TF-IDF vectorization is limited to 5000 features for performance
- Semantic similarity limits text to 1M characters per document
- The hybrid model adds minimal overhead compared to TF-IDF alone
- Suitable for processing hundreds to thousands of resumes efficiently

## Future Enhancements

Potential improvements to consider:

1. **Education matching**: Detect and score degree requirements
2. **Location matching**: Geographic preference alignment
3. **Industry experience**: Domain-specific experience detection
4. **Certification matching**: Professional certifications and licenses
5. **Custom keyword lists**: Per-job customizable skill requirements
6. **ML-based scoring**: Train a model on historical hiring decisions
7. **Soft skills detection**: Leadership, communication, teamwork indicators

---

**Last Updated**: January 15, 2026
**Version**: 2.0 (Hybrid Model)
