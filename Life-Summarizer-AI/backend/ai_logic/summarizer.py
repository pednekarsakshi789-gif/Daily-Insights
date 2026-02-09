from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import nltk

# Download tokenizer data once
nltk.download("punkt")

def summarize_text(text: str, sentence_count: int = 3) -> str:
    """
    Generates an extractive summary using TextRank.
    Lightweight and free-tier friendly.
    """

    if not text or len(text.split()) < 30:
        return text

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()

    summary_sentences = summarizer(parser.document, sentence_count)

    summary = " ".join(str(sentence) for sentence in summary_sentences)
    return summary
