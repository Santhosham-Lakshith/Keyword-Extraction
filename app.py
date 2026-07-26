from flask import Flask, render_template, request, jsonify
import pickle
import os
import math
import re
from collections import Counter

app = Flask(__name__)

# ── Vectorizer (optional – only needed if a pre-trained .pkl is present) ──────
VECTORIZER_PATH = os.path.join("models", "vectorizer.pkl")
vectorizer = None
feature_names = []

if os.path.exists(VECTORIZER_PATH):
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    feature_names = vectorizer.get_feature_names_out()


# ── Improved fallback: TF-IDF from scratch ────────────────────────────────────
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "must", "can", "this", "that",
    "these", "those", "i", "you", "he", "she", "it", "we", "they", "me",
    "him", "her", "us", "them", "my", "your", "his", "its", "our", "their",
    "what", "which", "who", "whom", "when", "where", "why", "how", "all",
    "each", "every", "both", "few", "more", "most", "other", "some", "such",
    "no", "not", "only", "same", "so", "than", "too", "very", "just",
    "as", "if", "up", "about", "into", "through", "also", "any", "here",
    "there", "then", "now", "like", "well", "even", "back", "still",
    "way", "take", "get", "make", "go", "see", "come", "know", "think",
    "look", "want", "give", "use", "find", "tell", "ask", "seem", "feel",
    "try", "leave", "call", "keep", "let", "begin", "show", "hear", "play",
    "run", "move", "live", "believe", "hold", "bring", "happen", "write",
    "provide", "sit", "stand", "lose", "pay", "meet", "include", "continue",
    "set", "learn", "change", "lead", "understand", "watch", "follow", "stop",
    "create", "open", "appear", "turn", "speak", "read", "spend", "grow",
    "become", "need", "add", "form", "help", "start", "while", "since"
}


def tokenize(text: str) -> list[str]:
    """Lowercase, strip punctuation, remove stopwords & short tokens."""
    words = re.findall(r"[a-zA-Z']+", text.lower())
    return [w.strip("'") for w in words if len(w) > 2 and w not in STOPWORDS]


def compute_tfidf_scratch(text: str, top_n: int = 10) -> list[dict]:
    """
    Compute TF-IDF on a single document using itself as the corpus.
    For single-doc scenarios we boost rare (longer, more specific) terms.
    Returns list of {word, score, rank}.
    """
    tokens = tokenize(text)
    if not tokens:
        return []

    total = len(tokens)
    tf = {w: count / total for w, count in Counter(tokens).items()}

    # Treat each sentence as a mini-document for IDF
    sentences = re.split(r"[.!?;]+", text.lower())
    doc_count = max(len(sentences), 1)
    word_doc_freq = Counter()
    for sent in sentences:
        sent_words = set(tokenize(sent))
        word_doc_freq.update(sent_words)

    tfidf = {}
    for word, tf_score in tf.items():
        df = word_doc_freq.get(word, 1)
        idf = math.log((doc_count + 1) / (df + 1)) + 1
        tfidf[word] = tf_score * idf

    sorted_words = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)
    results = []
    for rank, (word, score) in enumerate(sorted_words[:top_n], 1):
        results.append({
            "word": word,
            "score": round(score, 4),
            "rank": rank,
            "frequency": Counter(tokens)[word]
        })
    return results


def extract_keywords_vectorizer(text: str, top_n: int = 10) -> list[dict]:
    """Use pre-trained sklearn TF-IDF vectorizer if available."""
    tfidf_vector = vectorizer.transform([text])
    scores = list(zip(feature_names, tfidf_vector.toarray()[0]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    results = []
    for rank, (word, score) in enumerate(sorted_scores, 1):
        if score > 0 and len(results) < top_n:
            results.append({
                "word": word,
                "score": round(float(score), 4),
                "rank": rank,
                "frequency": text.lower().count(word)
            })
    return results


def extract_keywords(text: str, top_n: int = 10) -> list[dict]:
    """Route to best available method."""
    if not text or not text.strip():
        return []
    if vectorizer:
        return extract_keywords_vectorizer(text, top_n)
    return compute_tfidf_scratch(text, top_n)


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    text = request.form.get("text", "").strip()
    top_n = int(request.form.get("top_n", 10))

    if not text:
        return render_template("index.html", error="Please enter some text.", text=text)

    keywords = extract_keywords(text, top_n=top_n)
    word_count = len(text.split())
    char_count = len(text)
    sentence_count = len(re.split(r"[.!?]+", text.strip()))

    return render_template(
        "index.html",
        keywords=keywords,
        text=text,
        word_count=word_count,
        char_count=char_count,
        sentence_count=sentence_count,
        top_n=top_n
    )


@app.route("/api/extract", methods=["POST"])
def api_extract():
    """JSON API endpoint for programmatic access."""
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()
    top_n = int(data.get("top_n", 10))

    if not text:
        return jsonify({"error": "No text provided"}), 400

    keywords = extract_keywords(text, top_n=top_n)
    return jsonify({
        "keywords": keywords,
        "count": len(keywords),
        "method": "vectorizer" if vectorizer else "tfidf_scratch"
    })


if __name__ == "__main__":
    app.run(debug=True)
