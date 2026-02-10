"""
Lightweight text summarizer using TextRank (Sumy).
Free-tier friendly – no heavy ML models.
"""

import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

# Download tokenizer data once
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

def summarize_text(text: str, sentence_count: int = 3) -> str:
    """
    Generates an extractive summary using TextRank.
    Falls back gracefully for short inputs.
    """

    if not text:
        return ""

    # Skip summarization for very short text
    if len(text.split()) < 30:
        return text

    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = TextRankSummarizer()

        summary_sentences = summarizer(parser.document, sentence_count)

        summary = " ".join(str(sentence) for sentence in summary_sentences)
        return summary

    except Exception as e:
        # Fail-safe: return original text if summarization fails
        print("Summarization error:", e)
        return text
