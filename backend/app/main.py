from core.index import create_elasticsearch_index
from core.client import get_client
from core.documents import index_document, fetch_and_index_new_documents
from core.custom_search import fetch_custom_search_results, process_search_results
from core.suggestions import get_search_suggestions, update_search_stats
from core.custom_search import vector_text_search, advanced_search, generate_embedding
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from typing import List, Optional

load_dotenv()

app = FastAPI()

origins = [
    os.getenv("FRONTEND_URL"),
    os.getenv("FRONTEND_URL_LOCAL"),
]

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Modelos Pydantic
class SearchQuery(BaseModel):
    query: str
    size: int = 10

class AdvancedSearchQuery(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    keywords: Optional[List[str]] = None
    content: Optional[str] = None
    size: int = 10

# Rutas
@app.get("/")
async def root():
    return {"message": "API running"}

@app.post("/api/search")
async def search(query: SearchQuery):
    try:
        client = get_client()
        index_name = os.getenv("INDEX_NAME")
        
        # Actualizar estadísticas de búsqueda
        update_search_stats(client, index_name, query.query)
        
        # Generar embedding para la consulta
        query_vector = generate_embedding(query.query)
        
        # Realizar búsqueda
        results = vector_text_search(
            client=client,
            index_name=index_name,
            query_text=query.query,
            query_vector=query_vector,
            size=query.size
        )
        
        if not results:
            new_documents = await fetch_and_index_new_documents(
                client, 
                index_name, 
                query.query
            )
            
            if new_documents:
                results = vector_text_search(
                    client=client,
                    index_name=index_name,
                    query_text=query.query,
                    query_vector=query_vector,
                    size=query.size
                )
        
        return {"results": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/suggestions")
async def get_suggestions(query: str):
    try:
        client = get_client()
        index_name = os.getenv("INDEX_NAME")
        
        suggestions = get_search_suggestions(
            client=client,
            index_name=index_name,
            query=query
        )
        
        return {
            "suggestions": [suggestion.to_dict() for suggestion in suggestions]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/advanced-search")
async def advanced_search_endpoint(query: AdvancedSearchQuery):
    try:
        client = get_client()
        index_name = os.getenv("INDEX_NAME")
        
        results = advanced_search(
            client=client,
            index_name=index_name,
            title=query.title,
            author=query.author,
            date_from=query.date_from,
            date_to=query.date_to,
            keywords=query.keywords,
            content=query.content,
            size=query.size
        )
        
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# def main():
#     client = get_client()
#     index_name = os.getenv("INDEX_NAME")

#     #Crear el índice
#     if create_elasticsearch_index(client, index_name, vector_dims=384):
#         print(f"Índice '{index_name}' creado correctamente")

    # #Realizar la consulta
    # query = "Quantum Computing"

    # try:
    #     raw_results = fetch_custom_search_results(query, num_results=5)
    #     documents = process_search_results(raw_results)

    #     # Indexar cada documento en Elasticsearch
    #     for doc in documents:
    #         if index_document(client, index_name, doc):
    #             print(f"Documento '{doc['title']}' indexado correctamente")

    #     print("\n=== Pruebas de Búsqueda ===")
        
    #     #Búsqueda vectorial
    #     print("\nPrueba de búsqueda vectorial:")
    #     query_text = "cybersecurity attack prevention"
    #     query_vector = generate_embedding(query_text)
        
    #     results = vector_text_search(
    #         client=client,
    #         index_name=index_name,
    #         query_text=query_text,
    #         query_vector=query_vector,
    #         size=3
    #     )
        
    #     print(f"Resultados para '{query_text}':")
    #     for i, result in enumerate(results, 1):
    #         print(f"{i}. {result['title']} (Score: {result['score']:.2f})")

    #     print("\nPrueba de búsqueda avanzada:")
    #     advanced_results = advanced_search(
    #         client=client,
    #         index_name=index_name,
    #         content="Bitcoin",
    #         size=3
    #     )
        
    #     print("Resultados de búsqueda avanzada:")
    #     for i, result in enumerate(advanced_results, 1):
    #         print(f"{i}. {result['title']}")

    #     #Prueba de relevancia
    #     print("\nPrueba de relevancia temática:")
    #     topics = ["security", "bitcoin", "Quantum Computing"]
        
    #     for topic in topics:
    #         query_vector = generate_embedding(topic)
    #         results = vector_text_search(
    #             client=client,
    #             index_name=index_name,
    #             query_text=topic,
    #             query_vector=query_vector,
    #             size=1
    #         )
            
    #         if results:
    #             print(f"\nMejor resultado para '{topic}':")
    #             print(f"Título: {results[0]['title']}")
    #             print(f"Score: {results[0]['score']:.2f}")

    # except Exception as e:
    #     print(f"Error: {e}")

# if __name__ == "__main__":
#     main()