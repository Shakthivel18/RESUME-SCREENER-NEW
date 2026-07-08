import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# --- Step 1: Pre-requisites and Data Loading ---
# Ensure you have run: python -m spacy download en_core_web_sm
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("SpaCy model 'en_core_web_sm' not found. Please run 'python -m spacy download en_core_web_sm' in your terminal.")
    exit()

# Define the paths for both CSV files
# The training CSV is used to build the vocabulary for the vectorizer.
TRAINING_CSV_PATH = r"C:\Users\Aghamarsh\OneDrive\Desktop\New folder\resume\Resume.csv"
# The candidates CSV contains the resumes to be matched against the job description.
CANDIDATE_CSV_PATH = r"C:\Users\Aghamarsh\OneDrive\Desktop\New folder\resume\Summary.csv"

# --- Step 2: Text Preprocessing and Matching Functions ---
def preprocess(text):
    """
    Cleans and tokenizes text, converting it to lowercase lemmas.
    """
    doc = nlp(str(text))
    tokens = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop and not token.is_punct]
    return " ".join(tokens)

# --- Step 3: Main Logic to Match Candidates ---
def find_best_fit(training_csv, candidate_csv, job_description):
    """
    Finds the best-fit resumes from the candidate CSV based on a job description,
    using the vocabulary from the training CSV.
    """
    # Check if files exist
    if not os.path.exists(training_csv):
        print(f"Error: Training CSV file not found at '{training_csv}'")
        return []
    if not os.path.exists(candidate_csv):
        print(f"Error: Candidate CSV file not found at '{candidate_csv}'")
        return []

    # Read the CSV files
    try:
        training_df = pd.read_csv(training_csv)
        candidate_df = pd.read_csv(candidate_csv)
    except pd.errors.EmptyDataError:
        print("Error: One of the CSV files is empty.")
        return []

    # Preprocess all resumes to build a comprehensive corpus
    # This is the "training" part, where the model learns its vocabulary
    print("Preprocessing all resume data to build vocabulary...")
    all_resumes = pd.concat([training_df["Resume_str"], candidate_df["Resume_str"]])
    preprocessed_corpus = [preprocess(resume) for resume in all_resumes.dropna()]
    
    # Preprocess the job description
    print("Preprocessing job description...")
    job_clean = preprocess(job_description)
    
    # Use ngram_range=(1, 2) to capture single words and two-word phrases
    # Fit the vectorizer on the full corpus to create a unified vocabulary
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    vectorizer.fit(preprocessed_corpus)
    
    # Transform the job description and all candidate resumes into TF-IDF vectors
    job_tfidf = vectorizer.transform([job_clean])
    candidate_tfidfs = vectorizer.transform(candidate_df["Resume_str"].apply(preprocess))

    results = []
    # Calculate cosine similarity for each candidate resume
    print("Calculating fit scores for all candidate resumes...")
    for idx, row in candidate_df.iterrows():
        name = row["ID"]
        resume_tfidf = candidate_tfidfs[idx]
        score = cosine_similarity(job_tfidf, resume_tfidf)[0][0]
        results.append((name, score))

    return results

# --- Step 4: Define Inputs and Run the Process ---
# Input: A more specific job description
JOB_DESCRIPTION = "Seeking a Senior IT Consultant (18+ years experience) with expertise in technology implementation, project/information management, process analysis, and IT system efficiency; must be proficient in Windows/Mac/Linux, server/web technologies (Exchange, SharePoint, Apache, WordPress), programming (HTML5, CSS, PHP, Java, C++, VB), databases (MySQL, MS SQL, Oracle), Adobe/MS Office applications, and hardware (Dell, HP, Cisco); key expertise includes project/document management, network reporting, web design/development, information security, disaster recovery, and SOP/policy writing; Bachelor's in IT required."

# Define the fit threshold
FIT_THRESHOLD = 0.12 # You can adjust this value based on your requirements.

# Run the matching process
results = find_best_fit(TRAINING_CSV_PATH, CANDIDATE_CSV_PATH, JOB_DESCRIPTION)

# Output results sorted by score and classified
if results:
    print(f"\n--- Resume Classification (Threshold: {FIT_THRESHOLD:.2f}) ---")
    for name, score in sorted(results, key=lambda x: -x[1]):
        classification = "Fit" if score >= FIT_THRESHOLD else "Not Fit"
        print(f"{name}: Fit score = {score:.2f} ({classification})")

