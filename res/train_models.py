import os
import re
import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from gensim.models import Word2Vec
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Paths
_script_dir = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(_script_dir, "..", "Resume.csv")
MODELS_DIR = os.path.join(_script_dir, "models")

# Stop words fallback list in case nltk/spacy not fully loaded
STOP_WORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
    'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but',
    'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
    'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
    'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
    'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
    'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren',
    "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't",
    'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't",
    'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn',
    "wouldn't"
}

def clean_text(text):
    """Clean and normalize raw resume text"""
    if not isinstance(text, str):
        return ""
    # Lowercase
    text = text.lower()
    # Remove HTML if any
    text = re.sub(r'<[^>]*>', ' ', text)
    # Keep alphanumeric characters and basic punctuation/spacing
    text = re.sub(r'[^a-zA-Z0-9\s\#\+\-\.]', ' ', text)
    # Collapse multiple whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize(text):
    """Tokenize text into lowercased alphanumeric words, removing stop words"""
    words = clean_text(text).split()
    # Keep words that are not stop words and are at least 2 chars long (excluding C++, C#)
    filtered = []
    for w in words:
        if w in STOP_WORDS:
            continue
        if len(w) >= 2 or w in ('c', 'r'):
            filtered.append(w)
    return filtered

def train_models():
    logger.info(f"Checking for dataset at: {CSV_PATH}")
    if not os.path.exists(CSV_PATH):
        logger.error(f"Dataset not found at {CSV_PATH}. Aborting.")
        return

    logger.info("Reading dataset (Resume.csv)...")
    df = pd.read_csv(CSV_PATH)
    logger.info(f"Loaded {len(df)} resumes.")

    # Drop rows with missing text
    df = df.dropna(subset=['Resume_str', 'Category'])
    logger.info(f"Active dataset size: {len(df)}")

    # Clean text column
    logger.info("Cleaning resume texts...")
    df['cleaned_resume'] = df['Resume_str'].apply(clean_text)

    # Make target models directory
    os.makedirs(MODELS_DIR, exist_ok=True)

    # 1. Train Domain Classifier Model
    logger.info("Training Domain Classifier Model...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=15000,
        sublinear_tf=True,
        stop_words='english'
    )
    
    classifier = LogisticRegression(
        max_iter=1000,
        C=1.0,
        multi_class='multinomial',
        solver='lbfgs',
        random_state=42
    )

    # Fit pipeline
    pipeline = Pipeline([
        ('vectorizer', vectorizer),
        ('classifier', classifier)
    ])

    X = df['cleaned_resume']
    y = df['Category'].str.strip().str.upper()

    logger.info(f"Fitting TF-IDF + LogisticRegression on {len(X)} samples for {len(y.unique())} categories...")
    pipeline.fit(X, y)

    # Save classifier pipeline
    classifier_path = os.path.join(MODELS_DIR, "domain_classifier_pipeline.joblib")
    joblib.dump(pipeline, classifier_path)
    logger.info(f"Saved Domain Classifier Pipeline to {classifier_path}")

    # 2. Train Word2Vec Embedding Model
    logger.info("Tokenizing text for Word2Vec training...")
    sentences = df['Resume_str'].apply(tokenize).tolist()

    # Train Word2Vec model
    logger.info(f"Training Word2Vec model on {len(sentences)} document sentences...")
    
    w2v_model = Word2Vec(
        sentences=sentences,
        vector_size=100,     # Size of embedding vector
        window=5,            # Context window size
        min_count=2,         # Ignore words with total frequency < 2
        workers=4,           # Parallel threads
        epochs=15,           # Epochs
        seed=42
    )

    # Save Word2Vec model
    w2v_path = os.path.join(MODELS_DIR, "resume_word2vec.model")
    w2v_model.save(w2v_path)
    logger.info(f"Saved Word2Vec model to {w2v_path}")

    # Print some test synonyms
    logger.info("Verifying model semantic quality (top 5 synonyms for 'python'):")
    try:
        syns = w2v_model.wv.most_similar('python', topn=5)
        for word, sim in syns:
            logger.info(f"  - {word}: {sim:.4f}")
    except Exception as e:
        logger.warning(f"Verification query failed: {e}")

    logger.info("Model training completed successfully!")

if __name__ == "__main__":
    train_models()
