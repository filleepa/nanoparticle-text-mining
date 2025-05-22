"""Clean the text and prepare it for use in the model."""
import re, nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)
STOP = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    """Convert text to lowercase, strip punctuation, remove short/stop words."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    tokens = [t for t in text.split() if t not in STOP and len(t) > 3]
    return " ".join(tokens)

def add_clean_column(df):
    df["clean"] = (df["Title"]).fillna("") + " " + df["Abstract"].fillna("").map(clean_text)
    return df