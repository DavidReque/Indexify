from elasticsearch import Elasticsearch
from typing import Optional, Dict, Any
import logging

def create_elasticsearch_index(
    client: Elasticsearch,
    index_name: str,
    vector_dims: int = 3
) -> bool:
    """
    Crea un índice en Elasticsearch con un mapeo predefinido para artículos.

    Args:
        client: Cliente de Elasticsearch
        index_name: Nombre del índice a crear
        vector_dims: Dimensión del vector denso (default: 3)

    Returns:
        bool: True si se creó el índice correctamente, False en caso contrario
    """
    try:
        # Definir el mapeo del índice
        index_mapping = {
            "mappings": {
                "properties": {
                    "title": {
                        "type": "text",
                        "analyzer": "standard"
                    },
                    "author": {
                        "type": "keyword"
                    },
                    "publication_date": {
                        "type": "date"
                    },
                    "abstract": {
                        "type": "text",
                        "analyzer": "standard"
                    },
                    "keywords": {
                        "type": "keyword"
                    },
                    "content": {
                        "type": "text",
                        "analyzer": "standard"
                    },
                    "vector": {
                        "type": "dense_vector",
                        "dims": vector_dims
                    }
                }
            }
        }

        # Verificar si el índice ya existe
        if client.indices.exists(index=index_name):
            logging.warning(f"El índice '{index_name}' ya existe")
            return False

        # Crear el índice
        response = client.indices.create(
            index=index_name,
            body=index_mapping
        )
        
        logging.info(f"Índice '{index_name}' creado exitosamente")
        return True

    except Exception as e:
        logging.error(f"Error al crear el índice: {str(e)}")
        return False

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    import ssl
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Configurar el cliente
    client = Elasticsearch(
        hosts=[os.getenv("ELASTICSEARCH_CLOUD_ID")],
        api_key=os.getenv("ELASTICSEARCH_API_KEY"),
        verify_certs=True,
        ssl_context=ssl.create_default_context()
    )
    
    # Crear el índice
    success = create_elasticsearch_index(
        client=client,
        index_name=os.getenv("INDEX_NAME"),
        vector_dims=3
    )
    
    print("Índice creado exitosamente" if success else "Error al crear el índice")