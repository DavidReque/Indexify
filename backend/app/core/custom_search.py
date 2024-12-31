import requests
import os
import numpy as np
import logging 
from elasticsearch import Elasticsearch
from typing import List, Dict, Any, Optional
from transformers import AutoTokenizer, AutoModel
import torch

model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def fetch_custom_search_results(query: str, num_results: int = 10) -> list[dict]:
    """
    Consulta la API de Google Custom Search JSON y obtiene resultados.

    Args:
        query: Consulta de búsqueda
        num_results: Número de resultados a obtener (máximo 10 por página)

    Returns:
        list[dict]: Lista de resultados con datos relevantes
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("SEARCH_ENGINE_ID")
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "q": query,
        "key": api_key,
        "cx": search_engine_id,
        "num": num_results
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("items", [])
        return results
    else:
        raise Exception(f"Error al consultar la API: {response.status_code}, {response.text}")
    
def generate_embedding(text: str) -> list[float]:
    """
    Genera un embedding para un texto dado utilizando Hugging Face.

    Args:
        text: El texto a procesar.

    Returns:
        list[float]: Embedding del texto como una lista de floats.
    """
    # Tokenizar el texto
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

    # Generar las representaciones del modelo
    with torch.no_grad():
        outputs = model(**inputs)

    # Extraer la representación del token [CLS]
    # Generalmente el embedding del token [CLS] (posición 0) es representativo del texto completo
    embedding = outputs.last_hidden_state[:, 0, :].squeeze().tolist()
    return embedding

def process_search_results(results: list[dict]) -> list[dict]:
    """
    Procesa los resultados de la API de Custom Search JSON y los prepara para Elasticsearch.
    Genera embeddings usando Hugging Face.

    Args:
        results: Lista de resultados crudos de la API.

    Returns:
        list[dict]: Lista de documentos procesados.
    """
    documents = []
    for item in results:
        # Texto combinado del título y el snippet
        text = f"{item.get('title', '')} {item.get('snippet', '')}".strip()

        # Generar el embedding utilizando Hugging Face
        vector = generate_embedding(text)

        # Crear el documento procesado
        documents.append({
            "title": item.get("title", ""),
            "author": "Google Search",
            "publication_date": None,
            "abstract": item.get("snippet", ""),
            "keywords": [],
            "content": item.get("link", ""),
            "vector": vector  # Vector generado por el modelo
        })
    return documents

def vector_text_search(
    client: Elasticsearch,
    index_name: str,
    query_text: str,
    query_vector: List[float],
    min_score: float = 0.1,
    size: int = 10
) -> List[Dict[str, Any]]:
    """
    Realiza una búsqueda combinada por texto y similitud de vectores.

    Args:
        client: Cliente de Elasticsearch
        index_name: Nombre del índice
        query_text: Texto para búsqueda
        query_vector: Vector de búsqueda
        min_score: Puntuación mínima para filtrar resultados
        size: Número máximo de resultados

    Returns:
        List[Dict]: Lista de documentos encontrados
    """
    try:
        query = {
            "size": size,
            "query": {
                "script_score": {
                    "query": {
                        "multi_match": {
                            "query": query_text,
                            "fields": ["title^3", "abstract^2", "content"],
                            "fuzziness": "AUTO"
                        }
                    },
                    "script": {
                        "source": """
                            cosineSimilarity(params.query_vector, 'vector') + 1.0 + 
                            (doc['keywords'].size() > 0 ? 0.5 : 0)
                        """,
                        "params": {"query_vector": query_vector}
                    }
                }
            }
        }

        response = client.search(index=index_name, body=query)
        
        results = []
        for hit in response['hits']['hits']:
            result = {
                'id': hit['_id'],
                'score': hit['_score'],
                'title': hit['_source'].get('title', ''),
                'abstract': hit['_source'].get('abstract', ''),
                'author': hit['_source'].get('author', ''),
                'publication_date': hit['_source'].get('publication_date'),
                'keywords': hit['_source'].get('keywords', []),
                'content': hit['_source'].get('content', '')
            }
            results.append(result)

        logging.info(f"Búsqueda completada. Encontrados {len(results)} resultados")
        return results

    except Exception as e:
        logging.error(f"Error en la búsqueda: {str(e)}")
        return []
    
def advanced_search(
    client: Elasticsearch,
    index_name: str,
    title: Optional[str] = None,
    author: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    keywords: Optional[List[str]] = None,
    content: Optional[str] = None,
    size: int = 10
) -> List[Dict[str, Any]]:
    """
    Realiza una búsqueda avanzada con múltiples criterios.

    Args:
        client: Cliente de Elasticsearch
        index_name: Nombre del índice
        title: Texto a buscar en el título
        author: Autor específico
        date_from: Fecha inicial (formato: YYYY-MM-DD)
        date_to: Fecha final (formato: YYYY-MM-DD)
        keywords: Lista de palabras clave
        content: Texto a buscar en el contenido
        size: Número máximo de resultados

    Returns:
        List[Dict]: Lista de documentos encontrados
    """
    try:
        must_conditions = []
        
        if title:
            must_conditions.append({
                "match": {
                    "title": {
                        "query": title,
                        "fuzziness": "AUTO"
                    }
                }
            })
            
        if author:
            must_conditions.append({
                "term": {
                    "author.keyword": author
                }
            })
            
        if date_from or date_to:
            must_conditions.append({
                "range": {
                    "publication_date": {
                        "gte": date_from,
                        "lte": date_to,
                        "format": "yyyy-MM-dd"
                    }
                }
            })
            
        if keywords:
            must_conditions.append({
                "terms": {
                    "keywords": keywords
                }
            })
            
        if content:
            must_conditions.append({
                "match": {
                    "content": {
                        "query": content,
                        "fuzziness": "AUTO"
                    }
                }
            })

        query = {
            "size": size,
            "query": {
                "bool": {
                    "must": must_conditions if must_conditions else [{"match_all": {}}]
                }
            },
            "sort": [
                {"_score": "desc"},
                {"publication_date": {"order": "desc", "missing": "_last"}}
            ]
        }

        response = client.search(index=index_name, body=query)
        
        results = []
        for hit in response['hits']['hits']:
            results.append(hit['_source'])

        logging.info(f"Búsqueda avanzada completada. Encontrados {len(results)} resultados")
        return results

    except Exception as e:
        logging.error(f"Error en la búsqueda avanzada: {str(e)}")
        return []