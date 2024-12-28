from elasticsearch import Elasticsearch
import logging
import numpy as np

def index_document(
    client: Elasticsearch,
    index_name: str,
    document: dict
) -> bool:
    """
    Indexa un documento en Elasticsearch.

    Args:
        client: Cliente de Elasticsearch
        index_name: Nombre del índice
        document: Documento a indexar

    Returns:
        bool: True si se indexó correctamente, False en caso contrario
    """
    try:
        response = client.index(index=index_name, document=document)
        logging.info(f"Documento indexado: {response['_id']}")
        return True
    except Exception as e:
        logging.error(f"Error al indexar documento: {str(e)}")
        return False

def process_search_results(results: list[dict]) -> list[dict]:
    """
    Procesa los resultados de la API de Custom Search JSON y los prepara para Elasticsearch.
    Genera vectores aleatorios de ejemplo para cada documento.

    Args:
        results: Lista de resultados crudos de la API

    Returns:
        list[dict]: Lista de documentos procesados
    """
    documents = []
    for item in results:
        # Genera un vector aleatorio de 3 dimensiones como ejemplo
        # En un caso real, aquí utilizaríamos un modelo para generar los embeddings
        vector = np.random.rand(3).tolist()
        
        documents.append({
            "title": item.get("title", ""),
            "author": "Google Search",
            "publication_date": None,
            "abstract": item.get("snippet", ""),
            "keywords": [],
            "content": item.get("link", ""),
            "vector": vector  # Vector de 3 dimensiones
        })
    return documents
