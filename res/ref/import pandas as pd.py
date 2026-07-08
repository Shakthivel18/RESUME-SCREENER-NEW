import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load SpaCy model
# Ensure you have run: python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    doc = nlp(str(text))
    # Keep only alphanumeric characters and convert to lowercase lemma
    tokens = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def match_resume(resume_text, job_desc):
    # Use ngram_range=(1, 2) to capture single words and two-word phrases
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    tfidf = vectorizer.fit_transform([resume_text, job_desc])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return score[0][0]

# Input: CSV file path and a more specific job description
CSV_PATH = r"C:\Users\Aghamarsh\OneDrive\Desktop\New folder\resume\Resume.csv" # Use 'r' before the string for raw string to handle backslashes

JOB_DESCRIPTION = "Seeking a Senior IT Consultant (18+ years experience) with expertise in technology implementation, project/information management, process analysis, and IT system efficiency; must be proficient in Windows/Mac/Linux, server/web technologies (Exchange, SharePoint, Apache, WordPress), programming (HTML5, CSS, PHP, Java, C++, VB), databases (MySQL, MS SQL, Oracle), Adobe/MS Office applications, and hardware (Dell, HP, Cisco); key expertise includes project/document management, network reporting, web design/development, information security, disaster recovery, and SOP/policy writing; Bachelor's in IT required."

# Define the fit threshold
FIT_THRESHOLD = 0.12 # You can adjust this value based on your requirements.

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
        results.append((name, 0)) # Assign a score of 0 for empty/null resumes

# Output results sorted by score and classified
print(f"--- Resume Classification (Threshold: {FIT_THRESHOLD:.2f}) ---")
for name, score in sorted(results, key=lambda x: -x[1]):
    classification = "Fit" if score >= FIT_THRESHOLD else "Not Fit"
    print(f"{name}: Fit score = {score:.2f} ({classification})")