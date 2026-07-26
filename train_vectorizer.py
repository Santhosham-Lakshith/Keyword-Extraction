"""
train_vectorizer.py
───────────────────
Run once to generate models/vectorizer.pkl from a sample corpus.
You can replace CORPUS with your own documents.

Usage:
    python train_vectorizer.py
"""

import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

CORPUS = [
    "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
    "Deep learning uses neural networks with many layers to model complex patterns in data.",
    "Natural language processing allows computers to understand and generate human language.",
    "Python is a versatile programming language widely used in data science and web development.",
    "Flask is a lightweight web framework for Python that is easy to use and extend.",
    "TF-IDF stands for term frequency-inverse document frequency, a popular text feature extraction method.",
    "Keyword extraction identifies the most relevant words or phrases in a document.",
    "Data science combines statistics, programming, and domain expertise to extract insights from data.",
    "Supervised learning algorithms learn from labeled training data to make predictions.",
    "Unsupervised learning discovers hidden patterns in data without predefined labels.",
    "Text classification assigns predefined categories to text documents using machine learning models.",
    "Named entity recognition identifies and classifies entities like names, organizations, and locations.",
    "Sentiment analysis determines the emotional tone of a piece of text.",
    "Word embeddings represent words as dense vectors in a continuous vector space.",
    "Transformers are a neural network architecture that has revolutionized natural language processing.",
    "Web scraping automates the extraction of data from websites using HTTP requests and HTML parsing.",
    "REST APIs allow different software applications to communicate over the internet using HTTP.",
    "Databases store and manage structured data for efficient retrieval and manipulation.",
    "Version control systems like Git track changes to source code over time.",
    "Cloud computing provides on-demand access to computing resources over the internet.",
]

os.makedirs("models", exist_ok=True)

vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words="english",
    ngram_range=(1, 2),
    min_df=1,
    sublinear_tf=True,
)
vectorizer.fit(CORPUS)

with open(os.path.join("models", "vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)

print(f"✓ Vectorizer trained on {len(CORPUS)} documents.")
print(f"  Vocabulary size: {len(vectorizer.vocabulary_)}")
print(f"  Saved to: models/vectorizer.pkl")
