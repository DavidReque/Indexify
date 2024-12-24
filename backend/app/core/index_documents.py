import os
from elasticsearch import Elasticsearch, helpers
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Obtener las variables de entorno
elasticsearch_url = os.getenv("ELASTICSEARCH_CLOUD_ID")
elasticsearch_api_key = os.getenv("ELASTICSEARCH_API_KEY")
elasticsearch_index = os.getenv("INDEX_NAME")

# Conectar a Elasticsearch
client = Elasticsearch(
    elasticsearch_url,
    api_key=elasticsearch_api_key
)

index_name = elasticsearch_index
docs = [
    {
        "vector": [
            6.294,
            4.035,
            1.473
        ],
        "text": "Yellowstone National Park"
    },
    {
        "vector": [
            4.908,
            7.094,
            3.556
        ],
        "text": "Yosemite National Park"
    },
    {
        "vector": [
            9.692,
            2.295,
            7.824
        ],
        "text": "Rocky Mountain National Park"
    }
]

# Indexar documentos
bulk_response = helpers.bulk(client, docs, index=index_name)
print(bulk_response)

# Verificar los documentos indexados
search_response = client.search(index=index_name, body={"query": {"match_all": {}}})
print(search_response['hits']['hits'])