from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
import ssl

load_dotenv()

def get_client() -> Elasticsearch:
    """
        Create an Elasticsearh client
    """
    return Elasticsearch(
        hosts=[os.getenv("ELASTICSEARCH_CLOUD_ID")],
        api_key=os.getenv("ELASTICSEARCH_API_KEY"),
        verify_certs=True,
        ssl_context=ssl.create_default_context()
    )