from elasticsearch import Elasticsearch
from typing import List, Dict, Any
import logging
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SearchSuggestion:
    text: str
    count: int
    trending: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "count": self.count,
            "trending": self.trending
        }

def update_search_stats(client: Elasticsearch, index_name: str, query: str):
    """
    Updates search statistics
    """
    try:
        stats_index = f"{index_name}_stats"
        now = datetime.utcnow()
        
        existing_stats = client.search(
            index=stats_index,
            body={
                "query": {"term": {"query.keyword": query.lower()}}
            }
        )

        if existing_stats['hits']['hits']:
            doc_id = existing_stats['hits']['hits'][0]['_id']
            current_count = existing_stats['hits']['hits'][0]['_source']['count']
            client.update(
                index=stats_index,
                id=doc_id,
                body={
                    "doc": {
                        "count": current_count + 1,
                        "last_searched": now,
                        "is_trending": current_count > 5
                    }
                }
            )
        else:
            client.index(
                index=stats_index,
                document={
                    "query": query.lower(),
                    "count": 1,
                    "last_searched": now,
                    "is_trending": False
                }
            )
    except Exception as e:
        logging.error(f"Error updating search statistics: {str(e)}")

def get_search_suggestions(
    client: Elasticsearch,
    index_name: str,
    query: str,
    size: int = 5
) -> List[SearchSuggestion]:
    """
    Retrieves suggestions based on title, keywords, and search statistics
    """
    try:
        # Search in search statistics
        stats_response = client.search(
            index=f"{index_name}_stats",
            body={
                "query": {
                    "prefix": {"query.keyword": query.lower()}
                },
                "sort": [{"count": "desc"}],
                "size": size
            }
        )

        suggestions = []
        seen_texts = set()

        # Add suggestions from statistics
        for hit in stats_response['hits']['hits']:
            source = hit['_source']
            if source['query'] not in seen_texts:
                suggestions.append(SearchSuggestion(
                    text=source['query'],
                    count=source['count'],
                    trending=source['is_trending']
                ))
                seen_texts.add(source['query'])

        # Fill with suggestions from titles and keywords
        if len(suggestions) < size:
            completion_response = client.search(
                index=index_name,
                body={
                    "query": {
                        "multi_match": {
                            "query": query,
                            "fields": ["title^3", "keywords.text"],  #
                            "type": "phrase_prefix"
                        }
                    },
                "size": size - len(suggestions)
    }
)

            for hit in completion_response['hits']['hits']:
                text = hit['_source']['title']
                if text not in seen_texts:
                    suggestions.append(SearchSuggestion(
                        text=text,
                        count=0,
                        trending=False
                    ))
                    seen_texts.add(text)

        return suggestions

    except Exception as e:
        logging.error(f"Error retrieving suggestions: {str(e)}")
        return []