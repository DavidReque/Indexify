from typing import List

def extract_keywords(text: str) -> List[str]:
    """
    Extrae keywords del texto usando técnicas básicas de NLP
    """
    words = text.lower().split()
    # Eliminar palabras comunes y cortas
    keywords = [word for word in words if len(word) > 3]
    return list(set(keywords))[:5]  # Limitamos a 5 keywords únicas
