import re
import pandas as pd


HOT_KEYWORDS = [
    "buy now",
    "purchase",
    "ready to buy",
    "payment",
    "pay now",
    "today",
    "immediately",
    "urgent",
    "book now",
    "sign up",
    "place order",
]

WARM_KEYWORDS = [
    "price",
    "pricing",
    "cost",
    "details",
    "interested",
    "demo",
    "quote",
    "quotation",
    "discount",
    "features",
    "more information",
    "call me",
]

COLD_KEYWORDS = [
    "just browsing",
    "not interested",
    "maybe later",
    "future",
    "just checking",
    "researching",
    "no requirement",
    "not now",
    "unsubscribe",
]


def clean_text(text):
    """Convert enquiry text into a normalized format."""

    if pd.isna(text):
        return ""

    text = str(text).lower()

    # Remove punctuation and special characters
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def count_keywords(text, keywords):
    """Count how many keywords appear in the enquiry."""

    return sum(1 for keyword in keywords if keyword in text)


def qualify_lead(enquiry):
    """Classify a lead as Hot, Warm, or Cold."""

    cleaned = clean_text(enquiry)

    hot_score = count_keywords(cleaned, HOT_KEYWORDS)
    warm_score = count_keywords(cleaned, WARM_KEYWORDS)
    cold_score = count_keywords(cleaned, COLD_KEYWORDS)

    highest_score = max(hot_score, warm_score, cold_score)

    # No keyword matches
    if highest_score == 0:
        qualification = "Cold"

    # Hot gets priority when tied
    elif hot_score == highest_score:
        qualification = "Hot"

    # Warm gets priority over Cold
    elif warm_score == highest_score:
        qualification = "Warm"

    else:
        qualification = "Cold"

    return {
        "cleaned_text": cleaned,
        "hot_score": hot_score,
        "warm_score": warm_score,
        "cold_score": cold_score,
        "qualification": qualification,
    }


if __name__ == "__main__":

    test_enquiry = "I am ready to buy today. Please send payment details."

    result = qualify_lead(test_enquiry)

    print("Original Enquiry:", test_enquiry)
    print("Cleaned Text:", result["cleaned_text"])
    print("Hot Score:", result["hot_score"])
    print("Warm Score:", result["warm_score"])
    print("Cold Score:", result["cold_score"])
    print("Qualification:", result["qualification"])