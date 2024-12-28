import requests
import os

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
