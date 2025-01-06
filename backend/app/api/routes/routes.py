from fastapi import APIRouter, HTTPException
from core.models import SearchQuery, AdvancedSearchQuery
from core.client import get_client
import os
from dotenv import load_dotenv
from core.custom_search import vector_text_search, advanced_search, generate_embedding
from core.suggestions import update_search_stats, get_search_suggestions
from core.documents import fetch_and_index_new_documents

load_dotenv()

# Create the router with a prefix and tags
router = APIRouter(
    prefix="/api",
    tags=["search"]
)

@router.post("/search")
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
    
@router.get("/suggestions")
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
    
@router.post("/advanced-search")
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