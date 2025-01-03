from elasticsearch import Elasticsearch
from typing import List, Dict
import logging

class SearchSuggestion:
    def __init__(self, text: str, count: int = 0, trending: bool = False):
        self.text = text
        self.count = count
        self.trending = trending

    def to_dict(self) -> Dict:
        return {
            "text": self.text,
            "count": self.count,
            "trending": self.trending
        }

def get_search_suggestions(
    client: Elasticsearch,
    index_name: str,
    query: str,
    max_suggestions: int = 5
) -> List[SearchSuggestion]:
    """
    Obtiene sugerencias de búsqueda usando prefix y fuzzy matching.
    """
    try:
        search_body = {
            "size": 0,
            "_source": False,
            "query": {
                "bool": {
                    "should": [
                        {
                            "prefix": {
                                "title.keyword": {
                                    "value": query,
                                    "boost": 2.0
                                }
                            }
                        },
                        {
                            "match": {
                                "title": {
                                    "query": query,
                                    "fuzziness": "AUTO",
                                    "operator": "and"
                                }
                            }
                        }
                    ]
                }
            },
            "aggs": {
                "suggestions": {
                    "terms": {
                        "field": "title.keyword",
                        "size": max_suggestions,
                        "min_doc_count": 1,
                        "order": {
                            "_count": "desc"
                        }
                    }
                }
            }
        }

        response = client.search(index=index_name, body=search_body)
        
        suggestions = []
        # Verifica si existen agregaciones en la respuesta
        if "aggregations" in response and "suggestions" in response["aggregations"]:
            for bucket in response["aggregations"]["suggestions"]["buckets"]:
                doc_count = bucket["doc_count"]
                is_trending = doc_count > 1
                
                suggestion = SearchSuggestion(
                    text=bucket["key"],
                    count=doc_count,
                    trending=is_trending
                )
                suggestions.append(suggestion)
                
            logging.info(f"Se encontraron {len(suggestions)} sugerencias para '{query}'")
        else:
            logging.warning(f"No se encontraron sugerencias para '{query}'")
            
        return suggestions

    except Exception as e:
        logging.error(f"Error al obtener sugerencias: {str(e)}")
        return []
