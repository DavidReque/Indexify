from core.index import create_elasticsearch_index
from core.client import get_client
import os
from dotenv import load_dotenv

load_dotenv()

def main ():
    client = get_client()
    index_name = os.getenv("INDEX_NAME"),

    # Crear el índice
    if create_elasticsearch_index(client, index_name, vector_dims=3):
        print(f"Índice '{index_name}' creado correctamente")

if __name__ == "__main__":
    main()