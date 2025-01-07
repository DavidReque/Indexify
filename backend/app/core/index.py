from elasticsearch import Elasticsearch
import logging

def create_elasticsearch_index(client: Elasticsearch, index_name: str, vector_dims: int = 384) -> bool:
    """
    Create an index in Elasticsearch with support for suggestions and search counting
    """
    try:
        index_mapping = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "custom_text_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": ["lowercase", "stop", "snowball"]
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "title": {
                        "type": "text",
                        "analyzer": "custom_text_analyzer",
                        "fields": {
                            "keyword": {"type": "keyword"},
                            "completion": {
                                "type": "completion",
                                "analyzer": "custom_text_analyzer"
                            }
                        }
                    },
                    "author": {"type": "keyword"},
                    "publication_date": {"type": "date"},
                    "abstract": {"type": "text", "analyzer": "custom_text_analyzer"},
                    "keywords": {
                        "type": "keyword",
                        "fields": {
                            "text": {
                                "type": "text",
                                "analyzer": "custom_text_analyzer"
                            }
                        }
                    },
                    "content": {"type": "text", "analyzer": "custom_text_analyzer"},
                    "vector": {"type": "dense_vector", "dims": vector_dims},
                    "search_count": {"type": "long"}
                }
            }
        }

        if not client.indices.exists(index=index_name):
            client.indices.create(index=index_name, body=index_mapping)
            logging.info(f"Índice '{index_name}' successfully created")
            
            # Create index for statistics
            search_stats_mapping = {
                "mappings": {
                    "properties": {
                        "query": {"type": "keyword"},
                        "count": {"type": "long"},
                        "last_searched": {"type": "date"},
                        "is_trending": {"type": "boolean"}
                    }
                }
            }
            client.indices.create(index=f"{index_name}_stats", body=search_stats_mapping)
            return True
        return False

    except Exception as e:
        logging.error(f"Error creating index: {str(e)}")
        return False