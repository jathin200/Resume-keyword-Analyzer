# setup_nltk.py
import nltk

print("Downloading NLTK packages...")

# A comprehensive list of all required resources we've discovered.
packages = [
    'punkt',
    'punkt_tab', 
    'stopwords', 
    'averaged_perceptron_tagger',
    'averaged_perceptron_tagger_eng', # The specific one we just added
    'wordnet'
]

for package in packages:
    try:
        # A more robust check for different types of NLTK resources
        if nltk.data.find(f'tokenizers/{package}') or \
           nltk.data.find(f'corpora/{package}') or \
           nltk.data.find(f'taggers/{package}'):
            print(f"Package '{package}' already exists.")
    except LookupError:
        print(f"Downloading {package}...")
        nltk.download(package, quiet=True)

print("NLTK setup complete.")