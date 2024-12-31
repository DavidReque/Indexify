from core.index import create_elasticsearch_index
from core.client import get_client
from core.documents import index_document
from core.custom_search import fetch_custom_search_results, process_search_results
from core.custom_search import vector_text_search, advanced_search, generate_embedding
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    client = get_client()
    index_name = os.getenv("INDEX_NAME")

    # Crear el índice
    # if create_elasticsearch_index(client, index_name, vector_dims=384):
    #     print(f"Índice '{index_name}' creado correctamente")

    # Realizar la consulta
    query = "Quantum Computing"

    try:
        # raw_results = fetch_custom_search_results(query, num_results=5)
        # documents = process_search_results(raw_results)

        # # Indexar cada documento en Elasticsearch
        # for doc in documents:
        #     if index_document(client, index_name, doc):
        #         print(f"Documento '{doc['title']}' indexado correctamente")

        print("\n=== Pruebas de Búsqueda ===")
        
        # Búsqueda vectorial
        print("\nPrueba de búsqueda vectorial:")
        query_text = "cybersecurity attack prevention"
        query_vector = generate_embedding(query_text)
        
        results = vector_text_search(
            client=client,
            index_name=index_name,
            query_text=query_text,
            query_vector=query_vector,
            size=3
        )
        
        print(f"Resultados para '{query_text}':")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']} (Score: {result['score']:.2f})")

        print("\nPrueba de búsqueda avanzada:")
        advanced_results = advanced_search(
            client=client,
            index_name=index_name,
            content="Bitcoin",
            size=3
        )
        
        print("Resultados de búsqueda avanzada:")
        for i, result in enumerate(advanced_results, 1):
            print(f"{i}. {result['title']}")

        # Prueba de relevancia
        print("\nPrueba de relevancia temática:")
        topics = ["security", "bitcoin", "Quantum Computing"]
        
        for topic in topics:
            query_vector = generate_embedding(topic)
            results = vector_text_search(
                client=client,
                index_name=index_name,
                query_text=topic,
                query_vector=query_vector,
                size=1
            )
            
            if results:
                print(f"\nMejor resultado para '{topic}':")
                print(f"Título: {results[0]['title']}")
                print(f"Score: {results[0]['score']:.2f}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()