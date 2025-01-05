from elasticsearch import Elasticsearch
import logging
from typing import List
from .custom_search import fetch_custom_search_results, process_search_results
from .utils import extract_keywords

def index_document(client: Elasticsearch, index_name: str, document: dict) -> bool:
    """
    Indexa un documento con procesamiento de keywords
    """
    try:
        # Extraer keywords del título y contenido si no se proporcionan
        if not document.get('keywords'):
            text = f"{document.get('title', '')} {document.get('abstract', '')}"
            document['keywords'] = extract_keywords(text)
        
        # Agregar campo de completion suggestion
        document['title_completion'] = {
            "input": [document['title']] + document['keywords'],
            "weight": 1
        }
        
        response = client.index(index=index_name, document=document)
        logging.info(f"Documento indexado: {response['_id']}")
        return True
    except Exception as e:
        logging.error(f"Error al indexar documento: {str(e)}")
        return False

async def fetch_and_index_new_documents(client: Elasticsearch, index_name: str, query: str) -> List[dict]:
    """
    Busca y indexa nuevos documentos cuando no se encuentran resultados.
    """
    try:
        raw_results = fetch_custom_search_results(query, num_results=10)
        documents = process_search_results(raw_results)
        
        indexed_documents = []
        for doc in documents:
            if index_document(client, index_name, doc):
                indexed_documents.append(doc)
                logging.info(f"Documento '{doc['title']}' indexado correctamente")
        
        return indexed_documents
    except Exception as e:
        logging.error(f"Error al indexar nuevos documentos: {e}")
        return []
