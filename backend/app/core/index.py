from elasticsearch import Elasticsearch
import logging

def create_elasticsearch_index(
    client: Elasticsearch,
    index_name: str,
    vector_dims: int = 3
) -> bool:
    """
    Crea un índice en Elasticsearch

    Args:
        client: Cliente de Elasticsearch
        index_name: Nombre del índice a crear
        vector_dims: Dimensión del vector denso (default: 3)

    Returns:
        bool: True si se creó el índice correctamente, False en caso contrario
    """
    try:
        if vector_dims <= 0:
            raise ValueError("La dimensión del vector debe ser mayor a 0")

        index_mapping = {
            "settings": {
                "analysis": {
                    "analyzer": {
                        "custom_text_analyzer": {
                            "type": "standard",
                            "stopwords": "_english_"
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
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            },
                            "suggestion": {
                                "type": "completion",
                                "analyzer": "custom_text_analyzer"
                            }
                        }
                    },
                    "author": {"type": "keyword"},
                    "publication_date": {"type": "date"},
                    "abstract": {"type": "text", "analyzer": "custom_text_analyzer"},
                    "keywords": {"type": "keyword"},
                    "content": {"type": "text", "analyzer": "custom_text_analyzer"},
                    "vector": {"type": "dense_vector", "dims": vector_dims}
                }
            }
        }

        if client.indices.exists(index=index_name):
            logging.warning(f"El índice '{index_name}' ya existe")
            return False

        client.indices.create(index=index_name, body=index_mapping)
        logging.info(f"Índice '{index_name}' creado exitosamente")
        return True

    except Exception as e:
        logging.error(f"Error al crear el índice: {str(e)}")
        return False
