# Advanced Resume Screening System - Complete Guide

## 🚀 Overview

The resume screening system has been upgraded with a **sophisticated multi-domain classification and advanced scoring algorithm** that provides:

- **10 Domain Categories** with specialized keyword sets
- **6-Factor Scoring** (TF-IDF, Keywords, Semantic, Experience, Domain, Education)
- **Configurable Thresholds** for different fit levels
- **Interview Recommendations** based on multiple criteria
- **Education Level Matching**
- **Transparent Scoring** with detailed breakdowns

---

## 📊 Domain Categories

The system automatically detects and classifies resumes into these domains:

### 1. **Software Engineering**
- **Keywords**: Python, Java, JavaScript, React, Django, Flask, Git, Agile, TDD, Design Patterns
- **Focus**: General software development, coding, testing, version control

### 2. **Data Science & Machine Learning**
- **Keywords**: Python, R, TensorFlow, PyTorch, Pandas, NumPy, NLP, Computer Vision, Kaggle
- **Focus**: ML/AI, data analysis, statistical modeling, feature engineering

### 3. **DevOps & Cloud Engineering**
- **Keywords**: AWS, Azure, GCP, Docker, Kubernetes, Terraform, CI/CD, Monitoring, Infrastructure as Code
- **Focus**: Cloud platforms, automation, infrastructure, deployment

### 4. **Frontend Development**
- **Keywords**: HTML, CSS, JavaScript, React, Angular, Vue, Responsive Design, Accessibility, Performance
- **Focus**: UI development, web frameworks, user experience

### 5. **Backend Development**
- **Keywords**: Python, Java, Node.js, Django, Spring, REST API, GraphQL, Databases, Microservices
- **Focus**: Server-side logic, API design, database management

### 6. **Mobile Development**
- **Keywords**: iOS, Android, Swift, Kotlin, React Native, Flutter, Mobile UI/UX
- **Focus**: Mobile app development, cross-platform frameworks

### 7. **Cybersecurity**
- **Keywords**: Security, Penetration Testing, Encryption, OWASP, Compliance, Incident Response
- **Focus**: Security assessment, ethical hacking, compliance

### 8. **UI/UX Design**
- **Keywords**: Figma, Sketch, Adobe XD, Wireframing, Prototyping, User Research, Design Systems
- **Focus**: User interface and experience design

### 9. **Product Management**
- **Keywords**: Product Strategy, Roadmap, Agile, Stakeholder Management, KPIs, A/B Testing
- **Focus**: Product lifecycle, strategy, cross-functional leadership

### 10. **General IT**
- **Keywords**: IT Support, Troubleshooting, Networking, Active Directory, ITIL, Help Desk
- **Focus**: Technical support, IT operations, infrastructure

---

## 🎯 Scoring Algorithm

### Component Weights (Configurable in `config.py`)

```python
TF-IDF Similarity:      25%  # Overall text similarity
Keyword Matching:       30%  # Exact skill matches
Semantic Similarity:    15%  # Contextual understanding
Experience Matching:    10%  # Years of experience
Domain Matching:        15%  # Domain-specific scoring
Education Matching:      5%  # Education level alignment
```

### Scoring Process

1. **Domain Detection**: Automatically identifies the primary domain from job description
2. **Feature Extraction**: Extracts keywords, experience, education from both JD and resume
3. **Multi-Factor Scoring**: Calculates 6 component scores
4. **Weighted Combination**: Combines scores using configured weights
5. **Classification**: Assigns category and interview recommendation

---

## 📈 Thresholds & Classification

### Score Thresholds (Configurable)

| Score Range | Category | Status | Interview |
|-------------|----------|--------|-----------|
| ≥ 0.20 | Excellent | Excellent Fit - Highly Recommended | ✓ Yes |
| 0.15 - 0.19 | Good | Good Fit - Recommended | ✓ Yes |
| 0.10 - 0.14 | Potential | Potential Fit - Consider | ✓ Yes |
| 0.05 - 0.09 | Marginal | Marginal Fit - Review Carefully | ✗ No |
| < 0.05 | Reject | Not Fit - Reject | ✗ No |

### Additional Filters

- **Minimum Interview Score**: 0.10 (configurable)
- **Minimum Keyword Match**: 30% of required keywords
- **Auto-Reject Below Threshold**: Enabled by default

---

## 🔧 Configuration Options

All settings are in `config.py`:

### Adjust Scoring Weights

```python
SCORING_WEIGHTS = {
    "tfidf": 0.25,
    "keyword": 0.30,
    "semantic": 0.15,
    "experience": 0.10,
    "domain": 0.15,
    "education": 0.05
}
```

### Modify Thresholds

```python
THRESHOLDS = {
    "excellent": 0.20,
    "good": 0.15,
    "potential": 0.10,
    "marginal": 0.05,
    "reject": 0.05
}
```

### Add Custom Keywords to Domains

```python
DOMAINS["SOFTWARE_ENGINEERING"]["keywords"].extend([
    'your_custom_keyword',
    'another_technology'
])
```

### Enable/Disable Features

```python
STRICT_FILTERING = False          # Strict filtering mode
AUTO_REJECT_BELOW_THRESHOLD = True  # Auto-reject low scores
MIN_KEYWORD_MATCH_PERCENT = 0.30    # 30% minimum keyword match
```

---

## 📤 API Response Format

### Enhanced Response Structure

```json
{
  "message": "Matching process completed successfully!",
  "matched_resumes": [
    {
      "id": "resume.pdf",
      "name": "resume.pdf",
      "score": 0.2456,
      "status": "Excellent Fit - Highly Recommended",
      "category": "excellent",
      "should_interview": true,
      "score_breakdown": {
        "tfidf": 0.3456,
        "keyword": 0.5234,
        "semantic": 0.1876,
        "experience": 0.8000,
        "domain": 0.6543,
        "education": 0.6000
      },
      "matched_keywords": 15,
      "total_keywords": 18,
      "keyword_match_percent": 0.8333,
      "experience_years": 6,
      "required_experience": 5,
      "jd_domain": "Software Engineering",
      "resume_domain": "Software Engineering",
      "domain_match": true,
      "source": "upload"
    }
  ]
}
```

---

## 🖥️ Console Output

### Example Output for Top Candidates

```
==================================================
TOP 10 MATCHES for Job Description
==================================================

1. [0.2456] john_doe_resume.pdf
   Status: Excellent Fit - Highly Recommended
   JD Domain: Software Engineering | Resume Domain: Software Engineering
   Domain Match: ✓ Match
   Scores: TF-IDF=0.346 | Keywords=0.523 | Semantic=0.188
           Experience=0.800 | Domain=0.654 | Education=0.600
   Keywords: 15/18 (83.3% match)
   Experience: 6 years (Required: 5)
   Interview: ✓ RECOMMEND

2. [0.1987] jane_smith_resume.pdf
   Status: Good Fit - Recommended
   JD Domain: Software Engineering | Resume Domain: Software Engineering
   Domain Match: ✓ Match
   Scores: TF-IDF=0.289 | Keywords=0.412 | Semantic=0.145
           Experience=0.500 | Domain=0.543 | Education=0.800
   Keywords: 12/18 (66.7% match)
   Experience: 3 years (Required: 5)
   Interview: ✓ RECOMMEND

==================================================
```

---

## 🎓 Education Level Detection

The system automatically detects education levels:

- **PhD/Doctorate**: Highest score (1.0)
- **Master's Degree**: High score (0.8)
- **Bachelor's Degree**: Medium score (0.6)
- **Associate/Diploma**: Lower score (0.4)
- **None Detected**: Minimal score (0.2)

**Keywords Detected**:
- PhD: "phd", "ph.d", "doctorate", "doctoral"
- Master's: "masters", "master's", "m.s", "m.tech", "mba"
- Bachelor's: "bachelors", "bachelor's", "b.s", "b.tech", "b.e"
- Associate: "associate", "diploma", "certification"

---

## 🚀 How to Use

### 1. **Upload Resumes**
- Navigate to http://localhost:5000
- Upload PDF, DOCX, or image files
- System automatically extracts and processes text

### 2. **Enter Job Description**
- Paste or type the complete job description
- Include required skills, experience level, education
- Be specific about domain and technologies

### 3. **Get Results**
- System automatically detects domain
- Scores all resumes across 6 factors
- Provides interview recommendations
- Shows detailed breakdowns

### 4. **Review Candidates**
- Check console for top 10 detailed breakdowns
- Review API response for all candidates
- Filter by `should_interview` flag
- Sort by score or category

---

## 🔬 Advanced Features

### 1. **Domain-Aware Keyword Extraction**
- Extracts keywords specific to detected domain
- Prioritizes domain-relevant skills
- Reduces noise from irrelevant keywords

### 2. **Multi-Factor Experience Scoring**
- Nuanced scoring based on experience gap
- Considers overqualification vs underqualification
- Rewards close matches more heavily

### 3. **Diversity Bonus**
- Rewards candidates with varied skill sets
- Adds bonus for high keyword diversity
- Encourages well-rounded candidates

### 4. **Exact Skill Boost**
- Multiplier for candidates with exact skill matches
- Rewards precision in skill alignment
- Configurable boost factor

### 5. **Graceful Degradation**
- Falls back to basic hybrid scoring if advanced scorer unavailable
- Handles missing spaCy word vectors
- Continues operation even with component failures

---

## 📊 Performance Considerations

- **TF-IDF**: Limited to 10,000 features with trigrams for better context
- **Semantic Similarity**: Text limited to 100k characters per document
- **Batch Processing**: TF-IDF calculated once for all resumes
- **Efficient**: Suitable for hundreds to thousands of resumes
- **Scalable**: Can be optimized further with caching and parallel processing

---

## 🛠️ Customization Examples

### Example 1: Adjust for Senior Roles

```python
# In config.py
SCORING_WEIGHTS["experience"] = 0.20  # Increase experience weight
SCORING_WEIGHTS["keyword"] = 0.25     # Decrease keyword weight
THRESHOLDS["excellent"] = 0.25        # Raise bar for excellence
```

### Example 2: Focus on Skills Over Experience

```python
SCORING_WEIGHTS["keyword"] = 0.40     # Emphasize skills
SCORING_WEIGHTS["experience"] = 0.05  # De-emphasize experience
MIN_KEYWORD_MATCH_PERCENT = 0.50      # Require 50% keyword match
```

### Example 3: Domain-Specific Hiring

```python
# Add specialized keywords for your domain
DOMAINS["SOFTWARE_ENGINEERING"]["keywords"].extend([
    'your_framework',
    'proprietary_tool',
    'specific_methodology'
])
```

---

## 🎯 Best Practices

1. **Write Detailed Job Descriptions**: More keywords = better matching
2. **Specify Experience Clearly**: Use "5+ years" or "3-5 years"
3. **Mention Education Requirements**: Include degree requirements
4. **List Technologies**: Be specific about required tools/frameworks
5. **Review Thresholds**: Adjust based on your hiring standards
6. **Check Domain Detection**: Verify the detected domain is correct
7. **Use Interview Flag**: Filter candidates by `should_interview`
8. **Review Score Breakdowns**: Understand why candidates scored high/low

---

## 📝 Files Created

1. **`config.py`** - Configuration file with all settings
2. **`advanced_scorer.py`** - Advanced scoring algorithm implementation
3. **`utils.py`** - Updated with advanced scoring integration
4. **`main.py`** - Enhanced API endpoints with detailed output

---

## ✅ Status

✅ **Advanced Scoring System**: Fully operational  
✅ **Domain Classification**: 10 categories implemented  
✅ **Configurable Thresholds**: All settings in config.py  
✅ **Interview Recommendations**: Automated based on criteria  
✅ **Education Matching**: Automatic detection and scoring  
✅ **Enhanced API**: Comprehensive response format  
✅ **Detailed Console Output**: Top 10 with full breakdowns  

---

**Version**: 3.0 (Advanced Multi-Domain System)  
**Last Updated**: January 15, 2026, 8:45 PM IST  
**Status**: Production Ready 🚀
