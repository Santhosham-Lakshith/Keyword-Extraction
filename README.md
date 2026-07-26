# KeyLens – NLP Keyword Extractor

A Flask web app that extracts top keywords from any text using **TF-IDF scoring**.  
Works out-of-the-box *without* a pre-trained model (built-in scratch TF-IDF), and upgrades automatically if you supply a `models/vectorizer.pkl`.

---

## Project Structure

```
keyword_extractor/
├── app.py                  # Flask app (improved)
├── train_vectorizer.py     # One-time script to build vectorizer.pkl
├── requirements.txt
├── models/
│   └── vectorizer.pkl      # (generated – optional)
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    └── js/main.js
```

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. (Optional) Train the vectorizer
```bash
python train_vectorizer.py
```
> If skipped, the app uses its built-in TF-IDF engine automatically.

### 3. Run the app
```bash
python app.py
```
Open **http://127.0.0.1:5000**

---

## Features

| Feature | Detail |
|---|---|
| **Dual engine** | Uses sklearn vectorizer if available, otherwise built-in TF-IDF |
| **Keyword scores** | TF-IDF score + frequency shown for every result |
| **Tag cloud** | Visual word cloud sized by relevance |
| **JSON API** | `POST /api/extract` for programmatic use |
| **Live stats** | Real-time char/word count as you type |
| **Responsive** | Mobile-friendly dark UI |

---

## API Usage

```bash
curl -X POST http://localhost:5000/api/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here...", "top_n": 10}'
```

Response:
```json
{
  "keywords": [
    {"word": "machine", "score": 0.412, "rank": 1, "frequency": 5}
  ],
  "count": 10,
  "method": "tfidf_scratch"
}
```

---

## Improvements Over Original

- **No model required** – built-in TF-IDF with sentence-level IDF works instantly
- **Richer output** – score, rank, and frequency for each keyword
- **JSON REST API** endpoint (`/api/extract`)
- **Input validation** with user-friendly error messages
- **Text statistics** – word count, character count, sentence count
- **Configurable `top_n`** from the UI (3–25 keywords)
- **Polished UI** – dark editorial design, animated bars, tag cloud, copy-on-click
