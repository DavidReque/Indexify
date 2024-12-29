from elasticsearch import Elasticsearch
import logging

def index_document(
    client: Elasticsearch,
    index_name: str,
    document: dict
) -> bool:
    """
    Indexa un documento en Elasticsearch.

    Args:
        client: Cliente de Elasticsearch
        index_name: Nombre del índice
        document: Documento a indexar

    Returns:
        bool: True si se indexó correctamente, False en caso contrario
    """
    try:
        response = client.index(index=index_name, document=document)
        logging.info(f"Documento indexado: {response['_id']}")
        return True
    except Exception as e:
        logging.error(f"Error al indexar documento: {str(e)}")
        return False

