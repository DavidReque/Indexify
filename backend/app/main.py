from core.index import create_elasticsearch_index
from core.client import get_client
from core.documents import index_document, process_search_results
from core.custom_search import fetch_custom_search_results
import os
from dotenv import load_dotenv

load_dotenv()

def main ():
    client = get_client()
    index_name = os.getenv("INDEX_NAME")

    # Crear el índice
    if create_elasticsearch_index(client, index_name, vector_dims=3):
        print(f"Índice '{index_name}' creado correctamente")

    # Realizar la consulta
    query = "ai papers"
    try:
        raw_results = fetch_custom_search_results(query, num_results=5)
        documents = process_search_results(raw_results)

         # Indexar cada documento en Elasticsearch
        for doc in documents:
            if index_document(client, index_name, doc):
                print(f"Documento '{doc['title']}' indexado correctamente")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()