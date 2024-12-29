from core.index import create_elasticsearch_index
from core.client import get_client
from core.documents import index_document
from core.custom_search import fetch_custom_search_results, process_search_results
from core.custom_search import vector_text_search, advanced_search
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    client = get_client()
    index_name = os.getenv("INDEX_NAME")

    # Crear el índice
    if create_elasticsearch_index(client, index_name, vector_dims=3):
        print(f"Índice '{index_name}' creado correctamente")

    # Realizar la consulta
    query = "quantum computing"

    try:
        raw_results = fetch_custom_search_results(query, num_results=5)
        documents = process_search_results(raw_results)

        # Indexar cada documento en Elasticsearch
        for doc in documents:
            if index_document(client, index_name, doc):
                print(f"Documento '{doc['title']}' indexado correctamente")

        query_text = "Papers With Code: The latest in Machine Learning"
        query_vector = [
            0.9247752018468114,
            0.8836068744467774,
            0.42019556281960824
        ]

        results = vector_text_search(
            client=client,
            index_name=index_name,
            query_text=query_text,
            query_vector=query_vector
        )

        for result in results:
            print(f"Documento: {result}")

        results = advanced_search(
            client=client,
            index_name=index_name,
            title="machine learning",
            author="Google Search", 
            date_from="2024-01-01",
            date_to="2024-12-31"
        )

        for result in results:
            print(f"Documento: {result}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()