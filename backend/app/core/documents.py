from elasticsearch import Elasticsearch
import logging
from typing import List
from core.custom_search import fetch_custom_search_results, process_search_results

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

async def fetch_and_index_new_documents(client, index_name: str, query: str) -> List[dict]:
    """
    Busca y indexa nuevos documentos cuando no se encuentran resultados.
    Retorna los nuevos documentos indexados.
    """
    try:
        # Buscar nuevos documentos
        raw_results = fetch_custom_search_results(query, num_results=5)
        documents = process_search_results(raw_results)
        
        # Indexar los nuevos documentos
        indexed_documents = []
        for doc in documents:
            if index_document(client, index_name, doc):
                indexed_documents.append(doc)
                print(f"Documento '{doc['title']}' indexado correctamente")
        
        return indexed_documents
    except Exception as e:
        print(f"Error al indexar nuevos documentos: {e}")
        return []