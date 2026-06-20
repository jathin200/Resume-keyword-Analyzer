# analyzer.py

import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

# Ensure you've run setup_nltk.py first

# This is the function that app.py is looking for.
# The name must match exactly.
def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None
    return text

# This is the second function app.py is looking for.
def extract_keywords(text):
    """Extracts keywords from a given text using NLTK."""
    if not text:
        return set()
        
    # Tokenize the text (split into words)
    words = word_tokenize(text.lower())
    
    # Remove punctuation
    words = [word for word in words if word.isalpha()]
    
    # Remove stopwords (common words like 'the', 'a', 'is')
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    # Lemmatization (reducing words to their base form, e.g., 'running' -> 'run')
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(word) for word in words]
    
    # Part-of-Speech (POS) tagging to identify nouns
    # Keywords are often nouns (NN, NNP, NNS)
    pos_tags = nltk.pos_tag(lemmas)
    
    keywords = {word for word, pos in pos_tags if pos.startswith('NN')}
    
    return keywords

# This is the third function app.py is looking for.
def compare_keywords(resume_keywords, jd_keywords):
    """Compares resume keywords against job description keywords."""
    if not jd_keywords:
        return {
            "score": 0,
            "matched_keywords": set(),
            "missing_keywords": set(),
        }
        
    matched_keywords = resume_keywords.intersection(jd_keywords)
    missing_keywords = jd_keywords.difference(resume_keywords)
    
    # Calculate score as a percentage of matched keywords from the job description
    score = (len(matched_keywords) / len(jd_keywords)) * 100 if len(jd_keywords) > 0 else 0
    
    return {
        "score": round(score, 2),
        "matched_keywords": sorted(list(matched_keywords)),
        "missing_keywords": sorted(list(missing_keywords)),
    }