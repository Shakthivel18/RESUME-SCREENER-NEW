# Quick Reference - Resume Screening System

## 🎯 Scoring Thresholds

| Score | Category | Status | Action |
|-------|----------|--------|--------|
| ≥ 0.20 | Excellent | Excellent Fit - Highly Recommended | ✓ Interview |
| 0.15-0.19 | Good | Good Fit - Recommended | ✓ Interview |
| 0.10-0.14 | Potential | Potential Fit - Consider | ✓ Interview |
| 0.05-0.09 | Marginal | Marginal Fit - Review Carefully | ✗ Reject |
| < 0.05 | Reject | Not Fit - Reject | ✗ Reject |

**Minimum Interview Score**: 0.10  
**Minimum Keyword Match**: 30%

---

## 📊 Scoring Weights

| Component | Weight | Purpose |
|-----------|--------|---------|
| TF-IDF | 25% | Overall text similarity |
| Keywords | 30% | Exact skill matches |
| Semantic | 15% | Contextual understanding |
| Experience | 10% | Years of experience match |
| Domain | 15% | Domain-specific alignment |
| Education | 5% | Education level match |

**Total**: 100%

---

## 🏢 10 Domain Categories

1. **Software Engineering** - General software development, coding, testing
2. **Data Science & ML** - Machine learning, AI, data analysis
3. **DevOps & Cloud** - Cloud platforms, automation, infrastructure
4. **Frontend Development** - UI development, web frameworks
5. **Backend Development** - Server-side logic, APIs, databases
6. **Mobile Development** - iOS, Android, cross-platform apps
7. **Cybersecurity** - Security assessment, compliance, ethical hacking
8. **UI/UX Design** - User interface and experience design
9. **Product Management** - Product strategy, stakeholder management
10. **General IT** - IT support, troubleshooting, operations

---

## 🎓 Education Levels

| Level | Score | Keywords |
|-------|-------|----------|
| PhD | 1.0 | phd, ph.d, doctorate, doctoral |
| Master's | 0.8 | masters, m.s, m.tech, mba |
| Bachelor's | 0.6 | bachelors, b.s, b.tech, b.e |
| Associate | 0.4 | associate, diploma, certification |
| None | 0.2 | (not detected) |

---

## 🔧 Quick Configuration

### To Adjust Thresholds
Edit `config.py`:
```python
THRESHOLDS = {
    "excellent": 0.20,  # Change these values
    "good": 0.15,
    "potential": 0.10,
    "marginal": 0.05,
    "reject": 0.05
}
```

### To Change Scoring Weights
Edit `config.py`:
```python
SCORING_WEIGHTS = {
    "tfidf": 0.25,      # Adjust these percentages
    "keyword": 0.30,    # Must sum to 1.0
    "semantic": 0.15,
    "experience": 0.10,
    "domain": 0.15,
    "education": 0.05
}
```

### To Add Keywords to a Domain
Edit `config.py`:
```python
DOMAINS["SOFTWARE_ENGINEERING"]["keywords"].extend([
    'your_keyword_here',
    'another_technology'
])
```

---

## 📤 API Response Fields

### Core Fields (Always Present)
- `id` - Resume identifier
- `name` - Resume filename
- `score` - Final hybrid score (0-1)
- `status` - Classification status
- `source` - "upload" or "database"
- `score_breakdown` - Dict with all component scores
- `matched_keywords` - Number of matched keywords
- `total_keywords` - Total keywords in JD
- `experience_years` - Detected years of experience

### Advanced Fields (When Available)
- `category` - "excellent", "good", "potential", "marginal", "reject"
- `should_interview` - Boolean recommendation
- `keyword_match_percent` - Percentage of keywords matched (0-1)
- `required_experience` - Required years from JD
- `jd_domain` - Detected job description domain
- `resume_domain` - Detected resume domain
- `domain_match` - Boolean if domains match

---

## 🖥️ Console Output Format

```
1. [0.2456] candidate_name.pdf
   Status: Excellent Fit - Highly Recommended
   JD Domain: Software Engineering | Resume Domain: Software Engineering
   Domain Match: ✓ Match
   Scores: TF-IDF=0.346 | Keywords=0.523 | Semantic=0.188
           Experience=0.800 | Domain=0.654 | Education=0.600
   Keywords: 15/18 (83.3% match)
   Experience: 6 years (Required: 5)
   Interview: ✓ RECOMMEND
```

---

## 🚀 Quick Start

1. **Start Server**: `python main.py`
2. **Open Browser**: http://localhost:5000
3. **Upload Resumes**: Click upload button
4. **Enter Job Description**: Paste JD with requirements
5. **Click Match**: Get ranked results
6. **Review Console**: See top 10 detailed breakdowns
7. **Check API Response**: Full results with all fields

---

## 📊 Interpretation Guide

### High Score (≥ 0.20)
- Strong match across multiple dimensions
- Recommend for immediate interview
- Likely has required skills and experience

### Good Score (0.15-0.19)
- Solid candidate worth considering
- May have minor gaps but overall good fit
- Recommend for interview

### Potential Score (0.10-0.14)
- Some alignment with requirements
- Review carefully for specific needs
- Consider if candidate pool is limited

### Low Score (< 0.10)
- Significant mismatch with requirements
- Missing critical skills or experience
- Generally not recommended

---

## 🎯 Best Practices

✓ Write detailed job descriptions with specific keywords  
✓ Specify experience requirements clearly (e.g., "5+ years")  
✓ Include education requirements if applicable  
✓ List all required technologies and tools  
✓ Review top 10 console output for insights  
✓ Use `should_interview` flag to filter candidates  
✓ Adjust thresholds based on your hiring standards  
✓ Check domain detection accuracy  

---

## 🔍 Troubleshooting

**Low Scores for Good Candidates?**
- Lower the thresholds in `config.py`
- Adjust scoring weights to emphasize different factors
- Add more domain-specific keywords

**Too Many Interview Recommendations?**
- Raise `MIN_INTERVIEW_SCORE` in `config.py`
- Increase `MIN_KEYWORD_MATCH_PERCENT`
- Raise threshold values

**Wrong Domain Detected?**
- Add more specific keywords to correct domain
- Review job description for clarity
- Manually specify domain if needed

---

**Version**: 3.0  
**Last Updated**: January 15, 2026
