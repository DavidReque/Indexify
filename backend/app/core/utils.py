from typing import List

def extract_keywords(text: str) -> List[str]:
    """
    Extract keywords text using basic NLP techniques
    """
    words = text.lower().split()
    # Delete common and short  words
    keywords = [word for word in words if len(word) > 3]
    return list(set(keywords))[:5]  # 5 unique keywords
