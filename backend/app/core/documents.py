from elasticsearch import Elasticsearch
import logging
from typing import List
from .custom_search import fetch_custom_search_results, process_search_results
from .utils import extract_keywords

def index_document(client: Elasticsearch, index_name: str, document: dict) -> bool:
    """
    Indexes a document with keyword processing
    """
    try:
        # Extract keywords from title and content if not provided
        if not document.get('keywords'):
            text = f"{document.get('title', '')} {document.get('abstract', '')}"
            document['keywords'] = extract_keywords(text)
        
        # Add completion suggestion field
        document['title_completion'] = {
            "input": [document['title']] + document['keywords'],
            "weight": 1
        }
        
        response = client.index(index=index_name, document=document)
        logging.info(f"Document indexed: {response['_id']}")
        return True
    except Exception as e:
        logging.error(f"Error indexing document: {str(e)}")
        return False

async def fetch_and_index_new_documents(client: Elasticsearch, index_name: str, query: str) -> List[dict]:
    """
    Fetches and indexes new documents when no results are found.
    """
    try:
        raw_results = fetch_custom_search_results(query, num_results=10)
        documents = process_search_results(raw_results)
        
        indexed_documents = []
        for doc in documents:
            if index_document(client, index_name, doc):
                indexed_documents.append(doc)
                logging.info(f"Document '{doc['title']}' indexed successfully")
        
        return indexed_documents
    except Exception as e:
        logging.error(f"Error indexing new documents: {e}")
        return []