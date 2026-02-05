# Life Summarizer AI - Copilot Instructions

## Project Overview
**Life Summarizer AI** is a full-stack application enabling users to write daily journal entries and receive AI-generated summaries, sentiment analysis, and emotional trend visualization. The architecture separates concerns into three layers: Flask backend with NLP pipeline, React frontend with Recharts visualization, and encrypted data persistence.

## Architecture

### Backend (Flask + AI Pipeline)
- **Entry Point**: [`backend/app.py`](backend/app.py) - Flask server with CORS enabled, runs on `http://localhost:5000`
- **Data Flow**: User journal entry → text preprocessing → T5 summarization → TextBlob sentiment analysis → Fernet encryption → CSV storage
- **Key Endpoints**:
  - `POST /journal` - Processes new entries through AI pipeline, returns summary/sentiment/metrics
  - `GET /history` - Returns all journal entries (decrypted)
  - `GET /weekly-trends` - Aggregates daily sentiment scores into mood trends

### AI Logic Modules (`backend/ai_logic/`)
- **`summarizer.py`**: T5-small model for abstractive summarization. Key behavior: skips entries <30 words, uses `max_length=100`, `num_beams=4`, `length_penalty=2.0`
- **`sentiment.py`**: TextBlob polarity-based sentiment. Thresholds: >0.1 = Positive, <-0.1 = Negative, else = Neutral
- **`preprocess.py`**: Lowercase, whitespace normalization, special character removal
- **`security.py`**: Fernet encryption with auto-generated key in `data/secret.key`; handles encrypted CSV read/write

### Frontend (React + Recharts)
- **Entry Point**: [`frontend/my-app/src/App.js`](frontend/my-app/src/App.js) - Unified interface with live history and weekly mood chart
- **Visualization**: Recharts LineChart for 7-day trend (maps sentiment to numeric scores: Positive=1, Neutral=0, Negative=-1)
- **Note**: [`pages/Journal.js`](frontend/my-app/src/pages/Journal.js) exists but is unused; App.js handles all UI

## Data Flow & Integration Points

1. **Entry Submission** (App.js → Flask):
   - Frontend sends JSON: `{ entry: string }`
   - Backend returns: `{ summary, sentiment, polarity, original_length, summary_length, compression_ratio }`

2. **History Retrieval**: Decrypts stored CSV, returns full records with date, entry, summary, sentiment, polarity

3. **Weekly Aggregation**: Groups last 7 days by date, computes average mood score per day

## Development Workflow

### Running Backend
```bash
cd backend
python app.py  # Runs Flask debug server on :5000
```

### Running Frontend
```bash
cd frontend/my-app
npm start  # Runs dev server on :3000 with React scripts
```

### Key Dependencies
- **Core**: Flask, Pandas, PyTorch, Transformers (T5)
- **AI**: TextBlob (sentiment), cryptography (Fernet)
- **Frontend**: React 19, Recharts 3.6

## Project-Specific Patterns

### Model Loading Convention
T5 tokenizer and model are loaded once at module import time in `summarizer.py` (not per-request) to avoid repeated downloads. GPU/CPU auto-detection via `torch.device()`.

### Encryption Pattern
- Encryption is **transparent** in the pipeline; `decrypt_data()` handles both encrypted and plain CSV fallback
- Key generation is idempotent; rerunning code reuses existing `data/secret.key`

### State Management in Frontend
- Single `response` state for latest journal submission details
- Separate `history` (full records) and `weeklyTrends` (aggregated scores) states
- Sentiment color mapping utility (`getSentimentColor()`) centralizes UI conventions: green for positive, red for negative

## Critical Files for Understanding
- [backend/app.py](backend/app.py) - Complete Flask server & API contracts
- [backend/ai_logic/security.py](backend/ai_logic/security.py) - Encryption/decryption logic
- [frontend/my-app/src/App.js](frontend/my-app/src/App.js) - Frontend UI state and fetch patterns
- [requirements.txt](requirements.txt) - Python dependency versions

## Common Tasks

### Adding a New AI Feature
1. Create module in `backend/ai_logic/` (e.g., `emotion_detector.py`)
2. Import and call in `/journal` POST handler pipeline
3. Add response field to JSON return in `app.py`

### Modifying Sentiment Thresholds
Edit thresholds in `sentiment.py` (currently 0.1/-0.1). Update sentiment mapping in App.js weekly aggregation if logic changes.

### Changing Summarization Length
Modify `max_length` parameter in `summarizer.py` function call (currently 100).

## Known Limitations & Future Work
- No user authentication; all data stored locally
- Summarizer skips entries <30 words (intended behavior, prevents over-compression)
- Mobile/responsive design not implemented
- Weekly trends limited to 7-day window
