import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    doc = nlp(str(text))
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def match_resume(resume_text, job_desc):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([resume_text, job_desc])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return score[0][0]

# Input: CSV file path and job description
CSV_PATH = "Resume.csv"
JOB_DESCRIPTION = "Python developer with experience in NLP and machine learning."

job_clean = preprocess(JOB_DESCRIPTION)
results = []

# Read the CSV
df = pd.read_csv(CSV_PATH)

# Loop over resumes
for idx, row in df.iterrows():
    resume_text = row["Resume_str"]
    name = row["ID"]
    if pd.notnull(resume_text):
        resume_clean = preprocess(resume_text)
        score = match_resume(resume_clean, job_clean)
        results.append((name, score))
    else:
        results.append((name, 0))

# Output results sorted by score
for name, score in sorted(results, key=lambda x: -x[1]):
    print(f"{name}: Fit score = {score:.2f}")